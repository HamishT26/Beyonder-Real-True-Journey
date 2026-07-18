from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v649-v1"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class EirenV649V1CloseoutTests(unittest.TestCase):
    def test_overview_and_baton_are_bounded_and_substantive(self):
        overview = (PHASE / "integrated-overview.md").read_text(encoding="utf-8")
        baton = (PHASE / "handoffs/ilyra-fen-v649-v2-activation.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(overview.split()), 1200)
        self.assertGreaterEqual(len(baton.split()), 2000)
        self.assertLessEqual(len(overview.split()), 6000)
        self.assertLessEqual(len(baton.split()), 6000)
        self.assertIn("NOT_READY_FOR_STAGE_20", overview)
        self.assertIn("PREPARED_NOT_SENT", baton)

    def test_accessible_report_reserves_manual_evaluation(self):
        report = (PHASE / "accessible-report.html").read_text(encoding="utf-8")
        for token in ("<main", "<nav", "<table", "<caption", 'scope="col"', 'scope="row"', ":focus", "Skip to evidence"):
            self.assertIn(token, report)
        self.assertIn("Manual keyboard", report)
        self.assertIn("NOT READY", report)

    def test_outcomes_portfolios_and_gates(self):
        truth = load("phase-truth-final-candidate.json")
        portfolio = load("x2/portfolio-ledger.json")
        gates = load("exact-open-gate-register-final.json")
        self.assertEqual(truth["outcomes"], {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
        self.assertEqual((portfolio["safe_completed"], portfolio["candidates_completed"], portfolio["skills_completed"], portfolio["runners_completed"], portfolio["clean_refine_completed"]), (30, 20, 20, 10, 30))
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"], gates["silently_closed"]), (35, 36, 0))

    def test_negatives_and_method_flow_are_additive(self):
        negatives = load("retained-negative-register-final.json")
        methods = load("method-flow/method-flow-summary.json")
        self.assertEqual(negatives["effective_current"], 4742)
        self.assertEqual(4665 + 2 + 70 + 3 + 2, negatives["effective_current"])
        self.assertFalse(negatives["negative_erased"])
        self.assertEqual(methods["counts"]["methods"], 7)
        self.assertEqual(methods["counts"]["witness_results"], {"fail": 7, "pass": 7})

    def test_single_full_suite_pass_is_reserved_without_replay(self):
        plan = load("validation/final-validation-plan.json")
        no_replay = load("reproduction/no-replay-plan.json")
        self.assertTrue(plan["full_repository_suite"])
        self.assertEqual(plan["canonical_successful_pass_budget"], 1)
        self.assertEqual(plan["successful_passes_used_before_final"], 0)
        self.assertEqual(len(plan["exact_excluded_test_ids"]), 4)
        self.assertEqual(plan["replay_budget"], 0)
        self.assertEqual(no_replay["named_lane_count"], 0)
        self.assertEqual(no_replay["detached_lane_count"], 0)

    def test_candidate_records_do_not_preclaim_terminal_truth(self):
        seal = load("seal-receipt.json")
        final = load("final-receipt.json")
        route = load("orchestration/terminal-route-state.json")
        self.assertIsNone(seal["final_commit"])
        self.assertFalse(seal["full_suite_completed"])
        self.assertFalse(seal["baton_send_allowed_now"])
        self.assertIsNone(final["final_commit"])
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["message_sent"] or route["task_created"] or route["task_forked"] or route["subagent_spawned"])

    def test_documents_respect_word_cap(self):
        receipt = load("validation/document-cap-candidate.json")
        self.assertTrue(receipt["all_under_6000"])
        for path in list(PHASE.rglob("*.md")) + list(PHASE.rglob("*.html")) + list(PHASE.rglob("*.txt")):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 6000, path.as_posix())

    def test_threat_model_and_checklist_keep_external_boundaries(self):
        threat = load("threat-model.json")
        checklist = load("complete-incomplete-checklist.json")
        self.assertFalse(threat["exhaustive"])
        self.assertGreaterEqual(len(threat["threats"]), 8)
        self.assertIn("software_to_authority_substitution", {row["threat"] for row in threat["threats"]})
        self.assertTrue({"real_gmut_data_and_likelihood", "real_thos_arms", "production_freed_id", "maori_authority_review", "independent_reproduction", "stage20"}.issubset(checklist["incomplete"]))


if __name__ == "__main__":
    unittest.main()
