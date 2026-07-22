from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"
EVIDENCE = "4dda60a276f4401d5dc52eaddf6c4ff14fadc4c0"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V651V7SpecialCloseoutTests(unittest.TestCase):
    def test_final_truth_arithmetic(self) -> None:
        truth = load("truth/phase-truth.json")
        self.assertEqual(truth["effective_negatives"], 7570)
        self.assertEqual((truth["effective_open_gaps"], truth["effective_exact_gates"]), (59, 60))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_closeout_binds_credited_evidence(self) -> None:
        closeout = load("closeout/closeout-receipt.json")
        self.assertEqual(closeout["evidence_commit"], EVIDENCE)
        self.assertTrue(closeout["evidence_validation"]["valid"])
        self.assertEqual(closeout["evidence_validation"]["tests"], 18)
        self.assertTrue(closeout["complete"])

    def test_seal_requires_one_final_pass_without_replay(self) -> None:
        seal = load("seal/seal-receipt.json")
        self.assertEqual(seal["state"], "READY_FOR_FINAL_COMMIT")
        self.assertEqual(seal["canonical_terminal_passes_required"], 1)
        self.assertFalse(seal["replay_after_success"])
        self.assertEqual(seal["future_cli_created"], 0)

    def test_final_record_is_pre_send_and_not_stage20(self) -> None:
        final = load("final/final-record.json")
        self.assertEqual(final["state"], "FINAL_CANDIDATE_PENDING_EXACT_HEAD_VALIDATION")
        self.assertEqual(final["delivery_state"], "PREPARED_NOT_SENT")
        self.assertEqual(final["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(final["independent_reproduction"])

    def test_method_flow_includes_post_evidence_wrapper_failure(self) -> None:
        summary = load("method-flow/method-flow-summary.json")
        self.assertEqual(summary["counts"]["methods"], 10)
        self.assertEqual(summary["counts"]["states"]["preferred"], 10)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 12, "pass": 11})

    def test_anchor_contract_uses_three_commits_and_zero_merges(self) -> None:
        anchors = load("lifecycle/anchor-contract.json")
        self.assertEqual(anchors["evidence"], EVIDENCE)
        self.assertEqual(anchors["planned_special_commits"], 3)
        self.assertEqual(anchors["merge_commits_allowed"], 0)

    def test_completion_gate_stops_before_delivery(self) -> None:
        gate = load("completion/completion-gate-receipt.json")
        self.assertEqual(gate["status"], "READY_FOR_EXACT_FINAL_VALIDATION")
        self.assertIn("one acknowledged Ilyra message", gate["open_terminal_gates"])

    def test_future_route_remains_unlaunched(self) -> None:
        closeout = load("closeout/closeout-receipt.json")
        self.assertEqual(closeout["future_cli_seats"], {"prepared": 8, "named": 0, "launched": 0})
        self.assertEqual(closeout["immediate_successor"], {"owner": "Ilyra Fen", "phase": "v651-v8"})


if __name__ == "__main__":
    unittest.main()
