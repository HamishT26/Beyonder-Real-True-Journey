#!/usr/bin/env python3
"""Pure structural models for the Eiren v644-v5 evidence packet."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def evaluate(proposal_id: str, row: dict[str, Any]) -> bool:
    if proposal_id == "V6445-P01":
        return bool(
            row.get("failure_signature")
            and row.get("trigger_preconditions")
            and row.get("validation_passed") is True
            and row.get("retained_negative_ids")
            and row.get("privacy_safe") is True
            and row.get("state") in {"validated", "preferred"}
            and row.get("rollback")
        )
    if proposal_id == "V6445-P02":
        return bool(
            row.get("conformal_factor_nonzero") is True
            and row.get("inverse_denominator_nonzero") is True
            and row.get("jacobian_full_rank") is True
            and row.get("singular_branches_declared") is True
            and row.get("matter_metric_declared") is True
            and row.get("causal_cone_accounted") is True
            and row.get("claim_class") == "formal_structural_only"
        )
    if proposal_id == "V6445-P03":
        return bool(
            row.get("derived_gmut_observable") is True
            and row.get("checksum_bound_real_rows") is True
            and row.get("lens_environment_covariance") is True
            and row.get("blind_holdout") is True
            and row.get("identifiability") is True
            and row.get("independent_review") is True
            and row.get("claim_class") == "empirical_analysis_ready"
        )
    if proposal_id == "V6445-P04":
        return bool(
            row.get("randomization_unit") == "site"
            and row.get("estimand_declared") in {"site_average", "participant_average"}
            and row.get("cluster_size_mechanism_declared") is True
            and row.get("recruitment_timing_declared") is True
            and row.get("contamination_modeled") is True
            and row.get("real_arm_count") == 0
            and row.get("claim_class") == "proxy_only"
        )
    if proposal_id == "V6445-P05":
        return bool(
            row.get("list_purpose") in {"revocation", "suspension"}
            and isinstance(row.get("issuer_epoch"), int)
            and isinstance(row.get("observed_epoch"), int)
            and row["observed_epoch"] >= row["issuer_epoch"]
            and row.get("cache_age_seconds", -1) <= row.get("maximum_cache_age_seconds", -2)
            and row.get("retrieval_failure_policy") == "indeterminate_not_valid"
            and row.get("claim_class") == "synthetic_proxy_only"
        )
    if proposal_id == "V6445-P06":
        return bool(
            row.get("authorized_affected_parties") is True
            and row.get("competent_legal_authority") is True
            and row.get("confidentiality_protocol") is True
            and row.get("reprisal_remedy_authority") is True
            and row.get("maori_authority_if_applicable") is True
            and row.get("real_case_privacy_assurance") is True
            and row.get("claim_class") == "authorized_case_action"
        )
    if proposal_id == "V6445-P07":
        return bool(
            row.get("source_revision_bound") is True
            and row.get("dependency_closure_complete") is True
            and row.get("file_count", 15001) < 15000
            and row.get("canonical_history_preserved") is True
            and row.get("rollback_declared") is True
            and row.get("public_remote_replaced") is False
            and row.get("claim_class") == "local_additive_companion"
        )
    if proposal_id == "V6445-P08":
        return bool(
            row.get("skip_link_first") is True
            and row.get("unique_main_target") is True
            and row.get("keyboard_reachable") is True
            and row.get("focus_visible") is True
            and row.get("target_not_hidden") is True
            and row.get("manual_user_evaluation") is False
            and row.get("claim_class") == "static_structural_only"
        )
    if proposal_id == "V6445-P09":
        return bool(
            row.get("physical_units_declared") is True
            and row.get("current_affinity_consistent") is True
            and row.get("housekeeping_rate_nonnegative") is True
            and row.get("steady_state_reference_declared") is True
            and row.get("coarse_graining_scope_declared") is True
            and row.get("psyche_conversion") is False
            and row.get("claim_class") == "physical_synthetic_only"
        )
    if proposal_id == "V6445-P10":
        return bool(
            row.get("risk_class_declared") is True
            and row.get("check_diversity_declared") is True
            and row.get("failed_checks_retained") is True
            and row.get("domain_vetoes_preserved") is True
            and row.get("authority_substitution") is False
            and row.get("independent_reproduction_claim") is False
            and row.get("claim_class") == "assurance_allocation_only"
        )
    raise KeyError(proposal_id)


BASE_CASES: dict[str, dict[str, Any]] = {
    "V6445-P01": {
        "failure_signature": "bounded signature",
        "trigger_preconditions": ["declared trigger"],
        "validation_passed": True,
        "retained_negative_ids": ["negative"],
        "privacy_safe": True,
        "state": "preferred",
        "rollback": "restore prior validated method",
    },
    "V6445-P02": {
        "conformal_factor_nonzero": True,
        "inverse_denominator_nonzero": True,
        "jacobian_full_rank": True,
        "singular_branches_declared": True,
        "matter_metric_declared": True,
        "causal_cone_accounted": True,
        "claim_class": "formal_structural_only",
    },
    "V6445-P03": {
        "derived_gmut_observable": False,
        "checksum_bound_real_rows": False,
        "lens_environment_covariance": False,
        "blind_holdout": False,
        "identifiability": False,
        "independent_review": False,
        "claim_class": "study_preregistration_only",
    },
    "V6445-P04": {
        "randomization_unit": "site",
        "estimand_declared": "participant_average",
        "cluster_size_mechanism_declared": True,
        "recruitment_timing_declared": True,
        "contamination_modeled": True,
        "real_arm_count": 0,
        "claim_class": "proxy_only",
    },
    "V6445-P05": {
        "list_purpose": "revocation",
        "issuer_epoch": 4,
        "observed_epoch": 4,
        "cache_age_seconds": 60,
        "maximum_cache_age_seconds": 300,
        "retrieval_failure_policy": "indeterminate_not_valid",
        "claim_class": "synthetic_proxy_only",
    },
    "V6445-P06": {
        "authorized_affected_parties": False,
        "competent_legal_authority": False,
        "confidentiality_protocol": False,
        "reprisal_remedy_authority": False,
        "maori_authority_if_applicable": False,
        "real_case_privacy_assurance": False,
        "claim_class": "neutral_question_set_only",
    },
    "V6445-P07": {
        "source_revision_bound": True,
        "dependency_closure_complete": True,
        "file_count": 900,
        "canonical_history_preserved": True,
        "rollback_declared": True,
        "public_remote_replaced": False,
        "claim_class": "local_additive_companion",
    },
    "V6445-P08": {
        "skip_link_first": True,
        "unique_main_target": True,
        "keyboard_reachable": True,
        "focus_visible": True,
        "target_not_hidden": True,
        "manual_user_evaluation": False,
        "claim_class": "static_structural_only",
    },
    "V6445-P09": {
        "physical_units_declared": True,
        "current_affinity_consistent": True,
        "housekeeping_rate_nonnegative": True,
        "steady_state_reference_declared": True,
        "coarse_graining_scope_declared": True,
        "psyche_conversion": False,
        "claim_class": "physical_synthetic_only",
    },
    "V6445-P10": {
        "risk_class_declared": True,
        "check_diversity_declared": True,
        "failed_checks_retained": True,
        "domain_vetoes_preserved": True,
        "authority_substitution": False,
        "independent_reproduction_claim": False,
        "claim_class": "assurance_allocation_only",
    },
}


MUTATIONS: dict[str, list[tuple[str, Any]]] = {
    "V6445-P01": [
        ("failure_signature", ""),
        ("trigger_preconditions", []),
        ("validation_passed", False),
        ("retained_negative_ids", []),
        ("privacy_safe", False),
        ("state", "candidate"),
        ("rollback", ""),
    ],
    "V6445-P02": [
        ("conformal_factor_nonzero", False),
        ("inverse_denominator_nonzero", False),
        ("jacobian_full_rank", False),
        ("singular_branches_declared", False),
        ("matter_metric_declared", False),
        ("causal_cone_accounted", False),
        ("claim_class", "empirically_equivalent"),
    ],
    "V6445-P03": [
        ("derived_gmut_observable", False),
        ("checksum_bound_real_rows", False),
        ("lens_environment_covariance", False),
        ("blind_holdout", False),
        ("identifiability", False),
        ("independent_review", False),
        ("claim_class", "confirmed"),
    ],
    "V6445-P04": [
        ("randomization_unit", "participant"),
        ("estimand_declared", ""),
        ("cluster_size_mechanism_declared", False),
        ("recruitment_timing_declared", False),
        ("contamination_modeled", False),
        ("real_arm_count", 1),
        ("claim_class", "effective"),
    ],
    "V6445-P05": [
        ("list_purpose", "unknown"),
        ("issuer_epoch", "four"),
        ("observed_epoch", 3),
        ("cache_age_seconds", 301),
        ("maximum_cache_age_seconds", -1),
        ("retrieval_failure_policy", "assume_valid"),
        ("claim_class", "production"),
    ],
    "V6445-P06": [
        ("authorized_affected_parties", False),
        ("competent_legal_authority", False),
        ("confidentiality_protocol", False),
        ("reprisal_remedy_authority", False),
        ("maori_authority_if_applicable", False),
        ("real_case_privacy_assurance", False),
        ("claim_class", "repository_decision"),
    ],
    "V6445-P07": [
        ("source_revision_bound", False),
        ("dependency_closure_complete", False),
        ("file_count", 15000),
        ("canonical_history_preserved", False),
        ("rollback_declared", False),
        ("public_remote_replaced", True),
        ("claim_class", "canonical_cutover"),
    ],
    "V6445-P08": [
        ("skip_link_first", False),
        ("unique_main_target", False),
        ("keyboard_reachable", False),
        ("focus_visible", False),
        ("target_not_hidden", False),
        ("manual_user_evaluation", True),
        ("claim_class", "complete_wcag"),
    ],
    "V6445-P09": [
        ("physical_units_declared", False),
        ("current_affinity_consistent", False),
        ("housekeeping_rate_nonnegative", False),
        ("steady_state_reference_declared", False),
        ("coarse_graining_scope_declared", False),
        ("psyche_conversion", True),
        ("claim_class", "consciousness_measure"),
    ],
    "V6445-P10": [
        ("risk_class_declared", False),
        ("check_diversity_declared", False),
        ("failed_checks_retained", False),
        ("domain_vetoes_preserved", False),
        ("authority_substitution", True),
        ("independent_reproduction_claim", True),
        ("claim_class", "stage20_ready"),
    ],
}


def proposal_cases(proposal_id: str) -> dict[str, Any]:
    baseline = deepcopy(BASE_CASES[proposal_id])
    baseline_accept = evaluate(proposal_id, baseline)
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
        "baseline_accept": baseline_accept,
        "cases": cases,
        "case_count": len(cases),
        "matched_count": sum(case["matched"] for case in cases),
    }
