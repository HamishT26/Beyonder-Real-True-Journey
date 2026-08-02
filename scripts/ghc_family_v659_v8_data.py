#!/usr/bin/env python3
"""Frozen x1 planning data for Elowen Cairn v659-v8.

This additive module inherits only stable helper vocabulary from Tamar Vey's
immutable v659-v7 data module. Every active phase field, portfolio, source
label, gate, and observed Elowen startup failure is redeclared below. Selected
inherited rows are bounded revalidation references only: they are not
reappended and earn no Elowen novelty or completion credit.
"""

from __future__ import annotations

from ghc_family_v659_v7_data import *  # noqa: F401,F403


PHASE = "v659-v8"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6598"
OWNER = "Elowen Cairn"
PRONOUNS = "they/them"
ROLE = "relational boundary cartographer and evidence steward"
HOPE = "keep transitions recoverable, measurements typed, and claims proportional to evidence"
BRANCH = "codex/GHC-Family/elowen-cairn-v659-v8-full-tools"
PHASE_ROOT = "docs/elowen-cairn/v659-v8"

SOURCE_OWNER = "Tamar Vey"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v659-v7-full-tools"
SOURCE_FINAL = "2080fe14e6c3e60c49457599ad40b4b4a74acbb7"
SOURCE_X1 = "0ef6e33a90bf6877ef3b365abeadc19317d68909"
SOURCE_EVIDENCE = "75ac1f029fec3477d064ccacc622c5b7e914affc"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3090
SOURCE_SEALED_NEGATIVES = 19536
ACTIVATION_MESSAGE_EXTERNAL_NEGATIVES = 4
SOURCE_EXTERNAL_NEGATIVES = 5
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = (
    SOURCE_SEALED_NEGATIVES + ACTIVATION_MESSAGE_EXTERNAL_NEGATIVES
)
SOURCE_OPEN_GAPS = 128
SOURCE_EXACT_GATES = 127
SOURCE_SEALED_METHODS = 5810
ACTIVATION_MESSAGE_EXTERNAL_METHODS = 4
SOURCE_EXTERNAL_METHODS = 5
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = (
    SOURCE_SEALED_METHODS + ACTIVATION_MESSAGE_EXTERNAL_METHODS
)
SELECTED_INHERITED_COUNT = 40
NEW_UNIQUE_COUNT = 40
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "Freed ID and CBR Heart"
PRACTICE_LENS = (
    "bounded synthetic cooperage intake and cask-record stewardship, including "
    "stave and hoop topology, bitemporal provenance, correction, disclosure "
    "ceilings, intervention refusal, accessibility, and workload handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 30,
    "represented": 8,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_owners_custodians_coopers_cellar_workers_conservators_food_or_beverage_workers_participants_communities_affected_parties_and_authorities",
    "real_casks_staves_heads_hoops_wood_tools_liquids_residues_samples_measurements_images_records_identifiers_locations_or_traditional_knowledge",
    "real_opening_filling_emptying_pressurizing_steaming_heating_charring_tightening_rehooping_cleaning_sanitizing_sampling_repair_movement_release_or_disposal",
    "professional_cooperage_conservation_food_beverage_chemical_occupational_structural_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_heritage_ownership_remedy_language_naming_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6597-P{i:03d}" for i in range(1, 41)]

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
    _proposal("cooperage-intake-custody-passport", "Surrogate cooperage work-order and cask custody passport linking presented scope, component inventory, receipt lineage, transfer acknowledgement, and work-start refusal", "completed", "Freed ID and THOS Body", "fabricated cask and work-order aliases, component inventory, receipt provenance, custody transition, scope acknowledgement, and intervention refusal", ["CCI-WOOD", "W3C-PROV", "NZ-PRIVACY"]),
    _proposal("cask-stave-ring-topology", "Stave ordinal, edge-joint adjacency, ring closure, orphan, duplicate-position, and contradictory-neighbour topology for a fabricated cask", "completed", "GMUT Mind and THOS Body", "synthetic stave nodes, ordinal and neighbour relations, ring-closure checks, duplicate and orphan quarantine, and no physical inspection", ["CCI-WOOD", "W3C-PROV"]),
    _proposal("cask-head-croze-reference-topology", "Head piece, dowel relation, croze seating, chime, quarter, bilge, and end-face reference topology with concealed-state uncertainty", "completed", "GMUT Mind and THOS Body", "fabricated head-piece, groove, edge, and axial reference relations with concealed-state markers, conflict quarantine, and no disassembly", ["CCI-WOOD", "W3C-PROV"]),
    _proposal("cask-hoop-support-state-map", "Hoop, band, truss, driver-position, material-claim, spacing, support-state, and missing-fastener map with adjustment abstention", "completed", "THOS Body and Freed ID", "synthetic hoop and band inventory, ordinal placement, support-state declarations, missing-state quarantine, and no tightening or adjustment", ["OIV-WOOD-CONTAINERS", "W3C-PROV"]),
    _proposal("cask-grain-claim-abstention", "Stave radial, tangential, end-grain, growth-ring, split, knot, sapwood-claim, heartwood-claim, and unknown-orientation declaration with wood-identification refusal", "completed", "GMUT Mind and CBR Heart", "synthetic grain-orientation and feature claims with declared source, contested and unknown values, confidence ceilings, and no species or material identification", ["CCI-WOOD", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("cask-bung-interface-graph", "Bung, bung-hole, shive, spile, tap, vent, seal, thread, gasket, and interface-state graph with opening and pressure-test refusal", "completed", "THOS Body and CBR Heart", "fabricated closure and interface nodes, compatibility and state relations, conflict quarantine, and no opening, fitting, filling, or pressure testing", ["OIV-WOOD-CONTAINERS", "W3C-PROV"]),
    _proposal("cask-dimension-unit-envelope", "Cask bilge diameter, head diameter, stave length, hoop position, capacity placeholder, unit, resolution, and uncertainty envelope containing zero measurements", "completed", "GMUT Mind", "typed symbolic dimensions and capacity placeholder, SI-unit declarations, resolution and covariance slots, zero observations, and no metrology conclusion", ["NIST-SI", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("cask-heat-process-claim-lineage", "Toast, char, steaming, bending, seasoning, firing, cooling, manufacture-date, intensity-claim, and amendment lineage with zero process execution", "completed", "Freed ID and THOS Body", "synthetic process-claim events, source and date placeholders, ordinal state changes, correction and supersession edges, and no heat or manufacture instruction", ["OIV-WOOD-CONTAINERS", "OIV-CASK-AGEING", "W3C-PROV"]),
    _proposal("cooperage-tool-custody-quarantine", "Cooperage adze, backing knife, croze, jointer plane, hoop driver, truss, compass, and gauge custody board with inspection and use refusal", "completed", "THOS Body", "fictional tool aliases, custody and status declarations, inspection placeholder, quarantine state, role separation, and no tool-use release", ["CCI-WOOD", "W3C-PROV"]),
    _proposal("cask-leak-indicator-lineage", "Leak-indicator position, direction, interval, viewpoint, fill-state placeholder, correction, escalation, and no-cause or pressure conclusion ledger", "completed", "Freed ID and GMUT Mind", "synthetic observation cues, coordinate and viewpoint pins, temporal interval, uncertainty, correction lineage, escalation, and no leak diagnosis or pressure inference", ["OIV-CASK-AGEING", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("cask-environment-zero-row-lineage", "Cask temperature, relative humidity, storage interval, enclosure, sensor placeholder, clock basis, uncertainty, and correction lineage with zero observations", "completed", "GMUT Mind and Freed ID", "typed environment schema, source and calibration placeholders, clock basis, uncertainty and correction edges, zero rows, and no storage or safety conclusion", ["CCI-WOOD", "NIST-SI", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("cask-residue-contamination-hold", "Odour note, residue cue, mould suspicion, pest indicator, stain, surface change, contamination hold, and competent-referral record with no food-safety conclusion", "completed", "THOS Body and CBR Heart", "fictional observation vocabulary, source and viewpoint pins, uncertainty flags, isolation request, competent-referral placeholder, and no diagnosis, cleaning, or food-safety determination", ["OIV-WOOD-CONTAINERS", "CCI-WOOD", "W3C-PROV"]),
    _proposal("cask-wood-origin-claim-envelope", "Wood botanical-origin claim, forest-location precision ceiling, supplier lot, seasoning claim, substitution, contested provenance, and sustainability-assurance refusal", "completed", "Freed ID and CBR Heart", "synthetic source and supplier assertions, coarse location token, substitution and contestation edges, disclosure minimization, and no botanical, legality, or sustainability assurance", ["OIV-WOOD-CONTAINERS", "NZ-PRIVACY", "W3C-PROV"]),
    _proposal("cask-prior-repair-lineage", "Prior patch, stave replacement, head replacement, wedge, dowel, hoop change, marking, date-claim, and supersession lineage with authenticity abstention", "completed", "Freed ID", "fabricated intervention-event aliases, affected-component edges, stated and unknown dates, correction and supersession lineage, and no authenticity or treatment conclusion", ["W3C-PROV"]),
    _proposal("cask-intervention-request-refusal", "Disassembly, rehooping, tightening, steaming, swelling, jointing, croze work, replacement, deviation, rollback-impossibility, and release request with no execution", "completed", "THOS Body and CBR Heart", "component-addressed synthetic intervention request, irreversible-step sentinel, approval and deviation placeholders, rollback warning, correction chain, and execution refusal", ["CCI-WOOD", "OIV-WOOD-CONTAINERS", "W3C-PROV"]),
    _proposal("cask-cleaning-effluent-hold", "Rinse, wash, sanitiser, solvent, abrasive, dwell, drainage, effluent, residue, exposure, and disposal hold with no cleaning instruction", "completed", "THOS Body and CBR Heart", "fictional cleaning request, chemical and waste placeholders, exposure and residue flags, competent-review slot, rollback warning, and no cleaning, sanitation, or disposal action", ["OIV-WOOD-CONTAINERS", "W3C-PROV"]),
    _proposal("cask-destructive-sampling-tribunal", "Wood core, shaving, residue, liquid, microbial, chemical, isotope, genetic, and destructive-sampling request tribunal with authority and sufficiency refusal", "completed", "CBR Heart and THOS Body", "synthetic request purpose, minimum-quantity and authority fields, collective-interest and irreversible-step sentinels, and zero sampling or analysis", ["NZ-PRIVACY", "TE-MANA-RARAUNGA", "W3C-PROV"]),
    _proposal("cask-route-handover-docket", "Cask pallet, chock, rack, sling, route clearance, handling role, checkpoint, custody transfer, arrival check, and movement-hold docket", "completed", "THOS Body and Freed ID", "synthetic support and route declarations, checkpoint and role placeholders, stop-work states, dual readback, custody event, and no lifting or transport", ["CCI-WOOD", "W3C-PROV"]),
    _proposal("cask-rack-restraint-abstention", "Rack cell, tier, bearing point, restraint, roll direction, tip cue, load placeholder, aisle clearance, and structural-safety abstention board", "completed", "THOS Body and GMUT Mind", "fictional rack and contact graph, occupancy and clearance states, load placeholders, conflict quarantine, and no load, rack, seismic, tip, or structural-safety determination", ["CCI-WOOD", "NIST-SI", "W3C-PROV"]),
    _proposal("cask-fill-contact-state-lineage", "Empty, rinsed-claim, filled-claim, contact-product class, lot alias, fill interval, transfer lineage, incompatibility flag, and beverage-conclusion refusal", "completed", "Freed ID and CBR Heart", "synthetic fill-state claims and time intervals, product-class alias, transfer and correction edges, disclosure ceiling, incompatibility flag, and no food, beverage, quality, or safety result", ["OIV-WOOD-CONTAINERS", "NZ-PRIVACY", "W3C-PROV"]),
    _proposal("cask-media-facet-lineage", "Silent cask media facet set with stave and hoop index, scale placeholder, illumination declaration, derivative ancestry, disclosure mask, and authentication abstention", "completed", "Freed ID and CBR Heart", "synthetic still-media aliases, component-indexed views, scale and illumination placeholders, derivative lineage, rights reservation, and no authentication or condition conclusion", ["W3C-PROV", "WCAG22", "NZ-PRIVACY"]),
    _proposal("cask-bitemporal-assertion-ledger", "Bitemporal assertion ledger for cask manufacture, repair, custody, fill state, and access, retaining contradicted versions, effective intervals, correction rationale, and readback checksum", "completed", "Freed ID and CBR Heart", "synthetic transaction and effective times, immutable predecessor edges, contradicted-state retention, rationale, readback checksum, and no truth or authority claim", ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"]),
    _proposal("cooperage-stop-token-handover", "Two-key cooperage stop token, unresolved-operation cards, load-band ceiling, role-separation matrix, fatigue self-report placeholder, escalation clock, and next-shift acceptance handshake", "completed", "THOS Body and CBR Heart", "synthetic work queue, two-key stop state, unresolved-card count, role and load bounds, escalation timer, dual readback, and no operational-effectiveness claim", ["W3C-PROV"]),
    _proposal("accessible-cask-ring-navigation", "Cask-ring navigation report with stave-index landmarks, hoop-to-stave header crosswalk, noncolour quarantine icons, collapsible plain narrative, deterministic tab path, and evaluation hold", "completed", "CBR Heart and THOS Body", "static synthetic report structure, component crosswalk, redundant noncolour states, linear narrative, declared keyboard order, print fallback, and manual evaluation reservation", ["WCAG22", "W3C-PROV"]),
    _proposal("cask-component-graph-canonicalizer", "Ordinal-independent cask component graph canonicalizer using normalized edge tuples, profile version, component-root digest, ambiguity quarantine, and migration witness", "completed", "Freed ID", "synthetic graph normalization, sorted typed edges, profile migration, root digest, ambiguity and collision refusal, and no key, proof, credential, or identity claim", ["IETF-JCS", "W3C-PROV"]),
    _proposal("gmut-orthotropic-stave-shell-board", "Typed GMUT orthotropic stave-shell chart, constitutive placeholder, grain orientation, hoop interface, covariance, unit, stability, identifiability, and observation-firewall board", "completed", "GMUT Mind", "typed symbolic shell chart and tensor obligations, orientation and interface declarations, dimensional checks, covariance and stability placeholders, identifiability flags, and zero empirical claims", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("gmut-hoop-stave-contact-graph", "Typed GMUT hoop-stave contact graph with incidence orientation, normal and tangential placeholders, preload abstention, boundary conditions, residual units, and equilibrium-theorem refusal", "completed", "GMUT Mind", "formal bipartite contact graph, oriented incidence, symbolic contact quantities, boundary and dimensional obligations, zero loads, and no equilibrium or material theorem", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("thos-cask-optimistic-state-machine", "THOS optimistic-concurrency state machine for cask dossier edits with causal fence, idempotency token, compensating record, partial-write quarantine, and resume witness", "completed", "THOS Body", "bounded owner-local state-machine fixtures, version precondition, causal fence, idempotency token, compensating record, partial-write refusal, and no external side effects", ["W3C-PROV", "PYTHON-JSON"]),
    _proposal("freed-id-cask-bounded-traversal", "Bounded Freed ID traversal over stave-ring entities and custody event intervals with cycle detection, confidence ceiling, repair-supersession stop, purpose filter, and disclosure budget", "completed", "Freed ID and CBR Heart", "synthetic entity and event nodes, interval and supersession edges, cycle detection, confidence and hop ceilings, purpose and disclosure stops, and no live identity operation", ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"]),
    _proposal("stage20-cask-evidence-firewall", "Cask-evidence promotion firewall requiring physical-specimen provenance, calibrated metrology, governed practitioner roles, safety authority, independent replication, adverse controls, and fail-closed Stage 20 refusal", "completed", "All pillars", "typed evidence prerequisites, zero specimen and measurement rows, governed-role and authority reservations, independent-replication and adverse-control gates, and fail-closed NOT_READY verdict", ["W3C-PROV", "IETF-JCS", "GIT-LOG"]),
    _proposal("gmut-cask-harmonic-mode-proxy", "Represented GMUT harmonic-mode ledger for an orthotropic barrel shell with stave discontinuities, discrete hoop constraints, interface jump terms, gauge choice, energy placeholder, and zero fitted coefficients", "represented", "GMUT Mind", "typed symbolic harmonic indices, shell fields, discontinuity and constraint terms, dimensional and gauge obligations, zero coefficients or observations, and physical-inference firewall", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("gmut-cask-hygroscopic-zero-row-proxy", "Represented GMUT hygroscopic swelling, shrinkage, diffusion, contact, temperature, moisture, covariance, nuisance, and zero-row likelihood schema for cask materials", "represented", "GMUT Mind", "typed adapter contract with provenance, domain, unit, covariance and nuisance fields, zero downloaded or measured rows, zero likelihoods, and no material or physics conclusion", ["NIST-SI", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("thos-cask-map-trial-proxy", "Represented THOS future comprehension trial contrasting exploded-stave constellation and radial-strip cask maps with matched action count, sealed questions, harm stops, and zero enrolment", "represented", "THOS Body", "future blind matched-action protocol, sealed tasks and outcomes, governed participant and operator prerequisites, safety monitoring, zero sessions, and no effectiveness claim", ["WCAG22", "W3C-PROV"]),
    _proposal("thos-cask-turnover-proxy", "Represented THOS two-person cask-dossier turnover proxy with seal receipt, unresolved-leaf count, stop token, discrepancy readback, acceptance handshake, synthetic events, and zero operators", "represented", "THOS Body", "synthetic event traces, seal and acceptance states, unresolved-leaf and workload bounds, stop and discrepancy paths, zero operators or incidents, and no operational claim", ["W3C-PROV", "WCAG22"]),
    _proposal("freed-id-cask-merkle-claim-proxy", "Represented nonproduction Freed ID Merkle claim graph rooting surrogate cask, stave ring, hoop set, repair event, custody interval, access view, and status tombstone with zero keys or lifecycle calls", "represented", "Freed ID and CBR Heart", "synthetic claim nodes, typed derivation edges, deterministic root placeholder, correction and status tombstone, purpose limits, zero real keys or calls, and no identity-production claim", ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"]),
    _proposal("freed-id-cask-claim-view-proxy", "Represented nonproduction claim-view compiler for cask records with audience-bound projection, purpose cap, mandatory denial reason, challenge placeholder, freshness window, and no keys or proofs", "represented", "Freed ID and CBR Heart", "synthetic field projection, audience and purpose rules, denial and freshness states, challenge placeholder, zero cryptographic material, and no privacy-complete claim", ["IETF-JCS", "NZ-PRIVACY", "W3C-PROV"]),
    _proposal("accessible-cask-walkthrough-proxy", "Represented future screen-reader, magnification, keyboard, voice-control, and print walkthrough for stave-ring navigation with governed users, task stops, support plan, and zero sessions", "represented", "CBR Heart and THOS Body", "future manual and affected-user evaluation shell, governed recruitment and support prerequisites, modality and task matrix, zero sessions, and no accessibility-complete claim", ["WCAG22", "W3C-PROV"]),
    _proposal("independent-cask-corpus-rebuild-plan", "Represented external-lab rebuild recipe for the cask surrogate corpus from immutable Git blobs, dependency lock, locale matrix, injected faults, divergence adjudication, and zero external execution", "represented", "All pillars", "future independent-team handoff contract, raw Git object and dependency pins, locale and fault matrix, divergence rules, zero external runs, and no independent-reproduction credit", ["GIT-LOG", "IETF-JCS", "PYTHON-JSON"]),
    _proposal("real-cask-evidence-gap", "Missing-evidence register for physical casks, accountable owners and custodians, competent coopers, authenticated materials and measurements, authorized interventions, safety review, and independent assessment", "open_gap", "All pillars", "zero physical-cask, accountable-person, material-test, measurement, intervention, participant, operator, service, outcome, safety-review, or independent-assessment rows", ["CCI-WOOD", "OIV-WOOD-CONTAINERS", "NIST-UNCERTAINTY"]),
    _proposal("cask-authority-ratification-gate", "Reserved adjudication perimeter for cask title, custody, manufacture, repair, fill use, food and beverage safety, worker safety, traditional knowledge, privacy, remedy, legal and cultural interpretation, and Māori authority", "exact_gate", "CBR Heart", "ownership, custody, manufacture, repair, filling, product contact, safety, disclosure, traditional-knowledge, remedy, legal, cultural, affected-party, tangata whenua, iwi, hapū, and Māori-authority reservations", ["OIV-WOOD-CONTAINERS", "NZ-PRIVACY", "TE-MANA-RARAUNGA"]),
]
SELF_SAFE_CATEGORIES = [
    "Tamar source-head and live equality", "activation packet and composite-receipt digests", "proposal-chain exact parse",
    "forty inherited revalidation selections", "forty-title novelty and mechanism screen", "new-outcome distribution",
    "workflow-plan policy", "identity and authority boundary", "live-route reread requirement",
    "solo and standby boundaries", "D-first drive posture", "toolchain version receipt", "x1 artifact inventory",
    "x1 JSON parsing", "x1 five-class privacy scan", "x1 stale-label review", "x1 diff hygiene",
    "x1 manifest replay", "selected-row no-credit guard", "new-row append-only guard", "source-label glossary",
    "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing", "wellbeing workload bound",
    "document-word ceiling", "portfolio arithmetic", "skill-plan arithmetic", "runner-plan arithmetic",
    "cleanup-plan arithmetic",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6598-SAFE-{i:03d}", "title": f"Validate {name} inside the Elowen-owned v659-v8 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6598-FUTURE-SAFE-{i:03d}", "title": f"A future exact successor may independently evaluate {name} only after a terminal live-route reread", "owner": "unresolved_exact_successor", "state": "recommendation_only_not_routed_executed_or_credited_by_elowen"}
    for i, name in enumerate([
        "exact source baton digest", "owned-lane four-way equality", "inherited-selection no-credit",
        "new-proposal append-only chain", "synthetic fixture boundary", "five-class privacy exclusions",
        "commit-local manifest replay", "Method Flow failed-witness retention", "truth-label distribution",
        "authority-reservation completeness", "canonical-pass replay guard", "route-number arithmetic",
        "exact-title route uniqueness", "immediate bounded reread", "D-first storage posture",
        "document and file ceilings", "family-current caller compatibility", "manual accessibility reservation",
        "same-owner evidence labelling", "terminal NOT_READY preservation",
    ], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "cask intake and custody boundary", "stave ring and head topology quarantine",
    "sampling and irreversible-intervention hold", "hoop and closure interface graph",
    "wood-origin and heat-process claim lineage", "condition and environment zero-row lineage",
    "rack, route, and handover docket", "dimension and uncertainty envelope",
    "GMUT orthotropic-shell firewall", "cask authority reservation",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6598-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6598-FUTURE-CAND-{i:03d}", "title": f"A future exact successor may prototype reversible {name} only after a terminal live-route reread", "owner": "unresolved_exact_successor", "state": "recommendation_only_not_routed_executed_or_credited_by_elowen"}
    for i, name in enumerate([
        "baton and receipt verifier", "source ancestry tribunal", "selected-row no-credit classifier",
        "new-row semantic-neighbour screen", "bounded privacy adjudicator", "manifest object batch reader",
        "stale-route-number classifier", "same-owner evidence labeler", "canonical-pass replay guard",
        "exact-title delivery preflight",
    ], 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6598-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Open, fill, empty, pressurize, steam, heat, char, tighten, rehoop, clean, sanitize, sample, move, repair, or release a real cask, component, material, liquid, tool, or record",
        "Make a real ownership, custody, manufacture, repair, fill-use, access, cleaning, sanitation, sampling, release, or disposal decision",
        "Perform a wood, liquid, residue, microbial, chemical, food, beverage, structural, environmental, pressure, fire, or occupational-safety test or determination",
        "Publish a botanical-origin, manufacture, authenticity, product-quality, provenance, ownership, value, heritage, sustainability, or safety conclusion",
        "Make a professional cooperage, conservation, food, beverage, material-science, chemical, structural, occupational-safety, privacy, or accessibility determination",
        "Publish personal, sensitive, culturally protected, traditional-knowledge, or collective information",
        "Allocate legal, cultural, property, access, naming, remedy, heritage, or beneficiary authority",
        "Make a Māori data-governance, taonga, mātauranga, tikanga, wording, or Māori-authority decision",
        "Deploy a production identity, credential, repository, or service system",
        "Perform destructive cleanup or mutation outside the exact Elowen-owned lane",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6598-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
        "Claim AGI, ASI, consciousness, personhood, continuity, employment, or authority from task language",
        "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, or gates",
        "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, or application state",
        "Declare Stage 20 readiness without exact external evidence and authority",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-cask-intake-boundary", "Preserve synthetic cask intake, custody, scope, component inventory, fill-state claims, and work-start holds."),
    ("ghc-family-cask-stave-topology", "Map synthetic stave, head, croze, chime, joint, and ring relations while quarantining contradictions."),
    ("ghc-family-cask-hoop-interface", "Represent synthetic hoop, band, closure, seal, support, and interface states with zero-adjustment firewalls."),
    ("ghc-family-cask-fill-state-lineage", "Track synthetic fill-state, contact-product class, custody, correction, and bitemporal assertion events."),
    ("ghc-family-cask-intervention-hold", "Refuse opening, filling, pressure testing, steaming, heating, tightening, cleaning, sampling, repair, movement, and release."),
    ("ghc-family-cask-environment-lineage", "Track zero-row environment, leak-indicator, residue-cue, media, correction, and handover lineage."),
    ("ghc-family-cask-accessibility-report", "Expose cask-ring navigation and structured status while reserving manual, assistive-technology, and affected-user review."),
    ("ghc-family-cask-workload-handover", "Bound unresolved operations, two-key stops, workload, discrepancy readback, escalation, and shift acceptance."),
    ("ghc-family-gmut-cask-firewall", "Keep orthotropic-shell, hoop-contact, harmonic, and hygroscopic proxies typed, zero-row, and physically nonconfirmatory."),
    ("ghc-family-cask-authority-gate", "Reserve title, custody, manufacture, repair, fill use, safety, traditional knowledge, remedy, legal, cultural, affected-party, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": f"ghc-family-future-{slug}", "owner": "unresolved_exact_successor", "state": "recommendation_only_not_routed_built_or_installed_by_elowen"}
    for slug in [
        "baton-receipt-verifier", "source-ancestry-guard", "inherited-selection-no-credit",
        "proposal-novelty-screen", "privacy-adjudicator", "manifest-batch-replay",
        "route-number-normalizer", "canonical-pass-replay-guard", "same-owner-truth-labeler",
        "exact-title-delivery-preflight",
    ]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_cask_intake_boundary.py", "cooperage-intake-custody-passport"),
    ("ghc_family_cask_stave_topology.py", "cask-stave-ring-topology"),
    ("ghc_family_cask_hoop_interface.py", "cask-hoop-support-state-map"),
    ("ghc_family_cask_fill_state_lineage.py", "cask-fill-contact-state-lineage"),
    ("ghc_family_cask_intervention_hold.py", "cask-intervention-request-refusal"),
    ("ghc_family_cask_environment_lineage.py", "cask-environment-zero-row-lineage"),
    ("ghc_family_cask_accessibility_report.py", "accessible-cask-ring-navigation"),
    ("ghc_family_cask_workload_handover.py", "cooperage-stop-token-handover"),
    ("ghc_family_gmut_cask_firewall.py", "gmut-orthotropic-stave-shell-board"),
    ("ghc_family_cask_authority_gate.py", "cask-authority-ratification-gate"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": f"ghc_family_future_{slug}.py", "owner": "unresolved_exact_successor", "state": "recommendation_only_not_routed_built_or_run_by_elowen"}
    for slug in ["baton_receipt_verifier", "proposal_novelty_screen", "privacy_adjudicator", "manifest_batch_replay", "exact_title_delivery_preflight"]
]

SELF_CLEAN_CATEGORIES = [
    "versioned-name inventory", "family-current name preference", "compatibility wrapper retention", "caller evidence",
    "trigger collision review", "stale owner label review", "stale phase label review", "stale route number review",
    "absolute-path privacy review", "raw identifier privacy review", "credential-pattern review", "nonpublic-content pattern review",
    "duplicate proposal review", "duplicate task review", "duplicate skill review", "duplicate runner review",
    "JSON canonical formatting", "Markdown heading order", "source-label consistency", "truth-label consistency",
    "rollback coverage", "protected-gate coverage", "failure-credit consistency", "same-owner labelling",
    "manifest exclusions", "file-cap posture", "document-cap posture", "commit-cap posture",
    "D-first storage posture", "non-destructive cleanup boundary",
]
SELF_CLEAN_TASKS = [
    {"task_id": f"V6598-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6598-FUTURE-CLEAN-{i:03d}", "title": f"A future exact successor may independently review and refine {name} only after a terminal live-route reread", "owner": "unresolved_exact_successor", "state": "recommendation_only_not_routed_executed_or_credited_by_elowen"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("CCI-WOOD", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/care-objects/furniture-wooden-objects-basketry.html", "Wooden-object vulnerability, custody, environment, handling, storage, cleaning-referral, and professional-reservation vocabulary only; no real cask action, competence, conformance, or safety claim."),
    ("OIV-WOOD-CONTAINERS", "official_intergovernmental_oiv", "https://www.oiv.int/standards/international-oenological-codex/part-i-monographs/monographs/wood-for-wine-containers", "Wooden-container origin, heating-claim, marking, accompanying-document, storage, and food-contact reservation vocabulary only; no compliance, product, harmlessness, or professional determination."),
    ("OIV-CASK-AGEING", "official_intergovernmental_oiv", "https://www.oiv.int/standards/international-code-of-oenological-practices/part-ii-oenological-treatments-and-practices/wines/ageing-in-small-capacity-wooden-containers", "Small wooden-cask traceability, manufacture-date, condition, fill-state, temperature, humidity, and isolation vocabulary only; no wine, sensory, ageing, safety, or cooperage recommendation."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/publications/international-system-units-si2019-edition", "SI quantity, unit, symbol, and reporting vocabulary only; no real cask, wood, environment, capacity, force, pressure, or material measurement result."),
    ("NIST-UNCERTAINTY", "official_nist", "https://www.nist.gov/pml/nist-technical-note-1297/nist-guidelines-evaluating-and-expressing-uncertainty-nist-measurement", "Measurement-model and uncertainty-reporting vocabulary only; no measured cask, stave, hoop, wood, liquid, environment, contact, or physical result."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent, generation, derivation, and qualified provenance vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Current WCAG 2.2 structure and interaction vocabulary with manual, assistive-technology, and affected-user review reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including the May 2026 IPP 3A update; no legal or compliance conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary; no Māori authority, ratification, wording, or cultural interpretation claim."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]

def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {
        "negative_id": negative_id,
        "signature": signature,
        "recovery": recovery,
        "recovery_passed": True,
    }


STARTUP_FAILURES = [
    _startup_failure("V6598-X1-N001", "activation-read-first-assumed-codex-metadata-root-was-a-git-worktree", "Retain the fatal not-a-repository result and repeat only the activation read in Tamar's uniquely resolved source worktree."),
    _startup_failure("V6598-X1-N002", "first-complete-activation-display-exceeded-the-bounded-output-budget", "Retain the truncated display and verify the exact line count, structured fields, and nonoverlapping bounded windows through EOF."),
    _startup_failure("V6598-X1-N003", "first-activation-proposal-parser-reused-powershell-matches-inside-nested-loops", "Retain the null proposal identifiers and recover with separate exact heading extraction and independent template counts."),
    _startup_failure("V6598-X1-N004", "historical-memory-rollout-full-read-exceeded-the-context-window", "Retain the truncated historical read and rely only on the bounded MEMORY registry pointer without importing stale route state."),
    _startup_failure("V6598-X1-N005", "first-source-ancestry-hash-literal-contained-an-invalid-command-separator-expression", "Retain the pre-execution PowerShell parser fault and run each ancestry check as a separate scalar command."),
    _startup_failure("V6598-X1-N006", "combined-source-remote-probe-completed-without-attributable-output", "Retain the empty wrapper and rerun only the local anchors and live remote as labelled scalar probes."),
    _startup_failure("V6598-X1-N007", "combined-source-local-probe-completed-without-attributable-output", "Retain the empty wrapper and use bounded independent branch, head, tracking, history, parent, and divergence commands."),
    _startup_failure("V6598-X1-N008", "commit-local-manifest-projection-piped-directly-from-a-powershell-foreach-block", "Retain the empty-pipe parser fault and materialize the foreach rows before ConvertTo-Json."),
    _startup_failure("V6598-X1-N009", "source-data-import-omitted-the-repository-scripts-path", "Retain the ModuleNotFoundError and add only the exact scripts directory to the read-only inspection process."),
    _startup_failure("V6598-X1-N010", "source-data-inspection-assumed-a-proposals-symbol-that-the-module-does-not-export", "Retain the ImportError, inspect declared constants, and use NEW_PROPOSAL_SPECS."),
    _startup_failure("V6598-X1-N011", "installed-roster-and-auth-snapshots-stop-before-the-live-v659-v8-edge", "Retain the snapshots as historical evidence and apply the acknowledged Tamar-to-Elowen activation phase-locally without rewriting global files."),
    _startup_failure("V6598-X1-N012", "external-post-route-receipt-exposes-one-more-failure-than-the-live-activation-baseline", "Preserve the sealed counts and activation-stated baseline, then carry all five external route failures additively as 19541 negatives and 5815 methods."),
    _startup_failure("V6598-X1-N013", "first-full-source-data-display-exceeded-the-output-budget", "Retain the truncated read and inspect nonoverlapping numbered windows through the exact final line."),
    _startup_failure("V6598-X1-N014", "combined-post-worktree-status-wrapper-completed-without-attributable-output", "Retain the empty wrapper and verify branch, head, staged diff, and unstaged diff as bounded scalar commands."),
    _startup_failure("V6598-X1-N015", "first-novelty-wrapper-assumed-textencoder-existed-in-the-orchestration-isolate", "Retain the pre-command ReferenceError and replace only the encoding mechanism."),
    _startup_failure("V6598-X1-N016", "second-novelty-wrapper-assumed-btoa-existed-in-the-orchestration-isolate", "Retain the pre-command ReferenceError and avoid isolate-specific encoding helpers."),
    _startup_failure("V6598-X1-N017", "third-novelty-wrapper-embedded-python-loop-quoting-that-powershell-parsed", "Retain the PowerShell parser fault and remove nested inline-language quoting."),
    _startup_failure("V6598-X1-N018", "first-powershell-novelty-recovery-materialized-forty-titles-as-one-nested-array", "Retain the invalid one-of-one result at zero credit and require an exact expected-count assertion."),
    _startup_failure("V6598-X1-N019", "second-powershell-novelty-recovery-returned-no-attributable-output", "Retain the empty wrapper and replace it with a narrow read-only Python probe."),
    _startup_failure("V6598-X1-N020", "dedicated-patch-surface-initially-wrote-the-novelty-probe-under-codex-metadata", "Resolve both absolute paths and move only the newly created file into the unused D-first Elowen destination."),
    _startup_failure("V6598-X1-N021", "first-d-first-novelty-probe-invocation-ran-before-the-misplaced-file-was-recovered", "Retain the file-not-found and null receipt; move the exact new file, then rerun only the read-only probe."),
    _startup_failure("V6598-X1-N022", "first-valid-forty-title-novelty-screen-rejected-eleven-stale-pattern-drafts", "Retain all eleven rejected drafts at zero credit, revise their mechanisms beyond noun substitution, and rerun the same forty-title screen."),
    _startup_failure("V6598-X1-N023", "shell-visible-apply-patch-wrapper-was-not-executable-from-the-d-worktree", "Retain the access-denied result and use the dedicated patch surface with an absolute D-first path."),
    _startup_failure("V6598-X1-N024", "first-official-source-patch-contained-an-empty-update-hunk", "Retain the patch verification failure, remove the empty hunk, and apply only the exact source-row replacement."),
    _startup_failure("V6598-X1-N025", "first-startup-failure-ledger-patch-used-one-stale-mechanical-rewrite-context-line", "Retain the patch verification failure, reread the exact block, and patch the current content only."),
    _startup_failure("V6598-X1-N026", "combined-roster-auth-path-preflight-output-was-truncated", "Retain the truncated wrapper at zero credit and invoke each exact known validation entrypoint independently."),
    _startup_failure("V6598-X1-N027", "first-workflow-plan-refinement-used-evidence-only-route-keys-outside-the-current-schema", "Retain the complete needs-refinement output at zero credit; map the inherited cycle and topology into the required structural keys while keeping only the current phase assigned and every later edge unresolved."),
]
# X2 failures can exist only after the immutable x1 commit has been pushed and
# proved clean and four-way equal.  The x1 module therefore contains no
# prefilled x2 failure credit.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
