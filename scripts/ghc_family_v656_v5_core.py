#!/usr/bin/env python3
"""Bounded synthetic coffee-roasting contract and mutation engine for v656-v5."""

from __future__ import annotations

import copy
from collections import Counter
from typing import Any

import ghc_family_v656_v5_phase_data as d


MUTATION_CLASSES = [
    "missing_required_obligation",
    "wrong_type_or_domain",
    "resource_or_freshness_overrun",
    "unsupported_promotion",
    "authority_privacy_or_route_breach",
]

ZERO_REAL_COUNTS = {
    "people_or_customers": 0,
    "workers_or_professionals": 0,
    "workshops_or_buildings": 0,
    "coffee_lots_roasts_or_brews": 0,
    "beans_samples_or_packaging": 0,
    "images_or_media": 0,
    "water_food_chemicals_or_cleaners": 0,
    "roasters_grinders_brewers_or_instruments": 0,
    "measurements_sensory_sessions_or_tests": 0,
    "roasting_grinding_brewing_or_service_actions": 0,
    "handling_storage_packaging_transport_or_returns": 0,
    "identity_or_transparency_events": 0,
    "external_queries_or_downloads": 0,
    "legal_cultural_or_authority_decisions": 0,
    "participant_or_affected_party_events": 0,
}

FORBIDDEN_CLAIMS = [
    "real_food_or_beverage_produced",
    "professional_roasting_or_sensory_competence",
    "roast_profile_cup_quality_or_score",
    "food_safety_or_regulatory_compliance",
    "caffeine_or_nutrition",
    "origin_variety_or_processing_authenticity",
    "machinery_or_chemical_safety",
    "commercial_value_or_fitness",
    "customer_consent_or_remedy_decision",
    "privacy_or_accessibility_complete",
    "legal_or_cultural_legitimacy",
    "maori_authority",
    "independent_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def make_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.v656-v5.coffee-surface-contract.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "proposal_id": proposal["proposal_id"],
        "slug": proposal["slug"],
        "title": proposal["title"],
        "pillar": proposal["pillar"],
        "mechanism": proposal["mechanism"],
        "expected_disposition": proposal["expected_disposition"],
        "mode": "synthetic_zero_real_action",
        "required_obligations": [
            "synthetic_scope_declared",
            "source_vocabulary_bounded",
            "typed_fields_and_domains_declared",
            "uncertainty_or_absence_visible",
            "provenance_and_correction_visible",
            "five_mutation_classes_rejected",
            "rollback_preserves_external_state",
            "protected_gates_not_promoted",
        ],
        "official_source_ids": proposal["official_or_primary_source_needs"],
        "protected_gates": proposal["protected_gates"],
        "acceptance_gate": proposal["falsifier_or_acceptance_gate"],
        "rollback": proposal["rollback_or_recovery"],
        "resource_budget": {
            "max_records": 64,
            "max_assets": 0,
            "max_external_requests": 0,
            "max_real_objects": 0,
            "max_real_people": 0,
        },
        "freshness": {
            "source_metadata_checked_at": "2026-07-31",
            "real_observation_timestamp": None,
            "real_measurement_timestamp": None,
        },
        "zero_real_counts": copy.deepcopy(ZERO_REAL_COUNTS),
        "claim_flags": {claim: False for claim in FORBIDDEN_CLAIMS},
        "authority_state": {
            "real_producer_worker_or_customer_approval": "absent",
            "professional_review": "absent",
            "affected_party_acceptance": "absent",
            "legal_review": "absent",
            "cultural_review": "absent",
            "maori_authority": "absent",
            "terminal_route_contact": "absent",
        },
        "fixture": {
            "synthetic_token": f"SYNTHETIC-{proposal['proposal_id']}",
            "records": [],
            "assets": [],
            "external_requests": [],
            "notes": [
                "No real coffee, person, measurement, sensory session, roast, brew, service, or authority event."
            ],
        },
    }


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_top = {
        "schema",
        "phase",
        "owner",
        "proposal_id",
        "slug",
        "pillar",
        "mechanism",
        "expected_disposition",
        "mode",
        "required_obligations",
        "official_source_ids",
        "protected_gates",
        "acceptance_gate",
        "rollback",
        "resource_budget",
        "freshness",
        "zero_real_counts",
        "claim_flags",
        "authority_state",
        "fixture",
    }
    missing = sorted(required_top - contract.keys())
    if missing:
        errors.append("missing_top_fields:" + ",".join(missing))
    if contract.get("schema") != "ghc.family.v656-v5.coffee-surface-contract.v1":
        errors.append("wrong_schema")
    if contract.get("phase") != d.PHASE or contract.get("owner") != d.OWNER:
        errors.append("wrong_phase_or_owner")
    if contract.get("mode") != "synthetic_zero_real_action":
        errors.append("wrong_mode")
    if contract.get("expected_disposition") not in d.OUTCOME_CLASSES:
        errors.append("wrong_disposition")
    obligations = contract.get("required_obligations")
    if not isinstance(obligations, list) or len(obligations) != 8:
        errors.append("required_obligations_incomplete")
    if not isinstance(contract.get("official_source_ids"), list) or not contract.get(
        "official_source_ids"
    ):
        errors.append("source_ids_missing")
    if contract.get("protected_gates") != d.PROTECTED_GATES:
        errors.append("protected_gates_changed")
    budget = contract.get("resource_budget", {})
    if (
        not isinstance(budget.get("max_records"), int)
        or budget.get("max_records", 65) > 64
        or budget.get("max_assets") != 0
        or budget.get("max_external_requests") != 0
        or budget.get("max_real_objects") != 0
        or budget.get("max_real_people") != 0
    ):
        errors.append("resource_budget_overrun")
    zero_counts = contract.get("zero_real_counts")
    if not isinstance(zero_counts, dict) or zero_counts != ZERO_REAL_COUNTS:
        errors.append("real_count_or_domain_breach")
    flags = contract.get("claim_flags")
    if (
        not isinstance(flags, dict)
        or set(flags) != set(FORBIDDEN_CLAIMS)
        or any(value is not False for value in flags.values())
    ):
        errors.append("unsupported_claim_promotion")
    authority = contract.get("authority_state")
    if not isinstance(authority, dict) or any(
        value != "absent" for value in authority.values()
    ):
        errors.append("authority_or_route_breach")
    fixture = contract.get("fixture")
    if not isinstance(fixture, dict):
        errors.append("fixture_wrong_type")
    else:
        if fixture.get("records") != [] or fixture.get("assets") != []:
            errors.append("nonzero_fixture_data")
        if fixture.get("external_requests") != []:
            errors.append("external_request_breach")
        if not str(fixture.get("synthetic_token", "")).startswith("SYNTHETIC-V6565-P"):
            errors.append("synthetic_token_invalid")
    freshness = contract.get("freshness")
    if (
        not isinstance(freshness, dict)
        or freshness.get("source_metadata_checked_at") != "2026-07-31"
        or freshness.get("real_observation_timestamp") is not None
        or freshness.get("real_measurement_timestamp") is not None
    ):
        errors.append("freshness_or_real_observation_breach")
    return sorted(set(errors))


def mutations(contract: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    items: list[tuple[str, dict[str, Any]]] = []
    missing = copy.deepcopy(contract)
    missing.pop("rollback")
    items.append((MUTATION_CLASSES[0], missing))

    wrong = copy.deepcopy(contract)
    wrong["zero_real_counts"]["measurements_sensory_sessions_or_tests"] = "zero"
    items.append((MUTATION_CLASSES[1], wrong))

    overrun = copy.deepcopy(contract)
    overrun["resource_budget"]["max_external_requests"] = 1
    overrun["fixture"]["external_requests"] = ["forbidden-synthetic-placeholder"]
    items.append((MUTATION_CLASSES[2], overrun))

    promotion = copy.deepcopy(contract)
    promotion["claim_flags"]["roast_profile_cup_quality_or_score"] = True
    items.append((MUTATION_CLASSES[3], promotion))

    authority = copy.deepcopy(contract)
    authority["authority_state"]["maori_authority"] = "claimed"
    authority["authority_state"]["terminal_route_contact"] = "attempted"
    items.append((MUTATION_CLASSES[4], authority))
    return items


def execute_contract(contract: dict[str, Any]) -> dict[str, Any]:
    valid_errors = validate_contract(contract)
    mutation_rows = []
    for index, (mutation_class, mutated) in enumerate(mutations(contract), 1):
        errors = validate_contract(mutated)
        mutation_rows.append(
            {
                "mutation_id": f"{contract['proposal_id']}-M{index}",
                "mutation_class": mutation_class,
                "accepted": not errors,
                "rejected": bool(errors),
                "errors": errors,
                "retained_negative_id": f"V6565-NEG-MUT-{contract['proposal_id'][-2:]}-{index}",
            }
        )
    passed = not valid_errors and all(row["rejected"] for row in mutation_rows)
    return {
        "schema": "ghc.family.v656-v5.runner-result.v1",
        "proposal_id": contract["proposal_id"],
        "slug": contract["slug"],
        "valid_fixture_errors": valid_errors,
        "valid_fixture_passed": not valid_errors,
        "mutation_count": len(mutation_rows),
        "mutations_rejected": sum(row["rejected"] for row in mutation_rows),
        "mutation_rows": mutation_rows,
        "passed": passed,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": (
            "Deterministic synthetic software evidence only; no real coffee, person, "
            "measurement, sensory session, roast, brew, professional review, authority, "
            "or Stage 20 claim."
        ),
    }


def run_proposals(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [execute_contract(make_contract(proposal)) for proposal in proposals]
    return {
        "schema": "ghc.family.v656-v5.suite-result.v1",
        "proposal_count": len(rows),
        "passed": sum(row["passed"] for row in rows),
        "failed": sum(not row["passed"] for row in rows),
        "mutations": sum(row["mutation_count"] for row in rows),
        "mutations_rejected": sum(row["mutations_rejected"] for row in rows),
        "outcomes": dict(
            Counter(proposal["expected_disposition"] for proposal in proposals)
        ),
        "rows": rows,
        "valid": all(row["passed"] for row in rows),
    }
