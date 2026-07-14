from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PHASE = ROOT / "docs/orin-thale/v643-v4"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


evidence = load_module("ghc_family_boundary_evidence", "ghc_family_boundary_evidence.py")
validator = load_module("ghc_family_boundary_evidence_validator", "ghc_family_boundary_evidence_validator.py")
minimal = load_module("ghc_family_boundary_evidence_minimal", "ghc_family_boundary_evidence_minimal.py")


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def canonical(proposal_id: str) -> dict:
    return copy.deepcopy(evidence.canonical_inputs()[proposal_id])


class TestGhcFamilyV643V4(unittest.TestCase):
    def test_01_frozen_distribution(self):
        distribution = {label: list(evidence.OBSERVED.values()).count(label) for label in evidence.TRUTH_LABELS}
        self.assertEqual(distribution, {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})

    def test_02_ten_groups_eighty_cases(self):
        groups = evidence.fixture_catalog()
        self.assertEqual(len(groups), 10)
        self.assertEqual(sum(len(rows) for rows in groups.values()), 80)

    def test_03_all_expectations_match_and_seventy_reject(self):
        evaluated = evidence.evaluate_catalog()
        self.assertTrue(all(row["matched_expectation"] for rows in evaluated.values() for row in rows))
        self.assertEqual(sum(not row["accepted"] for rows in evaluated.values() for row in rows), 70)

    def test_04_correction_rejects_stale_promotion(self):
        case = canonical("V6434-P01")
        case["stale_claim_promoted"] = True
        accepted, reasons, _ = evidence.correction_decision(case)
        self.assertFalse(accepted)
        self.assertIn("stale_downstream_claim_promoted", reasons)

    def test_05_wellposedness_rejects_missing_continuous_dependence(self):
        case = canonical("V6434-P02")
        case["continuous_dependence_obligation_recorded"] = False
        self.assertFalse(evidence.wellposedness_decision(case)[0])

    def test_06_mnar_rejects_empirical_overclaim(self):
        case = canonical("V6434-P03")
        case["empirical_confirmation_claim"] = True
        self.assertFalse(evidence.mnar_decision(case)[0])

    def test_07_mediation_rejects_post_treatment_erasure(self):
        case = canonical("V6434-P04")
        case["post_treatment_confounding_erased"] = True
        self.assertFalse(evidence.mediation_decision(case)[0])

    def test_08_facilitator_accepts_only_open_gap(self):
        accepted, reasons, details = evidence.facilitator_decision(canonical("V6434-P05"))
        self.assertTrue(accepted, reasons)
        self.assertEqual(details["gap_state"], "open")
        case = canonical("V6434-P05")
        case["learning_curve_estimated"] = True
        self.assertFalse(evidence.facilitator_decision(case)[0])

    def test_09_delegation_rejects_cycle(self):
        case = canonical("V6434-P06")
        case["acyclic"] = False
        self.assertFalse(evidence.delegation_decision(case)[0])

    def test_10_confidentiality_accepts_only_pending_gate(self):
        accepted, reasons, details = evidence.confidentiality_decision(canonical("V6434-P07"))
        self.assertTrue(accepted, reasons)
        self.assertEqual(details["state"], "pending_exact_authority")
        case = canonical("V6434-P07")
        case["maori_authority_or_wording_claim"] = True
        self.assertFalse(evidence.confidentiality_decision(case)[0])

    def test_11_canonicalization_rejects_duplicate_names(self):
        case = canonical("V6434-P08")
        case["duplicate_member_names"] = True
        self.assertFalse(evidence.canonicalization_decision(case)[0])

    def test_12_floating_rejects_cross_architecture_overclaim(self):
        case = canonical("V6434-P09")
        case["cross_architecture_parity_claim"] = True
        self.assertFalse(evidence.floating_environment_decision(case)[0])

    def test_13_coarse_graining_rejects_memory_erasure(self):
        case = canonical("V6434-P10")
        case["memory_effects_retained"] = False
        self.assertFalse(evidence.coarse_graining_decision(case)[0])

    def test_14_canonical_cases_are_bounded(self):
        for pid, case in evidence.canonical_inputs().items():
            accepted, reasons, _ = evidence.DECISIONS[pid](case)
            self.assertTrue(accepted, (pid, reasons))

    def test_15_x1_content_seal(self):
        seal = read("reproduction/x1-content-seal.json")
        self.assertEqual(seal["x1_commit"], evidence.X1_COMMIT)
        self.assertEqual(seal["entry_count"], 27)
        self.assertTrue(seal["all_unchanged"])

    def test_16_retained_negative_floor_and_exact_count(self):
        negatives = read("retained-negative-register.json")
        expected = 637 + 70 + 7 + len(evidence.X2_OPERATIONAL_NEGATIVES)
        self.assertEqual(negatives["negative_count"], expected)
        self.assertEqual(len(negatives["negatives"]), expected)
        self.assertTrue(negatives["all_retained"])

    def test_17_inherited_negatives_preserved_exactly(self):
        current = read("retained-negative-register.json")["negatives"][:637]
        inherited = json.loads((ROOT / "docs/sable-rook/v643-v3/retained-negative-register.json").read_text(encoding="utf-8"))["negatives"]
        self.assertEqual(current, inherited)

    def test_18_phase_truth_boundaries(self):
        truth = read("phase-truth.json")
        self.assertEqual(truth["primary_focus"], "GMUT Mind")
        self.assertTrue(all(value is False for value in truth["protected_claims"].values()))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["outbound_message_count"], 0)

    def test_19_five_open_and_six_exact_gates(self):
        gates = read("exact-open-gate-register.json")
        self.assertEqual((gates["open_gap_count"], gates["exact_gate_count"]), (5, 6))
        self.assertIn("Māori", json.dumps(gates, ensure_ascii=False))

    def test_20_no_external_claims_established(self):
        ledger = read("x2-proposal-ledger.json")
        self.assertTrue(all(row["external_claims_established"] == [] for row in ledger["proposals"]))

    def test_21_manifest_exact_and_parity(self):
        manifest = read("reproduction/manifest.json")
        self.assertEqual(manifest["entry_count"], 77)
        self.assertEqual(len(manifest["entries"]), 77)
        for row in manifest["entries"]:
            target = ROOT / row["repo_path"]
            self.assertTrue(target.is_file(), row["repo_path"])
            self.assertEqual(evidence.normalized_sha256(target), row["sha256_lf_normalized"])

    def test_22_static_report_boundaries(self):
        report = (PHASE / "deliverables/v643-v4-boundary-evidence-report.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="en-NZ">', report)
        self.assertIn("Māori", report)
        self.assertNotIn("MÄori", report)
        self.assertIn("NOT_READY_FOR_STAGE_20", report)

    def test_23_stage20_veto(self):
        board = read("stage20/domain-veto-evidence-board.json")
        self.assertFalse(board["compensation_across_domains_allowed"])
        self.assertTrue(all(row["decision"] == "veto" for row in board["vetoes"]))

    def test_24_detailed_validator_pending_snapshot(self):
        result = validator.validate(ROOT, PHASE, allow_pending_snapshot=True)
        self.assertTrue(result["valid"], result["issues"])

    def test_25_minimal_validator_pending_snapshot(self):
        result = minimal.verify(PHASE, allow_pending_snapshot=True)
        self.assertTrue(result["valid"], result["issues"])


if __name__ == "__main__":
    unittest.main()
