#!/usr/bin/env python3
"""Frozen x1 data for Elowen Cairn's v656-v2 phase."""

from __future__ import annotations

from ghc_family_v656_v2_phase_catalogue import (
    CLEAN_SURFACES,
    OFFICIAL_SOURCES,
    PROPOSAL_ROWS,
    RUNNER_IDEAS,
    SKILL_IDEAS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v656-v2"
PHASE_CODE = "V6562"
OWNER = "Elowen Cairn"
PRONOUNS = "they/them"
ROLE = "relational boundary cartographer and evidence steward"
HOPE = "make every transition recoverable and every claim proportionate to proof"
BRANCH = "codex/GHC-Family/elowen-cairn-v656-v2-full-tools"
PHASE_ROOT = "docs/elowen-cairn/v656-v2"

SOURCE_OWNER = "Tamar Vey"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_X1_FREEZE = "ed877dc0be03fdd82318ba218926f517f30779ae"
SOURCE_X1_FINAL = SOURCE_X1_FREEZE
SOURCE_EVIDENCE = "995ce2973d72debdf7f3d7fca42f4f0afae2b6bb"
SOURCE_EVIDENCE_CORRECTION = None
SOURCE_FINAL = "19cc5abb533f7ad402e8e3a70f2bfb667b0be558"
PRIOR_FROZEN = 2200
SOURCE_SEALED_REPOSITORY_NEGATIVES = 13792
SOURCE_LIVE_OVERLAY = [
    {
        "negative_id": f"V6561-ROUTE-N{index:02d}",
        "failure": failure,
        "credit": "zero",
        "recovery": recovery,
    }
    for index, (failure, recovery) in enumerate(
        [
            (
                "An obsolete schema-name assumption was rejected.",
                "Resolve the current schema from the selected skill before validation.",
            ),
            (
                "A second obsolete schema-name assumption was rejected.",
                "Use the current declared schema identifier without legacy projection.",
            ),
            (
                "A direct PowerShell foreach-pipeline parser form failed.",
                "Materialize loop output before applying a pipeline.",
            ),
            (
                "A second direct PowerShell foreach-pipeline parser form failed.",
                "Use a conventionally spaced scalar loop and downstream pipeline.",
            ),
            (
                "An overbroad receipt search exceeded its useful evidence scope.",
                "Resolve the exact receipt name and read that literal path.",
            ),
            (
                "A second overbroad receipt search exceeded its useful evidence scope.",
                "Use bounded local filtering over the exact receipt directory.",
            ),
            (
                "The phase-locked authorization baton renderer failed compatibility review before execution.",
                "Keep it unexecuted until it is genuinely phase-neutral, tested, and validated.",
            ),
            (
                "An invalid workflow-plan policy literal was rejected.",
                "Use only the current schema's declared policy literals.",
            ),
            (
                "An overbroad privacy-runner search returned no attributable evidence.",
                "Select the current family privacy runner from the committed index.",
            ),
            (
                "A legacy --help invocation executed and rewrote two tracked receipts.",
                "Restore the exact prior bytes and inspect caller semantics before help probes.",
            ),
            (
                "A diff-hygiene probe timed out.",
                "Split name-status, whitespace, and status probes and retain the timeout.",
            ),
            (
                "An index-stat refresh returned needs-update despite exact clean-filter equality.",
                "Use the exact clean filter as truth and retain the advisory mismatch.",
            ),
            (
                "A patch-context assumption was atomically rejected.",
                "Reread the exact context and apply a bounded replacement.",
            ),
        ],
        1,
    )
]
SOURCE_EFFECTIVE_NEGATIVES = 13805
SOURCE_OPEN_GAPS = 97
SOURCE_EXACT_GATES = 96
SOURCE_METHODS_SEALED = 383
SOURCE_ROUTE_METHODS = 9
SOURCE_METHODS = 392
SOURCE_ROUTE_METHOD_ROWS = [
    (
        "current_schema_resolution",
        "Two obsolete schema-name assumptions were rejected.",
        "Read the selected current skill schema and use its declared identifier.",
        "Never project a legacy schema name into a current validator.",
        ["V6561-ROUTE-N01", "V6561-ROUTE-N02"],
    ),
    (
        "powershell_foreach_materialization",
        "Two direct foreach-pipeline forms failed at parse time.",
        "Materialize a conventionally spaced foreach loop before applying a pipeline.",
        "Do not attach a pipeline to an unparenthesized foreach statement.",
        ["V6561-ROUTE-N03", "V6561-ROUTE-N04"],
    ),
    (
        "exact_receipt_resolution",
        "Two overbroad receipt searches exceeded their useful evidence scope.",
        "Resolve the exact receipt directory and filter locally by the literal expected name.",
        "Do not recursively search the repository for a known receipt class.",
        ["V6561-ROUTE-N05", "V6561-ROUTE-N06"],
    ),
    (
        "phase_neutral_baton_renderer_gate",
        "The phase-locked authorization baton renderer failed compatibility review before execution.",
        "Leave it unexecuted until a phase-neutral implementation is tested and validated.",
        "Inspect renderer phase and schema contracts before any invocation.",
        ["V6561-ROUTE-N07"],
    ),
    (
        "workflow_policy_enum_validation",
        "An invalid workflow-plan policy literal was rejected.",
        "Use only current schema-declared workflow policy literals.",
        "Validate policy enums before building the committed request.",
        ["V6561-ROUTE-N08"],
    ),
    (
        "bounded_privacy_runner_selection",
        "An overbroad privacy-runner search returned no attributable evidence.",
        "Select the current family privacy runner from the committed index.",
        "Resolve current callers before scanning for stale owner/version surfaces.",
        ["V6561-ROUTE-N09"],
    ),
    (
        "side_effect_aware_cli_introspection",
        "A legacy --help invocation executed and rewrote two tracked receipts.",
        "Restore the exact prior bytes and inspect source semantics before help probes.",
        "Do not assume --help is side-effect free for legacy repository runners.",
        ["V6561-ROUTE-N10"],
    ),
    (
        "split_diff_and_index_hygiene",
        "A diff-hygiene timeout and an index-stat advisory mismatch returned no aggregate credit.",
        "Split name-status, whitespace, status, and exact clean-filter checks.",
        "Treat index-stat refresh as advisory when the exact clean filter is equal.",
        ["V6561-ROUTE-N11", "V6561-ROUTE-N12"],
    ),
    (
        "atomic_patch_context_recovery",
        "A patch-context assumption was atomically rejected.",
        "Reread exact context and apply one bounded replacement.",
        "Never widen a rejected patch without an exact context reread.",
        ["V6561-ROUTE-N13"],
    ),
]

PRIMARY_FOCUS = (
    "GMUT Mind through bounded typed anisotropic sail-membrane, seam-interface, "
    "corner-refinement, pattern-topology, unit, provenance, and falsification contracts, "
    "with THOS Body and Freed ID/CBR Heart visible and protected"
)
BOUNDED_PRACTICE = (
    "synthetic sailmaker loft intake, presented measurement, coordinate-frame, panel "
    "topology, cloth orientation, seam, reinforcement, reef, batten-pocket, attachment, "
    "cut-plan, material-lot, repair, condition, equipment-state, workload, custody, "
    "accessibility, privacy, remedy, and shift-handover records used only as software, "
    "formal, structural, and learning lenses; no real person, worker, owner, designer, "
    "maker, repairer, vessel, voyage, sail, sailcloth, hardware, machine, tool, loft, "
    "measurement, inspection, test, cut, stitch, repair, installation, load, sea trial, "
    "professional competence, safety decision, legal decision, cultural decision, Māori "
    "wording, affected-party acceptance, or Māori authority"
)
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "real_people_workers_owners_designers_makers_repairers_sailors_and_affected_parties",
    "real_vessels_voyages_sails_sailcloth_hardware_machines_tools_lofts_and_workplaces",
    "real_measurement_inspection_testing_cutting_stitching_repair_installation_and_sea_trials",
    "real_load_strength_stability_serviceability_weather_and_performance_determinations",
    "real_guarding_isolation_lockout_stop_work_emergency_and_safety_decisions",
    "professional_sailmaking_textile_marine_engineering_inspection_safety_and_class_authority",
    "production_identity_interoperability_live_keys_proofs_status_resolution_and_revocation",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_design_knowledge_collective_interest_and_maori_authority",
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
            "and the receipt makes no real-person, sail, vessel, loft, machine, material, "
            "measurement, load, safety, professional, production, legal, cultural, "
            "authority, effectiveness, or completeness claim."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_representation_only"
        acceptance = (
            "The protocol and mutation evidence pass while real people, sails, vessels, "
            "materials, machines, measurements, tests, loads, participants, sea trials, "
            "safety decisions, professional review, identity operations, and authority stay absent."
        )
    elif disposition == "open_gap":
        approval = (
            "candidate_real_sail_textile_measurement_participant_professional_and_privacy_evidence_required"
        )
        lane = "x2_zero_live_action_readiness_only"
        acceptance = (
            "Emit a zero-person, zero-sail, zero-vessel, zero-material, zero-machine, "
            "zero-query, zero-download, zero-measurement, zero-test, zero-trial, and zero-row "
            "refusal receipt and leave empirical, participant, professional, privacy, "
            "accessibility, safety, and authorization gaps open."
        )
    else:
        approval = "exact_affected_party_legal_cultural_design_knowledge_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        acceptance = (
            "Emit unresolved person, whānau, vessel, voyage, place, design-knowledge, "
            "collective-interest, tikanga, disability, privacy, access, return, remedy, "
            "governance, legal, cultural, and authority reservations only; make no tangata-"
            "whenua, iwi, hapū, Māori-authority, competent-authority, or affected-party decision."
        )
    return {
        "proposal_id": f"{PHASE_CODE}-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mechanism": mechanism,
        "hypothesis": (
            f"A bounded {mechanism} contract can expose falsifiable obligations while "
            "refusing unsupported sailmaking, textile, marine, measurement, load, safety, "
            "professional, identity, legal, cultural, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a required {mechanism} obligation, accepts a frozen mutation, "
            "erases a failure, or exceeds its sailmaking, textile, measurement, safety, "
            "professional, legal, cultural, or authority lane."
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
            "people, whānau, workers, vessels, voyages, sails, cloth, hardware, machines, "
            "tools, lofts, measurements, tests, cuts, stitches, repairs, installations, "
            "loads, sea trials, accounts, siblings, professional, production, legal, "
            "cultural, Māori-authority, and external state unchanged."
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
