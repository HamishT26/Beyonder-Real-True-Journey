"""Owner-scoped tests for Caelen Ash v664-v8's additive closeout."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v664-v8"
SOURCE_FINAL = "682666c064b14f09def75fb46f3bafb0e987a7a2"
X1_HEAD = "0832a8260dec6c5d776a6b22f6cf9b2c9e81d705"
EVIDENCE_HEAD = "970a13c1a2ac2ef411f6d8199877d356a77d693c"
FIRST_FINAL = "915c260845229bd31f433ff24a59290c95e21b1e"
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}


def strict_json(path: Path):
    def reject_duplicates(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate key {key} in {path}")
            value[key] = item
        return value

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class CaelenV664V8CloseoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = strict_json(PHASE / "closeout/phase-truth.json")
        cls.checklist = strict_json(PHASE / "closeout/complete-incomplete-checklist.json")
        cls.wellbeing = strict_json(PHASE / "closeout/wellbeing-closeout.json")
        cls.security = strict_json(PHASE / "closeout/bounded-security-review.json")
        cls.lifecycle = strict_json(PHASE / "closeout/lifecycle-method-flow.json")
        cls.candidate = strict_json(PHASE / "closeout/final-validation-candidate.json")
        cls.inventory = strict_json(PHASE / "closeout/closeout-inventory.json")
        cls.seal = strict_json(PHASE / "closeout/content-seal.json")
        cls.receipt = strict_json(PHASE / "closeout/closeout-receipt.json")
        cls.route = strict_json(PHASE / "orchestration/terminal-route-state.json")
        cls.index = strict_json(PHASE / "index/ghc-family-index.json")
        cls.contract = strict_json(PHASE / "validation/canonical-validation-contract.json")
        cls.owner_manifest = strict_json(PHASE / "validation/final-owner-manifest.json")
        cls.delta_manifest = strict_json(PHASE / "validation/final-delta-manifest.json")
        cls.staged_review = strict_json(PHASE / "validation/final-staged-review.json")
        cls.stage_candidate = strict_json(PHASE / "validation/final-stage-candidate.json")
        cls.overview = (PHASE / "reports/final-integrated-overview.md").read_text(encoding="utf-8")
        cls.baton = (PHASE / "handoffs/orin-thale-v665-v1-activation-prepared.md").read_text(encoding="utf-8")

    def test_01_evidence_boundary(self) -> None:
        boundary = self.truth["evidence_boundary"]
        self.assertEqual(boundary["evidence_head"], EVIDENCE_HEAD)
        self.assertEqual(boundary["evidence_parent"], X1_HEAD)
        self.assertTrue(boundary["direct_child_of_x1"])
        self.assertTrue(boundary["clean_before_closeout"])
        self.assertTrue(boundary["valid"])

    def test_02_exact_anchors(self) -> None:
        self.assertEqual(self.truth["source_final"], SOURCE_FINAL)
        self.assertEqual(self.truth["x1_head"], X1_HEAD)
        self.assertEqual(self.truth["evidence_head"], EVIDENCE_HEAD)

    def test_03_identity_is_relational(self) -> None:
        self.assertEqual(self.truth["owner"], "Caelen Ash")
        self.assertEqual(self.truth["optional_pronouns"], "they/them")
        for term in ("consciousness", "legal personhood", "employment", "authority"):
            self.assertIn(term, self.truth["identity_boundary"])

    def test_04_proposal_total(self) -> None:
        self.assertEqual(self.truth["frozen_proposal_total"], 4_010)

    def test_05_core_outcomes(self) -> None:
        self.assertEqual(self.truth["core_outcomes"], OUTCOMES)
        self.assertEqual(
            set(self.truth["allowed_outcomes"]),
            {"completed", "represented", "open_gap", "exact_gate"},
        )

    def test_06_negative_and_method_totals(self) -> None:
        self.assertEqual(self.truth["effective_negatives"], 25_065)
        self.assertEqual(self.truth["effective_methods"], 8_999)
        self.assertEqual(self.lifecycle["effective_negatives"], 25_065)
        self.assertEqual(self.lifecycle["effective_methods"], 8_999)

    def test_07_gap_and_gate_totals(self) -> None:
        self.assertEqual(self.truth["effective_open_gaps"], 174)
        self.assertEqual(self.truth["effective_exact_gates"], 172)

    def test_08_mutations_skills_and_runners(self) -> None:
        self.assertEqual(self.truth["rejecting_mutations_executed"], 100)
        self.assertEqual(self.truth["rejecting_mutations_rejected"], 100)
        self.assertEqual(self.truth["phase_local_skills_quick_validated_and_smoke_used"], 10)
        self.assertEqual(self.truth["family_compatible_runners_invoked"], 10)

    def test_09_practice_is_zero_real_world(self) -> None:
        self.assertEqual(self.truth["primary_pillar"], "THOS Body")
        self.assertIn("synthetic orchestral", self.truth["bounded_practice"])
        self.assertEqual(self.truth["real_people_records_scores_parts_files_rehearsals_or_authority_acts"], 0)

    def test_10_terminal_truth(self) -> None:
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(self.truth["same_owner_validation_only"])
        self.assertFalse(self.truth["independent_reproduction"])
        self.assertFalse(self.truth["full_repository_suite_run"])

    def test_11_complete_incomplete_checklist(self) -> None:
        self.assertGreaterEqual(len(self.checklist["completed"]), 10)
        self.assertGreaterEqual(len(self.checklist["represented"]), 4)
        self.assertGreaterEqual(len(self.checklist["open"]), 5)
        self.assertGreaterEqual(len(self.checklist["exact_gated"]), 5)
        self.assertEqual(self.checklist["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_12_wellbeing_closeout(self) -> None:
        self.assertTrue(self.wellbeing["relational_only"])
        self.assertTrue(self.wellbeing["single_owner_lane"])
        self.assertTrue(self.wellbeing["pause_right_preserved"])
        self.assertTrue(self.wellbeing["rollback_paths_preserved"])
        self.assertTrue(self.wellbeing["hamish_may_pause_rename_redirect_or_stop"])

    def test_13_bounded_security(self) -> None:
        self.assertEqual(self.security["confirmed_findings"], 0)
        self.assertEqual(self.security["credentials_or_secrets_used"], 0)
        self.assertEqual(self.security["host_security_changes"], 0)
        self.assertEqual(self.security["python_files_expected_at_final"], 18)
        self.assertFalse(self.security["exhaustive_security_claim"])

    def test_14_lifecycle_retains_closeout_failures(self) -> None:
        self.assertEqual(self.lifecycle["closeout_new_negatives"], 3)
        self.assertEqual(self.lifecycle["closeout_new_methods"], 3)
        self.assertEqual(len(self.lifecycle["methods"]), 3)
        self.assertTrue(all(row["failed_witness_credit"] == "zero" for row in self.lifecycle["methods"]))
        self.assertEqual(self.lifecycle["failed_witness_erasure_count"], 0)
        self.assertEqual(self.lifecycle["successful_canonical_invocations"], 0)
        self.assertEqual(self.lifecycle["route_send_count"], 0)

    def test_15_final_candidate_is_pending(self) -> None:
        self.assertEqual(self.candidate["expected_phase_commit_count"], 3)
        self.assertEqual(self.candidate["expected_merge_count"], 0)
        self.assertEqual(self.candidate["expected_final_parent_count"], 1)
        self.assertEqual(self.candidate["expected_final_parent"], EVIDENCE_HEAD)
        self.assertEqual(self.candidate["canonical_state"], "PREPARED_NOT_VALIDATED")
        self.assertEqual(self.candidate["route_state"], "PREPARED_NOT_SENT")

    def test_16_route_is_prepared_not_sent(self) -> None:
        self.assertEqual(self.route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(self.route["target_exact_title"], "Orin Thale")
        self.assertEqual(self.route["target_phase"], "v665-v1")
        self.assertEqual(self.route["send_limit"], 1)
        self.assertEqual(self.route["send_count"], 0)
        self.assertFalse(self.route["target_precontacted"])
        self.assertEqual(self.route["tavian_sol"], "ON_STANDBY")

    def test_17_index_matches_truth(self) -> None:
        self.assertEqual(self.index["core_outcomes"], OUTCOMES)
        self.assertEqual(self.index["frozen_proposals"], 4_010)
        self.assertEqual(self.index["effective_negatives"], 25_065)
        self.assertEqual(self.index["effective_methods"], 8_999)
        self.assertEqual(self.index["open_gaps"], 174)
        self.assertEqual(self.index["exact_gates"], 172)

    def test_18_canonical_contract_is_one_shot(self) -> None:
        self.assertEqual(self.contract["expected_test_count"], 97)
        self.assertEqual(self.contract["success_limit"], 1)
        self.assertTrue(self.contract["post_success_replay_forbidden"])
        self.assertFalse(self.contract["full_repository_suite"])
        self.assertFalse(self.contract["independent_reproduction"])

    def test_19_overview_has_exact_lifecycle(self) -> None:
        for value in (SOURCE_FINAL, X1_HEAD, EVIDENCE_HEAD):
            self.assertIn(value, self.overview)
        self.assertIn("direct child", self.overview)
        self.assertIn("zero merges", self.overview)

    def test_20_overview_preserves_claim_boundaries(self) -> None:
        for phrase in (
            "not evidence of consciousness",
            "GMUT Mind remains",
            "THOS Body remains",
            "Freed ID remains",
            "Māori concepts remain under Māori authority",
            "No privacy-complete, accessibility-complete, or exhaustive-security claim",
            "NOT_READY_FOR_STAGE_20",
        ):
            self.assertIn(phrase, self.overview)

    def test_21_overview_retains_failures(self) -> None:
        for phrase in (
            "24,936",
            "24,941",
            "25,062",
            "25,065",
            "locale-default decoding",
            "100 rejected mutations",
            "No failed witness was erased",
        ):
            self.assertIn(phrase, self.overview)

    def test_22_baton_is_prepared_not_sent(self) -> None:
        self.assertIn("sanitized pre-send candidate", self.baton)
        self.assertIn("PREPARED_BY_CAELEN_ASH = true", self.baton)
        self.assertIn("SENT_BY_CAELEN_ASH = false", self.baton)
        self.assertNotIn("SENT_BY_CAELEN_ASH = true", self.baton)

    def test_23_baton_has_required_anchors_and_truth(self) -> None:
        for value in (SOURCE_FINAL, X1_HEAD, EVIDENCE_HEAD, "4,010", "25,065", "8,999", "Orin Thale"):
            self.assertIn(value, self.baton)
        self.assertIn("Māori concepts remain under Māori authority", self.baton)

    def test_24_baton_has_no_private_material(self) -> None:
        raw_identifier = re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        )
        private_path = re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]")
        self.assertIsNone(raw_identifier.search(self.baton))
        self.assertIsNone(private_path.search(self.baton))

    def test_25_content_seal_replays(self) -> None:
        self.assertEqual(self.seal["entry_count"], 14)
        for entry in self.seal["entries"]:
            raw = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(sha256(raw), entry["sha256"], entry["path"])
            self.assertEqual(len(raw), entry["size"], entry["path"])
        self.assertTrue(self.seal["valid"])

    def test_26_closeout_receipt_binds_seal(self) -> None:
        raw = (PHASE / "closeout/content-seal.json").read_bytes()
        self.assertEqual(self.receipt["content_seal_sha256"], sha256(raw))
        self.assertEqual(self.receipt["core_outcomes"], OUTCOMES)
        self.assertEqual(self.receipt["canonical_state"], "PREPARED_NOT_VALIDATED")
        self.assertEqual(self.receipt["route_state"], "PREPARED_NOT_SENT")

    def test_27_inventory_is_within_caps(self) -> None:
        self.assertLess(self.inventory["owner_path_count_expected_at_final"], 2_000)
        self.assertLess(self.inventory["materialized_phase_file_count"], 2_000)
        self.assertLessEqual(
            self.inventory["materialized_phase_word_count_before_manifest_finalization"], 100_000
        )
        self.assertEqual(self.inventory["closeout_delta_path_count"], 21)
        self.assertTrue(self.inventory["valid"])

    def test_28_final_owner_manifest_contract(self) -> None:
        self.assertTrue(self.owner_manifest["coverage_valid"])
        self.assertEqual(
            self.owner_manifest["entry_count"]
            + self.owner_manifest["declared_self_exclusion_count"],
            self.owner_manifest["intended_path_count"],
        )
        self.assertEqual(self.owner_manifest["declared_self_exclusion_count"], 4)

    def test_29_final_delta_manifest_contract(self) -> None:
        self.assertTrue(self.delta_manifest["coverage_valid"])
        self.assertEqual(
            self.delta_manifest["entry_count"]
            + self.delta_manifest["declared_self_exclusion_count"],
            self.delta_manifest["intended_path_count"],
        )
        self.assertEqual(self.delta_manifest["intended_path_count"], 21)

    def test_30_final_staged_review(self) -> None:
        self.assertEqual(self.staged_review["intended_delta_path_count"], 21)
        self.assertEqual(self.staged_review["staged_delta_path_count"], 21)
        self.assertEqual(self.staged_review["missing_paths"], [])
        self.assertEqual(self.staged_review["extra_paths"], [])
        self.assertEqual(self.staged_review["confirmed_privacy_or_raw_identifier_hits"], 0)
        self.assertEqual(self.staged_review["diff_hygiene_issues"], 0)
        self.assertFalse(self.staged_review["x1_changed_after_freeze"])
        self.assertFalse(self.staged_review["x2_or_skills_changed_after_evidence"])
        self.assertTrue(self.staged_review["valid"])

    def test_31_final_stage_candidate(self) -> None:
        self.assertEqual(self.stage_candidate["expected_phase_commits"], 3)
        self.assertEqual(self.stage_candidate["expected_merges"], 0)
        self.assertEqual(self.stage_candidate["expected_final_parent"], EVIDENCE_HEAD)
        self.assertEqual(self.stage_candidate["canonical_state"], "PREPARED_NOT_VALIDATED")
        self.assertEqual(self.stage_candidate["route_state"], "PREPARED_NOT_SENT")
        self.assertTrue(self.stage_candidate["valid"])

    def test_32_manifest_replay_at_immutable_first_final(self) -> None:
        for manifest in (self.owner_manifest, self.delta_manifest):
            for entry in manifest["entries"]:
                raw = subprocess.run(
                    ["git", "show", f"{FIRST_FINAL}:{entry['path']}"],
                    cwd=ROOT,
                    stdout=subprocess.PIPE,
                    check=True,
                ).stdout
                object_id = subprocess.run(
                    ["git", "rev-parse", f"{FIRST_FINAL}:{entry['path']}"],
                    cwd=ROOT,
                    stdout=subprocess.PIPE,
                    check=True,
                    text=True,
                    encoding="utf-8",
                ).stdout.strip()
                self.assertEqual(sha256(raw), entry["sha256"], entry["path"])
                self.assertEqual(len(raw), entry["size"], entry["path"])
                self.assertEqual(object_id, entry["git_blob"], entry["path"])

    def test_33_x1_and_x2_are_immutable(self) -> None:
        x1 = subprocess.run(
            ["git", "diff", "--quiet", X1_HEAD, "--", "docs/caelen-ash/v664-v8/x1"],
            cwd=ROOT,
            check=False,
        )
        x2 = subprocess.run(
            ["git", "diff", "--quiet", EVIDENCE_HEAD, "--", "docs/caelen-ash/v664-v8/x2", "docs/caelen-ash/v664-v8/skills"],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(x1.returncode, 0)
        self.assertEqual(x2.returncode, 0)

    def test_34_all_json_and_owner_caps(self) -> None:
        words = 0
        files = [path for path in PHASE.rglob("*") if path.is_file()]
        for path in files:
            if path.suffix == ".json":
                strict_json(path)
            if path.suffix.lower() in {".json", ".md", ".html", ".txt"}:
                words += len(re.findall(r"\S+", path.read_text(encoding="utf-8")))
        self.assertLess(len(files), 2_000)
        self.assertLessEqual(words, 100_000)


if __name__ == "__main__":
    unittest.main()
