#!/usr/bin/env python3
"""Bounded x2 evidence tests for Sylven Arc v647-v4."""

from __future__ import annotations

import json
import re
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v647-v4"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_v647_v4_definitions import PROPOSALS  # noqa: E402
from ghc_family_v647_v4_runtime import evaluate, mutation_payloads, positive_payload  # noqa: E402


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class SylvenV647V4EvidenceTests(unittest.TestCase):
    def test_x1_freeze_and_x2_ten(self):
        x1 = load("x1-proposals.json")
        x2 = load("x2-proposal-ledger.json")
        self.assertEqual(x1["frozen_chain_count_after_x1"], 510)
        self.assertEqual(len(x1["proposals"]), 10)
        self.assertEqual(len(x2["rows"]), 10)

    def test_outcome_vocabulary_and_distribution(self):
        x2 = load("x2-proposal-ledger.json")
        outcomes = Counter(row["outcome"] for row in x2["rows"])
        self.assertEqual(outcomes, Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}))
        self.assertEqual(set(x2["outcome_vocabulary"]), {"completed", "represented", "open_gap", "exact_gate"})

    def test_all_concrete_artifacts_exist(self):
        for proposal in PROPOSALS:
            for relative in proposal["concrete_artifacts"]:
                self.assertTrue((PHASE / relative).is_file(), relative)

    def test_runtime_positive_and_mutation_falsifiers(self):
        for proposal in PROPOSALS:
            proposal_id = proposal["proposal_id"]
            accepted, reasons = evaluate(positive_payload(proposal_id))
            self.assertTrue(accepted, reasons)
            rows = mutation_payloads(proposal_id)
            self.assertEqual(len(rows), 7)
            self.assertTrue(all(row["observed"] == "reject" and row["pass"] for row in rows))

    def test_seventy_mutations_retained(self):
        receipt = load("validation/preregistered-synthetic-negatives.json")
        self.assertEqual((receipt["count"], receipt["executed"], receipt["rejected"]), (70, 70, 70))
        self.assertEqual(len({row["negative_id"] for row in receipt["rows"]}), 70)
        self.assertTrue(all(row["retained"] for row in receipt["rows"]))

    def test_all_real_world_counters_zero(self):
        receipt = load("validation/real-world-zero-receipt.json")
        self.assertTrue(receipt["all_zero"])
        self.assertTrue(receipt["counters"])
        self.assertTrue(all(value == 0 for value in receipt["counters"].values()))

    def test_negative_arithmetic_and_method_flow(self):
        negatives = load("retained-negative-register.json")
        expected = negatives["inherited_effective"] + negatives["x1_operational"] + negatives["preregistered_synthetic"] + negatives["x2_operational"]
        self.assertEqual(negatives["effective_total"], expected)
        self.assertTrue(negatives["no_negative_erased"])
        state = load("method-flow/method-flow-state.json")
        results = state["counts"]["witness_results"]
        self.assertGreaterEqual(results["fail"], 3)
        self.assertIn(results["fail"] - results["pass"], (0, 1))
        self.assertGreaterEqual(state["counts"]["states"]["preferred"], 3)

    def test_open_and_exact_gate_arithmetic(self):
        gates = load("exact-open-gate-register.json")
        self.assertEqual((gates["effective_open_gaps"], gates["effective_exact_gates"]), (21, 22))
        self.assertEqual(gates["closed_without_exact_evidence"], 0)

    def test_portfolio_floors(self):
        self.assertEqual(load("approval-packets/x2-safe-portfolio-execution.json")["completed"], 30)
        self.assertEqual(load("prototypes/x2-candidate-execution.json")["completed"], 20)
        self.assertEqual(load("maintenance/x2-clean-refine-ledger.json")["completed"], 30)

    def test_skills_and_family_runners(self):
        skills = load("skills/skill-build-receipt.json")
        runners = load("tooling/runner-execution.json")
        self.assertEqual((skills["count"], skills["quick_validated"], skills["smoke_used"]), (20, 20, 20))
        self.assertEqual((runners["built_count"], runners["used_count"]), (10, 10))

    def test_overview_is_three_page_equivalent_with_boundaries(self):
        text = (PHASE / "v647-v4-integrated-overview.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\b\w+\b", text, re.UNICODE))
        self.assertGreaterEqual(words, 1200)
        self.assertLessEqual(words, 6000)
        for token in ("THOS Body", "GMUT Mind", "Freed ID/CBR Heart", "NOT_READY_FOR_STAGE_20", "PREPARED_NOT_SENT", "same-owner"):
            self.assertIn(token, text)

    def test_static_report_structure_and_reserved_evaluation(self):
        text = (PHASE / "deliverables" / "v647-v4-static-report.html").read_text(encoding="utf-8")
        for token in ("<main", "<nav", "<table", "<caption", 'scope="col"', "Manual keyboard", "assistive-technology", "affected-user evaluation", "@media print"):
            self.assertIn(token, text)

    def test_route_full_suite_and_terminal_truth(self):
        truth = load("phase-truth.json")
        orchestration = load("orchestration/x2-update.json")
        self.assertEqual(truth["route_state"], "PREPARED_NOT_SENT")
        self.assertFalse(truth["full_repository_suite_run"])
        self.assertEqual(truth["full_repository_suite_owner"], "Eiren Kestrel")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(orchestration["send_count"], 0)
        self.assertFalse(orchestration["successor_task_created"])

    def test_owner_threshold_and_document_caps(self):
        rotation = load("environment/x2-rotation-receipt.json")
        self.assertLess(rotation["owner_generated_count"], rotation["threshold"])
        for path in PHASE.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".html"}:
                words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8"), re.UNICODE))
                self.assertLessEqual(words, 6000, str(path))


if __name__ == "__main__":
    unittest.main()
