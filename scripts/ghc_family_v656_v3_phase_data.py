#!/usr/bin/env python3
"""Frozen x1 data for Sylven Arc's v656-v3 phase."""

from __future__ import annotations

from ghc_family_v656_v3_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v656-v3"
PHASE_CODE = "V6563"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint-cartographer and falsifier-keeper"
HOPE = "keep each claim small enough to test, each failure visible, and each authority boundary intact"
BRANCH = "codex/GHC-Family/sylven-arc-v656-v3-full-tools"
PHASE_ROOT = "docs/sylven-arc/v656-v3"

SOURCE_OWNER = "Elowen Cairn"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v656-v2-full-tools"
SOURCE_X1_FREEZE = "8264f7fc34cf61d4c35026a92ca3cdb4807d2c3c"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "16f5af6a7b0ae03deb1d692b392f579d608985bb"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "b18aab36fd8193fce55df3d5b7055b94354dda7e"
PRIOR_FROZEN = 2230
SOURCE_SEALED_REPOSITORY_NEGATIVES = 13998
SOURCE_LIVE_OVERLAY: list[dict] = []
SOURCE_EFFECTIVE_NEGATIVES = 13998
SOURCE_OPEN_GAPS = 98
SOURCE_EXACT_GATES = 97
SOURCE_METHODS_SEALED = 435
SOURCE_ROUTE_METHODS = 0
SOURCE_METHODS = 435
SOURCE_ROUTE_METHOD_ROWS: list[tuple] = []

PRIMARY_FOCUS = (
    "Freed ID and CBR Heart through bounded synthetic stained-glass panel, "
    "fragment, condition-image, intervention, provenance, custody, privacy, "
    "accessibility, remedy, and authority-reservation contracts, with GMUT Mind "
    "and THOS Body explicit and protected"
)
BOUNDED_PRACTICE = (
    "synthetic stained-glass conservation documentation, panel and fragment "
    "provenance, condition mapping, proposed-intervention lineage, image records, "
    "packing, custody, accessibility, workload, privacy, remedy, and handover used "
    "only as software, formal, structural, and learning lenses; no real person, "
    "worker, owner, custodian, donor, conservator, glazier, architect, scientist, "
    "building, place, panel, glass, came, foil, solder, paint, stain, fragment, "
    "image, crate, tool, equipment, material, measurement, test, treatment, "
    "handling, transport, installation, exposure assessment, safety decision, "
    "professional competence, heritage determination, legal decision, cultural "
    "decision, Māori wording, affected-party acceptance, or Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_people_workers_owners_custodians_donors_conservators_glaziers_and_affected_parties",
    "real_buildings_places_panels_glass_came_foil_solder_paint_stain_fragments_images_crates_tools_and_equipment",
    "real_measurement_analysis_testing_treatment_handling_packing_transport_installation_and_monitoring",
    "real_material_colour_optical_structural_condition_authentication_and_heritage_determinations",
    "real_lead_exposure_guarding_isolation_stop_work_emergency_and_safety_decisions",
    "professional_conservation_glazing_architecture_engineering_science_safety_and_heritage_authority",
    "production_identity_interoperability_live_keys_proofs_status_resolution_revocation_and_transparency_services",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_sacred_image_taonga_donor_collective_interest_and_maori_authority",
    "affected_party_acceptance_access_restriction_return_repatriation_remedy_and_beneficiary_privacy",
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
            "The valid fixture passes, all five preregistered mutations are rejected, "
            "and the receipt makes no real-person, object, building, material, image, "
            "measurement, treatment, safety, professional, production, legal, cultural, "
            "authority, effectiveness, authenticity, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, objects, buildings, "
            "materials, images, measurements, treatments, participants, professional review, "
            "identity or transparency operations, trust decisions, and authority stay absent."
        )
    elif disposition == "open_gap":
        approval = (
            "candidate_real_collection_object_measurement_rights_professional_and_privacy_evidence_required"
        )
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-object, zero-image, zero-query, zero-download, "
            "zero-measurement, zero-interpretation, and zero-row refusal receipt and leave "
            "empirical, professional, rights, privacy, accessibility, cultural, and "
            "authorization gaps open."
        )
    else:
        approval = (
            "exact_affected_party_legal_cultural_sacred_image_taonga_collective_interest_and_maori_authority_required"
        )
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved person, whānau, building, place, subject, sacred-image, taonga-"
            "possibility, donor, collective-interest, disability, privacy, access, restriction, "
            "return, repatriation, remedy, governance, legal, cultural, and authority reservations "
            "only; make no tangata-whenua, iwi, hapū, Māori-authority, competent-authority, or "
            "affected-party decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable obligations while "
            "refusing unsupported conservation, glazing, optical, structural, material, "
            "safety, professional, identity, legal, cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or exceeds its conservation, object, material, measurement, "
            "safety, professional, legal, cultural, or authority lane."
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
            "Stop, retain the failed witness at zero credit, rewrite no history, and leave "
            "people, whānau, workers, owners, custodians, donors, buildings, places, panels, "
            "glass, came, foil, solder, paint, stain, fragments, images, crates, tools, "
            "equipment, materials, measurements, tests, treatments, handling, transport, "
            "installation, accounts, siblings, professional, production, legal, cultural, "
            "Māori-authority, and external state unchanged."
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
