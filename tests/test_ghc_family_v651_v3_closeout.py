import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v651-v3"
SOURCE = "7706cd8d92b1911e0cb61542469707baf2ec3ac6"
X1 = "111e53d75eaa3560b48c3573507552b9ddb5ddfc"
EVIDENCE = "449f3a29402459a66838cbf1cc8a3b110c145162"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TamarV651V3CloseoutTests(unittest.TestCase):
    def test_final_truth_uses_only_permitted_outcomes(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["full_repository_suite_run"])
        self.assertFalse(truth["named_or_detached_replay_run"])
        self.assertFalse(truth["independent_reproduction_claimed"])

    def test_negatives_and_gates_are_preserved(self):
        negatives = load("final/retained-negative-register.json")
        self.assertEqual(negatives["evidence_effective"], 6816)
        self.assertEqual(negatives["closeout_operational"], 8)
        self.assertEqual(negatives["effective"], 6824)
        self.assertTrue(negatives["no_failure_erased"])
        gates = load("final/gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 53)
        self.assertEqual(gates["effective_exact_gates"], 54)
        self.assertEqual(gates["silently_closed"], 0)

    def test_method_flow_retains_paired_witnesses(self):
        summary = load("method-flow/method-flow-summary.json")
        self.assertTrue(summary["valid"])
        self.assertEqual(summary["counts"]["methods"], 33)
        self.assertEqual(summary["counts"]["states"]["preferred"], 33)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 34, "pass": 33})

    def test_closeout_and_seal_bind_exact_anchors(self):
        closeout = load("closeout/closeout-record.json")
        self.assertTrue(closeout["combined_closeout_and_seal"])
        self.assertEqual(closeout["source"], SOURCE)
        self.assertEqual(closeout["x1_commit"], X1)
        self.assertEqual(closeout["evidence_commit"], EVIDENCE)
        self.assertEqual(closeout["expected_final_parent"], "5b46077beb30019d5904c7d6d8fac5202c00ab82")
        self.assertEqual(closeout["expected_phase_commit_count"], 4)
        seal = load("seal/seal-candidate.json")
        self.assertEqual(seal["final_head_binding"], "commit_containing_this_record")
        self.assertTrue(seal["final_validation_required"])
        self.assertTrue(seal["route_held_until_validation"])

    def test_final_validation_contract_is_exact_and_bounded(self):
        contract = load("final/final-validation-contract.json")
        self.assertEqual(contract["eligible_tests"], 88)
        self.assertEqual(contract["v651_v1_eligible"], 22)
        self.assertEqual(contract["v651_v2_eligible"], 35)
        self.assertEqual(contract["v651_v3_eligible"], 31)
        self.assertEqual(len(contract["exclusions"]), 5)
        self.assertTrue(contract["single_successful_canonical_pass"])
        self.assertTrue(contract["no_replay_after_success"])
        self.assertFalse(contract["full_repository_suite"])
        self.assertFalse(contract["named_or_detached_replay"])

    def test_static_report_has_structural_accessibility_basics(self):
        report = (ROOT / "reports/final-static-report.html").read_text(encoding="utf-8")
        for token in ("<html lang='en'>", "Skip to content", "<main id='main'>", "aria-label='Report sections'", "<caption>", "scope='col'", "scope='row'", "NOT_READY_FOR_STAGE_20", "assistive-technology", "affected-user"):
            self.assertIn(token, report)
        self.assertIn("not complete accessibility conformance", report)

    def test_overview_handoff_and_document_caps(self):
        overview = (ROOT / "overview/final-integrated-overview.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\b[\w'-]+\b", overview))
        self.assertGreaterEqual(words, 1500)
        self.assertLessEqual(words, 6000)
        handoff = (ROOT / "handoffs/sylven-arc-v651-v4-activation.md").read_text(encoding="utf-8")
        self.assertIn("PREPARED_NOT_SENT", handoff)
        self.assertNotRegex(handoff, r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")
        self.assertNotIn("<source_thread_id>", handoff)
        self.assertNotIn("codex://", handoff)
        self.assertTrue(load("validation/closeout-build-receipt.json")["valid"])

    def test_environment_was_observed_without_mutation(self):
        receipt = load("final/environment-receipt.json")
        self.assertEqual(receipt["codex_cli_observed"], "0.144.5")
        self.assertEqual(receipt["codex_desktop_observed"], "26.715.4045.0")
        for field in ("desktop_updated", "sandbox_or_hyperv_session", "elevation", "host_security_weakened", "windows_feature_changed", "unrelated_installation", "reboot"):
            self.assertFalse(receipt[field])

    def test_route_remains_prepared_and_unsent(self):
        route = load("route/final-phase-state.json")
        self.assertEqual(route["target_exact_title"], "Sylven Arc")
        self.assertEqual(route["target_phase"], "v651-v4")
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
