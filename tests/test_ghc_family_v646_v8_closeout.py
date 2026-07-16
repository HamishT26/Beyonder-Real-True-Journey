"""Scoped lifecycle tests for the Ilyra Fen v646-v8 closeout packet."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v8"


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TestV646V8Closeout(unittest.TestCase):
    def test_closeout_truth(self):
        receipt = read("closeout-receipt.json")
        self.assertEqual(receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(receipt["core_distribution"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})

    def test_commit_caps(self):
        receipt = read("closeout-receipt.json")
        self.assertLessEqual(receipt["phase_commit_count_before_final"] + 1, receipt["phase_commit_cap"])
        self.assertLessEqual(receipt["x2_commit_count_before_final"] + 1, receipt["x2_commit_cap"])

    def test_all_portfolios_complete(self):
        receipt = read("closeout-receipt.json")
        self.assertEqual((receipt["safe_completed"], receipt["candidate_completed"], receipt["clean_refine_completed"]), (30, 20, 30))

    def test_protected_packets_unexecuted(self):
        receipt = read("closeout-receipt.json")
        self.assertEqual((receipt["exact_packets_executed"], receipt["blocked_packets_executed"]), (0, 0))

    def test_route_is_held(self):
        gate = read("orchestration/final-route-gate.json")
        self.assertEqual(gate["state"], "HELD_UNTIL_POST_COMMIT_VALIDATION")
        self.assertEqual((gate["send_count"], gate["create_count"]), (0, 0))

    def test_named_lane_preflight(self):
        lane = read("validation/named-lane-preflight.json")
        self.assertTrue(lane["named_not_detached"] and lane["local_only"] and lane["final_replay_reserved"])
        self.assertFalse(lane["upstream_configured"] or lane["live_remote_ref"] or lane["tests_or_replay_run"])

    def test_evidence_remote_equality(self):
        receipt = read("validation/evidence-remote-equality.json")
        self.assertTrue(receipt["equal"])
        self.assertEqual(len({receipt["local"], receipt["upstream"], receipt["tracking"], receipt["fresh_live_remote"]}), 1)

    def test_exact_final_claim_is_reserved(self):
        record = read("final-validation-record.json")
        self.assertEqual(record["exact_final_canonical_validation"], "required_after_commit")
        self.assertEqual(record["named_local_only_replay"], "required_after_commit")

    def test_same_owner_only(self):
        record = read("final-validation-record.json")
        self.assertTrue(record["same_owner_repeatability_only"])
        self.assertFalse(record["independent_reproduction"])

    def test_final_overview_is_three_page_equivalent(self):
        words = (PHASE / "deliverables/v646-v8-final-integrated-overview.md").read_text(encoding="utf-8").split()
        self.assertGreaterEqual(len(words), 1500)
        self.assertLessEqual(len(words), 6000)


if __name__ == "__main__":
    unittest.main()
