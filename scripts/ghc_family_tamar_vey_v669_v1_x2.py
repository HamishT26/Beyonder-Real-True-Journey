#!/usr/bin/env python3
"""Fail-closed synthetic upholstery controls for Tamar Vey v669-v1 x2.

The module evaluates owner-local fixtures only. It never touches a real upholstered item,
material, product, person, workplace, identity service, network, or authority.
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
    "material_identity_or_fitness",
    "product_or_food_contact_safety",
    "workplace_or_fire_safety",
    "production_readiness",
    "deployment_authority",
    "legal_authority",
    "cultural_authority",
    "Māori_authority",
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
    "real_rows",
    "real_people",
    "real_materials",
    "external_actions",
    "network_requests",
    "production",
    "authority_state",
    "protected_claims",
    "source_use",
    "unit_domain",
    "rollback",
    "obligation_states",
}
EXPECTED_STATE = {
    "completed": "bounded_positive_witness",
    "represented": "represented_only",
    "open_gap": "open_gap_held",
    "exact_gate": "exact_gate_held",
}


SPECIAL_OBLIGATIONS: dict[str, list[str]] = {
    "TV6691-N019": [
        "UTF8_domain",
        "bitemporal_domain",
        "hash_domain",
        "number_as_text_refusal",
        "canonicalization_scope",
        "authenticity_noninference",
    ],
    "TV6691-N022": [
        "issue_escrow_id",
        "escrow_state",
        "timeout_state",
        "owner_vacancy",
        "capacity_token",
        "dual_readback_digest",
    ],
    "TV6691-N025": [
        "zero_real_keys",
        "zero_real_proofs",
        "disclosure_scope",
        "withdrawal_state",
        "contest_state",
        "expiry_state",
        "verifier_vacancy",
    ],
    "TV6691-N026": [
        "dependency_DAG",
        "refusal_edge",
        "work_cap_token",
        "correction_echo",
        "handover_vacancy",
        "zero_operator",
    ],
    "TV6691-N027": [
        "covariant_phase_space_scope",
        "presymplectic_current_scope",
        "boundary_flux_obligation",
        "gauge_degeneracy_obligation",
        "EFT_scope",
        "field_equation_vacancy",
        "observation_firewall",
    ],
    "TV6691-N023": [
        "official_vocabulary_class",
        "symbolic_class",
        "synthetic_rejection_class",
        "empirical_class",
        "professional_class",
        "authority_class",
        "nonpromotion_edges",
    ],
    "TV6691-N028": [
        "compressed_air_hold",
        "staple_and_sharp_tool_hold",
        "dust_hold",
        "adhesive_and_solvent_hold",
        "stored_energy_hold",
        "fire_hold",
        "ergonomics_hold",
        "workplace_hold",
        "no_safety_release",
    ],
    "TV6691-N029": ["practice_lens", "zero_real_upholstered_item", "zero_real_material", "zero_competence_inference"],
    "TV6691-N030": ["synthetic_studio_intake", "correction_readback", "workload_budget", "shift_handover", "zero_object_handling"],
    "TV6691-N031": ["structural_navigation", "error_summary", "text_status", "focus_order", "print_view", "human_review_reserved"],
    "TV6691-N032": ["THOS_proxy_only", "paired_synthetic_dockets", "symmetric_budget", "abstention_scoring", "zero_people", "no_effectiveness_estimate"],
    "TV6691-N033": ["Freed_ID_nonproduction", "issuer_vacant", "verifier_vacant", "status_service_vacant", "recovery_vacant", "correlation_risk"],
    "TV6691-N034": ["least_disclosure", "correction_evidence", "appeal_deadline", "remedy_vacancy", "decision_authority_abstention"],
    "TV6691-N035": ["typed_scalar_tensor_scope", "upholstery_stress_analogy_label", "physical_prediction_refusal"],
    "TV6691-N036": ["material_deformation_scope", "stored_energy_scope", "damping_scope", "agency_nonconversion", "justice_nonconversion", "mind_nonconversion"],
    "TV6691-N037": [
        "Smithsonian_Open_Access_vocabulary",
        "API_key_vacancy",
        "zero_network_requests",
        "zero_real_rows",
        "zero_media",
        "zero_object_identification",
        "rights_claim_refusal",
    ],
    "TV6691-N038": [
        "upholsterer_review_vacancy",
        "material_review_vacancy",
        "fire_and_workplace_review_vacancy",
        "ergonomics_review_vacancy",
        "accessibility_and_language_review_vacancy",
        "affected_party_review_vacancy",
    ],
    "TV6691-N039": [
        "upholstery_release_authority",
        "object_safety_authority",
        "custody_and_ownership_authority",
        "legal_and_cultural_authority",
        "affected_party_authority",
        "Māori_authority",
    ],
    "TV6691-N040": [
        "empirical_GMUT_receipt",
        "blinded_THOS_receipt",
        "live_identity_receipt",
        "governed_rights_receipt",
        "safety_and_professional_receipt",
        "independent_review_receipt",
        "non_substitution",
    ],
}


def obligations_for(row: dict[str, Any]) -> list[str]:
    if row["proposal_id"] in SPECIAL_OBLIGATIONS:
        return SPECIAL_OBLIGATIONS[row["proposal_id"]]
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
        "real_rows": 0,
        "real_people": 0,
        "real_materials": 0,
        "external_actions": 0,
        "network_requests": 0,
        "production": False,
        "authority_state": "vacant",
        "protected_claims": [],
        "source_use": "vocabulary_and_refusal_conditions_only",
        "unit_domain": "declared_or_not_applicable",
        "rollback": "retain_failure_stop_smallest_control",
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
    if fixture.get("execution_state") != EXPECTED_STATE[row["expected_disposition"]]:
        reasons.append("execution_state_mismatch")
    for field in ("real_rows", "real_people", "real_materials", "external_actions", "network_requests"):
        if fixture.get(field, 0) != 0:
            reasons.append(f"{field}_must_be_zero")
    if fixture.get("production") is not False:
        reasons.append("production_must_be_false")
    if fixture.get("authority_state") != "vacant":
        reasons.append("authority_must_remain_vacant")
    claims = fixture.get("protected_claims")
    if not isinstance(claims, list):
        reasons.append("protected_claims_wrong_type")
    elif claims or set(claims) & PROTECTED_CLAIMS:
        reasons.append("protected_claim_promotion")
    if fixture.get("source_use") != "vocabulary_and_refusal_conditions_only":
        reasons.append("source_credit_promotion")
    if fixture.get("unit_domain") != "declared_or_not_applicable":
        reasons.append("unit_domain_ambiguous")
    if fixture.get("rollback") != "retain_failure_stop_smallest_control":
        reasons.append("rollback_missing_or_promoted")
    obligations = fixture.get("obligation_states")
    expected = set(obligations_for(row))
    if not isinstance(obligations, dict):
        reasons.append("obligations_wrong_type")
    elif set(obligations) != expected or any(value != "declared" for value in obligations.values()):
        reasons.append("obligations_incomplete_or_promoted")
    accepted = not reasons
    return {
        "accepted": accepted,
        "reasons": reasons,
        "proposal_id": row["proposal_id"],
        "disposition": row["expected_disposition"],
        "completion_credit": int(accepted and row["expected_disposition"] == "completed"),
        "representation_credit": int(accepted and row["expected_disposition"] == "represented"),
        "open_gap_held": bool(accepted and row["expected_disposition"] == "open_gap"),
        "exact_gate_held": bool(accepted and row["expected_disposition"] == "exact_gate"),
    }


def mutated_fixture(row: dict[str, Any], mutation_class: str) -> dict[str, Any]:
    fixture = positive_fixture(row)
    if mutation_class == "missing_required_state":
        fixture.pop("proposal_id")
        fixture.pop("rollback")
    elif mutation_class == "ambiguous_domain_or_unit":
        fixture["unit_domain"] = "unspecified"
        fixture["real_rows"] = "zero"
    elif mutation_class == "real_world_or_external_action":
        fixture["real_materials"] = 1
        fixture["external_actions"] = 1
        fixture["evidence_class"] = "real_upholstery"
    elif mutation_class == "protected_claim_promotion":
        fixture["authority_state"] = "granted_by_software"
        fixture["protected_claims"] = ["professional_competence", "Māori_authority", "Stage_20"]
    else:
        raise ValueError(f"unknown mutation class: {mutation_class}")
    return fixture


def evaluate_runner_fixture(control_id: str, fixture: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if not control_id.startswith("ghc_family_upholstery_"):
        reasons.append("non_family_current_control_id")
    if fixture.get("domain") != "owner_local_synthetic":
        reasons.append("unbounded_domain")
    if fixture.get("authority_state") != "vacant":
        reasons.append("authority_not_vacant")
    if fixture.get("protected_claims") != []:
        reasons.append("protected_claim_promotion")
    if fixture.get("real_rows") != 0 or fixture.get("real_materials") != 0:
        reasons.append("real_state_not_zero")
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
        "real_materials": 0,
    }
    if args.fixture == "reject":
        fixture.update({"domain": "production", "authority_state": "granted_by_software", "real_materials": 1})
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
