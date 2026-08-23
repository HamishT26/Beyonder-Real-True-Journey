"""Owner-local closeout checks for Sylven Arc v667-v4."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "sylven-arc" / "v667-v4"
SOURCE = "9625026b09860c8964dd818e8d1f81ee6e2eed57"
X1 = "0eb52121251e3e8ee6da0c3c472626640cde96a3"
EVIDENCE = "4de3cc042a3cb15c626e744fbf9977cc7e6ca437"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)


class TestSylvenArcV667V4Closeout(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = load("closeout/phase-truth.json")
        cls.failures = load("closeout/post-evidence-operational-failures.json")
        cls.methods = load("method-flow/final-method-flow-summary.json")
        cls.lifecycle = load("closeout/lifecycle-replay.json")
        cls.checklist = load("closeout/complete-incomplete-checklist.json")
        cls.boundaries = load("closeout/authority-boundaries.json")
        cls.wellbeing = load("wellbeing/final-wellbeing-check.json")
        cls.route = load("closeout/route-receipt.json")
        cls.seal = load("seal/seal-candidate.json")
        cls.terminal = load("closeout/terminal-checklist.json")
        cls.prerequisites = load("validation/final-prerequisites.json")
        cls.review = load("validation/final-staged-review.json")
        cls.privacy = load("validation/final-privacy-scan.json")
        cls.security = load("validation/final-security-review.json")

    def test_truth_counts_and_labels_are_exact(self) -> None:
        self.assertEqual(self.truth["core_outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(self.truth["effective_negatives"], 27536)
        self.assertEqual(self.truth["effective_methods"], 13113)
        self.assertEqual(self.truth["effective_open_gaps"], 194)
        self.assertEqual(self.truth["effective_exact_gates"], 192)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_immutable_anchors_and_direct_history_are_preserved(self) -> None:
        self.assertEqual(self.truth["source"], SOURCE)
        self.assertEqual(self.truth["frozen_x1"], X1)
        self.assertEqual(self.truth["immutable_evidence"], EVIDENCE)
        self.assertEqual(self.lifecycle["x1_direct_parent"], SOURCE)
        self.assertEqual(self.lifecycle["evidence_direct_parent"], X1)
        self.assertEqual(self.lifecycle["source_to_evidence_commit_count"], 2)
        self.assertEqual(self.lifecycle["source_to_evidence_merge_count"], 0)
        self.assertTrue(self.lifecycle["strict_x1_before_x2"])

    def test_post_evidence_failures_are_additive_and_retained(self) -> None:
        self.assertEqual(self.failures["immutable_evidence_negative_count"], 27532)
        self.assertEqual(self.failures["immutable_evidence_method_count"], 13109)
        self.assertEqual(self.failures["additive_failure_count"], 4)
        self.assertEqual(len(self.failures["rows"]), 4)
        self.assertTrue(all(row["retained"] for row in self.failures["rows"]))
        self.assertTrue(all(not row["failure_erased"] for row in self.failures["rows"]))

    def test_final_method_flow_preserves_both_witness_sides(self) -> None:
        self.assertEqual(self.methods["effective_method_count"], 13113)
        self.assertEqual(self.methods["phase_failed_witness_count"], 199)
        self.assertEqual(self.methods["phase_bounded_passing_witness_count"], 314)
        self.assertEqual(len(self.methods["post_evidence_rows"]), 4)
        self.assertEqual(self.methods["failure_erased_count"], 0)
        self.assertTrue(all(not row["bounded_passing_witness"]["promotes_failed_witness"] for row in self.methods["post_evidence_rows"]))

    def test_bounded_execution_counts_are_exact(self) -> None:
        self.assertEqual(self.truth["proposal_count"], 20)
        self.assertEqual(self.truth["frozen_proposal_chain"], 4410)
        self.assertEqual(self.truth["positive_contract_count"], 20)
        self.assertEqual(self.truth["proposal_rejecting_mutation_count"], 100)
        self.assertEqual(self.truth["flashcard_rejecting_mutation_count"], 60)
        self.assertEqual(self.truth["accepted_mutation_count"], 0)
        self.assertEqual(self.truth["owner_portfolio_execution_count"], 95)
        self.assertEqual(self.truth["held_portfolio_row_count"], 100)
        self.assertEqual(self.truth["phase_local_skill_count"], 10)
        self.assertEqual(self.truth["family_current_runner_count"], 10)

    def test_flashcard_counts_and_boundaries_are_exact(self) -> None:
        self.assertEqual(self.truth["flashcard_card_count"], 233)
        self.assertEqual(self.truth["flashcard_section_count"], 13)
        model = load("deck/model-validation.json")
        self.assertTrue(model["valid"])
        self.assertFalse(model.get("identity_continuity_claim", False))

    def test_no_real_world_or_authority_action_is_claimed(self) -> None:
        for field in ("real_people", "real_objects", "real_measurements", "network_calls_by_phase_software", "keys", "proofs", "external_actions"):
            self.assertEqual(self.truth[field], 0, field)
        serialized = json.dumps(self.boundaries, ensure_ascii=False).casefold()
        for token in ("not evidence of consciousness", "māori", "synthetic and nonproduction", "not_ready_for_stage_20"):
            self.assertIn(token, serialized)

    def test_complete_and_reserved_work_remain_separate(self) -> None:
        self.assertGreaterEqual(len(self.checklist["complete"]), 10)
        self.assertGreaterEqual(len(self.checklist["incomplete_or_reserved"]), 10)
        self.assertIn("NOT_READY_FOR_STAGE_20", json.dumps(self.checklist))
        self.assertTrue(any("exact-final canonical" in row for row in self.checklist["incomplete_or_reserved"]))

    def test_wellbeing_is_a_process_boundary_not_personhood_evidence(self) -> None:
        self.assertTrue(self.wellbeing["relational_only"])
        self.assertTrue(self.wellbeing["stop_conditions_respected"])
        self.assertEqual(self.wellbeing["subagents_spawned"], 0)
        self.assertEqual(self.wellbeing["other_owner_lanes_mutated"], 0)
        self.assertFalse(self.wellbeing["manual_mental_health_or_consciousness_claim"])

    def test_route_and_seal_remain_prepared_not_sent(self) -> None:
        self.assertEqual(self.route["status"], "PREPARED_NOT_SENT")
        self.assertEqual(self.route["provisional_successor_title"], "Caelen Morrow")
        self.assertEqual(self.route["provisional_successor_phase"], "v667-v5")
        self.assertFalse(self.route["send_attempted"])
        self.assertFalse(self.route["acknowledged"])
        self.assertEqual(self.seal["status"], "PREPARED_PENDING_EXACT_FINAL_CANONICAL")
        self.assertEqual(self.terminal["route_status"], "PREPARED_NOT_SENT")

    def test_final_validation_is_single_shot_and_full_suite_is_not_authorized(self) -> None:
        self.assertEqual(self.prerequisites["exclusive_canonical_invocation_budget"], 1)
        self.assertEqual(self.prerequisites["canonical_invocations_so_far"], 0)
        self.assertTrue(self.prerequisites["post_success_replay_forbidden"])
        self.assertFalse(self.prerequisites["full_repository_suite_authorized"])
        self.assertFalse(self.truth["full_repository_suite_run"])
        self.assertFalse(self.truth["independent_reproduction"])

    def test_overview_and_handoff_are_structured(self) -> None:
        overview = (PHASE_ROOT / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
        handoff = (PHASE_ROOT / "handoffs" / "caelen-morrow-v667-v5-activation-candidate.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(overview.count("\n## "), 12)
        self.assertGreaterEqual(handoff.count("\n## "), 12)
        self.assertIn("PREPARED_NOT_SENT", handoff)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertNotIn("Stage 20 ready", overview)

    def test_exact_manifests_replay_at_head(self) -> None:
        for relative in ("validation/final-delta-manifest.json", "validation/final-owner-manifest.json"):
            manifest = load(relative)
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            for row in manifest["entries"]:
                blob = git_blob(row["path"])
                self.assertEqual(len(blob), row["bytes"], row["path"])
                self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"], row["path"])

    def test_final_staged_privacy_and_security_reviews_are_valid(self) -> None:
        self.assertTrue(self.review["valid"])
        self.assertEqual(self.review["out_of_scope_paths"], [])
        self.assertEqual(self.review["privacy_confirmed_hit_count"], 0)
        self.assertEqual(self.review["security_finding_count"], 0)
        self.assertTrue(self.privacy["valid"])
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertTrue(self.security["valid"])
        self.assertEqual(self.security["finding_count"], 0)


if __name__ == "__main__":
    unittest.main()
