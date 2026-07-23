"""Closeout tests for Sylven Arc v652-v4."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v652-v4"


class TestSylvenV652V4Closeout(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_final_truth(self):
        truth = self.load("final/final-phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed":23,"represented":5,"open_gap":1,"exact_gate":1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_negatives_and_gates(self):
        self.assertEqual(self.load("final/retained-negative-register.json")["effective_count"], 8549)
        self.assertEqual(self.load("final/open-gap-register.json")["effective_count"], 65)
        self.assertEqual(self.load("final/exact-gate-register.json")["effective_count"], 66)

    def test_outcomes_and_mutations(self):
        outcomes = self.load("evidence/proposal-outcomes.json")
        self.assertEqual(outcomes["proposal_count"], 30)
        self.assertEqual(outcomes["mutation_count"], 150)
        self.assertEqual(outcomes["mutation_rejected_or_quarantined_count"], 150)

    def test_baton_contract_and_route(self):
        baton = (ROOT / "handoffs/eiren-kestrel-v652-v5-activation.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\b[\w'-]+\b", baton))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        route = self.load("route/final-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)

    def test_overview_and_accessible_report(self):
        overview = (ROOT / "overview/final-integrated-overview.md").read_text(encoding="utf-8")
        report = (ROOT / "reports/final-static-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 1500)
        for token in ("Skip to main content", "<caption>", "scope='col'", "tabindex='0'", "NOT_READY_FOR_STAGE_20"):
            self.assertIn(token, report)

    def test_closeout_manifest_review(self):
        review = self.load("validation/closeout-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["frozen_x1_or_evidence_changes"], [])

    def test_environment_and_skills(self):
        env = self.load("final/environment-version-receipt.json")
        skills = self.load("skills/skill-build-receipt.json")
        self.assertTrue(env["versions_verified_only"])
        self.assertFalse(env["desktop_updated"])
        self.assertEqual(skills["validated_count"], 10)
        self.assertFalse(skills["globally_installed"])

    def test_document_and_growth_contracts(self):
        receipt = self.load("validation/closeout-build-receipt.json")
        self.assertTrue(receipt["valid"])
        self.assertLess(receipt["owner_generated_file_count"], 15000)
        self.assertEqual(receipt["expected_scoped_tests"], 69)


if __name__ == "__main__":
    unittest.main()
