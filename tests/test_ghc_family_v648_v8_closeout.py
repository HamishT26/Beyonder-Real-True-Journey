import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v648-v8"


def load(relative):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TestGhcFamilyV648V8Closeout(unittest.TestCase):
    def test_overview_is_three_page_equivalent_and_bounded(self):
        words = re.findall(r"\b\w+\b", (PHASE / "integrated-overview.md").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(words), 1200)
        self.assertLessEqual(len(words), 6000)
        self.assertIn("NOT_READY_FOR_STAGE_20", (PHASE / "integrated-overview.md").read_text(encoding="utf-8"))

    def test_static_report_has_structural_accessibility_surface(self):
        text = (PHASE / "accessible-report.html").read_text(encoding="utf-8")
        for marker in ["Skip to main content", "<main", "<caption>", "scope=\"col\"", "@media print", "affected-user evaluation remain reserved"]:
            self.assertIn(marker, text)

    def test_core_outcome_and_stage20_truth(self):
        truth = load("phase-truth-final-candidate.json")
        self.assertEqual(truth["outcomes"], {"completed":6,"represented":2,"open_gap":1,"exact_gate":1})
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(load("stage20-terminal-board.json")["ready"])

    def test_negative_and_gate_truth(self):
        negatives = load("retained-negative-register-final.json")
        gates = load("exact-open-gate-register-final.json")
        self.assertGreaterEqual(negatives["effective_total"], 4665)
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (34, 35))
        self.assertEqual(gates["silently_closed"], 0)

    def test_portfolio_floors_and_no_inherited_credit(self):
        portfolio = load("x2/portfolio-ledger.json")
        self.assertEqual((portfolio["safe_completed"], portfolio["candidates_completed"], portfolio["skills_completed"], portfolio["runners_completed"], portfolio["clean_refine_completed"]), (30,20,20,10,30))
        self.assertEqual(portfolio["inherited_completion_credit"], 0)

    def test_method_flow_retains_failures(self):
        summary = load("method-flow/method-flow-summary.json")
        self.assertGreaterEqual(summary["counts"]["methods"], 14)
        self.assertEqual(summary["counts"]["witness_results"]["fail"], summary["counts"]["witness_results"]["pass"])
        self.assertTrue(load("method-flow/method-flow-validation.json")["valid"])

    def test_validation_budget_is_one_pass_no_replay(self):
        plan = load("validation/final-validation-plan.json")
        self.assertEqual(plan["canonical_successful_pass_budget"], 1)
        self.assertEqual(plan["successful_passes_used"], 0)
        self.assertEqual(plan["failed_canonical_attempts"], 0)
        self.assertEqual(plan["replay_budget"], 0)
        self.assertFalse(plan["full_repository_suite"])
        self.assertEqual(len(plan["excluded_source_local_tests"]), 2)
        self.assertGreater(plan["selected_test_count"], 80)

    def test_solo_route_is_prepared_not_sent(self):
        state = load("orchestration/final-phase-state.json")
        self.assertEqual((state["subagents"], state["tasks_created"], state["tasks_forked"], state["cross_platform_messages"]), (0,0,0,0))
        self.assertEqual(state["terminal_route"], "PREPARED_NOT_SENT")

    def test_checklist_keeps_external_work_open(self):
        incomplete = load("complete-incomplete-checklist.json")["incomplete"]
        self.assertIn("manual_accessibility", incomplete)
        self.assertIn("independent_reproduction", incomplete)
        self.assertIn("stage20", incomplete)

    def test_owner_manifest_contract(self):
        manifest = load("validation/final-owner-manifest.json")
        self.assertTrue(manifest["coverage_complete"])
        self.assertGreater(manifest["entry_count"], 200)
        self.assertEqual(len(manifest["declared_self_exclusions"]), 4)


if __name__ == "__main__":
    unittest.main()
