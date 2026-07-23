"""Tests for the additive Eiren v652-v5 CLI route correction."""

import json
import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v652-v5"


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestEirenV652V5CliRouteCorrection(unittest.TestCase):
    def test_prior_ilyra_route_is_explicitly_unsent(self):
        prior = load("route/superseded-ilyra-route.json")
        self.assertTrue(prior["superseded_unsent"])
        self.assertEqual(prior["prior_send_count"], 0)

    def test_cli_route_is_prepared_not_spawned(self):
        route = load("route/final-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SPAWNED")
        self.assertEqual(route["target_kind"], "bounded_codex_collaboration_agent")
        self.assertEqual(route["target_phase"], "v652-v6")
        self.assertEqual(route["spawn_count"], 0)

    def test_induction_packet_contract(self):
        packet = (
            ROOT / "handoffs/cli-collaborator-v652-v6-induction.md"
        ).read_text(encoding="utf-8")
        words = len(re.findall(r"\b[\w'-]+\b", packet))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("SPAWNED_BY_EIREN_KESTREL = false", packet)
        self.assertIn("PREPARED_NOT_SPAWNED", packet)

    def test_scientific_and_authority_truth_is_unchanged(self):
        correction = load("final/terminal-route-correction.json")
        self.assertEqual(
            correction["sealed_closeout_effective_negatives"], 8721
        )
        self.assertEqual(correction["effective_final_negatives"], 8727)
        self.assertEqual(correction["open_gaps_unchanged"], 66)
        self.assertEqual(correction["exact_gates_unchanged"], 67)
        self.assertEqual(
            correction["terminal_verdict"], "NOT_READY_FOR_STAGE_20"
        )

    def test_validation_contract_is_corrected(self):
        contract = load("final/final-validation-contract.json")
        if contract["schema"].endswith("v2"):
            self.assertEqual(contract["expected_phase_commits"], 4)
            self.assertEqual(contract["expected_scoped_tests"], 76)
        else:
            self.assertEqual(
                contract["schema"],
                "ghc.family.v652-v5.final-validation-contract.corrected.v3",
            )
            self.assertEqual(contract["expected_phase_commits"], 5)
            self.assertEqual(contract["expected_scoped_tests"], 82)
        self.assertLessEqual(contract["expected_phase_commits"], 6)
        self.assertTrue(contract["route_correction_manifest_required"])
        self.assertEqual(contract["route_state"], "PREPARED_NOT_SPAWNED")

    def test_correction_review_and_privacy(self):
        review = load("validation/route-correction-staged-review.json")
        privacy = load("validation/route-correction-staged-privacy.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["frozen_x1_evidence_or_closeout_paths"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_route_method_flow_retains_timeout_and_recovery(self):
        negative = load("truth/route-correction-retained-negative.json")
        flow = load("method-flow/route-correction-method-flow-ledger.json")
        self.assertEqual(negative["effective_final"], 8727)
        self.assertEqual(flow["counts"]["methods"], 6)
        self.assertEqual(
            flow["counts"]["witness_results"], {"fail": 6, "pass": 6}
        )


if __name__ == "__main__":
    unittest.main()
