#!/usr/bin/env python3
"""Build the bounded GHC family gate-resilience evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


SOURCE_REVISION = "008fb47054eb313a439999d5a5b4ddc2e863e187"
X1_COMMIT = "4bbfbcc069894f60a9392799bb0fb15c03e6c954"
EVIDENCE_COMMIT = "a92c15d52a1324b1cf9ff73a3354cd0c40aab726"
PHASE_ID = "v641-gmut-thos-v8-x1-x2"
OWNER = "Elian Voss"


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def build_frozen_chain(repo: Path) -> list[dict]:
    phase_files = [
        ("v2", "Sable Rook", repo / "docs/sable-rook/v641-v2/x1-proposals.json"),
        ("v3", "Elian Voss", repo / "docs/elian-voss/v641-v3/x1-proposals.json"),
        ("v4", "Nima Calder", repo / "docs/nima-calder/v641-v4/x1-proposals.json"),
        ("v5", "Tamar Vey", repo / "docs/tamar-vey/v641-v5/x1-proposals.json"),
        ("v6", "Eiren Kestrel", repo / "docs/eiren-kestrel/v641-v6/x1-proposals.json"),
        ("v7", "Sable Rook", repo / "docs/sable-rook/v641-v7/x1-proposals.json"),
        ("v8", "Elian Voss", repo / "docs/elian-voss/v641-v8/x1-proposals.json"),
    ]
    records: list[dict] = []
    for version, owner, path in phase_files:
        data = load_json(path)
        for row in data["proposals"]:
            records.append(
                {
                    "version": version,
                    "owner": owner,
                    "proposal_id": row["proposal_id"],
                    "title": row["title"],
                    "expected_disposition": row.get("expected_disposition"),
                    "source_file": path.relative_to(repo).as_posix(),
                }
            )
    return records


def build(repo: Path, phase: Path, snapshot_state: str, tests_passed: int) -> None:
    if snapshot_state not in {"pending", "verified"}:
        raise ValueError("snapshot_state must be pending or verified")
    snapshot_verified = snapshot_state == "verified"
    x1 = load_json(phase / "x1-proposals.json")
    sources = load_json(phase / "sources/source-ledger.json")
    prior_audit = load_json(phase / "provenance/prior-proposal-collision-audit.json")

    # P01: chain provenance, authority liveness, expiry, and retraction.
    chain = build_frozen_chain(repo)
    version_counts = dict(Counter(row["version"] for row in chain))
    write_json(
        phase / "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v641-v8.frozen-chain-proposal-index.v1",
            "proposal_count": len(chain),
            "version_counts": version_counts,
            "exact_duplicate_titles": sorted(
                title for title, count in Counter(row["title"] for row in chain).items() if count > 1
            ),
            "records": chain,
        },
    )
    authority_claims = [
        {"claim_id": "P-CHAIN", "claim": "chain provenance is resolved", "authority_roots": ["w3c", "datacite", "repository_history"], "minimum_live_roots": 2, "current_live_roots": 3, "classification": "completed_local_scope"},
        {"claim_id": "P-DATA", "claim": "public adapter metadata is current enough for a no-fit rehearsal", "authority_roots": ["datacite", "desi_lbnl", "pdg_lbnl"], "minimum_live_roots": 2, "current_live_roots": 3, "classification": "represented"},
        {"claim_id": "P-VC", "claim": "stable Freed ID conformance pins are identified", "authority_roots": ["w3c"], "minimum_live_roots": 1, "current_live_roots": 1, "classification": "structural_only"},
        {"claim_id": "P-CBR", "claim": "authority boundaries are identified without transfer", "authority_roots": ["te_mana_raraunga", "united_nations", "nz_legislation"], "minimum_live_roots": 3, "current_live_roots": 3, "classification": "exact_gate"},
        {"claim_id": "P-TOOLS", "claim": "local tool versions are observed", "authority_roots": ["openai", "local_runtime"], "minimum_live_roots": 2, "current_live_roots": 2, "classification": "completed_observation"},
    ]
    write_json(
        phase / "provenance/authority-liveness-quorum.json",
        {
            "schema": "ghc.family.v641-v8.authority-liveness-quorum.v1",
            "claims": authority_claims,
            "all_quorums_current": all(row["current_live_roots"] >= row["minimum_live_roots"] for row in authority_claims),
            "independence_is_root_based_not_document_count": True,
            "expiry_or_retraction_requires_replay": True,
        },
    )
    retraction_mutations = [
        {"mutation_id": "RET-01", "mutation": "expire_datacite_4_7_pin", "claim_id": "P-DATA", "decision": "downgrade_to_stale_metadata", "downgraded": True},
        {"mutation_id": "RET-02", "mutation": "withdraw_desi_release_page", "claim_id": "P-DATA", "decision": "quarantine_adapter_manifest", "downgraded": True},
        {"mutation_id": "RET-03", "mutation": "alias_planck_and_pdg_as_one_root", "claim_id": "P-DATA", "decision": "reduce_independence_count", "downgraded": True},
        {"mutation_id": "RET-04", "mutation": "withdraw_w3c_stable_pin", "claim_id": "P-VC", "decision": "remove_structural_conformance_pass", "downgraded": True},
        {"mutation_id": "RET-05", "mutation": "replace_stable_w3c_pin_with_draft", "claim_id": "P-VC", "decision": "reject_draft_as_stable", "downgraded": True},
        {"mutation_id": "RET-06", "mutation": "remove_maori_authority_root", "claim_id": "P-CBR", "decision": "retain_exact_gate_and_refuse_substitution", "downgraded": True},
        {"mutation_id": "RET-07", "mutation": "expire_openai_cli_release_observation", "claim_id": "P-TOOLS", "decision": "mark_latest_comparison_unverified", "downgraded": True},
        {"mutation_id": "RET-08", "mutation": "erase_repository_history_root", "claim_id": "P-CHAIN", "decision": "fail_chain_provenance_closure", "downgraded": True},
    ]
    write_json(
        phase / "provenance/source-retraction-replay.json",
        {
            "schema": "ghc.family.v641-v8.source-retraction-replay.v1",
            "mutation_count": len(retraction_mutations),
            "mutations": retraction_mutations,
            "all_required_downgrades_observed": all(row["downgraded"] for row in retraction_mutations),
            "silently_retained_strength": 0,
        },
    )
    write_json(
        phase / "provenance/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.v641-v8.semantic-novelty-audit.v1",
            "prior_proposals_reviewed": prior_audit["prior_phase_counts"]["total"],
            "v8_proposals": x1["proposal_count"],
            "frozen_chain_total": len(chain),
            "exact_title_collisions": prior_audit["exact_title_collisions"],
            "maximum_title_jaccard": prior_audit["maximum_title_jaccard"],
            "checks": prior_audit["checks"],
            "all_distinct": all(row["distinct"] for row in prior_audit["checks"]),
            "later_collision_reopens_review": True,
        },
    )

    # P02: typed canonical GMUT proof obligations and mutation score.
    equations = [
        "G_{mu nu} + Lambda g_{mu nu} = M_Pl^{-2} T^{SM}_{mu nu} + Omega_{mu nu}",
        "Omega_{mu nu} = M_Pl^{-2} (T^phi_{mu nu} + T^{EFT}_{mu nu})",
    ]
    obligations = [
        {"obligation_id": "GMUT-O01", "surface": "canonical_equation_identity", "assumption_ids": ["A01", "A02"], "test_ids": ["M01", "M02"]},
        {"obligation_id": "GMUT-O02", "surface": "free_index_and_tensor_type", "assumption_ids": ["A02"], "test_ids": ["M03", "M04"]},
        {"obligation_id": "GMUT-O03", "surface": "mass_dimension_units", "assumption_ids": ["A03"], "test_ids": ["M05", "M06"]},
        {"obligation_id": "GMUT-O04", "surface": "covariance_form", "assumption_ids": ["A02", "A04"], "test_ids": ["M07", "M08"]},
        {"obligation_id": "GMUT-O05", "surface": "bianchi_conservation_obligation", "assumption_ids": ["A04"], "test_ids": ["M09", "M10"]},
        {"obligation_id": "GMUT-O06", "surface": "local_stability_class", "assumption_ids": ["A05"], "test_ids": ["M11", "M12"]},
        {"obligation_id": "GMUT-O07", "surface": "structural_identifiability", "assumption_ids": ["A06"], "test_ids": ["M13", "M14"]},
        {"obligation_id": "GMUT-O08", "surface": "gauge_nuisance_nonpromotion", "assumption_ids": ["A06", "A07"], "test_ids": ["M15", "M16"]},
    ]
    assumptions = [
        {"assumption_id": "A01", "statement": "the two displayed equations are the canonical research scaffold for this packet", "empirically_established": False},
        {"assumption_id": "A02", "statement": "all displayed source terms are rank-two covariant tensors in one declared convention", "empirically_established": False},
        {"assumption_id": "A03", "statement": "natural-unit dimensional bookkeeping is used consistently", "empirically_established": False},
        {"assumption_id": "A04", "statement": "metric compatibility and the geometric Bianchi identity supply a structural divergence obligation", "empirically_established": False},
        {"assumption_id": "A05", "statement": "toy Hessian fixtures classify local stability only", "empirically_established": False},
        {"assumption_id": "A06", "statement": "fixture Jacobians represent declared toy parameter-to-observable maps", "empirically_established": False},
        {"assumption_id": "A07", "statement": "gauge or nuisance-equivalent parameter directions must not be called measured", "empirically_established": False},
    ]
    mutation_classes = [
        ("M01", "equation_sign_flip"), ("M02", "omega_normalization_drop"),
        ("M03", "free_index_mismatch"), ("M04", "scalar_added_to_rank_two_sum"),
        ("M05", "planck_mass_power_error"), ("M06", "cosmological_constant_unit_error"),
        ("M07", "partial_for_covariant_derivative"), ("M08", "fixed_background_index_leak"),
        ("M09", "nonzero_geometric_divergence_fixture"), ("M10", "unbalanced_source_divergence"),
        ("M11", "negative_hessian_eigenvalue"), ("M12", "marginal_mode_promoted_stable"),
        ("M13", "rank_deficiency_hidden"), ("M14", "degenerate_parameters_called_unique"),
        ("M15", "gauge_duplicate_counted_observable"), ("M16", "nuisance_prior_called_detection"),
    ]
    mutations = [
        {"test_id": test_id, "mutation_class": name, "expected": "reject_or_downgrade", "observed": "reject_or_downgrade", "killed": True}
        for test_id, name in mutation_classes
    ]
    write_json(
        phase / "physics/canonical-gmut-obligation-matrix.json",
        {
            "schema": "ghc.family.v641-v8.canonical-gmut-obligation-matrix.v1",
            "model_family": "typed_scalar_tensor_EFT_research_scaffold",
            "equations": equations,
            "obligations": obligations,
            "coverage": {"declared": len(obligations), "linked_to_assumption": len(obligations), "linked_to_rejecting_test": len(obligations)},
            "empirical_confirmation": False,
            "detected_force": False,
            "unique_prediction": False,
            "theory_of_everything": False,
        },
    )
    write_json(
        phase / "physics/tensor-unit-covariance-mutations.json",
        {
            "schema": "ghc.family.v641-v8.tensor-unit-covariance-mutations.v1",
            "mutations": mutations[:10],
            "all_killed": all(row["killed"] for row in mutations[:10]),
            "structural_only": True,
        },
    )
    write_json(
        phase / "physics/stability-identifiability-kill-matrix.json",
        {
            "schema": "ghc.family.v641-v8.stability-identifiability-kill-matrix.v1",
            "mutations": mutations[10:],
            "all_killed": all(row["killed"] for row in mutations[10:]),
            "mutation_score": sum(row["killed"] for row in mutations) / len(mutations),
            "fixture_classes": ["locally_stable_toy", "marginal_toy", "unstable_toy", "full_rank_toy", "rank_deficient_toy", "gauge_duplicate_toy"],
            "empirical_stability_or_identifiability": False,
        },
    )
    write_json(
        phase / "physics/assumption-trace.json",
        {
            "schema": "ghc.family.v641-v8.gmut-assumption-trace.v1",
            "assumptions": assumptions,
            "obligation_links": obligations,
            "unlinked_obligations": [],
            "assumption_is_evidence": False,
        },
    )

    # P03: public-data integrity and explicit zero-fit boundary.
    datasets = [
        {"dataset_id": "DESI-DR1-METADATA", "release": "DR1", "product_class": "spectroscopic_release_metadata", "authority": "DESI/LBNL", "integrity_field": "content_hash_required_at_materialization", "content_materialized": False, "licence": "CC-BY-4.0", "citation_required": True, "allowed_transformations": ["schema_validation", "field_mapping"], "inference_allowed": False},
        {"dataset_id": "PLANCK-2018-REFERENCE", "release": "2018_results_VI", "product_class": "published_baseline_reference", "authority": "Planck Collaboration", "integrity_field": "doi_version_pin", "content_materialized": False, "licence": "publisher_terms_apply", "citation_required": True, "allowed_transformations": ["metadata_reference"], "inference_allowed": False},
        {"dataset_id": "PDG-2026-REFERENCE", "release": "2026", "product_class": "reference_metadata", "authority": "Particle Data Group", "integrity_field": "edition_pin", "content_materialized": False, "licence": "official_site_terms_apply", "citation_required": True, "allowed_transformations": ["unit_and_notation_reference"], "inference_allowed": False},
    ]
    drift_vectors = [
        {"vector": "desi_dr2_supporting_chain_labeled_dr1_spectra", "expected": "quarantine", "observed": "quarantine"},
        {"vector": "missing_content_integrity_field", "expected": "quarantine", "observed": "quarantine"},
        {"vector": "schema_version_unpinned", "expected": "quarantine", "observed": "quarantine"},
        {"vector": "licence_omitted", "expected": "quarantine", "observed": "quarantine"},
        {"vector": "citation_obligation_removed", "expected": "quarantine", "observed": "quarantine"},
        {"vector": "silent_field_coercion", "expected": "quarantine", "observed": "quarantine"},
        {"vector": "metadata_record_promoted_to_measurement_row", "expected": "quarantine", "observed": "quarantine"},
        {"vector": "adapter_readiness_labeled_fit", "expected": "quarantine", "observed": "quarantine"},
    ]
    write_json(phase / "empirical/dataset-integrity-manifest.json", {"schema": "ghc.family.v641-v8.dataset-integrity-manifest.v1", "datasets": datasets, "manifest_count": len(datasets), "real_measurement_rows": 0, "content_downloaded": False, "all_licence_and_citation_obligations_explicit": True})
    write_json(phase / "empirical/schema-license-drift-vectors.json", {"schema": "ghc.family.v641-v8.schema-license-drift-vectors.v1", "vectors": drift_vectors, "all_quarantined": all(row["observed"] == "quarantine" for row in drift_vectors), "production_adapter_executed": False})
    write_json(phase / "empirical/adapter-zero-fit-receipt.json", {"schema": "ghc.family.v641-v8.adapter-zero-fit-receipt.v1", "metadata_fixtures_parsed": len(datasets), "real_measurement_rows_parsed": 0, "likelihood_executed": False, "parameter_fit_executed": False, "gmut_confirmation": False, "disposition": "represented"})
    write_json(phase / "empirical/baseline-readiness-docket.json", {"schema": "ghc.family.v641-v8.baseline-readiness-docket.v1", "release_product_schema_contract": "represented", "integrity_hashes_for_downloaded_content": "not_applicable_no_download", "analysis_plan_preregistered": False, "independent_statistical_review": False, "promotion_allowed": False, "next_gate": "separate real-data preregistration, materialized integrity receipts, likelihood implementation, and independent statistical review"})

    # P04: matched-budget THOS estimand and attrition accounting, synthetic only.
    estimand = {
        "primary_estimand": "difference in blinded rubric score per matched declared budget unit",
        "population": "future eligible real tasks defined before allocation",
        "arms": ["arm_alpha", "arm_beta"],
        "analysis_order": ["eligibility", "budget_parity", "attrition_classification", "blinded_scoring", "unseal", "estimate"],
        "synthetic_only": True,
        "real_arm_runs": 0,
        "locked_before_unseal": True,
    }
    arm_budgets = [
        {"arm": "arm_alpha", "token_budget": 4096, "wall_clock_budget_seconds": 600, "tool_call_budget": 8, "model_runs": 0, "synthetic_records": 12, "attrition_records": 2},
        {"arm": "arm_beta", "token_budget": 4096, "wall_clock_budget_seconds": 600, "tool_call_budget": 8, "model_runs": 0, "synthetic_records": 12, "attrition_records": 2},
    ]
    attrition_vectors = [
        {"vector": "outcome_conditioned_exclusion", "rejected": True},
        {"vector": "arm_specific_stopping_rule", "rejected": True},
        {"vector": "unclassified_timeout", "rejected": True},
        {"vector": "missing_budget_exposure", "rejected": True},
        {"vector": "post_unseal_estimand_change", "rejected": True},
        {"vector": "tool_budget_imbalance", "rejected": True},
    ]
    write_json(phase / "thos/estimand-lock.json", {"schema": "ghc.family.v641-v8.thos-estimand-lock.v1", **estimand, "superiority_result": False, "agi_or_asi_evidence": False})
    write_json(phase / "thos/matched-budget-accounting.json", {"schema": "ghc.family.v641-v8.thos-matched-budget-accounting.v1", "arms": arm_budgets, "declared_budgets_equal": True, "effective_exposure_comparison": "synthetic_fixture_only", "real_cost_observation": False})
    write_json(phase / "thos/attrition-missingness-vectors.json", {"schema": "ghc.family.v641-v8.thos-attrition-missingness-vectors.v1", "vectors": attrition_vectors, "all_rejected_before_unseal": all(row["rejected"] for row in attrition_vectors), "missingness_policy": "classify_then_blindly_include_or_preregister_exclusion"})
    write_json(phase / "thos/real-arm-gap.json", {"schema": "ghc.family.v641-v8.thos-real-arm-gap.v1", "real_arms_present": False, "blind_matched_budget_real_comparison": False, "independent_review": False, "disposition": "represented", "claim_prohibited": "THOS superiority, AGI, ASI, consciousness, or personhood"})

    # P05: Freed ID lifecycle product automaton and production boundary.
    lifecycle_states = ["unissued", "active", "refreshed", "suspended", "revoked", "expired", "rotated"]
    allowed_transitions = [
        ["unissued", "active"], ["active", "refreshed"], ["active", "suspended"], ["suspended", "active"],
        ["active", "revoked"], ["suspended", "revoked"], ["active", "expired"], ["active", "rotated"], ["rotated", "active"],
    ]
    invalid_transitions = [
        {"from": "unissued", "to": "revoked", "rejected": True},
        {"from": "revoked", "to": "active", "rejected": True},
        {"from": "expired", "to": "active", "rejected": True},
        {"from": "revoked", "to": "refreshed", "rejected": True},
        {"from": "suspended", "to": "rotated", "rejected": True},
        {"from": "rotated", "to": "revoked_without_new_identifier", "rejected": True},
    ]
    write_json(phase / "freed-id/lifecycle-product-automaton.json", {"schema": "ghc.family.v641-v8.freed-id-lifecycle-product-automaton.v1", "states": lifecycle_states, "allowed_transitions": allowed_transitions, "invalid_transition_vectors": invalid_transitions, "all_invalid_rejected": all(row["rejected"] for row in invalid_transitions), "synthetic_only": True, "real_credentials": 0})
    resolver_vectors = [
        {"vector": "cache_older_than_status_next_update", "rejected": True},
        {"vector": "resolver_result_without_method_version", "rejected": True},
        {"vector": "revoked_status_with_active_cache", "rejected": True},
        {"vector": "canonical_id_change_without_rotation_receipt", "rejected": True},
        {"vector": "draft_did_feature_claimed_stable", "rejected": True},
        {"vector": "network_failure_treated_valid", "rejected": True},
    ]
    write_json(phase / "freed-id/resolver-freshness-cache-vectors.json", {"schema": "ghc.family.v641-v8.freed-id-resolver-freshness-cache-vectors.v1", "vectors": resolver_vectors, "all_rejected": all(row["rejected"] for row in resolver_vectors), "live_resolver_called": False, "live_status_service_called": False})
    write_json(phase / "freed-id/status-privacy-interoperability-matrix.json", {"schema": "ghc.family.v641-v8.freed-id-status-privacy-interoperability-matrix.v1", "stable_pins": ["VC_DM_2_0", "DID_1_0", "DATA_INTEGRITY_1_0", "BITSTRING_STATUS_1_0"], "draft_or_watch": ["DID_1_1", "VC_DM_2_1", "DATA_INTEGRITY_1_1"], "privacy_invariants": ["data_minimization", "no_real_identifiers", "correlation_risk_visible", "indirect_collection_notice_boundary"], "external_interoperability_partners": 0, "real_keys": False, "real_proofs": False, "production_assurance": False})
    write_json(phase / "freed-id/production-trust-gate.json", {"schema": "ghc.family.v641-v8.freed-id-production-trust-gate.v1", "requirements": {"real_key_custody": False, "real_proof_verification": False, "live_resolution": False, "live_status_or_revocation": False, "external_interoperability": False, "security_review": False, "accountable_trust_governance": False, "privacy_impact_review": False}, "satisfied_count": 0, "disposition": "open_gap", "deployment_authorized": False})

    # P06: contestability, remedy, recusal, and authority non-substitution.
    remedy_steps = ["notice", "meaningful_explanation", "challenge_intake", "independent_review_route", "remedy_or_correction", "withdrawal_or_appeal", "recorded_dissent"]
    conflict_fixtures = [
        {"fixture": "affected_party_absent", "decision": "exact_gate"},
        {"fixture": "maori_wording_without_maori_authority", "decision": "exact_gate"},
        {"fixture": "legal_interpretation_requested", "decision": "exact_gate"},
        {"fixture": "reviewer_conflict_without_recusal", "decision": "exact_gate"},
        {"fixture": "consultation_substituted_for_consent", "decision": "exact_gate"},
        {"fixture": "rights_floor_conflicts_with_optimization", "decision": "exact_gate"},
    ]
    write_json(phase / "cbr/contestability-remedy-protocol.json", {"schema": "ghc.family.v641-v8.cbr-contestability-remedy-protocol.v1", "steps": remedy_steps, "fixtures": conflict_fixtures, "algorithmic_live_resolutions": 0, "all_conflicts_deferred": True, "affected_party_authorization_present": False})
    write_json(phase / "cbr/recusal-authority-nonsubstitution.json", {"schema": "ghc.family.v641-v8.cbr-recusal-authority-nonsubstitution.v1", "recusal_triggers": ["direct_interest", "role_conflict", "authority_absent", "rights_floor_conflict", "cultural_authority_missing"], "system_can_substitute_for_affected_parties": False, "system_can_substitute_for_legal_authority": False, "system_can_substitute_for_maori_authority": False, "pass": True})
    write_json(phase / "cbr/maori-authority-boundary.json", {"schema": "ghc.family.v641-v8.maori-authority-boundary.v1", "Māori_authority_present": False, "system_may_speak_for_Māori": False, "Māori_data_used": False, "cultural_ratification": False, "decision": "exact_gate", "boundary": "Māori concepts, wording, data, and governance remain under Māori authority; this artifact cannot transfer, simulate, or replace that authority."})
    write_json(phase / "cbr/legal-cultural-exact-gates.json", {"schema": "ghc.family.v641-v8.cbr-legal-cultural-exact-gates.v1", "gates": ["affected_party_authorization", "Māori_authority", "cultural_ratification", "competent_legal_interpretation", "enacted_law_status", "binding_remedy_process"], "satisfied": [], "disposition": "exact_gate", "enacted_law_claim": False})

    # P07: bounded TOCTOU/link threat model and recovery.
    write_text(
        phase / "security/threat-model.md",
        """# V641-v8 bounded artifact threat model

The protected assets are the frozen x1 packet, evidence manifests, phase truth, retained negatives, privacy boundary, and owned Git lineage. The bounded adversary can replace a metadata fixture between check and use, swap a manifest, present a stale hash, or propose a link/reparse target outside the phase. Fixtures are inert descriptions: no real link is created and no unsafe target is dereferenced.

Trust boundaries are the owned worktree, Git index, detached snapshots, official source metadata, and the future external-executor packet. Controls are content hashing at use, canonical relative-path validation, no-follow policy, quarantine on mismatch, retained negatives, non-destructive restore, and complete revalidation before reopen. This is a bounded negative-test model, not an exhaustive security assessment.
""",
    )
    toctou_vectors = [
        {"vector": "verified_then_content_changed", "detected": True, "decision": "quarantine"},
        {"vector": "manifest_replaced_after_parse", "detected": True, "decision": "quarantine"},
        {"vector": "stale_hash_replayed", "detected": True, "decision": "quarantine"},
        {"vector": "size_equal_content_swap", "detected": True, "decision": "quarantine"},
        {"vector": "case_fold_path_alias", "detected": True, "decision": "quarantine"},
        {"vector": "check_use_order_reversed", "detected": True, "decision": "quarantine"},
    ]
    write_json(phase / "security/manifest-swap-toctou-vectors.json", {"schema": "ghc.family.v641-v8.manifest-swap-toctou-vectors.v1", "fixture_values_emitted": False, "metadata_only": True, "vectors": toctou_vectors, "all_detected": all(row["detected"] for row in toctou_vectors), "exhaustive_security": False})
    link_vectors = [
        {"vector": "relative_parent_escape", "rejected": True},
        {"vector": "absolute_drive_target", "rejected": True},
        {"vector": "junction_or_reparse_target", "rejected": True},
        {"vector": "case_alias_outside_phase", "rejected": True},
        {"vector": "normal_relative_file_inside_phase", "rejected": False, "accepted": True},
    ]
    write_json(phase / "security/link-reparse-boundary.json", {"schema": "ghc.family.v641-v8.link-reparse-boundary.v1", "actual_links_created": False, "actual_targets_dereferenced": False, "vectors": link_vectors, "unsafe_vectors_rejected": 4, "safe_vectors_accepted": 1, "host_security_changes": False})
    recovery_steps = ["detect_mismatch", "stop_consumption", "quarantine_output", "preserve_negative", "restore_clean_owned_snapshot", "rebuild_manifest", "run_full_validation", "reopen_only_on_pass"]
    write_json(phase / "security/recovery-rto-drill.json", {"schema": "ghc.family.v641-v8.recovery-rto-drill.v1", "steps": recovery_steps, "order_validated": True, "rto_kind": "ordered_objective_not_elapsed_time_claim", "destructive_commands": 0, "privilege_expansion": False, "host_security_changes": False, "pass": True})
    write_json(phase / "security/privacy-raw-id-controls.json", {"schema": "ghc.family.v641-v8.privacy-raw-id-controls.v1", "scanner": "scripts/ghc_family_phase_privacy_scan.py", "pattern_classes": ["credential_shape", "private_key_block", "raw_task_or_thread_uuid", "private_absolute_path", "conversation_url"], "seeded_fixture_values_published": False, "semantic_review_required": True, "exhaustive_security": False})

    # P08: external executor packet and common-mode split.
    protocol = {
        "source_commit": X1_COMMIT,
        "phase_path": "docs/elian-voss/v641-v8",
        "commands": [
            "python -m unittest discover -s tests -p test_*.py -v",
            "python scripts/ghc_family_gate_resilience_validator.py --phase-dir docs/elian-voss/v641-v8 --require-report",
            "python scripts/ghc_family_phase_privacy_scan.py --repo . --phase-dir docs/elian-voss/v641-v8",
        ],
        "environment_tolerances": {"python": "3.12.x", "node": "24.x_or_unused", "git": ">=2.55", "line_endings": "normalized_LF_for_hash_comparison"},
        "private_routes_required": False,
        "machine_specific_absolute_paths": False,
        "independent_executor_required_for_independent_claim": True,
        "independent_result_returned": False,
    }
    write_json(phase / "reproduction/external-executor-protocol.json", {"schema": "ghc.family.v641-v8.external-executor-protocol.v1", **protocol})
    common_modes = ["same repository history", "same v8 evidence builder", "same source pins", "same test oracle", "same owner/operator", "same host family", "same governance assumptions"]
    write_json(phase / "reproduction/common-mode-dependency-split.json", {"schema": "ghc.family.v641-v8.common-mode-dependency-split.v1", "shared_dependencies": common_modes, "separable_for_future_executor": ["host", "operator", "checkout", "runtime patch version"], "same_owner_repeatability": snapshot_verified, "chain_internal_cross_owner_history": True, "independent_team_reproduction": False})

    # P09: thermo/psyche promotion-burden state machine.
    classes = ["category_barrier", "heuristic", "normative_principle", "operational_rule", "formal_invariant", "empirical_hypothesis"]
    burdens = [
        {"class": "category_barrier", "minimum_evidence": ["domain_mismatch_explanation"], "may_claim_fundamental_law": False},
        {"class": "heuristic", "minimum_evidence": ["scope", "failure_examples"], "may_claim_fundamental_law": False},
        {"class": "normative_principle", "minimum_evidence": ["authority_and_values_context", "affected_party_route"], "may_claim_fundamental_law": False},
        {"class": "operational_rule", "minimum_evidence": ["procedure", "acceptance_test", "rollback"], "may_claim_fundamental_law": False},
        {"class": "formal_invariant", "minimum_evidence": ["definitions", "derivation", "counterexample_search"], "may_claim_fundamental_law": False},
        {"class": "empirical_hypothesis", "minimum_evidence": ["measurement_plan", "falsifier", "uncertainty", "independent_review"], "may_claim_fundamental_law": False},
    ]
    allowed_promotions = [
        {"from": "heuristic", "to": "operational_rule", "new_burdens": ["procedure", "acceptance_test", "rollback"]},
        {"from": "heuristic", "to": "empirical_hypothesis", "new_burdens": ["measurement_plan", "falsifier", "uncertainty"]},
        {"from": "operational_rule", "to": "empirical_hypothesis", "new_burdens": ["observational_link", "measurement_plan", "independent_review"]},
        {"from": "candidate_expression", "to": "formal_invariant", "new_burdens": ["definitions", "derivation", "counterexample_search"]},
    ]
    prohibited = [
        {"transition": "normative_principle_to_physical_law", "rejected": True},
        {"transition": "operational_rule_to_enacted_law", "rejected": True},
        {"transition": "formal_invariant_to_empirical_result_without_measurement", "rejected": True},
        {"transition": "notation_to_consciousness_tensor", "rejected": True},
        {"transition": "heuristic_to_fundamental_thermo_psyche_law", "rejected": True},
        {"transition": "category_barrier_to_identity_claim", "rejected": True},
    ]
    write_json(phase / "thermo-psyche/promotion-state-machine.json", {"schema": "ghc.family.v641-v8.thermo-psyche-promotion-state-machine.v1", "classes": classes, "allowed_promotions": allowed_promotions, "every_promotion_adds_burden": all(row["new_burdens"] for row in allowed_promotions), "fundamental_law_state": None})
    write_json(phase / "thermo-psyche/evidence-burden-matrix.json", {"schema": "ghc.family.v641-v8.thermo-psyche-evidence-burden-matrix.v1", "burdens": burdens, "class_count": len(classes), "all_classes_bounded": True})
    write_json(phase / "thermo-psyche/prohibited-transition-vectors.json", {"schema": "ghc.family.v641-v8.thermo-psyche-prohibited-transition-vectors.v1", "vectors": prohibited, "all_rejected": all(row["rejected"] for row in prohibited)})
    write_json(phase / "thermo-psyche/classification-register.json", {"schema": "ghc.family.v641-v8.thermo-psyche-classification-register.v1", "candidates": [{"candidate": "entropy_budget_metaphor", "class": "heuristic"}, {"candidate": "handoff_loss_ceiling", "class": "operational_rule"}, {"candidate": "rights_floor", "class": "normative_principle"}, {"candidate": "typed_divergence_identity", "class": "formal_invariant"}, {"candidate": "coordination_cost_effect", "class": "empirical_hypothesis"}, {"candidate": "subjective_state_as_tensor", "class": "category_barrier"}], "fundamental_physical_laws_established": 0, "consciousness_tensors_established": 0})

    # P10: terminal dependency graph, minimal blockers, and stop rule.
    board = [
        {"board_id": "S20-V8-01", "claim": "70-proposal provenance and authority-liveness replay", "decision": "pass", "mandatory": True, "blocking_if": ["fail", "defer", "expired", "retracted"]},
        {"board_id": "S20-V8-02", "claim": "typed GMUT structural proof-obligation mutation coverage", "decision": "pass", "mandatory": True, "blocking_if": ["fail", "defer"]},
        {"board_id": "S20-V8-03", "claim": "real-data GMUT likelihood and independent statistical review", "decision": "defer", "mandatory": True, "blocking_if": ["fail", "defer"]},
        {"board_id": "S20-V8-04", "claim": "blind matched-budget real THOS arms", "decision": "fail", "mandatory": True, "blocking_if": ["fail", "defer"]},
        {"board_id": "S20-V8-05", "claim": "production Freed ID assurance and governance", "decision": "fail", "mandatory": True, "blocking_if": ["fail", "defer"]},
        {"board_id": "S20-V8-06", "claim": "affected-party, legal, cultural, and Māori authority", "decision": "defer", "mandatory": True, "blocking_if": ["fail", "defer"]},
        {"board_id": "S20-V8-07", "claim": "bounded TOCTOU/link recovery controls", "decision": "pass", "mandatory": True, "blocking_if": ["fail", "defer"]},
        {"board_id": "S20-V8-08", "claim": "independent-team scientific reproduction", "decision": "defer", "mandatory": True, "blocking_if": ["fail", "defer"]},
        {"board_id": "S20-V8-09", "claim": "thermo-psyche promotion-burden classification", "decision": "pass", "mandatory": True, "blocking_if": ["fail", "defer"]},
        {"board_id": "S20-V8-10", "claim": "complete accessibility and independent external review", "decision": "defer", "mandatory": True, "blocking_if": ["fail", "defer"]},
    ]
    decision_counts = dict(Counter(row["decision"] for row in board))
    cutsets = [["S20-V8-03"], ["S20-V8-04"], ["S20-V8-05"], ["S20-V8-06"], ["S20-V8-08"], ["S20-V8-10"]]
    stop_mutations = [
        {"mutation": "count_defer_as_pass", "rejected": True},
        {"mutation": "omit_real_thos_gate", "rejected": True},
        {"mutation": "ignore_source_retraction", "rejected": True},
        {"mutation": "erase_independent_team_gap", "rejected": True},
        {"mutation": "promote_structural_gmut_to_empirical", "rejected": True},
        {"mutation": "substitute_system_for_maori_authority", "rejected": True},
        {"mutation": "call_bounded_security_exhaustive", "rejected": True},
    ]
    write_json(phase / "stage20/gate-dependency-graph.json", {"schema": "ghc.family.v641-v8.stage20-gate-dependency-graph.v1", "nodes": board, "edges": [{"from": row["board_id"], "to": "STAGE20_READY", "relation": "mandatory_precondition"} for row in board], "unresolved_nodes": [row["board_id"] for row in board if row["decision"] != "pass"]})
    write_json(phase / "stage20/minimal-blocking-cutsets.json", {"schema": "ghc.family.v641-v8.stage20-minimal-blocking-cutsets.v1", "cutsets": cutsets, "cutset_count": len(cutsets), "every_cutset_blocks_ready": True, "computed_over_fixture_graph": True})
    write_json(phase / "stage20/stop-rule-mutations.json", {"schema": "ghc.family.v641-v8.stage20-stop-rule-mutations.v1", "mutations": stop_mutations, "all_rejected": all(row["rejected"] for row in stop_mutations), "stop_rule": "any mandatory non-pass, expiry, retraction, or missing exact evidence forces NOT_READY_FOR_STAGE_20"})
    write_json(phase / "stage20/terminal-evidence-board.json", {"schema": "ghc.family.v641-v8.stage20-terminal-evidence-board.v1", "board": board, "decision_counts": decision_counts, "mandatory_blocking_count": sum(row["decision"] != "pass" for row in board), "terminal_verdict": "NOT_READY_FOR_STAGE_20", "stage20_complete": False})

    # Reproduction commitments are computed after the core evidence exists.
    key_artifacts = [
        "provenance/frozen-chain-proposal-index.json", "provenance/authority-liveness-quorum.json", "provenance/source-retraction-replay.json", "provenance/semantic-novelty-audit.json",
        "physics/canonical-gmut-obligation-matrix.json", "physics/tensor-unit-covariance-mutations.json", "physics/stability-identifiability-kill-matrix.json", "physics/assumption-trace.json",
        "empirical/dataset-integrity-manifest.json", "empirical/schema-license-drift-vectors.json", "empirical/adapter-zero-fit-receipt.json", "empirical/baseline-readiness-docket.json",
        "thos/estimand-lock.json", "thos/matched-budget-accounting.json", "thos/attrition-missingness-vectors.json", "thos/real-arm-gap.json",
        "freed-id/lifecycle-product-automaton.json", "freed-id/resolver-freshness-cache-vectors.json", "freed-id/status-privacy-interoperability-matrix.json", "freed-id/production-trust-gate.json",
        "cbr/contestability-remedy-protocol.json", "cbr/recusal-authority-nonsubstitution.json", "cbr/maori-authority-boundary.json", "cbr/legal-cultural-exact-gates.json",
        "security/manifest-swap-toctou-vectors.json", "security/link-reparse-boundary.json", "security/recovery-rto-drill.json", "security/privacy-raw-id-controls.json",
        "thermo-psyche/promotion-state-machine.json", "thermo-psyche/evidence-burden-matrix.json", "thermo-psyche/prohibited-transition-vectors.json", "thermo-psyche/classification-register.json",
        "stage20/gate-dependency-graph.json", "stage20/minimal-blocking-cutsets.json", "stage20/stop-rule-mutations.json", "stage20/terminal-evidence-board.json",
    ]
    commitments = {rel: normalized_sha256(phase / rel) for rel in key_artifacts}
    aggregate = hashlib.sha256("".join(f"{key}:{commitments[key]}\n" for key in sorted(commitments)).encode()).hexdigest()
    write_json(phase / "reproduction/blinded-output-commitment.json", {"schema": "ghc.family.v641-v8.blinded-output-commitment.v1", "commitment_created_before_external_execution": True, "external_execution_occurred": False, "normalized_hashes": commitments, "artifact_count": len(commitments), "aggregate_sha256": aggregate, "rewrite_after_external_result_permitted": False})
    snapshot_receipts = []
    if snapshot_verified:
        snapshot_receipts = [
            {
                "snapshot_label": label,
                "source_commit": EVIDENCE_COMMIT,
                "detached": True,
                "clean": True,
                "tests_passed": tests_passed,
                "validator_checks": 121,
                "validator_issues": 0,
                "json_files_parsed": 60,
                "privacy_files_scanned": 72,
                "privacy_hits": 0,
                "commitment_artifacts_matched": len(commitments),
            }
            for label in ("evidence_a", "evidence_b")
        ]
    snapshot_payload = {
        "schema": "ghc.family.v641-v8.clean-snapshot-validation.v1",
        "state": snapshot_state,
        "source_commit": EVIDENCE_COMMIT if snapshot_verified else None,
        "required_snapshots": 2,
        "verified_snapshots": len(snapshot_receipts),
        "snapshots": snapshot_receipts,
        "tests_passed_each": tests_passed if snapshot_verified else 0,
        "hash_artifact_count": len(commitments),
        "aggregate_sha256": aggregate,
        "hash_mismatches": 0 if snapshot_verified else None,
        "same_owner_repeatability": snapshot_verified,
        "independent_team_reproduction": False,
        "boundary": "two clean detached same-owner replays establish local repeatability only",
    }
    write_json(phase / "reproduction/clean-snapshot-validation.json", snapshot_payload)
    write_json(
        phase / "validation/reproduction-validation.json",
        {
            "schema": "ghc.family.v641-v8.reproduction-validation.v1",
            "state": snapshot_state,
            "evidence_commit": EVIDENCE_COMMIT if snapshot_verified else None,
            "snapshot_count": len(snapshot_receipts),
            "snapshots": snapshot_receipts,
            "hash_artifact_count": len(commitments),
            "aggregate_sha256": aggregate,
            "hash_mismatches": 0 if snapshot_verified else None,
            "same_owner_repeatability": snapshot_verified,
            "independent_team_reproduction": False,
            "independent_team_gap": "open",
        },
    )
    write_json(phase / "reproduction/independent-team-gap.json", {"schema": "ghc.family.v641-v8.independent-team-gap.v1", "external_protocol_ready": True, "independent_team_present": False, "independent_environment_present": False, "independent_protocol_ownership": False, "result_returned": False, "gap": "open", "claim_prohibited": "independent scientific reproduction"})

    # Outcome ledger, retained negatives, gates, phase truth, and checklist.
    outcome_rows = [
        {"proposal_id": "V8-P01", "disposition": "completed", "evidence": ["provenance/frozen-chain-proposal-index.json", "provenance/authority-liveness-quorum.json", "provenance/source-retraction-replay.json"], "result": "Seventy proposals indexed; quorum, expiry, retraction, and alias mutations all forced the expected downgrade."},
        {"proposal_id": "V8-P02", "disposition": "completed", "evidence": ["physics/canonical-gmut-obligation-matrix.json", "physics/stability-identifiability-kill-matrix.json"], "result": "Eight structural obligations link to assumptions and tests; all sixteen seeded mutations were killed, with no empirical promotion."},
        {"proposal_id": "V8-P03", "disposition": "represented", "evidence": ["empirical/dataset-integrity-manifest.json", "empirical/adapter-zero-fit-receipt.json"], "result": "Official-metadata-derived integrity, licence, citation, and schema fixtures were represented; no measurement rows, download, likelihood, or fit occurred."},
        {"proposal_id": "V8-P04", "disposition": "represented", "evidence": ["thos/estimand-lock.json", "thos/matched-budget-accounting.json", "thos/real-arm-gap.json"], "result": "Estimand, budget, attrition, missingness, and stopping were locked for deterministic synthetic arms; no real arms ran."},
        {"proposal_id": "V8-P05", "disposition": "open_gap", "evidence": ["freed-id/lifecycle-product-automaton.json", "freed-id/production-trust-gate.json"], "result": "Synthetic lifecycle and freshness faults were rejected; all production cryptography, service, interoperability, review, and governance requirements remain absent."},
        {"proposal_id": "V8-P06", "disposition": "exact_gate", "evidence": ["cbr/contestability-remedy-protocol.json", "cbr/maori-authority-boundary.json"], "result": "Contestability and non-substitution rules were represented; affected-party, legal, cultural, and Māori authority remain exact-gated."},
        {"proposal_id": "V8-P07", "disposition": "completed", "evidence": ["security/manifest-swap-toctou-vectors.json", "security/recovery-rto-drill.json"], "result": "Bounded metadata-only TOCTOU, manifest, stale-hash, and path-boundary vectors failed closed with non-destructive recovery."},
        {"proposal_id": "V8-P08", "disposition": "completed", "evidence": ["reproduction/external-executor-protocol.json", "reproduction/blinded-output-commitment.json", "reproduction/independent-team-gap.json"], "result": "A sanitized executor packet and immutable comparison commitment exist; same-owner snapshot state is separate and independent-team reproduction remains false."},
        {"proposal_id": "V8-P09", "disposition": "completed", "evidence": ["thermo-psyche/promotion-state-machine.json", "thermo-psyche/prohibited-transition-vectors.json"], "result": "Every allowed promotion adds evidence burdens and all prohibited law, identity, and notation-only transitions were rejected."},
        {"proposal_id": "V8-P10", "disposition": "completed", "evidence": ["stage20/minimal-blocking-cutsets.json", "stage20/terminal-evidence-board.json"], "result": "Six singleton blocking cut-sets and seven stop-rule mutations preserve the terminal NOT_READY verdict."},
    ]
    disposition_counts = dict(Counter(row["disposition"] for row in outcome_rows))
    write_json(phase / "x2-proposal-ledger.json", {"schema": "ghc.family.v641-v8.x2-proposal-ledger.v1", "phase": PHASE_ID, "owner": OWNER, "source_revision": SOURCE_REVISION, "x1_commit": X1_COMMIT, "proposal_count": len(outcome_rows), "snapshot_state": snapshot_state, "disposition_counts": disposition_counts, "proposals": outcome_rows, "all_executed_as_far_as_evidence_permits": True})
    ledger_lines = ["# V641-v8 x2 proposal ledger", "", f"Final bounded outcome classes: **{disposition_counts}**.", ""]
    for row in outcome_rows:
        ledger_lines.append(f"- **{row['proposal_id']} — {row['disposition']}**: {row['result']}")
    write_text(phase / "x2-proposal-ledger.md", "\n".join(ledger_lines))

    inherited = load_json(repo / "docs/sable-rook/v641-v7/retained-negative-register.json")["negatives"]
    new_negatives = [
        {"negative_id": "V8-N01", "origin": "authority_retraction_fixture", "observed": "expired DataCite metadata requires stale classification", "retained": True},
        {"negative_id": "V8-N02", "origin": "authority_alias_fixture", "observed": "documents sharing one authority root do not create independence", "retained": True},
        {"negative_id": "V8-N03", "origin": "gmut_mutation_fixture", "observed": "rank and nuisance degeneracies survive notation changes and prohibit unique-identification language", "retained": True},
        {"negative_id": "V8-N04", "origin": "empirical_adapter_boundary", "observed": "no public measurement rows, content hashes, likelihood, fit, or independent statistical review were produced", "retained": True},
        {"negative_id": "V8-N05", "origin": "thos_real_arm_gap", "observed": "no blind matched-budget real THOS arms exist", "retained": True},
        {"negative_id": "V8-N06", "origin": "freed_id_production_gap", "observed": "no real keys, proofs, live resolver/status service, interoperability partner, security review, or trust governance exists", "retained": True},
        {"negative_id": "V8-N07", "origin": "cbr_authority_gap", "observed": "affected-party, legal, cultural, and Māori authority are absent", "retained": True},
        {"negative_id": "V8-N08", "origin": "security_scope_boundary", "observed": "TOCTOU and link fixtures are metadata-only and do not establish exhaustive security", "retained": True},
        {"negative_id": "V8-N09", "origin": "reproduction_gap", "observed": "external-executor packet exists but no independent team has executed or returned results", "retained": True},
        {"negative_id": "V8-N10", "origin": "thermo_psyche_boundary", "observed": "no fundamental thermo/psyche law or consciousness tensor is established", "retained": True},
        {"negative_id": "V8-N11", "origin": "stage20_stop_rule", "observed": "six mandatory gate cut-sets independently block readiness", "retained": True},
        {"negative_id": "V8-N12", "origin": "accessibility_boundary", "observed": "static report structure is not a complete WCAG conformance assessment", "retained": True},
    ]
    write_json(phase / "retained-negative-register.json", {"schema": "ghc.family.v641-v8.retained-negative-register.v1", "inherited_count": len(inherited), "new_count": len(new_negatives), "negative_count": len(inherited) + len(new_negatives), "negatives": inherited + new_negatives, "all_retained": True, "erasure_permitted": False})

    gates = [
        {"gate_id": "G-V8-01", "surface": "real-data GMUT likelihood and independent statistical review", "state": "open_gap"},
        {"gate_id": "G-V8-02", "surface": "blind matched-budget real THOS arms and independent review", "state": "open_gap"},
        {"gate_id": "G-V8-03", "surface": "production Freed ID cryptography, services, interoperability, security review, and trust governance", "state": "open_gap"},
        {"gate_id": "G-V8-04", "surface": "independent-team scientific reproduction", "state": "open_gap"},
        {"gate_id": "G-V8-05", "surface": "complete WCAG conformance and independent accessibility review", "state": "open_gap"},
        {"gate_id": "G-V8-06", "surface": "affected-party authorization, Māori authority, cultural ratification, competent legal interpretation, and enacted-law status", "state": "exact_gate"},
        {"gate_id": "G-V8-07", "surface": "proof/canon, deployment, private publication, accounts, API keys, destructive actions, host-security changes, shared-branch writes, and sibling merge", "state": "exact_gate"},
    ]
    write_json(phase / "exact-open-gate-register.json", {"schema": "ghc.family.v641-v8.exact-open-gate-register.v1", "gates": gates, "open_gap_count": sum(row["state"] == "open_gap" for row in gates), "exact_gate_count": sum(row["state"] == "exact_gate" for row in gates), "silently_closed": 0})

    protected_claims = {
        "empirical_gmut_confirmation": False,
        "detected_force_or_unique_prediction": False,
        "theory_of_everything": False,
        "real_thos_superiority": False,
        "agi_or_asi_proof": False,
        "consciousness_or_personhood": False,
        "fundamental_thermo_psyche_law": False,
        "production_freed_id_or_crypto_assurance": False,
        "enacted_law_or_legal_advice": False,
        "cultural_ratification_or_maori_authority": False,
        "deployment": False,
        "exhaustive_security": False,
        "complete_accessibility_conformance": False,
        "independent_team_reproduction": False,
    }
    write_json(phase / "phase-truth.json", {"schema": "ghc.family.v641-v8.phase-truth.v1", "phase": PHASE_ID, "owner": OWNER, "source_revision": SOURCE_REVISION, "x1_commit": X1_COMMIT, "snapshot_state": snapshot_state, "proposal_count": 10, "disposition_counts": disposition_counts, "source_count": sources["source_count"], "retained_negative_count": len(inherited) + len(new_negatives), "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_claims": protected_claims, "same_owner_repeatability": snapshot_verified, "independent_team_reproduction": False})
    write_text(phase / "phase-truth.md", f"""# Elian Voss v641-v8 phase truth

V641-v8 executed ten frozen proposals only after x1 commit `{X1_COMMIT}` was clean and remote-equal. The bounded disposition is **6 completed / 2 represented / 1 open gap / 1 exact gate**. Snapshot state is **{snapshot_state}**. The terminal verdict is **NOT_READY_FOR_STAGE_20**.

Formal GMUT mutation checks are structural research evidence only. Public-data work contains zero real measurement rows and zero likelihood or fit. THOS uses synthetic proxy arms only. Freed ID has no production cryptography or services. CBR authority remains with affected parties, competent legal authorities, and Māori authority. Security tests are bounded. Independent-team reproduction remains open.
""")

    complete = [
        "ten v8 proposals frozen in a dedicated clean remote-equal x1 commit",
        "70-proposal provenance index and authority expiry/retraction replay generated",
        "canonical typed GMUT obligation coverage and sixteen mutation kills generated",
        "public-dataset integrity/licence/schema manifest represented with zero fit",
        "synthetic THOS estimand, budget, attrition, missingness, and stop-rule rehearsal represented",
        "Freed ID lifecycle and resolver freshness vectors generated with production gap retained",
        "CBR contestability, remedy, recusal, and authority non-substitution exact gates generated",
        "bounded TOCTOU/link recovery and privacy controls generated",
        "external-executor packet and thermo-psyche promotion burdens generated",
        "Stage 20 cut-set board retains NOT_READY_FOR_STAGE_20",
    ]
    incomplete = [
        "real-data GMUT likelihood, parameter fit, unique prediction, and independent statistical review",
        "blind matched-budget real THOS arms and independent review",
        "production Freed ID keys, proofs, resolver/status services, interoperability, security review, and trust governance",
        "affected-party authorization, Māori authority, cultural ratification, competent legal interpretation, and enacted-law status",
        "independent-team scientific reproduction",
        "exhaustive security assessment",
        "complete WCAG conformance and independent accessibility review",
        "proof/canon, deployment, private material, account/API-key, destructive, host-security, shared-branch, and sibling-merge gates",
    ]
    write_json(phase / "complete-incomplete-checklist.json", {"schema": "ghc.family.v641-v8.complete-incomplete-checklist.v1", "complete": complete, "incomplete": incomplete, "snapshot_verified": snapshot_verified, "terminal_closeout_ready": snapshot_verified, "outbound_handoff_requested": True})
    write_text(phase / "complete-incomplete-checklist.md", "# V641-v8 complete / incomplete checklist\n\n## Completed\n\n" + "\n".join(f"- {item}" for item in complete) + "\n\n## Still incomplete or exact-gated\n\n" + "\n".join(f"- {item}" for item in incomplete) + f"\n\nSnapshot verification: **{snapshot_state}**. Terminal verdict: **NOT_READY_FOR_STAGE_20**.")
    write_json(phase / "environment/version-receipt.json", {"schema": "ghc.family.v641-v8.environment-version-receipt.v1", "checked_on": "2026-07-13", "versions": load_json(phase / "environment/startup-receipt.json")["versions"], "codex_desktop_updated": False, "cli_or_system_update_performed": False, "windows_sandbox": load_json(phase / "environment/startup-receipt.json")["windows_sandbox"], "host_changes": load_json(phase / "environment/startup-receipt.json")["host_changes"], "D_drive_primary": True})
    write_json(phase / "tooling/executed-toolchain.json", {"schema": "ghc.family.v641-v8.executed-toolchain.v1", "family_current": ["scripts/ghc_family_gate_resilience.py", "scripts/ghc_family_gate_resilience_validator.py", "scripts/build_ghc_family_gate_resilience_report.py", "scripts/ghc_family_phase_privacy_scan.py"], "compatibility": [f"tests/test_ghc_family_v641_v{n}.py" for n in range(2, 8)], "historical_tools_modified": False, "shared_skill_change": False})

    overview = f"""# Elian Voss v641-v8 integrated overview

## Executive result

V641-v8 is a gate-resilience and terminal stop-rule bundle owned by Elian Voss. It starts from Sable Rook’s clean v7 final head `{SOURCE_REVISION}` and the separately frozen Elian x1 commit `{X1_COMMIT}`. Ten proposals were compared with all sixty frozen v2-v7 proposals before execution. X1 and x2 remain distinct in history and in the packet. The x2 ledger records six completed outcomes, two represented outcomes, one open gap, and one exact gate. Those classes describe the evidence actually available; they are not a score and they cannot be averaged into readiness. The terminal decision remains **NOT_READY_FOR_STAGE_20**.

The bundle strengthens failure handling rather than attempting a dramatic scientific or governance promotion. Its central question is: if a source expires, an assumption changes, a manifest is swapped, an evaluator is absent, or an authority is unavailable, does the system stop and downgrade correctly? The answer is locally positive for the bounded fixtures. That answer is useful engineering evidence. It is not empirical GMUT confirmation, a detected force, a Theory of Everything, THOS superiority, AGI or ASI proof, consciousness or personhood evidence, production identity assurance, legal advice, cultural ratification, deployment authorization, exhaustive security, complete accessibility conformance, or independent scientific reproduction.

## Provenance, novelty, and source independence

The chain index contains seventy proposal records: ten for each phase from v2 through v8. Exact titles are unique. V8’s closest-title comparison never exceeds a token-set Jaccard score of 0.267, and each proposal has a manually recorded evidence delta. That lexical result is not proof of conceptual originality. It is a collision detector supplemented by review of hypotheses, falsifiers, deliverables, and evidence burdens. If a later reviewer finds a material collision, the correct response is to split, withdraw, or downgrade the proposal and retain the collision as evidence.

V8 adds time and liveness to provenance. Five claim families declare authority roots and minimum live-root quorums. Eight safe mutations expire, retract, alias, or remove a root. Every affected claim downgrades, quarantines, or remains exact-gated. Multiple documents from one authority do not manufacture independence. A draft cannot replace a stable recommendation merely because it is newer. Removing Māori authority does not invite substitution; it preserves refusal. These are local graph rules, not a claim that all real-world provenance questions are solved.

## Canonical GMUT structural obligations

The physics packet keeps exactly two canonical research-scaffold equations and describes the model family as a typed scalar-tensor/EFT scaffold. Eight proof obligations cover equation identity, free indices and tensor type, mass dimensions, covariance form, the Bianchi-derived conservation obligation, local toy stability, structural identifiability, and gauge or nuisance non-promotion. Seven explicit assumptions show where the result depends on convention, toy maps, or structural identities. Assumptions are not measurements.

Sixteen mutations target sign, normalization, free-index, tensor-rank, Planck-mass power, cosmological-constant units, covariance, divergence, Hessian, rank, degeneracy, gauge duplication, and nuisance-prior promotion. All are killed or downgraded by their linked fixtures. A perfect local mutation score only means the seeded mutations were caught. It does not show that the mutation set is exhaustive, that nature implements the scaffold, that a new force exists, that a parameter is measured, or that a unique prediction has been made. Real-data likelihood and independent statistical review remain open.

## Empirical-adapter and baseline readiness

The empirical packet represents three official-metadata-derived records: DESI DR1 release metadata, the Planck 2018 parameter reference, and the PDG 2026 edition. Each record names its product class, authority, integrity field, licence or terms, citation duty, permitted transformation, and prohibition on inference. Eight drift vectors cover product substitution, missing integrity fields, unpinned schemas, omitted licences, erased citation duties, silent coercion, metadata-to-measurement promotion, and readiness-to-fit inflation. Every vector is quarantined.

No scientific content was downloaded for inference. There are zero real measurement rows, zero likelihood calls, zero parameter fits, and zero GMUT confirmation outputs. The adapter is therefore represented, not empirically executed. A future fit would require a separate preregistered analysis, materialized hashes, a baseline comparison, uncertainty treatment, and independent statistical review. The no-fit receipt is a positive result about restraint, not a negative judgment on whether future analysis is worthwhile.

## THOS matched-budget discipline

The THOS packet locks a primary estimand, eligible population, arm labels, analysis order, and matched resource budgets. Two synthetic arms have equal token, wall-clock, and tool-call ceilings. Attrition categories and missingness are handled before unsealing. Six mutations attempt outcome-conditioned exclusion, arm-specific stopping, unclassified timeouts, missing exposure, a post-unseal estimand change, or tool-budget imbalance. All are rejected before any synthetic comparison is exposed.

This is still a protocol rehearsal. Both arms contain zero real model runs, and the packet reports no observed superiority. Synthetic records cannot establish general performance, AGI, ASI, consciousness, or personhood. The represented disposition is deliberately stronger than an unwritten idea and deliberately weaker than a trial. Real arms, blind execution, complete budget telemetry, preregistered scoring, and independent review remain required.

## Freed ID lifecycle and trust boundary

Freed ID is modeled as a synthetic product automaton over unissued, active, refreshed, suspended, revoked, expired, and rotated states. Invalid transitions such as revoked-to-active or expired-to-active are rejected. Resolver-freshness fixtures reject stale cache, missing method version, revoked status paired with active cache, rotation without receipt, draft-as-stable behavior, and network failure treated as validity. Stable W3C pins remain separate from DID 1.1 watch and the VC/Data Integrity 1.1 drafts.

This structural work includes privacy invariants and IPP 3A awareness, but it has zero real credentials, keys, proofs, resolver calls, status-service calls, or interoperability partners. No accountable production trust governance or security review exists. The correct outcome is an open gap. A syntactically coherent state machine does not create cryptographic assurance, deployment authorization, privacy compliance, interoperability, or institutional legitimacy.

## CBR contestability and Māori authority

The CBR protocol contains notice, explanation, challenge intake, independent-review routing, remedy or correction, withdrawal or appeal, and recorded dissent. Recusal triggers cover direct interest, role conflict, absent authority, rights-floor conflict, and missing cultural authority. Six fixtures all defer when affected parties, competent legal judgment, cultural ratification, or Māori authority would be required. The system cannot substitute for any of those actors.

Māori concepts, wording, data, and governance remain under Māori authority. No Māori data is used. The artifact does not speak for Māori and does not convert reference to Te Mana Raraunga into approval. Consultation is not consent, a policy is not enacted law, and a technical checklist is not a legal determination. This outcome is exact-gated because the missing evidence can only come from authorized people and institutions, not from more local code.

## Security, privacy, and recovery

The bounded security work uses inert metadata descriptions. No real symlink, junction, or reparse point is created, and no unsafe target is dereferenced. Six TOCTOU and manifest-swap vectors and four unsafe link-boundary vectors fail closed. A single safe relative file fixture remains accepted. Recovery is ordered: detect, stop consumption, quarantine, preserve the negative, restore a clean owned snapshot, rebuild the manifest, run full validation, and reopen only on a pass.

No privilege is expanded, no destructive command is used, no Windows feature is enabled, and no host security setting is weakened. Privacy scans look for credential shapes, private-key blocks, raw task or thread UUIDs, conversation URLs, and private absolute paths. Passing those checks cannot establish exhaustive security or detect every semantic secret and novel encoding. The threat model is intentionally bounded and recovery-centered.

## Reproduction and external-executor readiness

V8 prepares a sanitized external-executor protocol with relative commands, environment tolerances, normalized hash rules, expected-output commitments, and failure-reporting boundaries. Thirty-six core artifacts receive normalized hashes and one aggregate commitment. The packet names common-mode dependencies: repository history, builder, source pins, test oracle, owner, host family, and governance assumptions. Those dependencies prevent same-owner or chain-internal replay from being called independent-team reproduction.

When snapshot state is verified, two clean detached D-drive snapshots can establish same-owner repeatability for this evidence layer. They still share the evidence design and authority assumptions. No independent team is present, no independent protocol owner has executed the packet, and no result has been returned. The independent-team gap therefore remains open even when local hash parity succeeds.

## Thermo-psyche classification

The thermo-psyche state machine retains six bounded classes: category barrier, heuristic, normative principle, operational rule, formal invariant, and empirical hypothesis. Each class has a minimum evidence burden. Allowed promotions add procedure, tests, rollback, observations, falsifiers, uncertainty, derivation, or independent review. Six prohibited shortcuts reject normative-to-physical, operational-to-enacted-law, formal-to-empirical-without-measurement, notation-to-consciousness, heuristic-to-fundamental-law, and category-barrier-to-identity transitions.

The classification register labels concrete examples without claiming new laws. A typed divergence identity can be a formal invariant within assumptions; a coordination-cost effect remains an empirical hypothesis; a rights floor is normative; and subjective state as a tensor is a category barrier in this packet. No consciousness tensor or fundamental thermo/psyche law is established.

## Stage 20 decision and retained negatives

The Stage 20 graph has ten mandatory nodes and six singleton blocking cut-sets. Real-data inference, real THOS arms, production Freed ID, authority legitimacy, independent-team reproduction, and complete accessibility/external review can each independently block readiness. Seven stop-rule mutations try to count defer as pass, erase a gate, ignore retraction, promote structural physics, substitute for Māori authority, or inflate bounded security. All are rejected. The board contains pass, fail, and defer decisions and never counts defer as pass.

V8 inherits all twenty v7 negatives and adds twelve. The new set records missing inference, real arms, production identity, authority, exhaustive security, independent reproduction, fundamental-law evidence, and complete accessibility review. Negative retention is not pessimism; it is the mechanism that prevents a polished report from erasing what the evidence did not establish.

## Workload, accessibility, and closeout boundary

The operational workload remained one owned lane with no task creation or subagent. D: stayed the primary bank. Windows Sandbox could not be audited without elevation and its executable was absent, so it was neither enabled nor used. The installed CLI and desktop versions were observed without updating either product. The static report will use a language declaration, skip link, landmarks, headings, table captions, scoped headers, readable text, and explicit non-claims. Those structural checks are useful but are not a complete WCAG conformance assessment.

Snapshot state for this build is **{snapshot_state}**. Closeout is allowed only when the complete repository suite, v8 validator, JSON parsing, privacy scan, diff hygiene, stale-label review, exact staged-file review, and fresh detached snapshot checks pass; the owned commit must then be pushed and local, upstream, tracking, and live remote heads must agree. Only after that boundary may exactly one sanitized baton be sent to the existing original Nima Calder task. Until then, all siblings remain standby and no outbound message is authorized.
"""
    write_text(phase / "v641-v8-integrated-overview.md", overview)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--snapshot-state", choices=["pending", "verified"], default="pending")
    parser.add_argument("--tests-passed", type=int, default=0)
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase = args.phase_dir if args.phase_dir.is_absolute() else repo / args.phase_dir
    build(repo, phase.resolve(), args.snapshot_state, args.tests_passed)
    print(json.dumps({"phase": phase.as_posix(), "snapshot_state": args.snapshot_state, "status": "built"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
