from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/orin-thale/v650-v4"
X1 = "2aef76bbfc315857ff5bd134424a346fa70d1ec3"
EVIDENCE = "6a25ee7cefa63039a4b17b56c06462b6cf622ea9"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class OrinV650V4CloseoutTests(unittest.TestCase):
    def test_final_truth_and_outcome_vocabulary(self):
        truth = load("phase-truth-final.json")
        self.assertEqual(truth["outcomes"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(truth["effective_negatives"], 5925)
        self.assertEqual((truth["open_gaps"], truth["exact_gates"]), (46, 47))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(truth["same_owner_only"])
        self.assertFalse(truth["independent_reproduction"])

    def test_negative_and_gate_totals_are_exact(self):
        negatives = load("retained-negative-register-final.json")
        self.assertEqual(negatives["activation_baseline"], 5811)
        self.assertEqual((negatives["x1_operational"], negatives["synthetic_mutations"], negatives["x2_operational"], negatives["closeout_operational"]), (5, 100, 6, 3))
        self.assertEqual(negatives["effective_total"], 5925)
        self.assertEqual(negatives["erased"], 0)
        gates = load("exact-open-gate-register-final.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (46, 47))
        self.assertEqual(gates["closed_without_exact_evidence"], 0)

    def test_method_flow_retains_fourteen_paired_witnesses(self):
        state = load("method-flow/method-flow-state.json")
        self.assertEqual(state["counts"]["methods"], 14)
        self.assertEqual(state["counts"]["witness_results"], {"fail": 14, "pass": 14})
        self.assertEqual({row["recommendation_state"] for row in state["methods"]}, {"preferred"})
        self.assertTrue(load("method-flow/method-flow-validation.json")["valid"])

    def test_baton_range_privacy_and_delivery_state(self):
        baton = (PHASE / "handoffs/tamar-vey-v650-v5-activation.md").read_text(encoding="utf-8")
        words = len(baton.split())
        self.assertGreaterEqual(words, 8000)
        self.assertLessEqual(words, 20000)
        self.assertIn("PREPARED_NOT_SENT", baton)
        for forbidden in ("source_thread_id", "thread_id", "C:\\Users\\", "file://", "codex://"):
            self.assertNotIn(forbidden.casefold(), baton.casefold())

    def test_closeout_and_seal_remain_candidates(self):
        closeout = load("closeout/closeout-receipt.json")
        seal = load("closeout/seal-candidate.json")
        self.assertEqual(closeout["phase_commit_plan"], 3)
        self.assertTrue(closeout["x1_before_x2"] and closeout["evidence_remote_equal_before_closeout"])
        self.assertFalse(closeout["terminal_message_sent"])
        self.assertEqual(seal["retained_negatives"], 5925)
        self.assertFalse(seal["retained_negatives_erased"])

    def test_terminal_route_is_prepared_not_sent(self):
        route = load("orchestration/terminal-route-state-final.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["target_title"], "Tamar Vey")
        self.assertFalse(route["sent"])
        self.assertTrue(route["target_resolution_pending"] and route["final_validation_pending"])

    def test_final_validation_contract_is_one_shot_and_bounded(self):
        contract = load("validation/final-canonical-validation-contract.json")
        self.assertEqual(contract["mode"], "one_successful_exact_final_canonical_pass_external_receipt")
        self.assertEqual(len(contract["modules"]), 6)
        self.assertEqual(contract["historical_exclusions"], [])
        self.assertFalse(contract["full_repository_suite"])
        self.assertFalse(contract["named_replay"] or contract["detached_replay"] or contract["post_success_replay"])

    def test_final_manifest_contracts_cover_exact_surfaces(self):
        owner = load("validation/final-owner-manifest.json")
        staged = load("validation/final-staged-manifest.json")
        review = load("validation/final-staged-review.json")
        owner_paths = [path for path in PHASE.rglob("*") if path.is_file()]
        self.assertEqual(owner["entry_count"] + len(owner["self_exclusions"]), len(owner_paths))
        self.assertEqual(staged["entry_count"] + len(staged["self_exclusions"]), review["intended_path_count"])
        self.assertTrue(review["passed"])
        self.assertEqual(review["frozen_x1_changes"], [])

    def test_x1_and_evidence_anchors_remain_immutable(self):
        for relative, commit in (("validation/x1-staged-manifest.json", X1), ("validation/evidence-staged-manifest.json", EVIDENCE)):
            manifest = load(relative)
            for row in manifest["entries"]:
                proc = subprocess.run(["git", "rev-parse", f"{commit}:{row['path']}"], cwd=REPO, text=True, capture_output=True)
                self.assertEqual(proc.returncode, 0, row["path"])
                self.assertEqual(proc.stdout.strip(), row["git_blob"], row["path"])

    def test_environment_document_and_threshold_boundaries(self):
        env = load("environment/final-environment-receipt.json")
        self.assertTrue(env["versions_verified_only"])
        for key in ("desktop_updated", "sandbox_or_hyperv_launched", "elevation", "host_security_weakened", "windows_feature_changed", "unrelated_software_installed", "reboot"):
            self.assertFalse(env[key])
        self.assertTrue(load("validation/final-document-cap-receipt.json")["all_under_20000"])
        self.assertTrue(load("validation/final-owner-file-threshold.json")["below_threshold"])
        self.assertTrue(load("validation/stale-label-review.json")["passed"])


if __name__ == "__main__":
    unittest.main()
