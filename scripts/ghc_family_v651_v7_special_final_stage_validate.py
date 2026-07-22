#!/usr/bin/env python3
"""Validate the exact staged closeout boundary for Vesper v651-v7 special."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"
PHASE_REL = PHASE.relative_to(ROOT).as_posix()
TEXT_SUFFIXES = {".json", ".md", ".txt", ".html", ".yaml", ".yml", ".py"}
PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|file|vscode)://"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret)\s*[:=]\s*[^\s,}\]]+"),
    "delegation_markup": re.compile(r"(?i)<\s*codex_delegation\b"),
}
ALLOWED_GLOBALS = {
    "scripts/build_ghc_family_v651_v7_special_closeout.py",
    "scripts/ghc_family_v651_v7_special_final_stage_validate.py",
    "scripts/ghc_family_v651_v7_special_terminal_validate.py",
    "tests/test_ghc_family_v651_v7_special_closeout.py",
    "tests/test_ghc_family_v651_v7_special_x2.py",
}
SCANNER_DEFINITIONS = {
    "scripts/ghc_family_v651_v7_special_final_stage_validate.py",
    "scripts/ghc_family_v651_v7_special_terminal_validate.py",
}


def git_text(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", check=True,
    ).stdout.strip()


def git_bytes(spec: str) -> bytes:
    return subprocess.run(
        ["git", "show", spec], cwd=ROOT, capture_output=True, check=True,
    ).stdout


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def run_tests() -> dict[str, Any]:
    suite = unittest.defaultTestLoader.loadTestsFromNames(
        [
            "tests.test_ghc_family_v651_v7_special_x1",
            "tests.test_ghc_family_v651_v7_special_x2",
            "tests.test_ghc_family_v651_v7_special_closeout",
        ]
    )
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "output": stream.getvalue()[-2000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any, expected: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed, "expected": expected})

    staged = [row for row in git_text("diff", "--cached", "--name-only", "HEAD").splitlines() if row]
    out_of_scope = [
        path for path in staged
        if not path.startswith(PHASE_REL + "/") and path not in ALLOWED_GLOBALS
    ]
    required = {
        f"{PHASE_REL}/closeout/closeout-receipt.json",
        f"{PHASE_REL}/seal/seal-receipt.json",
        f"{PHASE_REL}/final/final-record.json",
        f"{PHASE_REL}/lifecycle/anchor-contract.json",
        "scripts/ghc_family_v651_v7_special_terminal_validate.py",
        "tests/test_ghc_family_v651_v7_special_closeout.py",
    }
    check("owner_scope", not out_of_scope, out_of_scope, [])
    check("required_paths", required.issubset(staged), sorted(required - set(staged)), [])

    json_issues: list[dict[str, str]] = []
    privacy_candidates: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    staged_json = 0
    for path in staged:
        data = git_bytes(f":{path}")
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
                staged_json += 1
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_issues.append({"path": path, "error": type(exc).__name__})
        if Path(path).suffix.lower() in TEXT_SUFFIXES:
            text = data.decode("utf-8", errors="replace")
            for label, pattern in PATTERNS.items():
                if pattern.search(text):
                    row = {"path": path, "class": label}
                    if path in SCANNER_DEFINITIONS:
                        privacy_candidates.append(row)
                    else:
                        privacy_hits.append(row)
    check("staged_json", not json_issues, {"parsed": staged_json, "issues": json_issues}, "all staged JSON parses")
    check("staged_privacy", not privacy_hits, {"candidates": privacy_candidates, "confirmed": privacy_hits}, "zero confirmed hits")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    exclusions = set(manifest["self_exclusions"])
    index_paths = set(git_text("ls-files", "--cached", "--", PHASE_REL).splitlines())
    expected = index_paths - exclusions
    listed = {row["path"] for row in manifest["entries"]}
    mismatches = []
    for row in manifest["entries"]:
        data = git_bytes(f":{row['path']}")
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    check(
        "index_manifest",
        manifest.get("domain") == "index" and expected == listed and not mismatches,
        {"entries": len(listed), "domain_equal": expected == listed, "mismatches": mismatches, "exclusions": sorted(exclusions)},
        "exact index phase domain",
    )

    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8",
    )
    check("diff_hygiene", diff_check.returncode == 0, diff_check.stdout + diff_check.stderr, "clean")
    tests = run_tests()
    check("scoped_tests", tests["successful"] and tests["tests_run"] == 26, tests, "26 passing tests")

    truth = load("truth/phase-truth.json")
    check("outcomes", truth["outcomes"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}, truth["outcomes"], "23/5/1/1")
    check("negatives", truth["effective_negatives"] == 7570, truth["effective_negatives"], 7570)
    check("gates", (truth["effective_open_gaps"], truth["effective_exact_gates"]) == (59, 60), [truth["effective_open_gaps"], truth["effective_exact_gates"]], [59, 60])
    method = load("method-flow/method-flow-summary.json")
    check("method_flow", method["valid"] and method["counts"]["states"]["preferred"] == 10 and method["counts"]["witness_results"] == {"fail": 12, "pass": 11}, method["counts"], "10 preferred, 12 fail, 11 pass")

    payload = {
        "schema": "ghc.family.v651-v7-special.final-staged-review.v1",
        "valid": all(row["passed"] for row in checks),
        "checks_passed": sum(row["passed"] for row in checks),
        "check_count": len(checks),
        "checks": checks,
        "tests": tests,
        "reviewed_paths": len(staged),
        "staged_json": staged_json,
        "privacy_pattern_classes": len(PATTERNS),
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": privacy_hits,
        "manifest_entries": manifest["entry_count"],
        "receipt_self_excluded_from_manifest": args.receipt.as_posix() in exclusions,
        "boundary": "Exact staged same-owner closeout review only; not terminal validation, independent reproduction, production assurance, or Stage 20 evidence.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": payload["valid"], "tests": tests["tests_run"], "checks": f"{payload['checks_passed']}/{payload['check_count']}", "paths": len(staged), "json": staged_json, "manifest": manifest["entry_count"]}))
    return 0 if payload["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
