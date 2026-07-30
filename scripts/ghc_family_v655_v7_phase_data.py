#!/usr/bin/env python3
"""Frozen x1 data for Orin Thale's v655-v7 phase."""

from __future__ import annotations

from ghc_family_v655_v7_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v655-v7"
PHASE_CODE = "V6557"
OWNER = "Orin Thale"
PRONOUNS = "they/them"
ROLE = "relational boundary-and-method steward"
HOPE = (
    "keep every surviving claim traceable, falsifiable, and retractable within "
    "its actual evidence class"
)
BRANCH = "codex/GHC-Family/orin-thale-v655-v7-full-tools"
PHASE_ROOT = "docs/orin-thale/v655-v7"

SOURCE_OWNER = "Caelen Ash"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v655-v6-full-tools"
SOURCE_X1_FREEZE = "0d1b9b0542235cc8d11c7f73cd394852b4382960"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "d732e94bfedad2c2c6df49096add5ea1d0de2280"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "2e4d87db052aa2788a4436ce59d427ba40bae442"
PRIOR_FROZEN = 2110
SOURCE_SEALED_REPOSITORY_NEGATIVES = 13238
SOURCE_LIVE_OVERLAY: list[dict] = [
    {
        "negative_id": "V6556-POST-N01",
        "failure": (
            "The first direct task reread exceeded the endpoint's accepted turn "
            "window and was rejected before returning content or changing route state."
        ),
        "credit": "zero",
    }
]
SOURCE_EFFECTIVE_NEGATIVES = 13239
SOURCE_OPEN_GAPS = 94
SOURCE_EXACT_GATES = 93
SOURCE_METHODS_SEALED = 290
SOURCE_METHODS = 290

PRIMARY_FOCUS = (
    "GMUT Mind through bounded typed geomechanics, evidence firewalls, and "
    "zero-row empirical refusal, with THOS Body and Freed ID/CBR Heart visible "
    "and protected"
)
BOUNDED_PRACTICE = (
    "synthetic geotechnical borehole logging, sample custody, piezometer and "
    "inclinometer monitoring, hazard holds, accessible notice, correction "
    "readback, workload control, and shift handover used only as a software, "
    "formal, structural, and learning lens; no real site, land parcel, person, "
    "borehole, sample, instrument, measurement, investigation, laboratory test, "
    "hazard assessment, engineering interpretation, design, consent, safety "
    "decision, professional competence, legal decision, cultural decision, "
    "Māori wording, affected-party acceptance, or Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_geotechnical_field_laboratory_monitoring_and_hazard_data",
    "real_people_land_parcels_sites_samples_instruments_and_affected_parties",
    "professional_geotechnical_geological_laboratory_design_consent_and_safety_authority",
    "production_identity_interoperability_live_keys_status_resolution_and_revocation",
    "real_fieldwork_drilling_sampling_installation_monitoring_testing_and_remediation",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_land_heritage_and_maori_authority",
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
            "The valid fixture passes, all five preregistered mutations are "
            "rejected, and the receipt makes no real-site, fieldwork, measurement, "
            "professional, production, legal, cultural, authority, effectiveness, "
            "or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, sites, "
            "boreholes, samples, instruments, fieldwork, laboratory work, hazards, "
            "engineering decisions, and professional authority stay absent."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_material_data_and_professional_evidence_required"
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-site, zero-query, zero-download, zero-row, "
            "zero-sample, zero-instrument, zero-measurement, zero-analysis, and "
            "zero-design refusal receipt and leave every empirical, professional, "
            "privacy, and authorization gap open."
        )
    else:
        approval = "exact_affected_party_legal_cultural_land_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved land, access, disability, privacy, remedy, heritage, "
            "language, governance, legal, cultural, and authority reservations "
            "only; make no tangata-whenua, iwi, hapū, Māori-authority, competent-"
            "authority, or affected-party decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable obligations "
            "while refusing unsupported geotechnical, scientific, operational, "
            "professional, identity, legal, cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a "
            "frozen mutation, erases a failure, or exceeds its evidence, fieldwork, "
            "measurement, privacy, professional, legal, cultural, or authority lane."
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
            "and leave people, land, sites, boreholes, samples, instruments, "
            "fieldwork, measurements, laboratories, hazards, designs, consents, "
            "accounts, siblings, professional, production, legal, cultural, Māori-"
            "authority, and external state unchanged."
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
