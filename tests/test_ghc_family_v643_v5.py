from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PHASE = ROOT / "docs/tamar-vey/v643-v5"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


evidence = load_module("ghc_family_v643_v5_evidence_tests", "ghc_family_v643_v5_evidence.py")
validator = load_module("ghc_family_v643_v5_validator_tests", "ghc_family_v643_v5_validator.py")
minimal = load_module("ghc_family_v643_v5_minimal_tests", "ghc_family_v643_v5_minimal.py")


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def canonical(proposal_id: str) -> dict:
    return copy.deepcopy(evidence.canonical_inputs()[proposal_id])


class TestGhcFamilyV643V5(unittest.TestCase):
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

    def test_04_registry_graph_rejects_omitted_outcome_promotion(self):
        case = canonical("V6435-P01")
        case["omitted_outcome_promoted"] = True
        accepted, reasons, _ = evidence.DECISIONS["V6435-P01"](case)
        self.assertFalse(accepted)
        self.assertIn("omitted_outcome_promoted_forbidden", reasons)

    def test_05_gmut_obligation_rejects_global_claim(self):
        case = canonical("V6435-P02")
        case["global_existence_claim"] = True
        self.assertFalse(evidence.DECISIONS["V6435-P02"](case)[0])

    def test_06_nonregular_likelihood_rejects_real_row_invention(self):
        case = canonical("V6435-P03")
        case["real_rows"] = 1
        self.assertFalse(evidence.DECISIONS["V6435-P03"](case)[0])

    def test_07_thos_control_rejects_superiority_claim(self):
        case = canonical("V6435-P04")
        case["superiority_claim"] = True
        self.assertFalse(evidence.DECISIONS["V6435-P04"](case)[0])

    def test_08_freed_id_sync_rejects_production_claim(self):
        case = canonical("V6435-P05")
        case["production_claim"] = True
        self.assertFalse(evidence.DECISIONS["V6435-P05"](case)[0])

    def test_09_cbr_hold_stays_pending_exact_authority(self):
        accepted, reasons, details = evidence.DECISIONS["V6435-P06"](canonical("V6435-P06"))
        self.assertTrue(accepted, reasons)
        self.assertEqual(details["state"], "pending_exact_authority")
        case = canonical("V6435-P06")
        case["repository_legal_hold"] = True
        self.assertFalse(evidence.DECISIONS["V6435-P06"](case)[0])

    def test_10_complexity_harness_rejects_exhaustive_security(self):
        case = canonical("V6435-P07")
        case["exhaustive_security_claim"] = True
        self.assertFalse(evidence.DECISIONS["V6435-P07"](case)[0])

    def test_11_timing_harness_rejects_constant_time_assurance(self):
        case = canonical("V6435-P08")
        case["constant_time_assurance_claim"] = True
        self.assertFalse(evidence.DECISIONS["V6435-P08"](case)[0])

    def test_12_thermo_classifier_rejects_false_equilibrium(self):
        case = canonical("V6435-P09")
        case["equilibrium_if_current_nonzero"] = True
        self.assertFalse(evidence.DECISIONS["V6435-P09"](case)[0])

    def test_13_stage20_board_rejects_pass_overclaim(self):
        case = canonical("V6435-P10")
        case["stage20_pass_claim"] = True
        self.assertFalse(evidence.DECISIONS["V6435-P10"](case)[0])

    def test_14_canonical_cases_are_bounded(self):
        for pid, case in evidence.canonical_inputs().items():
            accepted, reasons, _ = evidence.DECISIONS[pid](case)
            self.assertTrue(accepted, (pid, reasons))

    def test_15_x1_content_seal(self):
        seal = read("reproduction/x1-content-seal.json")
        self.assertEqual(seal["x1_commit"], evidence.X1_COMMIT)
        self.assertEqual(seal["entry_count"], 30)
        self.assertTrue(seal["all_unchanged"])

    def test_16_retained_negative_floor_and_exact_count(self):
        negatives = read("retained-negative-register.json")
        expected = 721 + 14 + 70 + len(evidence.X2_OPERATIONAL_NEGATIVES)
        self.assertEqual(negatives["negative_count"], expected)
        self.assertEqual(len(negatives["negatives"]), expected)
        self.assertTrue(negatives["all_retained"])

    def test_17_inherited_negatives_preserved_exactly(self):
        current = read("retained-negative-register.json")["negatives"][:721]
        inherited = json.loads((ROOT / "docs/orin-thale/v643-v4/retained-negative-register.json").read_text(encoding="utf-8"))["negatives"]
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

    def test_21_manifest_parity(self):
        manifest = read("reproduction/manifest.json")
        self.assertGreater(manifest["entry_count"], 0)
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            target = ROOT / row["repo_path"]
            self.assertTrue(target.is_file(), row["repo_path"])
            self.assertEqual(evidence.normalized_sha256(target), row["sha256_lf_normalized"])

    def test_22_static_report_boundaries(self):
        report = (PHASE / "deliverables/v643-v5-boundary-evidence-report.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="en-NZ">', report)
        self.assertIn("Māori", report)
        self.assertIn("NOT_READY_FOR_STAGE_20", report)
        self.assertNotIn("<script", report.casefold())

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
