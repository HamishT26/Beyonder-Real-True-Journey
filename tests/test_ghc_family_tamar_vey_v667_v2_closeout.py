from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v667-v2"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TamarVeyV667V2CloseoutTests(unittest.TestCase):
    def test_phase_truth(self):
        value = load("closeout/phase-truth.json")
        self.assertEqual(value["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(value["proposal_chain"], 4370)
        self.assertEqual(value["effective_negatives"], 27223)
        self.assertEqual(value["effective_methods"], 12570)
        self.assertEqual(value["open_gaps"], 192)
        self.assertEqual(value["exact_gates"], 190)
        self.assertEqual(value["canonical_aggregate_status"], "NOT_YET_INVOKED")
        self.assertEqual(value["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_lifecycle_replay(self):
        value = load("closeout/lifecycle-replay.json")
        self.assertEqual(value["source_to_evidence_commits"], 2)
        self.assertEqual(value["source_to_evidence_merges"], 0)
        self.assertTrue(value["x1_manifest"]["valid"])
        self.assertTrue(value["evidence_manifest"]["valid"])
        self.assertTrue(value["strict_x1_before_x2"])
        self.assertTrue(value["valid"])

    def test_retained_negatives(self):
        value = load("closeout/retained-negative-register.json")
        self.assertEqual(value["startup_additions"], 12)
        self.assertEqual(value["x2_structural_rejections"], 100)
        self.assertEqual(value["x2_operational_additions"], 4)
        self.assertEqual(value["evidence_operational_additions"], 1)
        self.assertEqual(value["closeout_operational_additions"], 4)
        self.assertEqual(len(value["owner_operational_rows"]), 21)
        self.assertTrue(value["all_failed_witnesses_zero_credit"])
        self.assertTrue(value["no_failure_erased"])

    def test_method_flow_summary(self):
        value = load("closeout/method-flow-summary.json")
        self.assertEqual(value["effective_methods"], 12570)
        self.assertEqual(value["failed_witnesses_retained"], 121)
        self.assertEqual(value["failed_witnesses_promoted"], 0)

    def test_open_and_exact_gates(self):
        value = load("closeout/open-exact-gate-register.json")
        self.assertEqual(value["open_gaps"], 192)
        self.assertEqual(value["exact_gates"], 190)
        self.assertEqual(value["phase_open_gap"], "TV6672-N019")
        self.assertEqual(value["phase_exact_gate"], "TV6672-N020")

    def test_terminal_checklist(self):
        value = load("closeout/terminal-checklist.json")
        self.assertTrue(value["all_pre_final_checks_pass"])
        self.assertTrue(all(value["checks"].values()))

    def test_route_is_prepared_not_sent(self):
        value = load("handoffs/terminal-route-state.json")
        self.assertEqual(value["successor_exact_title"], "Elowen Cairn")
        self.assertEqual(value["successor_phase"], "v667-v3")
        self.assertTrue(value["prepared"])
        self.assertFalse(value["sent"])
        self.assertTrue(value["duplicate_activation_guard"])

    def test_handoff_is_sanitized(self):
        text = (PHASE / "handoffs" / "elowen-cairn-v667-v3-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("PREPARED_NOT_SENT", text)
        self.assertIn("Elowen Cairn", text)
        self.assertNotIn("source_thread_id", text)
        self.assertNotIn("task_id", text)
        self.assertNotIn("thread_id", text)
        self.assertNotIn(":\\Users\\", text)
        self.assertNotIn(":\\GHC-Archives\\", text)

    def test_final_overview_preserves_boundaries(self):
        text = (PHASE / "closeout" / "final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertIn("not empirical confirmation", text)
        self.assertIn("Māori authority", text)

    def test_closeout_json_parses(self):
        paths = sorted((PHASE / "closeout").glob("*.json")) + sorted((PHASE / "seal").glob("*.json")) + sorted((PHASE / "handoffs").glob("*.json"))
        self.assertGreaterEqual(len(paths), 9)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
