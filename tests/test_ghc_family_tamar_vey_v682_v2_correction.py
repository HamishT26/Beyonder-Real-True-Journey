"""Additive terminal-correction tests for Tamar Vey v682-v2."""

from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

from scripts.ghc_family_privacy_candidate_adjudication import scan_text_items


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "tamar-vey" / "v682-v2"
CORRECTION = BASE / "correction"
VALIDATION = BASE / "validation"
ORIGINAL_FINAL = "d00443492f9e1a950e752aa2c1b5a1bf0613db44"
SOURCE = "34536c2bb4c9fefb04cc0b571839e9ba54b3c497"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class TamarVeyV682V2CorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.intake = load(CORRECTION / "correction-intake.json")
        cls.truth = load(CORRECTION / "corrected-phase-truth.json")
        cls.flow = load(CORRECTION / "method-flow-correction.json")
        cls.privacy = load(VALIDATION / "correction-privacy-scan.json")
        cls.delta = load(VALIDATION / "correction-delta-manifest.json")
        cls.owner = load(VALIDATION / "correction-owner-manifest.json")
        cls.review = load(VALIDATION / "correction-staged-review.json")
        cls.seal = load(CORRECTION / "content-seal.json")

    def test_01_fresh_authority_is_additive_and_bounded(self) -> None:
        self.assertEqual(self.intake["original_final"], ORIGINAL_FINAL)
        self.assertTrue(self.intake["fresh_user_authority_for_additive_correction"])
        self.assertFalse(self.intake["old_canonical_replayed"])
        self.assertFalse(self.intake["sibling_lane_mutation"])

    def test_02_failed_canonical_and_zero_credit_composite_are_retained(self) -> None:
        prior = self.intake["prior_terminal_evidence"]
        self.assertEqual(prior["canonical_status"], "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL")
        self.assertEqual(prior["canonical_success_count"], 0)
        self.assertEqual(prior["canonical_replay_count"], 0)
        self.assertFalse(prior["composite_promoted_canonical_success"])
        self.assertEqual(
            self.flow["retained_failure_ids"],
            ["TV6822-POST-N001", "TV6822-COR-N002", "TV6822-COR-N003"],
        )

    def test_03_corrected_totals_ingest_the_external_overlay(self) -> None:
        self.assertEqual(
            self.truth["totals"],
            {
                "bounded_passing_witnesses": 47314,
                "effective_methods": 65914,
                "effective_negatives": 55810,
                "exact_gates": 485,
                "failed_witnesses": 27471,
                "open_gaps": 494,
            },
        )
        self.assertEqual(
            self.truth["outcomes"],
            {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        )

    def test_04_method_flow_preserves_failure_and_recovery(self) -> None:
        self.assertEqual(self.flow["phase_methods"], 773)
        self.assertEqual(self.flow["phase_failed_witnesses"], 321)
        self.assertEqual(self.flow["phase_passing_witnesses"], 711)
        self.assertFalse(self.flow["recovery_erases_failure"])
        self.assertEqual(self.flow["correction_method"]["recommendation_state"], "preferred")
        self.assertEqual(self.flow["correction_method"]["method_id"], "TV6822-COR-M003")
        self.assertEqual(
            {row["method_id"] for row in self.flow["correction_methods"]},
            {"TV6822-COR-M002", "TV6822-COR-M003", "TV6822-COR-M004", "TV6822-COR-M005"},
        )

    def test_05_boundary_and_scanner_candidates_are_not_payloads(self) -> None:
        boundary_text = (
            "This bounded packet contains no private "
            + "callable identifier and no session "
            + "stream content."
        )
        scanner_text = (
            "marker = re."
            + "compile(\n"
            + "    r'(?:thread"
            + "Id)'\n"
            + ")"
        )
        result = scan_text_items(
            [("boundary.md", boundary_text), ("scanner.py", scanner_text)]
        )
        self.assertEqual(result["confirmed_hit_count"], 0)
        self.assertEqual(result["boundary_metadata_count"], 2)
        self.assertEqual(result["scanner_definition_count"], 1)
        mixed = scan_text_items(
            [
                (
                    "mixed.md",
                    "This packet contains no session "
                    + "stream content.\nA later session "
                    + "stream value is present.",
                )
            ]
        )
        self.assertEqual(mixed["boundary_metadata_count"], 1)
        self.assertEqual(mixed["confirmed_hit_count"], 1)

    def test_06_payload_shaped_fixtures_remain_confirmed(self) -> None:
        fixtures = [
            ("id.json", "019" + "a" * 29),
            ("route.json", "thread" + "Id" + "=opaque"),
            ("connector.json", "app:" + "//connector_" + "opaque"),
            ("credential.json", "bearer " + "abcdefghijklmnop"),
            ("path.json", "C:" + "\\Users\\" + "private"),
            ("record.json", "raw " + "transcript payload"),
        ]
        result = scan_text_items(fixtures)
        self.assertEqual(result["confirmed_hit_count"], len(fixtures))

    def test_07_exact_owner_privacy_scan_has_zero_confirmed_hits(self) -> None:
        self.assertEqual(self.privacy["class_count"], 5)
        self.assertEqual(self.privacy["confirmed_hit_count"], 0)
        self.assertEqual(self.privacy["confirmed_hits"], [])
        self.assertEqual(
            self.privacy["candidate_count"],
            self.privacy["boundary_metadata_count"]
            + self.privacy["scanner_definition_count"],
        )

    def test_08_correction_manifests_replay_normalized_worktree_bytes(self) -> None:
        for manifest in (self.delta, self.owner):
            self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
            for entry in manifest["entries"]:
                data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n")
                self.assertEqual(len(data), entry["bytes"], entry["path"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])
        expected = {row["path"] for row in self.delta["entries"]} | set(
            self.delta["declared_self_exclusions"]
        )
        self.assertEqual(set(self.review["expected_paths"]), expected)

    def test_09_original_final_owner_manifest_remains_immutable(self) -> None:
        path = "docs/tamar-vey/v682-v2/validation/final-owner-manifest.json"
        manifest = json.loads(
            subprocess.run(
                ["git", "show", f"{ORIGINAL_FINAL}:{path}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout.decode("utf-8")
        )
        for entry in manifest["entries"]:
            data = subprocess.run(
                ["git", "show", f"{ORIGINAL_FINAL}:{entry['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_10_correction_content_seal_replays(self) -> None:
        self.assertEqual(self.seal["target_count"], len(self.seal["targets"]))
        for entry in self.seal["targets"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n")
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])

    def test_11_lifecycle_is_one_additive_direct_correction(self) -> None:
        lifecycle = load(CORRECTION / "lifecycle-replay.json")
        self.assertEqual(lifecycle["source"], SOURCE)
        self.assertEqual(lifecycle["original_final"], ORIGINAL_FINAL)
        self.assertEqual(lifecycle["commit_ceiling"], 4)
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.strip()
        if head != ORIGINAL_FINAL:
            parent = subprocess.run(
                ["git", "rev-parse", "HEAD^"], cwd=ROOT, check=True, capture_output=True, text=True
            ).stdout.strip()
            self.assertEqual(parent, ORIGINAL_FINAL)
            commits = subprocess.run(
                ["git", "rev-list", "--reverse", f"{SOURCE}..HEAD"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
            self.assertEqual(len(commits), 4)

    def test_12_delivery_is_still_prepared_until_new_canonical_success(self) -> None:
        delivery = load(CORRECTION / "delivery-state.json")
        self.assertEqual(delivery["candidate_repository_state"], "PREPARED_NOT_SENT")
        self.assertEqual(delivery["send_count"], 0)
        self.assertEqual(delivery["prospective_successor_exact_title"], "Elowen Cairn")
        self.assertEqual(delivery["prospective_successor_phase"], "v682-v3")
        self.assertTrue(delivery["new_exact_final_canonical_success_required"])


if __name__ == "__main__":
    unittest.main()
