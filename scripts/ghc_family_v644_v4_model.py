#!/usr/bin/env python3
"""Pure synthetic decision model for Sylven Arc v644-v4 evidence cases."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


SPECS: dict[str, dict[str, Any]] = {
    "V6444-P01": {
        "outcome": "completed",
        "control": {
            "treatment_assignment": "explicit_experimental_unit",
            "experimental_unit": "stable_independent_unit_id",
            "observation_nesting": "observations_nested_under_unit",
            "technical_replicate": "not_counted_as_independent_n",
            "shared_batch": "declared_dependence_or_none",
            "independent_n": "count_of_treatment_assigned_units",
            "claim_class": "structural_unit_contract_only",
        },
        "mutations": {
            "treatment_assignment": "missing_or_assigned_to_subsample",
            "experimental_unit": "observation_row_called_unit",
            "observation_nesting": "flattened_as_independent",
            "technical_replicate": "inflates_independent_n",
            "shared_batch": "common_treatment_hidden",
            "independent_n": "row_count_substituted",
            "claim_class": "empirical_independence_certified",
        },
    },
    "V6444-P02": {
        "outcome": "completed",
        "control": {
            "derivative_order": "highest_time_derivatives_explicit",
            "kinetic_matrix_rank": "degeneracy_condition_and_branch_declared",
            "primary_constraint": "derived_from_null_direction",
            "secondary_constraint": "preservation_condition_explicit",
            "constraint_class": "first_and_second_class_separated",
            "dof_count": "formal_count_with_rank_assumptions",
            "claim_class": "formal_obligation_only",
        },
        "mutations": {
            "derivative_order": "higher_derivative_hidden",
            "kinetic_matrix_rank": "invertible_but_called_degenerate",
            "primary_constraint": "asserted_without_null_direction",
            "secondary_constraint": "time_preservation_missing",
            "constraint_class": "gauge_and_second_class_conflated",
            "dof_count": "healthy_modes_asserted_without_count",
            "claim_class": "ghost_free_gmut_established",
        },
    },
    "V6444-P03": {
        "outcome": "open_gap",
        "control": {
            "observable_signature": "missing_model_specific_gmut_llr_derivation",
            "eligible_rows": "zero_frozen_normal_point_rows",
            "station_reflector_metadata": "unbound_pending_real_packet",
            "timing_frame": "unbound_pending_real_packet",
            "covariance_nuisance": "missing_source_covariance_and_model",
            "blind_holdout": "absent",
            "claim_class": "open_gap_protocol_only",
        },
        "mutations": {
            "observable_signature": "generic_equivalence_signal_assumed",
            "eligible_rows": "catalogue_metadata_called_observations",
            "station_reflector_metadata": "stations_or_reflectors_untracked",
            "timing_frame": "time_scales_or_frames_mixed",
            "covariance_nuisance": "ignored_or_post_hoc",
            "blind_holdout": "unblinded_same_owner",
            "claim_class": "empirical_equivalence_confirmation",
        },
    },
    "V6444-P04": {
        "outcome": "represented",
        "control": {
            "adaptation_rule": "prospective_formula_and_timing",
            "probability_floor": "nonzero_prespecified_minimum",
            "delayed_outcomes": "lag_handling_preregistered",
            "temporal_drift": "calendar_time_adjustment_required",
            "concealment": "future_assignment_not_predictable",
            "real_arm_count": 0,
            "claim_class": "adaptive_protocol_proxy_only",
        },
        "mutations": {
            "adaptation_rule": "changed_after_outcomes",
            "probability_floor": "arm_starved_without_rule",
            "delayed_outcomes": "pending_responses_ignored",
            "temporal_drift": "arm_effect_confounded_with_time",
            "concealment": "next_assignment_predictable",
            "real_arm_count": 2,
            "claim_class": "thos_adaptive_effectiveness_established",
        },
    },
    "V6444-P05": {
        "outcome": "represented",
        "control": {
            "context_url": "synthetic_declared_context",
            "context_bytes_digest": "synthetic_exact_binding",
            "related_resource": "digest_and_media_type_declared",
            "term_definitions": "protected_explicit_meanings",
            "alias_policy": "aliases_resolve_to_frozen_iris",
            "undefined_terms": "reject_or_explicit_policy",
            "claim_class": "structural_semantic_proxy_only",
        },
        "mutations": {
            "context_url": "mutable_remote_latest",
            "context_bytes_digest": "missing_or_mismatched",
            "related_resource": "unbound_external_resource",
            "term_definitions": "meaning_changes_silently",
            "alias_policy": "keyword_or_term_substitution",
            "undefined_terms": "silently_accepted",
            "claim_class": "production_identity_assurance",
        },
    },
    "V6444-P06": {
        "outcome": "exact_gate",
        "control": {
            "fund_target": "unassigned",
            "priority_classes": "unassigned",
            "investment_rule": "unassigned",
            "present_future_weight": "unassigned",
            "authority_evidence": "absent_exact_participation",
            "cultural_legal_status": "unratified_uninterpreted",
            "claim_class": "exact_gate_unresolved",
        },
        "mutations": {
            "fund_target": "repository_set_actuarial_target",
            "priority_classes": "repository_ranked_beneficiaries",
            "investment_rule": "repository_selected_risk",
            "present_future_weight": "future_claims_discounted_unilaterally",
            "authority_evidence": "official_sources_substituted_for_authority",
            "cultural_legal_status": "maori_and_legal_ratification_claimed",
            "claim_class": "fund_governance_authorized",
        },
    },
    "V6444-P07": {
        "outcome": "completed",
        "control": {
            "replacement_refs": "explicit_inventory_none_or_declared",
            "original_object": "raw_object_identity_preserved",
            "presented_object": "replacement_identity_separately_recorded",
            "alternate_store": "explicit_inventory_none_or_declared",
            "allowed_root": "bounded_owner_snapshot_only",
            "borrowing_disclosure": "required_before_validation",
            "claim_class": "bounded_fixture_only",
        },
        "mutations": {
            "replacement_refs": "hidden_history_replacement",
            "original_object": "original_identity_erased",
            "presented_object": "replacement_called_original",
            "alternate_store": "undeclared_borrowed_objects",
            "allowed_root": "escapes_bounded_snapshot",
            "borrowing_disclosure": "snapshot_called_independent",
            "claim_class": "exhaustive_repository_security",
        },
    },
    "V6444-P08": {
        "outcome": "completed",
        "control": {
            "abbreviation_token": "declared_technical_token",
            "expanded_form": "plain_language_expansion",
            "first_use": "expansion_precedes_or_accompanies_use",
            "programmatic_markup": "abbr_title_or_equivalent",
            "glossary_target": "existing_unique_anchor",
            "domain_meaning": "consistent_within_scope",
            "claim_class": "structural_audit_only",
        },
        "mutations": {
            "abbreviation_token": "unfamiliar_and_unlisted",
            "expanded_form": "missing",
            "first_use": "expansion_after_repeated_use",
            "programmatic_markup": "visual_expansion_only",
            "glossary_target": "broken_or_duplicate_anchor",
            "domain_meaning": "same_token_conflicting_meanings",
            "claim_class": "accessibility_complete",
        },
    },
    "V6444-P09": {
        "outcome": "completed",
        "control": {
            "phase_definition": "ordered_and_disordered_states_explicit",
            "order_parameter": "physical_normalized_quantity",
            "control_variable": "typed_temperature_field_or_equivalent",
            "units_normalization": "units_or_dimensionless_derivation_declared",
            "critical_regime": "bounded_with_finite_size_qualifier",
            "psyche_mapping": "none_category_barrier",
            "claim_class": "thermodynamic_classifier_only",
        },
        "mutations": {
            "phase_definition": "states_undefined",
            "order_parameter": "generic_score_or_binary_label",
            "control_variable": "missing",
            "units_normalization": "arbitrary_scale_called_universal",
            "critical_regime": "scaling_asserted_globally",
            "psyche_mapping": "consciousness_or_worth_threshold",
            "claim_class": "fundamental_psyche_transition_law",
        },
    },
    "V6444-P10": {
        "outcome": "completed",
        "control": {
            "specification_universe": "defensible_and_prospectively_bounded",
            "inclusion_rules": "substantive_rules_declared",
            "coding_choices": "all_defensible_codings_retained",
            "covariates_estimators": "all_defensible_sets_retained",
            "preregistration": "before_evidence_inspection",
            "unfavorable_retention": "sign_and_decision_changes_visible",
            "claim_class": "structural_decision_board_only",
        },
        "mutations": {
            "specification_universe": "defined_after_results",
            "inclusion_rules": "implausible_variants_dilute_or_favorable_only",
            "coding_choices": "preferred_coding_selected_silently",
            "covariates_estimators": "one_favorable_model_only",
            "preregistration": "post_hoc",
            "unfavorable_retention": "negative_or_unstable_results_removed",
            "claim_class": "stage20_ready",
        },
    },
}


def evaluate_record(proposal_id: str, record: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one synthetic record against its frozen control contract."""

    if proposal_id not in SPECS:
        return {"proposal_id": proposal_id, "decision": "rejected", "reasons": ["unknown_proposal_id"], "retained_negative": True}
    spec = SPECS[proposal_id]
    control = spec["control"]
    reasons = []
    for key, expected in control.items():
        if key not in record:
            reasons.append(f"missing:{key}")
        elif record[key] != expected:
            reasons.append(f"mismatch:{key}")
    for key in record:
        if key not in control:
            reasons.append(f"unexpected:{key}")
    if reasons:
        return {"proposal_id": proposal_id, "decision": "rejected", "reasons": reasons, "retained_negative": True}
    return {"proposal_id": proposal_id, "decision": spec["outcome"], "reasons": [], "retained_negative": False}


def build_cases(proposal_id: str) -> dict[str, Any]:
    """Return one accepted-or-held control and seven rejected mutations."""

    spec = SPECS[proposal_id]
    control_record = copy.deepcopy(spec["control"])
    control = {
        "case_id": f"{proposal_id}-C00",
        "kind": "control",
        "record": control_record,
        "evaluation": evaluate_record(proposal_id, control_record),
    }
    mutations = []
    for index, (field, bad_value) in enumerate(spec["mutations"].items(), start=1):
        record = copy.deepcopy(control_record)
        record[field] = bad_value
        mutations.append(
            {
                "negative_id": f"{proposal_id}-N{index:02d}",
                "kind": "single_field_mutation",
                "mutated_field": field,
                "record": record,
                "evaluation": evaluate_record(proposal_id, record),
                "retained": True,
            }
        )
    payload = {"proposal_id": proposal_id, "control": control, "mutations": mutations}
    payload["case_set_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return payload


def all_cases() -> dict[str, dict[str, Any]]:
    return {proposal_id: build_cases(proposal_id) for proposal_id in SPECS}


if __name__ == "__main__":
    print(json.dumps({"proposals": len(SPECS), "cases": 80, "synthetic_negatives": 70}, sort_keys=True))
