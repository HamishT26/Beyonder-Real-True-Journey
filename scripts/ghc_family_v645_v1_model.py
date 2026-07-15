#!/usr/bin/env python3
"""Pure bounded structural models for Tamar Vey v645-v1."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


BASE_CASES: dict[str, dict[str, Any]] = {
    "V6451-P01": {
        "parser_preflight_classified": True,
        "launcher_preflight_classified": True,
        "child_start_attested": True,
        "completion_receipt_bound": True,
        "zero_credit_for_unstarted": True,
        "negative_retained": True,
        "claim_class": "bounded_process_evidence_only",
    },
    "V6451-P02": {
        "long_wavelength_scaling_valid": True,
        "residual_gauge_generator_typed": True,
        "constraints_satisfied": True,
        "regularity_declared": True,
        "entropy_source_accounted": True,
        "conserved_quantity_scoped": True,
        "claim_class": "formal_soft_limit_scaffold_only",
    },
    "V6451-P03": {
        "official_real_rows": 0,
        "map_mask_lineage_bound": False,
        "tracer_kernel_bound": False,
        "covariance_bound": False,
        "nuisance_lock_frozen": False,
        "blind_holdout": False,
        "independent_review": False,
    },
    "V6451-P04": {
        "roles_separated": True,
        "closed_session_sealed": True,
        "sponsor_recommendation_minimized": True,
        "comparative_reconstruction_rejected": True,
        "matched_budget_preserved": True,
        "real_arm_count": 0,
        "claim_class": "synthetic_monitoring_proxy_only",
    },
    "V6451-P05": {
        "issuer_subject_edges_bound": True,
        "authority_hints_bound": True,
        "trust_anchor_declared": True,
        "expiry_order_valid": True,
        "policy_operators_supported": True,
        "rollover_linkage_bound": True,
        "claim_class": "synthetic_federation_proxy_only",
    },
    "V6451-P06": {
        "affected_party_authority": False,
        "maori_authority_where_applicable": False,
        "beneficiary_privacy_authority": False,
        "fiduciary_authority": False,
        "competent_legal_authority": False,
        "enacted_rule_identified": False,
        "claim_class": "refusal_first_authority_matrix_only",
    },
    "V6451-P07": {
        "pointer_grammar_valid": True,
        "sha256_oid_typed": True,
        "declared_size_valid": True,
        "materialization_state_explicit": True,
        "missing_content_rejected": True,
        "network_fetch_performed": False,
        "root_containment_valid": True,
    },
    "V6451-P08": {
        "visible_status_text": True,
        "noncolor_cue_present": True,
        "contrast_tokens_pass": True,
        "monochrome_meaning_preserved": True,
        "semantic_landmarks_present": True,
        "manual_evaluation_complete": False,
        "claim_class": "structural_accessibility_only",
    },
    "V6451-P09": {
        "heat_capacity_units_valid": True,
        "constraint_variable_declared": True,
        "derivative_typed": True,
        "stability_scope_declared": True,
        "psyche_conversion": False,
        "participant_evidence_count": 0,
        "claim_class": "thermodynamic_classification_only",
    },
    "V6451-P10": {
        "support_graph_directed": True,
        "strong_components_detected": True,
        "circular_roots_zero_credit": True,
        "external_roots_separated": True,
        "exact_gates_retained": True,
        "readiness_promoted": False,
        "claim_class": "stage20_rejection_board_only",
    },
}


MUTATIONS: dict[str, list[tuple[str, Any]]] = {
    "V6451-P01": [
        ("parser_preflight_classified", False),
        ("launcher_preflight_classified", False),
        ("child_start_attested", False),
        ("completion_receipt_bound", False),
        ("zero_credit_for_unstarted", False),
        ("negative_retained", False),
        ("claim_class", "independent_reproduction"),
    ],
    "V6451-P02": [
        ("long_wavelength_scaling_valid", False),
        ("residual_gauge_generator_typed", False),
        ("constraints_satisfied", False),
        ("regularity_declared", False),
        ("entropy_source_accounted", False),
        ("conserved_quantity_scoped", False),
        ("claim_class", "confirmed_unique_prediction"),
    ],
    "V6451-P03": [
        ("official_real_rows", 1),
        ("map_mask_lineage_bound", True),
        ("tracer_kernel_bound", True),
        ("covariance_bound", True),
        ("nuisance_lock_frozen", True),
        ("blind_holdout", True),
        ("independent_review", True),
    ],
    "V6451-P04": [
        ("roles_separated", False),
        ("closed_session_sealed", False),
        ("sponsor_recommendation_minimized", False),
        ("comparative_reconstruction_rejected", False),
        ("matched_budget_preserved", False),
        ("real_arm_count", 1),
        ("claim_class", "real_arm_superiority"),
    ],
    "V6451-P05": [
        ("issuer_subject_edges_bound", False),
        ("authority_hints_bound", False),
        ("trust_anchor_declared", False),
        ("expiry_order_valid", False),
        ("policy_operators_supported", False),
        ("rollover_linkage_bound", False),
        ("claim_class", "production_identity_assurance"),
    ],
    "V6451-P06": [
        ("affected_party_authority", True),
        ("maori_authority_where_applicable", True),
        ("beneficiary_privacy_authority", True),
        ("fiduciary_authority", True),
        ("competent_legal_authority", True),
        ("enacted_rule_identified", True),
        ("claim_class", "repository_investment_decision"),
    ],
    "V6451-P07": [
        ("pointer_grammar_valid", False),
        ("sha256_oid_typed", False),
        ("declared_size_valid", False),
        ("materialization_state_explicit", False),
        ("missing_content_rejected", False),
        ("network_fetch_performed", True),
        ("root_containment_valid", False),
    ],
    "V6451-P08": [
        ("visible_status_text", False),
        ("noncolor_cue_present", False),
        ("contrast_tokens_pass", False),
        ("monochrome_meaning_preserved", False),
        ("semantic_landmarks_present", False),
        ("manual_evaluation_complete", True),
        ("claim_class", "complete_accessibility"),
    ],
    "V6451-P09": [
        ("heat_capacity_units_valid", False),
        ("constraint_variable_declared", False),
        ("derivative_typed", False),
        ("stability_scope_declared", False),
        ("psyche_conversion", True),
        ("participant_evidence_count", 1),
        ("claim_class", "psyche_heat_capacity_law"),
    ],
    "V6451-P10": [
        ("support_graph_directed", False),
        ("strong_components_detected", False),
        ("circular_roots_zero_credit", False),
        ("external_roots_separated", False),
        ("exact_gates_retained", False),
        ("readiness_promoted", True),
        ("claim_class", "stage20_ready"),
    ],
}


def evaluate(proposal_id: str, row: dict[str, Any]) -> bool:
    baseline = BASE_CASES[proposal_id]
    if proposal_id in {"V6451-P03", "V6451-P06"}:
        return False
    return row == baseline


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
