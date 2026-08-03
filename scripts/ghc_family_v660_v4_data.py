#!/usr/bin/env python3
"""Frozen x1 planning data for Neris Solane v660-v4.

Elaren Kestrel's immutable v660-v3 surface supplies compatibility vocabulary
only. Twenty inherited rows are selected for bounded revalidation with zero
Neris novelty or completion credit. Only the twenty new rows below extend the
append-only proposal chain. Every domain fixture is synthetic and zero-row.
"""

from __future__ import annotations

from ghc_family_v660_v3_data import *  # noqa: F401,F403


PHASE = "v660-v4"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6604"
OWNER = "Neris Solane"
PRONOUNS = "they/them"
ROLE = "relational volcanic-observatory provenance steward"
HOPE = (
    "make synthetic archive obligations auditable without converting software "
    "structure into scientific, operational, legal, cultural, or Māori authority"
)
BRANCH = "codex/GHC-Family/neris-solane-v660-v4-full-tools"
PHASE_ROOT = "docs/neris-solane/v660-v4"

SOURCE_OWNER = "Elaren Kestrel"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v660-v3-full-tools"
SOURCE_BASE = "6608caa62705bffd485e734e9b6a576c99b2862e"
SOURCE_X1 = "759c285c49ed95175437f0dd08aff403cfb38618"
SOURCE_EVIDENCE = "8dc2da4c781343f5ad16264b166fbf04bdd0e1e1"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "425fd1e4a0a96b285064c66d736b77a23f58bfb0"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_FAILED_AGGREGATE_WITNESS_SHA256 = (
    "20fddbd0e2f746fe12fc7b88f54972bd25aa6d986d1ddd6fbe9e7272099829f4"
)
SOURCE_COMPOSITE_RECEIPT_SHA256 = (
    "96379b33cfc684474ae2b2358294fcb5e5252d4ae6544e4612a1d41f5f26c79f"
)
SOURCE_ROUTE_RECEIPT_SHA256 = (
    "b77258fa81dafc7d9d157cd548a6dda26f35b998c7e81433e3002c6a10976756"
)
ACTIVATION_PACKET_SHA256 = (
    "3e9822ca5349971b699cc30fb5db91fe32702bc97ed21345ed44c239658fb162"
)
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3190
SOURCE_SEALED_NEGATIVES = 20185
SOURCE_EXTERNAL_NEGATIVES = 3
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = ACTIVATION_NEGATIVES
SOURCE_OPEN_GAPS = 132
SOURCE_EXACT_GATES = 131
SOURCE_SEALED_METHODS = 6219
SOURCE_EXTERNAL_METHODS = 3
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = ACTIVATION_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic ice-core curation and proxy-provenance records, section "
    "topology, cold-chain and measurement obligations, chronology abstention, "
    "sensitive-location protection, accessibility, and handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_ice_firn_cores_sections_chips_meltwater_gases_dust_tephra_reagents_archives_locations_measurements_chronologies_or_climate_records",
    "real_drillers_researchers_curators_technicians_investigators_communities_indigenous_rights_holders_affected_parties_and_authorities",
    "real_drilling_recovery_transport_storage_racking_cutting_sampling_melting_analysis_allocation_publication_transfer_or_deaccession",
    "professional_glaciology_paleoclimatology_geochronology_curation_laboratory_cold_chain_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "sensitive_location_indigenous_or_traditional_knowledge_bioprospecting_and_benefit_sharing",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_naming_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_takedown_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6603-P{i:03d}" for i in range(1, 21)]


def _proposal(
    slug: str,
    title: str,
    outcome: str,
    pillar: str,
    mechanism: str,
    sources: list[str],
) -> dict[str, object]:
    return {
        "slug": slug,
        "title": title,
        "outcome": outcome,
        "pillar": pillar,
        "mechanism": mechanism,
        "sources": sources,
    }


NEW_PROPOSAL_SPECS = [
    _proposal(
        "ice-core-section-intake-passport",
        "Synthetic ice-core section intake passport linking surrogate core, run, tube, box, rack, custody event, quarantine cause, and accession refusal",
        "completed",
        "Freed ID and CBR Heart",
        "surrogate section and container identifiers, custody lineage, quarantine causes, corrections, inventory tombstones, and accession refusal",
        ["NSF-ICF-ABOUT", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "ice-core-depth-orientation-graph",
        "Directed ice-core depth and cut-face orientation graph with top-bottom claims, azimuth placeholders, discontinuities, uncertain edges, and orientation abstention",
        "completed",
        "GMUT Mind and CBR Heart",
        "typed surrogate depth nodes, top-bottom and cut-face edges, discontinuity flags, uncertainty, contradiction retention, and orientation abstention",
        ["NOAA-ICE-CORE", "NSF-ICF-ABOUT", "W3C-PROV"],
    ),
    _proposal(
        "ice-core-continuity-hiatus-ledger",
        "Ice-core piece continuity and hiatus ledger separating recovered, missing, fractured, rejoined, duplicated, unknown, and no-stratigraphic-conclusion states",
        "completed",
        "GMUT Mind and CBR Heart",
        "surrogate piece adjacency, gap classes, fracture and rejoin assertions, contradictions, correction lineage, and stratigraphic abstention",
        ["NSF-ICF-ABOUT", "W3C-PROV", "LOC-PREMIS-3"],
    ),
    _proposal(
        "ice-core-cold-chain-envelope",
        "Synthetic ice-core cold-chain envelope with logger identity placeholder, custody interval, excursion flag, missingness, digest, and zero temperature observations",
        "completed",
        "THOS Body and Freed ID",
        "surrogate shipment and logger identities, custody intervals, declared excursion states, missingness, digests, zero temperatures, and transport fitness refusal",
        ["NSF-ICF-POLICY", "NIST-UNCERTAINTY", "W3C-PROV"],
    ),
    _proposal(
        "ice-core-conductivity-uncertainty-budget",
        "Ice-core electrical-conductivity and dielectric-profile uncertainty budget with instrument-response placeholders, covariance, units, and zero measurements",
        "completed",
        "GMUT Mind",
        "typed quantity, unit, instrument response, calibration placeholder, covariance, missingness, zero-row measurement, and inference firewall obligations",
        ["NIST-SI", "NIST-UNCERTAINTY", "CF-1.13"],
    ),
    _proposal(
        "ice-core-visual-stratigraphy-annotation",
        "Layer-aware ice-core visual-stratigraphy annotation graph with bubble, dust, melt-feature, fracture, ambiguity, contradiction, and zero-image states",
        "completed",
        "GMUT Mind and CBR Heart",
        "surrogate layer assertions, annotation targets, ambiguity, contradiction, scale placeholders, zero images, and interpretation abstention",
        ["NOAA-ICE-CORE", "W3C-ANNOTATION", "W3C-PROV"],
    ),
    _proposal(
        "ice-core-sample-allocation-firewall",
        "Ice-core sample-allocation and destructive-use firewall with request scope, volume placeholder, priority conflict, return condition, and zero physical allocation",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic request and allocation declarations, destructive-use budget, authority holds, conflict retention, zero samples, and execution refusal",
        ["NSF-ICF-POLICY", "NSF-ICF-SERVICES", "W3C-PROV"],
    ),
    _proposal(
        "ice-core-melt-aliquot-lineage",
        "Nonproduction ice-core melt and aliquot lineage with parent section, split sequence, blank and contamination-control declarations, zero material, and laboratory refusal",
        "completed",
        "Freed ID and CBR Heart",
        "surrogate parent and aliquot links, split events, blank and contamination-control declarations, zero material, correction retention, and laboratory abstention",
        ["NSF-ICF-SERVICES", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "ice-core-age-depth-assertion-braid",
        "Ice-core age-depth assertion braid linking model version, tie-point placeholder, uncertainty, supersession, contradiction, and no accepted chronology",
        "completed",
        "GMUT Mind and Freed ID",
        "surrogate depth and age assertions, model-version provenance, tie-point placeholders, uncertainty, contradiction, supersession, and chronology abstention",
        ["NOAA-ICE-CORE", "CF-1.13", "W3C-PROV"],
    ),
    _proposal(
        "ice-core-stable-isotope-envelope",
        "Stable-isotope proxy metadata envelope with analyte name, reference-scale placeholder, unit, uncertainty, missingness, zero values, and climate-inference refusal",
        "completed",
        "GMUT Mind",
        "typed analyte, reference-scale and unit placeholders, uncertainty, covariance, missingness, zero values, and no climate inference",
        ["NOAA-ICE-CORE", "CF-1.13", "NIST-UNCERTAINTY"],
    ),
    _proposal(
        "ice-core-gas-age-offset-register",
        "Ice-core gas-depth and ice-age offset register with enclosure-depth placeholder, model dependency, uncertainty, contradiction, and zero gas observations",
        "completed",
        "GMUT Mind and Freed ID",
        "surrogate gas and ice depth relations, enclosure and offset placeholders, model lineage, uncertainty, contradiction, zero observations, and age abstention",
        ["NOAA-ICE-CORE", "NIST-UNCERTAINTY", "W3C-PROV"],
    ),
    _proposal(
        "ice-core-tephra-horizon-escrow",
        "Ice-core tephra-horizon assertion escrow with depth interval, morphology placeholder, comparison source, confidence, conflict, and no eruption attribution",
        "completed",
        "GMUT Mind and CBR Heart",
        "surrogate horizon assertions, depth intervals, morphology and comparison placeholders, confidence, conflicts, correction lineage, and attribution refusal",
        ["NOAA-ICE-CORE", "W3C-PROV", "NIST-UNCERTAINTY"],
    ),
    _proposal(
        "ice-core-scan-capture-covenant",
        "Ice-core scan and photography capture covenant with face declaration, scale placeholder, illumination, derivative lineage, disclosure mask, and zero authenticated images",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic capture-face and geometry declarations, scale and illumination placeholders, derivative lineage, disclosure masks, zero authenticated images, and comparison hold",
        ["W3C-ANNOTATION", "LOC-PREMIS-3", "NIST-SI"],
    ),
    _proposal(
        "ice-core-archive-tombstone-ledger",
        "Ice-core archive split, reserve, exhaustion, deaccession, and tombstone ledger retaining effective intervals, reasons, contradictions, and no disposal authority",
        "completed",
        "Freed ID and CBR Heart",
        "surrogate inventory states, split and reserve relations, effective intervals, contradictions, correction lineage, tombstones, and disposal refusal",
        ["NSF-ICF-POLICY", "LOC-PREMIS-3", "W3C-PROV"],
    ),
    _proposal(
        "gmut-ice-core-transport-proxy",
        "Represented GMUT ice-core coupled heat, gas, impurity, strain, and depth-coordinate proxy with units, covariance, zero coefficients, and likelihood firewall",
        "represented",
        "GMUT Mind",
        "typed symbolic thermal, gas, impurity, strain, and depth-coordinate roles, boundary data, units, covariance, zero coefficients, zero likelihood rows, and empirical abstention",
        ["NIST-SI", "NIST-UNCERTAINTY", "CF-1.13"],
    ),
    _proposal(
        "thos-ice-core-archive-backlog",
        "Represented THOS ice-core archive backlog portrait with intake debt, freezer dependency placeholders, stop tokens, escalation clocks, and zero operators",
        "represented",
        "THOS Body",
        "synthetic intake queues, debt states, cold-storage dependency placeholders, workload ceilings, stop tokens, escalation clocks, and zero operators",
        ["NSF-ICF-ABOUT", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "thos-ice-core-depth-view-trial",
        "Counterbalanced surrogate depth-interval comprehension protocol with shuffled adjacency questions, equal action budget, withdrawal boundary, masked scoring, and empty session ledger",
        "represented",
        "THOS Body",
        "future blind matched-budget protocol, randomized synthetic dossiers, sealed scoring, stop and withdrawal rules, zero participants, and no effectiveness claim",
        ["WCAG22", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "ice-core-stratigraphy-access-matrix",
        "Depth-index access reservation board for tactile relief, linear text, monochrome discontinuity symbols, speech traversal, language support, and unevaluated affected-user tasks",
        "represented",
        "CBR Heart and THOS Body",
        "static multimodal structure and reservations for tactile, monochrome, speech, language, manual, and affected-user evaluation with zero sessions",
        ["WCAG22", "NOAA-ICE-CORE", "TE-MANA-RARAUNGA"],
    ),
    _proposal(
        "real-ice-core-evidence-vault",
        "Empirical admission docket with empty rows for authenticated frozen material, traceable metrology, governed analyses, accountable specialists, adverse controls, and external paleoclimate reproduction",
        "open_gap",
        "All pillars",
        "zero authenticated cores, accountable professionals, calibrated observations, governed analyses, participant outcomes, or independent-review rows",
        ["NSF-ICF-POLICY", "NOAA-ICE-CORE", "NIST-UNCERTAINTY"],
    ),
    _proposal(
        "ice-core-knowledge-authority-register",
        "Reserved jurisdiction circuit for core-site knowledge, community protocols, access terms, benefit obligations, correction, removal, remedy, and Māori decision non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied affected-party, community, Indigenous-knowledge, benefit-sharing, takedown, remedy, tangata whenua, iwi, hapū, and Māori-authority reservations",
        ["TE-MANA-RARAUNGA", "LOCAL-CONTEXTS-TK", "NZ-PRIVACY", "W3C-PROV"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Elaren source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-one-hundred-ninety-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity boundary",
    "bounded Elaren-to-Neris live override",
    "solo and Tavian-standby boundaries",
    "D-first posture",
    "toolchain version receipt",
    "x1 artifact inventory",
    "x1 JSON parsing",
    "x1 five-class privacy scan",
    "x1 stale-label review",
    "x1 diff hygiene",
    "x1 manifest replay",
    "selected-row zero-credit guard",
    "new-row append-only guard",
    "source-label glossary",
    "protected-gate coverage",
    "failure-retention ledger",
    "Method Flow witness pairing",
    "wellbeing workload bound",
    "document-word ceiling",
    "portfolio arithmetic",
    "skill and runner arithmetic",
    "cleanup-plan arithmetic",
    "no-x2-in-x1 guard",
]
SELF_SAFE_TASKS = [
    {
        "task_id": f"V6604-SAFE-{i:03d}",
        "title": f"Validate {name} inside the Neris-owned v660-v4 lane",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {
        "task_id": f"V6605-REC-SAFE-{i:03d}",
        "title": f"Reassess {name} for Vesper-only v660-v5",
        "recipient": "Vesper Arlen",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "ice-core section intake passport",
    "ice-core depth orientation graph",
    "ice-core continuity and hiatus ledger",
    "ice-core cold-chain envelope",
    "ice-core conductivity uncertainty budget",
    "ice-core sample-allocation firewall",
    "ice-core age-depth assertion braid",
    "ice-core stable-isotope envelope",
    "GMUT ice-core transport obligations",
    "ice-core knowledge-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {
        "task_id": f"V6604-CAND-{i:03d}",
        "title": f"Build and test reversible {name}",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {
        "task_id": f"V6605-REC-CAND-{i:03d}",
        "title": f"Consider a distinct Vesper-owned refinement of {name}",
        "recipient": "Vesper Arlen",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6604-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Recover, transport, store, rack, cut, sample, melt, analyse, allocate, publish, transfer, or deaccession any real ice or firn material",
            "Make a real age-depth, isotope, gas, dust, tephra, chronology, climate, provenance, or stratigraphic determination",
            "Use real freezers, loggers, drills, saws, clean laboratories, reagents, instruments, transport, occupational, or public-safety systems",
            "Disclose precise core locations, protected knowledge, private records, beneficiary data, or restricted archive information",
            "Make a professional glaciology, paleoclimatology, geochronology, curation, laboratory, privacy, security, translation, or accessibility determination",
            "Publish a production repository assertion, identifier, credential, signed statement, proof, or interoperable archive record",
            "Allocate ownership, custody, sample access, legal, intellectual-property, benefit-sharing, takedown, remedy, or beneficiary authority",
            "Make a mātauranga, tikanga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, or Māori-authority decision",
            "Run a real participant study, operator trial, workplace workflow, professional review, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Neris-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6604-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate(
        [
            "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
            "Claim AGI, ASI, consciousness, personhood, continuity, employment, qualification, or authority from relational language",
            "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, gates, branches, worktrees, or callers",
            "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, session streams, or application state",
            "Declare Stage 20 readiness without exact external evidence and competent authority",
        ],
        1,
    )
]

SELF_SKILL_SPECS = [
    ("ghc-family-ice-core-section-identity", "Preserve surrogate core, run, section, tube, box, rack, custody, quarantine, correction, and accession-refusal states."),
    ("ghc-family-ice-core-depth-graph", "Represent typed surrogate depth, orientation, discontinuity, uncertainty, contradiction, and abstention."),
    ("ghc-family-ice-core-continuity-ledger", "Track recovered, missing, fractured, rejoined, duplicate, unknown, and no-conclusion states."),
    ("ghc-family-ice-core-cold-chain", "Bind synthetic custody intervals, logger placeholders, excursion flags, missingness, digests, and zero observations."),
    ("ghc-family-ice-core-uncertainty-budget", "Keep quantity, unit, response, covariance, missingness, zero-row, and inference-firewall obligations typed."),
    ("ghc-family-ice-core-allocation-firewall", "Reserve sample request, destructive-use, facility, safety, competent-authority, and zero-execution gates."),
    ("ghc-family-ice-core-chronology-assertion", "Track model-version, tie-point, uncertainty, contradiction, supersession, and chronology abstention."),
    ("ghc-family-gmut-ice-core-obligations", "Keep symbolic thermal, gas, impurity, strain, depth, unit, covariance, boundary, and likelihood obligations nonempirical."),
    ("ghc-family-thos-ice-core-backlog", "Track synthetic queue debt, cold-storage dependencies, workload ceilings, stop tokens, escalation, and zero operators."),
    ("ghc-family-ice-core-knowledge-authority", "Reserve sensitive places, Indigenous knowledge, benefit sharing, remedy, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {
        "name": f"ghc-family-vesper-v660-v5-recommendation-{i:02d}",
        "purpose": purpose,
        "recipient": "Vesper Arlen",
        "completion_credit": 0,
    }
    for i, purpose in enumerate(
        [
            "immutable source digest crosswalk",
            "selected-inheritance no-credit guard",
            "proposal semantic-neighbour tribunal",
            "explicit source-status ledger",
            "authority-boundary completeness check",
            "isolated-failure diagnostic receipt",
            "manifest self-exclusion contract",
            "one-shot canonical pass governor",
            "exact-title route reread shield",
            "successor recommendation provenance",
        ],
        1,
    )
]

SELF_RUNNER_SPECS = [
    ("ghc_family_ice_core_section_identity.py", "ice-core-section-intake-passport"),
    ("ghc_family_ice_core_depth_graph.py", "ice-core-depth-orientation-graph"),
    ("ghc_family_ice_core_continuity_ledger.py", "ice-core-continuity-hiatus-ledger"),
    ("ghc_family_ice_core_cold_chain.py", "ice-core-cold-chain-envelope"),
    ("ghc_family_ice_core_uncertainty_budget.py", "ice-core-conductivity-uncertainty-budget"),
    ("ghc_family_ice_core_allocation_firewall.py", "ice-core-sample-allocation-firewall"),
    ("ghc_family_ice_core_chronology_assertion.py", "ice-core-age-depth-assertion-braid"),
    ("ghc_family_gmut_ice_core_obligations.py", "gmut-ice-core-transport-proxy"),
    ("ghc_family_thos_ice_core_backlog.py", "thos-ice-core-archive-backlog"),
    ("ghc_family_ice_core_knowledge_authority.py", "ice-core-knowledge-authority-register"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {
        "name": f"ghc_family_vesper_v660_v5_recommendation_{i:02d}.py",
        "purpose": purpose,
        "recipient": "Vesper Arlen",
        "completion_credit": 0,
    }
    for i, purpose in enumerate(
        [
            "immutable-source receipt verification",
            "semantic-novelty bounded probe",
            "five-class owner privacy scan",
            "exact manifest replay",
            "one-shot terminal route governor",
        ],
        1,
    )
]

SELF_CLEAN_CATEGORIES = [
    "versioned-name inventory",
    "family-current name preference",
    "compatibility wrapper retention",
    "caller evidence",
    "trigger collision review",
    "stale owner label review",
    "stale phase label review",
    "stale route number review",
    "absolute-path privacy review",
    "raw identifier privacy review",
    "credential-pattern review",
    "nonpublic-content pattern review",
    "duplicate proposal review",
    "duplicate task review",
    "duplicate skill review",
    "duplicate runner review",
    "JSON canonical formatting",
    "Markdown heading order",
    "source-label consistency",
    "truth-label consistency",
    "rollback coverage",
    "protected-gate coverage",
    "failure-credit consistency",
    "same-owner labelling",
    "manifest exclusions",
    "file-cap posture",
    "document-cap posture",
    "commit-cap posture",
    "D-first storage posture",
    "non-destructive cleanup boundary",
]
SELF_CLEAN_TASKS = [
    {
        "task_id": f"V6604-CLEAN-{i:03d}",
        "title": f"Review and refine {name}",
        "state": "planned_x2_additive_only",
    }
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {
        "task_id": f"V6605-REC-CLEAN-{i:03d}",
        "title": f"Reassess {name} additively in Vesper v660-v5",
        "recipient": "Vesper Arlen",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("NOAA-ICE-CORE", "official_noaa_ncei", "https://www.ncei.noaa.gov/products/paleoclimatology/ice-core", "Ice-core archive, study, location, parameter, proxy, search, and contribution vocabulary only; zero data, locations, measurements, chronologies, reconstructions, or scientific conclusions."),
    ("NSF-ICF-ABOUT", "official_nsf_icf", "https://icecores.org/about", "Storage, curation, inventory, examination, and repository vocabulary only; no facility use, material access, handling, safety, or operational authority."),
    ("NSF-ICF-POLICY", "official_nsf_icf", "https://icecores.org/policy", "Use, sample-request, allocation, investigator-responsibility, storage, and facility-access boundary vocabulary only; no request, allocation, permission, or authority claim."),
    ("NSF-ICF-SERVICES", "official_nsf_icf", "https://icecores.org/services", "Sample-request, storage, cutting, processing, shipment, and planning vocabulary only; no service request, real material, or facility action."),
    ("USGS-ICF", "official_usgs", "https://www.usgs.gov/mission-areas/core-science-systems/national-science-foundation-ice-core-facility", "Long-term repository, curation, examination, and measurement vocabulary only; no USGS, NSF, facility, or scientific authority claim."),
    ("CF-1.13", "official_cf_conventions", "https://cfconventions.org/cf-conventions/cf-conventions-1.13/cf-conventions.html", "Released CF 1.13 variable, coordinate, unit, standard-name, missing-data, and provenance-adjacent metadata vocabulary only; no conformance or comparable-data claim."),
    ("LOC-PREMIS-3", "official_library_of_congress", "https://www.loc.gov/standards/premis/", "Preservation object, event, agent-placeholder, rights, relationship, fixity, and outcome-detail vocabulary only."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("W3C-ANNOTATION", "official_w3c", "https://www.w3.org/TR/annotation-model/", "Annotation body, target, motivation, selector, state, provenance, and lifecycle vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, text-alternative, noncolour, navigation, status, and interaction vocabulary with manual and affected-user evaluation reserved."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/publications/international-system-units-si2019-edition", "SI quantity, unit, symbol, and reporting vocabulary only; no measured core or physical result."),
    ("NIST-UNCERTAINTY", "official_nist", "https://www.nist.gov/pml/nist-technical-note-1297", "Measurement-model and uncertainty-reporting vocabulary only; no measurement, calibration certificate, or empirical result."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "New Zealand privacy-principle vocabulary only; no legal, compliance, collection, disclosure, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, or mātauranga claim."),
    ("LOCAL-CONTEXTS-TK", "primary_local_contexts", "https://localcontexts.org/labels/traditional-knowledge-labels/", "Community-defined traditional-knowledge access, use, provenance, permission, and authority-reservation context only; no label is selected or applied."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "NOAA-ICE-CORE": "current",
    "NSF-ICF-ABOUT": "current",
    "NSF-ICF-POLICY": "current",
    "NSF-ICF-SERVICES": "current",
    "USGS-ICF": "current",
    "CF-1.13": "released",
    "LOC-PREMIS-3": "stable",
    "W3C-PROV": "stable",
    "W3C-ANNOTATION": "stable",
    "WCAG22": "current",
    "NIST-SI": "stable",
    "NIST-UNCERTAINTY": "current",
    "NZ-PRIVACY": "current",
    "TE-MANA-RARAUNGA": "stable",
    "LOCAL-CONTEXTS-TK": "current",
    "IETF-JCS": "stable",
    "GIT-LOG": "current",
    "PYTHON-JSON": "current",
}


def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {
        "negative_id": negative_id,
        "signature": signature,
        "recovery": recovery,
        "recovery_passed": True,
    }


STARTUP_FAILURES = [
    _startup_failure("V6604-X1-N001", "ordered-hash-embedded-powershell-probe-and-lastexitcode-produced-a-parser-error", "Retain the parser fault at zero credit and use simple scalar probes with separately captured exit codes."),
    _startup_failure("V6604-X1-N002", "host-dotnet-runtime-did-not-expose-static-sha256-hashdata", "Retain the missing-method failure and use SHA256.Create().ComputeHash with deterministic disposal."),
    _startup_failure("V6604-X1-N003", "combined-source-state-wrapper-returned-no-attributable-output", "Retain the empty wrapper result and reverify each source-state scalar in bounded isolated probes."),
    _startup_failure("V6604-X1-N004", "first-inline-manifest-replay-lost-newline-transport-and-raised-syntaxerror", "Retain the SyntaxError and pass the unchanged UTF-8 Python program over standard input."),
    _startup_failure("V6604-X1-N005", "git-cat-file-batch-helper-wrote-all-requests-before-draining-output-and-deadlocked", "Retain the deadlock, stop only the exact owner-started process tree, and use communicate-style bounded input and output draining."),
    _startup_failure("V6604-X1-N006", "first-worktree-add-lost-windows-backslashes-in-javascript-string-and-created-a-malformed-drive-relative-checkout", "Retain the failed checkout, verify no registration and exact branch head, and use literal PowerShell D-drive paths with long-path support."),
    _startup_failure("V6604-X1-N007", "combined-malformed-checkout-audit-returned-no-serialized-output", "Retain the empty audit and inspect branch, directory, registration, and source cleanliness through isolated scalars."),
    _startup_failure("V6604-X1-N008", "computed-recursive-cleanup-command-was-rejected-by-command-safety-before-execution", "Retain the rejection, perform no delete, and prefer a fully verified recoverable same-volume quarantine move."),
    _startup_failure("V6604-X1-N009", "literal-recursive-cleanup-command-was-rejected-by-command-safety-before-execution", "Retain the rejection, perform no delete, and verify the exact target state before any recovery action."),
    _startup_failure("V6604-X1-N010", "quarantine-move-found-the-malformed-checkout-already-absent", "Retain the state-drift witness, make no mutation, and re-audit source cleanliness, intended branch head, and both exact paths."),
    _startup_failure("V6604-X1-N011", "first-scaffold-materialized-x2-and-closeout-source-before-the-x1-freeze", "Retain the lifecycle violation at zero credit, delete only the new untracked Neris x2 files, and require explicit stage selection in the scaffold."),
    _startup_failure("V6604-X1-N012", "pattern-count-projection-piped-directly-from-powershell-foreach-and-raised-empty-pipe-element", "Retain the parser fault and materialize the foreach rows before JSON serialization."),
    _startup_failure("V6604-X1-N013", "one-line-frozen-index-keyword-search-produced-truncated-non-attributable-output", "Retain the truncated display and parse the JSON index structurally before applying a bounded title predicate."),
    _startup_failure("V6604-X1-N014", "first-multi-section-x1-patch-was-rejected-atomically-on-encoding-sensitive-context", "Retain the rejected patch at zero credit, inspect the exact UTF-8 code points, and apply bounded Unicode-exact and ASCII-safe hunks."),
    _startup_failure("V6604-X1-N015", "first-3190-title-novelty-screen-passed-sixteen-of-twenty-and-rejected-four-near-template-neighbours", "Retain the four rejected title witnesses at zero credit, rewrite only those titles around distinct ice-core mechanisms, and rerun the unchanged bounded threshold."),
    _startup_failure("V6604-X1-N016", "first-scoped-x1-test-run-passed-twenty-one-of-twenty-three-and-found-two-family-current-receipt-groups-not-yet-materialized", "Retain the 21-pass and two missing-receipt errors at zero credit, invoke only the declared family-current receipt builders, refresh x1 manifests, and rerun the scoped suite."),
    _startup_failure("V6604-X1-N017", "exact-x1-add-succeeded-but-the-powershell-summary-used-bare-true-instead-of-the-boolean-variable", "Retain the post-stage summary fault at zero credit, inspect the index directly, use $true in later PowerShell objects, and restage the unchanged exact allowlist after receipt refresh."),
    _startup_failure("V6604-X1-N018", "first-x1-stale-domain-scan-treated-selected-inherited-lichen-rows-and-scaffold-compatibility-literals-as-current-domain-drift", "Retain the two false-positive files at zero credit, require inherited overview rows to keep their explicit zero-credit origin, and classify scaffold rewrite literals only inside the declared compatibility transformer."),
    _startup_failure("V6604-X1-N019", "first-index-derived-x1-review-assumed-owner-and-phase-fields-that-three-declared-schemas-do-not-use", "Retain the zero-credit schema-assumption failure, inspect each declared JSON key set, and rerun only the corrected staged reviewer against name/current_exact_title plus the actual owner and phase fields."),
]

# X2 failures may be appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
