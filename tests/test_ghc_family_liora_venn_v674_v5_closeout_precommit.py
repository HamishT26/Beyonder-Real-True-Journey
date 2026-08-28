from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "liora-venn" / "v674-v5"
SOURCE = "8979c6884c75232046a85fd18ae2d15af33f4a0e"
X1 = "8f1db387ab28e3b53e3aaadef33a044f2e023386"
FIRST_EVIDENCE = "06af8881c44826cd3161d80f0a4359912ff1ce68"
EVIDENCE = "475415e9ec5e12f7759fc95a081bf12a8d917201"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8"
    ).strip()


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)


def commit_blob(ref: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=REPO)


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class LioraV674V5CloseoutPrecommitTests(unittest.TestCase):
    def test_head_is_corrected_evidence_before_final_commit(self):
        self.assertEqual(git("rev-parse", "HEAD"), EVIDENCE)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), FIRST_EVIDENCE)
        self.assertEqual(git("rev-parse", f"{FIRST_EVIDENCE}^"), X1)
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)

    def test_phase_truth_and_terminal_verdict(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(
            truth["outcomes"],
            {
                "completed": 42,
                "exact_gate": 3,
                "open_gap": 3,
                "represented": 12,
            },
        )
        self.assertEqual(truth["proposal_chain_rows"], 6850)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertFalse(truth["successor_contacted"])

    def test_counts_include_retained_closeout_failure(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["effective_negatives"], 39125)
        self.assertEqual(truth["effective_methods"], 27278)
        self.assertEqual(truth["effective_failed_witnesses"], 10786)
        self.assertEqual(
            truth["effective_bounded_passing_witnesses"], 14561
        )
        self.assertEqual(truth["effective_open_gaps"], 322)
        self.assertEqual(truth["effective_exact_gates"], 315)

    def test_closeout_failure_is_retained(self):
        ledger = load("closeout/operational-failure-ledger.json")
        self.assertEqual(ledger["failure_count"], 2)
        self.assertEqual(
            [row["failure_id"] for row in ledger["failures"]],
            ["LV6745-CL-N001", "LV6745-CL-N002"],
        )
        self.assertTrue(
            all(row["initial_pass_credit"] == 0 for row in ledger["failures"])
        )
        self.assertTrue(
            all(
                not row["repository_changed_by_failure"]
                for row in ledger["failures"]
            )
        )
        self.assertTrue(
            all(row["failed_witness_retained"] for row in ledger["failures"])
        )

    def test_original_manifest_failure_and_correction_are_distinct(self):
        diagnostic = load(
            "x2/correction/original-manifest-diagnostic.json"
        )
        self.assertEqual(diagnostic["mismatch_count"], 20)
        self.assertFalse(diagnostic["original_manifest_passed"])
        self.assertTrue(diagnostic["original_failure_retained"])
        manifest = load(
            "x2/validation/evidence-correction-owner-manifest.json"
        )
        self.assertEqual(len(manifest["entries"]), 232)
        for entry in manifest["entries"]:
            raw = commit_blob(EVIDENCE, entry["path"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(),
                entry["sha256"],
                entry["path"],
            )
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_content_seal_matches_staged_index_blobs(self):
        seal = load("closeout/content-seal.json")
        self.assertEqual(seal["target_count"], 15)
        self.assertEqual(
            seal["domain"],
            "staged_index_normalized_git_blobs_before_exact_final_commit",
        )
        for entry in seal["targets"]:
            raw = index_blob(entry["path"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(),
                entry["sha256"],
                entry["path"],
            )
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_final_owner_and_delta_manifests_match_index(self):
        for relative in (
            "validation/final-owner-manifest.json",
            "validation/final-delta-manifest.json",
        ):
            manifest = load(relative)
            self.assertEqual(
                manifest["domain"],
                "staged_index_normalized_git_blobs_before_exact_final_commit",
            )
            for entry in manifest["entries"]:
                raw = index_blob(entry["path"])
                self.assertEqual(
                    hashlib.sha256(raw).hexdigest(),
                    entry["sha256"],
                    entry["path"],
                )
                self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_exact_staged_review_matches_index(self):
        review = load("validation/final-staged-review.json")
        self.assertEqual(review["status"], "passed")
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["unresolved_privacy_candidates"], [])
        self.assertEqual(review["confirmed_privacy_hits"], [])
        for entry in review["entries"]:
            raw = index_blob(entry["path"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(),
                entry["sha256"],
                entry["path"],
            )
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_handoff_is_prepared_not_sent(self):
        text = (
            ROOT
            / "handoffs"
            / "tamar-vey-v674-v6-activation-candidate.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PREPARED_BY_LIORA_VENN = true", text)
        self.assertIn("SENT_BY_LIORA_VENN = false", text)
        self.assertIn("v725-v8", text)
        self.assertIn("Elowen Cairn", text)
        self.assertIn("EXTERNAL_POSTCOMMIT_BINDING_REQUIRED", text)

    def test_checklist_retains_incomplete_items(self):
        value = load("closeout/complete-incomplete-checklist.json")
        self.assertGreater(len(value["completed_items"]), 12)
        self.assertGreater(len(value["incomplete_or_gated_items"]), 9)
        self.assertTrue(value["no_incomplete_item_silently_closed"])

    def test_all_phase_json_parses_and_caps_hold(self):
        files = [path for path in ROOT.rglob("*") if path.is_file()]
        self.assertLess(len(files), 2000)
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertLessEqual(len(text.split()), 100000, path)
            if path.suffix == ".json":
                json.loads(text)

    def test_closeout_receipt_has_zero_canonical_credit_before_final(self):
        receipt = load("closeout/closeout-receipt.json")
        self.assertEqual(receipt["canonical_invocations"], 0)
        self.assertEqual(receipt["canonical_successes"], 0)
        self.assertFalse(receipt["successor_contacted"])
        selection = load("validation/final-test-selection.json")
        self.assertFalse(selection["complete_repository_suite"])
        self.assertTrue(selection["one_successful_canonical_no_replay"])


if __name__ == "__main__":
    unittest.main()
