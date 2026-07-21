import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5"
SOURCE = "d5c9a16b3efb76a138944d97211bc0a3b7bcd716"
X1 = "c2c51a9e4f1786a45d77390b1d2e75e170dde170"
EVIDENCE = "4815a8471e83598df9ad9dabfeeed2a53d8eaebe"
CLOSEOUT = "27b34aa5d72ce4dd3c50d2423741e9c9eba77e1a"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class V651V5CloseoutTests(unittest.TestCase):
    def test_final_truth_uses_only_permitted_outcomes(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["full_repository_suite_run"])
        self.assertFalse(truth["named_or_detached_replay_run"])
        self.assertFalse(truth["post_success_replay_run"])
        self.assertFalse(truth["independent_reproduction_claimed"])

    def test_negatives_and_gates_are_preserved(self):
        negatives = load("final/retained-negative-register.json")
        self.assertEqual(negatives["evidence_effective"], 7073)
        self.assertEqual(negatives["closeout_operational"], 13)
        self.assertEqual(negatives["effective"], 7086)
        self.assertTrue(negatives["no_failure_erased"])
        gates = load("final/gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 55)
        self.assertEqual(gates["effective_exact_gates"], 56)
        self.assertEqual(gates["silently_closed"], 0)

    def test_method_flow_retains_paired_witnesses(self):
        summary = load("method-flow/method-flow-summary.json")
        self.assertTrue(summary["valid"])
        self.assertEqual(summary["counts"]["methods"], 38)
        self.assertEqual(summary["counts"]["states"]["preferred"], 38)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 38, "pass": 38})

    def test_closeout_and_seal_bind_exact_anchors(self):
        closeout = load("closeout/closeout-record.json")
        self.assertTrue(closeout["combined_closeout_and_seal"])
        self.assertEqual(closeout["source"], SOURCE)
        self.assertEqual(closeout["x1_commit"], X1)
        self.assertEqual(closeout["evidence_commit"], EVIDENCE)
        self.assertEqual(closeout["closeout_commit"], CLOSEOUT)
        self.assertEqual(closeout["expected_final_parent"], CLOSEOUT)
        self.assertEqual(closeout["expected_phase_commit_count"], 4)
        seal = load("seal/combined-closeout-seal.json")
        self.assertEqual(seal["closeout"], CLOSEOUT)
        self.assertTrue(seal["terminal_correction"])
        self.assertEqual(seal["phase_commit_count_required"], 4)
        self.assertEqual(seal["final_head_binding"], "commit_containing_this_record")
        self.assertTrue(seal["final_validation_required"])
        self.assertTrue(seal["route_held_until_validation"])

    def test_final_validation_contract_is_exact_and_bounded(self):
        contract = load("final/final-validation-contract.json")
        self.assertEqual(len(contract["exact_lifecycle_exclusions"]), 31)
        self.assertTrue(contract["failed_incomplete_attempt_retained"])
        self.assertTrue(contract["single_successful_canonical_pass"])
        self.assertTrue(contract["no_replay_after_success"])
        self.assertTrue(contract["full_repository_suite"])
        self.assertFalse(contract["named_or_detached_replay"])

    def test_static_report_has_structural_accessibility_basics(self):
        report = (ROOT / "reports/final-static-report.html").read_text(encoding="utf-8")
        for token in ("<html lang='en'>", "Skip to content", "<main id='main'>", "aria-label='Report sections'", "<caption>", "scope='col'", "scope='row'", "NOT_READY_FOR_STAGE_20", "assistive-technology", "affected-user"):
            self.assertIn(token, report)
        self.assertIn("not complete accessibility conformance", report)

    def test_overview_baton_and_document_caps(self):
        overview = (ROOT / "overview/final-integrated-overview.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 6000)
        self.assertGreaterEqual(len(re.findall(r"\b[\w'-]+\b", overview)), 1500)
        baton = (ROOT / "handoffs/ilyra-fen-v651-v6-activation.md").read_text(encoding="utf-8")
        baton_words = len(re.findall(r"\b[\w'-]+\b", baton))
        self.assertGreaterEqual(baton_words, 8000)
        self.assertLessEqual(baton_words, 20000)
        self.assertIn("PREPARED_NOT_SENT", baton)
        self.assertTrue(load("validation/closeout-build-receipt.json")["valid"])

    def test_environment_was_observed_without_mutation(self):
        receipt = load("final/environment-receipt.json")
        self.assertEqual(receipt["codex_cli_observed"], "0.144.5")
        self.assertEqual(receipt["codex_desktop_observed"], "26.715.4045.0")
        for field in ("desktop_updated", "sandbox_or_hyperv_session", "elevation", "host_security_weakened", "windows_feature_changed", "unrelated_installation", "reboot"):
            self.assertFalse(receipt[field])

    def test_route_remains_prepared_and_unsent(self):
        route = load("route/final-phase-state.json")
        self.assertEqual(route["target_exact_title"], "Ilyra Fen")
        self.assertEqual(route["target_phase"], "v651-v6")
        self.assertEqual(route["terminal_route"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)
        self.assertFalse(route["task_created"])
        self.assertFalse(route["task_forked"])
        self.assertFalse(route["collaboration_subagent"])
        self.assertFalse(route["cross_platform_substitute"])

    def test_checklist_reproduction_and_stage20_remain_bounded(self):
        checklist = load("truth/final-complete-incomplete-checklist.json")
        self.assertIn("independent-team reproduction", checklist["incomplete"])
        reproduction = load("reproduction/final-boundary.json")
        self.assertTrue(reproduction["same_owner"])
        self.assertFalse(reproduction["independent_team"])
        board = load("final/terminal-stage20-board.json")
        self.assertEqual(board["verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(board["empirical_confirmation"])
        self.assertFalse(board["production_identity"])
        self.assertFalse(board["legal_or_cultural_authority"])


if __name__ == "__main__":
    unittest.main()
