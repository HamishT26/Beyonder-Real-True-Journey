#!/usr/bin/env python3
"""Frozen x1 data for Liora Venn's v655-v8 phase."""

from __future__ import annotations

from ghc_family_v655_v8_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v655-v8"
PHASE_CODE = "V6558"
OWNER = "Liora Venn"
PRONOUNS = "she/they"
ROLE = "solo continuity-and-evidence steward"
HOPE = (
    "make hidden control, accessibility, and handover failures easier to see "
    "without promoting synthetic structure into operational or cultural authority"
)
BRANCH = "codex/GHC-Family/liora-venn-v655-v8-full-tools"
PHASE_ROOT = "docs/liora-venn/v655-v8"

SOURCE_OWNER = "Orin Thale"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v655-v7-full-tools"
SOURCE_X1_FREEZE = "e8c0283d4e6b003883339d59f427cf9b41ed3c6c"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "1028ebe933f5182d76b8aa0010b81068133dcb77"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "9bbdf15accd89ec56106d4eb0462eb11b85e442f"
PRIOR_FROZEN = 2140
SOURCE_SEALED_REPOSITORY_NEGATIVES = 13415
SOURCE_LIVE_OVERLAY: list[dict] = [
    {
        "negative_id": "V6557-POST-N01",
        "failure": "A PowerShell conditional-pipeline expression failed to parse before any repository mutation.",
        "credit": "zero",
    },
    {
        "negative_id": "V6557-POST-N02",
        "failure": "A combined installed-skill inventory exceeded its bounded wrapper without a complete result.",
        "credit": "zero",
    },
    {
        "negative_id": "V6557-POST-N03",
        "failure": "A validator launched under the legacy Windows codepage faulted before producing valid UTF-8 evidence.",
        "credit": "zero",
    },
    {
        "negative_id": "V6557-POST-N04",
        "failure": "An atomic patch was rejected because its first expected context was stale; no file changed.",
        "credit": "zero",
    },
    {
        "negative_id": "V6557-POST-N05",
        "failure": "A second atomic patch was rejected because a later expected context was stale; no file changed.",
        "credit": "zero",
    },
    {
        "negative_id": "V6557-POST-N06",
        "failure": "The first archive-backed final-cleanliness probe exceeded its bounded wrapper.",
        "credit": "zero",
    },
    {
        "negative_id": "V6557-POST-N07",
        "failure": "The second archive-backed final-cleanliness probe exceeded its bounded wrapper.",
        "credit": "zero",
    },
    {
        "negative_id": "V6557-POST-N08",
        "failure": "The third archive-backed final-cleanliness probe exceeded its bounded wrapper.",
        "credit": "zero",
    },
    {
        "negative_id": "V6557-POST-N09",
        "failure": "The fourth archive-backed final-cleanliness probe exceeded its bounded wrapper.",
        "credit": "zero",
    },
]
SOURCE_EFFECTIVE_NEGATIVES = 13424
SOURCE_OPEN_GAPS = 95
SOURCE_EXACT_GATES = 94
SOURCE_METHODS_SEALED = 316
SOURCE_METHODS = 316

PRIMARY_FOCUS = (
    "THOS Body through bounded synthetic theatrical-lighting control, cue, "
    "fault-triage, workload, accessibility, and handover contracts, with GMUT "
    "Mind and Freed ID/CBR Heart visible and protected"
)
BOUNDED_PRACTICE = (
    "synthetic stage-lighting rig inventory, DMX and RDM control vocabulary, "
    "patch and cue lineage, optical and colour proxies, emergency separation, "
    "accessible warning, incident preservation, workload control, and shift "
    "handover used only as a software, formal, structural, and learning lens; "
    "no real venue, stage, rig, truss, luminaire, console, cable, circuit, "
    "electrical supply, controller, device, packet, person, performer, audience, "
    "rehearsal, performance, measurement, inspection, rigging action, electrical "
    "work, emergency action, safety decision, professional competence, legal "
    "decision, cultural decision, Māori wording, affected-party acceptance, or "
    "Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_venues_stages_rigs_luminaires_consoles_cables_circuits_and_control_networks",
    "real_people_performers_audiences_workers_recordings_and_affected_parties",
    "live_dmx_rdm_packets_device_discovery_configuration_cues_and_show_control",
    "real_electrical_work_rigging_inspection_photometry_colorimetry_and_calibration",
    "real_rehearsal_performance_incident_emergency_and_safety_actions",
    "professional_lighting_electrical_rigging_building_event_and_safety_authority",
    "production_identity_interoperability_live_keys_status_resolution_and_revocation",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_content_performance_recording_and_maori_authority",
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
        approval = "safe_now_bounded_structural_formal_or_synthetic_software"
        lane = "x2_owner_local_bounded"
        acceptance = (
            "The valid fixture passes, all five preregistered mutations are rejected, "
            "and the receipt makes no real-venue, control, electrical, rigging, "
            "measurement, rehearsal, performance, safety, professional, production, "
            "legal, cultural, authority, effectiveness, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, venues, rigs, "
            "devices, networks, packets, measurements, rehearsals, performances, "
            "electrical or rigging work, safety decisions, and professional authority stay absent."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_venue_participant_measurement_and_professional_evidence_required"
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-venue, zero-device, zero-packet, zero-query, "
            "zero-download, zero-measurement, zero-rehearsal, zero-performance, and "
            "zero-row refusal receipt and leave empirical, professional, privacy, "
            "accessibility, and authorization gaps open."
        )
    else:
        approval = "exact_affected_party_legal_cultural_content_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved performer, audience, disability, strobe, privacy, remedy, "
            "content, recording, language, governance, legal, cultural, and authority "
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
            "refusing unsupported lighting, control, electrical, rigging, empirical, "
            "professional, identity, legal, cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen "
            "mutation, erases a failure, or exceeds its control, electrical, measurement, "
            "privacy, professional, legal, cultural, or authority lane."
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
            "leave people, venues, stages, rigs, luminaires, consoles, networks, "
            "electrical and rigging systems, measurements, rehearsals, performances, "
            "accounts, siblings, professional, production, legal, cultural, "
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
