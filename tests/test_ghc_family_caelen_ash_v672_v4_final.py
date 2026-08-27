from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v672-v4"
CLOSEOUT = PHASE / "closeout"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class CaelenAshV672V4FinalTests(unittest.TestCase):
    def test_closeout_truth(self):
        truth = load(CLOSEOUT / "phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["full_repository_suite_run"])
        self.assertFalse(truth["independent_reproduction"])

    def test_closeout_effective_counts(self):
        counts = load(CLOSEOUT / "phase-truth.json")["effective_counts"]
        self.assertEqual(counts, {"negatives": 35416, "methods": 21986, "failed_witnesses": 7237, "passing_witnesses": 9287, "open_gaps": 283, "exact_gates": 276})

    def test_content_seal_targets_match(self):
        seal = load(CLOSEOUT / "content-seal.json")
        self.assertEqual(seal["target_count"], len(seal["targets"]))
        for row in seal["targets"]:
            path = ROOT / row["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row["sha256"], row["path"])
            self.assertEqual(path.stat().st_size, row["bytes"])

    def test_route_is_held_and_unsent(self):
        route = load(PHASE / "handoffs" / "terminal-route-hold.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["target"], "not_resolved_before_terminal_gate")
        self.assertEqual(route["send_count"], 0)
        self.assertFalse(route["delivery_acknowledged"])

    def test_final_candidate_is_prospective(self):
        candidate = load(CLOSEOUT / "final-validation-candidate.json")
        self.assertEqual(candidate["canonical_invocations_at_commit_time"], 0)
        self.assertEqual(candidate["canonical_successes_at_commit_time"], 0)
        self.assertEqual(candidate["canonical_status"], "pending_exact_pushed_final")
        self.assertFalse(candidate["postsuccess_replay_allowed"])

    def test_wellbeing_and_identity_boundary(self):
        wellbeing = load(CLOSEOUT / "wellbeing-check.json")
        self.assertFalse(wellbeing["identity_evidence"])
        self.assertTrue(wellbeing["corrigible"])
        self.assertEqual(wellbeing["pronouns"], "they/them")

    def test_stale_label_review(self):
        review = load(CLOSEOUT / "stale-label-review.json")
        self.assertEqual(review["stale_labels_found"], 0)
        self.assertTrue(review["prospective_labels_are_not_failures"])

    def test_owner_manifest_has_exact_arithmetic(self):
        manifest = load(CLOSEOUT / "owner-manifest.json")
        self.assertEqual(manifest["owner_path_count"], manifest["expected_owner_path_count"])
        self.assertEqual(manifest["owner_path_count"], manifest["entry_count"] + len(manifest["self_exclusions"]))
        self.assertEqual(len(manifest["self_exclusions"]), 3)

    def test_owner_manifest_index_blob_oids(self):
        manifest = load(CLOSEOUT / "owner-manifest.json")
        for row in manifest["entries"]:
            observed = subprocess.run(
                ["git", "-C", str(ROOT), "rev-parse", f":{row['path']}"],
                text=True, capture_output=True, check=True,
            ).stdout.strip()
            self.assertEqual(observed, row["git_blob_oid"], row["path"])

    def test_final_staged_review_is_valid(self):
        review = load(PHASE / "validation" / "final-staged-review.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["x1_frozen_changes"], [])
        self.assertEqual(review["out_of_scope_paths"], [])
        self.assertEqual(review["json_parse"]["issues"], [])
        self.assertEqual(review["privacy_scan"]["confirmed_hits"], 0)
        self.assertEqual(review["diff_hygiene"]["exit_code"], 0)

    def test_final_staged_manifest_arithmetic(self):
        manifest = load(PHASE / "validation" / "final-staged-manifest.json")
        self.assertEqual(manifest["expected_surface_count"], manifest["entry_count"] + len(manifest["self_exclusions"]))
        self.assertEqual(len(manifest["self_exclusions"]), 2)

    def test_phase_index_and_file_ceiling(self):
        index = load(CLOSEOUT / "phase-index.json")
        self.assertTrue(index["owner_file_ceiling_passed"])
        self.assertLess(len([path for path in PHASE.rglob("*") if path.is_file()]), 2000)

    def test_every_phase_json_parses(self):
        for path in PHASE.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_document_ceiling(self):
        for path in PHASE.rglob("*.md"):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 100000, path)

    def test_diff_hygiene(self):
        result = subprocess.run(
            ["git", "-C", str(ROOT), "diff", "--cached", "--check"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
