from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v649-v7"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V649V7X1Tests(unittest.TestCase):
    def test_exact_twenty_proposals_and_fields(self):
        payload = load("x1-proposals.json")
        self.assertEqual(payload["prior_frozen_count"], 700)
        self.assertEqual(payload["new_frozen_count"], 20)
        self.assertEqual(payload["frozen_total_after_x1"], 720)
        self.assertFalse(payload["x2_started"])
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane",
            "official_or_primary_source_needs", "concrete_artifacts",
            "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
            "expected_disposition", "novelty_against_700_frozen_proposals",
        }
        self.assertEqual(len(payload["proposals"]), 20)
        for row in payload["proposals"]:
            self.assertTrue(required <= set(row))
            self.assertIn(row["expected_disposition"], payload["outcome_classes"])

    def test_expected_distribution_and_novelty(self):
        payload = load("x1-proposals.json")
        counts = {label: 0 for label in payload["outcome_classes"]}
        for row in payload["proposals"]:
            counts[row["expected_disposition"]] += 1
        self.assertEqual(counts, {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        audit = load("provenance/proposal-collision-audit.json")
        self.assertEqual(audit["prior_count"], 700)
        self.assertEqual(audit["new_count"], 20)
        self.assertEqual(audit["exact_collision_count"], 0)
        self.assertTrue(all(row["decision"] == "distinct" for row in audit["rows"]))

    def test_portfolio_floors_and_caps(self):
        self.assertEqual(load("portfolios/safe-now-plan.json")["count"], 40)
        self.assertEqual(load("portfolios/candidate-plan.json")["count"], 30)
        self.assertEqual(load("portfolios/skill-plan.json")["count"], 20)
        self.assertEqual(load("portfolios/runner-plan.json")["count"], 10)
        self.assertEqual(load("portfolios/clean-fix-refine-plan.json")["count"], 40)
        self.assertEqual(load("validation/x1-synthetic-mutation-plan.json")["count"], 100)
        self.assertTrue(load("portfolios/safe-now-plan.json")["cap_is_not_quota"])

    def test_x1_separation_and_retained_failures(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["stage"], "x1_frozen_not_executed")
        self.assertIsNone(truth["observed_distribution"])
        self.assertFalse(truth["x2_started"])
        self.assertFalse(truth["replay_used"])
        negatives = load("retained-negative-register.json")
        self.assertEqual(negatives["inherited_effective"], 5199)
        self.assertEqual(negatives["x1_operational"], 9)
        self.assertFalse(negatives["negative_erased"])

    def test_method_flow_and_workflow(self):
        ledger = load("method-flow/method-flow-ledger.json")
        frozen_ids = {f"V6497-M{i:02d}" for i in range(1, 10)}
        methods = [row for row in ledger["methods"] if row["method_id"] in frozen_ids]
        witnesses = [row for row in ledger["witnesses"] if row["method_id"] in frozen_ids]
        self.assertEqual(len(methods), 9)
        self.assertEqual(sum(row["result"] == "fail" for row in witnesses), 9)
        self.assertEqual(sum(row["result"] == "pass" for row in witnesses), 9)
        workflow = load("workflow/plan-refinement-receipt.json")
        self.assertTrue(workflow["valid"])
        self.assertEqual(workflow["assignment_count"], 90)
        self.assertEqual(workflow["next_owner"], "Elaren Kestrel")
        self.assertFalse(workflow["future_sibling_identity_set"])

    def test_manifest_privacy_and_gates(self):
        privacy = load("validation/x1-staged-privacy.json")
        self.assertEqual(privacy["pattern_class_count"], 5)
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        review = load("validation/x1-staged-review.json")
        self.assertTrue(review["x1_only"])
        self.assertTrue(review["passed"])
        self.assertEqual(review["x2_implementation_paths"], [])
        gates = load("exact-open-gate-register.json")
        self.assertTrue(gates["none_silently_closed"])
        self.assertEqual(gates["projected_open_gaps"], 41)
        self.assertEqual(gates["projected_exact_gates"], 42)


if __name__ == "__main__":
    unittest.main()
