from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v681-v7"
X2 = PHASE / "x2"
VALIDATION = PHASE / "validation"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class CaelenAshV681V7X2Tests(unittest.TestCase):
    def test_01_x1_is_the_exact_parent_and_is_immutable(self):
        receipt = load(X2 / "evidence-receipt.json")
        self.assertEqual(receipt["x1_head"], "f31bb3fb3738136db75dc264325f267dc4068f4a")
        self.assertEqual(receipt["source"], "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe")
        self.assertTrue(receipt["strict_x1_before_x2"])

    def test_02_positive_controls_pass(self):
        data = load(X2 / "positive-controls.json")
        self.assertEqual(data["count"], 60)
        self.assertTrue(all(row["accepted"] for row in data["controls"]))

    def test_03_all_five_mutations_per_proposal_are_rejected(self):
        data = load(X2 / "mutation-results.json")
        self.assertEqual(data["count"], 300)
        self.assertEqual(data["mutation_types"], 5)
        self.assertTrue(all(not row["accepted"] and row["expected"] == "reject" for row in data["results"]))
        counts = {}
        for row in data["results"]:
            counts[row["proposal_id"]] = counts.get(row["proposal_id"], 0) + 1
        self.assertEqual(set(counts.values()), {5})

    def test_04_outcome_vocabulary_and_counts_are_exact(self):
        data = load(X2 / "proposal-outcomes.json")
        self.assertEqual(data["counts"], {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12})
        self.assertEqual(set(data["counts"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertFalse(data["reserved_claims_closed"])

    def test_05_twenty_phase_local_skills_are_validated_and_used(self):
        data = load(X2 / "skill-smoke-receipts.json")
        self.assertEqual(data["count"], 20)
        self.assertFalse(data["global_install"])
        self.assertTrue(all(row["quick_validation"] == "passed" and row["smoke_use"] == "passed" for row in data["receipts"]))

    def test_06_ten_family_current_runners_are_built_and_used(self):
        data = load(X2 / "runner-smoke-receipts.json")
        self.assertEqual(data["count"], 10)
        self.assertTrue(all(row["structural_validation"] == "passed" and row["positive_invocations"] == 6 and row["rejecting_invocations"] == 30 for row in data["receipts"]))

    def test_07_portfolio_execution_is_bounded(self):
        data = load(X2 / "portfolio-execution.json")
        self.assertEqual(data["completed_counts"], {"bounded_candidate": 80, "clean_fix_refine": 100, "safe_now": 120})
        self.assertEqual(data["unexecuted_counts"], {"blocked": 10, "exact_approval": 20})
        self.assertTrue(data["caps_are_ceilings"])

    def test_08_method_flow_counts_are_additive(self):
        data = load(X2 / "method-flow-ledger.json")
        self.assertEqual(data["current_after_x2"]["effective_negatives"], 54848)
        self.assertEqual(data["current_after_x2"]["effective_methods"], 63645)
        self.assertEqual(data["current_after_x2"]["failed_witnesses"], 26509)
        self.assertEqual(data["current_after_x2"]["bounded_passing_witnesses"], 45167)
        self.assertEqual(data["current_after_x2"]["open_gaps"], 485)
        self.assertEqual(data["current_after_x2"]["exact_gates"], 476)
        self.assertFalse(data["failure_erasure"])

    def test_09_exact_and_blocked_work_remains_unexecuted(self):
        data = load(X2 / "portfolio-execution.json")
        for group in ("exact_approval", "blocked"):
            self.assertTrue(all(not row["executed_in_x2"] for row in data[group]))

    def test_10_privacy_and_authority_boundaries_hold(self):
        privacy = load(VALIDATION / "x2-privacy-scan.json")
        self.assertEqual(privacy["confirmed_hits"], [])
        evidence = load(X2 / "evidence-receipt.json")
        self.assertEqual(evidence["real_rows"], 0)
        self.assertFalse(evidence["external_actions"])
        self.assertEqual(evidence["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_11_static_report_reserves_manual_evaluation(self):
        text = (X2 / "accessible-static-report.html").read_text(encoding="utf-8")
        self.assertIn('lang="en"', text)
        self.assertIn("Manual and affected-user evaluation remains reserved", text)
        self.assertNotIn("<script", text.lower())

    def test_12_working_tree_manifest_replays(self):
        manifest = load(VALIDATION / "x2-evidence-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])


if __name__ == "__main__":
    unittest.main()
