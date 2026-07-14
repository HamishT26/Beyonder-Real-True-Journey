#!/usr/bin/env python3
"""Pure synthetic decision model for Orin Thale v644-v2 evidence cases."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


SPECS: dict[str, dict[str, Any]] = {
    "V6442-P01": {
        "outcome": "completed",
        "control": {
            "source_identity": "declared",
            "license_expression": "SPDX-VALID",
            "exception_binding": "explicit_or_none",
            "artifact_scope": "file_level",
            "access_class": "public_metadata_only",
            "redistribution_state": "unknown_without_review",
            "claim_class": "metadata_contract_only",
        },
        "mutations": {
            "source_identity": "missing",
            "license_expression": "guessed",
            "exception_binding": "detached",
            "artifact_scope": "implicit_repository_wide",
            "access_class": "private_material_assumed_public",
            "redistribution_state": "permitted_by_metadata",
            "claim_class": "legal_compatibility_established",
        },
    },
    "V6442-P02": {
        "outcome": "completed",
        "control": {
            "hypersurface_type": "declared_non_null",
            "normal_orientation": "minus_to_plus",
            "induced_metric": "typed_continuity_class",
            "jump_convention": "plus_minus_explicit",
            "scalar_matching": "value_and_normal_derivative_declared",
            "surface_source": "explicit_or_zero_by_derivation",
            "claim_class": "formal_obligation_only",
        },
        "mutations": {
            "hypersurface_type": "undeclared",
            "normal_orientation": "unoriented",
            "induced_metric": "silently_discontinuous",
            "jump_convention": "sign_flipped",
            "scalar_matching": "omitted",
            "surface_source": "hidden_distribution",
            "claim_class": "established_gmut_solution",
        },
    },
    "V6442-P03": {
        "outcome": "open_gap",
        "control": {
            "observable_map": "missing_model_specific_derivation",
            "eligible_rows": "zero_checksum_bound_timing_rows",
            "covariance": "missing_source_timing_covariance",
            "selection": "unfrozen",
            "blind_holdout": "absent",
            "independent_review": "absent",
            "claim_class": "open_gap_protocol_only",
        },
        "mutations": {
            "observable_map": "assumed_from_gr",
            "eligible_rows": "catalog_summary_called_likelihood",
            "covariance": "ignored",
            "selection": "post_hoc",
            "blind_holdout": "unblinded",
            "independent_review": "same_owner_called_independent",
            "claim_class": "empirical_confirmation",
        },
    },
    "V6442-P04": {
        "outcome": "represented",
        "control": {
            "exposure_origin": "preregistered_pre_outcome",
            "denominator": "arm_symmetric",
            "measurement_timing": "frozen_schedule",
            "switching_rule": "explicit_intercurrent_strategy",
            "confounder_set": "declared_proxy_assumptions",
            "real_arm_count": 0,
            "claim_class": "protocol_proxy_only",
        },
        "mutations": {
            "exposure_origin": "defined_after_outcome",
            "denominator": "arm_specific",
            "measurement_timing": "outcome_adaptive",
            "switching_rule": "discarded",
            "confounder_set": "assumed_complete",
            "real_arm_count": 2,
            "claim_class": "thos_effectiveness",
        },
    },
    "V6442-P05": {
        "outcome": "represented",
        "control": {
            "client_scheme": "declared",
            "request_digest": "synthetic_bound",
            "request_uri": "single_use_synthetic",
            "response_channel": "bound_to_request",
            "nonce": "unique_synthetic",
            "dcql_scope": "frozen_minimal",
            "claim_class": "structural_proxy_only",
        },
        "mutations": {
            "client_scheme": "substituted",
            "request_digest": "changed_after_consent",
            "request_uri": "replayed",
            "response_channel": "cross_client",
            "nonce": "reused",
            "dcql_scope": "silently_widened",
            "claim_class": "production_interoperability",
        },
    },
    "V6442-P06": {
        "outcome": "exact_gate",
        "control": {
            "fund_identity": "unassigned",
            "custodian": "unassigned",
            "beneficiary_rule": "unassigned",
            "distribution_amount": "unassigned",
            "conflict_decision": "unassigned",
            "authority_evidence": "absent_exact_participation",
            "claim_class": "exact_gate_unresolved",
        },
        "mutations": {
            "fund_identity": "repository_named",
            "custodian": "repository_selected",
            "beneficiary_rule": "repository_determined",
            "distribution_amount": "repository_set",
            "conflict_decision": "repository_resolved",
            "authority_evidence": "principles_document_substituted",
            "claim_class": "cultural_and_legal_ratification",
        },
    },
    "V6442-P07": {
        "outcome": "completed",
        "control": {
            "executable": "fully_qualified_or_verified",
            "argv": "explicit_sequence",
            "option_boundary": "declared",
            "leading_dash_operand": "handled",
            "shell": False,
            "environment": "minimal_allowlist",
            "claim_class": "bounded_fixture_only",
        },
        "mutations": {
            "executable": "path_ambiguous",
            "argv": "concatenated_string",
            "option_boundary": "missing",
            "leading_dash_operand": "parsed_as_option",
            "shell": True,
            "environment": "inherited_unbounded",
            "claim_class": "exhaustive_security",
        },
    },
    "V6442-P08": {
        "outcome": "completed",
        "control": {
            "href": "declared_safe_static_target",
            "visible_text": "descriptive",
            "accessible_name": "nonempty",
            "programmatic_context": "available",
            "duplicate_label_group": "consistent_destination",
            "icon_alternative": "decorative_or_named",
            "claim_class": "structural_audit_only",
        },
        "mutations": {
            "href": "empty_or_unsafe",
            "visible_text": "read_more_without_context",
            "accessible_name": "empty",
            "programmatic_context": "visual_only",
            "duplicate_label_group": "different_destinations_unflagged",
            "icon_alternative": "unnamed_only_content",
            "claim_class": "accessibility_complete",
        },
    },
    "V6442-P09": {
        "outcome": "completed",
        "control": {
            "regime": "near_equilibrium_linear_response",
            "force_flux_pairing": "typed_conjugate",
            "coefficient_units": "declared",
            "microscopic_reversibility": "explicit_assumption",
            "time_reversal_parity": "declared_per_variable",
            "field_reversal": "casimir_sign_rule_applied",
            "claim_class": "physics_classifier_only",
        },
        "mutations": {
            "regime": "far_from_equilibrium_unqualified",
            "force_flux_pairing": "generic_correlation",
            "coefficient_units": "missing",
            "microscopic_reversibility": "silently_assumed",
            "time_reversal_parity": "omitted",
            "field_reversal": "field_sign_ignored",
            "claim_class": "psyche_law",
        },
    },
    "V6442-P10": {
        "outcome": "completed",
        "control": {
            "reviewer_identity_class": "pseudonymous_declared_role",
            "owner_overlap": "declared",
            "institution_overlap": "declared_or_unknown",
            "data_code_overlap": "declared",
            "toolchain_overlap": "declared",
            "conflict_state": "unknown_is_veto",
            "claim_class": "dependence_graph_only",
        },
        "mutations": {
            "reviewer_identity_class": "same_reviewer_counted_twice",
            "owner_overlap": "same_owner_called_independent",
            "institution_overlap": "hidden",
            "data_code_overlap": "ignored",
            "toolchain_overlap": "ignored",
            "conflict_state": "unknown_treated_clear",
            "claim_class": "independent_review_and_reproduction",
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
    return {
        "proposal_id": proposal_id,
        "decision": spec["outcome"],
        "reasons": [],
        "retained_negative": False,
    }


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
