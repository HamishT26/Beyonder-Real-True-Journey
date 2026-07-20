"""Bounded x1-only tests for Sylven Arc v650-v6 preregistration."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v650_v6_phase_data as d  # noqa: E402


ROOT = REPO / d.PHASE_ROOT


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestSylvenV650V6X1(unittest.TestCase):
    def test_exact_proposal_count_and_ids(self):
        self.assertEqual(len(d.PROPOSALS), 20)
        self.assertEqual(
            [row["proposal_id"] for row in d.PROPOSALS],
            [f"V6506-P{index:02d}" for index in range(1, 21)],
        )

    def test_required_proposal_fields_are_present(self):
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
        for row in d.PROPOSALS:
            self.assertTrue(required.issubset(row), row["proposal_id"])
            self.assertTrue(all(row[key] for key in required), row["proposal_id"])

    def test_expected_distribution_is_exact(self):
        self.assertEqual(
            Counter(row["expected_disposition"] for row in d.PROPOSALS),
            Counter(completed=14, represented=4, open_gap=1, exact_gate=1),
        )

    def test_only_permitted_outcome_vocabulary_is_used(self):
        self.assertEqual(d.OUTCOME_CLASSES, ["completed", "represented", "open_gap", "exact_gate"])
        self.assertLessEqual(
            {row["expected_disposition"] for row in d.PROPOSALS}, set(d.OUTCOME_CLASSES)
        )

    def test_every_proposal_has_a_source(self):
        source_ids = {row["source_id"] for row in d.SOURCES}
        for row in d.PROPOSALS:
            self.assertTrue(row["official_or_primary_source_needs"])
            self.assertLessEqual(set(row["official_or_primary_source_needs"]), source_ids)

    def test_source_status_vocabulary_is_exact(self):
        self.assertEqual(d.SOURCE_STATUS_CLASSES, ["current", "stable", "draft", "watch"])
        self.assertLessEqual({row["status"] for row in d.SOURCES}, set(d.SOURCE_STATUS_CLASSES))

    def test_primary_pillar_and_bounded_practice_are_explicit(self):
        self.assertEqual(d.PRIMARY_FOCUS, "GMUT Mind")
        self.assertIn("seed-bank", d.BOUNDED_PRACTICE)
        self.assertIn("synthetic learning and design lens only", d.BOUNDED_PRACTICE)

    def test_all_pillars_remain_visible(self):
        pillars = {row["pillar"] for row in d.PROPOSALS}
        self.assertIn("GMUT Mind", pillars)
        self.assertIn("THOS Body", pillars)
        self.assertIn("Freed ID and CBR Heart", pillars)

    def test_portfolio_floors_are_exact_and_new(self):
        self.assertEqual(len(d.SAFE_TASKS), 40)
        self.assertEqual(len(d.CANDIDATE_TASKS), 30)
        self.assertEqual(len(d.SKILL_IDEAS), 20)
        self.assertEqual(len(d.RUNNER_IDEAS), 10)
        self.assertEqual(len(d.CLEAN_TASKS), 40)
        for collection in (
            d.SAFE_TASKS,
            d.CANDIDATE_TASKS,
            d.SKILL_IDEAS,
            d.RUNNER_IDEAS,
            d.CLEAN_TASKS,
        ):
            self.assertEqual(len(collection), len(set(collection)))

    def test_mutation_plan_is_exactly_one_hundred_and_unexecuted(self):
        plan = load("validation/x1-synthetic-mutation-plan.json")
        self.assertEqual(plan["count"], 100)
        self.assertEqual(len(plan["mutations"]), 100)
        self.assertTrue(all(row["x1_state"] == "preregistered_not_executed" for row in plan["mutations"]))

    def test_x1_contains_no_observed_outcome(self):
        packet = load("x1-proposals.json")
        self.assertEqual(packet["x1_state"], "frozen_not_executed")
        self.assertNotIn("observed_outcome", packet)
        for row in packet["proposals"]:
            self.assertNotIn("observed_outcome", row)

    def test_phase_truth_is_x1_only(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["stage"], "x1_frozen_not_executed")
        self.assertIsNone(truth["observed_distribution"])
        self.assertFalse(truth["x2_started"])
        self.assertEqual(truth["successful_canonical_passes_used"], 0)
        self.assertFalse(truth["post_success_replay_used"])

    def test_inherited_proposal_index_grows_840_to_860(self):
        packet = load("x1-proposals.json")
        frozen = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(packet["prior_frozen_proposal_count"], 840)
        self.assertEqual(packet["frozen_total_after_x1"], 860)
        self.assertEqual(frozen["count"], 860)

    def test_novelty_audit_has_no_collision(self):
        audit = load("provenance/proposal-collision-audit.json")
        self.assertEqual(audit["prior_count"], 840)
        self.assertEqual(audit["new_count"], 20)
        self.assertEqual(audit["exact_collision_count"], 0)
        self.assertLess(audit["maximum_observed_jaccard"], audit["threshold"])
        self.assertTrue(audit["manual_semantic_review_complete"])

    def test_method_flow_retains_failure_and_pass_witnesses(self):
        ledger = load("method-flow/method-flow-state.json")
        self.assertEqual(len(ledger["methods"]), 19)
        self.assertEqual(len(ledger["witnesses"]), 38)
        states = Counter(row["result"] for row in ledger["witnesses"])
        self.assertEqual(states["fail"], 19)
        self.assertEqual(states["pass"], 19)
        self.assertEqual(sum(row["recommendation_state"] == "preferred" for row in ledger["methods"]), 19)

    def test_x1_operational_negatives_are_additive(self):
        register = load("retained-negative-register.json")
        self.assertEqual(register["inherited_effective"], 6056)
        self.assertEqual(register["x1_operational"], 19)
        self.assertEqual(register["effective_at_x1"], 6075)
        self.assertEqual(register["projected_if_all_synthetic_execute_and_reject"], 6175)
        self.assertFalse(register["negative_erased"])

    def test_open_and_exact_gates_are_not_closed(self):
        register = load("exact-open-gate-register.json")
        self.assertEqual(register["inherited_open_gaps"], 47)
        self.assertEqual(register["inherited_exact_gates"], 48)
        self.assertEqual(register["projected_open_gaps_if_expected_dispositions_hold"], 48)
        self.assertEqual(register["projected_exact_gates_if_expected_dispositions_hold"], 49)
        self.assertEqual(register["closed_in_x1"], 0)
        self.assertEqual(register["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_single_pass_budget_is_unused(self):
        plan = load("validation/single-pass-validation-plan.json")
        self.assertFalse(plan["full_repository_suite"])
        self.assertEqual(plan["canonical_successful_pass_budget"], 1)
        self.assertEqual(plan["successful_passes_used"], 0)
        self.assertFalse(plan["post_success_replay"])
        self.assertFalse(plan["detached_replay"])
        self.assertFalse(plan["named_replay"])

    def test_privacy_scan_has_zero_confirmed_hits(self):
        receipt = load("validation/x1-staged-privacy.json")
        self.assertEqual(len(receipt["pattern_classes"]), 5)
        self.assertEqual(receipt["confirmed_hit_count"], 0)
        self.assertEqual(receipt["confirmed_hits"], [])

    def test_manifest_git_blob_parity(self):
        manifest = load("validation/x1-staged-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["self_exclusions"]), 3)
        for row in manifest["entries"]:
            blob = subprocess.check_output(
                ["git", "cat-file", "blob", row["git_blob"]], cwd=REPO
            )
            self.assertEqual(len(blob), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"], row["path"])

    def test_staged_review_is_x1_only(self):
        review = load("validation/x1-staged-review.json")
        self.assertTrue(review["x1_only"])
        self.assertEqual(review["x2_implementation_paths"], [])
        self.assertEqual(review["x2_outcome_paths"], [])
        self.assertEqual(review["privacy_confirmed_hits"], 0)
        self.assertEqual(review["terminal_route"], "PREPARED_NOT_SENT")

    def test_owned_index_is_current_and_phase_scoped(self):
        index = load("ghc-family-index.json")
        self.assertEqual(index["phase"], d.PHASE)
        self.assertEqual(index["owner"], d.OWNER)

    def test_terminal_route_is_not_claimed(self):
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["target_title"], "Eiren Kestrel")
        self.assertFalse(route["target_resolved"])
        self.assertEqual(route["messages_sent"], 0)

    def test_terminal_verdict_remains_not_ready(self):
        self.assertEqual(load("phase-truth.json")["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertIn("NOT_READY_FOR_STAGE_20", (ROOT / "integrated-overview.md").read_text(encoding="utf-8"))

    def test_overview_is_three_page_equivalent_and_bounded(self):
        words = (ROOT / "integrated-overview.md").read_text(encoding="utf-8").split()
        self.assertGreaterEqual(len(words), 900)
        self.assertLessEqual(len(words), 6000)

    def test_preregistration_narrative_has_current_counts(self):
        text = (ROOT / "x1-preregistration.md").read_text(encoding="utf-8")
        self.assertIn("nineteen operational failures", text)
        self.assertIn("eleven rejected semantic neighbors", text)


if __name__ == "__main__":
    unittest.main()
