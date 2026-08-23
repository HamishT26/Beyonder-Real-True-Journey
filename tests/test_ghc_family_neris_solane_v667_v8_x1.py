from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_x1.py"
SPEC = importlib.util.spec_from_file_location("_neris_v667_v8_x1", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load Neris x1 builder")
x1 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(x1)


class NerisSolaneV667V8X1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = x1.validate_tree()
        cls.root = x1.PHASE_ROOT
        cls.freeze = json.loads((cls.root / "x1/proposal-freeze.json").read_text(encoding="utf-8"))
        cls.novelty = json.loads((cls.root / "x1/novelty-audit.json").read_text(encoding="utf-8"))
        cls.charter = json.loads((cls.root / "x1/phase-charter.json").read_text(encoding="utf-8"))
        cls.portfolio = json.loads((cls.root / "x1/portfolio-freeze.json").read_text(encoding="utf-8"))

    def test_01_tree_validates(self) -> None:
        self.assertEqual(self.summary["status"], "PASS")

    def test_02_exact_source(self) -> None:
        self.assertEqual(self.charter["source_final"], x1.SOURCE_SHA)
        self.assertEqual(self.charter["source_x1"], x1.SOURCE_X1_SHA)
        self.assertEqual(self.charter["source_evidence"], x1.SOURCE_EVIDENCE_SHA)

    def test_03_planning_only(self) -> None:
        self.assertTrue(self.charter["x1_planning_only"])
        self.assertEqual(self.charter["x2_implementation_count"], 0)
        self.assertFalse(self.charter["outcomes_observed"])

    def test_04_proposal_chain(self) -> None:
        self.assertEqual(self.novelty["corpus_row_count"], 4510)
        self.assertEqual(self.novelty["new_frozen_total"], 4530)
        self.assertTrue(self.novelty["valid"])

    def test_05_proposal_counts(self) -> None:
        self.assertEqual(len(self.freeze["selected_inherited"]), 20)
        self.assertEqual(len(self.freeze["new_proposals"]), 20)
        self.assertEqual(self.freeze["preregistered_negative_fixture_count"], 100)

    def test_06_four_truth_labels(self) -> None:
        self.assertEqual(
            Counter(row["expected_disposition"] for row in self.freeze["new_proposals"]),
            Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        )
        self.assertEqual(self.charter["allowed_core_outcomes"], x1.ALLOWED_OUTCOMES)

    def test_07_selected_rows_zero_credit(self) -> None:
        for row in self.freeze["selected_inherited"]:
            self.assertEqual(row["neris_novelty_credit"], 0)
            self.assertEqual(row["neris_completion_credit"], 0)
            self.assertFalse(row["append_to_novelty_chain"])

    def test_08_portfolio_counts(self) -> None:
        self.assertEqual(len(self.portfolio["owner_safe_now"]), 30)
        self.assertEqual(len(self.portfolio["owner_candidates"]), 15)
        self.assertEqual(len(self.portfolio["owner_skill_ideas"]), 10)
        self.assertEqual(len(self.portfolio["owner_runner_ideas"]), 10)
        self.assertEqual(len(self.portfolio["owner_clean_fix_refine"]), 30)
        self.assertEqual(len(self.portfolio["exact_approval_packets"]), 10)
        self.assertEqual(len(self.portfolio["blocked_packets"]), 5)

    def test_09_tools_are_plan_only(self) -> None:
        tools = json.loads((self.root / "x1/toolchain-install-plan.json").read_text(encoding="utf-8"))
        self.assertEqual(len(tools["new_tools"]), 3)
        self.assertEqual(tools["x1_install_count"], 0)
        self.assertEqual(tools["x1_download_count"], 0)
        self.assertEqual(tools["x1_smoke_count"], 0)

    def test_10_startup_failures_retained(self) -> None:
        flow = json.loads((self.root / "x1/startup-method-flow.json").read_text(encoding="utf-8"))
        self.assertEqual(flow["failure_count"], 19)
        self.assertTrue(all(row["credit"] == 0 for row in flow["failures"]))

    def test_11_route_conflict_stops_send(self) -> None:
        auth = json.loads((self.root / "x1/auth-roster-receipt.json").read_text(encoding="utf-8"))
        self.assertTrue(auth["name_conflict"])
        self.assertEqual(auth["terminal_route_state"], "OPEN_ROUTE_GAP")
        self.assertFalse(auth["successor_contacted"])

    def test_12_boundaries_and_ceiling(self) -> None:
        self.assertEqual(self.charter["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(self.summary["privacy_candidates"], 0)
        self.assertLess(self.summary["owner_files"], 2000)
        self.assertGreaterEqual(self.summary["overview_words"], 1800)


if __name__ == "__main__":
    unittest.main()
