from __future__ import annotations

import copy
import importlib.util
import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PHASE = ROOT / "docs/eiren-kestrel/v643-v1"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


evidence = load_module("ghc_family_rights_resilience", "ghc_family_rights_resilience.py")
validator = load_module("ghc_family_rights_resilience_validator", "ghc_family_rights_resilience_validator.py")
minimal = load_module("ghc_family_rights_resilience_minimal", "ghc_family_rights_resilience_minimal.py")


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def canonical(proposal_id: str) -> dict:
    return copy.deepcopy(evidence.canonical_inputs()[proposal_id])


class TestGhcFamilyV643V1(unittest.TestCase):
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

    def test_04_purpose_rejects_secondary_use_drift(self):
        case = canonical("V6431-P01")
        case["derived_purpose"] = "marketing"
        accepted, reasons, _ = evidence.purpose_decision(case)
        self.assertFalse(accepted)
        self.assertIn("purpose_path_not_compatible", reasons)

    def test_05_positivity_rejects_wrong_sign(self):
        case = canonical("V6431-P02")
        case["coefficient"] = -0.1
        accepted, reasons, _ = evidence.positivity_decision(case)
        self.assertFalse(accepted)
        self.assertIn("non_positive_forward_coefficient", reasons)

    def test_06_covariate_rejects_support_gap(self):
        case = canonical("V6431-P03")
        case["target_support"] = [-0.1, 0.9]
        accepted, reasons, _ = evidence.covariate_decision(case)
        self.assertFalse(accepted)
        self.assertIn("target_support_outside_source_support", reasons)

    def test_07_rater_rejects_post_decode_calibration(self):
        case = canonical("V6431-P04")
        case["decoded_before_calibration"] = True
        accepted, reasons, _ = evidence.rater_decision(case)
        self.assertFalse(accepted)
        self.assertIn("post_decode_calibration", reasons)

    def test_08_pairwise_rejects_key_reuse(self):
        case = canonical("V6431-P05")
        case["relationships"][1]["verification_method"] = case["relationships"][0]["verification_method"]
        accepted, reasons, _ = evidence.pairwise_decision(case)
        self.assertFalse(accepted)
        self.assertIn("verification_material_correlates_relationships", reasons)

    def test_09_appeal_rejects_clock_without_notice(self):
        case = canonical("V6431-P06")
        case["clock_started"] = True
        accepted, reasons, _ = evidence.appeal_decision(case)
        self.assertFalse(accepted)
        self.assertIn("clock_started_without_notice", reasons)

    def test_10_parser_rejects_semantic_disagreement(self):
        case = canonical("V6431-P07")
        case["parser_outputs"] = ["one", "two"]
        accepted, reasons, _ = evidence.parser_decision(case)
        self.assertFalse(accepted)
        self.assertIn("parser_semantic_disagreement", reasons)

    def test_11_archive_is_order_independent_and_rejects_metadata_drift(self):
        a = evidence.deterministic_tar([("b", b"2"), ("a", b"1")])
        b = evidence.deterministic_tar([("a", b"1"), ("b", b"2")])
        self.assertEqual(a, b)
        case = canonical("V6431-P08")
        case["canonical_timestamps"] = False
        self.assertFalse(evidence.archive_decision(case)[0])

    def test_12_landauer_bound_is_typed_and_not_observed(self):
        case = canonical("V6431-P09")
        accepted, reasons, details = evidence.landauer_decision(case)
        self.assertTrue(accepted, reasons)
        self.assertTrue(math.isclose(details["conditional_lower_bound_joule"], 1.380649e-23 * 300 * math.log(2)))
        case["psyche_energy_claim"] = True
        self.assertFalse(evidence.landauer_decision(case)[0])

    def test_13_stage20_rejects_ready_promotion(self):
        case = canonical("V6431-P10")
        case["terminal_verdict"] = "READY_FOR_STAGE_20"
        accepted, reasons, _ = evidence.stage20_decision(case)
        self.assertFalse(accepted)
        self.assertIn("terminal_abstention_not_preserved", reasons)

    def test_14_constants_pin_source_and_x1(self):
        self.assertEqual(evidence.SOURCE_COMMIT, "259c46f80b9293723914bec49003280f20637e45")
        self.assertEqual(evidence.X1_COMMIT, "c64271e3bfb16a9fa0173d5901903bf967beb65f")

    def test_15_manifest_contract_has_sixty_unique_paths(self):
        proposals = read("x1-proposals.json")["proposals"]
        paths = evidence.manifest_paths(proposals)
        self.assertEqual(len(paths), 60)
        self.assertEqual(len(set(paths)), 60)

    def test_16_generated_ledgers_and_negative_floor(self):
        ledger = read("x2-proposal-ledger.json")
        negatives = read("retained-negative-register.json")
        self.assertEqual((ledger["case_count"], ledger["synthetic_rejection_count"]), (80, 70))
        self.assertEqual(negatives["negative_count"], 474)
        self.assertEqual(negatives["new_operational_count"], 3)
        self.assertTrue(negatives["all_retained"])

    def test_17_exact_gate_counts_and_terminal_verdict(self):
        gates = read("exact-open-gate-register.json")
        truth = read("phase-truth.json")
        self.assertEqual((gates["open_gap_count"], gates["exact_gate_count"]), (5, 6))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_18_static_report_structure(self):
        report = (PHASE / "deliverables/v643-v1-rights-resilience-report.html").read_text(encoding="utf-8")
        for marker in ('<html lang="en-NZ">', 'Skip to main content', '<main id="main">', '<caption>', 'NOT_READY_FOR_STAGE_20'):
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
