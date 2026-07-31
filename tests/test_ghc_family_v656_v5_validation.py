#!/usr/bin/env python3
"""Evidence validation tests for Eiren Kestrel v656-v5."""

from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v656_v5_phase_data as d
from ghc_family_v656_v5_phase_catalogue import X1_OPERATIONAL_NEGATIVES
from ghc_family_v656_v5_validate import detailed_checks, minimal_checks
from ghc_family_v656_v5_x2_data import X2_OPERATIONAL_NEGATIVES


ROOT = REPO / d.PHASE_ROOT


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class EirenKestrelV656V5ValidationTests(unittest.TestCase):
    def test_all_thirty_surface_triplets_exist(self) -> None:
        for proposal in d.PROPOSALS:
            for name in ("contract.json", "mutation-results.json", "bounded-receipt.json"):
                self.assertTrue((ROOT / "surfaces" / proposal["slug"] / name).is_file())

    def test_outcomes_are_exact(self) -> None:
        proposals = read_json("x2/proposal-ledger.json")["proposals"]
        self.assertEqual(
            Counter(item["observed_outcome"] for item in proposals),
            Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}),
        )

    def test_mutation_results_are_150_rejections(self) -> None:
        total = 0
        for proposal in d.PROPOSALS:
            result = read_json(f"surfaces/{proposal['slug']}/mutation-results.json")
            total += result["mutations_rejected"]
            self.assertEqual(result["mutation_count"], 5)
            self.assertTrue(result["passed"])
        self.assertEqual(total, 150)

    def test_bounded_receipts_refuse_independent_credit(self) -> None:
        for proposal in d.PROPOSALS:
            receipt = read_json(f"surfaces/{proposal['slug']}/bounded-receipt.json")
            self.assertTrue(receipt["valid"])
            self.assertTrue(receipt["same_owner_only"])
            self.assertFalse(receipt["independent_reproduction"])

    def test_skills_are_phase_local(self) -> None:
        skills = list((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 10)
        for path in skills:
            text = path.read_text(encoding="utf-8")
            self.assertIn("Phase-local", text)
            self.assertIn("no real", text.casefold())

    def test_runners_are_family_compatible(self) -> None:
        receipts = list((ROOT / "runners").glob("*-receipt.json"))
        self.assertEqual(len(receipts), 10)
        self.assertTrue(all(json.loads(p.read_text())["valid"] for p in receipts))

    def test_effective_negative_count(self) -> None:
        register = read_json("truth/retained-negative-register-x2.json")
        self.assertEqual(register["source_effective_count"], d.SOURCE_EFFECTIVE_NEGATIVES)
        self.assertEqual(register["x1_operational_count"], len(X1_OPERATIONAL_NEGATIVES))
        self.assertEqual(register["x2_operational_count"], len(X2_OPERATIONAL_NEGATIVES))
        self.assertEqual(register["mutation_count"], 150)
        self.assertEqual(
            register["effective_count"],
            d.SOURCE_EFFECTIVE_NEGATIVES
            + len(X1_OPERATIONAL_NEGATIVES)
            + len(X2_OPERATIONAL_NEGATIVES)
            + 150,
        )

    def test_gaps_and_gates_remain_open(self) -> None:
        self.assertEqual(
            read_json("truth/open-gap-register-x2.json")["effective_count"],
            d.SOURCE_OPEN_GAPS + 1,
        )
        self.assertEqual(
            read_json("truth/exact-gate-register-x2.json")["effective_count"],
            d.SOURCE_EXACT_GATES + 1,
        )

    def test_method_flow_pairs_are_equal(self) -> None:
        flow = read_json("method-flow/method-flow-ledger-x2.json")
        expected = (
            d.SOURCE_METHODS
            + len(X1_OPERATIONAL_NEGATIVES)
            + 150
            + len(X2_OPERATIONAL_NEGATIVES)
        )
        self.assertEqual(flow["counts"]["methods"], expected)
        self.assertEqual(flow["counts"]["witness_results"]["fail"], expected)
        self.assertEqual(flow["counts"]["witness_results"]["pass"], expected)

    def test_detailed_checks_are_82_of_82(self) -> None:
        checks = detailed_checks()
        self.assertEqual(len(checks), 82)
        self.assertTrue(all(item["passed"] for item in checks))

    def test_minimal_checks_are_15_of_15(self) -> None:
        checks = minimal_checks()
        self.assertEqual(len(checks), 15)
        self.assertTrue(all(item["passed"] for item in checks))

    def test_terminal_truth_is_bounded(self) -> None:
        truth = read_json("truth/phase-truth-evidence.json")
        self.assertEqual(truth["verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["terminal_route_contacted"])
        self.assertFalse(truth["full_repository_suite_run"])
        self.assertFalse(truth["independent_reproduction"])


if __name__ == "__main__":
    unittest.main()
