from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "orin-thale" / "v674-v4"
EVIDENCE_HEAD = "1a076e80fa77ea9d37ce1162174e3c1725f82e9b"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class OrinV674V4CloseoutPrecommitTests(unittest.TestCase):
    def test_head_is_immutable_evidence_before_final_commit(self):
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True, encoding="utf-8").strip()
        self.assertEqual(head, EVIDENCE_HEAD)

    def test_phase_truth_and_terminal_verdict(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12})
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["real_data_rows"], 0)
        self.assertFalse(truth["successor_contacted"])

    def test_counts_are_preserved(self):
        truth = load("closeout/phase-truth.json")
        self.assertEqual(truth["effective_negatives"], 38861)
        self.assertEqual(truth["effective_methods"], 26864)
        self.assertEqual(truth["effective_failed_witnesses"], 10522)
        self.assertEqual(truth["effective_bounded_passing_witnesses"], 14147)
        self.assertEqual(truth["effective_open_gaps"], 319)
        self.assertEqual(truth["effective_exact_gates"], 312)

    def test_content_seal_matches_current_bytes(self):
        seal = load("closeout/content-seal.json")
        self.assertEqual(seal["target_count"], 15)
        for entry in seal["targets"]:
            raw = (REPO / entry["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])

    def test_final_owner_and_delta_manifests_match_current_bytes(self):
        for relative in ("validation/final-owner-manifest.json", "validation/final-delta-manifest.json"):
            manifest = load(relative)
            for entry in manifest["entries"]:
                raw = (REPO / entry["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])
                self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_exact_staged_review_matches_index(self):
        review = load("validation/final-staged-review.json")
        self.assertEqual(review["status"], "passed")
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["unresolved_privacy_candidates"], [])
        self.assertEqual(review["confirmed_privacy_hits"], [])
        for entry in review["entries"]:
            raw = subprocess.check_output(["git", "show", f":{entry['path']}"], cwd=REPO)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])

    def test_handoff_is_prepared_not_sent(self):
        text = (ROOT / "handoffs" / "liora-venn-v674-v5-activation-candidate.md").read_text(encoding="utf-8")
        self.assertIn("PREPARED_BY_ORIN_THALE = true", text)
        self.assertIn("SENT_BY_ORIN_THALE = false", text)
        self.assertIn("v725-v8", text)
        self.assertIn("Tamar Vey", text)

    def test_checklist_retains_incomplete_items(self):
        checklist = load("closeout/complete-incomplete-checklist.json")
        self.assertGreater(len(checklist["completed_items"]), 10)
        self.assertGreater(len(checklist["incomplete_or_gated_items"]), 8)
        self.assertTrue(checklist["no_incomplete_item_silently_closed"])

    def test_all_closeout_json_parses_and_caps_hold(self):
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


if __name__ == "__main__":
    unittest.main()
