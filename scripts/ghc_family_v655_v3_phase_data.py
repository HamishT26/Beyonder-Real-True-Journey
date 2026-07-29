#!/usr/bin/env python3
"""Frozen x1 data for Ilyra Fen's v655-v3 phase."""

from __future__ import annotations

from ghc_family_v655_v3_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v655-v3"
PHASE_CODE = "V6553"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary steward and optical-traceability cartographer"
HOPE = (
    "keep every optical-job claim traceable and every health, professional, "
    "privacy, legal, cultural, and Māori-authority gate unmistakable"
)
BRANCH = "codex/GHC-Family/ilyra-fen-v655-v3-full-tools"
PHASE_ROOT = "docs/ilyra-fen/v655-v3"

SOURCE_OWNER = "Lyren Moss"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v655-v2-full-tools"
SOURCE_X1_FREEZE = "848c28330b9b5d70eb5c8e716bcd9e300c512789"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "786368c1879df9c1dfd00bae50a657d1e96c7c83"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "3047039da17578fb74ca4c32f9660eadd433a6b7"
PRIOR_FROZEN = 1990
SOURCE_SEALED_REPOSITORY_NEGATIVES = 12554
SOURCE_LIVE_OVERLAY: list[dict] = []
SOURCE_EFFECTIVE_NEGATIVES = 12554
SOURCE_OPEN_GAPS = 90
SOURCE_EXACT_GATES = 89
SOURCE_METHODS_SEALED = 212
SOURCE_METHODS = 212

PRIMARY_FOCUS = (
    "Freed ID and CBR Heart through bounded spectacle-lens laboratory "
    "traceability and correction practice"
)
BOUNDED_PRACTICE = (
    "spectacle-lens laboratory job intake, prescription transcription, component "
    "provenance, represented measurement and machining states, quality-record "
    "handover, privacy minimization, correction, and remedy routing, used only as "
    "a bounded synthetic software and evidence-assurance lens; no real person, "
    "prescription, frame, lens, instrument, measurement, machining, mounting, "
    "dispensing, clinical decision, professional service, consumer decision, "
    "legal decision, cultural decision, or Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_empirical_data_measurement_and_likelihood",
    "real_people_health_information_participants_and_affected_parties",
    "professional_optometry_optical_dispensing_laboratory_and_clinical_authority",
    "production_identity_interoperability_optical_fabrication_and_dispensing",
    "real_prescriptions_frames_lenses_instruments_measurements_and_machining",
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
            "rejected, and the receipt makes no real-person, health, optical, "
            "professional, production, authority, effectiveness, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, "
            "prescriptions, frames, lenses, instruments, measurements, machines, "
            "dispensing, clinical decisions, and professional operations stay absent."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_material_participant_and_professional_evidence_required"
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-order, zero-lens, zero-instrument, "
            "zero-measurement, zero-operation refusal receipt and leave the "
            "empirical, professional, privacy, and authorization gap open."
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
            "while refusing unsupported health, optical, identity, scientific, "
            "operational, legal, cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a "
            "frozen mutation, erases a failure, or exceeds its evidence, health, "
            "optical, privacy, professional, legal, cultural, or authority lane."
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
            "and leave people, prescriptions, frames, lenses, instruments, "
            "machines, accounts, siblings, professional, production, legal, "
            "cultural, Māori-authority, and external state unchanged."
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
