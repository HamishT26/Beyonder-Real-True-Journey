from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v650-v2"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class IlyraV650V2X1Tests(unittest.TestCase):
    def test_exact_proposal_chain_and_distribution(self):
        payload = load("x1-proposals.json")
        self.assertEqual(payload["prior_frozen_count"], 760)
        self.assertEqual(payload["new_frozen_count"], 20)
        self.assertEqual(payload["frozen_total_after_x1"], 780)
        self.assertFalse(payload["x2_started"])
        self.assertEqual(Counter(row["expected_disposition"] for row in payload["proposals"]), {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})

    def test_proposals_have_required_fields_and_unique_ids(self):
        rows = load("x1-proposals.json")["proposals"]
        required = {"proposal_id", "title", "pillar", "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane", "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates", "expected_disposition"}
        self.assertEqual(len({row["proposal_id"] for row in rows}), 20)
        self.assertEqual(len({row["title"] for row in rows}), 20)
        for row in rows:
            self.assertTrue(required <= row.keys())
            self.assertTrue(row["protected_gates"])
            self.assertEqual(len(row["concrete_artifacts"]), 3)

    def test_novelty_audit_is_exact_collision_free(self):
        audit = load("provenance/proposal-collision-audit.json")
        self.assertEqual(audit["prior_count"], 760)
        self.assertEqual(audit["new_count"], 20)
        self.assertEqual(audit["exact_collision_count"], 0)
        self.assertTrue(audit["semantic_review_completed"])
        self.assertTrue(all(row["decision"] == "distinct_after_semantic_review" for row in audit["rows"]))

    def test_source_status_vocabulary_and_boundaries(self):
        payload = load("sources/source-ledger.json")
        self.assertEqual(set(payload["status_counts"]), {"current", "stable", "draft", "watch"})
        self.assertGreater(payload["status_counts"]["current"], 0)
        self.assertGreater(payload["status_counts"]["stable"], 0)
        self.assertGreater(payload["status_counts"]["draft"], 0)
        self.assertGreater(payload["status_counts"]["watch"], 0)
        self.assertTrue(all("not observation" in row["use_boundary"] for row in payload["sources"]))

    def test_expanded_portfolios_are_frozen_only(self):
        expected = {
            "portfolios/safe-now-plan.json": 40,
            "portfolios/candidate-plan.json": 30,
            "portfolios/skill-plan.json": 20,
            "portfolios/runner-plan.json": 10,
            "portfolios/clean-fix-refine-plan.json": 40,
        }
        for relative, count in expected.items():
            payload = load(relative)
            self.assertEqual(payload["count"], count)
        safe = load("portfolios/safe-now-plan.json")
        self.assertTrue(safe["cap_is_not_quota"])
        self.assertTrue(all(row["x1_state"] == "frozen_not_executed" for row in safe["tasks"]))

    def test_mutations_are_preregistered_not_executed(self):
        payload = load("validation/x1-synthetic-mutation-plan.json")
        self.assertEqual(payload["count"], 100)
        self.assertEqual(payload["executed_count"], 0)
        self.assertTrue(all(row["x1_state"] == "preregistered_not_executed" and not row["completion_credit"] for row in payload["mutations"]))

    def test_startup_failures_are_retained(self):
        payload = load("retained-negative-register.json")
        self.assertEqual(payload["inherited_effective"], 5579)
        self.assertEqual(payload["x1_operational"], 8)
        self.assertEqual(payload["effective_at_x1"], 5587)
        self.assertFalse(payload["negative_erased"])
        self.assertEqual(len(payload["new_negatives"]), 8)

    def test_method_flow_preserves_fail_and_pass_witnesses(self):
        ledger = load("method-flow/method-flow-ledger.json")
        self.assertEqual(ledger["counts"]["methods"], 8)
        self.assertEqual(ledger["counts"]["witnesses"], 16)
        self.assertEqual(ledger["counts"]["witness_results"], {"fail": 8, "pass": 8})
        self.assertTrue(all(method["recommendation_state"] == "preferred" for method in ledger["methods"]))

    def test_workflow_plan_is_valid_and_owner_is_unambiguous(self):
        receipt = load("workflow/workflow-plan-validation.json")
        plan = load("workflow/workflow-plan-refinement.json")
        self.assertTrue(receipt["valid"])
        self.assertTrue(plan["valid"])
        self.assertFalse(plan["requires_user_confirmation"])

    def test_gates_and_terminal_verdict_remain_open(self):
        gates = load("exact-open-gate-register.json")
        truth = load("phase-truth.json")
        self.assertEqual(gates["projected_open_gaps"], 44)
        self.assertEqual(gates["projected_exact_gates"], 45)
        self.assertTrue(gates["none_silently_closed"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")

    def test_x1_review_has_no_x2_or_privacy_leak(self):
        review = load("validation/x1-staged-review.json")
        privacy = load("validation/x1-staged-privacy.json")
        self.assertTrue(review["passed"])
        self.assertTrue(review["x1_only"])
        self.assertEqual(review["x2_implementation_paths"], [])
        self.assertEqual(review["privacy_confirmed_hits"], 0)
        self.assertEqual(privacy["confirmed_hit_count"], 0)

    def test_source_and_owned_lane_receipt(self):
        startup = load("environment/startup-receipt.json")
        self.assertEqual(startup["source_head"], "f47cd5145647965935f80d67751f0e09d9740540")
        self.assertEqual(startup["source_phase_commits"], 4)
        self.assertEqual(startup["source_merges"], 0)
        self.assertTrue(startup["owned_fast_forward_only"])
        self.assertTrue(startup["owned_four_way_equal_before_x1"])


if __name__ == "__main__":
    unittest.main()
