#!/usr/bin/env python3
"""Pure structural models for the Ilyra Fen v644-v6 evidence packet."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from ghc_family_obligation_tribunals import evaluate_tribunal


PROPOSAL_TRIBUNAL = {
    "V6446-P01": "metrology",
    "V6446-P02": "self_adjoint",
    "V6446-P03": "cluster_real_data",
    "V6446-P04": "stepped_wedge",
    "V6446-P05": "consent_policy_binding",
    "V6446-P06": "beneficiary_authority",
    "V6446-P07": "git_config_scope",
    "V6446-P08": "figure_alternative",
    "V6446-P09": "thermodynamic_length",
    "V6446-P10": "assurance_defeater",
}


def evaluate(proposal_id: str, row: dict[str, Any]) -> bool:
    return evaluate_tribunal(PROPOSAL_TRIBUNAL[proposal_id], row)


BASE_CASES: dict[str, dict[str, Any]] = {
    "V6446-P01": {
        "measurand_defined": True,
        "traceability_chain_complete": True,
        "uncertainty_budget_complete": True,
        "decision_rule_preregistered": True,
        "guard_band_direction": "inside",
        "false_acceptance_owner": "declared_role",
        "claim_class": "synthetic_metrology_only",
    },
    "V6446-P02": {
        "hilbert_space_declared": True,
        "operator_domain_declared": True,
        "boundary_form_vanishes": True,
        "positive_self_adjoint_extension": True,
        "conserved_energy_declared": True,
        "spectral_lower_bound": True,
        "claim_class": "formal_structural_only",
    },
    "V6446-P03": {
        "derived_gmut_observable": False,
        "checksum_bound_real_rows": False,
        "selection_and_calibration": False,
        "covariance_complete": False,
        "blind_holdout": False,
        "independent_review": False,
        "claim_class": "study_preregistration_only",
    },
    "V6446-P04": {
        "rollout_sequence_frozen": True,
        "calendar_time_modeled": True,
        "secular_trend_declared": True,
        "switch_estimand_declared": True,
        "carryover_declared": True,
        "real_arm_count": 0,
        "claim_class": "proxy_only",
    },
    "V6446-P05": {
        "holder_consent": True,
        "requested_attributes": ["age_over_threshold", "membership"],
        "disclosed_attributes": ["age_over_threshold"],
        "purpose_bound": True,
        "verifier_policy_hash_bound": True,
        "audience_nonce_bound": True,
        "transaction_bound": True,
        "claim_class": "synthetic_proxy_only",
    },
    "V6446-P06": {
        "authorized_affected_parties": False,
        "maori_data_authority": False,
        "privacy_authority": False,
        "retention_deletion_authority": False,
        "secondary_use_authority": False,
        "competent_legal_authority": False,
        "claim_class": "neutral_question_set_only",
    },
    "V6446-P07": {
        "config_origin_declared": True,
        "config_scope_declared": True,
        "include_condition_resolved": True,
        "environment_overrides_declared": True,
        "safe_directory_broadened": False,
        "host_config_mutated": False,
        "claim_class": "read_only_diagnostic",
    },
    "V6446-P08": {
        "figure_purpose_declared": True,
        "short_alt_present": True,
        "caption_associated": True,
        "long_description_or_data": True,
        "decorative_status_consistent": True,
        "manual_user_evaluation": False,
        "claim_class": "static_structural_only",
    },
    "V6446-P09": {
        "metric_symmetric": True,
        "metric_positive": True,
        "coordinates_and_units_declared": True,
        "path_endpoints_declared": True,
        "covariance_source_declared": True,
        "psyche_conversion": False,
        "claim_class": "physical_synthetic_only",
    },
    "V6446-P10": {
        "claim_evidence_edges_valid": True,
        "defeaters_retained": True,
        "rebuttals_noncircular": True,
        "residual_uncertainty_owned": True,
        "evidence_freshness_declared": True,
        "domain_vetoes_preserved": True,
        "claim_class": "assurance_structure_only",
    },
}


MUTATIONS: dict[str, list[tuple[str, Any]]] = {
    "V6446-P01": [
        ("measurand_defined", False), ("traceability_chain_complete", False),
        ("uncertainty_budget_complete", False), ("decision_rule_preregistered", False),
        ("guard_band_direction", "unknown"), ("false_acceptance_owner", ""),
        ("claim_class", "empirically_confirmed"),
    ],
    "V6446-P02": [
        ("hilbert_space_declared", False), ("operator_domain_declared", False),
        ("boundary_form_vanishes", False), ("positive_self_adjoint_extension", False),
        ("conserved_energy_declared", False), ("spectral_lower_bound", False),
        ("claim_class", "canonical_proof"),
    ],
    "V6446-P03": [
        ("derived_gmut_observable", False), ("checksum_bound_real_rows", False),
        ("selection_and_calibration", False), ("covariance_complete", False),
        ("blind_holdout", False), ("independent_review", False),
        ("claim_class", "confirmed"),
    ],
    "V6446-P04": [
        ("rollout_sequence_frozen", False), ("calendar_time_modeled", False),
        ("secular_trend_declared", False), ("switch_estimand_declared", False),
        ("carryover_declared", False), ("real_arm_count", 1),
        ("claim_class", "effective"),
    ],
    "V6446-P05": [
        ("holder_consent", False), ("disclosed_attributes", ["age_over_threshold", "address"]),
        ("purpose_bound", False), ("verifier_policy_hash_bound", False),
        ("audience_nonce_bound", False), ("transaction_bound", False),
        ("claim_class", "production_identity"),
    ],
    "V6446-P06": [
        ("authorized_affected_parties", False), ("maori_data_authority", False),
        ("privacy_authority", False), ("retention_deletion_authority", False),
        ("secondary_use_authority", False), ("competent_legal_authority", False),
        ("claim_class", "repository_decision"),
    ],
    "V6446-P07": [
        ("config_origin_declared", False), ("config_scope_declared", False),
        ("include_condition_resolved", False), ("environment_overrides_declared", False),
        ("safe_directory_broadened", True), ("host_config_mutated", True),
        ("claim_class", "host_reconfiguration"),
    ],
    "V6446-P08": [
        ("figure_purpose_declared", False), ("short_alt_present", False),
        ("caption_associated", False), ("long_description_or_data", False),
        ("decorative_status_consistent", False), ("manual_user_evaluation", True),
        ("claim_class", "complete_accessibility"),
    ],
    "V6446-P09": [
        ("metric_symmetric", False), ("metric_positive", False),
        ("coordinates_and_units_declared", False), ("path_endpoints_declared", False),
        ("covariance_source_declared", False), ("psyche_conversion", True),
        ("claim_class", "consciousness_measure"),
    ],
    "V6446-P10": [
        ("claim_evidence_edges_valid", False), ("defeaters_retained", False),
        ("rebuttals_noncircular", False), ("residual_uncertainty_owned", False),
        ("evidence_freshness_declared", False), ("domain_vetoes_preserved", False),
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
