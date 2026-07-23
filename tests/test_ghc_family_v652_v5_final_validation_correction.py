"""Tests for the additive Eiren v652-v5 final-validation correction."""

import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v652-v5"


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestEirenV652V5FinalValidationCorrection(unittest.TestCase):
    def test_failed_attempt_is_retained_at_zero_credit(self):
        attempt = load("validation/final-validation-failed-attempt-01.json")
        self.assertFalse(attempt["valid"])
        self.assertEqual(attempt["canonical_success_credit"], 0)
        self.assertEqual(
            attempt["full_repository_tests"],
            {
                "passed": 2755,
                "total": 2759,
                "failures": 4,
                "errors": 0,
                "skipped": 0,
            },
        )
        self.assertEqual(len(attempt["failed_test_ids"]), 4)

    def test_exact_exclusion_correction_is_test_specific(self):
        correction = load(
            "validation/full-suite-lifecycle-exclusion-correction.json"
        )
        contract = load("final/final-validation-contract.json")
        self.assertEqual(correction["prior_exact_exclusion_count"], 35)
        self.assertEqual(correction["added_exact_exclusion_count"], 4)
        self.assertEqual(correction["corrected_exact_exclusion_count"], 39)
        self.assertFalse(correction["broad_module_exclusions"])
        self.assertEqual(
            contract["full_repository_suite_exact_lifecycle_exclusion_count"],
            39,
        )
        self.assertEqual(
            len(contract["full_repository_suite_exact_lifecycle_exclusions"]),
            39,
        )

    def test_final_validation_negatives_and_method_flow(self):
        negative = load("truth/final-validation-retained-negative.json")
        flow = load(
            "method-flow/final-validation-correction-method-flow-ledger.json"
        )
        self.assertEqual(negative["route_corrected_effective"], 8727)
        self.assertEqual(negative["final_validation_operational"], 7)
        self.assertEqual(negative["effective_final"], 8734)
        self.assertFalse(negative["failed_attempt_received_credit"])
        self.assertEqual(flow["counts"]["methods"], 7)
        self.assertEqual(
            flow["counts"]["witness_results"], {"fail": 7, "pass": 7}
        )

    def test_phase_truth_and_route_remain_fail_closed(self):
        truth = load("final/final-phase-truth.json")
        route = load("route/final-route-state.json")
        self.assertEqual(truth["effective_negatives"], 8734)
        self.assertEqual(truth["failed_exact_final_attempts_retained"], 1)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(route["state"], "PREPARED_NOT_SPAWNED")
        self.assertEqual(route["spawn_count"], 0)
        self.assertEqual(route["failed_exact_final_attempts_retained"], 1)

    def test_correction_manifest_review_and_privacy(self):
        manifest = load(
            "validation/final-validation-correction-staged-manifest.json"
        )
        review = load(
            "validation/final-validation-correction-staged-review.json"
        )
        privacy = load(
            "validation/final-validation-correction-staged-privacy.json"
        )
        self.assertGreater(manifest["entry_count"], 0)
        self.assertEqual(len(manifest["self_exclusions"]), 5)
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["frozen_predecessor_paths"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_retry_contract_preserves_one_success_and_no_post_success_replay(self):
        contract = load("final/final-validation-contract.json")
        self.assertEqual(contract["expected_phase_commits"], 5)
        self.assertEqual(
            contract["expected_final_parent"],
            "fb47648a1c136b8147d5d52f84c6615b718bd3c8",
        )
        self.assertEqual(contract["failed_exact_final_attempts_retained"], 1)
        self.assertEqual(contract["successful_canonical_pass_limit"], 1)
        self.assertFalse(contract["post_success_replay"])
        self.assertTrue(contract["retry_only_after_bounded_correction"])


if __name__ == "__main__":
    unittest.main()
