#!/usr/bin/env python3
"""Targeted tests for the Sylven Arc v688-v7 post-final correction."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
CORRECTION = BASE / "correction1"
FIRST_FINAL = "4e2421659eed8617cbd1fd45677b7248db2dfd11"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestSylvenArcV688V7Correction1(unittest.TestCase):
    def test_01_first_final_is_preserved(self):
        truth = load(CORRECTION / "phase-truth-overlay.json")
        self.assertEqual(truth["first_final"], FIRST_FINAL)
        self.assertFalse(truth["first_final_rewritten"])

    def test_02_method_flow_overlay_counts(self):
        flow = load(CORRECTION / "post-final-method-flow-overlay.json")
        self.assertEqual(flow["overlay_counts"], {"methods": 2, "witnesses": 4, "failed_witnesses": 2, "passing_witnesses": 2, "state_events": 2, "recommendations": 2})
        self.assertEqual(flow["combined_counts"], {"methods": 59, "witnesses": 621, "failed_witnesses": 547, "passing_witnesses": 74, "state_events": 59, "recommendations": 59})
        self.assertEqual(flow["failed_witnesses_erased"], 0)

    def test_03_effective_counts_include_two_post_final_failures(self):
        truth = load(CORRECTION / "phase-truth-overlay.json")
        self.assertEqual(truth["effective_counts"], {"proposals": 16830, "negatives": 85421, "methods": 94121, "failed_witnesses": 56299, "passing_witnesses": 86184, "open_gaps": 765, "exact_gates": 785})

    def test_04_preflight_failure_never_invoked_canonical(self):
        failure = load(CORRECTION / "canonical-preflight-failure.json")
        self.assertFalse(failure["preflight_receipt_written"])
        self.assertFalse(failure["canonical_marker_written"])
        self.assertEqual(failure["canonical_invocations"], 0)
        self.assertEqual(failure["success_credit"], 0)

    def test_05_manifest_adapter_is_explicit(self):
        policy = load(CORRECTION / "canonical-policy-overlay.json")
        self.assertEqual(policy["manifest_schema_adapter"]["supported_entry_fields"], [["bytes", "sha256"], ["bytes_normalized_lf", "sha256_normalized_lf"]])
        self.assertFalse(policy["manifest_schema_adapter"]["undeclared_schema_inference"])

    def test_06_canonical_source_contains_both_field_pairs(self):
        text = (ROOT / "scripts/ghc_family_sylven_arc_v688_v7_canonical.py").read_text(encoding="utf-8")
        for token in ("bytes_normalized_lf", "sha256_normalized_lf", 'item.get("bytes"', 'item.get("sha256"'):
            self.assertIn(token, text)

    def test_07_baton_supplement_hash_and_state(self):
        index = load(CORRECTION / "baton-supplement-index.json")
        path = ROOT / index["path"]
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), index["sha256"])
        self.assertEqual(index["delivery_state"], "PREPARED_NOT_SENT")
        self.assertGreaterEqual(index["word_count"], 500)

    def test_08_correction_content_seal_replays(self):
        seal = load(CORRECTION / "content-seal.json")
        for item in seal["targets"]:
            path = ROOT / item["path"]
            self.assertEqual(len(path.read_bytes()), item["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])

    def test_09_no_task_action_or_canonical_claim(self):
        truth = load(CORRECTION / "phase-truth-overlay.json")
        self.assertEqual((truth["canonical_invocations"], truth["canonical_successes"], truth["canonical_replays"]), (0, 0, 0))
        self.assertEqual((truth["successor_contacts"], truth["new_tasks_created"]), (0, 0))

    def test_10_terminal_verdict_and_boundaries_hold(self):
        truth = load(CORRECTION / "phase-truth-overlay.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["outcomes"], {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10})


if __name__ == "__main__":
    unittest.main()
