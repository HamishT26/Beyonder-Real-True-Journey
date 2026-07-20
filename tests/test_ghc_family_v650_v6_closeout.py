"""Combined closeout and seal tests for Sylven Arc v650-v6."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v650-v6"
SOURCE = "29439b5ed36d5b181c0d0f6a428dd872673d5194"
X1 = "b8e0109a003e2fa90794b48b3691dc76a3c06ef2"
EVIDENCE = "b8b858c3eb91201bcdea81813999a19426089f97"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class TestSylvenV650V6Closeout(unittest.TestCase):
    def test_closeout_receipt_preserves_outcomes(self):
        receipt = load("closeout/closeout-receipt.json")
        self.assertEqual(receipt["x1_commit"], X1)
        self.assertEqual(receipt["evidence_commit"], EVIDENCE)
        self.assertEqual(receipt["outcomes"], {"completed":14,"represented":4,"open_gap":1,"exact_gate":1})
        self.assertEqual(receipt["final_canonical_validation"], "PENDING_EXTERNAL_EXACT_HEAD_PASS")
        self.assertFalse(receipt["full_repository_suite"])

    def test_combined_seal_binds_to_containing_commit(self):
        seal = load("closeout/combined-seal-receipt.json")
        self.assertEqual(seal["seal_binding"], "containing_single_parent_commit")
        self.assertEqual(seal["evidence_parent"], EVIDENCE)
        self.assertTrue(seal["x1_immutable"])
        self.assertTrue(seal["evidence_immutable"])
        self.assertEqual(seal["phase_commits_expected"], 3)
        self.assertFalse(seal["post_success_replay"])

    def test_final_phase_truth_is_fail_closed(self):
        truth = load("final/phase-truth.json")
        self.assertEqual(truth["source_head"], SOURCE)
        self.assertEqual(truth["x1_commit"], X1)
        self.assertEqual(truth["evidence_commit"], EVIDENCE)
        self.assertEqual(truth["final_head_binding"], "containing_commit")
        self.assertEqual(truth["phase_commit_count"], 3)
        self.assertFalse(truth["full_repository_suite"])
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_all_negatives_remain_additive(self):
        register = load("final/retained-negative-register.json")
        self.assertEqual(register["activation_baseline"], 6056)
        self.assertEqual(register["x1_operational"], 19)
        self.assertEqual(register["synthetic_executed_and_rejected"], 100)
        self.assertEqual(register["x2_operational"], 3)
        self.assertEqual(register["closeout_operational"], 1)
        self.assertEqual(register["sealed_effective"], 6179)
        self.assertFalse(register["negative_erased"])

    def test_open_and_exact_gates_remain_open(self):
        gates = load("final/exact-open-gate-register.json")
        self.assertEqual(gates["effective_open_gaps"], 48)
        self.assertEqual(gates["effective_exact_gates"], 49)
        self.assertEqual(gates["silently_closed"], 0)
        self.assertTrue(gates["empirical_professional_legal_cultural_maori_and_stage20_gates_open"])

    def test_checklist_distinguishes_external_terminal_steps(self):
        checklist = load("final/complete-incomplete-checklist.json")
        self.assertIn("exact-title Eiren baton acknowledgement", checklist["pending_external"])
        self.assertIn("Māori-authority review", checklist["incomplete_authority_or_evidence"])
        self.assertEqual(checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_environment_was_verified_without_host_change(self):
        receipt = load("final/environment-version-receipt.json")
        self.assertTrue(receipt["verification_only"])
        for key in ("desktop_updated", "elevation", "security_weakened", "windows_feature_changed", "unrelated_software_installed", "reboot", "sandbox_or_hyperv_action"):
            self.assertFalse(receipt[key], key)

    def test_accessibility_evaluation_is_reserved(self):
        receipt = load("final/accessibility-evaluation-reservation.json")
        self.assertTrue(receipt["structural_report_present"])
        self.assertTrue(receipt["manual_keyboard_reserved"])
        self.assertTrue(receipt["assistive_technology_reserved"])
        self.assertTrue(receipt["maori_language_reserved"])
        self.assertTrue(receipt["affected_user_evaluation_reserved"])
        self.assertFalse(receipt["complete_accessibility_claim"])

    def test_closeout_method_flow_retains_refused_seal(self):
        ledger = load("closeout/method-flow-state.json")
        self.assertEqual(len(ledger["methods"]), 1)
        self.assertEqual([row["result"] for row in ledger["witnesses"]], ["fail", "pass"])
        self.assertEqual(ledger["methods"][0]["recommendation_state"], "preferred")

    def test_final_validation_contract_is_scoped_and_single_pass(self):
        contract = load("final/final-validation-contract.json")
        self.assertFalse(contract["full_repository_suite"])
        self.assertTrue(contract["eiren_owns_full_repository_suite"])
        self.assertTrue(contract["one_successful_exact_final_aggregate"])
        self.assertFalse(contract["post_success_replay"])
        self.assertFalse(contract["detached_or_named_replay"])
        self.assertEqual(len(contract["test_modules"]), 6)

    def test_terminal_route_is_prepared_not_sent(self):
        route = load("final/terminal-route-state.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["target_title"], "Eiren Kestrel")
        self.assertEqual(route["target_phase"], "v650-v7")
        self.assertFalse(route["target_resolved"])
        self.assertEqual(route["messages_sent"], 0)

    def test_final_static_report_has_landmarks_and_reservations(self):
        report = (ROOT / "final/final-report.html").read_text(encoding="utf-8")
        for token in ('href="#main"', '<header>', '<nav aria-label="Final report">', '<main id="main">', '<footer>'):
            self.assertIn(token, report)
        self.assertIn("affected-user evaluation remain reserved", report)
        self.assertIn("NOT_READY_FOR_STAGE_20", report)

    def test_prepared_baton_is_sanitized_and_not_delivery_claim(self):
        baton = (ROOT / "handoffs/eiren-kestrel-v650-v7-prepared.md").read_text(encoding="utf-8")
        self.assertIn("preparation artifact only", baton)
        self.assertIn("not evidence of delivery", baton)
        self.assertIn("PREPARED_NOT_SENT", load("final/terminal-route-state.json")["state"])
        forbidden_tokens = (
            "source" + "_" + "thread" + "_" + "id",
            "thread" + "_" + "id=",
            "session" + "_" + "stream",
            "conversation" + "_" + "export",
        )
        for forbidden in forbidden_tokens:
            self.assertNotIn(forbidden, baton)

    def test_final_is_direct_child_of_evidence(self):
        self.assertEqual(
            subprocess.check_output(["git", "rev-parse", "HEAD^"], cwd=REPO, text=True).strip(),
            EVIDENCE,
        )

    def test_source_to_final_history_is_three_single_parent_commits(self):
        count = int(subprocess.check_output(["git", "rev-list", "--count", f"{SOURCE}..HEAD"], cwd=REPO, text=True))
        merges = int(subprocess.check_output(["git", "rev-list", "--merges", "--count", f"{SOURCE}..HEAD"], cwd=REPO, text=True))
        parents = subprocess.check_output(["git", "show", "-s", "--format=%P", "HEAD"], cwd=REPO, text=True).split()
        self.assertEqual(count, 3)
        self.assertEqual(merges, 0)
        self.assertEqual(len(parents), 1)
        for anchor in (SOURCE, X1, EVIDENCE):
            self.assertEqual(subprocess.run(["git", "merge-base", "--is-ancestor", anchor, "HEAD"], cwd=REPO).returncode, 0)

    def test_final_manifest_has_exact_blob_evidence(self):
        manifest = load("validation/final-staged-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        self.assertEqual(len(manifest["self_exclusions"]), 3)
        for row in manifest["entries"]:
            blob = subprocess.check_output(["git", "cat-file", "blob", row["git_blob"]], cwd=REPO)
            self.assertEqual(len(blob), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), row["sha256"], row["path"])


if __name__ == "__main__":
    unittest.main()
