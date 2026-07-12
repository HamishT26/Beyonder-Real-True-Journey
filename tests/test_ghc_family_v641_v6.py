from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v641-v6"


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


class TerminalX1AndProvenanceTests(unittest.TestCase):
    def test_01_x1_has_ten_unique_proposals(self):
        data = load("x1-proposals.json")
        self.assertEqual(len(data["proposals"]), 10)
        self.assertEqual(len({row["proposal_id"] for row in data["proposals"]}), 10)
        self.assertEqual(data["prior_proposal_count"], 40)

    def test_02_source_statuses_reconcile(self):
        data = load("sources/source-ledger.json")
        counts = {key: sum(row["status_class"] == key for row in data["sources"]) for key in ["current", "stable", "draft", "watch"]}
        self.assertEqual(counts, data["status_counts"])
        self.assertEqual(counts, {"current": 13, "stable": 10, "draft": 2, "watch": 1})

    def test_03_x1_validation_is_clean_and_pre_x2(self):
        data = load("validation/x1-validation.json")
        self.assertTrue(data["valid"])
        self.assertEqual(data["issues"], [])
        self.assertFalse(data["sequence_integrity"]["x2_authorized_before_equality"])

    def test_04_sequential_ancestry_is_strict(self):
        data = load("provenance/sequential-ancestry.json")
        self.assertTrue(data["all_edges_strict"])
        self.assertTrue(all(row["strict_ancestor"] for row in data["edges"]))
        self.assertFalse(data["parallel_execution_inferred"])

    def test_05_prior_x1_x2_boundaries_hold(self):
        data = load("provenance/x1-x2-boundary-audit.json")
        self.assertTrue(data["completed_prior_boundaries_valid"])
        self.assertTrue(data["v6_x2_started_only_after_x1_equality"])


class TerminalMindAndFalsificationTests(unittest.TestCase):
    def test_06_equation_covenant_is_bounded(self):
        data = load("physics/equation-register-covenant.json")
        self.assertFalse(data["canonical"]["unique_prediction_established"])
        self.assertFalse(data["canonical"]["consciousness_tensor_present"])
        self.assertIn("effective_field_theory", data["canonical"]["status"])

    def test_07_translation_typecheck_rejects_category_jumps(self):
        data = load("physics/translation-typecheck.json")
        self.assertTrue(data["all_category_barriers_hold"])
        self.assertEqual(data["unexpected_acceptances"], 0)

    def test_08_null_limits_do_not_claim_empirical_validation(self):
        data = load("physics/null-limit-and-conservation-audit.json")
        self.assertTrue(all(row["pass"] for row in data["null_limits"]))
        self.assertFalse(data["empirical_validation_supplied"])
        self.assertFalse(data["full_dynamical_proof_supplied"])

    def test_09_inherited_and_v6_negatives_survive(self):
        data = load("falsification/inherited-negative-register.json")
        inherited = {"REPRO-V4-N01", "REPRO-V4-N02", "VALID-V5-N01", "VALID-V5-N02", "COMPAT-V5-N03", "CLI-V5-N04", "REPRO-V5-N05"}
        self.assertEqual(data["negative_count"], 9)
        self.assertEqual(len(set(data["negative_ids"])), 9)
        self.assertTrue(inherited <= set(data["negative_ids"]))
        self.assertTrue(data["all_retained"])

    def test_10_negative_mutations_are_rejected(self):
        data = load("falsification/mutation-tribunal.json")
        self.assertEqual(data["mutation_count"], 9)
        self.assertTrue(data["all_expected_rejections_observed"])


class TerminalBodyHeartAndLawTests(unittest.TestCase):
    def test_11_empirical_promotion_remains_open(self):
        data = load("empirical/promotion-docket.json")
        self.assertFalse(data["promotion_authorized"])
        self.assertFalse(data["gmute_confirmation"])
        self.assertEqual(data["requirements_met"], 0)

    def test_12_thos_remains_represented(self):
        data = load("thos/blind-evidence-audit.json")
        self.assertEqual(data["disposition"], "represented")
        self.assertFalse(data["matched_budget_real_arms"])
        self.assertFalse(data["independent_review"])

    def test_13_thermo_psyche_has_no_new_fundamental_law(self):
        data = load("thermo-psyche/candidate-register.json")
        self.assertEqual(data["candidate_count"], 7)
        self.assertEqual(data["fundamental_physical_laws_established"], 0)
        self.assertTrue(all(row["physical_law"] is False for row in data["candidates"]))

    def test_14_freed_id_non_escalation_holds(self):
        lattice = load("freed-id/assurance-lattice.json")
        proof = load("freed-id/non-escalation-proof.json")
        self.assertEqual(lattice["current_highest_level"], "L1_structural")
        self.assertEqual(lattice["current_disposition"], "open_gap")
        self.assertTrue(proof["proof_pass"])

    def test_15_cbr_empty_chair_veto_holds(self):
        matrix = load("cbr/authority-matrix.json")
        veto = load("cbr/empty-chair-veto.json")
        self.assertEqual(matrix["disposition"], "exact_gate")
        self.assertFalse(matrix["enactment_authorized"])
        self.assertTrue(veto["veto_active"])
        self.assertFalse(veto["Māori_authority_present"])


class TerminalAssuranceAndBoardTests(unittest.TestCase):
    def test_16_reproduction_scope_is_not_independent(self):
        data = load("reproduction/reproduction-report.json")
        self.assertFalse(data["independent_scientific_reproduction"])
        self.assertIn(data["state"], {"pending_clean_snapshots", "cross_owner_internal_repeatability_verified"})

    def test_17_ledger_distribution_matches_reproduction_state(self):
        ledger = load("x2-proposal-ledger.json")
        reproduction = load("reproduction/reproduction-report.json")
        expected = ({"completed": 6, "represented": 1, "open_gap": 2, "exact_gate": 1} if reproduction["state"] == "cross_owner_internal_repeatability_verified" else {"completed": 5, "represented": 1, "open_gap": 3, "exact_gate": 1})
        self.assertEqual(ledger["disposition_counts"], expected)

    def test_18_stage20_is_not_ready_and_protected_claims_false(self):
        data = load("stage20/terminal-evidence-board.json")
        self.assertEqual(data["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertTrue(all(value is False for value in data["protected_claims"].values()))

    def test_19_static_report_and_accessibility_audit(self):
        report = (PHASE / "deliverables/v641-v6-terminal-evidence-report.html").read_text(encoding="utf-8")
        audit = load("validation/accessibility-audit.json")
        self.assertIn('<html lang="en">', report)
        self.assertIn('<main id="main">', report)
        self.assertTrue(audit["valid"])
        self.assertFalse(audit["full_wcag_conformance_established"])

    def test_20_privacy_tests_and_overview_boundaries(self):
        privacy = load("validation/privacy-scan.json")
        receipt = load("validation/test-receipt.json")
        overview = (PHASE / "v641-v6-integrated-overview.md").read_text(encoding="utf-8")
        words = len(re.findall(r"\b\w+[\w'-]*\b", overview))
        self.assertTrue(privacy["valid"])
        self.assertEqual(privacy["hit_count"], 0)
        self.assertEqual(receipt["failed"], 0)
        self.assertGreaterEqual(receipt["passed"], 100)
        self.assertGreaterEqual(words, 2000)


if __name__ == "__main__":
    unittest.main()
