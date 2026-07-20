from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v650-v2"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class IlyraV650V2CloseoutTests(unittest.TestCase):
    def test_final_truth_is_bounded_and_unsent(self) -> None:
        truth = load("phase-truth-final.json")
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 5690)
        self.assertEqual((truth["effective_open_gaps"], truth["effective_exact_gates"]), (44, 45))
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["full_repository_suite"])
        self.assertFalse(truth["replay_used"])
        self.assertTrue(truth["same_owner_only"])
        self.assertFalse(truth["independent_reproduction"])

    def test_closeout_and_seal_preserve_lifecycle(self) -> None:
        closeout = load("closeout/closeout-receipt.json")
        seal = load("closeout/seal-receipt.json")
        self.assertEqual(closeout["phase_commit_plan"], 3)
        self.assertTrue(closeout["x1_before_x2"])
        self.assertTrue(closeout["evidence_remote_equal_before_closeout"])
        self.assertTrue(closeout["final_external_validation_pending"])
        self.assertTrue(seal["x1_blob_sealed"] and seal["evidence_blob_sealed"])
        self.assertFalse(seal["retained_negatives_erased"])
        self.assertEqual(seal["gates_silently_closed"], 0)
        self.assertFalse(seal["terminal_message_sent"])

    def test_successor_baton_word_range_and_boundaries(self) -> None:
        receipt = load("validation/final-document-cap-receipt.json")
        baton = (PHASE / "handoffs" / "sable-rook-v650-v3-activation.md").read_text(encoding="utf-8")
        self.assertTrue(receipt["all_under_20000"])
        self.assertTrue(receipt["baton_within_8000_20000"])
        self.assertGreaterEqual(receipt["baton_words"], 8000)
        self.assertLessEqual(receipt["baton_words"], 20000)
        self.assertIn("Sable Rook", baton)
        self.assertIn("NOT_READY_FOR_STAGE_20", baton)
        self.assertIn("SENT_BY_ILYRA_FEN", baton)
        self.assertIn("remains false", baton)
        self.assertNotIn("source_thread_id", baton.casefold())
        self.assertNotIn("thread_id", baton.casefold())

    def test_privacy_and_exact_staged_review(self) -> None:
        owner = load("validation/final-owner-privacy.json")
        staged = load("validation/final-staged-privacy.json")
        review = load("validation/final-staged-review.json")
        self.assertEqual(owner["pattern_class_count"], 5)
        self.assertEqual(staged["pattern_class_count"], 5)
        self.assertEqual(owner["confirmed_hit_count"], 0)
        self.assertEqual(staged["confirmed_hit_count"], 0)
        self.assertTrue(review["passed"])
        self.assertEqual(review["out_of_scope_paths"], [])
        self.assertEqual(review["evidence_frozen_changes"], [])

    def test_manifest_coverage_contracts(self) -> None:
        owner = load("validation/final-owner-manifest.json")
        staged = load("validation/final-staged-manifest.json")
        owner_paths = {row["path"] for row in owner["entries"]} | set(owner["self_exclusions"])
        actual_owner = {
            path.relative_to(ROOT).as_posix()
            for path in PHASE.rglob("*")
            if path.is_file()
        }
        self.assertEqual(owner_paths, actual_owner)
        self.assertEqual(staged["entry_count"] + len(staged["self_exclusions"]), load("validation/final-staged-review.json")["intended_path_count"])

    def test_final_validation_contract_is_external_and_single_pass(self) -> None:
        contract = load("validation/final-canonical-validation-contract.json")
        self.assertEqual(contract["mode"], "one_successful_exact_final_canonical_pass_external_receipt")
        self.assertEqual(contract["receipt_location"], "outside_repository")
        self.assertFalse(contract["full_repository_suite"])
        self.assertFalse(contract["named_replay"])
        self.assertFalse(contract["detached_replay"])
        self.assertFalse(contract["post_success_replay"])

    def test_environment_and_wellbeing_remain_safe(self) -> None:
        environment = load("environment/final-environment-receipt.json")
        wellbeing = load("wellbeing-check-final.json")
        self.assertTrue(environment["versions_verified_only"])
        self.assertFalse(environment["desktop_updated"])
        self.assertFalse(environment["sandbox_or_hyperv_launched"])
        self.assertFalse(environment["elevation"])
        self.assertFalse(environment["host_security_weakened"])
        self.assertFalse(environment["reboot"])
        self.assertTrue(wellbeing["pause_available"])
        self.assertFalse(wellbeing["identity_pressure"])

    def test_route_and_checklist_remain_held(self) -> None:
        route = load("orchestration/phase-state-closeout.json")
        checklist = load("complete-incomplete-checklist-final.json")
        self.assertEqual(route["active"], ["Ilyra Fen"])
        self.assertEqual(route["next_target"], "Sable Rook")
        self.assertEqual(route["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(route["sent_by_ilyra_fen"])
        self.assertIn("run one exact-final canonical pass", checklist["external_terminal_gate"])
        self.assertIn("Stage 20", checklist["incomplete_external"])


if __name__ == "__main__":
    unittest.main()
