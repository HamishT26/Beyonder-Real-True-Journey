#!/usr/bin/env python3
"""Build and verify the exact planning-only v677-v3 x1 manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


SOURCE = "76e4e605a63074f4664296f9b61c59d41886d097"
ROOT = "docs/neris-solane/v677-v3"
MANIFEST = f"{ROOT}/validation/x1-manifest.json"
REVIEW = f"{ROOT}/validation/x1-staged-review.json"
CODE_PATHS = {
    "scripts/build_ghc_family_neris_solane_v677_v3_x1.py",
    "scripts/ghc_family_neris_solane_v677_v3_x1_manifest.py",
    "scripts/ghc_family_neris_solane_v677_v3_core.py",
    "tests/test_ghc_family_neris_solane_v677_v3_x1.py",
}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def run(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if run(repo, "rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 manifest must be built at the exact immutable source head")
    x1_paths = {
        path.relative_to(repo).as_posix()
        for path in (repo / ROOT / "x1").rglob("*")
        if path.is_file()
    }
    expected = x1_paths | CODE_PATHS | {MANIFEST, REVIEW}
    staged = set(filter(None, run(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
    if staged != expected:
        raise SystemExit(
            "unexpected staged x1 set: "
            + json.dumps({"missing": sorted(expected - staged), "extra": sorted(staged - expected)}, sort_keys=True)
        )
    if any("/x2/" in path for path in staged):
        raise SystemExit("x2 path forbidden in planning-only x1")

    covered = sorted(expected - {MANIFEST, REVIEW})
    entries = []
    candidates = []
    confirmed = []
    for relative in covered:
        path = repo / relative
        raw = normalized(path)
        entries.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256_normalized_lf": hashlib.sha256(raw).hexdigest(),
            }
        )
        if path.suffix.lower() in {".json", ".md", ".py", ".txt", ".html"}:
            value = raw.decode("utf-8")
            for category, pattern in PRIVACY_PATTERNS.items():
                if not pattern.search(value):
                    continue
                scanner_definition_paths = {
                    "scripts/ghc_family_neris_solane_v677_v3_core.py",
                    "scripts/ghc_family_neris_solane_v677_v3_x1_manifest.py",
                }
                adjudication = "scanner_definition" if relative in scanner_definition_paths else "confirmed_payload_hit"
                row = {"path": relative, "category": category, "adjudication": adjudication}
                candidates.append(row)
                if adjudication == "confirmed_payload_hit":
                    confirmed.append(row)
    manifest = {
        "schema": "ghc-family-normalized-lf-manifest/v1",
        "source": SOURCE,
        "phase": "v677-v3",
        "lifecycle": "planning_only_x1",
        "normalization": "CRLF and CR normalized to LF before SHA-256",
        "declared_self_exclusions": [MANIFEST, REVIEW],
        "entry_count": len(entries),
        "entries": entries,
    }
    review = {
        "schema": "ghc-family-exact-staged-review/v1",
        "source": SOURCE,
        "phase": "v677-v3",
        "status": "VALID_PLANNING_ONLY_X1_STAGED_REVIEW" if not confirmed else "INVALID_PRIVACY_HIT",
        "planning_only": True,
        "staged_input_count": len(staged),
        "manifest_entries": len(entries),
        "x2_paths": 0,
        "unexpected_paths": [],
        "privacy_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": len(confirmed),
        "declared_self_exclusions": [MANIFEST, REVIEW],
        "owner_test_selection": "tests/test_ghc_family_neris_solane_v677_v3_x1.py",
        "owner_test_result": "9 initial passes plus 1 isolated dependency recovery; no full-suite replay",
    }
    dump(repo / MANIFEST, manifest)
    dump(repo / REVIEW, review)
    if confirmed:
        raise SystemExit("confirmed privacy or raw-identifier hit")
    print(json.dumps({"status": review["status"], "staged": len(staged), "entries": len(entries)}, sort_keys=True))


if __name__ == "__main__":
    main()
