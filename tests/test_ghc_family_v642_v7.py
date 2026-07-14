from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PHASE = ROOT / "docs/tamar-vey/v642-v7"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


evidence = load_module("ghc_family_constraint_evidence", "ghc_family_constraint_evidence.py")
validator = load_module("ghc_family_constraint_evidence_validator", "ghc_family_constraint_evidence_validator.py")
minimal = load_module("ghc_family_constraint_evidence_minimal", "ghc_family_constraint_evidence_minimal.py")


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TestGhcFamilyV642V7(unittest.TestCase):
    def test_frozen_observed_distribution(self):
        distribution = {label: list(evidence.OBSERVED.values()).count(label) for label in evidence.TRUTH_LABELS}
        self.assertEqual(distribution, {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})

    def test_exactly_ten_groups_and_eighty_cases(self):
        groups = evidence.case_groups()
        self.assertEqual(len(groups), 10)
        self.assertEqual(sum(len(group["cases"]) for group in groups), 80)

    def test_all_preregistered_cases_match(self):
        for group in evidence.case_groups():
            result = evidence.evaluate_group(group)
            self.assertEqual(result["case_count"], 8)
            self.assertEqual(result["matched_count"], 8)
            self.assertEqual(result["retained_negative_count"], 7)

    def test_constraint_algebra_rejects_miscount(self):
        observed, reasons = evidence.constraint_algebra_decision(
            dict(primary_constraints_declared=True, secondary_constraints_closed=True, poisson_brackets_closed=True, class_counts_valid=False, reduced_phase_space_even=True, dof_count_matches=False, dimensions_valid=True, empirical_promotion=False)
        )
        self.assertEqual(observed, "reject")
        self.assertIn("first_second_class_misclassification", reasons)
        self.assertIn("physical_degree_of_freedom_mismatch", reasons)

    def test_observation_process_remains_representation(self):
        canonical = evidence.case_groups()[2]["cases"][0].copy()
        canonical.pop("case_id")
        canonical.pop("expected")
        observed, reasons = evidence.observation_process_decision(canonical)
        self.assertEqual((observed, reasons), ("represented", []))

    def test_thos_real_arm_fails_closed(self):
        canonical = evidence.case_groups()[3]["cases"][0].copy()
        canonical.pop("case_id")
        canonical.pop("expected")
        canonical["real_arms"] = 1
        observed, reasons = evidence.thos_estimand_decision(canonical)
        self.assertEqual(observed, "reject")
        self.assertIn("unreviewed_real_arm_execution", reasons)

    def test_jurisdiction_never_selects_law(self):
        canonical = evidence.case_groups()[5]["cases"][0].copy()
        canonical.pop("case_id")
        canonical.pop("expected")
        observed, reasons = evidence.jurisdiction_decision(canonical)
        self.assertEqual((observed, reasons), ("exact_gate", []))
        canonical["governing_law_selected"] = True
        self.assertEqual(evidence.jurisdiction_decision(canonical)[0], "reject")

    def test_same_owner_is_not_independent_reproduction(self):
        canonical = evidence.case_groups()[7]["cases"][0].copy()
        canonical.pop("case_id")
        canonical.pop("expected")
        canonical["independent_reproduction_claimed"] = True
        observed, reasons = evidence.stochastic_replay_decision(canonical)
        self.assertEqual(observed, "reject")
        self.assertIn("same_owner_called_independent_reproduction", reasons)

    def test_stage20_canonical_abstains(self):
        canonical = evidence.case_groups()[9]["cases"][0].copy()
        canonical.pop("case_id")
        canonical.pop("expected")
        observed, reasons = evidence.stage20_abstention_decision(canonical)
        self.assertEqual((observed, reasons), ("open_gap", []))

    def test_generated_ledger_and_negative_floor(self):
        ledger = read("x2-proposal-ledger.json")
        negatives = read("retained-negative-register.json")
        self.assertEqual(ledger["total_case_count"], 80)
        self.assertEqual(ledger["total_matched_count"], 80)
        self.assertGreaterEqual(negatives["negative_count"], 308)
        self.assertTrue(negatives["all_retained"])

    def test_protected_claims_and_terminal_verdict(self):
        truth = read("phase-truth.json")
        self.assertTrue(all(value is False for value in truth["protected_claims"].values()))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_full_validator_pending_snapshot(self):
        result = validator.validate(ROOT, PHASE, allow_pending_snapshot=True)
        self.assertTrue(result["valid"], result["issues"])

    def test_minimal_validator_pending_snapshot(self):
        result = minimal.verify(PHASE, allow_pending_snapshot=True)
        self.assertTrue(result["valid"], result["checks"])


if __name__ == "__main__":
    unittest.main()
