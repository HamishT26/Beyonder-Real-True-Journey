#!/usr/bin/env python3
"""Pure bounded structural models for Orin Thale v644-v8."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


BASE_CASES: dict[str, dict[str, Any]] = {
    "V6448-P01": {
        "witness_context_bound": True,
        "drift_detection_enabled": True,
        "demotion_append_only": True,
        "historical_witness_retained": True,
        "negative_link_retained": True,
        "silent_preferred_persistence": False,
        "claim_class": "bounded_method_state_only",
    },
    "V6448-P02": {
        "screening_radius_dimensioned": True,
        "regime_order_valid": True,
        "overlap_nonempty": True,
        "matching_residual_within_tolerance": True,
        "assumptions_declared": True,
        "empirical_claim": False,
        "claim_class": "formal_screening_scaffold_only",
    },
    "V6448-P03": {
        "official_real_rows": 0,
        "covariance_bound": False,
        "window_operator_bound": False,
        "nuisance_lock_frozen": False,
        "blind_holdout": False,
        "independent_review": False,
        "claim_class": "study_preregistration_only",
    },
    "V6448-P04": {
        "arm_labels_sealed": True,
        "comparative_effects_hidden": True,
        "variance_rule_frozen": True,
        "information_target_frozen": True,
        "matched_budget_cap_preserved": True,
        "real_arm_count": 0,
        "claim_class": "synthetic_proxy_only",
    },
    "V6448-P05": {
        "offer_issuer_bound": True,
        "configuration_identifier_bound": True,
        "nonce_fresh": True,
        "proof_audience_bound": True,
        "holder_key_bound": True,
        "replay_rejected": True,
        "claim_class": "synthetic_issuance_proxy_only",
    },
    "V6448-P06": {
        "affected_party_authority": False,
        "maori_authority_where_applicable": False,
        "beneficiary_privacy_authority": False,
        "fiduciary_authority": False,
        "competent_legal_authority": False,
        "enacted_rule_identified": False,
        "claim_class": "neutral_question_set_only",
    },
    "V6448-P07": {
        "gitlink_mode_classified": True,
        "declaration_correlated": True,
        "deinitialized_state_explicit": True,
        "undeclared_nested_rejected": True,
        "network_fetch_performed": False,
        "root_containment_valid": True,
        "claim_class": "read_only_visibility_only",
    },
    "V6448-P08": {
        "essential_text_in_dom": True,
        "pseudo_content_not_sole_source": True,
        "icons_have_text_equivalent": True,
        "print_preserves_evidence": True,
        "style_off_semantics_preserved": True,
        "manual_evaluation_complete": False,
        "claim_class": "structural_accessibility_only",
    },
    "V6448-P09": {
        "thermal_domain_declared": True,
        "contact_condition_declared": True,
        "equilibrium_relation_typed": True,
        "intensive_units_valid": True,
        "psyche_conversion": False,
        "participant_evidence_count": 0,
        "claim_class": "thermodynamic_classification_only",
    },
    "V6448-P10": {
        "sampling_frame_frozen": True,
        "randomness_provenance_declared": True,
        "sample_selected_before_inspection": True,
        "missing_items_counted": True,
        "tamper_flags_retained": True,
        "clean_sample_promotes_readiness": False,
        "claim_class": "structural_audit_rehearsal_only",
    },
}


MUTATIONS: dict[str, list[tuple[str, Any]]] = {
    "V6448-P01": [
        ("witness_context_bound", False),
        ("drift_detection_enabled", False),
        ("demotion_append_only", False),
        ("historical_witness_retained", False),
        ("negative_link_retained", False),
        ("silent_preferred_persistence", True),
        ("claim_class", "universal_method_truth"),
    ],
    "V6448-P02": [
        ("screening_radius_dimensioned", False),
        ("regime_order_valid", False),
        ("overlap_nonempty", False),
        ("matching_residual_within_tolerance", False),
        ("assumptions_declared", False),
        ("empirical_claim", True),
        ("claim_class", "confirmed_new_force"),
    ],
    "V6448-P03": [
        ("official_real_rows", 1),
        ("covariance_bound", True),
        ("window_operator_bound", True),
        ("nuisance_lock_frozen", True),
        ("blind_holdout", True),
        ("independent_review", True),
        ("claim_class", "empirically_confirmed"),
    ],
    "V6448-P04": [
        ("arm_labels_sealed", False),
        ("comparative_effects_hidden", False),
        ("variance_rule_frozen", False),
        ("information_target_frozen", False),
        ("matched_budget_cap_preserved", False),
        ("real_arm_count", 1),
        ("claim_class", "effective_real_arm"),
    ],
    "V6448-P05": [
        ("offer_issuer_bound", False),
        ("configuration_identifier_bound", False),
        ("nonce_fresh", False),
        ("proof_audience_bound", False),
        ("holder_key_bound", False),
        ("replay_rejected", False),
        ("claim_class", "production_identity"),
    ],
    "V6448-P06": [
        ("affected_party_authority", True),
        ("maori_authority_where_applicable", True),
        ("beneficiary_privacy_authority", True),
        ("fiduciary_authority", True),
        ("competent_legal_authority", True),
        ("enacted_rule_identified", True),
        ("claim_class", "repository_insolvency_decision"),
    ],
    "V6448-P07": [
        ("gitlink_mode_classified", False),
        ("declaration_correlated", False),
        ("deinitialized_state_explicit", False),
        ("undeclared_nested_rejected", False),
        ("network_fetch_performed", True),
        ("root_containment_valid", False),
        ("claim_class", "exhaustive_repository_assurance"),
    ],
    "V6448-P08": [
        ("essential_text_in_dom", False),
        ("pseudo_content_not_sole_source", False),
        ("icons_have_text_equivalent", False),
        ("print_preserves_evidence", False),
        ("style_off_semantics_preserved", False),
        ("manual_evaluation_complete", True),
        ("claim_class", "complete_accessibility"),
    ],
    "V6448-P09": [
        ("thermal_domain_declared", False),
        ("contact_condition_declared", False),
        ("equilibrium_relation_typed", False),
        ("intensive_units_valid", False),
        ("psyche_conversion", True),
        ("participant_evidence_count", 1),
        ("claim_class", "psyche_temperature_law"),
    ],
    "V6448-P10": [
        ("sampling_frame_frozen", False),
        ("randomness_provenance_declared", False),
        ("sample_selected_before_inspection", False),
        ("missing_items_counted", False),
        ("tamper_flags_retained", False),
        ("clean_sample_promotes_readiness", True),
        ("claim_class", "stage20_ready"),
    ],
}


def evaluate(proposal_id: str, row: dict[str, Any]) -> bool:
    baseline = BASE_CASES[proposal_id]
    if proposal_id in {"V6448-P03", "V6448-P06"}:
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
