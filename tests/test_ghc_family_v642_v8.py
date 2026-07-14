from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PHASE = ROOT / "docs/sylven-arc/v642-v8"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


evidence = load_module("ghc_family_evidence_contract", "ghc_family_evidence_contract.py")
validator = load_module("ghc_family_evidence_contract_validator", "ghc_family_evidence_contract_validator.py")
minimal = load_module("ghc_family_evidence_contract_minimal", "ghc_family_evidence_contract_minimal.py")


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def canonical(proposal_id: str) -> dict:
    return copy.deepcopy(evidence.fixture_catalog()[proposal_id][0]["input"])


class TestGhcFamilyV642V8(unittest.TestCase):
    def test_01_frozen_observed_distribution(self):
        distribution = {label: list(evidence.OBSERVED.values()).count(label) for label in evidence.TRUTH_LABELS}
        self.assertEqual(distribution, {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})

    def test_02_exactly_ten_groups_and_eighty_cases(self):
        groups = evidence.fixture_catalog()
        self.assertEqual(len(groups), 10)
        self.assertEqual(sum(len(rows) for rows in groups.values()), 80)

    def test_03_all_preregistered_cases_match(self):
        evaluated = evidence.evaluate_catalog()
        self.assertTrue(all(row["matched_expectation"] for rows in evaluated.values() for row in rows))
        self.assertEqual(sum(not row["accepted"] for rows in evaluated.values() for row in rows), 70)

    def test_04_transparency_rejects_root_mismatch(self):
        case = canonical("V6428-P01")
        case["declared_previous_root"] = "0" * 64
        accepted, reasons, _ = evidence.transparency_decision(case)
        self.assertFalse(accepted)
        self.assertIn("previous_root_mismatch", reasons)

    def test_05_operator_basis_rejects_false_collapse(self):
        case = canonical("V6428-P02")
        case["false_collapse"] = True
        accepted, reasons, _ = evidence.operator_basis_decision(case)
        self.assertFalse(accepted)
        self.assertIn("inequivalent_operators_collapsed", reasons)

    def test_06_cutoff_rejects_empirical_promotion(self):
        case = canonical("V6428-P03")
        case["empirical_promotion"] = True
        accepted, reasons, _ = evidence.cutoff_decision(case)
        self.assertFalse(accepted)
        self.assertIn("synthetic_remainder_promoted_to_empirical_result", reasons)

    def test_07_instrument_rejects_scoring_drift(self):
        case = canonical("V6428-P04")
        case["scoring_key_after"] = "changed"
        accepted, reasons, _ = evidence.instrument_decision(case)
        self.assertFalse(accepted)
        self.assertIn("scoring_key_drift", reasons)

    def test_08_freed_id_rejects_replay(self):
        case = canonical("V6428-P05")
        case["used_challenges"] = [case["challenge"]]
        accepted, reasons, _ = evidence.freed_id_decision(case)
        self.assertFalse(accepted)
        self.assertIn("challenge_replay", reasons)

    def test_09_evidence_state_rejects_authority_substitution(self):
        case = canonical("V6428-P06")
        case["authority_substitution"] = True
        accepted, reasons, _ = evidence.evidence_state_decision(case)
        self.assertFalse(accepted)
        self.assertIn("technical_output_substituted_for_authority", reasons)

    def test_10_identifier_rejects_confusable(self):
        case = canonical("V6428-P07")
        case["identifier"] = "ph\u0430se-v642-v8"
        accepted, reasons, _ = evidence.identifier_decision(case)
        self.assertFalse(accepted)
        self.assertIn("confusable_skeleton_collision", reasons)

    def test_11_float_contract_rejects_nonfinite(self):
        case = canonical("V6428-P08")
        case["tokens"] = ["nan"]
        accepted, reasons, _ = evidence.float_decision(case)
        self.assertFalse(accepted)
        self.assertIn("non_finite_value_in_finite_contract", reasons)

    def test_12_path_contract_rejects_analogy_promotion(self):
        case = canonical("V6428-P09")
        case["consciousness_claim"] = True
        accepted, reasons, _ = evidence.path_dependence_decision(case)
        self.assertFalse(accepted)
        self.assertIn("analogy_promoted_to_consciousness_evidence", reasons)

    def test_13_reversibility_rejects_external_action(self):
        case = canonical("V6428-P10")
        case["deployment"] = True
        accepted, reasons, _ = evidence.reversibility_decision(case)
        self.assertFalse(accepted)
        self.assertIn("exact_gated_action_present", reasons)

    def test_14_merkle_root_is_deterministic_and_order_sensitive(self):
        events = [{"id": "a", "value": 1}, {"id": "b", "value": 2}]
        self.assertEqual(evidence.merkle_root(events), evidence.merkle_root(copy.deepcopy(events)))
        self.assertNotEqual(evidence.merkle_root(events), evidence.merkle_root(list(reversed(events))))

    def test_15_identifier_skeleton_is_nfkc_and_confusable_aware(self):
        self.assertEqual(evidence.identifier_skeleton("ＰHАSE"), evidence.identifier_skeleton("phase"))

    def test_16_constants_pin_source_and_x1(self):
        self.assertEqual(evidence.SOURCE_COMMIT, "79ee1b9e9b68bb6dc657a53ce1550c0ec2586f36")
        self.assertEqual(evidence.X1_COMMIT, "644210d1971e5475b308c288e202c986263a1da5")

    def test_17_manifest_contract_has_sixty_unique_paths(self):
        proposals = read("x1-proposals.json")["proposals"]
        paths = evidence.manifest_paths(proposals)
        self.assertEqual(len(paths), 60)
        self.assertEqual(len(set(paths)), 60)

    def test_18_generated_ledgers_and_negative_floor(self):
        ledger = read("x2-proposal-ledger.json")
        negatives = read("retained-negative-register.json")
        self.assertEqual((ledger["case_count"], ledger["synthetic_rejection_count"]), (80, 70))
        self.assertGreaterEqual(negatives["negative_count"], 393)
        self.assertTrue(negatives["all_retained"])

    def test_19_full_validator_pending_snapshot(self):
        result = validator.validate(ROOT, PHASE, allow_pending_snapshot=True)
        self.assertTrue(result["valid"], result["issues"])

    def test_20_minimal_validator_pending_snapshot(self):
        result = minimal.verify(PHASE, allow_pending_snapshot=True)
        self.assertTrue(result["valid"], result["checks"])


if __name__ == "__main__":
    unittest.main()
