#!/usr/bin/env python3
"""Targeted tests for Sylven Arc v688-v7 correction 4."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
C4 = BASE / "correction4"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestSylvenArcV688V7Correction4(unittest.TestCase):
    def test_01_prior_receipt_has_all_tests_and_one_false_aggregate(self):
        failure = load(C4 / "correction3-canonical-failure.json")
        self.assertTrue(failure["all_test_modules_passed"])
        self.assertEqual((failure["tests"], failure["test_modules"]), (78, 6))
        self.assertEqual(failure["false_checks"], ["all_lifecycle_tests"])
        self.assertEqual(failure["canonical_success_credit"], 0)

    def test_02_dynamic_policy_cardinality_is_in_source(self):
        text = (ROOT / "scripts/ghc_family_sylven_arc_v688_v7_canonical.py").read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count('len(state["policy"]["test_modules"])'), 1)
        self.assertIn('len(state.get("policy", {}).get("test_modules", []))', text)

    def test_03_effective_truth_and_method_counts(self):
        truth = load(C4 / "phase-truth-overlay.json")
        flow = load(C4 / "post-final-method-flow-overlay.json")
        self.assertEqual(truth["effective_counts"], {"proposals": 16830, "negatives": 85424, "methods": 94124, "failed_witnesses": 56302, "passing_witnesses": 86187, "open_gaps": 765, "exact_gates": 785})
        self.assertEqual(flow["combined_counts"], {"methods": 62, "witnesses": 627, "failed_witnesses": 550, "passing_witnesses": 77, "state_events": 62, "recommendations": 62})
        self.assertEqual(flow["failed_witnesses_erased"], 0)

    def test_04_policy_has_seven_modules_and_dependency_closed_x2(self):
        policy = load(C4 / "canonical-policy-overlay.json")
        self.assertEqual(len(policy["test_modules"]), 7)
        self.assertEqual([item["expected_tests"] for item in policy["test_modules"]], [12, 24, 20, 10, 6, 6, 5])
        x2 = next(item for item in policy["test_modules"] if item["stage"] == "x2")
        self.assertEqual(len(x2["dependency_manifests"]), 2)

    def test_05_supplement_seal_and_no_route(self):
        index = load(C4 / "baton-supplement-index.json")
        path = ROOT / index["path"]
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), index["sha256"])
        seal = load(C4 / "content-seal.json")
        for item in seal["targets"]:
            target = ROOT / item["path"]
            self.assertEqual((len(target.read_bytes()), hashlib.sha256(target.read_bytes()).hexdigest()), (item["bytes"], item["sha256"]))
        truth = load(C4 / "phase-truth-overlay.json")
        self.assertEqual((truth["current_exact_head_canonical_invocations"], truth["successor_contacts"], truth["new_tasks_created"]), (0, 0, 0))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
