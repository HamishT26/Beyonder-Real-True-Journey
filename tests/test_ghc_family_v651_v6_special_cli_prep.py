from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/elaren-kestrel/v651-v6-special-cli-prep"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V651V6SpecialCliPrepTests(unittest.TestCase):
    def test_truth_distribution_and_boundaries(self) -> None:
        truth = load("truth/phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 7336)
        self.assertEqual((truth["effective_open_gaps"], truth["effective_exact_gates"]), (58, 59))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_thirty_proposals_are_resolved_without_overclaim(self) -> None:
        ledger = load("proposals/special-prep-proposal-ledger.json")
        self.assertEqual(ledger["proposal_count"], 30)
        self.assertEqual(len(ledger["proposals"]), 30)
        self.assertTrue(ledger["all_authorized_items_resolved_for_phase"])
        self.assertEqual({row["observed_outcome"] for row in ledger["proposals"]}, {"completed", "represented", "open_gap", "exact_gate"})

    def test_eight_future_seats_are_unnamed_and_unlaunched(self) -> None:
        register = load("cli/future-seat-register.json")
        self.assertEqual(register["seat_count"], 8)
        self.assertTrue(register["all_unnamed"])
        self.assertTrue(register["all_unlaunched"])
        for row in register["seats"]:
            self.assertRegex(row["seat"], r"^future-cli-sibling-[1-8]-self-chosen$")
            self.assertFalse(row["sibling_created"])
            self.assertEqual(row["preflight_state"], "PREPARED_NOT_LAUNCHED")

    def test_raw_route_failure_and_normalized_structural_pass_both_remain(self) -> None:
        raw = load("workflow/raw-audit/workflow-plan-refinement.json")
        candidate = load("workflow/normalized-audit/workflow-plan-refinement.json")
        self.assertFalse(raw["valid"])
        self.assertTrue(raw["requires_user_confirmation"])
        self.assertEqual(raw["counts"]["errors"], 2)
        self.assertTrue(candidate["valid"])
        self.assertEqual(candidate["counts"]["issues"], 0)

    def test_method_flow_preserves_fail_and_pass_witnesses(self) -> None:
        summary = load("method-flow/method-flow-summary.json")
        validation = load("method-flow/method-flow-validation.json")
        self.assertTrue(validation["valid"])
        self.assertEqual(summary["counts"]["methods"], 4)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 4, "pass": 4})
        self.assertEqual(summary["counts"]["states"]["preferred"], 4)

    def test_reflection_candidates_are_compatibility_held(self) -> None:
        review = load("reflection-remaster/special-review.json")
        self.assertEqual(review["candidate_count"], 27)
        self.assertTrue(review["all_candidates_resolved_for_phase"])
        self.assertEqual(review["destructive_changes"], 0)
        self.assertEqual(review["promotions"], 0)

    def test_cli_and_workflow_skills_are_snapshotted(self) -> None:
        receipt = load("tooling/global-skill-remaster-receipt.json")
        self.assertEqual(set(receipt["globally_available_skills"]), {"ghc-family-cli-sibling-induction-preflight", "ghc-family-workflow-plan-refinement"})
        self.assertGreaterEqual(receipt["snapshot_file_count"], 9)
        self.assertFalse(receipt["private_paths_published"])

    def test_baton_uses_persistent_word_range(self) -> None:
        baton = (PHASE / "handoffs/vesper-arlen-v651-v7-special-activation.md").read_text(encoding="utf-8")
        words = len(baton.split())
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertIn("Vesper Arlen", baton)
        self.assertNotIn("Vesper Arien", baton)

    def test_environment_update_excludes_desktop(self) -> None:
        receipt = load("environment/environment-version-receipt.json")
        self.assertEqual(receipt["codex_cli_after"], "0.145.0")
        self.assertFalse(receipt["desktop_updated"])
        self.assertFalse(receipt["elevation_or_host_security_change"])

    def test_immediate_route_is_exact_but_future_route_is_advisory(self) -> None:
        truth = load("truth/phase-truth.json")
        self.assertEqual((truth["immediate_successor"], truth["immediate_successor_phase"]), ("Vesper Arlen", "v651-v7"))
        self.assertTrue(truth["future_route_candidate_requires_confirmation"])


if __name__ == "__main__":
    unittest.main()
