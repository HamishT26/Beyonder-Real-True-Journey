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
BRANCH = "codex/GHC-Family/liora-venn-v674-v5-full-tools"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8"
    ).strip()


def git_blob(path: str, ref: str = "HEAD") -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path}"], cwd=REPO
    )


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class LioraV674V5FinalTests(unittest.TestCase):
    def test_exact_branch_and_direct_parent(self):
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE)

    def test_four_direct_commits_and_zero_merges(self):
        self.assertEqual(git("rev-list", "--count", f"{SOURCE}..HEAD"), "4")
        self.assertEqual(
            git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD"),
            "0",
        )
        self.assertEqual(git("rev-parse", f"{X1}^"), SOURCE)
        self.assertEqual(git("rev-parse", f"{FIRST_EVIDENCE}^"), X1)
        self.assertEqual(git("rev-parse", f"{EVIDENCE}^"), FIRST_EVIDENCE)

    def test_final_has_one_parent(self):
        parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()
        self.assertEqual(len(parents), 2)

    def test_phase_truth_partition_and_verdict(self):
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
        self.assertFalse(truth["independent_reproduction"])
        self.assertFalse(truth["complete_repository_suite_run"])

    def test_final_counts_are_exact(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(
            (truth["effective_negatives"], truth["effective_methods"]),
            (39125, 27278),
        )
        self.assertEqual(
            (
                truth["effective_failed_witnesses"],
                truth["effective_bounded_passing_witnesses"],
            ),
            (10786, 14561),
        )
        self.assertEqual(
            (
                truth["effective_open_gaps"],
                truth["effective_exact_gates"],
            ),
            (322, 315),
        )

    def test_closeout_failure_remains_retained(self):
        ledger = load("closeout/operational-failure-ledger.json")
        self.assertEqual(ledger["failure_count"], 2)
        self.assertEqual(
            ledger["failures"][0]["failure_id"], "LV6745-CL-N001"
        )
        self.assertEqual(
            ledger["failures"][0]["initial_pass_credit"], 0
        )
        self.assertTrue(
            ledger["failures"][0]["failed_witness_retained"]
        )

    def test_content_seal_matches_exact_final_blobs(self):
        seal = load("closeout/content-seal.json")
        self.assertEqual(seal["target_count"], 15)
        for entry in seal["targets"]:
            raw = git_blob(entry["path"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(),
                entry["sha256"],
                entry["path"],
            )
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_final_owner_manifest_matches_exact_final_blobs(self):
        manifest = load("validation/final-owner-manifest.json")
        for entry in manifest["entries"]:
            raw = git_blob(entry["path"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(),
                entry["sha256"],
                entry["path"],
            )
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_final_delta_manifest_matches_exact_final_blobs(self):
        manifest = load("validation/final-delta-manifest.json")
        for entry in manifest["entries"]:
            raw = git_blob(entry["path"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(),
                entry["sha256"],
                entry["path"],
            )
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_final_staged_review_matches_exact_final_blobs(self):
        review = load("validation/final-staged-review.json")
        self.assertEqual(review["status"], "passed")
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["unresolved_privacy_candidates"], [])
        self.assertEqual(review["confirmed_privacy_hits"], [])
        for entry in review["entries"]:
            raw = git_blob(entry["path"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(),
                entry["sha256"],
                entry["path"],
            )
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_original_manifest_failure_and_correction_are_both_visible(self):
        diagnostic = load(
            "x2/correction/original-manifest-diagnostic.json"
        )
        self.assertEqual(diagnostic["mismatch_count"], 20)
        self.assertFalse(diagnostic["original_manifest_passed"])
        manifest = load(
            "x2/validation/evidence-correction-owner-manifest.json"
        )
        for entry in manifest["entries"]:
            raw = git_blob(entry["path"], EVIDENCE)
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(),
                entry["sha256"],
                entry["path"],
            )

    def test_all_phase_json_parses(self):
        paths = git(
            "ls-tree", "-r", "--name-only", "HEAD", "--",
            "docs/liora-venn/v674-v5",
        ).splitlines()
        parsed = 0
        for path in paths:
            if path.endswith(".json"):
                json.loads(git_blob(path))
                parsed += 1
        self.assertGreater(parsed, 170)

    def test_handoff_remains_prepared_not_sent(self):
        text = git_blob(
            "docs/liora-venn/v674-v5/handoffs/"
            "tamar-vey-v674-v6-activation-candidate.md"
        ).decode("utf-8")
        self.assertIn("PREPARED_BY_LIORA_VENN = true", text)
        self.assertIn("SENT_BY_LIORA_VENN = false", text)
        self.assertIn("EXTERNAL_POSTCOMMIT_BINDING_REQUIRED", text)
        self.assertIn("v725-v8", text)

    def test_clean_state(self):
        self.assertEqual(git("status", "--porcelain"), "")


if __name__ == "__main__":
    unittest.main()
