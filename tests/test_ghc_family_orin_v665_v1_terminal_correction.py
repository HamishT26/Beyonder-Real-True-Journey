"""Tests for Orin Thale v665-v1's additive terminal correction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest

from scripts.ghc_family_v665_v1_canonical_validator import (
    FIRST_FINAL,
    changed_paths,
    markdown_structure_issues,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v665-v1"
EVIDENCE_HEAD = "1104a4f2963c8782ddad8939e8b4aff50715cc42"
FAILED_SHA = "f0dc66c805f3b939ec12addbdebd828d891c2c59926b4f4249bb48ab0373d1e3"


def strict_json(path: Path):
    def reject_duplicates(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate key {key} in {path}")
            value[key] = item
        return value

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


class OrinV665V1TerminalCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.failure = strict_json(PHASE / "correction/canonical-failure-receipt.json")
        cls.methods = strict_json(PHASE / "correction/method-flow-overlay.json")
        cls.truth = strict_json(PHASE / "correction/phase-truth.json")
        cls.receipt = strict_json(PHASE / "correction/correction-receipt.json")
        cls.seal = strict_json(PHASE / "correction/content-seal.json")
        cls.inventory = strict_json(PHASE / "correction/correction-inventory.json")
        cls.route = strict_json(PHASE / "orchestration/terminal-route-state-correction.json")
        cls.contract = strict_json(PHASE / "validation/correction-canonical-contract.json")
        cls.owner = strict_json(PHASE / "validation/correction-owner-manifest.json")
        cls.delta = strict_json(PHASE / "validation/correction-delta-manifest.json")
        cls.review = strict_json(PHASE / "validation/correction-staged-review.json")
        cls.candidate = strict_json(PHASE / "validation/correction-stage-candidate.json")

    def test_01_retained_first_final_boundary(self) -> None:
        boundary = self.receipt["boundary"]
        self.assertEqual(boundary["retained_first_final"], FIRST_FINAL)
        self.assertEqual(boundary["first_final_parent"], EVIDENCE_HEAD)
        self.assertEqual(boundary["phase_commit_count"], 3)
        self.assertEqual(boundary["merge_count"], 0)
        self.assertEqual(boundary["ahead"], 0)
        self.assertEqual(boundary["behind"], 0)
        self.assertTrue(boundary["valid"])

    def test_02_failed_canonical_is_retained_zero_credit(self) -> None:
        self.assertEqual(self.failure["external_receipt_sha256"], FAILED_SHA)
        self.assertEqual(self.failure["status"], "failed")
        self.assertEqual(self.failure["credit"], "zero")
        self.assertEqual(self.failure["failed_detailed_checks"], ["markdown_structure"])
        self.assertFalse(self.failure["replayed"])

    def test_03_failure_passed_other_bounded_components(self) -> None:
        self.assertEqual(self.failure["tests_passed"], 90)
        self.assertEqual(self.failure["tests_failed"], 0)
        self.assertEqual(self.failure["minimal_passed"], 15)
        self.assertTrue(self.failure["owner_manifest_valid"])
        self.assertTrue(self.failure["delta_manifest_valid"])
        self.assertEqual(self.failure["privacy_confirmed_hits"], 0)

    def test_04_markdown_dispatch_is_corrected(self) -> None:
        paths = [
            path
            for path in changed_paths()
            if path.startswith("docs/orin-thale/v665-v1/") and path.endswith(".md")
        ]
        self.assertEqual(markdown_structure_issues(paths), [])
        self.assertGreaterEqual(sum(path.endswith("/SKILL.md") for path in paths), 10)

    def test_05_method_flow_adds_one_and_erases_none(self) -> None:
        self.assertEqual(self.methods["correction_negative_count"], 3)
        self.assertEqual(self.methods["correction_method_count"], 3)
        self.assertEqual(self.methods["effective_negatives"], 25_187)
        self.assertEqual(self.methods["effective_methods"], 9_049)
        self.assertEqual(self.methods["failure_erasure_count"], 0)
        self.assertEqual(len(self.methods["methods"]), 3)
        self.assertTrue(all(row["state"] == "preferred" for row in self.methods["methods"]))

    def test_06_corrected_truth_preserves_outcomes_and_gates(self) -> None:
        self.assertEqual(
            self.truth["outcomes"],
            {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4},
        )
        self.assertEqual(self.truth["effective_negatives"], 25_187)
        self.assertEqual(self.truth["effective_methods"], 9_049)
        self.assertEqual(self.truth["open_gaps"], 175)
        self.assertEqual(self.truth["exact_gates"], 173)
        self.assertEqual(self.truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_07_correction_seal_replays(self) -> None:
        self.assertEqual(len(self.seal["entries"]), 6)
        for entry in self.seal["entries"]:
            raw = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])
            self.assertEqual(len(raw), entry["size"])

    def test_08_correction_manifest_coverage(self) -> None:
        self.assertTrue(self.owner["coverage_valid"])
        self.assertEqual(
            self.owner["entry_count"] + self.owner["declared_self_exclusion_count"],
            self.owner["path_count"],
        )
        self.assertTrue(self.delta["coverage_valid"])
        self.assertEqual(
            self.delta["entry_count"] + self.delta["declared_self_exclusion_count"],
            self.delta["path_count"],
        )
        self.assertEqual(self.delta["parent"], FIRST_FINAL)

    def test_09_staged_review_and_candidate(self) -> None:
        self.assertEqual(self.review["missing_paths"], [])
        self.assertEqual(self.review["extra_paths"], [])
        self.assertEqual(self.review["confirmed_privacy_or_raw_identifier_hits"], 0)
        self.assertEqual(self.review["x1_or_x2_paths_modified"], [])
        self.assertEqual(self.candidate["canonical_state"], "PREPARED_CORRECTED_NOT_RUN")
        self.assertEqual(self.candidate["route_state"], "PREPARED_NOT_SENT")

    def test_10_corrected_canonical_contract_is_one_shot(self) -> None:
        self.assertEqual(self.contract["retained_failed_receipt_sha256"], FAILED_SHA)
        self.assertEqual(self.contract["corrected_run_count_ceiling"], 1)
        self.assertFalse(self.contract["replay_after_success"])
        self.assertEqual(self.contract["expected_test_count"], 102)
        self.assertFalse(self.contract["full_repository_suite"])

    def test_11_route_remains_unsent_and_uninferred(self) -> None:
        self.assertEqual(self.route["state"], "PREPARED_NOT_SENT")
        self.assertFalse(self.route["successor_inferred"])
        self.assertIsNone(self.route["successor_title"])
        self.assertFalse(self.route["precontact_performed"])
        self.assertEqual(self.route["send_count"], 0)

    def test_12_inventory_json_privacy_and_caps(self) -> None:
        self.assertEqual(self.inventory["path_count"], 16)
        for path in PHASE.rglob("*.json"):
            strict_json(path)
        raw_identifier = re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        )
        private_path = re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]")
        files = [path for path in PHASE.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2_000)
        for path in files:
            if path.suffix.lower() in {".json", ".md", ".html", ".txt"}:
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(raw_identifier.search(text), str(path))
                self.assertIsNone(private_path.search(text), str(path))
                self.assertLessEqual(len(re.findall(r"\S+", text)), 100_000)


if __name__ == "__main__":
    unittest.main()
