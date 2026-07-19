from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v649-v4"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TestGhcFamilyV649V4Closeout(unittest.TestCase):
    def test_overview_is_three_page_equivalent_and_bounded(self) -> None:
        words = len((PHASE / "integrated-overview.md").read_text(encoding="utf-8").split())
        self.assertGreaterEqual(words, 1200)
        self.assertLessEqual(words, 6000)

    def test_successor_baton_is_full_and_sanitized(self) -> None:
        text = (PHASE / "handoffs/tamar-vey-v649-v5-activation.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(text.split()), 1200)
        self.assertLessEqual(len(text.split()), 6000)
        self.assertIn("TAMAR VEY", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)
        self.assertNotRegex(text, r"(?i)(source_thread_id|thread_id)\s*[:=]")
        self.assertNotRegex(text, r"(?i)[A-Z]:\\Users\\")

    def test_accessible_report_has_structural_surface_and_reservations(self) -> None:
        text = (PHASE / "accessible-report.html").read_text(encoding="utf-8")
        for token in ["<main", "<nav", "<table", "<caption", 'scope="col"', 'scope="row"', ":focus", "Skip to evidence"]:
            self.assertIn(token, text)
        self.assertIn("Manual keyboard", text)
        self.assertIn("NOT_READY_FOR_STAGE_20", text)

    def test_complete_incomplete_checklist_preserves_external_gates(self) -> None:
        row = load("complete-incomplete-checklist.json")
        self.assertIn("ten_core_outcomes_classified", row["complete"])
        self.assertTrue({"real_gmut_implementation_data_likelihood", "real_thos_arms", "production_freed_id", "maori_authority_review", "independent_reproduction", "stage20"}.issubset(row["incomplete"]))
        self.assertEqual(row["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_threat_model_is_explicitly_nonexhaustive(self) -> None:
        row = load("threat-model.json")
        self.assertFalse(row["exhaustive"])
        self.assertGreaterEqual(len(row["threats"]), 8)
        self.assertIn("software_to_authority_substitution", {item["threat"] for item in row["threats"]})

    def test_final_negative_and_gate_candidates_preserve_counts(self) -> None:
        negatives = load("retained-negative-register-final.json")
        operational = load("validation/x2-operational-negatives.json")
        gates = load("exact-open-gate-register-final.json")
        self.assertEqual(negatives["effective_at_evidence"], 4929 + 17 + 70 + operational["count"])
        self.assertEqual(negatives["x2_operational"], operational["count"])
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (38, 39))
        self.assertEqual(gates["silently_closed"], 0)

    def test_all_skills_and_runners_are_finally_used(self) -> None:
        skills = load("x2/skill-use-ledger-final.json")
        runners = load("x2/runner-use-ledger-final.json")
        self.assertEqual((skills["skill_count"], skills["completed_count"], skills["pending_count"]), (20, 20, 0))
        self.assertEqual((runners["runner_count"], runners["completed_count"], runners["pending_count"]), (10, 10, 0))
        self.assertTrue(all(row["smoke_used"] for row in skills["items"]))
        self.assertTrue(all(row["invoked"] for row in runners["items"]))

    def test_stage20_board_and_closeout_candidate_abstain(self) -> None:
        board = load("stage20-terminal-board.json")
        closeout = load("closeout/closeout-candidate.json")
        self.assertFalse(board["ready"])
        self.assertEqual(board["verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(closeout["canonical_successful_pass_used"])
        self.assertEqual(closeout["terminal_route"], "PREPARED_NOT_SENT")

    def test_final_validation_plan_reserves_one_pass_and_no_replay(self) -> None:
        plan = load("validation/final-validation-plan.json")
        self.assertFalse(plan["full_repository_suite"])
        self.assertEqual(plan["canonical_successful_pass_budget"], 1)
        self.assertEqual(plan["successful_passes_used"], 0)
        self.assertEqual(plan["replay_budget"], 0)
        self.assertGreater(plan["selected_test_count"], 25)
        self.assertEqual((plan["detailed_check_count"], plan["minimal_check_count"]), (32, 20))

    def test_every_phase_document_respects_word_cap(self) -> None:
        for path in list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html")):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 6000, path.as_posix())


if __name__ == "__main__":
    unittest.main()
