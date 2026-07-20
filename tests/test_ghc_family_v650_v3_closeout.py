from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v650-v3"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V650V3CloseoutTests(unittest.TestCase):
    def test_final_truth_is_bounded_and_held(self):
        truth = load("phase-truth-final.json")
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 5807)
        self.assertEqual((truth["open_gaps"], truth["exact_gates"]), (45, 46))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["terminal_route"], "PREPARED_NOT_SENT")
        self.assertTrue(truth["final_external_validation_pending"])

    def test_closeout_and_seal_candidate(self):
        closeout = load("closeout/closeout-receipt.json")
        seal = load("closeout/seal-receipt.json")
        self.assertEqual(closeout["phase_commit_plan"], 3)
        self.assertTrue(closeout["x1_before_x2"] and closeout["evidence_remote_equal_before_closeout"])
        self.assertFalse(closeout["terminal_message_sent"])
        self.assertEqual(seal["retained_negatives"], 5807)
        self.assertFalse(seal["retained_negatives_erased"])

    def test_baton_word_range_and_privacy_boundary(self):
        baton = (PHASE / "handoffs/orin-thale-v650-v4-activation.md").read_text(encoding="utf-8")
        words = len(baton.split())
        self.assertGreaterEqual(words, 8000)
        self.assertLessEqual(words, 20000)
        self.assertIn("PREPARED_NOT_SENT", baton)
        self.assertNotIn("source_thread_id", baton.casefold())
        self.assertNotIn("thread_id", baton.casefold())
        self.assertNotIn("C:\\Users\\", baton)

    def test_final_manifest_contracts(self):
        owner = load("validation/final-owner-manifest.json")
        staged = load("validation/final-staged-manifest.json")
        review = load("validation/final-staged-review.json")
        owner_files = [path for path in PHASE.rglob("*") if path.is_file()]
        self.assertEqual(owner["entry_count"] + len(owner["self_exclusions"]), len(owner_files))
        self.assertEqual(staged["entry_count"] + len(staged["self_exclusions"]), review["intended_path_count"])
        self.assertTrue(review["passed"])
        self.assertEqual(review["x1_frozen_changes"], [])

    def test_method_flow_and_negatives(self):
        validation = load("method-flow/final-method-flow-validation.json")
        summary = load("method-flow/final-method-flow-summary.json")
        self.assertTrue(validation["valid"])
        self.assertEqual(summary["counts"]["methods"], 15)
        self.assertEqual(summary["counts"]["witness_results"], {"fail": 15, "pass": 15})
        self.assertEqual(load("retained-negative-register-final.json")["effective_total"], 5807)

    def test_environment_and_route_remain_safe(self):
        env = load("environment/final-environment-receipt.json")
        self.assertTrue(env["versions_verified_only"])
        for key in ("desktop_updated", "sandbox_or_hyperv_launched", "elevation", "host_security_weakened", "windows_feature_changed", "unrelated_software_installed", "reboot"):
            self.assertFalse(env[key])
        route = load("orchestration/terminal-route-state-final.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(route["sent"])

    def test_terminal_validation_contract_is_single_pass(self):
        contract = load("validation/final-canonical-validation-contract.json")
        self.assertEqual(contract["raw_test_count"], 71)
        self.assertEqual(contract["eligible_test_count"], 70)
        self.assertFalse(contract["full_repository_suite"])
        self.assertFalse(contract["named_replay"] or contract["detached_replay"] or contract["post_success_replay"])

    def test_documents_and_owner_threshold(self):
        receipt = load("validation/final-document-cap-receipt.json")
        self.assertTrue(receipt["all_under_20000"] and receipt["baton_within_8000_20000"])
        self.assertTrue(load("validation/final-owner-file-threshold.json")["below_threshold"])


if __name__ == "__main__":
    unittest.main()
