#!/usr/bin/env python3
"""Pure structural models for the Sable Rook v644-v7 evidence packet."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from ghc_family_obligation_tribunals import evaluate_tribunal


PROPOSAL_TRIBUNAL = {
    "V6447-P01": "evidence_min_cut",
    "V6447-P02": "tidal_real_data",
    "V6447-P03": "eft_running",
    "V6447-P04": "missing_tipping",
    "V6447-P05": "mdoc_binding",
    "V6447-P06": "residual_authority",
    "V6447-P07": "windows_path_portability",
    "V6447-P08": "diagnostic_minimization",
    "V6447-P09": "exergy_nonconversion",
    "V6447-P10": "sample_information_stop",
}


def evaluate(proposal_id: str, row: dict[str, Any]) -> bool:
    return evaluate_tribunal(PROPOSAL_TRIBUNAL[proposal_id], row)


BASE_CASES: dict[str, dict[str, Any]] = {
    "V6447-P01": {
        "failure_domains_declared": True,
        "aliases_collapsed": True,
        "minimum_cut_enumerated": True,
        "claim_survival_recomputed": True,
        "negative_sources_retained": True,
        "independent_team_reproduction": False,
        "claim_class": "structural_independence_only",
    },
    "V6447-P02": {
        "derived_gmut_observable": False,
        "checksum_bound_strain_rows": False,
        "calibration_and_waveform_frozen": False,
        "priors_selection_covariance_complete": False,
        "blind_holdout": False,
        "independent_review": False,
        "claim_class": "study_preregistration_only",
    },
    "V6447-P03": {
        "operator_basis_declared": True,
        "coefficient_units_declared": True,
        "anomalous_dimension_declared": True,
        "scheme_and_matching_scale_declared": True,
        "truncation_order_consistent": True,
        "physical_prediction_claim": False,
        "claim_class": "formal_eft_only",
    },
    "V6447-P04": {
        "estimand_declared": True,
        "missingness_assumptions_frozen": True,
        "delta_grid_preregistered": True,
        "attrition_and_harms_retained": True,
        "tipping_rule_frozen": True,
        "real_arm_count": 0,
        "claim_class": "proxy_only",
    },
    "V6447-P05": {
        "session_transcript_bound": True,
        "handover_bound": True,
        "origin_nonce_bound": True,
        "reader_auth_state_valid": True,
        "device_auth_state_valid": True,
        "requested_elements": ["org.iso.18013.5.1.family_name", "org.iso.18013.5.1.age_over_18"],
        "disclosed_elements": ["org.iso.18013.5.1.age_over_18"],
        "claim_class": "synthetic_mdoc_proxy_only",
    },
    "V6447-P06": {
        "affected_party_authority": False,
        "fund_governance_authority": False,
        "beneficiary_privacy_authority": False,
        "maori_authority_where_applicable": False,
        "fiduciary_authority": False,
        "competent_legal_authority": False,
        "claim_class": "neutral_question_set_only",
    },
    "V6447-P07": {
        "reserved_names_rejected": True,
        "casefold_collisions_rejected": True,
        "trailing_components_rejected": True,
        "path_policy_declared": True,
        "manifest_identity_stable": True,
        "host_configuration_mutated": False,
        "claim_class": "synthetic_portability_only",
    },
    "V6447-P08": {
        "raw_identifiers_present": False,
        "private_paths_present": False,
        "credentials_present": False,
        "correlation_scope": "single_purpose_window",
        "token_reversible": False,
        "retention_expiry_declared": True,
        "claim_class": "bounded_privacy_scan_only",
    },
    "V6447-P09": {
        "reference_environment_declared": True,
        "dead_state_declared": True,
        "interaction_class_declared": True,
        "energy_exergy_distinguished": True,
        "units_and_signs_consistent": True,
        "psyche_conversion": False,
        "claim_class": "physical_synthetic_only",
    },
    "V6447-P10": {
        "uncertainty_and_decision_declared": True,
        "evidence_domain_match": True,
        "cost_and_risk_declared": True,
        "irreversible_harm_blocked": True,
        "domain_vetoes_preserved": True,
        "negatives_retained": True,
        "claim_class": "structural_decision_only",
    },
}


MUTATIONS: dict[str, list[tuple[str, Any]]] = {
    "V6447-P01": [
        ("failure_domains_declared", False),
        ("aliases_collapsed", False),
        ("minimum_cut_enumerated", False),
        ("claim_survival_recomputed", False),
        ("negative_sources_retained", False),
        ("independent_team_reproduction", True),
        ("claim_class", "scientifically_independent"),
    ],
    "V6447-P02": [
        ("derived_gmut_observable", True),
        ("checksum_bound_strain_rows", True),
        ("calibration_and_waveform_frozen", True),
        ("priors_selection_covariance_complete", True),
        ("blind_holdout", True),
        ("independent_review", True),
        ("claim_class", "empirically_confirmed"),
    ],
    "V6447-P03": [
        ("operator_basis_declared", False),
        ("coefficient_units_declared", False),
        ("anomalous_dimension_declared", False),
        ("scheme_and_matching_scale_declared", False),
        ("truncation_order_consistent", False),
        ("physical_prediction_claim", True),
        ("claim_class", "unique_prediction"),
    ],
    "V6447-P04": [
        ("estimand_declared", False),
        ("missingness_assumptions_frozen", False),
        ("delta_grid_preregistered", False),
        ("attrition_and_harms_retained", False),
        ("tipping_rule_frozen", False),
        ("real_arm_count", 1),
        ("claim_class", "effective"),
    ],
    "V6447-P05": [
        ("session_transcript_bound", False),
        ("handover_bound", False),
        ("origin_nonce_bound", False),
        ("reader_auth_state_valid", False),
        ("device_auth_state_valid", False),
        ("disclosed_elements", ["org.iso.18013.5.1.age_over_18", "org.iso.18013.5.1.resident_address"]),
        ("claim_class", "production_identity"),
    ],
    "V6447-P06": [
        ("affected_party_authority", True),
        ("fund_governance_authority", True),
        ("beneficiary_privacy_authority", True),
        ("maori_authority_where_applicable", True),
        ("fiduciary_authority", True),
        ("competent_legal_authority", True),
        ("claim_class", "repository_wind_up_decision"),
    ],
    "V6447-P07": [
        ("reserved_names_rejected", False),
        ("casefold_collisions_rejected", False),
        ("trailing_components_rejected", False),
        ("path_policy_declared", False),
        ("manifest_identity_stable", False),
        ("host_configuration_mutated", True),
        ("claim_class", "independent_reproduction"),
    ],
    "V6447-P08": [
        ("raw_identifiers_present", True),
        ("private_paths_present", True),
        ("credentials_present", True),
        ("correlation_scope", "global_cross_purpose"),
        ("token_reversible", True),
        ("retention_expiry_declared", False),
        ("claim_class", "exhaustive_privacy_assurance"),
    ],
    "V6447-P09": [
        ("reference_environment_declared", False),
        ("dead_state_declared", False),
        ("interaction_class_declared", False),
        ("energy_exergy_distinguished", False),
        ("units_and_signs_consistent", False),
        ("psyche_conversion", True),
        ("claim_class", "consciousness_capacity"),
    ],
    "V6447-P10": [
        ("uncertainty_and_decision_declared", False),
        ("evidence_domain_match", False),
        ("cost_and_risk_declared", False),
        ("irreversible_harm_blocked", False),
        ("domain_vetoes_preserved", False),
        ("negatives_retained", False),
        ("claim_class", "stage20_ready"),
    ],
}


def proposal_cases(proposal_id: str) -> dict[str, Any]:
    baseline = deepcopy(BASE_CASES[proposal_id])
    cases = []
    for index, (field, value) in enumerate(MUTATIONS[proposal_id], 1):
        row = deepcopy(BASE_CASES[proposal_id])
        row[field] = value
        observed = evaluate(proposal_id, row)
        cases.append(
            {
                "case_id": f"{proposal_id}-M{index:02d}",
                "mutated_field": field,
                "mutated_value": value,
                "expected_accept": False,
                "observed_accept": observed,
                "matched": observed is False,
            }
        )
    return {
        "proposal_id": proposal_id,
        "baseline": baseline,
        "baseline_accept": evaluate(proposal_id, baseline),
        "cases": cases,
        "case_count": len(cases),
        "matched_count": sum(case["matched"] for case in cases),
    }
