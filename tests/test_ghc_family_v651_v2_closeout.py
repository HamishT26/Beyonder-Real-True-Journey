from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "orin-thale" / "v651-v2"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class V651V2CloseoutTests(unittest.TestCase):
    def test_final_truth_and_distribution(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertFalse(truth["full_repository_suite_run"])
        self.assertFalse(truth["named_or_detached_replay_run"])
        self.assertFalse(truth["independent_reproduction_claimed"])

    def test_negative_and_gate_retention(self):
        negatives = load("final/retained-negative-register.json")
        gates = load("final/gate-register.json")
        self.assertEqual(negatives["effective"], 6689)
        self.assertEqual((negatives["x1_operational"], negatives["x2_and_closeout_operational"], negatives["executed_rejected_synthetic"]), (9, 15, 100))
        self.assertTrue(negatives["no_failure_erased"])
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (52, 53))
        self.assertEqual(gates["silently_closed"], 0)

    def test_method_flow_balanced_retention(self):
        summary = load("method-flow/method-flow-summary.json")
        validation = load("method-flow/method-flow-validation.json")
        self.assertEqual(summary["counts"]["methods"], 22)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 23, "pass": 22})
        self.assertEqual(summary["counts"]["states"]["preferred"], 21)
        self.assertEqual(summary["counts"]["states"]["deprecated"], 1)
        self.assertTrue(summary["valid"] and validation["valid"])

    def test_route_is_prepared_not_sent(self):
        route = load("route/final-phase-state.json")
        self.assertEqual(route["target_exact_title"], "Tamar Vey")
        self.assertEqual(route["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)
        self.assertFalse(route["task_created"] or route["task_forked"] or route["collaboration_subagent"] or route["cross_platform_substitute"])

    def test_validation_contract_is_bounded(self):
        contract = load("final/final-validation-contract.json")
        self.assertEqual(contract["eligible_tests"], 58)
        self.assertEqual(contract["current_tests"], 36)
        self.assertEqual(len(contract["source_exclusions"]), 2)
        self.assertFalse(contract["full_repository_suite"])
        self.assertFalse(contract["named_or_detached_replay"])
        self.assertTrue(contract["single_successful_canonical_pass"])
        self.assertTrue(contract["no_replay_after_success"])

    def test_baton_and_overview_word_contracts(self):
        baton = (ROOT / "handoffs" / "tamar-vey-v651-v3-activation.md").read_text(encoding="utf-8")
        overview = (ROOT / "overview" / "final-integrated-overview.md").read_text(encoding="utf-8")
        baton_words = len(re.findall(r"\b\w+\b", baton, flags=re.UNICODE))
        overview_words = len(re.findall(r"\b\w+\b", overview, flags=re.UNICODE))
        self.assertGreaterEqual(baton_words, 8000)
        self.assertLessEqual(baton_words, 20000)
        self.assertGreaterEqual(overview_words, 1500)
        self.assertLessEqual(overview_words, 6000)

    def test_baton_is_sanitized(self):
        baton = (ROOT / "handoffs" / "tamar-vey-v651-v3-activation.md").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", baton, flags=re.I))
        self.assertNotRegex(baton, r"[A-Z]:\\(?:Users|GHC-Archives)\\")
        self.assertNotIn("<source_thread_id>", baton)
        self.assertNotIn("<codex_delegation>", baton)
        self.assertNotIn("app://", baton)

    def test_outcomes_portfolios_and_mutations(self):
        outcomes = load("outcomes/evidence-ledger.json")
        mutation = load("validation/mutation-execution-summary.json")
        self.assertEqual(len(outcomes["proposals"]), 20)
        self.assertEqual((mutation["executed"], mutation["rejected_or_quarantined"], mutation["accepted"]), (100, 100, 0))
        self.assertEqual(load("portfolios/safe-now-execution.json")["completed"], 40)
        self.assertEqual(load("portfolios/candidate-execution.json")["completed"], 30)
        self.assertEqual(load("portfolios/clean-fix-refine-execution.json")["completed"], 40)

    def test_accessible_report_reserves_manual_evaluation(self):
        report = (ROOT / "reports" / "final-static-report.html").read_text(encoding="utf-8").casefold()
        for phrase in ("skip to content", "not_ready_for_stage_20", "manual keyboard", "assistive-technology", "māori-language", "affected-user evaluation remain reserved"):
            self.assertIn(phrase, report)

    def test_closeout_and_seal_candidates(self):
        closeout = load("closeout/closeout-record.json")
        seal = load("seal/seal-candidate.json")
        self.assertEqual(closeout["evidence_commit"], "8b3c1bb68852acc52c4554c34f1b6689a7c49efd")
        self.assertEqual(closeout["expected_phase_commit_count"], 4)
        self.assertEqual(closeout["expected_merge_count"], 0)
        self.assertEqual(closeout["expected_final_parent_count"], 1)
        self.assertTrue(closeout["valid"] and seal["valid"])
        self.assertTrue(seal["final_validation_required"] and seal["route_held_until_validation"])


if __name__ == "__main__":
    unittest.main()
