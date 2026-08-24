#!/usr/bin/env python3
"""Bounded synthetic controls for Orin Thale v668-v7 x2.

This module evaluates owner-local fixtures only.  It does not touch real books,
people, identities, accounts, networks, instruments, services, or authorities.
"""

from __future__ import annotations

import argparse
import json
from typing import Any


ALLOWED_DISPOSITIONS = {"completed", "represented", "open_gap", "exact_gate"}
PROTECTED_CLAIMS = {
    "empirical_confirmation",
    "participant_evidence",
    "professional_competence",
    "production_readiness",
    "deployment_authority",
    "legal_authority",
    "cultural_authority",
    "Maori_authority",
    "affected_party_approval",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "AGI_or_ASI",
    "consciousness_or_personhood",
    "Theory_of_Everything",
    "proof_or_canon",
    "Stage_20",
}
COMMON_REQUIRED = {
    "proposal_id",
    "disposition",
    "evidence_class",
    "execution_state",
    "empirical_rows",
    "real_people",
    "external_actions",
    "production",
    "authority_state",
    "protected_claims",
    "source_use",
    "obligation_states",
}
EXPECTED_STATE = {
    "completed": "bounded_positive_witness",
    "represented": "represented_only",
    "open_gap": "open_gap_held",
    "exact_gate": "exact_gate_held",
}


SPECIAL_OBLIGATIONS: dict[str, list[str]] = {
    "OR6687-N027": [
        "two_point_distribution_scope",
        "wavefront_set_orientation",
        "Hadamard_condition",
        "causal_support",
        "units",
        "domain",
        "observation_firewall",
        "no_physical_solution_claim",
    ],
    "OR6687-N028": [
        "citation_class",
        "symbolic_class",
        "synthetic_class",
        "empirical_class",
        "authority_class",
        "nonpromotion_edges",
    ],
    "OR6687-N029": ["practice_lens", "zero_real_object", "zero_competence_inference", "handover_vacancy"],
    "OR6687-N030": ["library_preparation_proxy", "correction_readback", "workload_budget", "shift_handover"],
    "OR6687-N031": ["structural_accessibility", "manual_review_reserved", "affected_user_review_reserved"],
    "OR6687-N032": ["bounded_retry", "hold_point", "stop_token", "readback", "handover", "zero_operator"],
    "OR6687-N033": ["zero_key", "synthetic_alias", "correction", "challenge", "trust_governance_vacancy"],
    "OR6687-N034": ["access_vacancy", "privacy_vacancy", "contestability", "remedy_vacancy", "authority_vacancy"],
    "OR6687-N035": ["formal_adjacency", "analogy_label", "physical_prediction_refusal"],
    "OR6687-N036": ["energy_quantity", "material_change", "agency_nonconversion", "justice_nonconversion", "mind_nonconversion"],
    "OR6687-N037": [
        "GWOSC_v2_metadata_schema",
        "data_quality_vacancy",
        "provenance_vacancy",
        "zero_network_requests",
        "zero_rows",
        "zero_likelihoods",
        "inference_refusal",
    ],
    "OR6687-N038": [
        "bookbinder_review_vacancy",
        "conservator_review_vacancy",
        "librarian_review_vacancy",
        "accessibility_review_vacancy",
        "language_review_vacancy",
        "affected_party_review_vacancy",
    ],
    "OR6687-N039": [
        "treatment_release_authority",
        "copyright_authority",
        "property_authority",
        "access_authority",
        "cultural_care_authority",
        "Maori_authority",
    ],
    "OR6687-N040": [
        "empirical_GMUT_receipt",
        "blinded_THOS_receipt",
        "live_identity_receipt",
        "governed_rights_receipt",
        "independent_review_receipt",
        "noncompensation",
    ],
}


def obligations_for(row: dict[str, Any]) -> list[str]:
    proposal_id = row["proposal_id"]
    if proposal_id in SPECIAL_OBLIGATIONS:
        return SPECIAL_OBLIGATIONS[proposal_id]
    slug = row["semantic_slug"]
    return [
        f"{slug}_identity",
        f"{slug}_declared_state",
        f"{slug}_unit_or_domain",
        f"{slug}_failure_refusal",
        "real_material_vacancy",
        "professional_authority_vacancy",
    ]


def positive_fixture(row: dict[str, Any]) -> dict[str, Any]:
    disposition = row["expected_disposition"]
    return {
        "proposal_id": row["proposal_id"],
        "disposition": disposition,
        "evidence_class": "owner_local_synthetic",
        "execution_state": EXPECTED_STATE[disposition],
        "empirical_rows": 0,
        "real_people": 0,
        "external_actions": 0,
        "network_requests": 0,
        "likelihood_evaluations": 0,
        "production": False,
        "authority_state": "vacant",
        "protected_claims": [],
        "source_use": "vocabulary_and_refusal_conditions_only",
        "obligation_states": {name: "declared" for name in obligations_for(row)},
    }


def evaluate_fixture(row: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    missing = sorted(COMMON_REQUIRED - set(fixture))
    if missing:
        reasons.append("missing_required_fields:" + ",".join(missing))
    if fixture.get("proposal_id") != row["proposal_id"]:
        reasons.append("proposal_id_mismatch")
    disposition = fixture.get("disposition")
    if disposition not in ALLOWED_DISPOSITIONS or disposition != row["expected_disposition"]:
        reasons.append("disposition_mismatch")
    if fixture.get("evidence_class") != "owner_local_synthetic":
        reasons.append("evidence_class_not_bounded_synthetic")
    if fixture.get("execution_state") != EXPECTED_STATE.get(row["expected_disposition"]):
        reasons.append("execution_state_mismatch")
    for field in ("empirical_rows", "real_people", "external_actions", "network_requests", "likelihood_evaluations"):
        if fixture.get(field, 0) != 0:
            reasons.append(f"{field}_must_be_zero")
    if fixture.get("production") is not False:
        reasons.append("production_must_be_false")
    if fixture.get("authority_state") != "vacant":
        reasons.append("authority_must_remain_vacant")
    claims = fixture.get("protected_claims")
    if not isinstance(claims, list):
        reasons.append("protected_claims_wrong_type")
    elif set(claims) & PROTECTED_CLAIMS or claims:
        reasons.append("protected_claim_promotion")
    if fixture.get("source_use") != "vocabulary_and_refusal_conditions_only":
        reasons.append("source_credit_promotion")
    obligations = fixture.get("obligation_states")
    expected_obligations = set(obligations_for(row))
    if not isinstance(obligations, dict):
        reasons.append("obligations_wrong_type")
    elif set(obligations) != expected_obligations or any(value != "declared" for value in obligations.values()):
        reasons.append("obligations_incomplete_or_promoted")
    return {
        "accepted": not reasons,
        "reasons": reasons,
        "proposal_id": row["proposal_id"],
        "disposition": row["expected_disposition"],
        "completion_credit": 1 if not reasons and row["expected_disposition"] == "completed" else 0,
        "representation_credit": 1 if not reasons and row["expected_disposition"] == "represented" else 0,
        "open_gap_held": not reasons and row["expected_disposition"] == "open_gap",
        "exact_gate_held": not reasons and row["expected_disposition"] == "exact_gate",
    }


def mutated_fixture(row: dict[str, Any], mutation_class: str) -> dict[str, Any]:
    fixture = positive_fixture(row)
    if mutation_class == "missing_required_field":
        fixture.pop("proposal_id")
    elif mutation_class == "wrong_type_or_domain":
        fixture["evidence_class"] = "production"
        fixture["empirical_rows"] = "zero"
    elif mutation_class == "forbidden_claim_promotion":
        fixture["protected_claims"] = ["professional_competence", "Stage_20"]
    elif mutation_class == "boundary_order_or_authority_bypass":
        fixture["authority_state"] = "granted_by_software"
        fixture["external_actions"] = 1
    else:
        raise ValueError(f"unknown mutation class: {mutation_class}")
    return fixture


def evaluate_runner_fixture(control_id: str, fixture: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if not control_id.startswith("ghc_family_"):
        reasons.append("non_family_current_control_id")
    if fixture.get("domain") != "owner_local_synthetic":
        reasons.append("unbounded_domain")
    if fixture.get("authority_state") != "vacant":
        reasons.append("authority_not_vacant")
    if fixture.get("protected_claims") != []:
        reasons.append("protected_claim_promotion")
    if fixture.get("real_rows") != 0:
        reasons.append("real_rows_not_zero")
    return {"accepted": not reasons, "control_id": control_id, "reasons": reasons}


def runner_main(control_id: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", choices=("accept", "reject"), required=True)
    args = parser.parse_args()
    fixture = {
        "domain": "owner_local_synthetic",
        "authority_state": "vacant",
        "protected_claims": [],
        "real_rows": 0,
    }
    if args.fixture == "reject":
        fixture["domain"] = "production"
        fixture["authority_state"] = "granted_by_software"
    result = evaluate_runner_fixture(control_id, fixture)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["accepted"] else 2


__all__ = [
    "ALLOWED_DISPOSITIONS",
    "PROTECTED_CLAIMS",
    "evaluate_fixture",
    "evaluate_runner_fixture",
    "mutated_fixture",
    "obligations_for",
    "positive_fixture",
    "runner_main",
]
