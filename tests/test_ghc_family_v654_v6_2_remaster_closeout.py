"""Closeout tests for Eiren's bounded v654-v6 (2) remaster."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v654-v6-2-remaster"
SOURCE = "a6987b3a572254d52721066d19bdbcd0686a8098"
X1 = "37872a3fb9593bd0a8d862164a0ccc44bb946793"
EVIDENCE = "f878615e289d8d383bc54f75c0dca4c75b16b0e4"
ROUTE_STATE = "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestV654V6RemasterCloseout(unittest.TestCase):
    def test_final_truth_is_exact_and_bounded(self):
        truth = load("truth/final-phase-truth.json")
        self.assertEqual(
            truth["outcomes"],
            {
                "completed": 23,
                "represented": 5,
                "open_gap": 1,
                "exact_gate": 1,
            },
        )
        self.assertEqual(truth["proposal_count"], 30)
        self.assertEqual(truth["frozen_chain_count"], 1870)
        self.assertEqual(truth["synthetic_mutation_negative_count"], 150)
        self.assertEqual(truth["effective_negative_count"], 11871)
        self.assertEqual(truth["open_gap_count"], 86)
        self.assertEqual(truth["exact_gate_count"], 85)
        self.assertEqual(truth["method_count"], 130)
        self.assertEqual(truth["failed_witness_count"], 130)
        self.assertEqual(truth["passing_witness_count"], 130)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(
            truth["full_repository_suite_state"],
            "POSTCOMMIT_CANONICAL_PASS_REQUIRED",
        )
        self.assertEqual(truth["canonical_success_count"], 0)
        self.assertFalse(truth["post_success_replay"])

    def test_real_world_and_authority_counters_remain_zero(self):
        truth = load("truth/final-phase-truth.json")
        for key in (
            "real_queries",
            "real_downloads",
            "real_rows",
            "real_likelihoods",
            "real_participants",
            "real_keys_or_proofs",
            "training_events",
            "production_deployments",
            "authority_decisions",
        ):
            self.assertEqual(truth[key], 0, key)
        self.assertFalse(truth["independent_reproduction_claimed"])
        self.assertFalse(truth["theory_of_everything_claimed"])
        self.assertFalse(truth["agi_or_asi_claimed"])
        self.assertFalse(truth["consciousness_or_personhood_claimed"])

    def test_lifecycle_ancestry_is_preregistered(self):
        ancestry = load("provenance/lifecycle-ancestry.json")
        self.assertEqual(ancestry["source"], SOURCE)
        self.assertEqual(ancestry["x1"], X1)
        self.assertEqual(ancestry["evidence"], EVIDENCE)
        self.assertEqual(ancestry["final"], "resolved_at_terminal_gate")
        self.assertEqual(ancestry["expected_remaster_commit_count"], 3)
        self.assertEqual(ancestry["expected_merge_count"], 0)
        self.assertEqual(ancestry["expected_final_parent"], EVIDENCE)
        self.assertTrue(ancestry["x1_before_x2"])

    def test_elaren_baton_is_sanitized_and_terminal_gated(self):
        metadata = load(
            "handoffs/elaren-kestrel-v654-v7-activation-metadata.json"
        )
        baton = (
            ROOT / "handoffs/elaren-kestrel-v654-v7-activation.md"
        ).read_text(encoding="utf-8")
        words = re.findall(r"\b[\w'-]+\b", baton, flags=re.UNICODE)
        self.assertEqual(metadata["recipient"], "Elaren Kestrel")
        self.assertEqual(metadata["phase"], "v654-v7")
        self.assertEqual(metadata["endpoint_kind"], "main_task")
        self.assertEqual(metadata["next_recipient"], "Neris Solane")
        self.assertEqual(metadata["next_phase"], "v654-v8")
        self.assertEqual(metadata["delivery_state"], ROUTE_STATE)
        self.assertEqual(metadata["contact_count"], 0)
        self.assertEqual(metadata["send_cap"], 1)
        self.assertTrue(metadata["direct_and_fallback_mutually_exclusive"])
        self.assertFalse(metadata["private_route_values_present"])
        self.assertEqual(metadata["word_count"], len(words))
        self.assertGreaterEqual(len(words), 10000)
        self.assertLessEqual(len(words), 100000)
        self.assertIn("Elaren Kestrel", baton)
        self.assertIn("Neris Solane", baton)
        self.assertIn(ROUTE_STATE, baton)
        self.assertNotIn("source_thread_id", baton.casefold())
        self.assertNotIn("thread_id", baton.casefold())
        self.assertNotRegex(baton, r"(?i)[A-Z]:\\Users\\")

    def test_validation_protocol_has_one_new_exact_exclusion(self):
        protocol = load("validation/final-validation-protocol.json")
        exclusions = protocol["current_exact_lifecycle_exclusions"]
        self.assertEqual(protocol["inherited_exact_lifecycle_exclusion_count"], 57)
        self.assertEqual(len(exclusions), 1)
        self.assertIn(
            "test_x1_privacy_and_no_x2_surfaces",
            exclusions[0],
        )
        self.assertEqual(protocol["canonical_success_limit"], 1)
        self.assertFalse(protocol["post_success_replay_permitted"])
        self.assertTrue(protocol["full_repository_suite_required"])

    def test_packaging_failures_remain_retained(self):
        receipt = load("validation/evidence-packaging-closeout.json")
        self.assertEqual(receipt["failed_or_ambiguous_attempt_count"], 4)
        self.assertTrue(receipt["retained"])
        self.assertEqual(receipt["successful_manifest_entry_count"], 182)
        self.assertEqual(receipt["successful_privacy_scan_file_count"], 228)
        self.assertEqual(receipt["successful_privacy_confirmed_hits"], 0)
        self.assertEqual(receipt["successful_json_parse_count"], 183)
        self.assertEqual(receipt["successful_manifest_replay_issue_count"], 0)
        self.assertFalse(receipt["post_success_replay"])

    def test_closeout_failure_and_recovery_are_both_retained(self):
        supplement = load(
            "method-flow/method-flow-closeout-supplement.json"
        )
        self.assertEqual(supplement["prior_effective_negative_count"], 11870)
        self.assertEqual(supplement["prior_method_count"], 129)
        self.assertEqual(supplement["new_operational_negative_count"], 1)
        self.assertEqual(supplement["effective_negative_count"], 11871)
        self.assertEqual(supplement["effective_method_count"], 130)
        self.assertEqual(supplement["failed_witness"]["credit"], 0)
        self.assertTrue(supplement["failed_witness"]["retained"])
        self.assertTrue(supplement["passing_witness"]["bounded"])
        self.assertFalse(supplement["recovery_erased_failure"])


if __name__ == "__main__":
    unittest.main()
