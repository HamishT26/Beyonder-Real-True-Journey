from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v651-v8-special-cli-prep"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class SpecialCloseoutTests(unittest.TestCase):
    def test_closeout_anchors(self):
        row = load("closeout/closeout-receipt.json")
        self.assertEqual(row["x1_commit"], "580a3f0155c589866fd7f4aacd88790419cd147a")
        self.assertEqual(row["evidence_commit"], "0b382d660837536e12672e28cc68f6208e2b0069")

    def test_closeout_truth(self):
        row = load("closeout/closeout-receipt.json")
        self.assertEqual(row["outcomes"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual((row["effective_negatives"], row["effective_open_gaps"], row["effective_exact_gates"]), (7855, 61, 62))

    def test_seal_history_contract(self):
        row = load("seal/seal-receipt.json")
        self.assertEqual(row["expected_history"], {"phase_commits": 3, "merge_commits": 0, "final_parents": 1})
        self.assertFalse(row["replay_after_success"])

    def test_final_route_held(self):
        row = load("route/terminal-route-receipt.json")
        self.assertEqual((row["recipient_exact_title"], row["successor_phase"], row["send_state"]), ("Sable Rook", "v652-v1", "PREPARED_NOT_SENT"))

    def test_future_cli_stays_zero(self):
        row = load("final/final-record.json")
        self.assertEqual(row["future_cli"], {"prepared": 8, "named": 0, "launched": 0})

    def test_one_pass_contract(self):
        row = load("final/final-validation-contract.json")
        self.assertTrue(row["run_after_push"])
        self.assertFalse(row["replay_after_success"])
        self.assertFalse(row["full_repository_suite_planned"])

    def test_accessibility_reservation(self):
        row = load("accessibility/manual-evaluation-reservation.json")
        self.assertEqual(row["manual_keyboard"], "reserved")
        self.assertFalse(row["complete_conformance_claim"])

    def test_privacy_contract(self):
        row = load("privacy/final-privacy-contract.json")
        self.assertEqual(len(row["classes"]), 5)
        self.assertFalse(row["complete_privacy_claim"])


if __name__ == "__main__":
    unittest.main()
