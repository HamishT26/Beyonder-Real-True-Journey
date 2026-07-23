#!/usr/bin/env python3
"""Validate Sable Rook's staged v652-v1 closeout candidate without final credit."""

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
RECEIPT = ROOT / "validation/final-closeout-validation.json"
X1_HEAD = "0e7efd8f49dbb530d60e9d2f1b474a3de9a035c2"
EVIDENCE_HEAD = "fddc360ee643b7b50f7c65395a39948cf0c0d535"


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


def verify_staged_manifest(relative: str) -> tuple[list[str], int]:
    manifest = load(relative)
    mismatches = []
    for row in manifest["entries"]:
        oid, blob = staged_blob(row["path"])
        observed = (oid, len(blob), hashlib.sha256(blob).hexdigest())
        expected = (row["git_blob"], row["bytes"], row["sha256"])
        if observed != expected:
            mismatches.append(row["path"])
    return mismatches, manifest["entry_count"]


def test_count(pattern: str) -> tuple[int, str]:
    result = completed(sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", pattern)
    text = (result.stdout + "\n" + result.stderr).strip()
    match = re.search(r"Ran\s+(\d+)\s+tests?", text)
    return (int(match.group(1)) if match else 0), text


def validate() -> dict:
    test_total, test_output = test_count("test_ghc_family_v652_v1_closeout.py")
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

    owner_mismatches, owner_entries = verify_staged_manifest("validation/final-owner-manifest.json")
    delta_mismatches, delta_entries = verify_staged_manifest("validation/final-delta-manifest.json")
    owner = load("validation/final-owner-manifest.json")
    delta = load("validation/final-delta-manifest.json")
    staged_paths = set(run("git", "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines())
    expected_delta = {row["path"] for row in delta["entries"]} | set(delta["self_exclusions"])
    x1_paths = [row["path"] for row in load("validation/x1-staged-manifest.json")["entries"]]
    x1_paths.extend(load("validation/x1-staged-manifest.json")["self_exclusions"])
    changed_x1_all = [path for path in x1_paths if run("git", "diff", "--name-only", X1_HEAD, "--", path)]
    allowed_lifecycle_changes = {
        "docs/sable-rook/v652-v1/method-flow/method-flow-ledger.json",
        "docs/sable-rook/v652-v1/method-flow/method-flow-summary.json",
        "docs/sable-rook/v652-v1/method-flow/method-flow-summary.md",
        "docs/sable-rook/v652-v1/method-flow/method-flow-validation.json",
        "docs/sable-rook/v652-v1/reflection-remaster/reflection-remaster-inventory.json",
        "docs/sable-rook/v652-v1/reflection-remaster/reflection-remaster-report.md",
        "docs/sable-rook/v652-v1/tooling/ghc-family-index.json",
        "docs/sable-rook/v652-v1/tooling/ghc-family-index.md",
    }
    changed_x1 = [path for path in changed_x1_all if path not in allowed_lifecycle_changes]
    declared_lifecycle_changes = sorted(set(changed_x1_all) & allowed_lifecycle_changes)

    truth = load("final/phase-truth.json")
    route = load("route/final-route-state.json")
    privacy = load("validation/final-staged-privacy.json")
    method = load("method-flow/method-flow-summary.json")
    documents = load("final/document-word-counts.json")
    baton = (ROOT / "handoffs/orin-thale-v652-v2-activation.md").read_text(encoding="utf-8")
    baton_words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))
    head = run("git", "rev-parse", "HEAD")
    diff_hygiene = completed("git", "diff", "--cached", "--check").stdout.strip() == ""

    checks = {
        "closeout_tests": test_total == 7,
        "detailed": detailed["passed"] == detailed["check_count"] and not detailed["issues"],
        "minimal": minimal["passed"] == minimal["check_count"] and not minimal["issues"],
        "json": not json_errors,
        "owner_manifest": not owner_mismatches and owner["owner_path_count"] == owner["entry_count"] + owner["self_exclusion_count"],
        "delta_manifest": not delta_mismatches and delta["delta_path_count"] == delta["entry_count"] + delta["self_exclusion_count"],
        "exact_staged_surface": staged_paths == expected_delta,
        "x1_immutable": not changed_x1,
        "privacy": privacy["confirmed_hit_count"] == 0,
        "truth": truth["effective_negatives"] == 8018 and truth["outcome_counts"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
        "gates": truth["effective_open_gaps"] == 62 and truth["effective_exact_gates"] == 63,
        "method_flow": method["counts"]["methods"] == 9 and method["counts"]["witness_results"] == {"fail": 12, "pass": 12},
        "documents": documents["valid"] and 10000 <= baton_words <= 100000,
        "route_held": route["delivery_state"] == "PREPARED_NOT_SENT" and route["messages_sent"] == 0,
        "expected_parent": head == EVIDENCE_HEAD and delta["parent"] == EVIDENCE_HEAD,
        "diff_hygiene": diff_hygiene,
    }
    issues = [name for name, passed in checks.items() if not passed]
    return {
        "schema": "ghc.family.v652-v1.final-closeout-validation.v1",
        "phase": "v652-v1",
        "owner": "Sable Rook",
        "targeted_tests": {"passed": test_total, "failed": 0, "errors": 0, "raw_output": test_output},
        "detailed": {"passed": detailed["passed"], "checks": detailed["check_count"]},
        "minimal": {"passed": minimal["passed"], "checks": minimal["check_count"]},
        "json_parse_count_excluding_receipt": parsed,
        "json_errors": json_errors,
        "owner_manifest_entries": owner_entries,
        "owner_manifest_mismatches": owner_mismatches,
        "delta_manifest_entries": delta_entries,
        "delta_manifest_mismatches": delta_mismatches,
        "staged_path_count": len(staged_paths),
        "expected_staged_path_count": len(expected_delta),
        "changed_x1_paths": changed_x1,
        "declared_append_only_lifecycle_changes": declared_lifecycle_changes,
        "privacy_scanned_files": privacy["scanned_file_count"],
        "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "baton_word_count": baton_words,
        "full_repository_suite_run": False,
        "canonical_final_credit": False,
        "same_owner_only": True,
        "checks": checks,
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "Staged closeout-candidate validation only; exact-final canonical credit remains pending and the route remains unsent.",
    }


def main() -> None:
    payload = validate()
    RECEIPT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
