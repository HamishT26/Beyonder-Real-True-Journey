#!/usr/bin/env python3
"""Frozen x1 data for Tamar Vey's v656-v1 phase."""

from __future__ import annotations

from ghc_family_v656_v1_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v656-v1"
PHASE_CODE = "V6561"
OWNER = "Tamar Vey"
PRONOUNS = "they/them"
ROLE = "relational evidence-systems cartographer and boundary keeper"
HOPE = (
    "keep decisions legible, failures recoverable, and authority boundaries "
    "intact while new evidence remains challengeable"
)
BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
PHASE_ROOT = "docs/tamar-vey/v656-v1"

SOURCE_OWNER = "Liora Venn"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v655-v8-full-tools"
SOURCE_X1_FREEZE = "25a20a263dd0948df12ec2ef3eb09c5957b0600d"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "64814fc03c5941545dcaa916abd89e954ddbb411"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "5356483f4c4548f7276ede63a086745db5b30037"
PRIOR_FROZEN = 2170
SOURCE_SEALED_REPOSITORY_NEGATIVES = 13591
SOURCE_LIVE_OVERLAY: list[dict] = [
    {
        "negative_id": "V6558-POST-N01",
        "failure": (
            "The exact-final validator's first staged-name hash check included two "
            "declared lifecycle self-exclusions, so the full attempt retained zero "
            "canonical-pass credit."
        ),
        "credit": "zero",
        "recovery": (
            "Rerun only the failed name-hash check over the exact committed 28-entry "
            "domain with the declared self-exclusions; no successful subcheck was replayed."
        ),
    }
]
SOURCE_EFFECTIVE_NEGATIVES = 13592
SOURCE_OPEN_GAPS = 96
SOURCE_EXACT_GATES = 95
SOURCE_METHODS_SEALED = 333
SOURCE_METHODS = 333

PRIMARY_FOCUS = (
    "Freed ID and CBR Heart through bounded synthetic photographic-film custody, "
    "processing provenance, print-access, privacy, remedy, and authority-reservation "
    "contracts, with GMUT Mind and THOS Body visible and protected"
)
BOUNDED_PRACTICE = (
    "synthetic community photographic-darkroom film intake, light-tight loading, "
    "chemical-batch sequence, time-temperature and agitation records, contact-sheet "
    "and print lineage, negative storage, chemical and silver-waste holds, accessible "
    "status, incident preservation, workload control, and shift handover used only as "
    "software, formal, structural, and learning lenses; no real person, subject, "
    "bystander, whānau, photographer, worker, darkroom, film, negative, print, image, "
    "chemical, bath, vessel, enlarger, measurement, exposure, processing, archive, "
    "spill, waste action, disposal decision, professional competence, legal decision, "
    "cultural decision, Māori wording, affected-party acceptance, or Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_people_subjects_bystanders_whanau_photographers_workers_and_affected_parties",
    "real_darkrooms_film_negatives_prints_images_chemicals_vessels_enlargers_and_archives",
    "real_loading_processing_exposure_printing_washing_drying_storage_and_waste_actions",
    "real_sensitometry_densitometry_optical_chemical_environmental_and_workload_measurements",
    "real_spill_exposure_emergency_disposal_silver_recovery_and_safety_decisions",
    "professional_photographic_chemical_archival_conservation_safety_and_waste_authority",
    "production_identity_interoperability_live_keys_proofs_status_resolution_and_revocation",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_content_image_taonga_and_maori_authority",
    "affected_party_acceptance_complaint_return_remedy_and_beneficiary_privacy",
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
            "and the receipt makes no real-person, image, film, chemical, darkroom, "
            "measurement, processing, archival, waste, safety, professional, production, "
            "legal, cultural, authority, effectiveness, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, images, film, "
            "chemicals, equipment, measurements, processing, participants, safety "
            "decisions, professional review, live identity operations, and authority stay absent."
        )
    elif disposition == "open_gap":
        approval = (
            "candidate_real_film_participant_measurement_professional_and_privacy_evidence_required"
        )
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-film, zero-image, zero-chemical, zero-device, "
            "zero-query, zero-download, zero-measurement, zero-processing, and zero-row "
            "refusal receipt and leave empirical, participant, professional, privacy, "
            "accessibility, and authorization gaps open."
        )
    else:
        approval = "exact_affected_party_legal_cultural_image_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved subject, whānau, place, event, taonga-image, tikanga, "
            "disability, privacy, access, return, remedy, governance, legal, cultural, "
            "and authority reservations only; make no tangata-whenua, iwi, hapū, "
            "Māori-authority, competent-authority, or affected-party decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable obligations while "
            "refusing unsupported photographic, chemical, archival, empirical, "
            "professional, identity, legal, cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen "
            "mutation, erases a failure, or exceeds its photographic, chemical, "
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
            "Stop, retain the failed witness at zero credit, rewrite no history, and "
            "leave people, subjects, whānau, images, film, negatives, prints, darkrooms, "
            "chemicals, vessels, equipment, measurements, archives, waste routes, "
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
