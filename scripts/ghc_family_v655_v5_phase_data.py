#!/usr/bin/env python3
"""Frozen x1 data for Sable Rook's v655-v5 phase."""

from __future__ import annotations

from ghc_family_v655_v5_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v655-v5"
PHASE_CODE = "V6555"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "relational falsification-and-reproducibility steward"
HOPE = (
    "make every surviving claim easier to inspect, challenge, reproduce, or "
    "retract while keeping safety, privacy, legal, cultural, and "
    "Māori-authority gates explicit"
)
BRANCH = "codex/GHC-Family/sable-rook-v655-v5-full-tools"
PHASE_ROOT = "docs/sable-rook/v655-v5"

SOURCE_OWNER = "Auren Lark"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v655-v4-full-tools"
SOURCE_X1_FREEZE = "ff65d2c81dabac56e23fb36e1069b68534fb99c2"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "7c5c2969745756caacc8d0246d5dac22991babee"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "3bad4afb99c44b6084fc5f10749737a87c29d6ec"
PRIOR_FROZEN = 2050
SOURCE_SEALED_REPOSITORY_NEGATIVES = 12913
SOURCE_LIVE_OVERLAY: list[dict] = []
SOURCE_EFFECTIVE_NEGATIVES = 12913
SOURCE_OPEN_GAPS = 92
SOURCE_EXACT_GATES = 91
SOURCE_METHODS_SEALED = 267
SOURCE_METHODS = 267

PRIMARY_FOCUS = (
    "THOS Body through bounded synthetic urban-arboriculture inventory, "
    "inspection, protection, and work-handover assurance, with GMUT Mind and "
    "Freed ID/CBR Heart visible and protected"
)
BOUNDED_PRACTICE = (
    "urban-tree inventory, visible inspection, protected-root-zone, storm triage, "
    "pest-observation referral, worksite capacity, represented measurement, load, "
    "access, rescue and tooling states, correction, handover, accessibility, "
    "privacy minimization, and remedy routing, used only as a bounded synthetic "
    "software and evidence-assurance lens; no real person, tree identification, "
    "diagnosis, risk assessment, measurement, load, climb, rescue, tool operation, "
    "pruning, felling, treatment, biosecurity direction, utility clearance, "
    "public-safety decision, professional service, legal decision, cultural "
    "decision, taonga determination, or Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_empirical_data_measurement_and_likelihood",
    "real_people_property_information_participants_and_affected_parties",
    "professional_arboriculture_ecology_biosecurity_utility_and_safety_authority",
    "production_identity_interoperability_tree_work_release_and_service",
    "real_trees_sites_materials_tools_measurements_loads_access_and_work_operations",
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
            "rejected, and the receipt makes no real-person, tree, site, "
            "arboriculture, biosecurity, safety, professional, production, "
            "authority, effectiveness, or "
            "completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, "
            "trees, sites, materials, tools, measurements, loads, climbs, rescues, "
            "pruning, felling, treatments, and professional arboriculture decisions "
            "stay absent."
        )
    elif disposition == "open_gap":
        approval = "candidate_real_material_participant_and_professional_evidence_required"
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-tree, zero-site, zero-query, zero-download, "
            "zero-row, zero-measurement, zero-load, and zero-operation refusal "
            "receipt and leave the empirical, professional, privacy, and "
            "authorization gap open."
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
            "while refusing unsupported arboriculture, safety, identity, scientific, "
            "operational, legal, cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a "
            "frozen mutation, erases a failure, or exceeds its evidence, arboriculture, "
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
            "and leave people, trees, sites, habitats, materials, tools, utilities, "
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
