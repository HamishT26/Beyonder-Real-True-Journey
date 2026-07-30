#!/usr/bin/env python3
"""Frozen x1 data for Caelen Morrow's v656-v4 phase."""

from __future__ import annotations

from ghc_family_v656_v4_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v656-v4"
PHASE_CODE = "V6564"
OWNER = "Caelen Morrow"
PRONOUNS = "they/them"
ROLE = "relational chronometry boundary-mapper and failure custodian"
HOPE = (
    "make every timing claim traceable while leaving real competence and "
    "authority where they belong"
)
BRANCH = "codex/GHC-Family/caelen-morrow-v656-v4-full-tools"
PHASE_ROOT = "docs/caelen-morrow/v656-v4"

SOURCE_OWNER = "Sylven Arc"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v656-v3-full-tools"
SOURCE_X1_FREEZE = "ae46f611f3b13b2ae77d0f0a13d35f13049ef75d"
SOURCE_EVIDENCE = "f0de53a52e9f4e99e6dda1ee6d02de8cfb4e7da6"
SOURCE_FINAL = "7a599e8c7fc6eba09a93c7541e05cb841e2ffd4c"
PRIOR_FROZEN = 2260
SOURCE_SEALED_REPOSITORY_NEGATIVES = 14183
SOURCE_EXTERNAL_NEGATIVES = 1
SOURCE_EFFECTIVE_NEGATIVES = 14184
SOURCE_OPEN_GAPS = 99
SOURCE_EXACT_GATES = 98
SOURCE_METHODS = 470
SOURCE_FAILED_WITNESSES = 470
SOURCE_PASSING_WITNESSES = 470

PRIMARY_FOCUS = (
    "GMUT Mind through bounded typed timepiece component, oscillator, gear-train, "
    "observation, provenance, and claim-firewall contracts, with THOS Body, Freed "
    "ID, and CBR Heart explicit and protected"
)
BOUNDED_PRACTICE = (
    "synthetic independent horology and timepiece service documentation used only "
    "as software, formal, structural, and learning lenses; no real person, customer, "
    "worker, owner, watchmaker, horologist, jeweller, conservator, manufacturer, "
    "supplier, insurer, valuer, building, workshop, timepiece, watch, clock, movement, "
    "component, image, battery, chemical, lubricant, tool, machine, measurement, test, "
    "adjustment, repair, cleaning, handling, packing, transport, return, disposal, "
    "accuracy, water-resistance, magnetic-resistance, shock-resistance, authenticity, "
    "valuation, fitness, safety, professional, customer, legal, cultural, Māori, "
    "affected-party, or operational decision"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_people_customers_workers_owners_watchmakers_horologists_jewellers_conservators_manufacturers_suppliers_insurers_valuers_and_affected_parties",
    "real_buildings_workshops_timepieces_watches_clocks_movements_components_images_batteries_chemicals_lubricants_tools_and_machines",
    "real_intake_custody_disassembly_cleaning_lubrication_adjustment_repair_reassembly_handling_packing_transport_return_and_disposal",
    "real_timing_pressure_water_magnetic_shock_electrical_chemical_material_and_authenticity_measurements_or_tests",
    "real_accuracy_chronometer_water_resistance_depth_diving_magnetic_resistance_shock_resistance_authenticity_value_fitness_and_safety_claims",
    "professional_horology_watchmaking_jewellery_conservation_engineering_science_safety_valuation_and_manufacturer_authority",
    "customer_consent_scope_estimate_payment_complaint_remedy_liability_and_return_authority",
    "production_identity_interoperability_live_keys_proofs_status_resolution_revocation_and_transparency_services",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_heirloom_memorial_sacred_object_taonga_collective_interest_and_maori_authority",
    "affected_party_acceptance_access_restriction_return_remedy_and_beneficiary_privacy",
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
            "are rejected, and the receipt makes no real-person, customer, object, "
            "component, image, material, measurement, test, service, safety, "
            "professional, production, legal, cultural, authority, effectiveness, "
            "authenticity, fitness, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, timepieces, "
            "components, images, materials, measurements, tests, services, participants, "
            "professional review, identity or transparency operations, trust decisions, "
            "and authority stay absent."
        )
    elif disposition == "open_gap":
        approval = (
            "candidate_real_collection_query_rights_api_key_professional_privacy_and_cultural_evidence_required"
        )
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-key, zero-query, zero-download, zero-object, "
            "zero-image, zero-row, zero-measurement, and zero-interpretation refusal "
            "receipt and leave professional, rights, privacy, accessibility, cultural, "
            "and authorization gaps open."
        )
    else:
        approval = (
            "exact_affected_party_legal_cultural_heirloom_sacred_object_taonga_collective_interest_and_maori_authority_required"
        )
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved person, family, whānau, heirloom, memorial, sacred-object, "
            "taonga-possibility, donor, collective-interest, privacy, image, access, "
            "repair, return, remedy, governance, legal, cultural, and authority "
            "reservations only; make no tangata-whenua, iwi, hapū, Māori-authority, "
            "competent-authority, or affected-party decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable obligations while "
            "refusing unsupported horology, object, component, image, material, "
            "measurement, test, service, safety, professional, identity, legal, "
            "cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen "
            "mutation, erases a failure, or exceeds its object, component, material, "
            "measurement, service, safety, professional, legal, cultural, or authority lane."
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
            "leave people, customers, workers, owners, watches, clocks, movements, "
            "components, images, batteries, chemicals, lubricants, tools, machines, "
            "measurements, tests, services, accounts, siblings, professional, "
            "production, legal, cultural, Māori-authority, and external state unchanged."
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
