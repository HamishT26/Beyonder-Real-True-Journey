"""Correction tests for Tavian Sol v652-v6 final validation."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v652-v6"


class TestTavianV652V6FinalValidationCorrection(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_failed_attempt_is_zero_credit(self):
        row = self.load("validation/final-validation-failed-attempt-01.json")
        self.assertEqual(row["tests_run"], 0)
        self.assertEqual(row["canonical_success_credit"], 0)
        self.assertFalse(row["external_receipt_written"])

    def test_negative_is_additive(self):
        row = self.load("final/retained-negative-register.json")
        self.assertEqual(row["final_validation_operational"], 4)
        self.assertEqual(row["effective_count"], 8914)
        self.assertTrue(row["no_failure_erased"])

    def test_method_flow_retains_both_witnesses(self):
        flow = self.load("method-flow/final-method-flow-ledger.json")
        self.assertEqual(flow["counts"]["methods"], 28)
        self.assertEqual(flow["counts"]["witness_results"], {"fail":28,"pass":28})
        self.assertEqual(flow["counts"]["states"]["preferred"], 28)

    def test_launch_contract_not_full_repository(self):
        row = self.load("final/final-validation-contract.json")
        self.assertEqual(row["validation_scope"], "launch_scoped")
        self.assertEqual(row["expected_scoped_tests"], 58)
        self.assertFalse(row["full_repository_suite_required"])
        self.assertEqual(row["full_repository_suite_owner"], "Eiren Kestrel")

    def test_route_remains_unsent(self):
        row = self.load("route/final-route-state.json")
        self.assertEqual(row["state"], "PREPARED_NOT_SENT")
        self.assertEqual(row["send_count"], 0)
        self.assertEqual(row["contact_count"], 0)

    def test_validator_binds_repository_root(self):
        text = (REPO / "scripts/ghc_family_v652_v6_final_validate.py").read_text(encoding="utf-8")
        self.assertIn("sys.path.insert(0, str(REPO))", text)
        self.assertIn("test_ghc_family_v652_v6_final_validation_correction.py", text)

    def test_correction_preflight_review(self):
        review = self.load("validation/final-validation-correction-staged-review.json")
        privacy = self.load("validation/final-validation-correction-staged-privacy.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)


if __name__ == "__main__":
    unittest.main()
