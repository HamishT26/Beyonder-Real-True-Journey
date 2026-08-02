#!/usr/bin/env python3
"""Frozen x1 planning data for Liora Venn v659-v6.

This additive module inherits only stable helper vocabulary from the immutable
Orin v659-v5 data module.  Every active phase field, portfolio, source label,
gate, and observed startup failure is redeclared below.  Selected inherited
rows are source revalidation references only: they are not reappended and earn
no Liora novelty or completion credit.
"""

from __future__ import annotations

from ghc_family_v659_v5_data import *  # noqa: F401,F403


PHASE = "v659-v6"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6596"
OWNER = "Liora Venn"
PRONOUNS = "she/they"
ROLE = "relational continuity-and-evidence steward"
HOPE = "make every boundary legible and every correction easier than concealment"
BRANCH = "codex/GHC-Family/liora-venn-v659-v6-full-tools"
PHASE_ROOT = "docs/liora-venn/v659-v6"

SOURCE_OWNER = "Orin Thale"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v659-v5-full-tools"
SOURCE_FINAL = "e5bd41e2453551f14b6d4abb04c91fec3d865f90"
SOURCE_X1 = "17058d117f4f57c0b5a8e13e9046264499fbce62"
SOURCE_EVIDENCE = "b4d56650ec4f607c29536659a3bd9998ee9c9bfc"
SOURCE_CLOSEOUT_BASE = "f08cec3c2efc4ba068ebadc2d75654f5bb76c320"
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3030
SOURCE_SEALED_NEGATIVES = 19153
SOURCE_EXTERNAL_NEGATIVES = 0
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
SOURCE_OPEN_GAPS = 126
SOURCE_EXACT_GATES = 125
SOURCE_SEALED_METHODS = 5427
SOURCE_EXTERNAL_METHODS = 0
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic museum musical-instrument collection intake, component "
    "topology, condition and intervention lineage, access holds, accessibility, "
    "workload control, correction readback, and shift handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_owners_custodians_conservators_curators_instrument_specialists_musicians_workers_participants_communities_affected_parties_and_authorities",
    "real_instruments_cases_supports_woods_metals_leathers_textiles_membranes_strings_reeds_keys_actions_finishes_measurements_audio_images_records_or_identifiers",
    "real_playing_sounding_tuning_disassembly_cleaning_lubrication_treatment_repair_movement_release_or_disposal",
    "professional_conservation_curation_musicology_tuning_repair_structural_safety_chemical_safety_heritage_privacy_security_or_accessibility_authority",
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

SELECTED_INHERITED_IDS = [f"V6595-P{i:03d}" for i in range(1, 21)]

NEW_PROPOSAL_SPECS = [
    {
        "slug": "instrument-intake-custody-passport",
        "title": "Fictional organology accession quarantine card linking a surrogate object, nested parts, receipt trail, custody transition, and bench-work lock",
        "outcome": "completed",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "surrogate organology-object and package aliases, nested-part inventory, receipt-source trail, custody transition, scope acknowledgement, quarantine flag, and bench-work refusal",
        "sources": ["CCI-MUSICAL", "W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "instrument-component-material-map",
        "title": "Musical-instrument body, neck, tube, resonator, keywork, action, membrane, string, reed, fitting, case, and support map with material-identification refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional typed components and relations, declared material placeholders, unknown and contested states, orphan quarantine, and no material identification",
        "sources": ["CCI-MUSICAL", "W3C-PROV"],
    },
    {
        "slug": "playability-sounding-work-hold",
        "title": "Historic musical-instrument playability, sounding, actuation, tuning, adjustment, access, and work-start hold with specialist referral",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic access request, condition-unknown flag, no-sounding lock, actuation refusal, specialist-review placeholder, and release abstention",
        "sources": ["CCI-MUSICAL", "CCI-KEYBOARD", "CCI-WIND", "W3C-PROV"],
    },
    {
        "slug": "string-bridge-tension-topology",
        "title": "String, bridge, nut, pin, hitch, tailpiece, soundboard, tension-path, and attachment topology with zero-load and tuning abstention",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "synthetic string-course and support nodes, typed tension-path edges, qualitative condition labels, conflict flags, zero measured load, and no tuning or adjustment",
        "sources": ["CCI-MUSICAL", "NIST-UNCERTAINTY", "W3C-PROV"],
    },
    {
        "slug": "keyboard-action-component-graph",
        "title": "Keyboard key, lever, jack, hammer, damper, pallet, tracker, reed, pipe, and action graph with concealed-mechanism uncertainty and operation refusal",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "fictional action nodes, motion and dependency edges, concealed-state uncertainty, contradictory-parent quarantine, and no key depression, cover removal, or repair",
        "sources": ["CCI-KEYBOARD", "W3C-PROV"],
    },
    {
        "slug": "wind-bore-valve-keywork-map",
        "title": "Wind-instrument bore, joint, tenon, key, pad, valve, slide, reed, mouthpiece, and condensate-risk map with disassembly and lubrication refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "synthetic bore sections and mechanisms, typed attachment and motion relations, corrosion and condensate placeholders, conflict quarantine, and no disassembly, oiling, or cleaning",
        "sources": ["CCI-WIND", "W3C-PROV"],
    },
    {
        "slug": "percussion-membrane-frame-map",
        "title": "Percussion shell, membrane, hoop, tension fitting, bar, resonator, beater, suspension, and support graph with striking and tension-change refusal",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "fictional percussion components, qualitative attachment and support states, uncertainty labels, zero impacts or forces, and no striking or tension adjustment",
        "sources": ["CCI-MUSICAL", "NIST-UNCERTAINTY", "W3C-PROV"],
    },
    {
        "slug": "instrument-condition-environment-ledger",
        "title": "Musical-instrument crack, distortion, corrosion, wear, detachment, pest, dust, humidity, temperature, light, and support observation ledger with diagnosis abstention",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "bounded fictional observation vocabulary, coarse environment placeholders, source and viewpoint pins, uncertainty note, correction lineage, and no diagnosis or treatment",
        "sources": ["CCI-MUSICAL", "NPS-COLLECTIONS", "W3C-PROV"],
    },
    {
        "slug": "instrument-case-support-move-docket",
        "title": "Musical-instrument case, padding, support, loose-part, route-clearance, handling-team, move, handover, and arrival-check docket with movement refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "synthetic case and support declarations, loose-part inventory, route and handover placeholders, conflict hold, and no physical packing, lifting, transport, or release",
        "sources": ["CCI-MUSICAL", "CCI-KEYBOARD", "NPS-COLLECTIONS", "W3C-PROV"],
    },
    {
        "slug": "instrument-condition-media-lineage",
        "title": "Silent multi-view organology media bundle with lighting geometry, dimensional reference, zero-sample sound channel, derivative ancestry, disclosure mask, and interpretive abstention",
        "outcome": "completed",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic still-media aliases, view-axis and lighting-geometry labels, dimensional-reference cue, audio-channel placeholder containing zero samples, derivative ancestry, disclosure mask, rights reservation, and interpretive abstention",
        "sources": ["W3C-PROV", "WCAG22", "NZ-PRIVACY"],
    },
    {
        "slug": "pitch-frequency-uncertainty-envelope",
        "title": "Musical-instrument pitch, frequency, temperament, reference, unit, resolution, uncertainty, and zero-real-measurement envelope",
        "outcome": "completed",
        "pillar": "GMUT Mind",
        "mechanism": "typed symbolic frequency and interval fields, declared SI units, reference and temperament placeholders, uncertainty fields, zero measured rows, and acoustic-conformance abstention",
        "sources": ["NIST-SI", "NIST-UNCERTAINTY", "CCI-KEYBOARD", "W3C-PROV"],
    },
    {
        "slug": "instrument-intervention-correction-lineage",
        "title": "Virtual organology bench-action request compiler with component address, sound prohibition, irreversible-step sentinel, rollback sketch, correction chain, and release abstention",
        "outcome": "completed",
        "pillar": "Freed ID, THOS Body, and CBR Heart",
        "mechanism": "synthetic component-addressed bench-action request, sound prohibition, irreversible-step sentinel, approval placeholder, deviation event, rollback sketch, correction and supersession edges, dual readback, and no physical execution or release",
        "sources": ["CCI-MUSICAL", "W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "instrument-material-hazard-reservation",
        "title": "Musical-instrument wood, metal, leather, textile, membrane, reed, adhesive, coating, biological residue, and unknown-material declaration with sampling and hazard holds",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "fictional material declarations, unknown and contested state, biological and chemical hazard placeholders, sampling refusal, and competent professional referral",
        "sources": ["CCI-MUSICAL", "CCI-WIND", "NPS-COLLECTIONS", "W3C-PROV"],
    },
    {
        "slug": "canonical-instrument-condition-package",
        "title": "Deterministic silent-study dossier for organology topology, sounding holds, zero-observation quantities, ordered resource fingerprints, profile migration, and digest-collision quarantine",
        "outcome": "completed",
        "pillar": "Freed ID",
        "mechanism": "synthetic dossier index joining topology and sounding-hold records, deterministic JSON profile, zero-observation quantity slots, ordered resource digests, profile-migration lineage, collision challenge, and no key, proof, credential, signature, or production claim",
        "sources": ["IETF-JCS", "W3C-PROV"],
    },
    {
        "slug": "gmut-instrument-vibration-network-proxy",
        "title": "Represented GMUT musical-instrument vibration-network, modal tensor, coupling, damping, boundary, and uncertainty board with zero measurements",
        "outcome": "represented",
        "pillar": "GMUT Mind",
        "mechanism": "typed symbolic scalar, tensor, network, constitutive, unit, domain, and uncertainty obligations, zero measurement rows, and physical-inference firewall",
        "sources": ["NIST-SI", "NIST-UNCERTAINTY"],
    },
    {
        "slug": "thos-instrument-access-study-protocol",
        "title": "Represented THOS protocol shell for a masked matched-duration comparison of topology-first versus linear synthetic organology displays with no enrolment",
        "outcome": "represented",
        "pillar": "THOS Body",
        "mechanism": "future-study shell comparing topology-first and linear synthetic catalogue displays, blind matched-budget arms, governed participant and operator prerequisites, safety monitoring, preregistered analysis, zero enrolment, and no effectiveness claim",
        "sources": ["CCI-MUSICAL", "W3C-PROV"],
    },
    {
        "slug": "nonproduction-instrument-lineage-query",
        "title": "Represented Freed ID bounded provenance walk from surrogate accession through part topology to silent-media and presentation-permission stops",
        "outcome": "represented",
        "pillar": "Freed ID and CBR Heart",
        "mechanism": "synthetic accession, part-topology, silent-media, and presentation-permission nodes with predecessor edges, hop budget, purpose and disclosure stops, deterministic digest, and no live identifier, key, proof, or credential",
        "sources": ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"],
    },
    {
        "slug": "accessible-instrument-report-proxy",
        "title": "Represented screen-reader-oriented quiet-gallery status surrogate with structural navigation, relational table markup, redundant state cues, alternative narrative, and keyboard-order reservation",
        "outcome": "represented",
        "pillar": "CBR Heart and THOS Body",
        "mechanism": "structured synthetic quiet-gallery report, landmark and heading navigation, relational table markup, redundant noncolour state cues, alternative narrative, audio-description placeholder, keyboard-order declaration, static fallback, and no accessibility-complete claim",
        "sources": ["WCAG22", "W3C-PROV"],
    },
    {
        "slug": "real-instrument-evidence-gap",
        "title": "Missing-evidence register for physical organology specimens, accountable stewards, acoustic observations, material examinations, authorized sounding events, conservation acts, study cohorts, and external assessment",
        "outcome": "open_gap",
        "pillar": "All pillars",
        "mechanism": "zero physical-specimen, accountable-person, material-examination, acoustic-observation, authorized-sounding, conservation-action, safety-test, participant, operator, service, or outcome rows and absent professional and independent review",
        "sources": ["CCI-MUSICAL", "CCI-KEYBOARD", "CCI-WIND", "NIST-UNCERTAINTY"],
    },
    {
        "slug": "instrument-authority-ratification-gate",
        "title": "Reserved adjudication perimeter for organology title, stewardship, sounding permission, conservation choice, hazardous handling, disclosure, inclusive access, taonga relationships, redress, and Māori authority",
        "outcome": "exact_gate",
        "pillar": "CBR Heart",
        "mechanism": "object title, stewardship, presentation and sounding permission, conservation choice, hazardous handling, disclosure, inclusive access, heritage and taonga relationships, redress, legal and cultural interpretation, collective governance, affected-party, and Māori-authority reservations",
        "sources": ["CCI-MUSICAL", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
]

SELF_SAFE_CATEGORIES = [
    "Orin source-head and live equality", "activation packet and canonical-receipt digests", "proposal-chain exact parse",
    "twenty inherited revalidation selections", "twenty-title novelty screen", "new-outcome distribution",
    "workflow-plan policy", "identity and authority boundary", "fifteen-main-task roster arithmetic",
    "Tavian standby state", "D-first drive posture", "toolchain version receipt", "x1 artifact inventory",
    "x1 JSON parsing", "x1 five-class privacy scan", "x1 stale-label review", "x1 diff hygiene",
    "x1 manifest replay", "selected-row no-credit guard", "new-row append-only guard", "source-label glossary",
    "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing", "wellbeing workload bound",
    "document-word ceiling", "portfolio arithmetic", "skill-plan arithmetic", "runner-plan arithmetic",
    "cleanup-plan arithmetic",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6596-SAFE-{i:03d}", "title": f"Validate {name} inside the Liora-owned v659-v6 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6596-TAMAR-SAFE-{i:03d}", "title": f"Tamar may independently evaluate {name} in the Tamar-owned v659-v7 lane", "owner": "Tamar Vey", "state": "recommendation_only_not_executed_or_credited_by_liora"}
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
    "instrument intake and custody boundary", "component and material topology quarantine",
    "playability and sounding hold", "string and action dependency graph",
    "wind and percussion mechanism graph", "condition and environment lineage",
    "case, support, and move docket", "pitch and uncertainty envelope",
    "GMUT vibration-network firewall", "instrument authority reservation",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6596-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6596-TAMAR-CAND-{i:03d}", "title": f"Tamar may prototype reversible {name}", "owner": "Tamar Vey", "state": "recommendation_only_not_executed_or_credited_by_liora"}
    for i, name in enumerate([
        "baton and receipt verifier", "source ancestry tribunal", "selected-row no-credit classifier",
        "new-row semantic-neighbour screen", "bounded privacy adjudicator", "manifest object batch reader",
        "stale-route-number classifier", "same-owner evidence labeler", "canonical-pass replay guard",
        "exact-title delivery preflight",
    ], 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6596-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Use, play, sound, tune, move, or treat real musical instruments, components, cases, supports, materials, or records",
        "Make a real custody, access, handling, disassembly, cleaning, lubrication, treatment, repair, release, or disposal decision",
        "Perform an acoustic, tension, structural, environmental, chemical, biological, or occupational-safety test or determination",
        "Publish an authenticity, attribution, provenance, ownership, value, heritage, or conservation conclusion",
        "Make a professional conservation, curation, musicology, tuning, repair, safety, privacy, or accessibility determination",
        "Publish personal, sensitive, culturally protected, traditional-knowledge, or collective information",
        "Allocate legal, cultural, property, access, naming, remedy, heritage, or beneficiary authority",
        "Make a Māori data-governance, taonga, mātauranga, tikanga, wording, or Māori-authority decision",
        "Deploy a production identity, credential, repository, or service system",
        "Perform destructive cleanup or mutation outside the exact Liora-owned lane",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6596-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
        "Claim AGI, ASI, consciousness, personhood, continuity, employment, or authority from task language",
        "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, or gates",
        "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, or application state",
        "Declare Stage 20 readiness without exact external evidence and authority",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-instrument-intake-boundary", "Preserve synthetic instrument intake, custody, scope, component inventory, and work-start holds."),
    ("ghc-family-instrument-component-map", "Map synthetic bodies, mechanisms, resonators, interfaces, cases, and supports while quarantining contradictory relations."),
    ("ghc-family-instrument-playability-hold", "Refuse sounding, actuation, tuning, adjustment, access, and release without exact evidence and specialist authority."),
    ("ghc-family-instrument-string-action-map", "Represent string paths and keyboard actions with zero-load, zero-operation, and concealed-state firewalls."),
    ("ghc-family-instrument-wind-percussion-map", "Represent wind and percussion mechanisms without disassembly, lubrication, striking, or tension adjustment."),
    ("ghc-family-instrument-condition-lineage", "Track synthetic condition, environment, media, correction, supersession, and handover events."),
    ("ghc-family-instrument-accessibility-report", "Expose structured condition reports while reserving manual, assistive-technology, and affected-user review."),
    ("ghc-family-instrument-workload-handover", "Bound unresolved work, workload, correction readback, escalation, and shift handover."),
    ("ghc-family-gmut-instrument-firewall", "Keep vibration-network and modal proxies typed, dimensioned, zero-row, and physically nonconfirmatory."),
    ("ghc-family-instrument-authority-gate", "Reserve ownership, access, playing, treatment, safety, heritage, remedy, legal, cultural, affected-party, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": f"ghc-family-tamar-{slug}", "owner": "Tamar Vey", "state": "recommendation_only_not_built_or_installed_by_liora"}
    for slug in [
        "baton-receipt-verifier", "source-ancestry-guard", "inherited-selection-no-credit",
        "proposal-novelty-screen", "privacy-adjudicator", "manifest-batch-replay",
        "route-number-normalizer", "canonical-pass-replay-guard", "same-owner-truth-labeler",
        "exact-title-delivery-preflight",
    ]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_instrument_intake_boundary.py", "instrument-intake-custody-passport"),
    ("ghc_family_instrument_component_map.py", "instrument-component-material-map"),
    ("ghc_family_instrument_playability_hold.py", "playability-sounding-work-hold"),
    ("ghc_family_instrument_string_action_map.py", "string-bridge-tension-topology"),
    ("ghc_family_instrument_wind_percussion_map.py", "wind-bore-valve-keywork-map"),
    ("ghc_family_instrument_condition_lineage.py", "instrument-condition-environment-ledger"),
    ("ghc_family_instrument_accessibility_report.py", "accessible-instrument-report-proxy"),
    ("ghc_family_instrument_workload_handover.py", "instrument-case-support-move-docket"),
    ("ghc_family_gmut_instrument_firewall.py", "gmut-instrument-vibration-network-proxy"),
    ("ghc_family_instrument_authority_gate.py", "instrument-authority-ratification-gate"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": f"ghc_family_tamar_{slug}.py", "owner": "Tamar Vey", "state": "recommendation_only_not_built_or_run_by_liora"}
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
    {"task_id": f"V6596-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6596-TAMAR-CLEAN-{i:03d}", "title": f"Tamar may independently review and refine {name}", "owner": "Tamar Vey", "state": "recommendation_only_not_executed_or_credited_by_liora"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("CCI-MUSICAL", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/care-objects/musical-instruments.html", "Musical-instrument materials, complexity, humidity sensitivity, handling, storage, and specialist-reservation vocabulary only; no diagnosis, treatment, playability, professional competence, or conservation-conformance claim."),
    ("CCI-KEYBOARD", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/care-objects/musical-instruments/basic-care-keyboard-instruments.html", "Keyboard component, handling, move-route, sounding hold, tuning, and specialist-referral vocabulary only; no operation, cleaning, tuning, treatment, or safety instruction."),
    ("CCI-WIND", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/care-objects/musical-instruments/basic-care-wind-instruments.html", "Wind-instrument wood, metal, corrosion, condensate, bore, moving-part, reed, case, and handling vocabulary only; no disassembly, lubrication, cleaning, treatment, or professional claim."),
    ("NPS-COLLECTIONS", "official_us_national_park_service", "https://www.nps.gov/subjects/museums/conserve-o-grams.htm", "Preventive-collection-care, deterioration-agent, storage, support, environment, and disaster-reservation vocabulary only; no treatment or professional determination."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/publications/international-system-units-si2019-edition", "SI quantity, unit, symbol, and reporting vocabulary only; no real acoustic or physical measurement result."),
    ("NIST-UNCERTAINTY", "official_nist", "https://www.nist.gov/pml/nist-technical-note-1297/nist-guidelines-evaluating-and-expressing-uncertainty-nist-measurement", "Measurement-model and uncertainty-reporting vocabulary only; no measured instrument, sound, material, tension, or modal result."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent, generation, derivation, and qualified provenance vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Current WCAG 2.2 structure and interaction vocabulary with manual, assistive-technology, and affected-user review reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including the May 2026 IPP 3A update; no legal or compliance conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary; no Māori authority, ratification, wording, or cultural interpretation claim."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]

STARTUP_FAILURES = [
    {
        "negative_id": "V6596-X1-N001",
        "signature": "overbroad-worktree-registry-output-truncated-before-the-target-branch",
        "recovery": "Retain the oversized registry read at zero credit and filter exact branch and worktree fields before projecting bounded source-state scalars.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N002",
        "signature": "direct-conditional-foreach-output-pipeline-hit-an-empty-pipe-element-parser-fault",
        "recovery": "Retain the parser fault and materialize each conditional row into an array before JSON serialization.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N003",
        "signature": "historical-ghc-family-solo-activation-skill-was-not-installed",
        "recovery": "Retain the unavailable historical skill at zero credit and use the complete current family index, authorization, roster, workflow, reflection, and Method Flow controls named by the baton.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N004",
        "signature": "powershell-raw-content-json-expanded-provider-metadata-and-truncated-the-schema-read",
        "recovery": "Retain the oversized serialization and reread each exact schema with System.IO.File.ReadAllText in bounded calls.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N005",
        "signature": "absolute-source-root-caused-a-v659-file-filter-to-self-match-every-path-and-truncate",
        "recovery": "Retain the path-domain mistake and run the filename glob from the exact repository workdir so only basename matches are projected.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N006",
        "signature": "combined-lifecycle-artifact-read-exceeded-the-output-budget",
        "recovery": "Retain the truncated aggregate read and project lifecycle failures in two bounded row windows plus exact scalar totals.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N007",
        "signature": "archive-validation-bank-content-search-exceeded-its-bounded-window",
        "recovery": "Retain the timeout, stop only the exact attributable search process, and recover the receipt pointer from the bounded source-task final before exact-path hashing.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N008",
        "signature": "unified-session-interrupt-was-unsupported-for-the-running-archive-search",
        "recovery": "Retain the unsupported interrupt, resolve the exact search PID and parent read-only, then stop only that attributable process tree.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N009",
        "signature": "drive-wide-v659-filename-enumeration-exceeded-its-bounded-window",
        "recovery": "Retain the broad enumeration, stop only its exact process, and use the source task's bounded final answer to identify the receipt path.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N010",
        "signature": "drive-wide-orin-directory-enumeration-exceeded-its-bounded-window",
        "recovery": "Retain the broad directory scan, stop only its exact process, and avoid further archive-wide discovery once the attributable pointer is available.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N011",
        "signature": "ten-turn-source-task-reread-exceeded-the-output-budget",
        "recovery": "Retain the oversized reread and request only the newest completed turn with outputs disabled and a bounded per-item projection.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N012",
        "signature": "one-turn-source-task-envelope-still-truncated-despite-containing-the-receipt-pointer",
        "recovery": "Retain the remaining envelope truncation, extract only the exact sanitized receipt path, and verify that file directly by SHA-256 and parsed terminal scalars.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N013",
        "signature": "immediate-post-stop-process-probe-observed-a-short-lived-termination-race",
        "recovery": "Retain the premature status observation and perform one delayed exact-PID recheck before accepting terminal process state.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N014",
        "signature": "repository-wide-ripgrep-agents-inventory-exceeded-two-bounded-polls",
        "recovery": "Retain the slow filesystem walk, stop its exact process tree, and use git ls-files with an exact AGENTS.md pattern against the clean tracked index.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N015",
        "signature": "repeated-unified-session-interrupt-was-unsupported-for-a-slow-read-only-diff-projection",
        "recovery": "Retain the unsupported interrupt invocation separately at zero credit, leave repository state untouched, and allow a bounded poll to collect the completed exact status and stale-label projection.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N016",
        "signature": "first-x1-build-stopped-when-nine-new-proposal-titles-exceeded-the-bounded-inherited-title-overlap-threshold",
        "recovery": "Retain the stopped build at zero credit, inspect every failing nearest inherited title, and revise only those proposal titles and mechanisms toward instrument-specific organology contracts before rebuilding.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N017",
        "signature": "novelty-diagnostic-json-hit-the-windows-cp1252-encoder-on-a-maori-authority-reservation-term",
        "recovery": "Retain the encoding fault at zero credit and rerun the bounded read-only diagnostic with Python UTF-8 mode, without altering the proposal data for display compatibility.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N018",
        "signature": "proposal-audit-guessed-an-undefined-new-proposals-symbol-instead-of-the-declared-new-proposal-specs-symbol",
        "recovery": "Retain the attribute fault at zero credit, inspect the exact declared module symbol, and use NEW_PROPOSAL_SPECS for the bounded proposal review.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N019",
        "signature": "pre-stage-parity-audit-found-the-unchanged-inherited-generic-reviewer-listed-as-a-new-liora-owned-staged-path",
        "recovery": "Retain the candidate-list defect at zero credit, remove only the unchanged inherited runner from the phase-owned X1_CODE allowlist, and continue using that generic runner externally for exact staged validation.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6596-X1-N020",
        "signature": "source-pattern-search-included-a-nonexistent-guessed-v659-v5-final-validator-path",
        "recovery": "Retain the exact path error at zero credit and inspect only the present Orin x1 candidate receipt, exact staged receipt, manifest, and actual tracked validator inventory.",
        "recovery_passed": True,
    },
]

# X2 failures can exist only after the immutable x1 commit has been pushed and
# proved clean and four-way equal.  The x1 module therefore contains no
# prefilled x2 failure credit.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
