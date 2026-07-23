"""X1-only tests for Sylven Arc v652-v4."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v652-v4"


class TestSylvenV652V4X1(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_exactly_thirty_proposals(self):
        payload = self.load("preregistration/proposals.json")
        self.assertEqual(payload["proposal_count"], 30)
        self.assertEqual(len(payload["proposals"]), 30)
        self.assertFalse(payload["observed_outcomes_present"])

    def test_required_proposal_fields(self):
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs",
            "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        for row in self.load("preregistration/proposals.json")["proposals"]:
            self.assertTrue(required <= set(row))

    def test_novelty_chain(self):
        novelty = self.load("provenance/semantic-novelty-audit.json")
        chain = self.load("provenance/frozen-chain-proposal-index.json")
        self.assertTrue(novelty["valid"])
        self.assertLess(novelty["maximum_token_jaccard"], 0.60)
        self.assertEqual(chain["count"], 1300)
        self.assertEqual(len(chain["prior_proposals"] + chain["new_proposals"]), 1300)
        inherited_ids = {x["proposal_id"] for x in chain["prior_proposals"]}
        new_ids = [x["proposal_id"] for x in chain["new_proposals"]]
        self.assertEqual(len(set(new_ids)), 30)
        self.assertFalse(inherited_ids & set(new_ids))

    def test_expected_outcomes(self):
        counts = self.load("preregistration/proposals.json")["expected_disposition_counts"]
        self.assertEqual(counts, {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})

    def test_portfolios(self):
        counts = self.load("portfolios/expanded-portfolio-plan.json")["counts"]
        self.assertEqual(counts, {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})

    def test_x1_only(self):
        truth = self.load("truth/x1-phase-truth.json")
        self.assertEqual(truth["lifecycle"], "x1_frozen_not_executed")
        self.assertEqual(truth["observed_outcome_count"], 0)
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")

    def test_failures_retained(self):
        negatives = self.load("truth/retained-negative-register.json")
        flow = self.load("method-flow/method-flow-ledger.json")
        self.assertEqual(negatives["inherited_effective"], 8383)
        self.assertEqual(negatives["x1_operational_count"], 12)
        self.assertEqual(flow["counts"]["witness_results"]["fail"], 12)
        self.assertEqual(flow["counts"]["witness_results"]["pass"], 12)

    def test_sources_resolve(self):
        proposals = self.load("preregistration/proposals.json")["proposals"]
        source_ids = {x["source_id"] for x in self.load("sources/source-ledger.json")["sources"]}
        self.assertTrue(all(set(row["official_or_primary_source_needs"]) <= source_ids for row in proposals))

    def test_privacy_and_manifest(self):
        self.assertEqual(self.load("validation/x1-staged-privacy.json")["confirmed_hit_count"], 0)
        review = self.load("validation/x1-staged-review.json")
        self.assertTrue(review["x1_only"])
        self.assertEqual(review["out_of_scope_paths"], [])
        self.assertEqual(review["x2_implementation_paths"], [])

    def test_overview_and_document_caps(self):
        overview = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 1500)
        caps = self.load("validation/document-cap-receipt.json")
        self.assertTrue(caps["valid"])


if __name__ == "__main__":
    unittest.main()
