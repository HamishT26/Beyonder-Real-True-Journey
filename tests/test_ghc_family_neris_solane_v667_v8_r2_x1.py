from __future__ import annotations

import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_r2_x1.py"
SPEC = importlib.util.spec_from_file_location("_neris_v667_v8_r2_x1", BUILDER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load x1 builder")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class NerisV667V8R2X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = builder.validate_tree()
        cls.root = builder.PHASE_ROOT
        cls.freeze = json.loads((cls.root / "x1/proposal-freeze.json").read_text(encoding="utf-8"))
        cls.portfolio = json.loads((cls.root / "x1/portfolio-freeze.json").read_text(encoding="utf-8"))
        cls.tools = json.loads((cls.root / "x1/toolchain-install-plan.json").read_text(encoding="utf-8"))
        cls.auth = json.loads((cls.root / "x1/auth-roster-receipt.json").read_text(encoding="utf-8"))
        cls.charter = json.loads((cls.root / "x1/phase-charter.json").read_text(encoding="utf-8"))

    def test_validation(self) -> None:
        self.assertEqual(self.result["status"], "PASS")
        self.assertEqual(self.result["privacy_candidates"], 0)

    def test_lifecycle(self) -> None:
        self.assertTrue(self.charter["x1_planning_only"])
        self.assertFalse(self.charter["outcomes_observed"])
        self.assertEqual(self.charter["x2_implementation_count"], 0)
        for name in ("x2", "evidence", "closeout", "seal", "route"):
            self.assertFalse((self.root / name).exists())

    def test_proposals(self) -> None:
        self.assertEqual(self.freeze["inherited_proposal_count"], 4530)
        self.assertEqual(len(self.freeze["selected_inherited"]), 20)
        self.assertEqual(len(self.freeze["new_proposals"]), 20)
        self.assertEqual(self.freeze["new_frozen_total"], 4550)
        self.assertEqual(self.freeze["preregistered_negative_fixture_count"], 100)
        self.assertEqual(
            Counter(row["expected_disposition"] for row in self.freeze["new_proposals"]),
            Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        )

    def test_portfolio(self) -> None:
        expected = {
            "owner_safe_now": 30, "successor_safe_now_recommendations": 20,
            "owner_candidates": 15, "successor_candidate_recommendations": 15,
            "owner_skill_ideas": 10, "successor_skill_recommendations": 10,
            "owner_runner_ideas": 10, "successor_runner_recommendations": 10,
            "owner_clean_fix_refine": 30,
            "successor_clean_fix_refine_recommendations": 30,
            "exact_approval_packets": 10, "blocked_packets": 5,
        }
        self.assertEqual({key: len(self.portfolio[key]) for key in expected}, expected)
        self.assertTrue(all(row["x2_execution_count"] == 0 for key in expected for row in self.portfolio[key]))

    def test_tools(self) -> None:
        self.assertEqual(self.tools["family_global_direct_tool_baseline"], 41)
        self.assertEqual(len(self.tools["new_tools"]), 13)
        self.assertEqual(self.tools["planned_family_global_direct_tool_total"], 54)
        self.assertEqual(self.tools["x1_install_count"], 0)
        self.assertEqual(self.tools["x1_smoke_count"], 0)

    def test_route(self) -> None:
        self.assertEqual(self.auth["prospective_successor_title"], "Vesper Arlen")
        self.assertEqual(self.auth["prospective_successor_phase"], "v668-v1")
        self.assertFalse(self.auth["successor_contacted"])
        self.assertEqual(self.auth["delivery_state"], "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2")
        self.assertEqual(self.auth["standby"][0]["state"], "ON_STANDBY")

    def test_boundaries(self) -> None:
        self.assertEqual(self.charter["identity"]["relational_name"], "Neris Solane")
        self.assertEqual(self.charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(self.charter["repository_scan"])
        self.assertFalse(self.charter["cross_lane_scan"])
        self.assertFalse(self.charter["sibling_lane_mutation"])
        self.assertLess(self.result["owner_files"], 2000)


if __name__ == "__main__":
    unittest.main()
