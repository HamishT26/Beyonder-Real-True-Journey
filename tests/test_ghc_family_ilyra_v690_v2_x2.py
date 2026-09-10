"""X2 tests for Ilyra Fen v690-v2."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from scripts.ghc_family_obligation_graph_x1 import run as run_x1
from scripts.ghc_family_obligation_graph_x2 import run as run_x2

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "ilyra-fen" / "v690-v2" / "plan"
X2 = ROOT / "docs" / "ilyra-fen" / "v690-v2" / "x2"


class IlyraV690V2X2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads((PLAN / "new-proposals.json").read_text(encoding="utf-8"))
        cls.rows = [row for row in payload["proposals"] if row["lane"] == "x2"]

    def test_exact_safe_envelopes(self):
        self.assertEqual(len(self.rows), 100)
        for row in self.rows:
            request = copy.deepcopy(row["request"])
            original = copy.deepcopy(request)
            self.assertEqual(run_x2(request), row["expected"], row["proposal_id"])
            self.assertEqual(request, original, row["proposal_id"])

    def test_candidate_subjects_remain_failed(self):
        for row in self.rows:
            subject = copy.deepcopy(row["candidate_subject"])
            original = copy.deepcopy(subject)
            self.assertEqual(run_x2(subject), row["candidate_expected"], row["proposal_id"])
            self.assertEqual(subject, original, row["proposal_id"])

    def test_exact_outcome_distribution(self):
        observed = {"completed": 0, "represented": 0, "open_gap": 0, "exact_gate": 0}
        for row in self.rows:
            observed[run_x2(copy.deepcopy(row["request"]))["outcome"]] += 1
        self.assertEqual(observed, {"completed": 80, "represented": 10, "open_gap": 5, "exact_gate": 5})

    def test_x1_remains_compatible(self):
        x1_row = next(
            row
            for row in json.loads((PLAN / "new-proposals.json").read_text(encoding="utf-8"))["proposals"]
            if row["lane"] == "x1"
        )
        self.assertEqual(run_x1(copy.deepcopy(x1_row["request"])), x1_row["expected"])

    def test_unknown_operation_is_refused(self):
        self.assertEqual(
            run_x2({"operation": "native_task_send", "payload": {}}),
            {"ok": False, "error": "unknown_operation", "original_success_credit": 0},
        )

    def test_x2_evidence_counts(self):
        results = json.loads((X2 / "results.json").read_text(encoding="utf-8"))
        candidates = json.loads((X2 / "candidate-subjects.json").read_text(encoding="utf-8"))
        refinements = json.loads((X2 / "refinements.json").read_text(encoding="utf-8"))
        self.assertEqual(results["count"], 100)
        self.assertTrue(all(row["passed"] for row in results["records"]))
        self.assertEqual(candidates["count"], 100)
        self.assertTrue(all(row["subject_result"] == "fail" for row in candidates["records"]))
        self.assertEqual(refinements["count"], 100)
        self.assertTrue(all(row["lossless_equal"] for row in refinements["records"]))

    def test_method_and_package_counts(self):
        flow = json.loads((X2 / "method-flow.json").read_text(encoding="utf-8"))
        packages = json.loads(
            (X2 / "toolchain" / "package-comparisons.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            flow["counts"],
            {
                "effective_negatives": 138,
                "failed": 138,
                "methods": 11,
                "passing": 373,
                "witnesses": 511,
            },
        )
        self.assertEqual(len(packages["records"]), 30)
        self.assertTrue(all(row["passed"] for row in packages["records"]))
        self.assertFalse(packages["install_replayed"])

    def test_deck_immediate_parent_rules(self):
        paths = sorted((X2 / "deck" / "cards").glob("ghc-card-*.json"))
        cards = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
        self.assertEqual(len(cards), 213)
        by_id = {card["card_id"]: card for card in cards}
        self.assertEqual(len(by_id), 213)
        for card in cards:
            if card["tier"] == 1:
                self.assertEqual(card["parent_ids"], [])
            else:
                self.assertEqual(len(card["parent_ids"]), 1)
                parent = by_id[card["parent_ids"][0]]
                self.assertEqual(parent["tier"], card["tier"] - 1)

    def test_global_promotions_are_additive(self):
        receipt = json.loads(
            (X2 / "tooling" / "global-promotion.json").read_text(encoding="utf-8")
        )
        self.assertTrue(receipt["no_overwrite"])
        self.assertEqual(receipt["skills"], 5)
        self.assertEqual(receipt["runners"], 5)
        self.assertTrue(all(row["byte_parity"] for row in receipt["records"]))
        self.assertTrue(all(row["official_quick_validate"] for row in receipt["records"]))

    def test_x2_manifest_raw_worktree_bytes(self):
        manifest = json.loads((X2 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            data = (ROOT / row["path"]).read_bytes()
            self.assertEqual(len(data), row["bytes"], row["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"], row["path"])


if __name__ == "__main__":
    unittest.main()
