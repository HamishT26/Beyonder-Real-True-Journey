#!/usr/bin/env python3
"""Pure synthetic decision model for Tamar Vey v644-v3 evidence cases."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


SPECS: dict[str, dict[str, Any]] = {
    "V6443-P01": {
        "outcome": "completed",
        "control": {
            "input_columns": "explicit_entity_ids",
            "output_column": "single_declared_entity",
            "activity_version": "immutable_declared_version",
            "aggregation_grain": "declared_or_none",
            "loss_class": "typed_reversible_or_irreversible",
            "quarantine_state": "enforced_until_review",
            "independence_class": "derived_not_independent",
        },
        "mutations": {
            "input_columns": "missing",
            "output_column": "implicit",
            "activity_version": "floating_latest",
            "aggregation_grain": "hidden",
            "loss_class": "irreversible_called_lossless",
            "quarantine_state": "silently_released",
            "independence_class": "derived_counted_independent",
        },
    },
    "V6443-P02": {
        "outcome": "completed",
        "control": {
            "action_variation": "typed_fields_and_boundary_terms",
            "symplectic_potential": "degree_and_ambiguity_declared",
            "presymplectic_current": "antisymmetrized_variations_with_units",
            "gauge_directions": "degeneracies_explicit",
            "boundary_conditions": "fixed_named_class",
            "charge_integrability": "finite_path_independent_or_unresolved",
            "claim_class": "formal_obligation_only",
        },
        "mutations": {
            "action_variation": "charge_read_without_derivation",
            "symplectic_potential": "ambiguity_hidden",
            "presymplectic_current": "units_or_degree_missing",
            "gauge_directions": "gauge_called_physical",
            "boundary_conditions": "changed_silently",
            "charge_integrability": "divergent_nonintegrable_called_charge",
            "claim_class": "established_gmut_physics",
        },
    },
    "V6443-P03": {
        "outcome": "open_gap",
        "control": {
            "observable_map": "missing_model_specific_gmut_to_ppn_derivation",
            "eligible_rows": "zero_frozen_observation_rows",
            "frames_and_timescales": "unbound_pending_real_packet",
            "covariance": "missing_source_covariance",
            "selection_and_nuisance": "unfrozen",
            "blind_holdout": "absent",
            "claim_class": "open_gap_protocol_only",
        },
        "mutations": {
            "observable_map": "assumed_from_generic_scalar_tensor",
            "eligible_rows": "ephemeris_documentation_called_observations",
            "frames_and_timescales": "mixed_without_transform",
            "covariance": "ignored",
            "selection_and_nuisance": "post_hoc",
            "blind_holdout": "unblinded_same_owner",
            "claim_class": "empirical_likelihood_confirmation",
        },
    },
    "V6443-P04": {
        "outcome": "represented",
        "control": {
            "endpoint_direction": "frozen_before_outcomes",
            "margin_provenance": "historical_effect_and_preserved_fraction_required",
            "assay_sensitivity": "explicit_unproven_assumption",
            "constancy_assumption": "explicit_unproven_assumption",
            "analysis_populations": "itt_and_per_protocol_preregistered",
            "real_arm_count": 0,
            "claim_class": "protocol_proxy_only",
        },
        "mutations": {
            "endpoint_direction": "reversed_after_results",
            "margin_provenance": "convenience_margin",
            "assay_sensitivity": "silently_assumed",
            "constancy_assumption": "historical_incomparability_ignored",
            "analysis_populations": "favorable_population_selected",
            "real_arm_count": 2,
            "claim_class": "thos_noninferiority_established",
        },
    },
    "V6443-P05": {
        "outcome": "represented",
        "control": {
            "disclosure_digest": "synthetic_exact_binding",
            "salt_class": "synthetic_nonsecret_fixture",
            "decoy_semantics": "nonclaim_digest_declared",
            "array_placement": "index_bound",
            "disclosed_scope": "frozen_minimal",
            "holder_key_binding": "synthetic_audience_nonce_freshness",
            "claim_class": "structural_proxy_only",
        },
        "mutations": {
            "disclosure_digest": "substituted",
            "salt_class": "reused_or_exposed_as_real",
            "decoy_semantics": "accepted_as_claim",
            "array_placement": "moved_without_binding",
            "disclosed_scope": "silently_widened",
            "holder_key_binding": "detached_or_replayed",
            "claim_class": "production_cryptographic_assurance",
        },
    },
    "V6443-P06": {
        "outcome": "exact_gate",
        "control": {
            "audit_scope": "unassigned",
            "beneficiary_disclosure": "unassigned_minimize_by_default",
            "qualified_auditor": "unassigned",
            "oversight_body": "unassigned",
            "conflict_and_redress": "unassigned",
            "authority_evidence": "absent_exact_participation",
            "claim_class": "exact_gate_unresolved",
        },
        "mutations": {
            "audit_scope": "repository_decided",
            "beneficiary_disclosure": "personal_data_published",
            "qualified_auditor": "repository_appointed",
            "oversight_body": "repository_selected",
            "conflict_and_redress": "repository_resolved",
            "authority_evidence": "official_sources_substituted_for_authority",
            "claim_class": "privacy_cultural_and_legal_ratification",
        },
    },
    "V6443-P07": {
        "outcome": "completed",
        "control": {
            "discovery_root": "explicit_bounded_root",
            "response_files": "explicit_and_implicit_inventory",
            "parent_traversal": "bounded_and_visible",
            "precedence": "declared",
            "recursion_depth": "finite_ceiling",
            "encoding": "declared",
            "claim_class": "bounded_fixture_only",
        },
        "mutations": {
            "discovery_root": "ambient_working_tree",
            "response_files": "implicit_file_hidden",
            "parent_traversal": "escapes_allowed_root",
            "precedence": "unknown",
            "recursion_depth": "unbounded",
            "encoding": "token_changing_implicit",
            "claim_class": "exhaustive_security",
        },
    },
    "V6443-P08": {
        "outcome": "completed",
        "control": {
            "control_label": "programmatically_associated",
            "error_text": "explicit_noncolor_text",
            "error_association": "described_by_or_equivalent",
            "instructions": "available_before_error",
            "invalid_state": "programmatically_exposed",
            "status_message": "structurally_identifiable",
            "claim_class": "structural_audit_only",
        },
        "mutations": {
            "control_label": "visual_only",
            "error_text": "color_only",
            "error_association": "detached",
            "instructions": "revealed_only_after_failure",
            "invalid_state": "not_exposed",
            "status_message": "silent_dom_change",
            "claim_class": "accessibility_complete",
        },
    },
    "V6443-P09": {
        "outcome": "completed",
        "control": {
            "chemical_potential": "partial_gibbs_energy_per_amount",
            "held_variables": "temperature_pressure_other_amounts",
            "units": "energy_per_amount_declared",
            "particle_exchange": "reservoir_or_closed_state_explicit",
            "ensemble": "grand_canonical_only_when_applicable",
            "psyche_mapping": "none_category_barrier",
            "claim_class": "thermodynamic_classifier_only",
        },
        "mutations": {
            "chemical_potential": "generic_value_score",
            "held_variables": "missing",
            "units": "dimensionless_without_derivation",
            "particle_exchange": "closed_system_called_exchange",
            "ensemble": "grand_canonical_assumed_everywhere",
            "psyche_mapping": "human_worth_numeric_identity",
            "claim_class": "fundamental_psyche_law",
        },
    },
    "V6443-P10": {
        "outcome": "completed",
        "control": {
            "hypothesis_family": "prospectively_frozen",
            "endpoint_order": "fixed_before_evidence",
            "alpha_allocation": "nonoverlapping_declared_budget",
            "interim_looks": "count_and_timing_declared",
            "stopping_rule": "prospective",
            "negative_domain": "veto_not_compensated",
            "claim_class": "structural_decision_board_only",
        },
        "mutations": {
            "hypothesis_family": "undefined",
            "endpoint_order": "selected_after_inspection",
            "alpha_allocation": "reused_per_endpoint",
            "interim_looks": "unrecorded",
            "stopping_rule": "stop_on_significance",
            "negative_domain": "averaged_away",
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
