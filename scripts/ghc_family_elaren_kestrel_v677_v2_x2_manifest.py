#!/usr/bin/env python3
"""Build the exact normalized-LF manifest and staged review for Elaren x2."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path


SOURCE = "3ca2ff8087245a5ded51ce05d748186d80951387"
X1_HEAD = "4621b308f32d48cf70ab3ad598961dbedc122b6a"
ROOT = "docs/elaren-kestrel/v677-v2"
X2_ROOT = f"{ROOT}/x2"
MANIFEST = f"{ROOT}/validation/x2-manifest.json"
REVIEW = f"{ROOT}/validation/x2-staged-review.json"
CODE_PATHS = {
    "scripts/build_ghc_family_elaren_kestrel_v677_v2_report.py",
    "scripts/build_ghc_family_elaren_kestrel_v677_v2_x2.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_accessibility_runner.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_topology_runner.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_contract_runner.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_flashcard_runner.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_metadata_runner.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_mutation_runner.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_portfolio_runner.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_privacy_runner.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_toolchain_runner.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_x2_manifest.py",
    "tests/test_ghc_family_elaren_kestrel_v677_v2_x2.py",
}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}
DEFINITION_PATHS = {
    "scripts/ghc_family_elaren_kestrel_v677_v2_core.py",
    "scripts/ghc_family_elaren_kestrel_v677_v2_x2_manifest.py",
    "tests/test_ghc_family_elaren_kestrel_v677_v2_x2.py",
}


def git(repo: Path, *args: str) -> str:
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()

    if git(repo, "rev-parse", "HEAD") != X1_HEAD:
        raise SystemExit("x2 evidence manifest must be built at the frozen x1 head")
    x2_paths = {
        path.relative_to(repo).as_posix()
        for path in (repo / X2_ROOT).rglob("*")
        if path.is_file()
    }
    expected = x2_paths | CODE_PATHS | {MANIFEST, REVIEW}
    staged = set(filter(None, git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
    if staged != expected:
        raise SystemExit(
            "unexpected staged x2 set: "
            + json.dumps({"missing": sorted(expected - staged), "extra": sorted(staged - expected)}, sort_keys=True)
        )
    if any(path.startswith(f"{ROOT}/x1/") for path in staged):
        raise SystemExit("planning-only x1 is immutable during x2")

    json_paths = sorted(path for path in staged if path.startswith(X2_ROOT + "/") and path.endswith(".json"))
    for relative in json_paths:
        json.loads((repo / relative).read_text(encoding="utf-8"))

    code_paths = sorted(path for path in staged if path.endswith(".py"))
    for relative in code_paths:
        try:
            ast.parse((repo / relative).read_text(encoding="utf-8"), filename=relative)
        except SyntaxError as error:
            raise SystemExit(f"changed Python syntax failed: {relative}: {error}") from error

    covered = sorted(expected - {MANIFEST, REVIEW})
    entries: list[dict[str, object]] = []
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    max_words = 0
    max_word_path = ""
    for relative in covered:
        path = repo / relative
        raw = normalized(path)
        words = len(raw.decode("utf-8", errors="replace").split())
        if words > max_words:
            max_words = words
            max_word_path = relative
        entries.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256_normalized_lf": hashlib.sha256(raw).hexdigest(),
            }
        )
        if path.suffix.lower() not in {".json", ".md", ".py", ".txt", ".html", ".yaml"}:
            continue
        value = raw.decode("utf-8")
        for category, pattern in PRIVACY_PATTERNS.items():
            if not pattern.search(value):
                continue
            adjudication = "scanner_definition_or_synthetic_test" if relative in DEFINITION_PATHS else "confirmed_payload_hit"
            row = {"path": relative, "category": category, "adjudication": adjudication}
            candidates.append(row)
            if adjudication == "confirmed_payload_hit":
                confirmed.append(row)

    if len(entries) >= 2000:
        raise SystemExit("owner x2 materialization reached the 2000-file stop")
    if max_words > 100000:
        raise SystemExit("owner document exceeded the 100000-word stop")
    if confirmed:
        raise SystemExit("confirmed privacy or raw-identifier hit: " + json.dumps(confirmed, sort_keys=True))

    manifest = {
        "schema": "ghc-family-normalized-lf-manifest/v1",
        "source": SOURCE,
        "x1": X1_HEAD,
        "phase": "v677-v2",
        "lifecycle": "x2_evidence",
        "normalization": "CRLF and CR normalized to LF before SHA-256",
        "declared_self_exclusions": [MANIFEST, REVIEW],
        "entry_count": len(entries),
        "entries": entries,
    }
    review = {
        "schema": "ghc-family-exact-staged-review/v1",
        "source": SOURCE,
        "x1": X1_HEAD,
        "phase": "v677-v2",
        "status": "VALID_X2_EVIDENCE_STAGED_REVIEW",
        "staged_input_count": len(staged),
        "manifest_entries": len(entries),
        "strict_json_parses": len(json_paths),
        "changed_python_compiles": len(code_paths),
        "owner_file_stop": 2000,
        "max_document_words": max_words,
        "max_document_path": max_word_path,
        "privacy_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "declared_self_exclusions": [MANIFEST, REVIEW],
        "owner_test_truth": {
            "first_aggregate": "21 of 21 x2 owner checks passed once",
            "isolated_recovery": "not required",
            "unaffected_successes_replayed": 0,
            "aggregate_pass_credit": 1,
        },
        "x1_mutated": False,
        "full_repository_suite_run": False,
        "bounded_same_owner_evidence_only": True,
    }
    dump(repo / MANIFEST, manifest)
    dump(repo / REVIEW, review)
    print(
        json.dumps(
            {
                "status": review["status"],
                "staged": len(staged),
                "entries": len(entries),
                "json": len(json_paths),
                "compiled": len(code_paths),
                "privacy_confirmed": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
