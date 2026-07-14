from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PHASE = ROOT / "docs/ilyra-fen/v643-v2"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


evidence = load_module("ghc_family_model_assurance", "ghc_family_model_assurance.py")
validator = load_module("ghc_family_model_assurance_validator", "ghc_family_model_assurance_validator.py")
minimal = load_module("ghc_family_model_assurance_minimal", "ghc_family_model_assurance_minimal.py")


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def canonical(proposal_id: str) -> dict:
    return copy.deepcopy(evidence.canonical_inputs()[proposal_id])


class TestGhcFamilyV643V2(unittest.TestCase):
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

    def test_04_counterterm_rejects_missing_generated_operator(self):
        case = canonical("V6432-P01")
        case["declared_basis"] = ["kinetic"]
        accepted, reasons, _ = evidence.counterterm_decision(case)
        self.assertFalse(accepted)
        self.assertIn("loop_generated_operator_missing_from_basis", reasons)

    def test_05_frame_rejects_untransformed_matter_coupling(self):
        case = canonical("V6432-P02")
        case["matter_coupling_transformed"] = False
        self.assertFalse(evidence.frame_decision(case)[0])

    def test_06_running_rejects_prediction_promotion(self):
        case = canonical("V6432-P03")
        case["prediction_claim"] = True
        self.assertFalse(evidence.running_decision(case)[0])

    def test_07_expectancy_rejects_post_decode_freeze(self):
        case = canonical("V6432-P04")
        case["decoded_before_freeze"] = True
        accepted, reasons, _ = evidence.expectancy_decision(case)
        self.assertFalse(accepted)
        self.assertIn("decoded_before_analysis_freeze", reasons)

    def test_08_recovery_rejects_single_contact(self):
        case = canonical("V6432-P05")
        case["quorum"] = 1
        self.assertFalse(evidence.recovery_decision(case)[0])

    def test_09_accommodation_rejects_authority_substitution(self):
        case = canonical("V6432-P06")
        case["authority_substitution"] = True
        self.assertFalse(evidence.accommodation_decision(case)[0])

    def test_10_taint_rejects_private_to_public_derivative(self):
        case = canonical("V6432-P07")
        case["derived_label"] = "public"
        accepted, reasons, _ = evidence.taint_decision(case)
        self.assertFalse(accepted)
        self.assertIn("private_taint_not_propagated", reasons)

    def test_11_presentation_rejects_forced_color_loss(self):
        case = canonical("V6432-P08")
        case["forced_colors_preserve_meaning"] = False
        self.assertFalse(evidence.presentation_decision(case)[0])

    def test_12_fluctuation_rejects_psyche_promotion(self):
        case = canonical("V6432-P09")
        case["psyche_energy_claim"] = True
        accepted, reasons, _ = evidence.fluctuation_decision(case)
        self.assertFalse(accepted)
        self.assertIn("fluctuation_relation_promoted_beyond_domain", reasons)

    def test_13_multisite_rejects_transportability_promotion(self):
        case = canonical("V6432-P10")
        case["transportability_claim"] = True
        self.assertFalse(evidence.multisite_decision(case)[0])

    def test_14_constants_pin_source_and_x1(self):
        self.assertEqual(evidence.SOURCE_COMMIT, "bed184f32a3a390b573f8287ebd30032795fe9be")
        self.assertEqual(evidence.X1_COMMIT, "e65acfa996e367eb7f89a3143d5c247f70e704fc")

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
        self.assertEqual(negatives["negative_count"], 480 + 70 + expected_operational)
        self.assertEqual(negatives["new_operational_count"], expected_operational)
        self.assertTrue(negatives["all_retained"])

    def test_17_exact_gate_counts_and_terminal_verdict(self):
        gates = read("exact-open-gate-register.json")
        truth = read("phase-truth.json")
        self.assertEqual((gates["open_gap_count"], gates["exact_gate_count"]), (5, 6))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_18_static_report_structure(self):
        report = (PHASE / "deliverables/v643-v2-model-assurance-report.html").read_text(encoding="utf-8")
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
