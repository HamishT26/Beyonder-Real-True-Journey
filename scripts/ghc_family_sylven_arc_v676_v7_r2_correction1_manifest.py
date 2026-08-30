#!/usr/bin/env python3
"""Build the exact staged manifest for the first additive correction."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


FAILED_FINAL = "cee57870903bdb12dd908623bf29a49b63cc464e"
ROOT = "docs/sylven-arc/v676-v7-r2/correction1"
MANIFEST = f"{ROOT}/delta-manifest.json"
REVIEW = f"{ROOT}/staged-review.json"
EXPECTED = {
    f"{ROOT}/correction-truth.json",
    f"{ROOT}/failed-canonical-retention.json",
    MANIFEST,
    REVIEW,
    "scripts/ghc_family_sylven_arc_v676_v7_r2_correction1_composite.py",
    "scripts/ghc_family_sylven_arc_v676_v7_r2_correction1_manifest.py",
    "tests/test_ghc_family_sylven_arc_v676_v7_r2_final.py",
}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
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
    if git(repo, "rev-parse", "HEAD") != FAILED_FINAL:
        raise SystemExit("correction1 manifest must run at the retained failed canonical final")
    staged = set(filter(None, git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
    if staged != EXPECTED:
        raise SystemExit(
            "unexpected correction1 staged set: "
            + json.dumps({"missing": sorted(EXPECTED - staged), "extra": sorted(staged - EXPECTED)}, sort_keys=True)
        )
    if any("/x1/" in path or "/x2/" in path or "/final/" in path for path in staged):
        raise SystemExit("immutable lifecycle content cannot be modified by correction1")

    json_paths = sorted(path for path in staged if path.endswith(".json"))
    for relative in json_paths:
        json.loads((repo / relative).read_text(encoding="utf-8"))
    python_paths = sorted(path for path in staged if path.endswith(".py"))
    compile_result = subprocess.run(
        ["python", "-m", "py_compile", *(str(repo / path) for path in python_paths)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    if compile_result.returncode != 0:
        raise SystemExit("correction1 Python compile failed: " + compile_result.stderr)

    entries = []
    candidates = []
    confirmed = []
    for relative in sorted(staged - {MANIFEST, REVIEW}):
        raw = normalized(repo / relative)
        entries.append(
            {
                "path": relative,
                "bytes": (repo / relative).stat().st_size,
                "sha256_normalized_lf": hashlib.sha256(raw).hexdigest(),
            }
        )
        if Path(relative).suffix.lower() not in {".json", ".py", ".md", ".txt"}:
            continue
        text = raw.decode("utf-8")
        for category, pattern in PRIVACY_PATTERNS.items():
            if not pattern.search(text):
                continue
            adjudication = "scanner_definition_or_synthetic_test" if relative.endswith("_manifest.py") or relative.startswith("tests/") else "confirmed_payload_hit"
            row = {"path": relative, "category": category, "adjudication": adjudication}
            candidates.append(row)
            if adjudication == "confirmed_payload_hit":
                confirmed.append(row)
    if confirmed:
        raise SystemExit("confirmed correction1 privacy hit: " + json.dumps(confirmed, sort_keys=True))

    dump(
        repo / MANIFEST,
        {
            "schema": "ghc-family-normalized-lf-manifest/v1",
            "phase": "v676-v7-r2-correction1",
            "parent_failed_final": FAILED_FINAL,
            "normalization": "CRLF and CR normalized to LF before SHA-256",
            "declared_self_exclusions": [MANIFEST, REVIEW],
            "entry_count": len(entries),
            "entries": entries,
        },
    )
    dump(
        repo / REVIEW,
        {
            "schema": "ghc-family-additive-correction-staged-review/v1",
            "status": "VALID_CORRECTION1_STAGED_REVIEW",
            "phase": "v676-v7-r2-correction1",
            "parent_failed_final": FAILED_FINAL,
            "staged_input_count": len(staged),
            "manifest_entries": len(entries),
            "strict_json_parses": len(json_paths),
            "changed_python_compiles": len(python_paths),
            "privacy_candidates": candidates,
            "confirmed_privacy_or_raw_identifier_hits": 0,
            "failed_canonical_success_credit": 0,
            "retained_passing_owner_test_observations": 19,
            "isolated_failed_dependency": "test_baton_is_sanitized_prepared_state_not_delivery",
            "isolated_test_run_precommit": False,
            "full_repository_suite_run": False,
        },
    )
    print(
        json.dumps(
            {
                "status": "VALID_CORRECTION1_STAGED_REVIEW",
                "staged": len(staged),
                "entries": len(entries),
                "json": len(json_paths),
                "compiled": len(python_paths),
                "privacy_confirmed": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
