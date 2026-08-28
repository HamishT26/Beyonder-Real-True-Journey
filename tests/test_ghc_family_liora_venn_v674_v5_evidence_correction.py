from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs" / "liora-venn" / "v674-v5" / "x2"
ORIGINAL_EVIDENCE = "06af8881c44826cd3161d80f0a4359912ff1ce68"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)


class LioraV674V5EvidenceCorrectionTests(unittest.TestCase):
    def test_head_is_retained_first_evidence_before_correction_commit(self):
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True, encoding="utf-8").strip()
        self.assertEqual(head, ORIGINAL_EVIDENCE)

    def test_original_manifest_failure_is_exact_and_retained(self):
        diagnostic = load("correction/original-manifest-diagnostic.json")
        self.assertFalse(diagnostic["original_manifest_passed"])
        self.assertTrue(diagnostic["original_failure_retained"])
        self.assertEqual(diagnostic["entries_checked"], 204)
        self.assertEqual(diagnostic["mismatch_count"], 20)
        self.assertTrue(all(row["path"].endswith("/agents/openai.yaml") for row in diagnostic["mismatches"]))

    def test_four_operational_failures_are_retained(self):
        ledger = load("correction/operational-failure-ledger.json")
        self.assertEqual(ledger["failed_witness_count"], 4)
        self.assertEqual([row["id"] for row in ledger["failed_witnesses"]], ["LV6745-EV-N001", "LV6745-EV-N002", "LV6745-EV-N003", "LV6745-EV-N004"])
        self.assertTrue(all(row["initial_credit"] == 0 for row in ledger["failed_witnesses"]))
        self.assertTrue(ledger["recoveries_do_not_rewrite_failures"])

    def test_corrected_counts_are_additive(self):
        truth = load("correction/corrected-phase-truth.json")
        self.assertEqual(truth["outcomes"], {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12})
        self.assertEqual(truth["effective_negatives"], 39123)
        self.assertEqual(truth["effective_methods"], 27276)
        self.assertEqual(truth["effective_failed_witnesses"], 10784)
        self.assertEqual(truth["effective_bounded_passing_witnesses"], 14559)
        self.assertEqual(truth["effective_open_gaps"], 322)
        self.assertEqual(truth["effective_exact_gates"], 315)
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_correction_owner_manifest_matches_normalized_index_blobs(self):
        manifest = load("validation/evidence-correction-owner-manifest.json")
        self.assertEqual(manifest["domain"], "git_index_normalized_blob_bytes_before_correction_commit")
        self.assertGreater(len(manifest["entries"]), 200)
        for entry in manifest["entries"]:
            raw = index_blob(entry["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])
            self.assertEqual(len(raw), entry["bytes"], entry["path"])

    def test_correction_staged_review_matches_index(self):
        review = load("validation/evidence-correction-staged-review.json")
        self.assertEqual(review["status"], "passed")
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(review["unresolved_privacy_candidates"], [])
        self.assertEqual(review["confirmed_privacy_hits"], [])
        for entry in review["entries"]:
            raw = index_blob(entry["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"], entry["path"])

    def test_correction_receipt_has_no_canonical_or_route_credit(self):
        receipt = load("correction/correction-receipt.json")
        self.assertEqual(receipt["original_manifest_success_credit"], 0)
        self.assertEqual(receipt["corrected_evidence_binding"], "external_postcommit_binding_required")
        self.assertEqual(receipt["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_all_correction_json_parses_and_caps_hold(self):
        files = [path for path in (ROOT / "correction").rglob("*") if path.is_file()]
        self.assertLess(len(files) + 2, 2000)
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertLessEqual(len(text.split()), 100000, path)
            if path.suffix == ".json":
                json.loads(text)


if __name__ == "__main__":
    unittest.main()
