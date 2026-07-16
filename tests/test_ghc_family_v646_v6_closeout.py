from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sylven-arc/v646-v6"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class V646V6CloseoutTests(unittest.TestCase):
    def test_phase_truth(self):
        truth = load("phase-truth.json")
        self.assertEqual(truth["planned_phase_commit_count"], 3)
        self.assertEqual(truth["merge_commits_allowed"], 0)
        self.assertEqual(truth["proposal_distribution"], {"completed": 6, "exact_gate": 1, "open_gap": 1, "represented": 2})
        self.assertEqual(truth["effective_negatives"], 2973)
        self.assertEqual((truth["effective_open_gaps"], truth["effective_exact_gates"]), (15, 16))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_closeout_and_seal_bindings(self):
        closeout = load("closeout-receipt.json")
        seal = load("seal-receipt.json")
        self.assertEqual(closeout["evidence_revision"], seal["evidence_revision"])
        self.assertEqual(seal["expected_phase_commits"], 3)
        self.assertEqual(seal["expected_merge_commits"], 0)
        self.assertEqual(seal["negative_erasure_count"], 0)
        self.assertEqual(seal["silent_gate_closure_count"], 0)

    def test_final_route_prepared(self):
        route = load("orchestration/final-route-gate.json")
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)
        self.assertFalse(route["task_created"])
        self.assertFalse(route["standby_contacted"])

    def test_final_validation_record_boundaries(self):
        record = load("final-validation-record.json")
        self.assertTrue(record["same_owner_only"])
        self.assertFalse(record["independent_reproduction"])
        self.assertFalse(record["full_repository_suite_run"])
        self.assertIn("named replay", " ".join(record["required_post_commit"]))

    def test_manifest_shape(self):
        manifest = load("validation/final-owner-manifest.json")
        self.assertEqual(manifest["hash_domain"], "git_index_blob")
        self.assertEqual(len(manifest["entries"]), manifest["entry_count"])
        self.assertEqual(len(manifest["expected_owner_paths"]), manifest["expected_owner_path_count"])
        self.assertEqual(len(manifest["declared_self_exclusions"]), 3)

    def test_rotation_threshold_scope(self):
        receipt = load("environment/final-rotation-receipt.json")
        self.assertFalse(receipt["rotation_required"])
        self.assertFalse(receipt["inherited_files_counted_toward_rotation"])

    def test_final_checklist_keeps_external_work_open(self):
        checklist = load("final-complete-incomplete-checklist.json")
        self.assertGreaterEqual(len(checklist["externally_incomplete"]), 7)
        self.assertIn("one acknowledged Eiren v646-v7 baton", checklist["pending_until_post_commit"])


if __name__ == "__main__":
    unittest.main()
