#!/usr/bin/env python3
"""Run the non-Eiren scoped v645-v3 through v645-v6 validation floor."""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
import unittest
from pathlib import Path

from ghc_family_v645_v6_runtime import PHASE, ROOT, TRUTH_BOUNDARY, parse_json_documents, privacy_scan, write_json
from ghc_family_v645_v6_validator import validate

sys.path.insert(0, str(ROOT))


MODULES = [
    "tests.test_ghc_family_v645_v3_x1", "tests.test_ghc_family_v645_v3",
    "tests.test_ghc_family_v645_v4_x1", "tests.test_ghc_family_v645_v4",
    "tests.test_ghc_family_v645_v5_x1", "tests.test_ghc_family_v645_v5",
    "tests.test_ghc_family_v645_v6_x1", "tests.test_ghc_family_v645_v6",
]


def run_tests() -> tuple[unittest.result.TestResult, float]:
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for module in MODULES:
        suite.addTests(loader.loadTestsFromName(module))
    stream = io.StringIO()
    started = time.perf_counter()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return result, time.perf_counter() - started


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["evidence", "final", "replay"], required=True)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    if args.stage == "evidence" and not args.no_write:
        write_json("prototypes/runner-witnesses/ghc_family_v645_v6_validation_runner.json", {
            "schema": "ghc.family.v645-v6.validation-runner.v1",
            "stage": "evidence", "state": "bounded_run_in_progress",
            "full_repository_suite": False, "full_repository_suite_owner": "Eiren Kestrel",
            "same_owner_only": True, "independent_reproduction": False,
            "boundary": TRUTH_BOUNDARY,
        })
    tests, seconds = run_tests()
    detailed = validate("detailed")
    minimal = validate("minimal")
    json_receipt = parse_json_documents()
    privacy = privacy_scan()
    markdown = list(PHASE.rglob("*.md"))
    word_counts = {path.relative_to(PHASE).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in markdown}
    stale_hits = []
    stale_patterns = [re.compile(r"(?<!NOT_)READY_FOR_STAGE_20"), re.compile(r'"route_state"\s*:\s*"SENT"')]
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html"}:
            text = path.read_text(encoding="utf-8")
            if any(pattern.search(text) for pattern in stale_patterns):
                stale_hits.append(path.relative_to(ROOT).as_posix())
    test_passed = tests.testsRun - len(tests.failures) - len(tests.errors)
    passed = tests.wasSuccessful() and detailed["result"] == "pass" and minimal["result"] == "pass" and json_receipt["valid"] and privacy["valid"] and not stale_hits and not any(count > 6000 for count in word_counts.values())
    payload = {
        "schema": "ghc.family.v645-v6.validation-runner.v1",
        "stage": args.stage,
        "scope": "v645-v3 through v645-v6 x1/x2 modules only",
        "modules": MODULES,
        "scoped_tests": {"passed": test_passed, "total": tests.testsRun, "failures": len(tests.failures), "errors": len(tests.errors), "seconds": round(seconds, 3)},
        "detailed": {"passed": detailed["passed"], "total": detailed["check_count"]},
        "minimal": {"passed": minimal["passed"], "total": minimal["check_count"]},
        "json_documents": json_receipt["documents"],
        "json_failures": json_receipt["failures"],
        "privacy_files": privacy["files_scanned"],
        "privacy_pattern_classes": privacy["pattern_classes"],
        "privacy_hits": privacy["hits"],
        "stale_label_hits": stale_hits,
        "markdown_documents": len(markdown),
        "maximum_document_words": max(word_counts.values(), default=0),
        "over_6000_words": {path: count for path, count in word_counts.items() if count > 6000},
        "full_repository_suite": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "result": "pass" if passed else "fail",
        "boundary": TRUTH_BOUNDARY,
    }
    if not args.no_write:
        write_json(f"validation/{args.stage}-validation-runner-receipt.json", payload)
        write_json(f"validation/{args.stage}-detailed.json", detailed)
        write_json(f"validation/{args.stage}-minimal.json", minimal)
        if args.stage == "evidence":
            write_json("prototypes/runner-witnesses/ghc_family_v645_v6_validation_runner.json", payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
