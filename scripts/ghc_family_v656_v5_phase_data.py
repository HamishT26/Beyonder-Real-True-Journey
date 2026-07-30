#!/usr/bin/env python3
"""Frozen x1 data for Eiren Kestrel's v656-v5 phase."""

from __future__ import annotations

from ghc_family_v656_v5_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v656-v5"
PHASE_CODE = "V6565"
OWNER = "Eiren Kestrel"
PRONOUNS = "they/them"
ROLE = "relational thermodynamic boundary-cartographer and evidence custodian"
HOPE = (
    "make each coupled heat, mass, provenance, and authority claim small enough "
    "to falsify while keeping every real decision with competent and affected people"
)
BRANCH = "codex/GHC-Family/eiren-kestrel-v656-v5-full-tools"
PHASE_ROOT = "docs/eiren-kestrel/v656-v5"

SOURCE_OWNER = "Caelen Morrow"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v656-v4-full-tools"
SOURCE_X1_FREEZE = "1c84cf2616df4efbb13c2df89397941251e2def5"
SOURCE_EVIDENCE = "6f6c32a470b25ee46d16c2f8207018c701c81e02"
SOURCE_CLOSEOUT = "f5a8bcfc1480b4d600806b75a3c921bf3a132bb5"
SOURCE_DOCUMENT_CAP_CORRECTION = "14a04ce7607a839bcbff42d6daf59a1f1f24d2ed"
SOURCE_FINAL = "c1518e6873068f6cc20ff69a30437d69404ef057"
SOURCE_SUCCESSFUL_RECEIPT_SHA256 = (
    "15d4137f9452e4c54cc75b3d78d2cde910376d4b9d84bb139fdc4c4d5366f275"
)
PRIOR_FROZEN = 2290
SOURCE_SEALED_REPOSITORY_NEGATIVES = 14357
SOURCE_EXTERNAL_NEGATIVES = 1
SOURCE_EFFECTIVE_NEGATIVES = 14358
SOURCE_OPEN_GAPS = 100
SOURCE_EXACT_GATES = 99
SOURCE_METHODS = 644
SOURCE_FAILED_WITNESSES = 644
SOURCE_PASSING_WITNESSES = 644

PRIMARY_FOCUS = (
    "GMUT Mind through bounded typed coffee roast heat-and-mass transfer, "
    "porous-flow, observation, uncertainty, provenance, and claim-firewall "
    "contracts, with THOS Body, Freed ID, and CBR Heart explicit and protected"
)
BOUNDED_PRACTICE = (
    "synthetic specialty-coffee roasting and brew-lab documentation used only "
    "as software, formal, structural, and learning lenses; no real person, "
    "producer, farmer, cooperative, worker, customer, roaster, barista, cupper, "
    "food verifier, laboratory, farm, mill, warehouse, roastery, café, coffee, "
    "bean, lot, roast, grind, beverage, water, milk, allergen, chemical, machine, "
    "roaster, grinder, brewer, vessel, filter, package, image, measurement, test, "
    "analysis, tasting, preparation, service, food-safety, machinery-safety, "
    "quality, value, certification, origin, health, nutrition, professional, "
    "consumer, legal, cultural, indigenous, Māori, affected-party, or operational "
    "decision"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_people_producers_farmers_cooperatives_workers_customers_roasters_baristas_cuppers_food_verifiers_laboratories_and_affected_parties",
    "real_farms_mills_warehouses_roasteries_cafes_coffee_beans_lots_roasts_grinds_beverages_water_milk_allergens_chemicals_machines_vessels_filters_packages_and_images",
    "real_sampling_roasting_grinding_brewing_tasting_cleaning_packaging_storage_transport_service_recall_and_disposal",
    "real_temperature_mass_flow_pressure_particle_concentration_caffeine_acrylamide_contaminant_nutrition_sensory_and_laboratory_measurements_or_tests",
    "real_food_safety_machinery_heat_steam_pressure_electrical_guarding_isolation_emergency_and_stop_work_decisions",
    "real_quality_grade_score_value_freshness_shelf_life_fitness_health_nutrition_origin_certification_ethical_and_sustainability_claims",
    "professional_coffee_roasting_brewing_cupping_food_science_laboratory_engineering_safety_and_verification_authority",
    "consumer_scope_description_price_payment_complaint_remedy_liability_recall_and_return_authority",
    "production_identity_interoperability_live_keys_proofs_status_resolution_revocation_and_transparency_services",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_indigenous_traditional_knowledge_origin_place_collective_interest_data_governance_and_maori_authority",
    "affected_party_acceptance_access_restriction_benefit_living_income_remedy_and_beneficiary_privacy",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def _proposal(
    number: int,
    title: str,
    slug: str,
    pillar: str,
    disposition: str,
    mechanism: str,
    sources: list[str],
) -> dict:
    if disposition == "completed":
        approval = "safe_now_bounded_structural_formal_or_synthetic_software"
        lane = "x2_owner_local_bounded"
        acceptance = (
            "The valid synthetic fixture passes, all five preregistered mutations "
            "are rejected, and the receipt makes no real-person, producer, worker, "
            "customer, coffee, food, machine, material, measurement, test, service, "
            "safety, professional, production, legal, cultural, authority, quality, "
            "value, health, fitness, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, coffee, "
            "food, machines, materials, measurements, tests, tasting, services, "
            "participants, professional review, identity or transparency operations, "
            "trust decisions, and authority stay absent."
        )
    elif disposition == "open_gap":
        approval = (
            "candidate_real_food_data_query_api_key_nutrition_professional_privacy_and_interpretation_evidence_required"
        )
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-key, zero-request, zero-download, zero-food, "
            "zero-row, zero-measurement, zero-nutrient-interpretation, and zero-health-"
            "conclusion refusal receipt and leave professional, privacy, accessibility, "
            "interpretation, and authorization gaps open."
        )
    else:
        approval = (
            "exact_producer_worker_affected_party_legal_cultural_indigenous_traditional_knowledge_data_governance_and_maori_authority_required"
        )
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved producer, farmer, cooperative, worker, origin, place, "
            "indigenous and traditional-knowledge possibility, living-income, benefit, "
            "privacy, remedy, legal, cultural, data-governance, and authority "
            "reservations only; make no producer, affected-party, tangata-whenua, iwi, "
            "hapū, Māori-authority, competent-authority, or community decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable obligations while "
            "refusing unsupported coffee, food, machine, material, measurement, sensory, "
            "safety, professional, identity, legal, cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen "
            "mutation, erases a failure, or exceeds its coffee, food, machine, material, "
            "measurement, safety, professional, legal, cultural, or authority lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": acceptance,
        "rollback_or_recovery": (
            "Stop, retain the failed witness at zero credit, rewrite no history, and "
            "leave people, producers, farmers, cooperatives, workers, customers, "
            "coffee, food, water, milk, allergens, chemicals, machines, vessels, "
            "packages, images, measurements, tests, tasting, services, accounts, "
            "siblings, professional, production, legal, cultural, Māori-authority, "
            "and external state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
    }


PROPOSALS = [_proposal(*row) for row in PROPOSAL_ROWS]
SAFE_TASKS = [
    f"Build the bounded contract and five rejecting fixtures for {row['proposal_id']} {row['slug']}"
    for row in PROPOSALS
]
CANDIDATE_TASKS = [
    f"Resolve only the declared evidence lane for {row['proposal_id']} {row['mechanism']}"
    for row in PROPOSALS
]
CLEAN_TASKS = [
    f"{kind} owner-local {surface} without deletion, sibling mutation, gate weakening, or unsupported promotion"
    for kind in ("CLEAN", "FIX", "REFINE")
    for surface in CLEAN_SURFACES
]
