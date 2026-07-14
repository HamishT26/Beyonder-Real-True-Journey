from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PHASE = ROOT / "docs/sable-rook/v643-v3"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


evidence = load_module("ghc_family_thos_integrity", "ghc_family_thos_integrity.py")
validator = load_module("ghc_family_thos_integrity_validator", "ghc_family_thos_integrity_validator.py")
minimal = load_module("ghc_family_thos_integrity_minimal", "ghc_family_thos_integrity_minimal.py")


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def canonical(proposal_id: str) -> dict:
    return copy.deepcopy(evidence.canonical_inputs()[proposal_id])


class TestGhcFamilyV643V3(unittest.TestCase):
    def test_01_frozen_observed_distribution(self):
        distribution = {label: list(evidence.OBSERVED.values()).count(label) for label in evidence.TRUTH_LABELS}
        self.assertEqual(distribution, {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})

    def test_02_exactly_ten_groups_and_eighty_cases(self):
        groups = evidence.fixture_catalog()
        self.assertEqual(len(groups), 10)
        self.assertEqual(sum(len(rows) for rows in groups.values()), 80)

    def test_03_all_preregistered_cases_match_and_seventy_reject(self):
        evaluated = evidence.evaluate_catalog()
        self.assertTrue(all(row["matched_expectation"] for rows in evaluated.values() for row in rows))
        self.assertEqual(sum(not row["accepted"] for rows in evaluated.values() for row in rows), 70)

    def test_04_provenance_rejects_conflict_truth_shortcut(self):
        case = canonical("V6433-P01")
        case["conflict_invalidity_inference"] = True
        accepted, reasons, _ = evidence.provenance_decision(case)
        self.assertFalse(accepted)
        self.assertIn("disclosed_conflict_treated_as_automatic_invalidity", reasons)

    def test_05_causal_cone_rejects_missing_matter_relation(self):
        case = canonical("V6433-P02")
        case["matter_metric_relation"] = "missing"
        self.assertFalse(evidence.causal_cone_decision(case)[0])

    def test_06_fisher_rejects_empirical_promotion(self):
        case = canonical("V6433-P03")
        case["empirical_confirmation_claim"] = True
        self.assertFalse(evidence.fisher_decision(case)[0])

    def test_07_fidelity_rejects_broken_budget(self):
        case = canonical("V6433-P04")
        case["matched_budget"] = False
        accepted, reasons, _ = evidence.fidelity_decision(case)
        self.assertFalse(accepted)
        self.assertIn("matched_budget_broken", reasons)

    def test_08_burden_rejects_zero_row_parity_promotion(self):
        case = canonical("V6433-P05")
        case["burden_parity_claim"] = True
        self.assertFalse(evidence.burden_decision(case)[0])

    def test_09_suspension_rejects_unauthorized_reinstatement(self):
        case = canonical("V6433-P06")
        case["authorized_reinstater"] = False
        self.assertFalse(evidence.suspension_decision(case)[0])

    def test_10_emergency_rejects_authority_substitution(self):
        case = canonical("V6433-P07")
        case["technical_authority_substitution"] = True
        self.assertFalse(evidence.emergency_decision(case)[0])

    def test_11_logging_rejects_cr_injection(self):
        case = canonical("V6433-P08")
        case.update({"injected_char": "CR", "control_chars_escaped": False})
        accepted, reasons, _ = evidence.logging_decision(case)
        self.assertFalse(accepted)
        self.assertIn("control_character_not_escaped", reasons)

    def test_12_concurrency_rejects_interleaving_divergence(self):
        case = canonical("V6433-P09")
        case["equivalent_linearizations_same_hash"] = False
        self.assertFalse(evidence.concurrency_decision(case)[0])

    def test_13_free_energy_rejects_physical_unit_substitution(self):
        case = canonical("V6433-P10")
        case["physical_energy_unit"] = "joule"
        accepted, reasons, _ = evidence.free_energy_decision(case)
        self.assertFalse(accepted)
        self.assertIn("variational_objective_assigned_physical_energy_unit", reasons)

    def test_14_constants_pin_source_seal_and_x1(self):
        self.assertEqual(evidence.SOURCE_COMMIT, "6ad663e2198ca63490807fdc52890b08d8729b80")
        self.assertEqual(evidence.SOURCE_SEAL, "2ce0e9fa99f93a9d7e9c71c5c05f5df885f55c65")
        self.assertEqual(evidence.X1_COMMIT, "a90891bbb6a5aa8db8976277cafe324e12cbbb3b")

    def test_15_manifest_contract_has_sixty_unique_paths(self):
        proposals = read("x1-proposals.json")["proposals"]
        paths = evidence.manifest_paths(PHASE, proposals)
        self.assertEqual(len(paths), 60)
        self.assertEqual(len(set(paths)), 60)

    def test_16_generated_ledgers_and_negative_floor(self):
        ledger = read("x2-proposal-ledger.json")
        negatives = read("retained-negative-register.json")
        collision = read("provenance/prior-proposal-collision-audit.json")
        expected_operational = len(collision["x1_execution_negatives"]) + len(evidence.X2_OPERATIONAL_NEGATIVES)
        self.assertEqual((ledger["case_count"], ledger["synthetic_rejection_count"]), (80, 70))
        self.assertEqual(negatives["negative_count"], 558 + 70 + expected_operational)
        self.assertEqual(negatives["new_operational_count"], expected_operational)
        self.assertTrue(negatives["all_retained"])

    def test_17_exact_gate_counts_and_terminal_verdict(self):
        gates = read("exact-open-gate-register.json")
        truth = read("phase-truth.json")
        self.assertEqual((gates["open_gap_count"], gates["exact_gate_count"]), (5, 6))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_18_static_report_structure(self):
        report = (PHASE / "deliverables/v643-v3-thos-integrity-report.html").read_text(encoding="utf-8")
        for marker in ('<html lang="en-NZ">', 'Skip to main content', '<main id="main">', '<caption>', 'NOT_READY_FOR_STAGE_20', '@media print', 'forced-colors'):
            self.assertIn(marker, report)
        self.assertNotIn("<script", report.lower())

    def test_19_full_validator_pending_snapshot(self):
        result = validator.validate(ROOT, PHASE, allow_pending_snapshot=True)
        self.assertTrue(result["valid"], result["issues"])

    def test_20_minimal_validator_pending_snapshot(self):
        result = minimal.verify(PHASE, allow_pending_snapshot=True)
        self.assertTrue(result["valid"], result["issues"])


if __name__ == "__main__":
    unittest.main()
