"""Combined closeout and seal tests for Sable Rook v652-v1."""

import json
import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sable-rook/v652-v1"


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestV652V1Closeout(unittest.TestCase):
    def test_final_truth_and_board(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual((truth["effective_negatives"], truth["effective_open_gaps"], truth["effective_exact_gates"]), (8018, 62, 63))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction_claimed"])
    def test_route_is_prepared_not_sent(self):
        route = load("route/final-route-state.json")
        self.assertEqual(route["recipient_title"], "Orin Thale")
        self.assertEqual(route["recipient_phase"], "v652-v2")
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertEqual((route["messages_sent"], route["tasks_created"], route["tasks_forked"]), (0, 0, 0))
    def test_baton_and_documents(self):
        baton = (ROOT / "handoffs/orin-thale-v652-v2-activation.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", baton))
        self.assertGreaterEqual(words, 10000)
        self.assertLessEqual(words, 100000)
        self.assertTrue(load("final/document-word-counts.json")["valid"])
    def test_manifests_and_privacy(self):
        owner = load("validation/final-owner-manifest.json")
        delta = load("validation/final-delta-manifest.json")
        self.assertEqual(owner["owner_path_count"], owner["entry_count"] + owner["self_exclusion_count"])
        self.assertEqual(delta["delta_path_count"], delta["entry_count"] + delta["self_exclusion_count"])
        self.assertEqual(load("validation/final-staged-privacy.json")["confirmed_hit_count"], 0)
    def test_commit_contract(self):
        cap = load("final/commit-cap-contract.json")
        self.assertEqual(cap["planned_phase_total"], 3)
        self.assertLessEqual(cap["planned_phase_total"], cap["maximum"])
        self.assertEqual(cap["merge_commits_allowed"], 0)
    def test_skill_runner_and_future_seat_boundaries(self):
        self.assertEqual(load("validation/skill-validation.json")["count"], 10)
        self.assertEqual(load("validation/runner-validation.json")["count"], 10)
        seats = load("provenance/future-cli-x2-invariant.json")
        self.assertEqual((seats["named_count"], seats["created_count"], seats["launched_count"]), (0, 0, 0))
    def test_open_and_exact_gates_remain_open(self):
        gates = load("truth/final-open-and-exact-gate-register.json")
        self.assertEqual((gates["open_gaps"], gates["exact_gates"]), (62, 63))
        self.assertFalse(gates["phase_open_gap"]["closed"])
        self.assertFalse(gates["phase_exact_gate"]["closed"])


if __name__ == "__main__":
    unittest.main()
