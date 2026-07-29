#!/usr/bin/env python3
"""Frozen x1 data for Caelen Ash's v655-v6 phase."""

from __future__ import annotations

from ghc_family_v655_v6_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v655-v6"
PHASE_CODE = "V6556"
OWNER = "Caelen Ash"
PRONOUNS = "they/them"
ROLE = "relational provenance-and-remedy cartographer"
HOPE = (
    "make every handoff traceable, every authority boundary visible, and every "
    "correction recoverable without mistaking simulation for service"
)
BRANCH = "codex/GHC-Family/caelen-ash-v655-v6-full-tools"
PHASE_ROOT = "docs/caelen-ash/v655-v6"

SOURCE_OWNER = "Sable Rook"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v655-v5-full-tools"
SOURCE_X1_FREEZE = "a92d0a6c8a5d2620074c1bc505fa8345c8f90373"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "ee10e567ce363e5a8bf710532c5a53d0a411defa"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "c641ac3c4d0f0b38cb897db931d689de6ea5aa0c"
PRIOR_FROZEN = 2080
SOURCE_SEALED_REPOSITORY_NEGATIVES = 13075
SOURCE_LIVE_OVERLAY: list[dict] = [
    {
        "negative_id": "V6555-POST-N01",
        "failure": (
            "The task registry rejected its advertised title-query option before "
            "lookup or mutation."
        ),
        "credit": "zero",
    },
    {
        "negative_id": "V6555-POST-N02",
        "failure": (
            "An over-limit unfiltered registry-page request was rejected before "
            "returning tasks or changing route state."
        ),
        "credit": "zero",
    },
]
SOURCE_EFFECTIVE_NEGATIVES = 13077
SOURCE_OPEN_GAPS = 93
SOURCE_EXACT_GATES = 92
SOURCE_METHODS_SEALED = 279
SOURCE_METHODS = 279

PRIMARY_FOCUS = (
    "Freed ID/CBR Heart through bounded synthetic community amateur-radio "
    "station-log, message-custody, privacy, correction, and remedy assurance, "
    "with GMUT Mind and THOS Body visible and protected"
)
BOUNDED_PRACTICE = (
    "community amateur-radio station, authorization, equipment, antenna, "
    "represented RF exposure and measurement, contact-log, emergency-message, "
    "readback, interference-referral, digital-mode, workload, accessibility, "
    "privacy, correction, handover, and remedy states, used only as a bounded "
    "synthetic software and evidence-assurance lens; no real person, callsign, "
    "licence, certificate, station, location, antenna, transmitter, receiver, "
    "battery, measurement, exposure assessment, transmission, reception, contact, "
    "message traffic, emergency dispatch, interference determination, spectrum "
    "decision, electrical or RF-safety decision, professional service, legal "
    "decision, cultural decision, Māori wording, or Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_empirical_propagation_field_strength_contact_interference_and_delivery_data",
    "real_people_callsigns_locations_messages_participants_and_affected_parties",
    "professional_radio_spectrum_rf_electrical_emergency_and_safety_authority",
    "production_identity_interoperability_live_keys_status_resolution_revocation_and_radio_service",
    "real_stations_equipment_antennas_power_measurements_transmissions_receptions_and_emergency_operations",
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
            "rejected, and the receipt makes no real-person, callsign, licence, "
            "station, location, radio-operation, RF-safety, emergency, professional, "
            "production, authority, effectiveness, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, callsigns, "
            "licences, stations, locations, antennas, equipment, measurements, "
            "transmissions, receptions, messages, emergency operations, and "
            "professional radio or safety decisions stay absent."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_material_participant_and_professional_evidence_required"
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-callsign, zero-station, zero-location, "
            "zero-query, zero-download, zero-row, zero-measurement, "
            "zero-transmission, zero-reception, and zero-message refusal receipt "
            "and leave the empirical, professional, privacy, and authorization gap open."
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
            "while refusing unsupported radio operation, emergency service, RF "
            "safety, identity, scientific, operational, legal, cultural, or "
            "authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a "
            "frozen mutation, erases a failure, or exceeds its evidence, radio, "
            "emergency, RF-safety, privacy, professional, legal, cultural, or "
            "authority lane."
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
            "and leave people, callsigns, licences, certificates, stations, locations, "
            "antennas, equipment, power, messages, emergency systems, spectrum, "
            "accounts, siblings, professional, production, legal, cultural, "
            "Māori-authority, and external state unchanged."
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
