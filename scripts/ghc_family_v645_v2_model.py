#!/usr/bin/env python3
"""Pure bounded structural models for Sylven Arc v645-v2."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


BASE_CASES: dict[str, dict[str, Any]] = {
    "V6452-P01": {
        "attempt_ids_unique": True,
        "signatures_clustered_exactly": True,
        "events_append_only": True,
        "retry_budget": 2,
        "attempt_count": 2,
        "stop_after_budget": True,
        "claim_class": "same_owner_method_evidence_only",
    },
    "V6452-P02": {
        "local_gauge_generator_typed": True,
        "noether_identity_derived": True,
        "dependent_equations_marked": True,
        "reducibility_rank_declared": True,
        "boundary_terms_scoped": True,
        "gauge_fixing_separated": True,
        "claim_class": "formal_gmut_obligation_graph_only",
    },
    "V6452-P03": {
        "official_strain_rows": 0,
        "calibration_lineage_bound": False,
        "detector_geometry_bound": False,
        "data_quality_segments_bound": False,
        "injection_exclusions_frozen": False,
        "blind_null_stream_frozen": False,
        "independent_review": False,
    },
    "V6452-P04": {
        "priority_preserved": True,
        "cause_and_action_preserved": True,
        "acknowledgement_not_resolution": True,
        "shelving_owner_bound": True,
        "shelving_expiry_bound": True,
        "matched_information_budget": True,
        "claim_class": "synthetic_control_room_proxy_only",
    },
    "V6452-P05": {
        "credential_ids_resolve": True,
        "format_metadata_typed": True,
        "claim_paths_valid": True,
        "required_sets_all_or_nothing": True,
        "optional_alternatives_scoped": True,
        "overdisclosure_rejected": True,
        "claim_class": "synthetic_dcql_profile_only",
    },
    "V6452-P06": {
        "competent_legal_authority": False,
        "affected_consumer_authority": False,
        "privacy_authority": False,
        "maori_authority_where_relevant": False,
        "hardship_rule_enacted_and_interpreted": False,
        "disconnection_rule_authorized": False,
        "claim_class": "refusal_first_water_authority_matrix_only",
    },
    "V6452-P07": {
        "records_parse": True,
        "object_ids_typed": True,
        "modes_typed": True,
        "only_stage_zero": True,
        "path_multiplicity_absent": True,
        "index_mutations": 0,
        "claim_class": "read_only_manifest_guard",
    },
    "V6452-P08": {
        "descriptive_title": True,
        "meta_refresh_count": 0,
        "scripted_timer_count": 0,
        "automatic_navigation_count": 0,
        "visible_status_text": True,
        "manual_evaluation_complete": False,
        "claim_class": "structural_accessibility_only",
    },
    "V6452-P09": {
        "enthalpy_constraint_declared": True,
        "derivative_variables_typed": True,
        "units_valid": True,
        "inversion_scope_declared": True,
        "equation_of_state_scoped": True,
        "psyche_conversion": False,
        "claim_class": "thermodynamic_classification_only",
    },
    "V6452-P10": {
        "proxy_and_target_separated": True,
        "target_evidence_nonzero_required": True,
        "gaming_signal_retained": True,
        "countermetric_visible": True,
        "protected_gates_noncompensatory": True,
        "independent_review_required": True,
        "readiness_promoted": False,
    },
}


MUTATIONS: dict[str, list[tuple[str, Any]]] = {
    "V6452-P01": [
        ("attempt_ids_unique", False),
        ("signatures_clustered_exactly", False),
        ("events_append_only", False),
        ("retry_budget", -1),
        ("attempt_count", 3),
        ("stop_after_budget", False),
        ("claim_class", "independent_reproduction"),
    ],
    "V6452-P02": [
        ("local_gauge_generator_typed", False),
        ("noether_identity_derived", False),
        ("dependent_equations_marked", False),
        ("reducibility_rank_declared", False),
        ("boundary_terms_scoped", False),
        ("gauge_fixing_separated", False),
        ("claim_class", "empirical_confirmation"),
    ],
    "V6452-P03": [
        ("official_strain_rows", 1),
        ("calibration_lineage_bound", True),
        ("detector_geometry_bound", True),
        ("data_quality_segments_bound", True),
        ("injection_exclusions_frozen", True),
        ("blind_null_stream_frozen", True),
        ("independent_review", True),
    ],
    "V6452-P04": [
        ("priority_preserved", False),
        ("cause_and_action_preserved", False),
        ("acknowledgement_not_resolution", False),
        ("shelving_owner_bound", False),
        ("shelving_expiry_bound", False),
        ("matched_information_budget", False),
        ("claim_class", "real_plant_effectiveness"),
    ],
    "V6452-P05": [
        ("credential_ids_resolve", False),
        ("format_metadata_typed", False),
        ("claim_paths_valid", False),
        ("required_sets_all_or_nothing", False),
        ("optional_alternatives_scoped", False),
        ("overdisclosure_rejected", False),
        ("claim_class", "production_identity_assurance"),
    ],
    "V6452-P06": [
        ("competent_legal_authority", True),
        ("affected_consumer_authority", True),
        ("privacy_authority", True),
        ("maori_authority_where_relevant", True),
        ("hardship_rule_enacted_and_interpreted", True),
        ("disconnection_rule_authorized", True),
        ("claim_class", "repository_water_decision"),
    ],
    "V6452-P07": [
        ("records_parse", False),
        ("object_ids_typed", False),
        ("modes_typed", False),
        ("only_stage_zero", False),
        ("path_multiplicity_absent", False),
        ("index_mutations", 1),
        ("claim_class", "conflicted_index_clean"),
    ],
    "V6452-P08": [
        ("descriptive_title", False),
        ("meta_refresh_count", 1),
        ("scripted_timer_count", 1),
        ("automatic_navigation_count", 1),
        ("visible_status_text", False),
        ("manual_evaluation_complete", True),
        ("claim_class", "complete_accessibility"),
    ],
    "V6452-P09": [
        ("enthalpy_constraint_declared", False),
        ("derivative_variables_typed", False),
        ("units_valid", False),
        ("inversion_scope_declared", False),
        ("equation_of_state_scoped", False),
        ("psyche_conversion", True),
        ("claim_class", "psyche_cooling_law"),
    ],
    "V6452-P10": [
        ("proxy_and_target_separated", False),
        ("target_evidence_nonzero_required", False),
        ("gaming_signal_retained", False),
        ("countermetric_visible", False),
        ("protected_gates_noncompensatory", False),
        ("independent_review_required", False),
        ("readiness_promoted", True),
    ],
}


def evaluate(proposal_id: str, row: dict[str, Any]) -> bool:
    baseline = BASE_CASES[proposal_id]
    if proposal_id in {"V6452-P03", "V6452-P06"}:
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
