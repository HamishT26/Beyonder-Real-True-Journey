#!/usr/bin/env python3
"""Run the explicit non-Eiren successor-scoped v646-v2 test selection."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
MODULES = [
    "tests.test_ghc_family_v645_v8_x1",
    "tests.test_ghc_family_v645_v8",
    "tests.test_ghc_family_v646_v1_x1",
    "tests.test_ghc_family_v646_v1",
    "tests.test_ghc_family_v646_v2_x1",
    "tests.test_ghc_family_v646_v2",
]
EXCLUDED = {
    "tests.test_ghc_family_v646_v1.V646V1EvidenceTests.test_detailed_validator_precommit": "original v646-v1 phase-local commit-cap assertion",
    "tests.test_ghc_family_v646_v1.V646V1EvidenceTests.test_minimal_validator_precommit": "original v646-v1 phase-local commit-cap assertion",
}
BOUNDARY = "The explicit successor selection is bounded same-owner regression evidence, not the complete repository suite or independent reproduction."


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    head = git("rev-parse", "HEAD")
    if args.revision and head != args.revision:
        raise SystemExit("exact revision mismatch")
    clean = not bool(git("status", "--porcelain=v1"))
    if args.require_clean and not clean:
        raise SystemExit("clean state required")

    discovered = unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    tests = list(flatten(discovered))
    eligible = [test for test in tests if test.id() not in EXCLUDED]
    suite = unittest.TestSuite(eligible)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    payload = {
        "schema": "ghc.family.v646-v2.successor-scoped-tests.v1",
        "head": head,
        "clean": clean,
        "modules": MODULES,
        "discovered_count": len(tests),
        "excluded_phase_local_tests": [{"test_id": test_id, "reason": reason} for test_id, reason in sorted(EXCLUDED.items())],
        "excluded_count": len(EXCLUDED),
        "eligible_count": len(eligible),
        "tests_run": result.testsRun,
        "passed": passed,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "full_repository_suite_run": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid": result.wasSuccessful() and len(tests) == 67 and len(eligible) == 65,
        "boundary": BOUNDARY,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps({"head": head, "discovered": len(tests), "excluded": len(EXCLUDED), "tests": result.testsRun, "passed": passed, "failures": len(result.failures), "errors": len(result.errors), "clean": clean, "valid": payload["valid"]}))
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
