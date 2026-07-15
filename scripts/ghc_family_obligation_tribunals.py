#!/usr/bin/env python3
"""Reusable structural obligation tribunals for GHC-family evidence packets.

These predicates classify synthetic records only.  They never promote real-data,
participant, identity, legal, cultural, privacy, security, or deployment claims.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


Row = dict[str, Any]


def metrology(row: Row) -> bool:
    return bool(
        row.get("measurand_defined") is True
        and row.get("traceability_chain_complete") is True
        and row.get("uncertainty_budget_complete") is True
        and row.get("decision_rule_preregistered") is True
        and row.get("guard_band_direction") in {"inside", "outside"}
        and row.get("false_acceptance_owner")
        and row.get("claim_class") == "synthetic_metrology_only"
    )


def self_adjoint(row: Row) -> bool:
    return bool(
        row.get("hilbert_space_declared") is True
        and row.get("operator_domain_declared") is True
        and row.get("boundary_form_vanishes") is True
        and row.get("positive_self_adjoint_extension") is True
        and row.get("conserved_energy_declared") is True
        and row.get("spectral_lower_bound") is True
        and row.get("claim_class") == "formal_structural_only"
    )


def cluster_real_data(row: Row) -> bool:
    return bool(
        row.get("derived_gmut_observable") is True
        and row.get("checksum_bound_real_rows") is True
        and row.get("selection_and_calibration") is True
        and row.get("covariance_complete") is True
        and row.get("blind_holdout") is True
        and row.get("independent_review") is True
        and row.get("claim_class") == "empirical_analysis_ready"
    )


def stepped_wedge(row: Row) -> bool:
    return bool(
        row.get("rollout_sequence_frozen") is True
        and row.get("calendar_time_modeled") is True
        and row.get("secular_trend_declared") is True
        and row.get("switch_estimand_declared") is True
        and row.get("carryover_declared") is True
        and row.get("real_arm_count") == 0
        and row.get("claim_class") == "proxy_only"
    )


def consent_policy_binding(row: Row) -> bool:
    requested = set(row.get("requested_attributes") or [])
    disclosed = set(row.get("disclosed_attributes") or [])
    return bool(
        row.get("holder_consent") is True
        and disclosed <= requested
        and row.get("purpose_bound") is True
        and row.get("verifier_policy_hash_bound") is True
        and row.get("audience_nonce_bound") is True
        and row.get("transaction_bound") is True
        and row.get("claim_class") == "synthetic_proxy_only"
    )


def beneficiary_authority(row: Row) -> bool:
    return bool(
        row.get("authorized_affected_parties") is True
        and row.get("maori_data_authority") is True
        and row.get("privacy_authority") is True
        and row.get("retention_deletion_authority") is True
        and row.get("secondary_use_authority") is True
        and row.get("competent_legal_authority") is True
        and row.get("claim_class") == "authorized_real_data_action"
    )


def git_config_scope(row: Row) -> bool:
    return bool(
        row.get("config_origin_declared") is True
        and row.get("config_scope_declared") is True
        and row.get("include_condition_resolved") is True
        and row.get("environment_overrides_declared") is True
        and row.get("safe_directory_broadened") is False
        and row.get("host_config_mutated") is False
        and row.get("claim_class") == "read_only_diagnostic"
    )


def figure_alternative(row: Row) -> bool:
    return bool(
        row.get("figure_purpose_declared") is True
        and row.get("short_alt_present") is True
        and row.get("caption_associated") is True
        and row.get("long_description_or_data") is True
        and row.get("decorative_status_consistent") is True
        and row.get("manual_user_evaluation") is False
        and row.get("claim_class") == "static_structural_only"
    )


def thermodynamic_length(row: Row) -> bool:
    return bool(
        row.get("metric_symmetric") is True
        and row.get("metric_positive") is True
        and row.get("coordinates_and_units_declared") is True
        and row.get("path_endpoints_declared") is True
        and row.get("covariance_source_declared") is True
        and row.get("psyche_conversion") is False
        and row.get("claim_class") == "physical_synthetic_only"
    )


def assurance_defeater(row: Row) -> bool:
    return bool(
        row.get("claim_evidence_edges_valid") is True
        and row.get("defeaters_retained") is True
        and row.get("rebuttals_noncircular") is True
        and row.get("residual_uncertainty_owned") is True
        and row.get("evidence_freshness_declared") is True
        and row.get("domain_vetoes_preserved") is True
        and row.get("claim_class") == "assurance_structure_only"
    )


def evidence_min_cut(row: Row) -> bool:
    return bool(
        row.get("failure_domains_declared") is True
        and row.get("aliases_collapsed") is True
        and row.get("minimum_cut_enumerated") is True
        and row.get("claim_survival_recomputed") is True
        and row.get("negative_sources_retained") is True
        and row.get("independent_team_reproduction") is False
        and row.get("claim_class") == "structural_independence_only"
    )


def tidal_real_data(row: Row) -> bool:
    return bool(
        row.get("derived_gmut_observable") is True
        and row.get("checksum_bound_strain_rows") is True
        and row.get("calibration_and_waveform_frozen") is True
        and row.get("priors_selection_covariance_complete") is True
        and row.get("blind_holdout") is True
        and row.get("independent_review") is True
        and row.get("claim_class") == "empirical_analysis_ready"
    )


def eft_running(row: Row) -> bool:
    return bool(
        row.get("operator_basis_declared") is True
        and row.get("coefficient_units_declared") is True
        and row.get("anomalous_dimension_declared") is True
        and row.get("scheme_and_matching_scale_declared") is True
        and row.get("truncation_order_consistent") is True
        and row.get("physical_prediction_claim") is False
        and row.get("claim_class") == "formal_eft_only"
    )


def missing_tipping(row: Row) -> bool:
    return bool(
        row.get("estimand_declared") is True
        and row.get("missingness_assumptions_frozen") is True
        and row.get("delta_grid_preregistered") is True
        and row.get("attrition_and_harms_retained") is True
        and row.get("tipping_rule_frozen") is True
        and row.get("real_arm_count") == 0
        and row.get("claim_class") == "proxy_only"
    )


def mdoc_binding(row: Row) -> bool:
    requested = set(row.get("requested_elements") or [])
    disclosed = set(row.get("disclosed_elements") or [])
    return bool(
        row.get("session_transcript_bound") is True
        and row.get("handover_bound") is True
        and row.get("origin_nonce_bound") is True
        and row.get("reader_auth_state_valid") is True
        and row.get("device_auth_state_valid") is True
        and disclosed <= requested
        and row.get("claim_class") == "synthetic_mdoc_proxy_only"
    )


def residual_authority(row: Row) -> bool:
    return bool(
        row.get("affected_party_authority") is True
        and row.get("fund_governance_authority") is True
        and row.get("beneficiary_privacy_authority") is True
        and row.get("maori_authority_where_applicable") is True
        and row.get("fiduciary_authority") is True
        and row.get("competent_legal_authority") is True
        and row.get("claim_class") == "authorized_residual_fund_action"
    )


def windows_path_portability(row: Row) -> bool:
    return bool(
        row.get("reserved_names_rejected") is True
        and row.get("casefold_collisions_rejected") is True
        and row.get("trailing_components_rejected") is True
        and row.get("path_policy_declared") is True
        and row.get("manifest_identity_stable") is True
        and row.get("host_configuration_mutated") is False
        and row.get("claim_class") == "synthetic_portability_only"
    )


def diagnostic_minimization(row: Row) -> bool:
    return bool(
        row.get("raw_identifiers_present") is False
        and row.get("private_paths_present") is False
        and row.get("credentials_present") is False
        and row.get("correlation_scope") == "single_purpose_window"
        and row.get("token_reversible") is False
        and row.get("retention_expiry_declared") is True
        and row.get("claim_class") == "bounded_privacy_scan_only"
    )


def exergy_nonconversion(row: Row) -> bool:
    return bool(
        row.get("reference_environment_declared") is True
        and row.get("dead_state_declared") is True
        and row.get("interaction_class_declared") is True
        and row.get("energy_exergy_distinguished") is True
        and row.get("units_and_signs_consistent") is True
        and row.get("psyche_conversion") is False
        and row.get("claim_class") == "physical_synthetic_only"
    )


def sample_information_stop(row: Row) -> bool:
    return bool(
        row.get("uncertainty_and_decision_declared") is True
        and row.get("evidence_domain_match") is True
        and row.get("cost_and_risk_declared") is True
        and row.get("irreversible_harm_blocked") is True
        and row.get("domain_vetoes_preserved") is True
        and row.get("negatives_retained") is True
        and row.get("claim_class") == "structural_decision_only"
    )


TRIBUNALS: dict[str, Callable[[Row], bool]] = {
    "metrology": metrology,
    "self_adjoint": self_adjoint,
    "cluster_real_data": cluster_real_data,
    "stepped_wedge": stepped_wedge,
    "consent_policy_binding": consent_policy_binding,
    "beneficiary_authority": beneficiary_authority,
    "git_config_scope": git_config_scope,
    "figure_alternative": figure_alternative,
    "thermodynamic_length": thermodynamic_length,
    "assurance_defeater": assurance_defeater,
    "evidence_min_cut": evidence_min_cut,
    "tidal_real_data": tidal_real_data,
    "eft_running": eft_running,
    "missing_tipping": missing_tipping,
    "mdoc_binding": mdoc_binding,
    "residual_authority": residual_authority,
    "windows_path_portability": windows_path_portability,
    "diagnostic_minimization": diagnostic_minimization,
    "exergy_nonconversion": exergy_nonconversion,
    "sample_information_stop": sample_information_stop,
}


def evaluate_tribunal(name: str, row: Row) -> bool:
    """Evaluate one named structural tribunal."""

    try:
        tribunal = TRIBUNALS[name]
    except KeyError as exc:
        raise KeyError(f"unknown GHC-family obligation tribunal: {name}") from exc
    return tribunal(row)
