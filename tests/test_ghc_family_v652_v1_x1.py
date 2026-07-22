"""X1-only tests for Sable Rook v652-v1."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sable-rook/v652-v1"

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV652V1X1(unittest.TestCase):
    def test_exact_proposals_and_expected_dispositions(self):
        data = load("preregistration/proposals.json")
        self.assertEqual(data["proposal_count"], 30)
        self.assertEqual(data["expected_disposition_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(len({p["proposal_id"] for p in data["proposals"]}), 30)
        self.assertTrue(all("observed_outcome" not in p for p in data["proposals"]))
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertTrue(all(required <= set(p) for p in data["proposals"]))
    def test_frozen_chain_and_novelty(self):
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(index["prior_count"], 1180)
        self.assertEqual(index["new_count"], 30)
        self.assertEqual(index["count"], 1210)
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["valid"])
        self.assertTrue(all(row["passes"] for row in audit["rows"]))
        self.assertLess(max(row["token_jaccard"] for row in audit["rows"]), 0.60)
    def test_portfolios_skills_runners_and_mutations(self):
        packet = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(packet["counts"], {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})
        self.assertTrue(all(not row["completion_credit"] for key in packet["portfolios"] for row in packet["portfolios"][key]))
        mutations = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(mutations["count"], 150)
        self.assertTrue(all(row["execution_state"] == "frozen_unexecuted" for row in mutations["mutations"]))
    def test_source_and_gate_classes(self):
        sources = load("sources/source-ledger.json")
        self.assertEqual(set(sources["allowed_statuses"]), {"current", "stable", "draft", "watch"})
        self.assertEqual(sources["source_count"], 36)
        self.assertEqual(next(s for s in sources["sources"] if s["source_id"] == "SRC-FIDO-CREDENTIAL-EXCHANGE")["status"], "draft")
        self.assertEqual(next(s for s in sources["sources"] if s["source_id"] == "SRC-PANSTARRS-DR2")["status"], "current")
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(truth["independent_reproduction_claimed"])
    def test_failures_method_flow_and_workflow(self):
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 7856)
        self.assertEqual(negatives["x1_operational_count"], 6)
        self.assertEqual(negatives["effective_after_x1"], 7862)
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertGreaterEqual(sum(w["result"] == "fail" for w in ledger["witnesses"]), 6)
        self.assertGreaterEqual(sum(w["result"] == "pass" for w in ledger["witnesses"]), 6)
        workflow = load("workflow/workflow-plan-refinement.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
    def test_future_cli_seats_remain_placeholders(self):
        seats = load("provenance/future-cli-placeholder-invariant.json")
        self.assertEqual(seats["prepared_placeholder_count"], 8)
        self.assertEqual(seats["named_count"], 0)
        self.assertEqual(seats["created_count"], 0)
        self.assertEqual(seats["launched_count"], 0)
    def test_document_caps_privacy_and_x1_only(self):
        for path in ROOT.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)
        privacy = load("validation/x1-staged-privacy.json")
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertFalse((ROOT / "surfaces").exists())
        review = load("validation/x1-staged-review.json")
        self.assertTrue(review["x1_only"])
        self.assertEqual(review["x2_implementation_paths"], [])
        self.assertEqual(review["x2_outcome_paths"], [])

if __name__ == "__main__":
    unittest.main()
