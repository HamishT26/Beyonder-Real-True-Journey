from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PHASE = ROOT / "docs/tamar-vey/v644-v3"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_v644_v3_evidence as evidence  # noqa: E402
import ghc_family_v644_v3_minimal as minimal  # noqa: E402
import ghc_family_v644_v3_model as model  # noqa: E402
import ghc_family_v644_v3_validator as validator  # noqa: E402
from ghc_family_v644_v3_x1_definitions import PROPOSALS  # noqa: E402


def read(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TestGhcFamilyV644V3(unittest.TestCase):
    def test_01_exact_distribution(self):
        outcomes = [spec["outcome"] for spec in model.SPECS.values()]
        self.assertEqual(
            {label: outcomes.count(label) for label in ("completed", "represented", "open_gap", "exact_gate")},
            {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        )

    def test_02_ten_groups_eighty_cases(self):
        groups = model.all_cases()
        self.assertEqual(len(groups), 10)
        self.assertEqual(sum(1 + len(group["mutations"]) for group in groups.values()), 80)

    def test_03_controls_match_frozen_outcomes(self):
        for proposal_id, group in model.all_cases().items():
            self.assertEqual(group["control"]["evaluation"]["decision"], model.SPECS[proposal_id]["outcome"])

    def test_04_seventy_mutations_rejected_and_retained(self):
        mutations = [row for group in model.all_cases().values() for row in group["mutations"]]
        self.assertEqual(len(mutations), 70)
        self.assertTrue(all(row["evaluation"]["decision"] == "rejected" and row["retained"] for row in mutations))

    def test_05_missing_field_rejected(self):
        proposal_id = "V6443-P01"
        record = copy.deepcopy(model.SPECS[proposal_id]["control"])
        del record["input_columns"]
        self.assertEqual(model.evaluate_record(proposal_id, record)["decision"], "rejected")

    def test_06_unexpected_field_rejected(self):
        proposal_id = "V6443-P02"
        record = copy.deepcopy(model.SPECS[proposal_id]["control"])
        record["hidden_promotion"] = True
        self.assertEqual(model.evaluate_record(proposal_id, record)["decision"], "rejected")

    def test_07_solar_system_control_stays_open_gap(self):
        group = model.build_cases("V6443-P03")
        self.assertEqual(group["control"]["evaluation"]["decision"], "open_gap")
        self.assertEqual(group["control"]["record"]["eligible_rows"], "zero_frozen_observation_rows")

    def test_08_thos_control_stays_proxy(self):
        group = model.build_cases("V6443-P04")
        self.assertEqual(group["control"]["evaluation"]["decision"], "represented")
        self.assertEqual(group["control"]["record"]["real_arm_count"], 0)

    def test_09_freed_id_control_stays_proxy(self):
        group = model.build_cases("V6443-P05")
        self.assertEqual(group["control"]["evaluation"]["decision"], "represented")
        self.assertEqual(group["control"]["record"]["claim_class"], "structural_proxy_only")

    def test_10_remedy_control_stays_exact_gate(self):
        group = model.build_cases("V6443-P06")
        self.assertEqual(group["control"]["evaluation"]["decision"], "exact_gate")
        self.assertEqual(group["control"]["record"]["authority_evidence"], "absent_exact_participation")

    def test_11_response_file_mutation_rejected(self):
        group = model.build_cases("V6443-P07")
        traversal = next(row for row in group["mutations"] if row["mutated_field"] == "parent_traversal")
        self.assertEqual(traversal["evaluation"]["decision"], "rejected")

    def test_12_accessibility_promotion_rejected(self):
        group = model.build_cases("V6443-P08")
        claim = next(row for row in group["mutations"] if row["mutated_field"] == "claim_class")
        self.assertEqual(claim["evaluation"]["decision"], "rejected")

    def test_13_psyche_law_promotion_rejected(self):
        group = model.build_cases("V6443-P09")
        claim = next(row for row in group["mutations"] if row["mutated_field"] == "claim_class")
        self.assertEqual(claim["evaluation"]["decision"], "rejected")

    def test_14_alpha_reuse_rejected(self):
        group = model.build_cases("V6443-P10")
        allocation = next(row for row in group["mutations"] if row["mutated_field"] == "alpha_allocation")
        self.assertEqual(allocation["evaluation"]["decision"], "rejected")

    def test_15_preregistration_has_required_fields(self):
        required = {
            "hypothesis", "null_or_failure", "approval_class", "execution_lane",
            "authoritative_source_needs", "deliverables", "test_falsifier_or_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
        }
        self.assertEqual(len(PROPOSALS), 10)
        self.assertTrue(all(required <= set(row) for row in PROPOSALS))

    def test_16_x1_content_seal(self):
        seal = read("reproduction/x1-content-seal.json")
        self.assertEqual(seal["x1_commit"], evidence.X1_COMMIT)
        self.assertEqual(seal["file_count"], 27)
        self.assertTrue(seal["all_current_blobs_unchanged"])

    def test_17_retained_negative_exact_count(self):
        negatives = read("retained-negative-register.json")
        self.assertEqual(negatives["negative_count"], 1296 + negatives["x2_operational_count"])
        self.assertEqual(len(negatives["negatives"]), negatives["negative_count"])
        self.assertTrue(negatives["all_retained"])

    def test_18_inherited_negatives_preserved_exactly(self):
        inherited = json.loads((ROOT / "docs/orin-thale/v644-v2/retained-negative-register.json").read_text(encoding="utf-8"))["negatives"]
        self.assertEqual(read("retained-negative-register.json")["negatives"][:1220], inherited)

    def test_19_phase_truth_boundaries(self):
        truth = read("phase-truth.json")
        self.assertEqual(truth["primary_focus"], "GMUT Mind")
        self.assertTrue(all(value is False for value in truth["protected_claims"].values()))
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertEqual(truth["outbound_message_count"], 0)

    def test_20_five_open_and_six_exact_gates(self):
        gates = read("exact-open-gate-register.json")
        self.assertEqual((gates["open_gap_count"], gates["exact_gate_count"]), (5, 6))
        self.assertIn("Māori", json.dumps(gates, ensure_ascii=False))

    def test_21_manifest_parity(self):
        manifest = read("reproduction/manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for row in manifest["entries"]:
            target = ROOT / row["path"]
            self.assertTrue(target.is_file(), row["path"])
            self.assertEqual(evidence.normalized_sha256(target), row["sha256_lf_normalized"])

    def test_22_static_report_boundaries(self):
        report = (PHASE / "deliverables/v644-v3-boundary-evidence-report.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="en">', report)
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
