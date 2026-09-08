#!/usr/bin/env python3
"""Targeted tests for Sylven Arc v688-v7 correction 2."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
C2 = BASE / "correction2"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestSylvenArcV688V7Correction2(unittest.TestCase):
    def test_01_scope_bases_are_distinct(self):
        policy = load(C2 / "canonical-policy-overlay.json")
        self.assertEqual(policy["scope_bases"], {"owner_scope": "e7db6f3be1327de72f93873eb6540aabfc773344", "correction_scope": "c0f79218f2d644592bd4eee0947058f0f3803b50"})

    def test_02_counts_and_nonerasure(self):
        flow = load(C2 / "post-final-method-flow-overlay.json")
        self.assertEqual(flow["combined_counts"], {"methods": 60, "witnesses": 623, "failed_witnesses": 548, "passing_witnesses": 75, "state_events": 60, "recommendations": 60})
        self.assertEqual(flow["failed_witnesses_erased"], 0)

    def test_03_effective_truth(self):
        truth = load(C2 / "phase-truth-overlay.json")
        self.assertEqual(truth["effective_counts"], {"proposals": 16830, "negatives": 85422, "methods": 94122, "failed_witnesses": 56300, "passing_witnesses": 86185, "open_gaps": 765, "exact_gates": 785})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_04_no_canonical_preflight_or_action_claim(self):
        failure = load(C2 / "preflight-design-failure.json")
        truth = load(C2 / "phase-truth-overlay.json")
        self.assertFalse(failure["preflight_receipt_written"])
        self.assertFalse(failure["canonical_marker_written"])
        self.assertEqual((truth["canonical_invocations"], truth["successor_contacts"], truth["new_tasks_created"]), (0, 0, 0))

    def test_05_supplement_hash(self):
        index = load(C2 / "baton-supplement-index.json")
        path = ROOT / index["path"]
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), index["sha256"])
        self.assertEqual(index["delivery_state"], "PREPARED_NOT_SENT")

    def test_06_content_seal_and_test_policy(self):
        seal = load(C2 / "content-seal.json")
        for item in seal["targets"]:
            path = ROOT / item["path"]
            self.assertEqual((len(path.read_bytes()), hashlib.sha256(path.read_bytes()).hexdigest()), (item["bytes"], item["sha256"]))
        policy = load(C2 / "canonical-policy-overlay.json")
        self.assertEqual([item["expected_tests"] for item in policy["test_modules"]], [12, 24, 20, 10, 6])


if __name__ == "__main__":
    unittest.main()
