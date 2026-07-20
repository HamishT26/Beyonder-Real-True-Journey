from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v650-v3"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V650V3X1Tests(unittest.TestCase):
    def test_twenty_novel_proposals_and_distribution(self):
        packet = load("x1-proposals.json")
        self.assertEqual(len(packet["proposals"]), 20)
        self.assertEqual(packet["prior_frozen_count"], 780)
        self.assertEqual(packet["frozen_total_after_x1"], 800)
        self.assertEqual(packet["expected_distribution"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertFalse(packet["x2_started"])
        audit = load("provenance/proposal-collision-audit.json")
        self.assertEqual(audit["exact_collision_count"], 0)
        self.assertEqual(audit["quarantine_count"], 0)

    def test_required_fields_and_outcome_vocabulary(self):
        required = {"hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        proposals = load("x1-proposals.json")["proposals"]
        for proposal in proposals:
            self.assertTrue(required <= proposal.keys())
            self.assertIn(proposal["expected_disposition"], {"completed", "represented", "open_gap", "exact_gate"})

    def test_expanded_portfolios_are_frozen(self):
        self.assertEqual(load("portfolios/safe-now-plan.json")["count"], 40)
        self.assertEqual(load("portfolios/candidate-plan.json")["count"], 30)
        self.assertEqual(load("portfolios/skill-plan.json")["count"], 20)
        self.assertEqual(load("portfolios/runner-plan.json")["count"], 10)
        self.assertEqual(load("portfolios/clean-fix-refine-plan.json")["count"], 40)
        self.assertEqual(load("validation/x1-synthetic-mutation-plan.json")["count"], 100)
        self.assertEqual(load("validation/x1-synthetic-mutation-plan.json")["executed_count"], 0)

    def test_sources_and_identity_boundaries(self):
        sources = load("sources/source-ledger.json")
        self.assertGreaterEqual(len(sources["sources"]), 20)
        self.assertTrue(set(sources["status_counts"]) <= {"current", "stable", "draft", "watch"})
        identity = load("identity-receipt.json")
        self.assertTrue(identity["relational_only"])
        self.assertIn("personhood", identity["not_evidence_of"])

    def test_negatives_and_gates_are_retained(self):
        negatives = load("retained-negative-register.json")
        self.assertEqual(negatives["activation_baseline"], 5692)
        self.assertEqual(negatives["x1_operational"], 11)
        self.assertEqual(negatives["effective_total"], 5703)
        self.assertEqual(negatives["erased"], 0)
        gates = load("exact-open-gate-register.json")
        self.assertEqual(gates["projected_open_gaps"], 45)
        self.assertEqual(gates["projected_exact_gates"], 46)

    def test_method_flow_runner_was_used(self):
        state = load("method-flow/method-flow-state.json")
        self.assertEqual(len(state["methods"]), 11)
        self.assertEqual(len(state["witnesses"]), 22)
        self.assertEqual(state["counts"]["witness_results"]["fail"], 11)
        self.assertEqual(state["counts"]["witness_results"]["pass"], 11)
        self.assertTrue(load("method-flow/method-flow-validation.json")["valid"])

    def test_x1_truth_is_held(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["state"], "X1_FROZEN_NOT_EXECUTED")
        self.assertFalse(truth["x2_started"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(load("orchestration/terminal-route-state.json")["state"], "HELD_X1")


if __name__ == "__main__":
    unittest.main()
