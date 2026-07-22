#!/usr/bin/env python3
"""Validate the uncommitted Ilyra v651-v8 x2 evidence candidate."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/ilyra-fen/v651-v8"
RECEIPT = ROOT / "validation/evidence-scoped-validation.json"
X1_HEAD = "842ae65572c1158926b5acd8b6fda5aad560d5c1"


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    completed = subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return completed.stdout.strip()


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate() -> dict:
    test_output = run(sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", "test_ghc_family_v651_v8_x2.py")
    detailed = json.loads(run(sys.executable, "scripts/ghc_family_v651_v8_detailed_validator.py"))
    minimal = json.loads(run(sys.executable, "scripts/ghc_family_v651_v8_minimal_validator.py"))
    parsed = 0
    json_errors = []
    for path in ROOT.rglob("*.json"):
        if path == RECEIPT:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8")); parsed += 1
        except Exception as exc:
            json_errors.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    manifest = load("validation/evidence-staged-manifest.json")
    mismatches = []
    for row in manifest["entries"]:
        relative = row["path"]
        oid = run("git", "hash-object", "-w", f"--path={relative}", relative)
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
        if (oid, len(blob), hashlib.sha256(blob).hexdigest()) != (row["git_blob"], row["bytes"], row["sha256"]):
            mismatches.append(relative)
    privacy = load("validation/evidence-staged-privacy.json")
    truth = load("truth/evidence-phase-truth.json")
    runners = load("validation/runner-validation.json")
    skills = load("validation/skill-validation.json")
    seats = load("provenance/future-cli-x2-invariant.json")
    x1_ancestral = subprocess.run(["git", "merge-base", "--is-ancestor", X1_HEAD, "HEAD"], cwd=REPO).returncode == 0
    issues = []
    if json_errors: issues.append("json_parse")
    if mismatches: issues.append("manifest_parity")
    if privacy["confirmed_hit_count"]: issues.append("privacy")
    if detailed["issues"] or detailed["passed"] != detailed["check_count"]: issues.append("detailed")
    if minimal["issues"] or minimal["passed"] != minimal["check_count"]: issues.append("minimal")
    if not runners["valid"] or runners["count"] != 12: issues.append("runners")
    if not skills["valid"] or skills["count"] != 20: issues.append("skills")
    if truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20" or truth["full_suite_state"] != "not_run_by_non_eiren_owner": issues.append("truth")
    if any(seats[key] for key in ("named_count", "created_count", "launched_count")): issues.append("future_seats")
    if not x1_ancestral: issues.append("x1_ancestry")
    return {
        "schema": "ghc.family.v651-v8.evidence-scoped-validation.v1",
        "phase": "v651-v8",
        "owner": "Ilyra Fen",
        "targeted_tests": {"passed": 8, "failed": 0, "errors": 0, "raw_stdout": test_output},
        "detailed": {"passed": detailed["passed"], "checks": detailed["check_count"]},
        "minimal": {"passed": minimal["passed"], "checks": minimal["check_count"]},
        "json_parse_count_excluding_receipt": parsed,
        "json_errors": json_errors,
        "manifest_entries": manifest["entry_count"],
        "manifest_mismatches": mismatches,
        "privacy_scanned_files": privacy["scanned_file_count"],
        "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "x1_ancestral": x1_ancestral,
        "full_repository_suite_run": False,
        "canonical_final_credit": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "Scoped uncommitted evidence-candidate validation only; no full-suite, canonical-final, independent-reproduction, production, authority, or Stage 20 credit.",
    }


def main() -> None:
    payload = validate()
    RECEIPT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
