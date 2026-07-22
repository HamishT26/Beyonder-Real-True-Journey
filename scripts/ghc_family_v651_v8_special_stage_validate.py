#!/usr/bin/env python3
"""Validate the exact staged surface for Ilyra v651-v8 special CLI prep."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = "docs/ilyra-fen/v651-v8-special-cli-prep/"
ALLOWED = (
    PHASE,
    "scripts/build_ghc_family_v651_v8_special_preregistration.py",
    "scripts/ghc_family_v651_v8_special_x1_validate.py",
    "scripts/ghc_family_v651_v8_special_manifest.py",
    "scripts/ghc_family_v651_v8_special_integrity.py",
    "scripts/ghc_family_v651_v8_special_stage_validate.py",
    "tests/test_ghc_family_v651_v8_special_x1.py",
)
ALLOWED_PREFIXES = (
    "scripts/build_ghc_family_v651_v8_special_",
    "scripts/ghc_family_v651_v8_special_",
    "tests/test_ghc_family_v651_v8_special_",
)
PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "private_local_path": re.compile(r"(?i)(?:[a-z]:\\users\\|/users/|/home/)[^\s\"'<>]+"),
    "delegation_markup": re.compile(r"(?i)<\s*/?\s*codex_delegation\b"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|file)://[^\s\"'<>]+"),
    "credential_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|password|private[_-]?key|client[_-]?secret)\s*[:=]\s*[^\s,;}]+"
    ),
}
SCANNER_DEFINITIONS = {
    "scripts/ghc_family_v651_v8_special_closeout_validate.py",
    "scripts/ghc_family_v651_v8_special_evidence_validate.py",
    "scripts/ghc_family_v651_v8_special_integrity.py",
    "scripts/ghc_family_v651_v8_special_stage_validate.py",
    "scripts/ghc_family_v651_v8_special_terminal_validate.py",
}


def run(*args: str, binary: bool = False):
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=not binary, encoding=None if binary else "utf-8"
    ).stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--mode", choices=("x1", "evidence", "final"), required=True)
    args = parser.parse_args()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output_rel = output.relative_to(ROOT).as_posix()
    staged = sorted(filter(None, run("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()))
    if output_rel not in staged and output.exists():
        staged.append(output_rel)
        staged.sort()
    out_of_scope = [
        path
        for path in staged
        if not (path.startswith(PHASE) or path in ALLOWED or any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES))
    ]
    x2_markers = ("/x2-", "/evidence/", "/closeout/", "/seal/", "/final/")
    x2_in_x1 = [path for path in staged if args.mode == "x1" and any(marker in path.lower() for marker in x2_markers)]
    privacy_hits = []
    definition_exclusions = []
    for relative in staged:
        if relative == output_rel:
            continue
        if relative in SCANNER_DEFINITIONS:
            definition_exclusions.append(relative)
            continue
        try:
            raw = run("show", f":{relative}", binary=True)
            text = raw.decode("utf-8")
        except (subprocess.CalledProcessError, UnicodeDecodeError):
            continue
        for name, pattern in PATTERNS.items():
            count = len(pattern.findall(text))
            if count:
                privacy_hits.append({"path": relative, "class": name, "count": count})
    issues = [
        *[f"out_of_scope:{path}" for path in out_of_scope],
        *[f"x2_in_x1:{path}" for path in x2_in_x1],
        *[f"privacy_hit:{row['class']}:{row['path']}" for row in privacy_hits],
    ]
    payload = {
        "schema": "ghc.family.v651-v8-special.staged-review.v1",
        "phase": "v651-v8-special-cli-prep",
        "mode": args.mode,
        "staged_file_count": len(staged),
        "staged_files": staged,
        "out_of_scope": out_of_scope,
        "x2_paths_in_x1": x2_in_x1,
        "privacy_pattern_classes": sorted(PATTERNS),
        "scanner_definition_exclusions": sorted(definition_exclusions),
        "confirmed_privacy_hits": privacy_hits,
        "issues": issues,
        "valid": not issues,
        "boundary": "Scanner definition files are reviewed as code, not misclassified as private payload. Zero confirmed hits are bounded evidence only.",
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": not issues, "staged": len(staged), "issues": len(issues)}))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
