#!/usr/bin/env python3
"""Validate Ilyra v650-v8 staged evidence without running the full suite."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/ilyra-fen/v650-v8"
SOURCE = "f566d4b67bce4457cf5207f5409bbaa3427428a0"
X1 = "d8726faad1ae416ef31f98a8744901eeedfe3c56"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def status_paths() -> set[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    return {row[3:].replace("\\", "/") for row in raw.decode("utf-8").split("\0") if len(row) > 3}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt).resolve()

    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    tests = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_ghc_family_v650_v8_*.py", "-v"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    test_text = tests.stdout + tests.stderr
    match = re.search(r"Ran (\d+) tests?", test_text)
    test_count = int(match.group(1)) if match else 0

    manifest = load("validation/evidence-staged-manifest.json")
    hash_issues = []
    for row in manifest["entries"]:
        path = row["path"]
        oid = git("hash-object", f"--path={path}", path)
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
        if oid != row["git_blob"] or len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            hash_issues.append(path)

    receipt_relative = receipt.relative_to(REPO).as_posix()
    observed_status = status_paths() | {receipt_relative}
    declared_status = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    coverage_issues = sorted(observed_status ^ declared_status)

    json_files = sorted(ROOT.rglob("*.json"))
    json_issues = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_issues.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})

    document_issues = []
    max_words = 0
    max_document = None
    for path in sorted(list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.html"))):
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".html":
            text = re.sub(r"<[^>]+>", " ", text)
        words = len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))
        if words > max_words:
            max_words, max_document = words, path.relative_to(REPO).as_posix()
        if words > 6000:
            document_issues.append({"path": path.relative_to(REPO).as_posix(), "words": words})

    privacy = load("validation/evidence-staged-privacy.json")
    truth = load("truth/evidence-phase-truth.json")
    method = load("method-flow/method-flow-summary.json")
    checks = {
        "scoped_tests_12_of_12": tests.returncode == 0 and test_count == 12,
        "all_phase_json_parse": not json_issues,
        "five_class_privacy_zero_confirmed": len(privacy["pattern_classes"]) == 5 and privacy["confirmed_hit_count"] == 0,
        "manifest_hash_parity": not hash_issues,
        "manifest_surface_coverage": not coverage_issues,
        "documents_at_most_6000_words": not document_issues,
        "head_is_frozen_x1": git("rev-parse", "HEAD") == X1,
        "x1_direct_child_of_source": git("rev-parse", "HEAD^") == SOURCE,
        "one_phase_commit_at_evidence_stage": int(git("rev-list", "--count", f"{SOURCE}..HEAD")) == 1,
        "zero_phase_merges": int(git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD")) == 0,
        "truth_counts": truth["effective_negatives"] == 6425 and truth["effective_open_gaps"] == 50 and truth["effective_exact_gates"] == 51,
        "outcome_distribution": truth["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "method_failures_retained": method["counts"]["witness_results"] == {"fail": 14, "pass": 13},
        "terminal_route_held": truth["terminal_route"] == "PREPARED_NOT_SENT",
        "terminal_verdict_held": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "full_suite_not_run": truth["full_suite_state"] == "not_run_by_non_eiren_owner",
    }
    payload = {
        "schema": "ghc.family.v650-v8.evidence-scoped-validation.v1",
        "checks": checks,
        "check_count": len(checks),
        "passed_count": sum(checks.values()),
        "valid": all(checks.values()),
        "scoped_tests_run": test_count,
        "test_output_tail": test_text.strip().splitlines()[-4:],
        "json_parse_count_before_receipt": len(json_files),
        "json_issues": json_issues,
        "manifest_entry_count": manifest["entry_count"],
        "manifest_hash_issues": hash_issues,
        "manifest_coverage_issues": coverage_issues,
        "privacy_scanned_file_count": privacy["scanned_file_count"],
        "privacy_candidate_count": privacy["candidate_count"],
        "privacy_confirmed_hit_count": privacy["confirmed_hit_count"],
        "max_document_words": max_words,
        "max_document": max_document,
        "document_issues": document_issues,
        "same_owner_only": True,
        "independent_reproduction": False,
        "full_repository_suite_run": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Scoped owner-local evidence validation only; not the exact-final canonical pass, full-suite evidence, external audit, production assurance, complete privacy or accessibility, authority, or independent reproduction.",
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"checks": len(checks), "passed": payload["passed_count"], "tests": test_count, "json": len(json_files), "manifest": manifest["entry_count"], "privacy_hits": privacy["confirmed_hit_count"], "valid": payload["valid"]}, sort_keys=True))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
