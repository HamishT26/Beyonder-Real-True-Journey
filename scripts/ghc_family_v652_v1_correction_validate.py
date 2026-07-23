#!/usr/bin/env python3
"""Validate Sable Rook's staged v652-v1 terminal correction without final credit."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sable-rook/v652-v1"
RECEIPT = ROOT / "validation/correction-precommit-validation.json"
CLOSEOUT_HEAD = "67ea89adf25dc958c757123501cf43f62f461e2f"


def completed(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    return subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)


def run(*args: str) -> str:
    return completed(*args).stdout.strip()


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def staged_blob(relative: str) -> tuple[str, bytes]:
    line = run("git", "ls-files", "-s", "--", relative)
    if not line:
        return "", b""
    oid = line.split()[1]
    return oid, subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)


def verify_manifest(relative: str) -> tuple[list[str], int]:
    manifest = load(relative)
    mismatches = []
    for row in manifest["entries"]:
        oid, blob = staged_blob(row["path"])
        if (oid, len(blob), hashlib.sha256(blob).hexdigest()) != (row["git_blob"], row["bytes"], row["sha256"]):
            mismatches.append(row["path"])
    return mismatches, manifest["entry_count"]


def test_count(pattern: str) -> tuple[int, str]:
    result = completed(sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", pattern)
    text = (result.stdout + "\n" + result.stderr).strip()
    match = re.search(r"Ran\s+(\d+)\s+tests?", text)
    return (int(match.group(1)) if match else 0), text


def validate() -> dict:
    test_rows = []
    test_total = 0
    for pattern in ("test_ghc_family_v652_v1_x2.py", "test_ghc_family_v652_v1_closeout.py"):
        count, raw = test_count(pattern)
        test_rows.append({"pattern": pattern, "passed": count, "raw_output": raw})
        test_total += count
    detailed = json.loads(run(sys.executable, "-B", "scripts/ghc_family_v652_v1_detailed_validator.py"))
    minimal = json.loads(run(sys.executable, "-B", "scripts/ghc_family_v652_v1_minimal_validator.py"))
    json_errors = []
    parsed = 0
    for path in sorted(ROOT.rglob("*.json")):
        if path == RECEIPT:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            parsed += 1
        except Exception as exc:
            json_errors.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    owner = load("validation/correction-owner-manifest.json")
    delta = load("validation/correction-delta-manifest.json")
    owner_mismatches, owner_entries = verify_manifest("validation/correction-owner-manifest.json")
    delta_mismatches, delta_entries = verify_manifest("validation/correction-delta-manifest.json")
    staged_paths = set(run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines())
    expected_delta = {row["path"] for row in delta["entries"]} | set(delta["self_exclusions"])
    truth = load("final/phase-truth.json")
    route = load("route/final-route-state.json")
    privacy = load("validation/correction-staged-privacy.json")
    method = load("method-flow/method-flow-summary.json")
    cap = load("final/commit-cap-contract.json")
    checks = {
        "eligible_tests": test_total == 15,
        "detailed": detailed["passed"] == detailed["check_count"] and not detailed["issues"],
        "minimal": minimal["passed"] == minimal["check_count"] and not minimal["issues"],
        "json": not json_errors,
        "owner_manifest": not owner_mismatches and owner["owner_path_count"] == owner["entry_count"] + owner["self_exclusion_count"],
        "delta_manifest": not delta_mismatches and delta["delta_path_count"] == delta["entry_count"] + delta["self_exclusion_count"],
        "exact_staged_surface": staged_paths == expected_delta,
        "privacy": privacy["confirmed_hit_count"] == 0,
        "truth": truth["effective_negatives"] == 8021,
        "method_flow": method["counts"]["methods"] == 12 and method["counts"]["witness_results"] == {"fail": 17, "pass": 15},
        "commit_cap": cap["planned_phase_total"] == 4 and cap["maximum"] == 6,
        "route_held": route["delivery_state"] == "PREPARED_NOT_SENT" and route["messages_sent"] == 0,
        "expected_parent": run("git", "rev-parse", "HEAD") == CLOSEOUT_HEAD and delta["parent"] == CLOSEOUT_HEAD,
        "diff_hygiene": completed("git", "diff", "--cached", "--check").stdout.strip() == "",
    }
    issues = [name for name, passed in checks.items() if not passed]
    return {"schema": "ghc.family.v652-v1.correction-precommit-validation.v1", "phase": "v652-v1", "owner": "Sable Rook", "eligible_tests": {"passed": test_total, "failed": 0, "errors": 0, "selections": test_rows}, "detailed": {"passed": detailed["passed"], "checks": detailed["check_count"]}, "minimal": {"passed": minimal["passed"], "checks": minimal["check_count"]}, "json_parse_count_excluding_receipt": parsed, "json_errors": json_errors, "owner_manifest_entries": owner_entries, "owner_manifest_mismatches": owner_mismatches, "delta_manifest_entries": delta_entries, "delta_manifest_mismatches": delta_mismatches, "staged_path_count": len(staged_paths), "expected_staged_path_count": len(expected_delta), "privacy_scanned_files": privacy["scanned_file_count"], "privacy_confirmed_hits": privacy["confirmed_hit_count"], "failed_canonical_attempts_retained": 1, "successful_canonical_passes": 0, "full_repository_suite_run": False, "canonical_final_credit": False, "same_owner_only": True, "checks": checks, "issue_count": len(issues), "issues": issues, "valid": not issues, "boundary": "Staged additive correction validation only; the single successful exact-final canonical pass remains pending."}


def main() -> None:
    payload = validate()
    RECEIPT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
