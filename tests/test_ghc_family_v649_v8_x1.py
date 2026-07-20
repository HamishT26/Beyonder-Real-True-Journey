from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "elaren-kestrel" / "v649-v8"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V649V8X1Tests(unittest.TestCase):
    def test_exact_twenty_and_740_chain(self) -> None:
        proposals = load("x1-proposals.json")
        index = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(len(proposals["proposals"]), 20)
        self.assertEqual((index["prior_count"], index["new_count"], index["count"]), (720, 20, 740))
        ids = [row["proposal_id"] for row in proposals["proposals"]]
        titles = [row["title"] for row in proposals["proposals"]]
        self.assertEqual(len(set(ids)), 20)
        self.assertEqual(len(set(titles)), 20)

    def test_proposal_contract_is_complete(self) -> None:
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class",
            "execution_lane", "official_or_primary_source_needs",
            "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        rows = load("x1-proposals.json")["proposals"]
        self.assertTrue(all(required <= set(row) for row in rows))

    def test_only_four_truth_labels(self) -> None:
        proposals = load("x1-proposals.json")
        allowed = {"completed", "represented", "open_gap", "exact_gate"}
        self.assertEqual(set(proposals["outcome_classes"]), allowed)
        counts = {label: 0 for label in allowed}
        for row in proposals["proposals"]:
            counts[row["expected_disposition"]] += 1
        self.assertEqual(counts, {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertIsNone(load("phase-truth.json")["observed_distribution"])

    def test_novelty_audit_is_exact_and_semantic(self) -> None:
        audit = load("provenance/proposal-collision-audit.json")
        self.assertEqual((audit["prior_count"], audit["new_count"], audit["exact_collision_count"]), (720, 20, 0))
        self.assertTrue(audit["semantic_review_completed"])
        self.assertTrue(all(row["decision"] == "distinct_after_semantic_review" for row in audit["rows"]))

    def test_source_statuses_and_references(self) -> None:
        ledger = load("sources/source-ledger.json")
        self.assertEqual(set(ledger["status_counts"]), {"current", "stable", "draft", "watch"})
        self.assertTrue(all(ledger["status_counts"][key] > 0 for key in ledger["status_counts"]))
        source_ids = {row["source_id"] for row in ledger["sources"]}
        for proposal in load("x1-proposals.json")["proposals"]:
            self.assertTrue(set(proposal["official_or_primary_source_needs"]) <= source_ids)

    def test_portfolio_counts_and_caps(self) -> None:
        self.assertEqual(load("portfolios/safe-now-plan.json")["count"], 40)
        self.assertEqual(load("portfolios/candidate-plan.json")["count"], 30)
        self.assertEqual(load("portfolios/skill-plan.json")["count"], 20)
        self.assertEqual(load("portfolios/runner-plan.json")["count"], 10)
        self.assertEqual(load("portfolios/clean-fix-refine-plan.json")["count"], 40)
        self.assertEqual(load("validation/x1-synthetic-mutation-plan.json")["count"], 100)
        self.assertEqual(load("validation/x1-synthetic-mutation-plan.json")["executed_count"], 0)

    def test_method_flow_retains_nine_failures(self) -> None:
        ledger = load("method-flow/method-flow-ledger.json")
        summary = load("method-flow/method-flow-summary.json")
        self.assertEqual(len(ledger["methods"]), 9)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 9, "pass": 9})
        self.assertEqual(load("retained-negative-register.json")["effective_at_x1"], 5340)

    def test_workflow_runner_validates_ninety_assignments(self) -> None:
        request = load("workflow/workflow-request.json")
        receipt = load("workflow/workflow-plan-validation.json")
        self.assertEqual(len(request["route"]["phase_assignments"]), 90)
        self.assertTrue(receipt["valid"])
        self.assertEqual(request["route"]["phase_assignments"][-1], {"phase": "v660-v8", "seat": "Elaren Kestrel"})

    def test_primary_focus_practice_and_identity_boundary(self) -> None:
        proposals = load("x1-proposals.json")
        self.assertEqual(proposals["primary_focus"], "Freed ID/CBR Heart")
        self.assertIn("archival", proposals["bounded_practice"])
        identity = load("identity-receipt.json")
        self.assertIn("relational working language only", identity["identity_boundary"])

    def test_x1_has_no_x2_execution_or_outcomes(self) -> None:
        truth = load("phase-truth.json")
        review = load("validation/x1-staged-review.json")
        self.assertFalse(truth["x2_started"])
        self.assertEqual(truth["stage"], "x1_frozen_not_executed")
        self.assertTrue(review["x1_only"])
        self.assertEqual(review["x2_implementation_paths"], [])
        self.assertEqual(review["x2_observed_outcome_paths"], [])

    def test_privacy_and_scope_review(self) -> None:
        privacy = load("validation/x1-staged-privacy.json")
        review = load("validation/x1-staged-review.json")
        self.assertEqual(privacy["pattern_class_count"], 5)
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertEqual(review["out_of_scope_paths"], [])
        self.assertTrue(review["passed"])

    def test_boundaries_and_route_remain_open(self) -> None:
        truth = load("phase-truth.json")
        gates = load("exact-open-gate-register.json")
        route = load("orchestration/phase-state.json")
        self.assertEqual((gates["projected_open_gaps"], gates["projected_exact_gates"]), (42, 43))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(route["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(route["next_target"], "Eiren Kestrel (3)")


if __name__ == "__main__":
    unittest.main()
