#!/usr/bin/env python3
"""Run Sylven v658-v2's authorized current and bounded compatibility scope."""

from __future__ import annotations

import argparse
import importlib
import io
import json
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CURRENT_X1_TESTS = [
    "test_all_phase_json_parses",
    "test_every_x1_failure_has_fail_and_pass_witnesses",
    "test_expected_dispositions_are_not_outcomes",
    "test_novelty_audits_all_inherited_rows",
    "test_portfolios_and_tool_plans_are_frozen_only",
    "test_privacy_manifest_and_caps",
    "test_route_is_current_phase_only",
    "test_source_head_and_ancestry",
    "test_source_ledger_resolves_all_proposal_references",
    "test_thirty_complete_proposal_contracts",
]
FINAL_STABLE_TESTS = [
    "test_closeout_manifest_replay",
    "test_final_artifact_packet_exists",
    "test_final_method_pair",
    "test_final_record_does_not_preclaim",
    "test_final_truth_candidate",
    "test_phase_json_parses",
    "test_terminal_route_is_unsent",
]


def add_named_cases(
    suite: unittest.TestSuite, module_name: str, class_name: str, names: list[str]
) -> None:
    module = importlib.import_module(module_name)
    case = getattr(module, class_name)
    for name in names:
        suite.addTest(case(name))


def run_scope() -> dict[str, Any]:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    add_named_cases(
        suite,
        "tests.test_ghc_family_v658_v2_x1",
        "V658V2X1Tests",
        CURRENT_X1_TESTS,
    )
    suite.addTests(
        loader.loadTestsFromModule(importlib.import_module("tests.test_ghc_family_v658_v2"))
    )
    suite.addTests(
        loader.loadTestsFromModule(importlib.import_module("tests.test_ghc_family_v657_v6"))
    )
    suite.addTests(
        loader.loadTestsFromModule(importlib.import_module("tests.test_ghc_family_v657_v5"))
    )
    suite.addTests(
        loader.loadTestsFromModule(
            importlib.import_module("tests.test_ghc_family_v657_v5_successor_scope")
        )
    )
    add_named_cases(
        suite,
        "tests.test_ghc_family_v657_v5_final",
        "V657V5FinalTests",
        FINAL_STABLE_TESTS,
    )
    add_named_cases(
        suite,
        "tests.test_ghc_family_v657_v4_final",
        "V657V4FinalTests",
        FINAL_STABLE_TESTS,
    )
    expected = suite.countTestCases()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "schema": "ghc.family.v658-v2.authorized-scoped-tests.v1",
        "valid": result.wasSuccessful() and result.testsRun == expected and not result.skipped,
        "tests_run": result.testsRun,
        "expected_tests": expected,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "failed_test_ids": [case.id() for case, _ in result.failures],
        "error_test_ids": [case.id() for case, _ in result.errors],
        "selection": {
            "current_x1_immutable_safe": len(CURRENT_X1_TESTS),
            "current_x2": 41,
            "recent_orin_x2": 41,
            "recent_caelen_x2": 41,
            "caelen_successor_scope": 5,
            "caelen_final_stable": len(FINAL_STABLE_TESTS),
            "sable_final_stable": len(FINAL_STABLE_TESTS),
        },
        "explicit_exclusions": [
            {
                "module": "tests.test_ghc_family_v658_v2_x1",
                "test": "test_no_x2_or_outcome_artifacts_exist",
                "reason": "original x1 working-tree assertion; immutable x1 absence is checked from its exact Git tree by current x2",
            },
            {
                "module": "tests.test_ghc_family_v657_v5_final",
                "test": "test_anchor_chain_and_commit_cap",
                "reason": "original Caelen phase-local commit-count assertion; successor ancestry and zero merges are checked separately",
            },
            {
                "module": "tests.test_ghc_family_v657_v4_final",
                "test": "test_anchor_chain_and_commit_cap",
                "reason": "original Sable phase-local commit-count assertion; successor ancestry and zero merges are checked separately",
            },
        ],
        "full_repository_suite_run": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "runner_output": stream.getvalue(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = run_scope()
    if args.output:
        path = ROOT / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(
        json.dumps(
            {
                "valid": payload["valid"],
                "tests_run": payload["tests_run"],
                "expected_tests": payload["expected_tests"],
                "failures": payload["failures"],
                "errors": payload["errors"],
                "skipped": payload["skipped"],
            },
            sort_keys=True,
        )
    )
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
