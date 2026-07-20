from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / "v650-v2"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class IlyraV650V2TerminalCorrectionTests(unittest.TestCase):
    def test_failed_aggregate_is_retained_with_zero_pass_credit(self) -> None:
        receipt = load("validation/failed-canonical-validation-receipt.json")
        self.assertEqual(receipt["test_count"], 39)
        self.assertTrue(receipt["tests_passed"])
        self.assertEqual((receipt["detailed_count"], receipt["detailed_passed"]), (35, 34))
        self.assertEqual((receipt["minimal_count"], receipt["minimal_passed"]), (20, 19))
        self.assertEqual(receipt["successful_pass_credit"], 0)
        self.assertFalse(receipt["aggregate_replayed_before_correction"])
        self.assertFalse(receipt["repository_mutated_by_failed_run"])

    def test_effective_negative_total_includes_terminal_failure(self) -> None:
        negatives = load("x2/retained-negative-register-terminal.json")
        self.assertEqual(negatives["evidence_layer_total"], 5690)
        self.assertEqual(negatives["terminal_validation_operational"], 1)
        self.assertEqual(negatives["effective_activation_total"], 5691)
        self.assertFalse(negatives["negative_erased"])

    def test_method_flow_retains_failure_and_targeted_recovery(self) -> None:
        summary = load("method-flow/method-flow-summary-terminal.json")
        self.assertEqual(summary["counts"]["methods"], 12)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 12, "pass": 12})
        receipt = load("method-flow/method-flow-validation-terminal.json")
        self.assertTrue(receipt["valid"])

    def test_terminal_truth_and_route_remain_held(self) -> None:
        truth = load("phase-truth-terminal-correction.json")
        route = load("orchestration/phase-state-terminal-correction.json")
        self.assertEqual(truth["effective_negatives"], 5691)
        self.assertEqual((truth["effective_open_gaps"], truth["effective_exact_gates"]), (44, 45))
        self.assertEqual(truth["failed_canonical_aggregates"], 1)
        self.assertEqual(truth["successful_canonical_passes"], 0)
        self.assertTrue(truth["corrected_exact_final_pass_pending"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(route["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(route["sent_by_ilyra_fen"])

    def test_correction_privacy_and_staged_review_pass(self) -> None:
        privacy = load("validation/terminal-correction-staged-privacy.json")
        review = load("validation/terminal-correction-staged-review.json")
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(review["passed"])
        self.assertEqual(review["evidence_frozen_changes"], [])
        self.assertEqual(review["closeout_changes"], ["scripts/ghc_family_v650_v2_validate.py"])
        self.assertEqual(review["out_of_scope_paths"], [])

    def test_correction_owner_manifest_covers_packet(self) -> None:
        manifest = load("validation/terminal-correction-owner-manifest.json")
        declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
        actual = {path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()}
        self.assertEqual(declared, actual)

    def test_additive_handoff_carries_corrected_baseline(self) -> None:
        handoff = (PHASE / "handoffs" / "sable-rook-v650-v3-terminal-correction.md").read_text(encoding="utf-8")
        self.assertIn("5,691 negatives", handoff)
        self.assertIn("PREPARED_NOT_SENT", handoff)
        self.assertIn("NOT_READY_FOR_STAGE_20", handoff)


if __name__ == "__main__":
    unittest.main()
