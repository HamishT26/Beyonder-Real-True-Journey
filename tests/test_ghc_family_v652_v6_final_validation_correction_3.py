"""Third correction tests for Tavian Sol v652-v6 final validation."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v652-v6"


class TestTavianV652V6FinalValidationCorrection3(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_failed_retry_two_is_retained(self):
        row = self.load("validation/final-validation-failed-attempt-03.json")
        self.assertEqual(row["tests_run"], 58)
        self.assertEqual(row["tests_passed"], 56)
        self.assertEqual(row["canonical_success_credit"], 0)
        self.assertTrue(row["external_receipt_written"])

    def test_final_counts_are_additive(self):
        row = self.load("final/retained-negative-register.json")
        self.assertEqual(row["final_validation_operational"], 7)
        self.assertEqual(row["effective_count"], 8917)

    def test_method_flow_has_thirty_one_pairs(self):
        flow = self.load("method-flow/final-method-flow-ledger.json")
        self.assertEqual(flow["counts"]["methods"], 31)
        self.assertEqual(flow["counts"]["witness_results"], {"fail":31,"pass":31})
        self.assertEqual(flow["counts"]["states"]["preferred"], 31)

    def test_six_commit_launch_contract_and_route(self):
        contract = self.load("final/final-validation-contract.json")
        route = self.load("route/final-route-state.json")
        self.assertEqual(contract["expected_phase_commits"], 6)
        self.assertEqual(contract["expected_scoped_tests"], 58)
        self.assertFalse(contract["full_repository_suite_required"])
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)
        self.assertEqual(route["contact_count"], 0)

    def test_correction_three_review_and_privacy(self):
        review = self.load("validation/final-validation-correction-3-staged-review.json")
        privacy = self.load("validation/final-validation-correction-3-staged-privacy.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)


if __name__ == "__main__":
    unittest.main()
