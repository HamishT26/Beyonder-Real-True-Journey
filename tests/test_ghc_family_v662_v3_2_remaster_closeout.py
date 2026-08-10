"""Exact-final lifecycle checks for the Neris v662-v3-2 remaster."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = Path("docs/neris-solane/v662-v3-2-remaster")
PHASE = ROOT / PHASE_ROOT
BRANCH = "codex/GHC-Family/neris-solane-v662-v3-2-remaster"
SOURCE_FIRST_FINAL = "9d35f2c60bc1d124bbc67d000e7f5a4da6d95410"
X1 = "9b61b218956031d80da66a59924713778b63f31f"
EVIDENCE = "999de05624682c19226c1bd5f57f2682468ff072"
CORRECTION = "f8e9f59b0e16cd11da5b08cd00beafe65e6d7bf6"
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}


def read_json(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {completed.stderr[-1000:]}")
    return completed.stdout.strip()


def git_bytes(revision: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if completed.returncode:
        raise AssertionError(f"missing Git blob {revision}:{path}")
    return completed.stdout


class TestV662V3RemasterCloseout(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gate = read_json("closeout/correction-to-final-gate.json")
        cls.truth = read_json("truth/final-truth.json")
        cls.flow = read_json("method-flow/method-flow-state-final.json")
        cls.failures = read_json("truth/closeout-operational-failures.json")
        cls.inventory = read_json("validation/preflight-inventory-correction-snapshot.json")
        cls.pilots = read_json("validation/historical-pilot-receipt.json")
        cls.selection = read_json("validation/final-selection-contract.json")
        cls.owner_manifest = read_json("validation/final-owner-manifest.json")
        cls.delta_manifest = read_json("validation/final-delta-manifest.json")
        cls.privacy = read_json("validation/final-privacy-scan.json")
        cls.document = read_json("validation/final-document-cap.json")
        cls.staged = read_json("validation/final-staged-review.json")
        cls.validation = read_json("validation/final-validation.json")
        cls.route = read_json("routing/route-state-final.json")

    def test_01_final_is_direct_single_parent_child_of_correction(self) -> None:
        self.assertEqual(git("rev-parse", "HEAD^"), CORRECTION)
        self.assertEqual(git("rev-parse", "HEAD^^"), EVIDENCE)
        self.assertEqual(git("rev-parse", "HEAD^^^"), X1)
        self.assertEqual(git("rev-parse", "HEAD^^^^"), SOURCE_FIRST_FINAL)
        parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()
        self.assertEqual(len(parents), 2)
        self.assertEqual(parents[1], CORRECTION)
        self.assertEqual(git("rev-list", "--count", f"{SOURCE_FIRST_FINAL}..HEAD"), "4")
        self.assertEqual(git("rev-list", "--merges", f"{SOURCE_FIRST_FINAL}..HEAD"), "")
        self.assertEqual(git("branch", "--show-current"), BRANCH)

    def test_02_correction_gate_records_clean_live_equality(self) -> None:
        self.assertEqual(self.gate["x1"], X1)
        self.assertEqual(self.gate["evidence"], EVIDENCE)
        self.assertEqual(self.gate["correction"], CORRECTION)
        self.assertEqual(self.gate["local"], CORRECTION)
        self.assertEqual(self.gate["local"], self.gate["upstream"])
        self.assertEqual(self.gate["local"], self.gate["tracking"])
        self.assertEqual(self.gate["local"], self.gate["fresh_live"])
        self.assertTrue(self.gate["four_way_equal"])
        self.assertEqual(self.gate["divergence"], {"ahead": 0, "behind": 0})
        self.assertEqual(self.gate["merges"], 0)

    def test_03_x1_and_x2_manifest_domains_remain_immutable(self) -> None:
        x1_manifest = read_json("validation/x1-content-manifest.json")
        x2_manifest = read_json("validation/x2-content-manifest.json")
        for entry in x1_manifest["entries"]:
            self.assertEqual(git_bytes(X1, entry["path"]), git_bytes("HEAD", entry["path"]), entry["path"])
        for entry in x2_manifest["entries"]:
            payload = git_bytes("HEAD", entry["path"])
            self.assertEqual(len(payload), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(payload).hexdigest(), entry["sha256"], entry["path"])

    def test_04_final_truth_is_exact_and_terminally_bounded(self) -> None:
        self.assertEqual(self.truth["frozen_proposals"], 3530)
        self.assertEqual(self.truth["selected_inherited_credit"], 0)
        self.assertEqual(self.truth["outcomes"], OUTCOMES)
        self.assertEqual(self.truth["effective_negatives"], 23044)
        self.assertEqual(self.truth["effective_methods"], 7638)
        self.assertEqual(self.truth["open_gaps"], 149)
        self.assertEqual(self.truth["exact_gates"], 148)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(self.truth["same_owner_only"])
        self.assertFalse(self.truth["independent_reproduction"])

    def test_05_method_flow_retains_every_phase_failure_and_recovery(self) -> None:
        self.assertEqual(self.flow["method_count"], 53)
        self.assertEqual(self.flow["failed_witness_count"], 213)
        self.assertEqual(self.flow["passing_witness_count"], 53)
        self.assertEqual(self.flow["effective_negatives"], 23044)
        self.assertEqual(self.flow["effective_methods"], 7638)
        self.assertEqual(self.flow["counts"]["witnesses"], 266)
        self.assertEqual(len({row["method_id"] for row in self.flow["methods"]}), 53)
        self.assertEqual(len({row["witness_id"] for row in self.flow["witnesses"]}), 266)
        self.assertTrue(self.flow["all_failures_retained"])

    def test_06_closeout_failures_are_attributable_and_zero_credit(self) -> None:
        self.assertEqual(self.failures["failure_count"], 2)
        self.assertTrue(self.failures["all_zero_credit"])
        self.assertEqual(
            {row["negative_id"] for row in self.failures["failures"]},
            {"V6623R-CLOSEOUT-N001", "V6623R-CLOSEOUT-N002"},
        )
        self.assertTrue(all(row["failed_credit"] == 0 and row["canonical_credit"] == 0 for row in self.failures["failures"]))

    def test_07_inventory_snapshot_ran_no_test_bodies(self) -> None:
        self.assertEqual(self.inventory["revision"], CORRECTION)
        self.assertEqual(self.inventory["tests_discovered"], 7310)
        self.assertEqual(self.inventory["unique_tests"], 7310)
        self.assertEqual(self.inventory["modules"], 502)
        self.assertEqual(self.inventory["loader_errors"], 0)
        self.assertEqual(self.inventory["duplicate_ids"], 0)
        self.assertEqual(self.inventory["test_bodies_run"], 0)
        self.assertEqual(self.inventory["complete_suite_credit"], 0)

    def test_08_historical_pilots_are_bounded_zero_suite_credit(self) -> None:
        self.assertEqual(len(self.pilots["pilots"]), 4)
        self.assertEqual(self.pilots["tests"], 48)
        self.assertEqual(self.pilots["passed"], 48)
        self.assertEqual(self.pilots["complete_suite_credit"], 0)
        self.assertTrue(self.pilots["same_owner_only"])
        self.assertFalse(self.pilots["independent_reproduction"])

    def test_09_final_selection_contract_is_complete_and_one_shot(self) -> None:
        self.assertEqual(self.selection["discovery_root"], "tests")
        self.assertEqual(self.selection["pattern"], "test*.py")
        self.assertIsNone(self.selection["top_level_root_override"])
        self.assertTrue(self.selection["every_current_test_id"])
        self.assertEqual(self.selection["duplicate_policy"], "reject")
        self.assertEqual(self.selection["omission_policy"], "reject")
        self.assertEqual(self.selection["definition_commit_rule"], "last commit that changed exact module bytes")
        self.assertTrue(self.selection["blob_equality_required"])
        self.assertFalse(self.selection["historical_assertion_editing"])
        self.assertEqual(self.selection["successful_invocations_required"], 1)
        self.assertFalse(self.selection["replay_after_success"])

    def test_10_x2_quota_and_tooling_evidence_remains_visible(self) -> None:
        approval = read_json("evidence/approval-packet-receipts.json")
        cfr = read_json("evidence/clean-fix-refine-receipts.json")
        tools = read_json("tooling/skill-runner-aggregate.json")
        self.assertEqual(approval["counts"]["safe_total"], 50)
        self.assertEqual(approval["counts"]["candidate_total"], 30)
        self.assertEqual(approval["counts"]["owner_exact"], 10)
        self.assertEqual(approval["counts"]["owner_blocked"], 5)
        self.assertEqual(cfr["counts"], {"owner_completed": 30, "successor_recommendations": 30})
        self.assertFalse(cfr["destructive_cleanup_performed"])
        self.assertEqual(tools["skills_built_validated_smoke_used"], 10)
        self.assertEqual(tools["runners_built_invoked"], 10)
        self.assertEqual(tools["global_skill_promotions"], 10)
        self.assertEqual(len(tools["successor_skill_ideas"]), 10)
        self.assertEqual(len(tools["successor_runner_ideas"]), 10)
        self.assertFalse(tools["plugin_caches_mutated"])

    def test_11_final_owner_and_delta_manifests_replay_git_blobs(self) -> None:
        for manifest in (self.owner_manifest, self.delta_manifest):
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            self.assertEqual(manifest["hash_domain"], "Exact Git-clean bytes with CRLF and CR normalized to LF")
            self.assertEqual(len({row["path"] for row in manifest["entries"]}), manifest["entry_count"])
            for entry in manifest["entries"]:
                payload = git_bytes("HEAD", entry["path"])
                self.assertEqual(len(payload), entry["bytes"], entry["path"])
                self.assertEqual(hashlib.sha256(payload).hexdigest(), entry["sha256"], entry["path"])
        self.assertTrue(set(self.owner_manifest["exclusions"]).isdisjoint({row["path"] for row in self.owner_manifest["entries"]}))

    def test_12_privacy_document_staged_and_validation_receipts_pass(self) -> None:
        self.assertEqual(len(self.privacy["classes"]), 5)
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertFalse(self.privacy["privacy_complete"])
        self.assertTrue(self.document["valid"])
        self.assertEqual(self.document["over_cap"], [])
        self.assertEqual(self.staged["state"], "EXACT_STAGED_REVIEW")
        self.assertTrue(self.staged["valid"])
        self.assertEqual(self.staged["missing"], [])
        self.assertEqual(self.staged["unexpected"], [])
        self.assertTrue(self.validation["valid"])
        self.assertEqual(self.validation["passed"], self.validation["total"])
        self.assertEqual(self.validation["total"], 18)
        self.assertEqual(self.validation["json_errors"], [])

    def test_13_every_phase_json_file_parses(self) -> None:
        paths = list(PHASE.rglob("*.json"))
        self.assertGreaterEqual(len(paths), 160)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                json.loads(path.read_text(encoding="utf-8"))

    def test_14_route_is_one_edge_prepared_not_sent(self) -> None:
        self.assertEqual(self.route["current"]["owner"], "Neris Solane")
        self.assertEqual(self.route["current"]["variant"], "v662-v3-2-remaster")
        self.assertEqual(self.route["current"]["canonical_phase"], "v662-v3")
        self.assertEqual(
            self.route["next"],
            {"owner": "Vesper Arlen", "phase": "v662-v4", "endpoint_kind": "main_task", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"},
        )
        self.assertEqual(self.route["successor_after_vesper"]["owner"], "Lyren Moss")
        self.assertEqual(self.route["successor_after_vesper"]["phase"], "v662-v5")
        self.assertFalse(self.route["message_attempted"])
        self.assertFalse(self.route["sent"])
        self.assertFalse(self.route["acknowledged"])
        self.assertEqual(self.route["delivery_count"], 0)
        self.assertTrue(self.route["one_edge_at_a_time"])
        self.assertFalse(self.route["substitute_endpoint"])

    def test_15_activation_packet_contains_identity_and_authority_boundaries(self) -> None:
        packet = (PHASE / "routing/vesper-arlen-v662-v4-activation-candidate.md").read_text(encoding="utf-8")
        lower = packet.lower()
        self.assertGreaterEqual(len(packet.split()), 450)
        self.assertIn("relational working language only", lower)
        for phrase in (
            "consciousness",
            "sentience",
            "legal personhood",
            "identity continuity",
            "employment",
            "qualification",
            "independent agency",
            "m\u0101ori authority",
            "independent reproduction",
            "theory-of-everything",
            "stage 20",
        ):
            self.assertIn(phrase, lower)
        self.assertIn("existing exact-title main task `vesper arlen`", lower)
        self.assertIn("`lyren moss`", lower)
        self.assertIn("message acknowledgement", lower)

    def test_16_closeout_report_is_substantive_and_accessible(self) -> None:
        report = (PHASE / "closeout/terminal-closeout.md").read_text(encoding="utf-8")
        html = (PHASE / "reports/final-accessible-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(report.split()), 1800)
        self.assertIn("relational working language only", report.lower())
        self.assertIn("m\u0101ori authority", report.lower())
        self.assertIn("NOT_READY_FOR_STAGE_20", report)
        self.assertIn('href="#main"', html)
        self.assertIn('id="main"', html)
        self.assertIn("privacy-complete", html)

    def test_17_canonical_state_is_not_prematurely_claimed(self) -> None:
        self.assertEqual(self.truth["canonical_state"], "NOT_RUN_EXACT_FINAL_REQUIRED")
        self.assertEqual(self.truth["canonical_success_count"], 0)
        self.assertFalse(self.truth["message_attempted"])
        self.assertFalse(self.truth["message_sent"])
        self.assertTrue((ROOT / "scripts/ghc_family_v662_v3_2_remaster_canonical_driver.py").is_file())

    def test_18_final_workload_receipt_preserves_solo_scope(self) -> None:
        workload = read_json("wellbeing/final-workload-check.json")
        self.assertTrue(workload["solo"])
        self.assertFalse(workload["delegated"])
        self.assertEqual(workload["subagents"], 0)
        self.assertEqual(workload["historical_pilot_tests"], 48)
        self.assertFalse(workload["complete_suite_run"])
        self.assertTrue(workload["pause_redirect_stop_right_preserved"])


if __name__ == "__main__":
    unittest.main()
