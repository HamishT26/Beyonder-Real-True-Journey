from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"
X1 = "07785aa97b0aa46a4fbf0c60109a8ee8e678aacf"


class V6517SpecialX1Tests(unittest.TestCase):
    def load(self, relative: str):
        return json.loads((PHASE / relative).read_text(encoding="utf-8"))

    def test_exactly_thirty_distinct_proposals(self):
        data = self.load("preregistration/proposals.json")
        rows = data["proposals"]
        self.assertEqual(30, len(rows))
        self.assertEqual(30, len({row["slug"] for row in rows}))
        self.assertEqual(1090, data["inherited_frozen_rows"])
        self.assertEqual(1120, data["frozen_rows_after_x1"])

    def test_required_fields_and_four_expected_labels(self):
        rows = self.load("preregistration/proposals.json")["proposals"]
        required = {
            "hypothesis", "null_or_failure_condition", "approval_class", "execution_lane",
            "official_or_primary_source_needs", "concrete_artifacts", "falsifier_or_acceptance_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        for row in rows:
            self.assertTrue(required.issubset(row))
        self.assertEqual({"completed", "represented", "open_gap", "exact_gate"}, {r["expected_disposition"] for r in rows})

    def test_x1_is_plan_only(self):
        state = self.load("orchestration/x1-phase-state.json")
        self.assertTrue(state["strict_x1_only"])
        self.assertFalse(state["x2_started"])
        tree = set(
            subprocess.run(
                ["git", "ls-tree", "-r", "--name-only", X1],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            ).stdout.splitlines()
        )
        prefix = "docs/vesper-arlen/v651-v7-special-cli-prep/"
        forbidden = ["outcomes/core-outcomes.json", "closeout/closeout-receipt.json", "seal/seal-receipt.json"]
        for relative in forbidden:
            self.assertNotIn(prefix + relative, tree, relative)

    def test_immediate_route_is_exact_and_future_seats_are_placeholders(self):
        request = self.load("workflow/raw-workflow-request.json")
        self.assertEqual({"successor": "Ilyra Fen", "phase": "v651-v8", "authorized_live": True}, request["immediate_route"])
        placeholders = request["route"]["future_identity_placeholders"]
        self.assertEqual(8, len(placeholders))
        self.assertTrue(all("self-chosen" in seat for seat in placeholders))

    def test_special_caps_and_one_pass_policy(self):
        req = self.load("workflow/raw-workflow-request.json")["requirements"]
        self.assertEqual({"x1": 6, "x2": 6, "total": 12}, req["commit_cap"])
        self.assertEqual({"x1": 3, "x2": 3, "total": 6}, req["ordinary_future_commit_cap"])
        self.assertEqual("skip_when_first_passes", req["validation"]["replay_policy"])
        self.assertEqual(2000, req["owner_generated_file_threshold"])


if __name__ == "__main__":
    unittest.main()
