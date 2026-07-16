#!/usr/bin/env python3
"""Run bounded recent-round and current-packet v645-v8 validation."""

from __future__ import annotations

import argparse
import importlib.util
import io
import json
import sys
import unittest

from ghc_family_v645_v8_runtime import ROOT, TRUTH_BOUNDARY, parse_json_documents, privacy_scan, write_json
from ghc_family_v645_v8_validator import validate


TEST_FILES = [
    "tests/test_ghc_family_v645_v5_x1.py",
    "tests/test_ghc_family_v645_v5.py",
    "tests/test_ghc_family_v645_v6_x1.py",
    "tests/test_ghc_family_v645_v6.py",
    "tests/test_ghc_family_v645_v7.py",
    "tests/test_ghc_family_v645_v8.py",
]


def scoped_tests() -> dict:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for index, relative in enumerate(TEST_FILES, 1):
        path = ROOT / relative
        spec = importlib.util.spec_from_file_location(f"ghc_family_scoped_{index}", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Cannot load scoped test file {relative}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        suite.addTests(loader.loadTestsFromModule(module))
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
    return {
        "files": TEST_FILES,
        "file_count": len(TEST_FILES),
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "passed": result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
        "valid": result.wasSuccessful(),
        "full_repository_suite": False,
        "full_repository_suite_owner": "Eiren Kestrel",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", default="evidence", choices=["evidence", "closeout", "final", "replay"])
    args = parser.parse_args()
    detailed = validate("detailed")
    minimal = validate("minimal")
    tests = scoped_tests()
    parsed = parse_json_documents()
    privacy = privacy_scan()
    write_json(f"validation/{args.stage}-detailed.json", detailed)
    write_json(f"validation/{args.stage}-minimal.json", minimal)
    write_json(f"validation/{args.stage}-scoped-test-receipt.json", tests)
    write_json(f"validation/{args.stage}-json-document-receipt.json", parsed)
    write_json(f"validation/{args.stage}-privacy-scan.json", privacy)
    payload = {
        "schema": "ghc.family.v645-v8.validation-runner.v1",
        "stage": args.stage,
        "detailed": {"passed": detailed["passed"], "checks": detailed["check_count"], "result": detailed["result"]},
        "minimal": {"passed": minimal["passed"], "checks": minimal["check_count"], "result": minimal["result"]},
        "tests": tests,
        "json": parsed,
        "privacy": privacy,
        "full_repository_suite": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True,
        "independent_reproduction": False,
        "result": "pass" if detailed["result"] == minimal["result"] == "pass" and tests["valid"] and parsed["valid"] and privacy["valid"] else "fail",
        "boundary": TRUTH_BOUNDARY,
    }
    write_json(f"prototypes/runner-witnesses/ghc_family_v645_v8_validation_runner_{args.stage}.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
