#!/usr/bin/env python3
"""Targeted tests for Sylven Arc v688-v7 correction 3."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
C3 = BASE / "correction3"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestSylvenArcV688V7Correction3(unittest.TestCase):
    def test_01_effective_truth_and_outcomes(self):
        truth = load(C3 / "phase-truth-overlay.json")
        self.assertEqual(truth["effective_counts"], {"proposals": 16830, "negatives": 85423, "methods": 94123, "failed_witnesses": 56301, "passing_witnesses": 86186, "open_gaps": 765, "exact_gates": 785})
        self.assertEqual(truth["outcomes"], {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10})

    def test_02_method_flow_nonerasure(self):
        flow = load(C3 / "post-final-method-flow-overlay.json")
        self.assertEqual(flow["combined_counts"], {"methods": 61, "witnesses": 625, "failed_witnesses": 549, "passing_witnesses": 76, "state_events": 61, "recommendations": 61})
        self.assertEqual(flow["failed_witnesses_erased"], 0)

    def test_03_failed_canonical_and_recovery_are_distinct(self):
        receipt = load(C3 / "failed-canonical-and-isolated-recovery.json")
        self.assertEqual(receipt["failed_canonical"]["canonical_success_credit"], 0)
        self.assertFalse(receipt["failed_canonical"]["replayed"])
        self.assertTrue(receipt["isolated_recovery"]["passed"])
        self.assertFalse(receipt["isolated_recovery"]["aggregate_replayed"])
        self.assertEqual(receipt["isolated_recovery"]["dependencies_added"], 34)

    def test_04_x2_policy_is_dependency_closed(self):
        policy = load(C3 / "canonical-policy-overlay.json")
        x2 = next(item for item in policy["test_modules"] if item["stage"] == "x2")
        self.assertEqual(x2["dependency_manifests"], ["docs/sylven-arc/v688-v7/x1/x1-manifest.json", "docs/sylven-arc/v688-v7/x2/evidence-manifest.json"])
        self.assertEqual([item["expected_tests"] for item in policy["test_modules"]], [12, 24, 20, 10, 6, 6])

    def test_05_supplement_and_content_seal(self):
        index = load(C3 / "baton-supplement-index.json")
        supplement = ROOT / index["path"]
        self.assertEqual(hashlib.sha256(supplement.read_bytes()).hexdigest(), index["sha256"])
        self.assertEqual(index["delivery_state"], "PREPARED_NOT_SENT")
        seal = load(C3 / "content-seal.json")
        for item in seal["targets"]:
            path = ROOT / item["path"]
            self.assertEqual((len(path.read_bytes()), hashlib.sha256(path.read_bytes()).hexdigest()), (item["bytes"], item["sha256"]))

    def test_06_current_head_not_yet_invoked_or_routed(self):
        truth = load(C3 / "phase-truth-overlay.json")
        self.assertEqual((truth["prior_canonical_invocations"], truth["prior_canonical_successes"]), (1, 0))
        self.assertEqual((truth["current_exact_head_canonical_invocations"], truth["current_exact_head_canonical_successes"], truth["canonical_replays"]), (0, 0, 0))
        self.assertEqual((truth["successor_contacts"], truth["new_tasks_created"]), (0, 0))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")


if __name__ == "__main__":
    unittest.main()
