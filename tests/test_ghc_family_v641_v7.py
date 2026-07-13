from __future__ import annotations

import importlib.util
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v641-v7"


def load(rel: str) -> dict:
    return json.loads((PHASE / rel).read_text(encoding="utf-8"))


class TestGhcFamilyV641V7(unittest.TestCase):
    def test_01_x1_has_exactly_ten_complete_records(self) -> None:
        data = load("x1-proposals.json")
        required = {"hypothesis","null_or_failure","approval_class","execution_lane","authoritative_source_needs","deliverables","test_falsifier_or_gate","rollback_or_recovery","expected_disposition"}
        self.assertEqual(data["proposal_count"], 10)
        self.assertEqual(len(data["proposals"]), 10)
        self.assertTrue(all(required <= set(row) for row in data["proposals"]))

    def test_02_x1_is_frozen_before_x2_and_novelty_audited(self) -> None:
        data = load("x1-proposals.json")
        audit = load("provenance/prior-proposal-collision-audit.json")
        self.assertIn("No x2 outcome work", data["x1_freeze_rule"])
        self.assertEqual(audit["prior_phase_counts"]["total"], 50)
        self.assertEqual(audit["exact_title_collisions"], 0)
        self.assertTrue(all(row["distinct"] for row in audit["checks"]))

    def test_03_source_ledger_preserves_status_classes(self) -> None:
        data = load("sources/source-ledger.json")
        self.assertEqual(data["source_count"], 31)
        self.assertEqual(Counter(row["status_class"] for row in data["sources"]), Counter(data["status_counts"]))
        self.assertEqual(set(data["allowed_status_classes"]), {"current","stable","draft","watch"})

    def test_04_frozen_chain_contains_sixty_unique_records(self) -> None:
        data = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(data["proposal_count"], 60)
        self.assertEqual(data["version_counts"], {"v2":10,"v3":10,"v4":10,"v5":10,"v6":10,"v7":10})
        self.assertEqual(data["exact_duplicate_titles"], [])

    def test_05_authority_root_knockout_downgrades_fragile_claims(self) -> None:
        data = load("provenance/authority-root-knockout.json")
        self.assertTrue(data["pass"])
        self.assertEqual(data["unsafe_strength_retention_count"], 0)
        self.assertIn("downgrade_or_defer", {row["decision"] for row in data["mutations"]})

    def test_06_canonical_gmut_equations_and_nonclaims_are_exact(self) -> None:
        data = load("physics/canonical-gmut-register.json")
        self.assertEqual(data["equations"], [
            "G_{mu nu} + Lambda g_{mu nu} = M_Pl^{-2} T^{SM}_{mu nu} + Omega_{mu nu}",
            "Omega_{mu nu} = M_Pl^{-2} (T^phi_{mu nu} + T^{EFT}_{mu nu})",
        ])
        self.assertFalse(data["empirical_confirmation"])
        self.assertFalse(data["unique_prediction"])
        self.assertFalse(data["theory_of_everything"])

    def test_07_identifiability_rank_keeps_degeneracy_witnesses(self) -> None:
        data = load("physics/identifiability-rank-battery.json")
        self.assertTrue(data["all_expected_ranks_observed"])
        self.assertTrue(data["degeneracy_witnesses_retained"])
        self.assertFalse(data["empirical_identifiability_established"])
        self.assertTrue(any(not row["structurally_identifiable"] for row in data["fixtures"]))

    def test_08_conservation_and_stability_are_structural_only(self) -> None:
        data = load("physics/conservation-obligation-register.json")
        self.assertFalse(data["nature_claim"])
        self.assertEqual({row["classification"] for row in data["stability_fixtures"]}, {"locally_stable_toy","marginal_toy","unstable_toy"})
        self.assertTrue(any(not row["accepted"] for row in data["unit_checks"]))

    def test_09_empirical_adapter_has_real_metadata_and_zero_fit(self) -> None:
        handshake = load("empirical/official-metadata-handshake.json")
        receipt = load("empirical/no-fit-receipt.json")
        self.assertTrue(handshake["schema_adapter_executed_against_metadata_fixtures"])
        self.assertEqual(handshake["real_measurement_rows_parsed"], 0)
        self.assertFalse(receipt["likelihood_executed"])
        self.assertFalse(receipt["parameter_fit_executed"])
        self.assertEqual(receipt["disposition"], "represented")

    def test_10_thos_is_matched_budget_synthetic_proxy(self) -> None:
        packet = load("thos/outcome-sealed-arm-packet.json")
        sentinels = load("thos/exchangeability-sentinels.json")
        gap = load("thos/real-arm-gap.json")
        self.assertTrue(packet["synthetic_only"])
        self.assertEqual(packet["real_model_runs"], 0)
        self.assertTrue(sentinels["all_mutations_rejected_before_unseal"])
        self.assertFalse(gap["real_arms_present"])

    def test_11_freed_id_is_structural_and_open(self) -> None:
        matrix = load("freed-id/stable-draft-watch-conformance-matrix.json")
        faults = load("freed-id/resolution-status-fault-vectors.json")
        gap = load("freed-id/interoperability-trust-gap.json")
        self.assertEqual((matrix["stable_pin_count"], matrix["draft_or_watch_count"]), (4,3))
        self.assertFalse(matrix["production_assurance"])
        self.assertTrue(faults["all_faults_rejected"])
        self.assertEqual(gap["disposition"], "open_gap")

    def test_12_cbr_conflicts_are_exact_gated(self) -> None:
        casebook = load("cbr/rights-floor-precedence-casebook.json")
        maori = load("cbr/maori-authority-boundary.json")
        self.assertEqual(casebook["algorithmic_resolutions"], 0)
        self.assertTrue(casebook["all_live_conflicts_deferred"])
        self.assertFalse(maori["Māori_authority_present"])
        self.assertFalse(maori["system_may_speak_for_Māori"])
        self.assertEqual(maori["decision"], "exact_gate")

    def test_13_security_vectors_are_bounded_and_recoverable(self) -> None:
        vectors = load("security/adversarial-encoding-vectors.json")
        recovery = load("security/recovery-drill.json")
        controls = load("security/privacy-raw-id-controls.json")
        self.assertTrue(vectors["all_seeded_classes_detected"])
        self.assertFalse(vectors["exhaustive_security"])
        self.assertEqual(recovery["destructive_commands"], 0)
        self.assertFalse(recovery["privilege_expansion"])
        self.assertTrue(controls["pass"])

    def test_14_repeatability_keeps_independent_team_gap(self) -> None:
        budget = load("reproduction/common-mode-independence-budget.json")
        receipt = load("reproduction/repeatability-receipt.json")
        detached = load("reproduction/detached-snapshot-validation.json")
        gap = load("reproduction/independent-team-gap.json")
        self.assertGreaterEqual(len(budget["shared_dependencies"]), 5)
        self.assertFalse(budget["independent_team_reproduction"])
        self.assertFalse(receipt["independent_reproduction"])
        if receipt["state"] == "verified_same_owner_clean_snapshots":
            self.assertEqual(detached["normalized_hash_file_count"], 72)
            self.assertEqual(detached["mismatch_count"], 0)
        self.assertEqual(gap["gap"], "open")

    def test_15_thermo_psyche_has_exact_six_class_rubric(self) -> None:
        rubric = load("thermo-psyche/six-class-rubric.json")
        relabel = load("thermo-psyche/counterfactual-relabel-vectors.json")
        tribunal = load("thermo-psyche/classification-tribunal.json")
        self.assertEqual(set(rubric["classes"]), {"formal_invariant","operational_rule","normative_principle","heuristic","empirical_hypothesis","category_barrier"})
        self.assertEqual(relabel["vector_count"], 36)
        self.assertEqual(tribunal["fundamental_physical_laws_established"], 0)
        self.assertEqual(tribunal["consciousness_tensors_established"], 0)

    def test_16_stage20_board_has_exact_decisions_and_not_ready(self) -> None:
        matrix = load("stage20/claim-expiry-matrix.json")
        board = load("stage20/terminal-evidence-board.json")
        self.assertTrue(matrix["all_have_falsifier"])
        self.assertTrue(matrix["all_have_expiry_or_reopen"])
        self.assertEqual(set(row["decision"] for row in board["board"]), {"pass","fail","defer"})
        self.assertEqual(board["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(board["stage20_complete"])

    def test_17_all_inherited_and_v7_negatives_are_retained(self) -> None:
        data = load("retained-negative-register.json")
        self.assertEqual(data["inherited_count"], 9)
        self.assertEqual(data["new_count"], 11)
        self.assertEqual(data["negative_count"], 20)
        self.assertTrue(data["all_retained"])
        self.assertTrue(all(row["retained"] for row in data["negatives"]))

    def test_18_phase_truth_protects_every_claim(self) -> None:
        data = load("phase-truth.json")
        self.assertEqual(data["source_revision"], "313517217ddb820efb4c3fbbcdcfc3bed76ad429")
        self.assertEqual(data["x1_commit"], "f6281f48a3fad5b918df870117d2d02fdd4dba26")
        self.assertEqual(data["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(any(data["protected_claims"].values()))

    def test_19_overview_and_static_report_meet_structural_floor(self) -> None:
        overview = (PHASE / "v641-v7-integrated-overview.md").read_text(encoding="utf-8")
        report = (PHASE / "deliverables/v641-v7-chain-audit-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b\w+\b", overview)), 1800)
        for token in ['lang="en"','class="skip-link"','<main','<nav','<caption>','scope="col"']:
            self.assertIn(token, report)
        self.assertIn("not a complete WCAG conformance assessment", report)

    def test_20_phase_validator_accepts_current_coherent_state(self) -> None:
        module_path = ROOT / "scripts/ghc_family_chain_falsification_validator.py"
        spec = importlib.util.spec_from_file_location("v7_validator", module_path)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        snapshot_state = load("x2-proposal-ledger.json")["snapshot_state"]
        report = module.validate(PHASE, allow_pending=snapshot_state == "pending", require_report=True, output=None)
        self.assertTrue(report["valid"], report["issues"])


if __name__ == "__main__":
    unittest.main()
