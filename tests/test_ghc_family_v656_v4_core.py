#!/usr/bin/env python3
"""Core contract tests for Caelen Morrow v656-v4."""

from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v656_v4_phase_data as d
from ghc_family_v656_v4_core import (
    FORBIDDEN_CLAIMS,
    MUTATION_CLASSES,
    ZERO_REAL_COUNTS,
    execute_contract,
    make_contract,
    mutations,
    run_proposals,
    validate_contract,
)


class CaelenMorrowV656V4CoreTests(unittest.TestCase):
    def test_valid_contracts_pass(self) -> None:
        for proposal in d.PROPOSALS:
            self.assertEqual(validate_contract(make_contract(proposal)), [])

    def test_each_contract_has_five_mutations(self) -> None:
        for proposal in d.PROPOSALS:
            self.assertEqual(len(mutations(make_contract(proposal))), 5)

    def test_mutation_classes_are_exact(self) -> None:
        contract = make_contract(d.PROPOSALS[0])
        self.assertEqual([name for name, _ in mutations(contract)], MUTATION_CLASSES)

    def test_every_mutation_is_rejected(self) -> None:
        for proposal in d.PROPOSALS:
            for _, mutated in mutations(make_contract(proposal)):
                self.assertTrue(validate_contract(mutated))

    def test_every_contract_result_passes(self) -> None:
        for proposal in d.PROPOSALS:
            result = execute_contract(make_contract(proposal))
            self.assertTrue(result["passed"])
            self.assertEqual(result["mutations_rejected"], 5)

    def test_full_suite_is_30_and_150(self) -> None:
        result = run_proposals(d.PROPOSALS)
        self.assertTrue(result["valid"])
        self.assertEqual(result["proposal_count"], 30)
        self.assertEqual(result["passed"], 30)
        self.assertEqual(result["mutations"], 150)
        self.assertEqual(result["mutations_rejected"], 150)

    def test_disposition_distribution(self) -> None:
        self.assertEqual(
            Counter(p["expected_disposition"] for p in d.PROPOSALS),
            Counter({"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}),
        )

    def test_zero_real_counts_are_all_zero(self) -> None:
        self.assertTrue(ZERO_REAL_COUNTS)
        self.assertTrue(all(value == 0 for value in ZERO_REAL_COUNTS.values()))

    def test_all_claim_flags_are_false(self) -> None:
        for proposal in d.PROPOSALS:
            contract = make_contract(proposal)
            self.assertEqual(set(contract["claim_flags"]), set(FORBIDDEN_CLAIMS))
            self.assertFalse(any(contract["claim_flags"].values()))

    def test_authority_state_is_absent(self) -> None:
        for proposal in d.PROPOSALS:
            self.assertTrue(
                all(
                    value == "absent"
                    for value in make_contract(proposal)["authority_state"].values()
                )
            )


if __name__ == "__main__":
    unittest.main()
