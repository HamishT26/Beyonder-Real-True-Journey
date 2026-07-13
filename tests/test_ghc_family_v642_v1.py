from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "nima-calder" / "v642-v1"


def load(rel: str) -> dict:
    return json.loads((PHASE / rel).read_text(encoding="utf-8"))


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class TestGhcFamilyV642V1(unittest.TestCase):
    def test_01_x1_freeze_and_source_are_exact(self) -> None:
        x1 = load("x1-proposals.json")
        ledger = load("x2-proposal-ledger.json")
        self.assertEqual(x1["source_revision"], "62f35540964e964760fdf10c7acf580f320dcd29")
        self.assertEqual(ledger["x1_commit"], "4785eae506ec19152b282297e496ff7f0209fa2e")
        self.assertEqual(x1["proposal_count"], len(x1["proposals"]))
        self.assertFalse(x1["expected_counts_are_results"])

    def test_02_all_ten_proposals_have_complete_preregistration(self) -> None:
        x1 = load("x1-proposals.json")
        required = {"hypothesis", "null_or_failure", "approval_class", "execution_lane", "authoritative_source_needs", "deliverables", "test_falsifier_or_gate", "rollback_or_recovery", "protected_gates", "expected_disposition", "novelty_against_prior_chain"}
        self.assertEqual(len({row["proposal_id"] for row in x1["proposals"]}), 10)
        self.assertTrue(all(required <= set(row) for row in x1["proposals"]))

    def test_03_frozen_chain_has_eighty_without_duplicate_titles(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(chain["proposal_count"], 80)
        self.assertEqual(len(chain["records"]), 80)
        self.assertEqual(chain["version_counts"]["v642-v1"], 10)
        self.assertEqual(chain["exact_duplicate_titles"], [])

    def test_04_counterevidence_and_independence_are_monotonic(self) -> None:
        inheritance = load("provenance/counterevidence-inheritance-vectors.json")
        context = load("provenance/context-collision-matrix.json")
        partition = load("provenance/source-independence-partition.json")
        self.assertTrue(inheritance["all_rejected_or_quarantined"])
        self.assertEqual(inheritance["erased_negative_count"], 0)
        self.assertEqual(context["unsupported_scope_expansions"], 0)
        self.assertTrue(partition["independence_is_root_based_not_document_count"])
        self.assertEqual(partition["false_independent_root_count"], 0)

    def test_05_variational_boundary_audit_stays_structural(self) -> None:
        canonical = load("physics/canonical-variational-register.json")
        surface = load("physics/boundary-surface-equivalence-vectors.json")
        boundary = load("physics/initial-boundary-admissibility-matrix.json")
        receipt = load("physics/conservation-stability-identifiability-receipt.json")
        self.assertEqual(canonical["model_family"], "typed scalar-tensor/EFT research scaffold")
        self.assertTrue(canonical["boundary_term_required_for_declared_variational_problem"])
        self.assertTrue(surface["all_mutations_killed"])
        self.assertFalse(boundary["global_well_posedness_proved"])
        self.assertFalse(any([canonical["empirical_confirmation"], canonical["detected_force"], canonical["unique_prediction"], canonical["theory_of_everything"], receipt["empirical_stability_or_identifiability"], receipt["empirical_gmut_confirmation"], receipt["theory_of_everything"]]))

    def test_06_adapter_has_zero_rows_likelihoods_and_fits(self) -> None:
        contract = load("empirical/selection-window-contract.json")
        vectors = load("empirical/covariance-shape-vectors.json")
        receipt = load("empirical/zero-row-readiness-receipt.json")
        self.assertFalse(contract["content_downloaded"])
        self.assertTrue(vectors["all_quarantined"])
        self.assertEqual(receipt["real_measurement_rows_parsed"], 0)
        self.assertEqual(receipt["likelihood_calls"], 0)
        self.assertEqual(receipt["parameter_fits"], 0)
        self.assertEqual(receipt["disposition"], "represented")

    def test_07_thos_crossover_is_synthetic_and_matched(self) -> None:
        lock = load("thos/crossover-sequence-lock.json")
        vectors = load("thos/period-carryover-vectors.json")
        exposure = load("thos/matched-budget-exposure.json")
        gap = load("thos/real-arm-gap.json")
        self.assertTrue(lock["synthetic_only"])
        self.assertEqual(lock["real_arm_runs"], 0)
        self.assertTrue(vectors["all_rejected_before_unseal"])
        self.assertTrue(exposure["tokens_equal"] and exposure["time_equal"] and exposure["tools_equal"])
        self.assertFalse(any([gap["real_arms_present"], gap["blind_matched_budget_superiority_result"], gap["agi_evidence"], gap["asi_evidence"], gap["consciousness_evidence"], gap["personhood_evidence"]]))

    def test_08_freed_id_unlinkability_is_not_production_assurance(self) -> None:
        profile = load("freed-id/disclosure-minimization-profile.json")
        vectors = load("freed-id/correlation-linkability-vectors.json")
        standards = load("freed-id/status-resolution-standards-boundary.json")
        gate = load("freed-id/production-cryptographic-gate.json")
        self.assertEqual(profile["real_credentials"], profile["real_keys"])
        self.assertEqual(profile["real_keys"], profile["real_proofs"])
        self.assertEqual(profile["real_proofs"], 0)
        self.assertTrue(vectors["all_flagged_or_rejected"])
        self.assertFalse(standards["draft_replaces_stable"])
        self.assertEqual(gate["satisfied_count"], 0)
        self.assertFalse(gate["cryptographic_assurance"])
        self.assertEqual(gate["disposition"], "open_gap")

    def test_09_cbr_defers_to_affected_parties_and_maori_authority(self) -> None:
        standing = load("cbr/standing-representation-boundary.json")
        remedy = load("cbr/remedy-preservation-protocol.json")
        vectors = load("cbr/anti-retaliation-recusal-vectors.json")
        gates = load("cbr/legal-cultural-authority-gates.json")
        self.assertFalse(standing["system_can_determine_standing"])
        self.assertFalse(remedy["technical_artifact_can_waive_remedy"])
        self.assertTrue(vectors["all_deferred_or_rejected"])
        self.assertFalse(gates["system_may_speak_for_maori"])
        self.assertFalse(gates["system_may_substitute_for_affected_parties"])
        self.assertEqual(gates["decision"], "exact_gate")

    def test_10_resource_battery_is_bounded_and_non_destructive(self) -> None:
        policy = load("security/resource-ceiling-policy.json")
        vectors = load("security/parser-decompression-vectors.json")
        receipt = load("security/recovery-and-privacy-receipt.json")
        self.assertTrue(policy["checked_before_materialization"])
        self.assertFalse(policy["large_payloads_created"])
        self.assertEqual(vectors["unsafe_vectors_rejected"], 9)
        self.assertEqual(vectors["payload_bytes_materialized"], 0)
        self.assertFalse(vectors["exhaustive_security"])
        self.assertEqual(receipt["destructive_commands"], 0)
        self.assertFalse(receipt["privilege_expansion"])

    def test_11_dual_oracle_keeps_independent_gap_open(self) -> None:
        spec = load("reproduction/minimal-verifier-spec.json")
        ablation = load("reproduction/dependency-ablation-matrix.json")
        dual = load("reproduction/dual-oracle-receipt.json")
        gap = load("reproduction/independent-team-gap.json")
        self.assertEqual(spec["runtime"], "Python standard library only")
        self.assertTrue(ablation["all_declared_nonrequirements"])
        self.assertIn(dual["state"], {"pending_validator_execution", "verified"})
        if dual["state"] == "verified":
            self.assertTrue(dual["full_validator_valid"] and dual["minimal_verifier_valid"] and dual["core_outputs_equal"])
        self.assertFalse(gap["independent_team_reproduction"])
        self.assertEqual(gap["gap"], "open")

    def test_12_thermo_psyche_construct_and_causal_barriers_hold(self) -> None:
        register = load("thermo-psyche/construct-operationalization-register.json")
        causal = load("thermo-psyche/causal-direction-vectors.json")
        alternatives = load("thermo-psyche/alternative-explanation-matrix.json")
        receipt = load("thermo-psyche/classification-receipt.json")
        self.assertEqual(set(register["classes"]), {"category_barrier", "heuristic", "normative_principle", "operational_rule", "formal_invariant", "empirical_hypothesis"})
        self.assertTrue(causal["all_category_shortcuts_rejected"])
        self.assertTrue(alternatives["alternatives_required"])
        self.assertEqual(receipt["fundamental_physical_laws_established"], 0)
        self.assertEqual(receipt["consciousness_tensors_established"], 0)

    def test_13_stage20_authority_cannot_be_scored_away(self) -> None:
        order = load("stage20/evidence-order-register.json")
        vectors = load("stage20/authority-nonsubstitution-vectors.json")
        board = load("stage20/pass-fail-defer-board.json")
        terminal = load("stage20/terminal-verdict.json")
        self.assertFalse(order["exact_authority_scored"])
        self.assertTrue(vectors["all_rejected"])
        self.assertEqual({row["decision"] for row in board["board"]}, {"pass", "fail", "defer"})
        self.assertEqual(terminal["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(terminal["stage20_complete"])

    def test_14_negatives_are_inherited_and_extended_exactly(self) -> None:
        data = load("retained-negative-register.json")
        self.assertEqual((data["inherited_count"], data["new_count"], data["negative_count"]), (32, 14, 46))
        self.assertTrue(data["all_retained"])
        self.assertFalse(data["erasure_permitted"])
        self.assertTrue(all(row["retained"] for row in data["negatives"]))

    def test_15_gate_register_is_open_or_exact_only(self) -> None:
        data = load("exact-open-gate-register.json")
        counts = Counter(row["gate_class"] for row in data["gates"])
        self.assertEqual((data["open_gap_count"], data["exact_gate_count"]), (5, 6))
        self.assertEqual(counts, Counter({"exact_gate": 6, "open_gap": 5}))
        self.assertEqual(data["silently_closed"], 0)

    def test_16_outcome_ledger_has_four_exact_classes(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        truth = load("phase-truth.json")
        expected = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
        self.assertEqual(ledger["disposition_counts"], expected)
        self.assertEqual(truth["disposition_counts"], expected)
        self.assertTrue(ledger["all_executed_as_far_as_evidence_permits"])
        self.assertFalse(any(truth["protected_claims"].values()))

    def test_17_manifest_matches_all_committed_core_artifacts(self) -> None:
        data = load("reproduction/manifest.json")
        actual = {rel: normalized_sha256(PHASE / rel) for rel in data["normalized_hashes"]}
        self.assertEqual(actual, data["normalized_hashes"])
        aggregate = hashlib.sha256("".join(f"{key}:{actual[key]}\n" for key in sorted(actual)).encode()).hexdigest()
        self.assertEqual(aggregate, data["aggregate_sha256"])
        self.assertEqual(data["artifact_count"], len(actual))
        self.assertFalse(data["independent_team_reproduction"])

    def test_18_overview_and_static_report_meet_structural_floor(self) -> None:
        overview = (PHASE / "v642-v1-integrated-overview.md").read_text(encoding="utf-8")
        report = (PHASE / "deliverables/v642-v1-evidence-boundary-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b\w+\b", overview)), 1800)
        for token in ['lang="en"', 'class="skip-link"', "<main", "<nav", "<caption>", 'scope="col"']:
            self.assertIn(token, report)
        self.assertIn("not a complete WCAG conformance assessment", report)

    def test_19_source_statuses_and_refs_are_exact(self) -> None:
        source = load("sources/source-ledger.json")
        x1 = load("x1-proposals.json")
        self.assertEqual(source["source_count"], 34)
        self.assertEqual(Counter(row["status_class"] for row in source["sources"]), Counter(source["status_counts"]))
        ids = {row["source_id"] for row in source["sources"]}
        self.assertFalse({ref for row in x1["proposals"] for ref in row["authoritative_source_needs"]} - ids)
        self.assertEqual(next(row for row in source["sources"] if row["source_id"] == "V6421-S33")["status_class"], "draft")

    def test_20_full_family_validator_accepts_current_state(self) -> None:
        module_path = ROOT / "scripts" / "ghc_family_evidence_boundary_validator.py"
        spec = importlib.util.spec_from_file_location("boundary_validator", module_path)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        snapshot_state = load("reproduction/clean-snapshot-validation.json")["state"]
        report = module.validate(PHASE, allow_pending_snapshot=snapshot_state != "verified", require_report=True, output=None)
        self.assertTrue(report["valid"], report["issues"])


if __name__ == "__main__":
    unittest.main()
