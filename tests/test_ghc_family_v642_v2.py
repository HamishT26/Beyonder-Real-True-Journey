from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / "v642-v2"
SOURCE = "78fa2460eb223789e102c0627279d07acc216470"
X1 = "1dd4d7fa2c917ee838f9d8088df933e6ead22f6f"
EXPECTED = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}


def load(rel: str) -> dict:
    return json.loads((PHASE / rel).read_text(encoding="utf-8"))


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def import_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not import {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestGhcFamilyV642V2(unittest.TestCase):
    def test_01_x1_freeze_is_exact_and_not_retroactive(self) -> None:
        x1 = load("x1-proposals.json")
        x2 = load("x2-proposal-ledger.json")
        self.assertEqual(x1["source_revision"], SOURCE)
        self.assertEqual(x2["source_revision"], SOURCE)
        self.assertEqual(x2["x1_commit"], X1)
        self.assertFalse(x1["expected_counts_are_results"])

    def test_02_all_ten_proposals_have_complete_preregistration(self) -> None:
        x1 = load("x1-proposals.json")
        required = {
            "hypothesis", "null_or_failure", "approval_class", "execution_lane",
            "authoritative_source_needs", "deliverables", "test_falsifier_or_gate",
            "rollback_or_recovery", "protected_gates", "expected_disposition",
            "novelty_against_prior_chain",
        }
        self.assertEqual(x1["proposal_count"], len(x1["proposals"]))
        self.assertEqual(len({row["proposal_id"] for row in x1["proposals"]}), 10)
        self.assertTrue(all(required <= set(row) for row in x1["proposals"]))
        self.assertEqual(Counter(row["expected_disposition"] for row in x1["proposals"]), Counter(EXPECTED))

    def test_03_frozen_chain_has_ninety_unique_titles(self) -> None:
        chain = load("provenance/frozen-chain-proposal-index.json")
        self.assertEqual(chain["proposal_count"], len(chain["records"]))
        self.assertEqual(chain["proposal_count"], 90)
        self.assertEqual(chain["version_counts"]["v642-v2"], 10)
        self.assertEqual(len({row["title"] for row in chain["records"]}), 90)

    def test_04_provenance_exposes_overlap_and_independence_debt(self) -> None:
        overlap = load("provenance/evidence-root-overlap-matrix.json")
        debt = load("provenance/independence-debt-ledger.json")
        reach = load("provenance/negative-reachability-receipt.json")
        self.assertEqual(overlap["false_independent_cases_rejected"], 4)
        self.assertFalse(overlap["document_count_is_independence_count"])
        self.assertEqual(debt["open_debt_count"], len(debt["debts"]))
        self.assertFalse(debt["erasure_permitted"])
        self.assertEqual(reach["reachable_inherited_negatives"], 46)
        self.assertEqual(reach["unreachable_negatives"], [])

    def test_05_physics_is_typed_structural_and_nonempirical(self) -> None:
        ast = load("physics/canonical-equation-ast.json")
        units = load("physics/unit-basis-and-covariance-vectors.json")
        witness = load("physics/conservation-stability-jacobian-witness.json")
        boundary = load("physics/identifiability-claim-boundary.json")
        self.assertEqual(ast["model_class"], "typed scalar-tensor EFT research scaffold")
        self.assertEqual(ast["dimension_basis"], ["M", "L", "T"])
        self.assertTrue(all(eq["typed"] and not eq["empirically_confirmed"] for eq in ast["equations"]))
        self.assertEqual(units["invalid_vectors_rejected"], 5)
        self.assertTrue(witness["structural_observability_only"])
        self.assertFalse(witness["empirical_identifiability"])
        self.assertFalse(any(boundary[key] for key in ["detected_force", "unique_prediction", "empirical_gmut_confirmation", "proof_or_canon"]))

    def test_06_empirical_adapter_is_rowless_readiness_not_fit(self) -> None:
        adapter = load("empirical/public-data-adapter-contract.json")
        vectors = load("empirical/round-trip-schema-vectors.json")
        receipt = load("empirical/null-baseline-readiness.json")
        gate = load("empirical/real-data-likelihood-gate.json")
        self.assertEqual(adapter["mode"], "metadata_only_rowless")
        self.assertFalse(adapter["network_download"])
        self.assertEqual(vectors["invalid_vectors_quarantined"], 5)
        self.assertEqual(receipt["parsed_measurement_rows"], receipt["likelihoods_executed"])
        self.assertEqual(receipt["likelihoods_executed"], receipt["fits_executed"])
        self.assertEqual(receipt["fits_executed"], 0)
        self.assertFalse(receipt["readiness_is_fit"])
        self.assertFalse(gate["empirical_gmut_confirmation"])

    def test_07_thos_escrow_has_zero_real_arms(self) -> None:
        escrow = load("thos/allocation-escrow-spec.json")
        vectors = load("thos/blindness-budget-mutation-vectors.json")
        attrition = load("thos/attrition-decision-table.json")
        gate = load("thos/real-arm-execution-gate.json")
        self.assertEqual(escrow["mode"], "synthetic_protocol_only")
        self.assertEqual(escrow["real_arm_runs"], gate["real_arm_runs"])
        self.assertEqual(gate["real_arm_runs"], 0)
        self.assertEqual(vectors["mutations_rejected"], len(vectors["vectors"]))
        self.assertFalse(attrition["post_hoc_deletion_allowed"])
        self.assertFalse(any(gate[key] for key in ["superiority_established", "agi", "asi", "consciousness", "personhood"]))

    def test_08_freed_id_is_structural_without_production_assurance(self) -> None:
        profile = load("freed-id/cross-layer-conformance-profile.json")
        vectors = load("freed-id/status-resolver-consistency-vectors.json")
        trust = load("freed-id/trust-governance-assumption-ledger.json")
        gate = load("freed-id/production-assurance-gate.json")
        self.assertEqual(profile["mode"], "synthetic_structural_only")
        self.assertEqual(vectors["real_cryptographic_operations"], 0)
        self.assertTrue(all(row["state"] == "open" for row in trust["assumptions"]))
        self.assertFalse(trust["technical_artifact_can_assign_governance"])
        self.assertTrue(all(gate[key] == 0 for key in ["real_keys", "real_proofs", "live_resolvers", "live_status_services", "interoperability_partners", "independent_security_reviews"]))
        self.assertFalse(gate["cryptographic_assurance"])

    def test_09_cbr_defers_to_affected_parties_and_maori_authority(self) -> None:
        lifecycle = load("cbr/authority-scope-lifecycle.json")
        consent = load("cbr/consent-revocation-vectors.json")
        remedy = load("cbr/remedy-nonretrogression-matrix.json")
        gate = load("cbr/legal-cultural-authority-gate.json")
        self.assertFalse(lifecycle["system_may_assign_authority"])
        self.assertTrue(lifecycle["withdrawal_precedence"])
        self.assertTrue(lifecycle["maori_authority_nontransferable"])
        self.assertTrue(all(row["decision"] == "defer" for row in consent["vectors"]))
        self.assertTrue(all(row["remedy_floor_preserved"] for row in remedy["cases"]))
        self.assertEqual(gate["state"], "exact_gate")
        self.assertFalse(any(gate[key] for key in ["affected_party_authority_present", "maori_authority_present", "cultural_ratification_present", "competent_legal_authority_present", "enacted_law"]))

    def test_10_parser_and_recovery_battery_is_bounded(self) -> None:
        policy = load("security/canonical-input-policy.json")
        vectors = load("security/parser-differential-vectors.json")
        recovery = load("security/recovery-resource-receipt.json")
        self.assertEqual(policy["duplicate_keys"], "reject")
        self.assertEqual(policy["non_finite_numbers"], "reject")
        self.assertEqual(policy["unsafe_integer_domain"], "reject")
        self.assertEqual(policy["unicode_normalization_collision"], "reject")
        self.assertEqual(vectors["strict_rejections"], len(vectors["vectors"]))
        self.assertFalse(any(row["strict_accept"] for row in vectors["vectors"]))
        self.assertFalse(recovery["destructive_cleanup"] or recovery["elevation"] or recovery["host_security_changed"] or recovery["exhaustive_security"])

    def test_11_replay_is_cross_owner_internal_not_independent(self) -> None:
        replay = load("reproduction/cross-owner-lineage-replay.json")
        perturb = load("reproduction/environment-perturbation-receipt.json")
        gap = load("reproduction/independent-team-gap.json")
        self.assertEqual(replay["source_repository_tests"], {"passed": 170, "failed": 0})
        self.assertEqual(replay["source_phase_validator"], {"passed": 89, "issues": 0})
        self.assertEqual(replay["source_minimal_verifier"], {"passed": 17, "issues": 0})
        self.assertIn(perturb["state"], {"pending_clean_snapshots", "verified"})
        self.assertFalse(replay["independent_team_reproduction"])
        self.assertFalse(gap["independent_team_present"])
        self.assertIn("cross-owner internal repeatability", gap["strongest_allowed_claim"])

    def test_12_thermo_psyche_category_and_causal_barriers_hold(self) -> None:
        invariance = load("thermo-psyche/measurement-invariance-vectors.json")
        temporal = load("thermo-psyche/temporal-order-register.json")
        categories = load("thermo-psyche/category-boundary-matrix.json")
        receipt = load("thermo-psyche/classification-receipt.json")
        self.assertEqual(invariance["noninvariant_vectors_rejected"], 5)
        self.assertFalse(temporal["temporal_order_alone_proves_causality"])
        self.assertEqual(categories["classes"], ["thermodynamic", "computational", "psychological", "metaphorical", "emergent", "fundamental_law_candidate"])
        self.assertFalse(categories["automatic_cross_category_promotion"])
        self.assertFalse(categories["computational_telemetry_is_subjective_experience"])
        self.assertFalse(any(receipt[key] for key in ["fundamental_law_established", "consciousness_tensor", "consciousness", "personhood"]))

    def test_13_stage20_board_cannot_score_away_authority(self) -> None:
        dominance = load("stage20/gate-dominance-matrix.json")
        freshness = load("stage20/evidence-freshness-ledger.json")
        vectors = load("stage20/decision-monotonicity-vectors.json")
        board = load("stage20/pass-fail-defer-board.json")
        terminal = load("stage20/terminal-verdict.json")
        self.assertEqual(len(dominance["dominant_open_gaps"]), 5)
        self.assertEqual(len(dominance["dominant_exact_gates"]), 6)
        self.assertFalse(dominance["technical_score_may_override_exact_gate"])
        self.assertFalse(freshness["expired_or_withdrawn_supports_pass"] or freshness["freshness_implies_truth"])
        self.assertEqual(vectors["invalid_improvements_rejected"], 2)
        self.assertEqual(set(board["decisions"]), {"pass", "fail", "defer"})
        self.assertEqual(terminal["verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(terminal["deployment_authorized"])

    def test_14_all_inherited_new_and_execution_negatives_are_retained(self) -> None:
        data = load("retained-negative-register.json")
        incident = load("validation/execution-negative-log.json")
        self.assertEqual((data["inherited_count"], data["new_count"], data["negative_count"]), (46, 20, 66))
        self.assertEqual(data["negative_count"], len(data["negatives"]))
        self.assertTrue(data["all_retained"])
        self.assertFalse(data["erasure_permitted"])
        self.assertTrue(all(row["retained"] for row in data["negatives"]))
        self.assertEqual(incident["negative_count"], 6)
        self.assertEqual([row["negative_id"] for row in incident["negatives"]], ["V6422-N15", "V6422-N16", "V6422-N17", "V6422-N18", "V6422-N19", "V6422-N20"])
        self.assertTrue(all(row["preserved"] for row in incident["negatives"]))

    def test_15_gate_register_preserves_five_plus_six(self) -> None:
        data = load("exact-open-gate-register.json")
        self.assertEqual((data["open_gap_count"], data["exact_gate_count"]), (5, 6))
        self.assertEqual(Counter(row["gate_class"] for row in data["gates"]), Counter({"exact_gate": 6, "open_gap": 5}))
        self.assertEqual(data["silently_closed"], 0)
        self.assertTrue(all(row["state"] in {"open", "deferred"} for row in data["gates"]))

    def test_16_outcome_ledger_uses_only_four_exact_classes(self) -> None:
        ledger = load("x2-proposal-ledger.json")
        truth = load("phase-truth.json")
        self.assertEqual(ledger["disposition_counts"], EXPECTED)
        self.assertEqual(truth["disposition_counts"], EXPECTED)
        self.assertTrue(ledger["all_executed_as_far_as_evidence_permits"])
        self.assertFalse(any(truth["protected_claims"].values()))
        self.assertEqual(truth["independent_team_gap"], "open")

    def test_17_normalized_manifest_hashes_match(self) -> None:
        manifest = load("reproduction/semantic-normalization-manifest.json")
        actual = {rel: normalized_sha256(PHASE / rel) for rel in manifest["hashes"]}
        self.assertEqual(actual, manifest["hashes"])
        aggregate = hashlib.sha256("".join(f"{rel}:{actual[rel]}\n" for rel in sorted(actual)).encode("utf-8")).hexdigest()
        self.assertEqual(aggregate, manifest["aggregate_sha256"])
        self.assertEqual(manifest["artifact_count"], len(actual))
        self.assertFalse(manifest["absolute_paths_required"])
        self.assertFalse(manifest["independent_team_reproduction"])

    def test_18_overview_and_report_meet_structural_floor(self) -> None:
        overview = (PHASE / "v642-v2-integrated-overview.md").read_text(encoding="utf-8")
        report = (PHASE / "deliverables/v642-v2-evidence-crosscheck-report.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"\b\w+[\w'-]*\b", overview)), 1800)
        for token in ['lang="en"', 'class="skip-link"', "<main", "<nav", "<caption>", 'scope="col"']:
            self.assertIn(token, report)
        self.assertIn("not a complete WCAG conformance assessment", report)

    def test_19_source_statuses_and_references_are_exact(self) -> None:
        source = load("sources/source-ledger.json")
        x1 = load("x1-proposals.json")
        self.assertEqual(source["source_count"], 38)
        self.assertEqual(Counter(row["status_class"] for row in source["sources"]), Counter({"current": 20, "stable": 14, "draft": 3, "watch": 1}))
        ids = {row["source_id"] for row in source["sources"]}
        self.assertFalse({ref for proposal in x1["proposals"] for ref in proposal["authoritative_source_needs"]} - ids)
        self.assertTrue(all(row["status_class"] == "draft" for row in source["sources"] if row["source_id"] in {"V8-S14", "V8-S15", "V6421-S33"}))

    def test_20_full_and_minimal_validators_accept_state(self) -> None:
        full = import_script("crosscheck_validator", "ghc_family_evidence_crosscheck_validator.py")
        minimal = import_script("crosscheck_minimal", "ghc_family_evidence_crosscheck_minimal.py")
        state = load("x2-proposal-ledger.json")["snapshot_state"]
        allow_pending = state != "verified"
        full_result = full.validate(PHASE, allow_pending_snapshot=allow_pending, require_report=True)
        minimal_result = minimal.verify(PHASE, allow_pending_snapshot=allow_pending)
        self.assertTrue(full_result["valid"], full_result["issues"])
        self.assertTrue(minimal_result["valid"], minimal_result["issues"])


if __name__ == "__main__":
    unittest.main()
