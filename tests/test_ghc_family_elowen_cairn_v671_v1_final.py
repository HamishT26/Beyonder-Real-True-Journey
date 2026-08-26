from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_elowen_cairn_v671_v1_final as final


class ElowenCairnV671V1FinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = final.OWNER_ROOT
        cls.expected_final = os.environ.get("ELOWEN_V671_EXPECTED_FINAL", "")
        if not re.fullmatch(r"[0-9a-f]{40}", cls.expected_final):
            raise RuntimeError("ELOWEN_V671_EXPECTED_FINAL must bind the exact final head")

    def read_json(self, relative: str) -> dict:
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

    def replay_manifest(self, relative: str) -> None:
        manifest = self.read_json(relative)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            data = subprocess.check_output(["git", "show", f"{self.expected_final}:{row['path']}"], cwd=ROOT)
            oid = subprocess.check_output(["git", "hash-object", "--stdin"], cwd=ROOT, input=data).decode().strip()
            self.assertEqual(
                (row["bytes"], row["git_blob_oid"], row["sha256"]),
                (len(data), oid, hashlib.sha256(data).hexdigest()),
            )

    def test_01_exact_branch_head_clean_and_tracking(self) -> None:
        self.assertEqual(self.git("branch", "--show-current"), final.BRANCH)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.expected_final)
        self.assertEqual(self.git("rev-parse", "@{upstream}"), self.expected_final)
        self.assertEqual(self.git("rev-parse", f"refs/remotes/origin/{final.BRANCH}"), self.expected_final)
        self.assertEqual(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True), "")

    def test_02_exact_three_commit_single_parent_zero_merge_history(self) -> None:
        commits = self.git("rev-list", "--reverse", f"{final.SOURCE_FINAL}..{self.expected_final}").splitlines()
        self.assertEqual(commits, [final.FROZEN_X1, final.FROZEN_EVIDENCE, self.expected_final])
        self.assertEqual(self.git("rev-list", "--count", "--merges", f"{final.SOURCE_FINAL}..{self.expected_final}"), "0")
        expected_parents = [final.SOURCE_FINAL, final.FROZEN_X1, final.FROZEN_EVIDENCE]
        for child, parent in zip(commits, expected_parents, strict=True):
            self.assertEqual(self.git("rev-parse", f"{child}^"), parent)
            self.assertEqual(len(self.git("show", "-s", "--format=%P", child).split()), 1)

    def test_03_final_truth_and_four_outcomes_are_exact(self) -> None:
        truth = self.read_json("closeout/phase-truth.json")
        self.assertEqual(truth["core_outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(set(truth["core_outcomes"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertEqual(truth["proposal_chain_before"], 5550)
        self.assertEqual(truth["proposal_chain_after"], 5590)
        self.assertEqual(truth["terminal_verdict"], final.TERMINAL_VERDICT)

    def test_04_final_additive_overlay_is_exact(self) -> None:
        truth = self.read_json("closeout/phase-truth.json")
        for key, value in final.FINAL_OVERLAY.items():
            self.assertEqual(truth[key], value)

    def test_05_method_flow_preserves_failed_and_passing_witnesses(self) -> None:
        ledger = self.read_json("closeout/method-flow-final.json")
        self.assertEqual(ledger["counts"]["methods"], 230)
        self.assertEqual(ledger["counts"]["witnesses"], 419)
        self.assertEqual(ledger["counts"]["state_events"], 690)
        self.assertEqual(ledger["counts"]["recommendations"], 230)
        self.assertEqual(Counter(row["result"] for row in ledger["witnesses"]), {"pass": 230, "fail": 189})
        self.assertEqual(ledger["effective_overlay"]["effective_negatives"], 33521)

    def test_06_method_flow_skill_receipt_is_valid(self) -> None:
        receipt = self.read_json("validation/final-method-flow-validation.json")
        self.assertTrue(receipt["valid"])
        self.assertEqual(receipt["issue_count"], 0)
        self.assertEqual(receipt["method_count"], 230)
        self.assertEqual(receipt["witness_count"], 419)
        failed = self.read_json("validation/final-method-flow-validation-failed.json")
        self.assertFalse(failed["valid"])
        self.assertEqual(failed["issue_count"], 12)
        self.assertEqual(failed["failure_id"], "EC6711-FINAL-N001")
        contract = self.read_json("validation/final-contract-audit-failed.json")
        self.assertEqual(contract["failure_id"], "EC6711-FINAL-N002")
        self.assertFalse(contract["canonical_tests_executed"])
        preflight = self.read_json("validation/final-preflight-command-failed.json")
        classification = self.read_json("validation/final-privacy-classification-preflight-failed.json")
        self.assertEqual(preflight["failure_id"], "EC6711-FINAL-N003")
        self.assertEqual(classification["failure_id"], "EC6711-FINAL-N004")
        self.assertFalse(classification["broad_exemption_added"])

    def test_07_open_gaps_and_exact_gates_remain_visible(self) -> None:
        register = self.read_json("closeout/open-exact-gate-register.json")
        self.assertEqual(register["effective_open_gaps"], 257)
        self.assertEqual(register["effective_exact_gates"], 252)
        self.assertEqual(register["new_open_gaps"], ["EC6711-N037", "EC6711-N038"])
        self.assertEqual(register["new_exact_gates"], ["EC6711-N039", "EC6711-N040"])
        self.assertFalse(register["authority_promotion"])

    def test_08_retained_negative_layers_are_not_rewritten(self) -> None:
        register = self.read_json("closeout/retained-negative-register.json")
        self.assertEqual(register["tamar_repository_seal"], 33324)
        self.assertEqual(register["activation_declared_overlay"], 33329)
        self.assertEqual(register["post_route_overlay"], 33332)
        self.assertEqual(register["evidence_effective_negatives"], 33517)
        self.assertEqual(register["final_effective_negatives"], 33521)
        self.assertFalse(register["failure_erased"])

    def test_09_x1_failure_and_dependency_recovery_remain_distinct(self) -> None:
        receipt = self.read_json("validation/evidence-sequential-test-receipt.json")
        self.assertEqual(receipt["immutable_x1"]["aggregate_result"], "failed_23_of_24_zero_aggregate_pass_credit")
        self.assertEqual(receipt["immutable_x1"]["aggregate_success_credit"], 0)
        self.assertEqual(receipt["immutable_x1"]["isolated_failed_dependency_recovery"], "passed_1_of_1")
        self.assertFalse(receipt["immutable_x1"]["rerun_at_evidence_head"])

    def test_10_x2_test_selection_ran_once_and_full_suite_did_not_run(self) -> None:
        receipt = self.read_json("validation/evidence-sequential-test-receipt.json")
        self.assertEqual(receipt["current_x2"]["tests"], 30)
        self.assertEqual(receipt["current_x2"]["result"], "passed")
        self.assertEqual(receipt["dependency_corrected_x1_checks_plus_x2_tests"], 54)
        self.assertEqual(receipt["full_repository_suite"], "not_run_not_claimed")
        self.assertFalse(receipt["source_or_sibling_tests_replayed"])
        self.assertFalse(receipt["independent_reproduction"])

    def test_11_portfolios_are_completed_or_held_as_declared(self) -> None:
        portfolio = self.read_json("x2/portfolio-outcome.json")
        self.assertEqual(portfolio["counts"]["safe_now"], 60)
        self.assertEqual(portfolio["counts"]["candidates"], 30)
        self.assertEqual(portfolio["counts"]["clean_fix_refine"], 60)
        self.assertEqual(portfolio["counts"]["skills"], 20)
        self.assertEqual(portfolio["counts"]["runners"], 10)
        self.assertEqual(portfolio["exact_and_blocked_executed"], 0)
        for category in ("exact_approval", "blocked"):
            self.assertTrue(all(row["x2_state"] == "held_unexecuted" for row in portfolio["rows"][category]))

    def test_12_owner_local_skills_runners_and_tools_are_bounded(self) -> None:
        skills = self.read_json("x2/skill-evidence.json")["rows"]
        runners = self.read_json("x2/runner-evidence.json")["rows"]
        tools = self.read_json("x2/tool-evidence.json")
        self.assertEqual((len(skills), len(runners), len(tools["tools"])), (20, 10, 3))
        self.assertTrue(all(row["quick_validated"] and row["smoke_used"] and not row["global_install"] for row in skills))
        self.assertTrue(all(row["accepted"] and row["external_actions"] == 0 for row in runners))
        self.assertEqual(tools["external_actions"], 0)
        self.assertEqual((len(tools["observation_vacancy"]["accepting"]), tools["observation_vacancy"]["rejecting"]), (3, 5))
        self.assertEqual((len(tools["handover_lineage"]["accepting"]), tools["handover_lineage"]["rejecting"]), (3, 5))
        self.assertTrue(tools["footwear_guard"]["duplicate_rejected"] and tools["footwear_guard"]["nonfinite_rejected"])

    def test_13_final_overview_is_three_page_equivalent_and_bounded(self) -> None:
        text = (self.root / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", text))
        self.assertGreaterEqual(words, 1800)
        self.assertLessEqual(words, final.DOCUMENT_WORD_CEILING)
        for term in ("GMUT", "THOS", "Freed ID", "CBR", "Māori authority", final.TERMINAL_VERDICT):
            self.assertIn(term, text)

    def test_14_static_report_has_structural_accessibility(self) -> None:
        report = (self.root / "closeout/static-report.html").read_text(encoding="utf-8")
        required = ('href="#main"', '<main id="main">', '<nav aria-label="Report sections">', '<caption>Forty preregistered proposal outcomes</caption>', 'scope="col"', "scope='row'", ":focus", "@media print")
        self.assertTrue(all(token in report for token in required))
        self.assertIn("remain unperformed", report)

    def test_15_final_owner_manifest_replays_exact_head_blobs(self) -> None:
        self.replay_manifest("validation/final-owner-manifest.json")

    def test_16_final_delta_manifest_replays_exact_head_blobs(self) -> None:
        self.replay_manifest("validation/final-delta-manifest.json")

    def test_17_content_seal_replays_exact_head_blobs_and_payload(self) -> None:
        seal = self.read_json("seal/content-seal.json")
        payload = {key: value for key, value in seal.items() if key != "payload_sha256"}
        self.assertEqual(seal["payload_sha256"], final.sha256(final.canonical_bytes(payload)))
        for row in seal["files"]:
            data = subprocess.check_output(["git", "show", f"{self.expected_final}:{row['path']}"], cwd=ROOT)
            oid = subprocess.check_output(["git", "hash-object", "--stdin"], cwd=ROOT, input=data).decode().strip()
            self.assertEqual((len(data), oid, hashlib.sha256(data).hexdigest()), (row["bytes"], row["git_blob_oid"], row["sha256"]))

    def test_18_final_staged_privacy_and_review_are_valid(self) -> None:
        privacy = self.read_json("validation/final-staged-privacy.json")
        review = self.read_json("validation/final-staged-review.json")
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["confirmed_hit_count"], 0)
        self.assertTrue(review["valid"])
        self.assertEqual(review["out_of_scope"], [])
        self.assertEqual(review["frozen_x1_or_x2_changes"], [])
        self.assertLessEqual(review["owner_file_count"], final.FILE_CEILING)

    def test_19_lifecycle_replay_and_commit_ceiling_are_exact(self) -> None:
        lifecycle = self.read_json("closeout/lifecycle-replay.json")
        self.assertEqual(lifecycle["source_to_final_commits_after_commit"], 3)
        self.assertEqual(lifecycle["expected_final_parent"], final.FROZEN_EVIDENCE)
        self.assertTrue(lifecycle["single_parent_each"] and lifecycle["zero_merges"] and lifecycle["strict_x1_before_x2"])

    def test_20_complete_incomplete_wellbeing_and_threat_model_are_explicit(self) -> None:
        checklist = self.read_json("closeout/complete-incomplete-checklist.json")
        wellbeing = self.read_json("closeout/wellbeing-workload-check.json")
        threat = self.read_json("closeout/threat-model-final.json")
        self.assertGreaterEqual(len(checklist["completed"]), 10)
        self.assertTrue(checklist["represented"] and checklist["open_gap"] and checklist["exact_gate"])
        self.assertFalse(wellbeing["health_measurement_claim"])
        self.assertIn("route_ambiguity", wellbeing["stop_conditions"])
        self.assertIn("failure laundering", threat["threats"])

    def test_21_source_provenance_is_vocabulary_only(self) -> None:
        source = self.read_json("closeout/source-provenance-ledger.json")
        evidence = self.read_json("x2/source-evidence-ledger.json")
        self.assertEqual(source["network_downloads_during_execution_or_closeout"], 0)
        self.assertFalse(source["citations_are_observations"])
        self.assertFalse(source["authority_conferred"])
        self.assertTrue(all(row["observations"] == 0 for row in evidence["rows"]))

    def test_22_route_and_baton_are_prepared_not_sent(self) -> None:
        route = self.read_json("closeout/route-state-final-candidate.json")
        baton = (self.root / "handoffs/sylven-arc-v671-v2-activation-candidate.md").read_text(encoding="utf-8")
        self.assertEqual(route["delivery_state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["exact_target_title"], "Sylven Arc")
        self.assertEqual(route["next_phase"], "v671-v2")
        self.assertFalse(route["sent_by_elowen_cairn"])
        self.assertIn("SENT_BY_ELOWEN_CAIRN = false", baton)
        self.assertIn("TO_BE_BOUND_BY_ACKNOWLEDGED_LIVE_SEND_AFTER_CANONICAL_GATE", baton)

    def test_23_all_phase_json_parses_and_documents_obey_ceiling(self) -> None:
        json_paths = list(self.root.rglob("*.json"))
        self.assertGreaterEqual(len(json_paths), 140)
        for path in json_paths:
            json.loads(path.read_text(encoding="utf-8"))
        for path in self.root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}:
                self.assertLessEqual(len(re.findall(r"\S+", path.read_text(encoding="utf-8"))), final.DOCUMENT_WORD_CEILING)

    def test_24_final_python_and_boundary_surfaces_hold(self) -> None:
        for relative in final.FINAL_CODE_PATHS:
            ast.parse((ROOT / relative).read_text(encoding="utf-8"), filename=relative)
        overview = (self.root / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
        for phrase in ("no real likelihood", "participant-free proxy", "synthetic and nonproduction", "Māori concepts remain under Māori authority", final.TERMINAL_VERDICT):
            self.assertIn(phrase, overview)
        changed = self.git("diff", "--name-only", final.FROZEN_EVIDENCE, self.expected_final).splitlines()
        self.assertFalse(any(path.startswith("docs/elowen-cairn/v671-v1/x1/") or path.startswith("docs/elowen-cairn/v671-v1/x2/") or path in final.x2.BUILD_PATHS for path in changed))


if __name__ == "__main__":
    unittest.main()
