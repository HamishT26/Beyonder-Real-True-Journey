#!/usr/bin/env python3
"""Frozen x1 data for Auren Lark's v655-v4 phase."""

from __future__ import annotations

from ghc_family_v655_v4_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v655-v4"
PHASE_CODE = "V6554"
OWNER = "Auren Lark"
PRONOUNS = "they/them"
ROLE = "relational evidence-path cartographer and repair-traceability steward"
HOPE = (
    "make every repair path legible, recoverable, and honest while keeping "
    "craft, safety, privacy, legal, cultural, and Māori-authority gates explicit"
)
BRANCH = "codex/GHC-Family/auren-lark-v655-v4-full-tools"
PHASE_ROOT = "docs/auren-lark/v655-v4"

SOURCE_OWNER = "Ilyra Fen"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v655-v3-full-tools"
SOURCE_X1_FREEZE = "e98b40654e48f5adb75f8d436256978e4eb51070"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "009228e1a22ee840f2e13eda2718579136c02335"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "935f82a74348f702eb264e42f1f0ced08be4e98d"
PRIOR_FROZEN = 2020
SOURCE_SEALED_REPOSITORY_NEGATIVES = 12720
SOURCE_LIVE_OVERLAY: list[dict] = [
    {
        "negative_id": "V6553-POST-N01",
        "failure": (
            "A combined postflight wrapper used an invalid PowerShell "
            "command-and-status expression and failed before changing Git or route state."
        ),
        "credit": "zero",
    },
    {
        "negative_id": "V6553-POST-N02",
        "failure": (
            "The task-list surface rejected its documented query field before "
            "returning a task or changing route state."
        ),
        "credit": "zero",
    },
    {
        "negative_id": "V6553-POST-N03",
        "failure": (
            "The fallback unfiltered task listing rejected a limit of 100 before "
            "returning a task or changing route state."
        ),
        "credit": "zero",
    },
    {
        "negative_id": "V6553-POST-N04",
        "failure": (
            "The first exact Auren task reread exceeded the tool context before "
            "the one acknowledged activation."
        ),
        "credit": "zero",
    },
]
SOURCE_EFFECTIVE_NEGATIVES = 12724
SOURCE_OPEN_GAPS = 91
SOURCE_EXACT_GATES = 90
SOURCE_METHODS_SEALED = 228
SOURCE_METHODS = 228

PRIMARY_FOCUS = (
    "THOS Body and CBR Heart through bounded synthetic stringed-instrument "
    "repair and setup traceability"
)
BOUNDED_PRACTICE = (
    "stringed-instrument repair intake, component and material provenance, "
    "represented setup, tension, fret, adhesive, clamping, finish, acoustic, and "
    "handover states, privacy minimization, correction, and remedy routing, used "
    "only as a bounded synthetic software and evidence-assurance lens; no real "
    "person, instrument, timber determination, measurement, load, tool operation, "
    "cutting, sanding, heating, solvent use, gluing, clamping, setup, valuation, "
    "performance, craft service, consumer decision, legal decision, cultural "
    "decision, taonga determination, or Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_empirical_data_measurement_and_likelihood",
    "real_people_property_information_participants_and_affected_parties",
    "professional_luthiery_repair_setup_conservation_and_safety_authority",
    "production_identity_interoperability_repair_release_and_service",
    "real_instruments_materials_tools_measurements_loads_and_workshop_operations",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance_complaint_remedy_and_beneficiary_privacy",
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
        approval = "safe_now_bounded_structural_or_synthetic_software"
        lane = "x2_owner_local_bounded"
        acceptance = (
            "The valid fixture passes, all five preregistered mutations are "
            "rejected, and the receipt makes no real-person, instrument, craft, "
            "safety, professional, production, authority, effectiveness, or "
            "completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, "
            "instruments, materials, tools, measurements, loads, repair operations, "
            "valuations, performances, and professional craft decisions stay absent."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_material_participant_and_professional_evidence_required"
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-job, zero-instrument, zero-material, zero-tool, "
            "zero-measurement, zero-load, zero-operation refusal receipt and leave "
            "the empirical, professional, privacy, and authorization gap open."
        )
    else:
        approval = "exact_affected_party_legal_cultural_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved access, informed-choice, disability, privacy, "
            "affordability, complaint, remedy, language, governance, and authority "
            "reservations only; make no legal, cultural, Māori-authority, "
            "tangata-whenua, iwi, hapū, or affected-party decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable obligations "
            "while refusing unsupported craft, safety, identity, scientific, "
            "operational, legal, cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a "
            "frozen mutation, erases a failure, or exceeds its evidence, craft, "
            "safety, privacy, professional, legal, cultural, or authority lane."
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
            "Stop, retain the failed witness at zero credit, rewrite no history, "
            "and leave people, instruments, materials, tools, workshops, accounts, "
            "siblings, professional, production, legal, cultural, Māori-authority, "
            "and external state unchanged."
        ),
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
    }


PROPOSALS = [_proposal(*row) for row in PROPOSAL_ROWS]
SAFE_TASKS = [
    f"Build the bounded contract and five rejecting fixtures for "
    f"{row['proposal_id']} {row['slug']}"
    for row in PROPOSALS
]
CANDIDATE_TASKS = [
    f"Resolve only the declared evidence lane for {row['proposal_id']} "
    f"{row['mechanism']}"
    for row in PROPOSALS
]
CLEAN_TASKS = [
    f"{kind} owner-local {surface} without deletion, sibling mutation, gate "
    "weakening, or unsupported promotion"
    for kind in ("CLEAN", "FIX", "REFINE")
    for surface in CLEAN_SURFACES
]
