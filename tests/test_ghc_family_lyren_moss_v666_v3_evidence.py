from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v666-v3"
X1_SHA = "e121ea6e207ea032edb1a0825ed86b1334481213"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class LyrenV666V3EvidenceTests(unittest.TestCase):
    def test_evidence_truth_and_counts(self):
        summary = load("evidence/evidence-summary.json")
        self.assertEqual(summary["outcome_counts"], {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(summary["synthetic_mutation_count"], 100)
        self.assertEqual(summary["synthetic_mutation_rejected_count"], 100)
        self.assertEqual(summary["effective_negatives"], 26392)
        self.assertEqual(summary["effective_methods"], 10934)
        self.assertEqual(summary["open_gaps"], 185)
        self.assertEqual(summary["exact_gates"], 183)
        self.assertEqual(summary["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_no_real_data_network_external_or_canonical(self):
        summary = load("evidence/evidence-summary.json")
        self.assertEqual(summary["real_data_rows"], 0)
        self.assertEqual(summary["network_calls_by_phase_software"], 0)
        self.assertEqual(summary["external_actions"], 0)
        self.assertFalse(summary["canonical_aggregate_invoked"])
        self.assertFalse(summary["complete_repository_suite_run"])
        self.assertFalse(summary["independent_reproduction"])

    def test_gap_and_gate_are_additive(self):
        state = load("evidence/authority-and-evidence-gaps.json")
        self.assertEqual((state["inherited_open_gaps"], state["new_open_gaps"], state["effective_open_gaps"]), (184, 1, 185))
        self.assertEqual((state["inherited_exact_gates"], state["new_exact_gates"], state["effective_exact_gates"]), (182, 1, 183))
        self.assertEqual(state["new_open_gap_rows"][0]["completion_credit"], 0)
        self.assertFalse(state["new_exact_gate_rows"][0]["executed"])

    def test_x1_tree_and_manifest_are_immutable(self):
        manifest = load("validation/x1-content-manifest.json")
        self.assertEqual(manifest["entry_count"], 18)
        for entry in manifest["entries"]:
            blob = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{X1_SHA}:{entry['path']}"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])
            self.assertEqual(len(blob), entry["size_bytes"])

    def test_evidence_manifest_replays_git_index_blobs(self):
        manifest = load("validation/evidence-content-manifest.json")
        self.assertGreater(manifest["entry_count"], 100)
        self.assertTrue(manifest["additive_only"])
        for entry in manifest["entries"]:
            blob = subprocess.check_output(["git", "-C", str(ROOT), "show", f":{entry['path']}"])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), entry["sha256"])
            self.assertEqual(len(blob), entry["size_bytes"])

    def test_staged_review_and_operational_failures(self):
        review = load("validation/evidence-staged-review.json")
        ops = load("method-flow/x2-operational-overlay.json")
        self.assertTrue(review["valid"])
        self.assertTrue(all(review["checks"].values()))
        self.assertEqual(review["privacy_confirmed_hits"], 0)
        self.assertEqual(ops["new_negative_count"], 4)
        self.assertEqual(ops["new_method_count"], 4)
        self.assertTrue(ops["no_failure_erased"])

    def test_closeout_and_later_paths_absent(self):
        for name in ("closeout", "seal", "final", "handoffs"):
            self.assertFalse((PHASE / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
