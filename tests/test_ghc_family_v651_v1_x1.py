"""X1-only tests for Sable Rook v651-v1."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sable-rook/v651-v1"

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV651V1X1(unittest.TestCase):
    def test_exact_proposals_and_expected_dispositions(self):
        data = load("preregistration/proposals.json")
        self.assertEqual(data["proposal_count"], 20)
        self.assertEqual(data["expected_disposition_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(len({p["proposal_id"] for p in data["proposals"]}), 20)
        self.assertTrue(all("observed_outcome" not in p for p in data["proposals"]))
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertTrue(all(required <= set(p) for p in data["proposals"]))
    def test_frozen_chain_and_novelty(self):
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (900, 20, 920))
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["valid"])
        self.assertTrue(all(row["passes"] for row in audit["rows"]))
    def test_portfolios_and_mutations_are_unexecuted(self):
        p = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(p["counts"], {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40})
        self.assertTrue(all(not row["completion_credit"] for rows in p["portfolios"].values() for row in rows))
        m = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(m["count"], 100)
        self.assertTrue(all(row["execution_state"] == "frozen_unexecuted" for row in m["mutations"]))
    def test_truth_and_sources(self):
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(truth["independent_reproduction_claimed"])
        sources = load("sources/source-ledger.json")
        self.assertEqual(set(sources["allowed_statuses"]), {"current", "stable", "draft", "watch"})
        self.assertEqual(len(sources["sources"]), 23)
    def test_failure_and_method_flow_preserved(self):
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 6443)
        self.assertGreaterEqual(negatives["x1_operational_count"], 1)
        flow = load("method-flow/method-flow-state.json")
        self.assertGreaterEqual(flow["counts"]["witness_results"]["fail"], 1)
        self.assertGreaterEqual(flow["counts"]["witness_results"]["pass"], 1)
    def test_workflow_and_document_caps(self):
        workflow = load("workflow/workflow-plan-refinement.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
        for path in ROOT.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 6000, path)
    def test_x1_privacy(self):
        privacy = load("validation/x1-staged-privacy.json")
        self.assertEqual(privacy["confirmed_hit_count"], 0)

if __name__ == "__main__":
    unittest.main()
