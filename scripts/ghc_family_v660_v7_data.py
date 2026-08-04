#!/usr/bin/env python3
"""Frozen x1 planning data for Ilyra Fen v660-v7.

Lyren Moss's immutable v660-v6 surface supplies compatibility vocabulary only.
Twenty inherited rows are selected for bounded revalidation with zero Lyren
novelty or completion credit. Only the twenty new rows below extend the
append-only proposal chain. All physical, participant, professional, empirical,
production, legal, cultural, accessibility-complete, privacy-complete, and Māori
authority lanes remain empty or exact-gated.
"""

from __future__ import annotations

from ghc_family_v660_v6_data import *  # noqa: F401,F403


PHASE = "v660-v7"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6607"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary steward and permutation-obligation keeper"
HOPE = (
    "leave every synthetic row, change, method assertion, composition claim, "
    "correction, refusal, and authority gate traceable without converting notation "
    "or software structure into ringing skill, performance truth, safety, ownership, "
    "cultural legitimacy, or Māori authority"
)
BRANCH = "codex/GHC-Family/ilyra-fen-v660-v7-full-tools"
PHASE_ROOT = "docs/ilyra-fen/v660-v7"

SOURCE_OWNER = "Lyren Moss"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v660-v6-full-tools"
SOURCE_BASE = "050fd7559df40bc08f990fc26a8636636e520a3a"
SOURCE_X1 = "ec19bf7f868be7a040b5305f1f8f113062674fb6"
SOURCE_EVIDENCE = "b883d9239074b38c6e92c30859e2d0b442ed2985"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "6be1e90e55854f6e0dc0faeb38621b6086f4e688"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "bc0074b32cb5ee4921a1daa9005230bb71e01b0c74a630b208e2b3da6ab9f682"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED"
ACTIVATION_PACKET_SHA256 = (
    "75695fb04fae5214f8d5cdf8eed463901881b9dac6bacd21298c90b09fe9b1bc"
)
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3250
SOURCE_SEALED_NEGATIVES = 20594
SOURCE_EXTERNAL_NEGATIVES = 1
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 20595
SOURCE_OPEN_GAPS = 135
SOURCE_EXACT_GATES = 134
SOURCE_SEALED_METHODS = 6388
SOURCE_EXTERNAL_METHODS = 1
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6389
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic change-ringing notation and rehearsal handover: stage and row "
    "identity, adjacent changes, place notation, lead and method lineage, composition "
    "obligations, correction readback, accessible review, workload holds, provenance, "
    "privacy minimisation, rights reservation, and cultural and Māori non-substitution"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_bells_handbells_towers_rope_wheels_frames_clappers_fittings_simulators_venues_methods_compositions_performances_or_records",
    "real_ringers_learners_conductors_composers_steeplekeepers_tower_captains_clergy_owners_communities_affected_parties_and_authorities",
    "real_bell_handling_ringing_calling_conducting_teaching_maintenance_inspection_access_performance_publication_or_record_submission",
    "professional_ringing_composition_proving_instruction_safeguarding_tower_safety_engineering_conservation_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "performance_attribution_personal_data_safeguarding_venue_access_religious_heritage_community_traditional_knowledge_and_collective_interest",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_religious_naming_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_takedown_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6606-P{i:03d}" for i in range(1, 21)]


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
        "campanology-packet-identity",
        "Surrogate change-ringing dossier identity capsule with stage, bell-token alphabet, revision, source pin, and ringing refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic dossier and revision tokens, declared stage, bell-token alphabet, source pin, correction, tombstone, and zero-physical-ringing states",
        ["CCCBR-FMR-ED3", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "campanology-row-permutation-ledger",
        "Stage-bounded ringing-row permutation ledger with uniqueness, rounds, duplicate-bell, missing-bell, and foreign-token quarantine",
        "completed",
        "GMUT Mind and Freed ID",
        "typed synthetic rows over a declared stage and alphabet with bijection, rounds, duplicate, missing, foreign-token, unknown, and no-performance guards",
        ["CCCBR-FMR-ED3", "JSON-SCHEMA-2020-12", "IETF-JCS"],
    ),
    _proposal(
        "campanology-change-transition",
        "Adjacent and identity change transition tribunal with made-place, swapped-pair, source-row, result-row, and mismatch retention",
        "completed",
        "GMUT Mind",
        "synthetic source and result rows, made places, adjacent swaps, identity changes, mismatch witnesses, correction lineage, and physical-motion abstention",
        ["CCCBR-PLACE-NOTATION", "JSON-SCHEMA-2020-12", "W3C-PROV"],
    ),
    _proposal(
        "campanology-place-notation-parser",
        "Place-notation expansion and normalization contract for cross changes, external-place inference, symmetry markers, separators, and parse refusal",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic place-notation tokens, stage context, cross and external-place expansion, symmetry marker, separator, round-trip digest, ambiguity, and parse refusal",
        ["CCCBR-PLACE-NOTATION", "JSON-SCHEMA-2020-12", "IETF-JCS"],
    ),
    _proposal(
        "campanology-lead-course-block-graph",
        "Lead, lead-head, course, block, splice, and method-change dependency graph with cycle and incomplete-boundary quarantine",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic leads, lead heads, courses, blocks, method boundaries, splice edges, prerequisites, incomplete nodes, cycles, and no-ringing declaration",
        ["CCCBR-FMR-ED3", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "campanology-method-assertion-braid",
        "Method definition, class, stage, title, library-status placeholder, source, contestation, and supersession assertion braid",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic method assertions, class and stage placeholders, source status, title claim, library-state unknown, contradiction, retraction, correction, and naming-authority abstention",
        ["CCCBR-FMR-ED3", "CCCBR-TECHNICAL-TAXONOMY", "W3C-PROV"],
    ),
    _proposal(
        "campanology-composition-truth-board",
        "Touch and composition truth-obligation board with row count, repeated-row witness, rounds closure, call position, and proof-status refusal",
        "completed",
        "GMUT Mind",
        "synthetic composition rows, declared length, repeated-row witness, rounds start and finish, call positions, incomplete expansion, counterexample slot, and official-proof refusal",
        ["CCCBR-FMR-ED3", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "campanology-call-correction-lineage",
        "Call, calling-position, method-change, correction, supersession, readback, and unresolved-ambiguity lineage",
        "completed",
        "THOS Body and Freed ID",
        "synthetic calls, calling positions, method changes, conductor placeholder, correction, supersession, readback, ambiguity hold, cancellation, and no-conducting state",
        ["CCCBR-FMR-ED3", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "campanology-performance-record-provenance",
        "Synthetic ringing-performance record provenance covenant with venue and band placeholders, method or composition claim, correction, privacy mask, and publication refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic venue and band placeholders, method and composition assertions, date and duration placeholders, correction, disclosure mask, consent and privacy holds, and publication refusal",
        ["BELLBOARD", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "campanology-bitemporal-memory",
        "Bitemporal method, composition, call, performance-claim, correction, retraction, tombstone, and non-erasure memory",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic assertion and record intervals, predecessor links, correction, retraction, supersession, tombstone, contradiction retention, and record-erasure refusal",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "campanology-timing-uncertainty",
        "Row-interval, lead-duration, striking-offset placeholder, SI unit, resolution, covariance, missingness, and uncertainty envelope",
        "completed",
        "GMUT Mind",
        "typed synthetic time and offset placeholders, SI units, resolution, covariance, uncertainty, missingness, zero observations, and striking-quality firewall",
        ["BIPM-SI", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-campanology-permutation-obligations",
        "GMUT permutation-group, generator, orbit, stabilizer, parity, closure, and observation-firewall obligation board",
        "completed",
        "GMUT Mind",
        "typed symbolic permutations, generators, composition order, inverse, identity, orbit and stabilizer placeholders, parity, closure, units, and zero physical observations",
        ["CCCBR-PLACE-NOTATION", "BIPM-SI", "IETF-JCS"],
    ),
    _proposal(
        "campanology-physical-action-firewall",
        "Bell handling, ringing, calling, teaching, tower access, maintenance, and safety-action authorization firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic action request, local-risk-assessment placeholder, competent-person and tower-authority holds, safeguarding and access flags, stop token, and execution refusal",
        ["CCCBR-TOWER-SAFETY", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "campanology-canonical-package",
        "Canonical change-ringing documentation package with ordered row, notation, method, composition, correction, source, and profile digests",
        "completed",
        "Freed ID and THOS Body",
        "synthetic ordered dossier entries, profile version, normalized fields, row and notation digests, migration witness, collision quarantine, and no-key or credential declaration",
        ["IETF-JCS", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-campanology-striking-proxy",
        "GMUT bell-mode, rope-wheel, timing-coupling, damping, boundary, and uncertainty proxy with zero mechanical or acoustic observations",
        "represented",
        "GMUT Mind",
        "typed symbolic bell, wheel, rope, clapper, mode, timing and damping placeholders, boundary data, zero coefficients, zero likelihood rows, and physical-inference abstention",
        ["BIPM-SI", "CCCBR-TOWER-SAFETY", "IETF-JCS"],
    ),
    _proposal(
        "thos-campanology-rehearsal-handover",
        "THOS method-rehearsal queue, correction debt, workload ceiling, stop token, readback, escalation, and handover proxy",
        "represented",
        "THOS Body",
        "synthetic method and rehearsal queues, correction and ambiguity debt, workload ceilings, stop tokens, readback, escalation, acceptance digest, handover, and zero ringers or operators",
        ["CCCBR-FMR-ED3", "CCCBR-TOWER-SAFETY", "W3C-PROV"],
    ),
    _proposal(
        "campanology-comprehension-protocol",
        "Counterbalanced empty-session protocol comparing place-notation-first and row-path-first synthetic method explanations",
        "represented",
        "THOS Body",
        "future matched-budget synthetic dossiers, shuffled questions, equal action budgets, masked scoring, support and withdrawal rules, zero participants, and no learning-effect claim",
        ["WCAG22", "CCCBR-FMR-ED3", "W3C-PROV"],
    ),
    _proposal(
        "campanology-access-companion",
        "Nonvisual row, change, lead, call, and composition companion with linear traversal, redundant cues, keyboard path, print fallback, and manual-review reservation",
        "represented",
        "CBR Heart and THOS Body",
        "structural headings, row and change relations, linear traversal, noncolour cues, keyboard sequence, print fallback, language and tactile reservations, and zero affected-user sessions",
        ["WCAG22", "CCCBR-FMR-ED3", "W3C-PROV"],
    ),
    _proposal(
        "real-campanology-evidence-vault",
        "Real bells, towers, ringers, methods, compositions, performances, safety review, participant outcomes, and independent-assessment vault with zero-row refusal",
        "open_gap",
        "All pillars",
        "zero authenticated bells or towers, governed ringing sessions, accountable practitioners, measured mechanical or acoustic rows, participant outcomes, incident controls, or independent-review records",
        ["CCCBR-FMR-ED3", "CCCBR-TOWER-SAFETY", "BELLBOARD"],
    ),
    _proposal(
        "campanology-rights-cultural-authority",
        "Unoccupied mandate circuit for tower access, ringing consent, safeguarding, attribution, performance records, religious and heritage context, remedy, and Māori decision non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied tower-owner, clergy, safeguarding, ringer, composer, conductor, record, privacy, religious, heritage, community, takedown, remedy, tangata whenua, iwi, hapū, and Māori-authority reservations",
        ["CCCBR-TOWER-SAFETY", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Lyren source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-two-hundred-fifty-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level neighbor review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Lyren-to-Ilyra live edge",
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
    "no-x2-in-x1 guard",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6607-SAFE-{i:03d}", "title": f"Validate {name} inside the Ilyra-owned v660-v7 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6608-REC-SAFE-{i:03d}", "title": f"Reassess {name} for Auren-only v660-v8", "recipient": "Auren Lark", "completion_credit": 0}
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "stage-bounded row permutation ledger",
    "adjacent-change transition tribunal",
    "place-notation parser and normalizer",
    "lead-course-block dependency graph",
    "method assertion and contestation braid",
    "composition truth-obligation board",
    "call and correction lineage",
    "performance-record provenance covenant",
    "GMUT permutation obligation board",
    "ringing rights and cultural-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6607-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6608-REC-CAND-{i:03d}", "title": f"Consider a distinct Auren-owned refinement of {name}", "recipient": "Auren Lark", "completion_credit": 0}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6607-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Handle, ring, call, conduct, teach, inspect, maintain, repair, silence, sound, publish, or submit any real bell, tower, method, composition, performance, or record",
            "Make a real ringing-safety, tower-access, safeguarding, engineering, conservation, musical, performance-quality, or competence determination",
            "Use real ringers, learners, bands, towers, venues, ropes, bells, simulators, sensors, recordings, performance data, or personal information",
            "Disclose private attendance, safeguarding, health, access, keyholding, location, contact, performance, dispute, or restricted community information",
            "Make a professional composition-proof, method-classification, teaching, tower-management, privacy, security, translation, or accessibility determination",
            "Publish a production method, composition, performance assertion, identifier, credential, signed statement, proof, or interoperable ringing record",
            "Allocate title, authorship, composition credit, performance credit, access, ownership, custody, religious, heritage, takedown, remedy, or beneficiary authority",
            "Make a tikanga, mātauranga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, or Māori-authority decision",
            "Run a real participant study, rehearsal, ringing session, operator trial, professional review, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Ilyra-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6607-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
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
    ("ghc-family-campanology-row-validator", "Validate stage-bounded synthetic rows while preserving duplicate, missing, foreign-token, unknown, and no-performance states."),
    ("ghc-family-campanology-change-transition", "Check adjacent and identity change relations without claiming physical bell motion or ringing quality."),
    ("ghc-family-campanology-place-notation", "Parse and normalize bounded place notation with explicit stage, ambiguity, and refusal states."),
    ("ghc-family-campanology-lead-graph", "Represent lead, course, block, splice, dependency, cycle, and incomplete-boundary states."),
    ("ghc-family-campanology-method-assertion", "Retain method, class, title, source, contestation, correction, and naming-authority abstention."),
    ("ghc-family-campanology-composition-obligations", "Expose row-count, repeated-row, rounds-closure, call-position, and proof-refusal obligations."),
    ("ghc-family-campanology-call-lineage", "Preserve calls, calling positions, method changes, corrections, supersession, readback, and ambiguity holds."),
    ("ghc-family-campanology-record-provenance", "Track synthetic performance-record provenance, correction, minimisation, disclosure stop, and publication refusal."),
    ("ghc-family-gmut-campanology-permutation", "Preserve symbolic permutation, generator, inverse, orbit, stabilizer, parity, closure, and observation-firewall obligations."),
    ("ghc-family-campanology-rights-cultural-authority", "Keep tower, safeguarding, attribution, privacy, religious, heritage, remedy, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": name.replace("campanology", "successor-domain"), "recipient": "Auren Lark", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": name.replace("campanology", "successor_domain"), "recipient": "Auren Lark", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_RUNNER_SPECS
]

SELF_CLEAN_CATEGORIES = [
    "retain every inherited and current negative without folding it into a pass",
    "refresh count mirrors only from authoritative ledgers",
    "preserve Git-blob and logical-text hash-domain declarations",
    "pin UTF-8 before Unicode-emitting diagnostics",
    "split Windows probes into bounded scalar receipts",
    "keep expected-empty branch and remote checks null-safe",
    "preserve family-current callers and historical compatibility surfaces",
    "reject stale owner and phase labels in current-owner artifacts",
    "keep x1 immutable after its four-way-equality gate",
    "keep x2 implementation absent from x1",
    "keep exact and blocked packets visible and unexecuted",
    "keep real-world connector rows empty",
    "retain scanner candidates separately from confirmed payload hits",
    "scan only declared public owner surfaces across five classes",
    "refresh owner manifests after every additive lifecycle change",
    "verify deterministic JSON ordering and parsing",
    "verify proposal append-only arithmetic",
    "verify inherited revalidation receives zero novelty and completion credit",
    "verify outcome labels use only the four authorized states",
    "reserve manual and affected-user accessibility evaluation",
    "reserve legal, cultural, religious, safeguarding, and Māori authority",
    "reserve empirical GMUT and professional THOS claims",
    "reserve production Freed ID keys, proofs, status, recovery, and trust governance",
    "reserve privacy-complete and exhaustive-security claims",
    "keep every document under the declared word ceiling",
    "keep owner additions under the declared file ceiling",
    "verify source-to-final single-parent zero-merge ancestry",
    "hold terminal routing until exact final proof",
    "send no precontact or duplicate activation",
    "preserve NOT_READY_FOR_STAGE_20",
]
SELF_CLEAN_TASKS = [
    {"task_id": f"V6607-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6608-REC-CLEAN-{i:03d}", "title": title, "recipient": "Auren Lark", "completion_credit": 0}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("CCCBR-FMR-ED3", "official_central_council_framework", "https://framework.cccbr.org.uk/edition3/index.html", "Current living vocabulary for rows, changes, methods, calls, compositions, performances, classification, and records only; no method naming, record admission, ringing, or authority claim."),
    ("CCCBR-PLACE-NOTATION", "official_central_council_framework", "https://framework.cccbr.org.uk/version1/placenotation.html", "Place, cross-change, adjacent-change, sequence, symmetry, and abbreviation vocabulary only; no physical ringing or universal composition-proof claim."),
    ("CCCBR-TECHNICAL-TAXONOMY", "official_central_council", "https://cccbr.org.uk/about/workgroups/technical-and-taxonomy/", "Reference-standard, definitive-collection, consultation, and data-interchange boundary vocabulary only; no Central Council status or endorsement is claimed."),
    ("CCCBR-TOWER-SAFETY", "official_central_council", "https://runningatower.cccbr.org.uk/docs/healthsafety/riskassessment/", "Local risk-assessment, competent advice, hazard, control, access, and refusal vocabulary only; software cannot complete a tower risk assessment or authorize activity."),
    ("BELLBOARD", "primary_ringing_world_service", "https://www.bellboard.uk/", "Performance-record field and correction vocabulary only; zero records were queried, copied, submitted, validated, or treated as evidence."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("JSON-SCHEMA-2020-12", "primary_json_schema_project", "https://json-schema.org/draft/2020-12", "Schema, vocabulary, tuple, applicator, validation, annotation, and fail-closed structural vocabulary only."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, text alternative, noncolour, navigation, status, target, and interaction vocabulary with manual, assistive-technology, Māori-language, and affected-user evaluation reserved."),
    ("BIPM-SI", "official_bipm", "https://www.bipm.org/en/publications/si-brochure", "SI time, angle, frequency, quantity, unit, symbol, uncertainty-context, and reporting vocabulary only; no measurement, calibration, acoustic, mechanical, or performance result."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including indirect-collection notification context, only; no legal, compliance, collection, disclosure, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, or mātauranga claim."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "CCCBR-FMR-ED3": "living_current_edition3_checked_2026_08_04",
    "CCCBR-PLACE-NOTATION": "current_framework_appendix_checked_2026_08_04",
    "CCCBR-TECHNICAL-TAXONOMY": "current_checked_2026_08_04",
    "CCCBR-TOWER-SAFETY": "current_checked_2026_08_04",
    "BELLBOARD": "current_public_service_checked_2026_08_04_zero_rows_queried",
    "W3C-PROV": "stable_recommendation",
    "JSON-SCHEMA-2020-12": "current_2020_12",
    "IETF-JCS": "stable_informational_rfc",
    "WCAG22": "recommendation_2024",
    "BIPM-SI": "ninth_edition_updated_2026",
    "NZ-PRIVACY": "current_including_ipp3a_from_2026_05_01",
    "TE-MANA-RARAUNGA": "primary_principles_current",
    "GIT-LOG": "current",
    "PYTHON-JSON": "current",
}


def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {"negative_id": negative_id, "signature": signature, "recovery": recovery, "recovery_passed": True}


STARTUP_FAILURES = [
    _startup_failure("V6607-X1-N001", "skill-metadata-probe-serialized-rich-filesystem-provider-objects-and-truncated-an-oversized-display", "Retain the oversized display at zero credit and read literal UTF-8 line windows from each named skill and required reference through EOF."),
    _startup_failure("V6607-X1-N002", "first-manifest-replay-launched-one-git-process-per-blob-exceeded-the-bounded-window-and-lost-the-running-session-id", "Retain the wrapper at zero credit, verify no matching Python replay remains, and use one bounded git cat-file --batch object reader."),
    _startup_failure("V6607-X1-N003", "first-x1-manifest-coverage-comparison-mixed-phase-relative-exclusions-with-repository-relative-diff-paths", "Retain the false four-missing and four-extra result at zero credit, prefix the declared phase root, and rerun only the isolated set comparison."),
    _startup_failure("V6607-X1-N004", "mixed-powershell-and-cmd-temporary-redirection-for-packet-hashing-was-blocked-before-execution", "Retain the blocked wrapper at zero credit and hash the immutable raw Git blob in one in-memory Python process without a temporary file."),
    _startup_failure("V6607-X1-N005", "broad-exact-hash-rg-search-over-docs-scripts-and-tests-exceeded-the-bounded-window", "Retain the broad search at zero credit and use bounded git grep on exact paths plus direct lookup in the declared external receipt bank."),
    _startup_failure("V6607-X1-N006", "expected-empty-remote-branch-probe-called-trim-on-null-output", "Retain the null-value error at zero credit and materialize the remote rows with a null-safe array-count check."),
    _startup_failure("V6607-X1-N007", "initial-ls-tree-and-agents-probe-exceeded-its-short-wrapper-window", "Retain the initial timeout at zero credit, preserve the original session id, and poll the same process to attributable completion without rerunning it."),
    _startup_failure("V6607-X1-N008", "worktree-add-wrapper-outlived-its-visible-call-and-returned-no-attributable-final-receipt-while-checkout-continued", "Retain the wrapper at zero credit, inspect exact path, branch, registration, process, and lock state, and never rerun worktree add before quiescence."),
    _startup_failure("V6607-X1-N009", "first-post-create-audit-completed-without-returning-its-projected-json", "Retain the blank audit at zero credit and split path, branch, registration, process, head, and cleanliness into independent scalar probes."),
    _startup_failure("V6607-X1-N010", "broad-full-worktree-porcelain-list-truncated-before-the-new-registration", "Retain the truncated listing at zero credit and filter the same porcelain stream to the exact normalized Ilyra path with bounded context."),
    _startup_failure("V6607-X1-N011", "status-probe-ran-while-worktree-checkout-was-still-populating-and-emitted-a-massive-transient-deleted-and-untracked-surface", "Retain the transient observation at zero credit, mutate nothing, wait for all Git checkout processes to quiesce, then prove staged, unstaged, and untracked cleanliness separately."),
    _startup_failure("V6607-X1-N012", "exact-worktree-registration-filter-exceeded-its-first-wrapper-window", "Retain the timeout at zero credit, keep its session id, and poll that same filter to the exact three-line registration receipt."),
    _startup_failure("V6607-X1-N013", "first-proposal-index-parser-assumed-a-generic-rows-key-absent-from-the-partitioned-schema", "Retain the TypeError at zero credit, inspect the declared top-level keys and types, then union prior_proposals and new_proposals exactly."),
    _startup_failure("V6607-X1-N014", "second-proposal-index-probe-emitted-maori-text-through-the-windows-cp1252-console-and-raised-unicodeencodeerror", "Retain the encoding fault at zero credit and pin Python UTF-8 before emitting Unicode source and authority text."),
    _startup_failure("V6607-X1-N015", "one-stale-label-rg-expression-was-split-by-powershell-quoting-into-spurious-path-arguments", "Retain the three rg path errors at zero credit and run separate single-quoted literal searches over the exact current x1 files."),
    _startup_failure("V6607-X1-N016", "first-external-x1-manifest-replay-used-literal-backslash-r-backslash-n-bytes-through-nested-shell-quoting-and-falsely-reported-two-code-hash-mismatches", "Retain both false mismatches and the verifier assumption at zero credit, construct CRLF and LF from numeric byte values, and rerun only the manifest replay before staging."),
]

# X2 failures may be appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
