import json
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v650-v5"
SOURCE = "e3d115d7caade153086dea794131035bcd2192d0"
X1_INITIAL = "7c15d7e0f96e1ce5a1b7fd6049ef3c3285debc30"
X1_FINAL = "56ff8d5ab41d4b477184c854037122c81e2cc6a3"
EVIDENCE = "f485c4b053272eb384594d989ceeb6d85160111a"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TamarV650V5CloseoutTests(unittest.TestCase):
    def test_phase_truth_is_sealed_pending_one_external_pass(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["state"], "SEALED_PENDING_EXTERNAL_CANONICAL_PASS")
        self.assertEqual(truth["canonical_validation"], "pending_external_exact_head_pass")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_team_reproduction"])

    def test_all_anchors_are_declared_and_ancestral(self):
        ancestry = load("closeout/source-ancestry.json")
        self.assertEqual(ancestry["source"], SOURCE)
        self.assertEqual(ancestry["x1_initial"], X1_INITIAL)
        self.assertEqual(ancestry["x1_final"], X1_FINAL)
        self.assertEqual(ancestry["evidence"], EVIDENCE)
        for anchor in (SOURCE, X1_INITIAL, X1_FINAL, EVIDENCE):
            completed = subprocess.run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=REPO)
            self.assertEqual(completed.returncode, 0, anchor)

    def test_distribution_and_terminal_boundaries(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["proposal_count"], 20)
        self.assertEqual(truth["distribution"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertIn("no consciousness", truth["boundary"])
        self.assertIn("Stage 20 authorization", truth["boundary"])

    def test_negatives_and_gates_are_exact(self):
        negatives = load("retained-negative-register.json")
        self.assertEqual(negatives["effective_total"], 6055)
        self.assertEqual(negatives["x1_operational"], 22)
        self.assertEqual(negatives["x2_operational"], 4)
        self.assertEqual(negatives["closeout_operational"], 4)
        self.assertEqual(negatives["executed_rejected_synthetic_mutations"], 100)
        self.assertEqual(negatives["erased"], 0)
        gates = load("exact-open-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 47)
        self.assertEqual(gates["effective_exact_gates"], 48)
        self.assertEqual(gates["silently_closed"], 0)

    def test_method_flow_retains_failures_and_corrections(self):
        state = load("method-flow/method-flow-state.json")
        self.assertEqual(state["counts"]["methods"], 30)
        self.assertEqual(state["counts"]["witness_results"]["fail"], 30)
        self.assertEqual(state["counts"]["witness_results"]["pass"], 32)
        self.assertEqual(state["counts"]["states"]["preferred"], 30)
        stale = load("validation/stale-label-review.json")
        self.assertEqual(stale["confirmed_current_stale_claim_count"], 0)
        self.assertTrue(stale["passed"])

    def test_portfolios_and_skill_boundaries_remain_exact(self):
        for name, count in {
            "safe-now-execution.json": 40,
            "candidate-execution.json": 30,
            "skill-execution.json": 20,
            "runner-execution.json": 10,
            "clean-fix-refine-execution.json": 40,
        }.items():
            receipt = load(f"portfolios/{name}")
            self.assertEqual(receipt["completed"], count)
        self.assertFalse(load("portfolios/skill-execution.json")["global_install"])

    def test_closeout_and_seal_are_truthfully_pending(self):
        closeout = load("closeout/closeout-receipt.json")
        seal = load("closeout/seal-receipt.json")
        self.assertEqual(closeout["final_canonical_validation"], "PENDING_EXTERNAL_EXACT_HEAD_PASS")
        self.assertEqual(seal["seal_state"], "COMMITTED_PACKET_PENDING_EXTERNAL_CANONICAL_PASS")
        self.assertFalse(seal["full_repository_suite_run"])
        self.assertFalse(seal["post_success_replay_allowed"])
        self.assertFalse(seal["sandbox_or_hyperv_used"])

    def test_final_validation_contract_is_scoped(self):
        contract = load("validation/final-canonical-validation-contract.json")
        self.assertEqual(contract["test_count"], 62)
        self.assertEqual(contract["minimal_check_count"], 25)
        self.assertFalse(contract["full_repository_suite"])
        self.assertTrue(contract["one_successful_pass"])
        self.assertFalse(contract["post_success_replay"])

    def test_document_and_owner_caps_pass(self):
        documents = load("validation/final-document-cap-receipt.json")
        owner = load("validation/final-owner-file-threshold.json")
        self.assertTrue(documents["passed"])
        self.assertEqual(documents["violations"], [])
        self.assertLess(documents["maximum_words"], 20000)
        self.assertFalse(owner["exceeded"])
        self.assertFalse(owner["inherited_baseline_counted"])

    def test_route_is_prepared_not_sent_and_report_is_qualified(self):
        route = load("orchestration/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["messages_sent"], 0)
        self.assertFalse(route["cross_platform_send"])
        report = (ROOT / "report.html").read_text(encoding="utf-8").lower()
        self.assertIn("not complete accessibility conformance", report)
        self.assertIn("not_ready_for_stage_20", report)


if __name__ == "__main__":
    unittest.main()
