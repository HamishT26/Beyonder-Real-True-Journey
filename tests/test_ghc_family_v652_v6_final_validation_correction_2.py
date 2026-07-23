"""Second correction tests for Tavian Sol v652-v6 final validation."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v652-v6"


class TestTavianV652V6FinalValidationCorrection2(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_failed_retry_is_retained(self):
        row = self.load("validation/final-validation-failed-attempt-02.json")
        self.assertEqual(row["tests_run"], 58)
        self.assertEqual(row["tests_passed"], 57)
        self.assertEqual(row["canonical_success_credit"], 0)
        self.assertTrue(row["external_receipt_written"])

    def test_all_negatives_are_additive(self):
        row = self.load("final/retained-negative-register.json")
        self.assertEqual(row["final_validation_operational"], 6)
        self.assertEqual(row["effective_count"], 8916)
        self.assertTrue(row["no_failure_erased"])

    def test_method_flow_contains_thirty_pairs(self):
        flow = self.load("method-flow/final-method-flow-ledger.json")
        self.assertEqual(flow["counts"]["methods"], 30)
        self.assertEqual(flow["counts"]["witness_results"], {"fail":30,"pass":30})
        self.assertEqual(flow["counts"]["states"]["preferred"], 30)

    def test_five_commit_launch_contract(self):
        row = self.load("final/final-validation-contract.json")
        self.assertEqual(row["expected_scoped_tests"], 58)
        self.assertEqual(row["expected_phase_commits"], 5)
        self.assertFalse(row["full_repository_suite_required"])
        self.assertEqual(row["full_repository_suite_owner"], "Eiren Kestrel")

    def test_route_is_still_prepared_only(self):
        row = self.load("route/final-route-state.json")
        self.assertEqual(row["state"], "PREPARED_NOT_SENT")
        self.assertEqual(row["send_count"], 0)
        self.assertEqual(row["contact_count"], 0)

    def test_correction_two_review_and_privacy(self):
        review = self.load("validation/final-validation-correction-2-staged-review.json")
        privacy = self.load("validation/final-validation-correction-2-staged-privacy.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)


if __name__ == "__main__":
    unittest.main()
