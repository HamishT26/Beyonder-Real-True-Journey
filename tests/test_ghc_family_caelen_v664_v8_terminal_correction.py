"""Tests for Caelen Ash v664-v8's additive terminal correction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v664-v8"
SOURCE_FINAL = "682666c064b14f09def75fb46f3bafb0e987a7a2"
X1_HEAD = "0832a8260dec6c5d776a6b22f6cf9b2c9e81d705"
EVIDENCE_HEAD = "970a13c1a2ac2ef411f6d8199877d356a77d693c"
FIRST_FINAL = "915c260845229bd31f433ff24a59290c95e21b1e"
FAILED_SHA256 = "c7901af9706a91ad8540029dac02bc05840a21ac5bde4e05d6f42eea0b9a8664"
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


class CaelenV664V8TerminalCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.failure = strict_json(PHASE / "correction/canonical-failure-receipt.json")
        cls.methods = strict_json(PHASE / "correction/method-flow-overlay.json")
        cls.truth = strict_json(PHASE / "correction/phase-truth.json")
        cls.inventory = strict_json(PHASE / "correction/correction-inventory.json")
        cls.seal = strict_json(PHASE / "correction/content-seal.json")
        cls.receipt = strict_json(PHASE / "correction/correction-receipt.json")
        cls.route = strict_json(PHASE / "orchestration/terminal-route-state-correction.json")
        cls.contract = strict_json(PHASE / "validation/correction-canonical-contract.json")
        cls.owner = strict_json(PHASE / "validation/correction-owner-manifest.json")
        cls.delta = strict_json(PHASE / "validation/correction-delta-manifest.json")
        cls.review = strict_json(PHASE / "validation/correction-staged-review.json")
        cls.candidate = strict_json(PHASE / "validation/correction-stage-candidate.json")
        cls.overview = (PHASE / "reports/terminal-correction-overview.md").read_text(encoding="utf-8")
        cls.baton = (PHASE / "handoffs/orin-thale-v665-v1-activation-corrected-prepared.md").read_text(encoding="utf-8")

    def test_01_first_final_boundary(self) -> None:
        self.assertEqual(self.truth["source_final"], SOURCE_FINAL)
        self.assertEqual(self.truth["x1_head"], X1_HEAD)
        self.assertEqual(self.truth["evidence_head"], EVIDENCE_HEAD)
        self.assertEqual(self.truth["first_final"], FIRST_FINAL)

    def test_02_failed_receipt_is_retained(self) -> None:
        self.assertEqual(self.failure["external_receipt_sha256"], FAILED_SHA256)
        self.assertFalse(self.failure["success"])
        self.assertEqual(self.failure["credit"], "zero")
        self.assertFalse(self.failure["failure_erased"])

    def test_03_failed_receipt_exact_diagnostics(self) -> None:
        self.assertEqual(self.failure["test_loader_error_count"], 3)
        self.assertEqual(self.failure["test_loader_synthetic_test_count"], 3)
        self.assertEqual(self.failure["intended_test_count"], 97)
        self.assertEqual(self.failure["passed_gates"]["owner_path_count"], 155)
        self.assertEqual(self.failure["passed_gates"]["strict_json_count"], 123)
        self.assertEqual(self.failure["passed_gates"]["privacy_confirmed_hits"], 0)
        self.assertEqual(self.failure["passed_gates"]["bounded_security_findings"], 0)

    def test_04_method_flow_retains_all_correction_failures(self) -> None:
        self.assertEqual(self.methods["first_final_effective_negatives"], 25_065)
        self.assertEqual(self.methods["first_final_effective_methods"], 8_999)
        self.assertEqual(self.methods["new_failed_witness_count"], 6)
        self.assertEqual(self.methods["new_method_count"], 4)
        self.assertEqual(self.methods["effective_negatives"], 25_071)
        self.assertEqual(self.methods["effective_methods"], 9_003)
        self.assertEqual(self.methods["failure_erasure_count"], 0)

    def test_05_corrected_truth_arithmetic(self) -> None:
        self.assertEqual(self.truth["core_outcomes"], OUTCOMES)
        self.assertEqual(self.truth["frozen_proposal_total"], 4_010)
        self.assertEqual(self.truth["effective_negatives"], 25_071)
        self.assertEqual(self.truth["effective_methods"], 9_003)
        self.assertEqual(self.truth["first_corrected_precommit_rehearsal_tests"], 117)
        self.assertEqual(self.truth["first_corrected_precommit_rehearsal_passes"], 116)
        self.assertEqual(self.truth["first_corrected_precommit_rehearsal_failures"], 1)
        self.assertEqual(self.truth["effective_open_gaps"], 174)
        self.assertEqual(self.truth["effective_exact_gates"], 172)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_06_first_manifest_replays_passed(self) -> None:
        self.assertEqual(len(self.truth["first_final_manifest_replays"]), 2)
        self.assertTrue(all(row["valid"] for row in self.truth["first_final_manifest_replays"]))
        self.assertEqual(sum(row["mismatch_count"] for row in self.truth["first_final_manifest_replays"]), 0)

    def test_07_corrected_history_contract(self) -> None:
        self.assertEqual(self.truth["phase_commit_count_expected"], 4)
        self.assertEqual(self.truth["merge_count_expected"], 0)
        self.assertEqual(self.truth["corrected_final_parent_expected"], FIRST_FINAL)

    def test_08_corrected_route_is_not_sent(self) -> None:
        self.assertEqual(self.route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(self.route["target_exact_title"], "Orin Thale")
        self.assertEqual(self.route["target_phase"], "v665-v1")
        self.assertFalse(self.route["first_canonical_success"])
        self.assertEqual(self.route["send_count"], 0)
        self.assertFalse(self.route["target_precontacted"])
        self.assertEqual(self.route["tavian_sol"], "ON_STANDBY")

    def test_09_corrected_canonical_contract(self) -> None:
        self.assertEqual(self.contract["failed_first_receipt_sha256"], FAILED_SHA256)
        self.assertTrue(self.contract["failed_first_final_replay_forbidden"])
        self.assertEqual(self.contract["corrected_expected_test_modules"], 4)
        self.assertEqual(self.contract["corrected_expected_test_count"], 117)
        self.assertEqual(self.contract["corrected_expected_phase_commits"], 4)
        self.assertEqual(self.contract["corrected_expected_final_parent"], FIRST_FINAL)
        self.assertTrue(self.contract["post_success_replay_forbidden"])

    def test_10_correction_overview_is_exact(self) -> None:
        for value in (FIRST_FINAL, EVIDENCE_HEAD, FAILED_SHA256, "25,071", "9,003", "117 tests"):
            self.assertIn(value, self.overview)
        self.assertIn("three error witnesses", self.overview)
        self.assertIn("failed receipt is never relabelled as a pass", self.overview)

    def test_11_overview_preserves_boundaries(self) -> None:
        for phrase in (
            "GMUT remains",
            "THOS remains",
            "Freed ID remains",
            "Māori concepts remain under Māori authority",
            "NOT_READY_FOR_STAGE_20",
            "PREPARED_NOT_SENT",
        ):
            self.assertIn(phrase, self.overview)

    def test_12_corrected_baton_is_prepared_only(self) -> None:
        for value in (SOURCE_FINAL, X1_HEAD, EVIDENCE_HEAD, FIRST_FINAL, FAILED_SHA256, "25,071", "9,003", "Orin Thale"):
            self.assertIn(value, self.baton)
        self.assertIn("PREPARED_BY_CAELEN_ASH = true", self.baton)
        self.assertIn("SENT_BY_CAELEN_ASH = false", self.baton)
        self.assertNotIn("SENT_BY_CAELEN_ASH = true", self.baton)

    def test_13_no_private_route_or_absolute_path(self) -> None:
        raw_identifier = re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        )
        private_path = re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]")
        for text in (self.overview, self.baton):
            self.assertIsNone(raw_identifier.search(text))
            self.assertIsNone(private_path.search(text))

    def test_14_correction_content_seal(self) -> None:
        self.assertEqual(self.seal["entry_count"], 8)
        for entry in self.seal["entries"]:
            raw = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(sha256(raw), entry["sha256"], entry["path"])
            self.assertEqual(len(raw), entry["size"], entry["path"])

    def test_15_correction_receipt(self) -> None:
        self.assertEqual(self.receipt["first_final"], FIRST_FINAL)
        self.assertEqual(self.receipt["failed_first_receipt_sha256"], FAILED_SHA256)
        self.assertEqual(self.receipt["effective_negatives"], 25_071)
        self.assertEqual(self.receipt["effective_methods"], 9_003)
        self.assertEqual(self.receipt["canonical_state"], "PREPARED_NOT_VALIDATED")
        self.assertEqual(self.receipt["route_state"], "PREPARED_NOT_SENT")

    def test_16_inventory_within_caps(self) -> None:
        self.assertLess(self.inventory["owner_path_count_expected_at_corrected_final"], 2_000)
        self.assertLess(self.inventory["materialized_phase_file_count"], 2_000)
        self.assertLessEqual(
            self.inventory["materialized_phase_word_count_before_manifest_finalization"], 100_000
        )
        self.assertEqual(self.inventory["correction_delta_path_count"], 19)

    def test_17_correction_manifest_contracts(self) -> None:
        for manifest in (self.owner, self.delta):
            self.assertTrue(manifest["coverage_valid"])
            self.assertEqual(
                manifest["entry_count"] + manifest["declared_self_exclusion_count"],
                manifest["intended_path_count"],
            )
            self.assertEqual(manifest["declared_self_exclusion_count"], 4)
        self.assertEqual(self.delta["intended_path_count"], 19)

    def test_18_correction_staged_review(self) -> None:
        self.assertEqual(self.review["intended_delta_path_count"], 19)
        self.assertEqual(self.review["staged_delta_path_count"], 19)
        self.assertEqual(self.review["missing_paths"], [])
        self.assertEqual(self.review["extra_paths"], [])
        self.assertEqual(self.review["confirmed_privacy_or_raw_identifier_hits"], 0)
        self.assertFalse(self.review["x1_changed"])
        self.assertFalse(self.review["x2_or_skills_changed"])
        self.assertFalse(self.review["first_closeout_or_manifest_changed"])
        self.assertTrue(self.review["valid"])

    def test_19_validator_has_process_local_root_binding(self) -> None:
        text = (ROOT / "scripts/ghc_family_v664_v8_canonical_validator.py").read_text(encoding="utf-8")
        self.assertIn("sys.path.insert(0, str(ROOT))", text)
        self.assertIn("count == 117", text)
        self.assertIn("FIRST_FINAL", text)
        self.assertIn("correction-owner-manifest.json", text)

    def test_20_manifest_replay_and_caps_in_current_domain(self) -> None:
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            check=True,
            text=True,
            encoding="utf-8",
        ).stdout.splitlines()
        if staged:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/build_ghc_family_v664_v8_terminal_correction.py"), "--check-staged"],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["valid"])
        else:
            head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                check=True,
                text=True,
                encoding="utf-8",
            ).stdout.strip()
            for manifest in (self.owner, self.delta):
                for entry in manifest["entries"]:
                    raw = subprocess.run(
                        ["git", "show", f"{head}:{entry['path']}"],
                        cwd=ROOT,
                        stdout=subprocess.PIPE,
                        check=True,
                    ).stdout
                    object_id = subprocess.run(
                        ["git", "rev-parse", f"{head}:{entry['path']}"],
                        cwd=ROOT,
                        stdout=subprocess.PIPE,
                        check=True,
                        text=True,
                        encoding="utf-8",
                    ).stdout.strip()
                    self.assertEqual(sha256(raw), entry["sha256"], entry["path"])
                    self.assertEqual(len(raw), entry["size"], entry["path"])
                    self.assertEqual(object_id, entry["git_blob"], entry["path"])
        files = [path for path in PHASE.rglob("*") if path.is_file()]
        words = sum(
            len(re.findall(r"\S+", path.read_text(encoding="utf-8")))
            for path in files
            if path.suffix.lower() in {".json", ".md", ".html", ".txt"}
        )
        self.assertLess(len(files), 2_000)
        self.assertLessEqual(words, 100_000)


if __name__ == "__main__":
    unittest.main()
