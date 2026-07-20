from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v650-v5"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def load_at_x1(relative: str):
    phase_truth = load("phase-truth.json")
    x1_commit = phase_truth.get("x1_commit")
    if not x1_commit:
        return load(relative)
    completed = subprocess.run(
        ["git", "show", f"{x1_commit}:docs/tamar-vey/v650-v5/{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(completed.stdout)


class TamarV650V5X1Tests(unittest.TestCase):
    def test_twenty_novel_proposals_and_distribution(self):
        packet = load("x1-proposals.json")
        self.assertEqual(len(packet["proposals"]), 20)
        self.assertEqual(packet["prior_frozen_count"], 820)
        self.assertEqual(packet["frozen_total_after_x1"], 840)
        self.assertEqual(
            packet["expected_distribution"],
            {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        )
        self.assertFalse(packet["x2_started"])
        audit = load("provenance/proposal-collision-audit.json")
        self.assertEqual(audit["screened_count"], 20)
        self.assertEqual(audit["exact_collision_count"], 0)
        self.assertEqual(audit["quarantine_count"], 0)
        self.assertLess(audit["maximum_token_jaccard"], 0.50)
        self.assertGreaterEqual(len(audit["rejected_near_neighbors"]), 5)

    def test_required_fields_and_outcome_vocabulary(self):
        required = {
            "hypothesis",
            "null_or_failure_condition",
            "approval_class",
            "execution_lane",
            "official_or_primary_source_needs",
            "concrete_artifacts",
            "falsifier_or_acceptance_gate",
            "rollback_or_recovery",
            "protected_gates",
            "expected_disposition",
        }
        proposals = load("x1-proposals.json")["proposals"]
        self.assertEqual(len({row["proposal_id"] for row in proposals}), 20)
        for proposal in proposals:
            self.assertTrue(required <= proposal.keys())
            self.assertIn(
                proposal["expected_disposition"],
                {"completed", "represented", "open_gap", "exact_gate"},
            )
            self.assertGreaterEqual(len(proposal["protected_gates"]), 10)

    def test_expanded_portfolios_are_frozen(self):
        self.assertEqual(load("portfolios/safe-now-plan.json")["count"], 40)
        self.assertEqual(load("portfolios/candidate-plan.json")["count"], 30)
        self.assertEqual(load("portfolios/skill-plan.json")["count"], 20)
        self.assertEqual(load("portfolios/runner-plan.json")["count"], 10)
        self.assertEqual(
            load("portfolios/clean-fix-refine-plan.json")["count"], 40
        )
        mutations = load("validation/x1-synthetic-mutation-plan.json")
        self.assertEqual(mutations["count"], 100)
        self.assertEqual(mutations["executed_count"], 0)
        self.assertEqual(
            {row["x1_state"] for row in load("portfolios/safe-now-plan.json")["tasks"]},
            {"frozen_not_executed"},
        )

    def test_sources_identity_and_practice_boundaries(self):
        sources = load("sources/source-ledger.json")
        self.assertGreaterEqual(len(sources["sources"]), 20)
        self.assertTrue(set(sources["status_counts"]) <= {"current", "stable", "draft", "watch"})
        identity = load("identity-receipt.json")
        self.assertTrue(identity["relational_only"])
        self.assertIn("personhood", identity["not_evidence_of"])
        focus = load("primary-focus-receipt.json")
        self.assertEqual(focus["primary"], "Freed ID and CBR Heart")
        self.assertTrue(focus["practice_is_learning_lens_only"])

    def test_negatives_and_gates_are_retained(self):
        negatives = load_at_x1("retained-negative-register.json")
        self.assertEqual(negatives["activation_baseline"], 5925)
        operational = [
            row for row in negatives["entries"] if row["class"] == "x1_operational"
        ]
        self.assertEqual(negatives["x1_operational"], len(operational))
        self.assertEqual(
            negatives["effective_total"],
            negatives["activation_baseline"] + len(operational),
        )
        self.assertEqual(negatives["erased"], 0)
        gates = load_at_x1("exact-open-gate-register.json")
        self.assertEqual(gates["inherited_open_gaps"], 46)
        self.assertEqual(gates["inherited_exact_gates"], 47)
        self.assertEqual(gates["projected_open_gaps_after_x2"], 47)
        self.assertEqual(gates["projected_exact_gates_after_x2"], 48)

    def test_method_flow_runner_was_used(self):
        state = load_at_x1("method-flow/method-flow-state.json")
        negative_count = load_at_x1("retained-negative-register.json")["x1_operational"]
        self.assertEqual(len(state["methods"]), negative_count)
        corrections = [
            row for row in state["witnesses"] if "-WPASS-CORR" in row["witness_id"]
        ]
        self.assertEqual(len(corrections), 2)
        self.assertEqual(len(state["witnesses"]), negative_count * 2 + len(corrections))
        self.assertEqual(state["counts"]["witness_results"]["fail"], negative_count)
        self.assertEqual(
            state["counts"]["witness_results"]["pass"],
            negative_count + len(corrections),
        )
        self.assertEqual(
            {row["witness_id"] for row in corrections},
            {"V6505-M17-WPASS-CORR1", "V6505-M18-WPASS-CORR1"},
        )
        self.assertEqual({row["result"] for row in corrections}, {"pass"})
        self.assertTrue(load_at_x1("method-flow/method-flow-validation.json")["valid"])
        self.assertEqual(
            {row["recommendation_state"] for row in state["methods"]}, {"preferred"}
        )

    def test_file_rotation_and_environment_boundaries(self):
        counts = load("environment/file-count-receipt.json")
        self.assertGreater(counts["tracked_checkout_files_at_inherited_head"], 15000)
        self.assertEqual(counts["tamar_generated_files_before_phase"], 0)
        self.assertFalse(counts["inherited_baseline_triggers_rotation"])
        startup = load("environment/startup-receipt.json")
        self.assertEqual(startup["source_phase_commits"], 3)
        self.assertEqual(startup["source_merges"], 0)
        self.assertEqual(startup["source_manifest_contracts_verified"], 4)
        self.assertFalse(startup["sandbox_or_hyper_v_launched"])

    def test_x1_truth_and_route_are_held(self):
        truth = load_at_x1("phase-truth.json")
        self.assertEqual(truth["state"], "X1_FROZEN_NOT_EXECUTED")
        self.assertFalse(truth["x2_started"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        route = load_at_x1("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "HELD_X1")
        self.assertFalse(route["sent"])


if __name__ == "__main__":
    unittest.main()
