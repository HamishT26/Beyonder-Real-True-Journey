from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "orin-thale" / "v674-v4"
SOURCE_FINAL = "dcdc2921b193516242c93e6ef303f854e9d21264"
X1_HEAD = "5728299ca983aa504a64a5038197358bc50c4ceb"
EVIDENCE_HEAD = "1a076e80fa77ea9d37ce1162174e3c1725f82e9b"
BRANCH = "codex/GHC-Family/orin-thale-v674-v4-full-tools"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def git_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=REPO)


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class OrinV674V4FinalTests(unittest.TestCase):
    def test_exact_branch_and_direct_parent(self):
        self.assertEqual(git("branch", "--show-current"), BRANCH)
        self.assertEqual(git("rev-parse", "HEAD^"), EVIDENCE_HEAD)

    def test_three_direct_commits_and_zero_merges(self):
        self.assertEqual(git("rev-list", "--count", f"{SOURCE_FINAL}..HEAD"), "3")
        self.assertEqual(git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..HEAD"), "0")
        self.assertEqual(git("rev-parse", f"{X1_HEAD}^"), SOURCE_FINAL)
        self.assertEqual(git("rev-parse", f"{EVIDENCE_HEAD}^"), X1_HEAD)

    def test_final_has_one_parent(self):
        parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()
        self.assertEqual(len(parents), 2)

    def test_phase_truth_partition_and_verdict(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction"])
        self.assertFalse(truth["complete_repository_suite_run"])

    def test_final_counts_are_exact(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual((truth["effective_negatives"], truth["effective_methods"]), (38861, 26864))
        self.assertEqual((truth["effective_failed_witnesses"], truth["effective_bounded_passing_witnesses"]), (10522, 14147))
        self.assertEqual((truth["effective_open_gaps"], truth["effective_exact_gates"]), (319, 312))

    def test_content_seal_matches_exact_final_blobs(self):
        seal = load("closeout/content-seal.json")
        for entry in seal["targets"]:
            raw = git_blob(entry["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])

    def test_final_owner_manifest_matches_exact_final_blobs(self):
        manifest = load("validation/final-owner-manifest.json")
        for entry in manifest["entries"]:
            raw = git_blob(entry["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_final_delta_manifest_matches_exact_final_blobs(self):
        manifest = load("validation/final-delta-manifest.json")
        for entry in manifest["entries"]:
            raw = git_blob(entry["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])

    def test_final_staged_review_matches_exact_final_blobs(self):
        review = load("validation/final-staged-review.json")
        self.assertEqual(review["status"], "passed")
        self.assertEqual(review["confirmed_privacy_hits"], [])
        for entry in review["entries"]:
            raw = git_blob(entry["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])

    def test_all_phase_json_parses(self):
        paths = git("ls-tree", "-r", "--name-only", "HEAD", "--", "docs/orin-thale/v674-v4").splitlines()
        parsed = 0
        for path in paths:
            if path.endswith(".json"):
                json.loads(git_blob(path))
                parsed += 1
        self.assertGreater(parsed, 160)

    def test_handoff_remains_prepared_not_sent(self):
        text = git_blob("docs/orin-thale/v674-v4/handoffs/liora-venn-v674-v5-activation-candidate.md").decode("utf-8")
        self.assertIn("SENT_BY_ORIN_THALE = false", text)
        self.assertIn("EXTERNAL_POSTCOMMIT_BINDING_REQUIRED", text)

    def test_clean_state(self):
        self.assertEqual(git("status", "--porcelain"), "")


if __name__ == "__main__":
    unittest.main()
