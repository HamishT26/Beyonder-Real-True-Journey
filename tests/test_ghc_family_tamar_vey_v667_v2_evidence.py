from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v667-v2"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TamarVeyV667V2EvidenceTests(unittest.TestCase):
    def test_evidence_receipt_exact_truth(self):
        value = load("evidence/evidence-receipt.json")
        self.assertEqual(value["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(value["effective_negatives"], 27219)
        self.assertEqual(value["effective_methods"], 12566)
        self.assertEqual(value["open_gaps"], 192)
        self.assertEqual(value["exact_gates"], 190)
        self.assertEqual(value["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_tests_are_exactly_bounded(self):
        value = load("evidence/owner-test-receipt.json")
        self.assertEqual(value["immutable_x1"]["tests_run"], 16)
        self.assertEqual(value["live_x2"]["tests_run"], 67)
        self.assertEqual(value["total_attributable_tests"], 83)
        self.assertFalse(value["full_repository_suite"])
        self.assertFalse(value["independent_reproduction"])

    def test_x1_is_immutable(self):
        value = load("evidence/x1-immutability-replay.json")
        self.assertEqual(value["x1_sha"], "491aa870cb1f6a020ef9778cbd1a1c4d220adbf4")
        self.assertEqual(value["changed_x1_paths"], [])
        self.assertTrue(value["manifest_replay"]["valid"])
        self.assertTrue(value["immutable"])

    def test_structural_execution(self):
        value = load("evidence/structural-execution-receipt.json")
        self.assertEqual(value["contracts"]["contract_count"], 20)
        self.assertEqual(value["mutations"]["rejected_total"], 100)
        self.assertEqual(value["skills"]["skill_count"], 10)
        self.assertEqual(value["runners"]["runner_count"], 10)
        self.assertEqual(value["portfolio"]["executed_owner_method_count"], 95)
        self.assertEqual(value["real_rows"], 0)
        self.assertEqual(value["participants"], 0)
        self.assertEqual(value["network_calls"], 0)
        self.assertEqual(value["external_actions"], 0)

    def test_privacy_and_security_are_bounded(self):
        privacy = load("evidence/privacy-adjudication.json")
        security = load("evidence/security-review.json")
        self.assertEqual(privacy["confirmed_hits"], 0)
        self.assertFalse(privacy["complete_privacy_assurance"])
        self.assertEqual(security["findings"], [])
        self.assertFalse(security["exhaustive_security"])

    def test_accessibility_reservations(self):
        value = load("evidence/accessibility-review.json")
        self.assertTrue(value["manual_evaluation_reserved"])
        self.assertTrue(value["affected_user_evaluation_reserved"])
        self.assertFalse(value["accessibility_complete"])
        self.assertTrue(value["valid"])

    def test_all_evidence_json_parses(self):
        paths = sorted((PHASE / "evidence").glob("*.json"))
        self.assertGreaterEqual(len(paths), 9)
        for path in paths:
            json.loads(path.read_text(encoding="utf-8"))

    def test_reports_keep_stage_boundary(self):
        markdown = (PHASE / "evidence" / "integrated-overview.md").read_text(encoding="utf-8")
        html = (PHASE / "evidence" / "static-report.html").read_text(encoding="utf-8")
        self.assertIn("NOT_READY_FOR_STAGE_20", markdown)
        self.assertIn("NOT_READY_FOR_STAGE_20", html)
        self.assertIn("independent reproduction", markdown)
        self.assertIn("<caption>", html)

    def test_workload_is_solo_and_bounded(self):
        value = load("evidence/wellbeing-workload-check.json")
        self.assertEqual(value["subagents"], 0)
        self.assertEqual(value["sibling_lanes_mutated"], 0)
        self.assertEqual(value["standby_contacts"], 0)
        self.assertFalse(value["terminal_route_contacted"])
        self.assertEqual(value["retained_failures"], 17)


if __name__ == "__main__":
    unittest.main()
