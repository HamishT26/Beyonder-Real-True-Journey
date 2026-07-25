"""X1-only tests for Tavian Sol v654-v6."""
import json
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v654-v6"
X1_COMMIT = subprocess.check_output(
    ["git", "rev-list", "--all", "--max-count=1", "--fixed-strings", "--grep=feat(ghc-family): freeze Tavian v654-v6 x1"],
    cwd=REPO,
    text=True,
).strip()

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV654V6X1(unittest.TestCase):
    def test_proposals_and_expected_dispositions(self):
        data = load("preregistration/proposals.json")
        self.assertEqual(data["proposal_count"], 30)
        self.assertEqual(data["expected_disposition_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertTrue(all("observed_outcome" not in p for p in data["proposals"]))
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertTrue(all(required <= set(p) for p in data["proposals"]))
    def test_frozen_chain_and_novelty(self):
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (1810, 30, 1840))
        audit = load("provenance/semantic-novelty-audit.json")
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["manual_mechanism_review_count"], 30)
        self.assertLess(max(row["token_jaccard"] for row in audit["rows"]), 0.60)
    def test_portfolios_and_mutations_are_frozen(self):
        packet = load("portfolios/expanded-portfolio-plan.json")
        self.assertEqual(packet["counts"], {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})
        self.assertTrue(all(not row["completion_credit"] for key in packet["portfolios"] for row in packet["portfolios"][key]))
        mutations = load("validation/preregistered-mutation-plan.json")
        self.assertEqual(mutations["count"], 150)
        self.assertTrue(all(row["execution_state"] == "frozen_unexecuted" for row in mutations["mutations"]))
    def test_sources_truth_and_gates(self):
        self.assertEqual(load("sources/source-ledger.json")["source_count"], 13)
        truth = load("truth/x1-phase-truth.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED")
        self.assertFalse(truth["independent_reproduction_claimed"])
    def test_failures_method_flow_and_workflow(self):
        negatives = load("truth/retained-negative-register.json")
        self.assertEqual((negatives["inherited_effective"], negatives["x1_operational_count"], negatives["effective_after_x1"]), (11510, 9, 11519))
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertEqual(len(ledger["methods"]), 83)
        self.assertEqual(sum(w["result"] == "fail" for w in ledger["witnesses"]), 83)
        self.assertEqual(sum(w["result"] == "pass" for w in ledger["witnesses"]), 83)
        workflow = load("workflow/workflow-plan-refinement.json")
        self.assertTrue(workflow["valid"])
        self.assertFalse(workflow["requires_user_confirmation"])
    def test_route_privacy_and_x1_only(self):
        route = load("provenance/successor-authority-invariant.json")
        self.assertEqual((route["created_count"], route["forked_count"], route["delegated_count"], route["contacted_count"]), (0, 0, 0, 0))
        self.assertEqual(route["state"], "ACTIVE_CURRENT_PHASE_ELAREN_PREPARED_TERMINAL_GATE_REQUIRED")
        self.assertEqual(load("validation/x1-staged-privacy.json")["confirmed_hit_count"], 0)
        historical_surface = subprocess.run(
            ["git", "cat-file", "-e", f"{X1_COMMIT}:docs/tavian-sol/v654-v6/surfaces"],
            cwd=REPO,
            capture_output=True,
        )
        self.assertNotEqual(historical_surface.returncode, 0)
        self.assertTrue(load("validation/x1-staged-review.json")["x1_only"])

if __name__ == "__main__":
    unittest.main()
