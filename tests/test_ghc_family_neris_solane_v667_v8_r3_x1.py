from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_r3_x1.py"
SPEC = importlib.util.spec_from_file_location("_neris_v667_v8_r3_x1", BUILDER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load r3 x1 builder")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class NerisSolaneV667V8R3X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = builder.validate_tree()
        cls.root = builder.PHASE_ROOT
        cls.freeze = json.loads((cls.root / "x1/proposal-freeze.json").read_text(encoding="utf-8"))
        cls.portfolio = json.loads((cls.root / "x1/portfolio-freeze.json").read_text(encoding="utf-8"))
        cls.tools = json.loads((cls.root / "x1/toolchain-plan.json").read_text(encoding="utf-8"))
        cls.route = json.loads((cls.root / "x1/route-roster-auth.json").read_text(encoding="utf-8"))

    def test_01_validation(self) -> None:
        self.assertEqual(self.summary["status"], "PASS")
        self.assertEqual(self.summary["privacy_candidates"], 0)

    def test_02_orphan_unborn_before_commit(self) -> None:
        result = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--verify", "HEAD"], capture_output=True, text=True, check=False)
        self.assertNotEqual(result.returncode, 0)

    def test_03_lifecycle_separation(self) -> None:
        for name in ("x2", "evidence", "closeout", "seal", "handoffs", "route"):
            self.assertFalse((self.root / name).exists())

    def test_04_proposal_chain(self) -> None:
        self.assertEqual(self.freeze["inherited_proposal_count"], 4550)
        self.assertEqual(self.freeze["new_frozen_total"], 4570)
        self.assertEqual(len(self.freeze["selected_inherited"]), 20)
        self.assertEqual(len(self.freeze["new_proposals"]), 20)
        self.assertEqual(self.freeze["preregistered_negative_fixture_count"], 100)

    def test_05_four_labels(self) -> None:
        self.assertEqual(
            Counter(row["expected_disposition"] for row in self.freeze["new_proposals"]),
            Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        )
        self.assertEqual(self.freeze["allowed_core_outcomes"], builder.ALLOWED_OUTCOMES)

    def test_06_zero_credit_revalidation(self) -> None:
        self.assertTrue(all(row["novelty_credit"] == row["completion_credit"] == 0 for row in self.freeze["selected_inherited"]))

    def test_07_portfolio_counts(self) -> None:
        expected = {
            "owner_safe_now": 30, "successor_safe_now_recommendations": 20,
            "owner_candidates": 15, "successor_candidate_recommendations": 15,
            "owner_skill_ideas": 10, "successor_skill_recommendations": 10,
            "owner_runner_ideas": 10, "successor_runner_recommendations": 10,
            "owner_clean_fix_refine": 30, "successor_clean_fix_refine_recommendations": 30,
            "exact_approval_packets": 10, "blocked_packets": 5,
        }
        self.assertEqual({key: len(self.portfolio[key]) for key in expected}, expected)

    def test_08_x1_has_no_execution(self) -> None:
        keys = [key for key, value in self.portfolio.items() if isinstance(value, list)]
        self.assertTrue(all(row["x2_execution_count"] == 0 for key in keys for row in self.portfolio[key]))
        self.assertEqual(self.tools["install_count"], 0)

    def test_09_tool_count_and_isolation(self) -> None:
        self.assertEqual(len(self.tools["python_tools"]), 8)
        self.assertEqual(len(self.tools["node_tools"]), 5)
        self.assertEqual(self.tools["planned_family_direct_tool_total"], 67)
        self.assertTrue(self.tools["D_isolated_transaction"])
        self.assertFalse(self.tools["global_or_system_install"])

    def test_10_route_stop(self) -> None:
        self.assertEqual(self.route["immediate_successor"]["title"], "Vesper Arlen")
        self.assertEqual(self.route["immediate_successor"]["phase"], "v668-v1")
        self.assertFalse(self.route["successor_contacted"])
        self.assertEqual(self.route["delivery_state"], "PREPARED_NOT_SENT_X1_PLANNING_ONLY")

    def test_11_boundaries(self) -> None:
        charter = json.loads((self.root / "x1/phase-charter.json").read_text(encoding="utf-8"))
        self.assertTrue(charter["synthetic_only"])
        self.assertEqual(charter["real_people"] + charter["real_measurements"] + charter["real_datasets"] + charter["real_authority_actions"], 0)
        self.assertEqual(charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_12_file_ceiling(self) -> None:
        self.assertLess(self.summary["owner_files"], 2000)


if __name__ == "__main__":
    unittest.main()
