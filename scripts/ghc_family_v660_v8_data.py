#!/usr/bin/env python3
"""Frozen x1 planning data for Auren Lark v660-v8.

Ilyra Fen's immutable v660-v7 surface supplies compatibility vocabulary only.
Twenty inherited rows are selected for bounded revalidation with zero Auren
novelty or completion credit. Only the twenty new rows below extend the
append-only proposal chain. All physical, participant, professional, empirical,
production, legal, cultural, accessibility-complete, privacy-complete, and Māori
authority lanes remain empty or exact-gated.
"""

from __future__ import annotations

from ghc_family_v660_v7_data import *  # noqa: F401,F403


PHASE = "v660-v8"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6608"
OWNER = "Auren Lark"
PRONOUNS = "they/them"
ROLE = "relational evidence-path cartographer and repair-traceability steward"
HOPE = (
    "keep every synthetic position, move, variation, correction, refusal, source, "
    "and authority boundary legible, recoverable, and honest without converting "
    "software structure into play, rating, adjudication, expertise, identity, or authority"
)
BRANCH = "codex/GHC-Family/auren-lark-v660-v8-full-tools"
PHASE_ROOT = "docs/auren-lark/v660-v8"

SOURCE_OWNER = "Ilyra Fen"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v660-v7-full-tools"
SOURCE_BASE = "6be1e90e55854f6e0dc0faeb38621b6086f4e688"
SOURCE_X1 = "ae06de953f21db197bb7a57a5a5e70cc7e97da0a"
SOURCE_EVIDENCE = "1e7c8872c7c775eb97e64c93d5cd0f2330e8802d"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "8edf12352101f3a78f0db738a431b3ebb64e07f5"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "d1ee480bd423135a46353232b4bc027950b79f1782a8234c81bf7de1b762755b"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED"
ACTIVATION_PACKET_SHA256 = (
    "3f295cd6aa2347d77c01df2cf97d0f890b20c819a73828edede9373d3c486d51"
)
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3270
SOURCE_SEALED_NEGATIVES = 20737
SOURCE_EXTERNAL_NEGATIVES = 3
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 20740
SOURCE_OPEN_GAPS = 136
SOURCE_EXACT_GATES = 135
SOURCE_SEALED_METHODS = 6451
SOURCE_EXTERNAL_METHODS = 3
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6454
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "bounded synthetic chess-position, legal-move, notation, variation, clock, correction, "
    "study-handover, provenance, accessibility, privacy, rights-reservation, and cultural "
    "and Māori non-substitution lens"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_chess_games_positions_moves_variations_problems_studies_boards_pieces_clocks_venues_platforms_broadcasts_ratings_titles_or_records",
    "real_players_opponents_coaches_arbiters_organizers_federations_spectators_rights_holders_communities_affected_parties_and_authorities",
    "real_play_move_entry_adjudication_coaching_analysis_pairing_clock_operation_rating_reporting_publication_or_tournament_action",
    "professional_chess_play_coaching_arbitration_composition_analysis_event_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "game_attribution_player_data_fair_play_safeguarding_accessibility_event_access_broadcast_community_traditional_knowledge_and_collective_interest",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_naming_rating_title_record_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_correction_takedown_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6607-P{i:03d}" for i in range(1, 21)]


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
        "chess-dossier-identity",
        "Surrogate chess dossier identity capsule with variant, board geometry, piece alphabet, revision, source pin, and play refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic dossier and revision tokens, declared variant, board geometry, piece alphabet, source pin, correction, tombstone, and zero-real-play states",
        ["FIDE-LAWS-2023", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "chess-position-state-ledger",
        "Board-bounded chess position ledger with square uniqueness, side-to-move, castling and en-passant claims, duplicate-piece, and foreign-token quarantine",
        "completed",
        "GMUT Mind and Freed ID",
        "typed synthetic square and piece states with side-to-move, castling and en-passant placeholders, occupancy uniqueness, contradiction, unknown, and no-game guards",
        ["FIDE-LAWS-2023", "JSON-SCHEMA-2020-12", "IETF-JCS"],
    ),
    _proposal(
        "chess-legal-move-transition",
        "Synthetic chess move-transition tribunal with source position, destination position, side-to-move, capture and promotion claims, and mismatch retention",
        "completed",
        "GMUT Mind",
        "synthetic source and destination positions, side-to-move, origin and target squares, capture and promotion placeholders, mismatch witnesses, correction lineage, and physical-action abstention",
        ["FIDE-LAWS-2023", "JSON-SCHEMA-2020-12", "W3C-PROV"],
    ),
    _proposal(
        "chess-algebraic-notation-parser",
        "Algebraic chess-notation expansion and normalization contract for piece, square, capture, promotion, castling, check markers, and parse refusal",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic notation tokens, board context, piece and square fields, capture and promotion markers, castling and check placeholders, round-trip digest, ambiguity, and parse refusal",
        ["FIDE-LAWS-2023", "JSON-SCHEMA-2020-12", "IETF-JCS"],
    ),
    _proposal(
        "chess-variation-tree",
        "Chess mainline, variation, branch, transposition-placeholder, annotation, and study dependency tree with cycle and incomplete-boundary quarantine",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic positions, moves, mainline and variation edges, transposition placeholders, prerequisites, incomplete nodes, cycles, and no-play declaration",
        ["FIDE-LAWS-2023", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "chess-position-claim-braid",
        "Chess position, move, result, annotation, puzzle-status placeholder, source, contestation, and supersession assertion braid",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic position and move assertions, result and annotation placeholders, source status, puzzle-state unknown, contradiction, retraction, correction, and adjudication-authority abstention",
        ["FIDE-LAWS-2023", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "chess-termination-obligation-board",
        "Chess termination and draw-claim obligation board with checkmate, stalemate, repetition, move-count, agreement, timeout placeholders, and ruling refusal",
        "completed",
        "GMUT Mind",
        "synthetic position histories, declared termination, repetition and move-count witnesses, agreement and timeout placeholders, incomplete evidence, counterexample slot, and official-ruling refusal",
        ["FIDE-LAWS-2023", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "chess-move-correction-lineage",
        "Chess move, clock, annotation, result, correction, supersession, readback, and unresolved-ambiguity lineage",
        "completed",
        "THOS Body and Freed ID",
        "synthetic moves, clocks, annotations and result placeholders, correction, supersession, readback, ambiguity hold, cancellation, and no-adjudication state",
        ["FIDE-LAWS-2023", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "chess-game-record-provenance",
        "Synthetic chess-game record provenance covenant with event and player placeholders, position and result claims, correction, privacy mask, and publication refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic event and player placeholders, position and result assertions, date and clock placeholders, correction, disclosure mask, consent and privacy holds, and publication refusal",
        ["FIDE-LAWS-2023", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "chess-bitemporal-memory",
        "Bitemporal position, move, variation, game-claim, correction, retraction, tombstone, and non-erasure memory",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic assertion and record intervals, predecessor links, correction, retraction, supersession, tombstone, contradiction retention, and record-erasure refusal",
        ["W3C-PROV", "IETF-JCS", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "chess-clock-uncertainty",
        "Chess clock reading, move interval, increment and delay placeholder, SI unit, resolution, covariance, missingness, and uncertainty envelope",
        "completed",
        "GMUT Mind",
        "typed synthetic clock and move-interval placeholders, SI units, increment and delay fields, resolution, covariance, uncertainty, missingness, zero observations, and performance firewall",
        ["BIPM-SI", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-chess-state-graph-obligations",
        "GMUT chess state-graph, generator, reachability, symmetry, invariant, cycle, closure, and observation-firewall obligation board",
        "completed",
        "GMUT Mind",
        "typed symbolic position nodes, move generators, reachability, symmetry and invariant placeholders, cycles, closure, units, and zero game or physical observations",
        ["FIDE-LAWS-2023", "BIPM-SI", "IETF-JCS"],
    ),
    _proposal(
        "chess-physical-action-firewall",
        "Chess play, move entry, clock operation, coaching, arbitration, pairing, rating, and publication action-authorization firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic action request, event-rule placeholder, player, coach, arbiter, organizer, federation and platform holds, safeguarding and access flags, stop token, and execution refusal",
        ["FIDE-LAWS-2023", "W3C-PROV", "NZ-PRIVACY"],
    ),
    _proposal(
        "chess-canonical-package",
        "Canonical synthetic chess documentation package with ordered position, move, notation, variation, correction, source, and profile digests",
        "completed",
        "Freed ID and THOS Body",
        "synthetic ordered dossier entries, profile version, normalized fields, position and notation digests, migration witness, collision quarantine, and no-key or credential declaration",
        ["IETF-JCS", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "gmut-chess-evaluation-proxy",
        "GMUT chess state, material-balance, mobility, transition-cost, boundary, and uncertainty proxy with zero played games or engine observations",
        "represented",
        "GMUT Mind",
        "typed symbolic position, material, mobility, transition-cost and boundary placeholders, zero fitted coefficients, zero likelihood rows, zero engine outputs, and game-strength inference abstention",
        ["FIDE-LAWS-2023", "BIPM-SI", "IETF-JCS"],
    ),
    _proposal(
        "thos-chess-study-handover",
        "THOS bounded chess-study handoff with ambiguity budget, stop condition, acceptance digest, and workload refusal",
        "represented",
        "THOS Body",
        "synthetic position and variation study queues, correction and ambiguity debt, workload ceilings, stop tokens, readback, escalation, acceptance digest, handover, and zero players, coaches, or operators",
        ["FIDE-LAWS-2023", "WCAG22", "W3C-PROV"],
    ),
    _proposal(
        "chess-comprehension-protocol",
        "Counterbalanced empty-session protocol comparing notation-first and board-state-first synthetic chess explanations",
        "represented",
        "THOS Body",
        "future matched-budget synthetic dossiers, shuffled questions, equal action budgets, masked scoring, support and withdrawal rules, zero participants, and no learning-effect claim",
        ["WCAG22", "FIDE-LAWS-2023", "W3C-PROV"],
    ),
    _proposal(
        "chess-access-companion",
        "Accessible nonvisual synthetic board narrative with square relations, sequential navigation, redundant cues, and affected-user review reservation",
        "represented",
        "CBR Heart and THOS Body",
        "structural headings, square and move relations, linear traversal, noncolour cues, keyboard sequence, print fallback, language and tactile reservations, and zero affected-user sessions",
        ["WCAG22", "FIDE-LAWS-2023", "W3C-PROV"],
    ),
    _proposal(
        "real-chess-evidence-vault",
        "Real games, players, boards, clocks, events, ratings, rulings, participant outcomes, and independent-assessment vault with zero-row refusal",
        "open_gap",
        "All pillars",
        "zero authenticated games, governed player sessions, accountable arbiters or coaches, calibrated board or clock observations, participant outcomes, fair-play controls, or independent-review records",
        ["FIDE-LAWS-2023", "NZ-PRIVACY", "W3C-PROV"],
    ),
    _proposal(
        "chess-rights-rating-authority",
        "Unoccupied mandate circuit for participation, safeguarding, attribution, game records, ratings, titles, fair-play review, remedy, and Māori decision non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied player, opponent, guardian, coach, arbiter, organizer, federation, platform, record, rating, title, privacy, fair-play, community, takedown, remedy, tangata whenua, iwi, hapū, and Māori-authority reservations",
        ["FIDE-LAWS-2023", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Ilyra source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-two-hundred-seventy-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "mechanism-level neighbor review",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity and relational-language boundary",
    "Hamish-authorized Ilyra-to-Auren live edge",
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
    {"task_id": f"V6608-SAFE-{i:03d}", "title": f"Validate {name} inside the Auren-owned v660-v8 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6611-REC-SAFE-{i:03d}", "title": f"Reassess {name} for Sable-only v661-v1", "recipient": "Sable Rook", "completion_credit": 0}
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "synthetic chess-dossier identity ledger",
    "position-state and legal-move transition tribunal",
    "algebraic-notation parser and normalizer",
    "variation-tree dependency graph",
    "position-claim and contestation braid",
    "termination truth-obligation board",
    "move and correction lineage",
    "synthetic game-record provenance covenant",
    "GMUT chess-state graph obligation board",
    "chess rights, rating, and cultural-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6608-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6611-REC-CAND-{i:03d}", "title": f"Consider a distinct Sable-owned refinement of {name}", "recipient": "Sable Rook", "completion_credit": 0}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6608-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Play, enter, alter, adjudicate, analyze, publish, submit, rate, title, pair, schedule, or certify any real chess game, position, move, event, account, result, or record",
            "Make a real legality, clock, result, draw, termination, fair-play, safeguarding, rating, title, eligibility, or competence determination",
            "Use real players, opponents, guardians, coaches, arbiters, organizers, federations, platforms, boards, clocks, accounts, games, telemetry, recordings, or personal information",
            "Disclose private identity, contact, age, disability, safeguarding, location, account, game, fair-play, dispute, or restricted community information",
            "Make a professional chess, arbitral, coaching, event-management, privacy, security, translation, or accessibility determination",
            "Publish a production game record, result, rating, title assertion, identifier, credential, signed statement, proof, or interoperable chess record",
            "Allocate authorship, game credit, result credit, rating, title, access, ownership, custody, takedown, remedy, or beneficiary authority",
            "Make a tikanga, mātauranga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, or Māori-authority decision",
            "Run a real participant study, chess session, event trial, platform trial, professional review, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Auren-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6608-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
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
    ("ghc-family-chess-position-validator", "Validate bounded synthetic positions while preserving illegal, incomplete, ambiguous, unknown, and no-real-game states."),
    ("ghc-family-chess-move-transition", "Check synthetic legal-move state transitions without playing, adjudicating, rating, or claiming chess competence."),
    ("ghc-family-chess-notation", "Parse and normalize bounded synthetic algebraic notation with explicit ambiguity, context, and refusal states."),
    ("ghc-family-chess-variation-tree", "Represent variation, dependency, cycle-refusal, transposition-reference, and incomplete-boundary states."),
    ("ghc-family-chess-claim-assertion", "Retain position, move, source, contestation, correction, supersession, and authority abstention."),
    ("ghc-family-chess-termination-obligations", "Expose checkmate, stalemate, draw-claim, resignation, time, result, and adjudication-refusal obligations."),
    ("ghc-family-chess-correction-lineage", "Preserve moves, corrections, supersession, readback, ambiguity, and non-adjudication holds."),
    ("ghc-family-chess-record-provenance", "Track synthetic game-record provenance, correction, minimisation, disclosure stop, and publication refusal."),
    ("ghc-family-gmut-chess-state-graph", "Preserve symbolic state, transition, inverse-edge, reachability, invariant, and observation-firewall obligations."),
    ("ghc-family-chess-rights-rating-authority", "Keep participation, safeguarding, attribution, privacy, fair-play, rating, title, remedy, and Māori decision rights unoccupied."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": name.replace("chess", "successor-domain"), "recipient": "Sable Rook", "state": "recommendation_only", "completion_credit": 0}
    for name, _ in SELF_SKILL_SPECS
]
SELF_RUNNER_SPECS = [
    (name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py", purpose)
    for name, purpose in SELF_SKILL_SPECS
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": name.replace("chess", "successor_domain"), "recipient": "Sable Rook", "state": "recommendation_only", "completion_credit": 0}
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
    {"task_id": f"V6608-CLEAN-{i:03d}", "title": title, "owner": OWNER, "mode": "additive_review_only"}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6611-REC-CLEAN-{i:03d}", "title": title, "recipient": "Sable Rook", "completion_credit": 0}
    for i, title in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("FIDE-LAWS-2023", "official_fide_handbook", "https://handbook.fide.com/chapter/E012023", "Current official Laws of Chess vocabulary for position, move, notation, clock, completion, result, and arbiter-reserved obligations only; no game, ruling, rating, title, event, or authority claim."),
    ("FIDE-HANDBOOK", "official_fide_handbook", "https://handbook.fide.com/", "Official handbook index and document-status vocabulary only; no federation status, endorsement, professional interpretation, or authority is claimed."),
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
    "FIDE-LAWS-2023": "official_laws_effective_2023_01_01_checked_2026_08_04",
    "FIDE-HANDBOOK": "official_index_checked_2026_08_04",
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
    _startup_failure("V6608-X1-N001", "first-activation-packet-window-was-oversized-and-truncated-before-eof", "Retain the truncated display at zero credit and read literal UTF-8 one-hundred-line windows through the exact EOF."),
    _startup_failure("V6608-X1-N002", "first-exact-tree-inventory-projection-exited-without-usable-output", "Retain the blank projection at zero credit and split branch, head, ancestry, cleanliness, and tree inventory into bounded scalar Git probes."),
    _startup_failure("V6608-X1-N003", "startup-guessed-a-nonexistent-final-validation-prerequisites-path", "Retain the absent-path lookup at zero credit and enumerate the declared phase validation directories before opening exact files."),
    _startup_failure("V6608-X1-N004", "shallow-inventory-guessed-a-nonexistent-phase-tests-directory", "Retain the absent-directory lookup at zero credit and enumerate only existing phase top-level directories."),
    _startup_failure("V6608-X1-N005", "first-batched-official-source-open-returned-no-usable-content", "Retain the empty batch at zero credit and inspect each bounded primary or official source individually."),
    _startup_failure("V6608-X1-N006", "direct-approved-framework-place-notation-url-returned-not-found", "Retain the not-found response at zero credit and use the official approved-edition result while keeping the failed URL out of the current source ledger."),
    _startup_failure("V6608-X1-N007", "direct-technical-taxonomy-source-open-timed-out", "Retain the timeout at zero credit and recover only the official-domain source status through a bounded search."),
    _startup_failure("V6608-X1-N008", "direct-public-performance-service-homepage-open-timed-out", "Retain the timeout at zero credit and require no performance record or service content for this phase."),
    _startup_failure("V6608-X1-N009", "public-performance-service-recovery-search-surfaced-personal-performance-rows", "Retain the privacy-stop at zero credit, use none of the surfaced content, persist none of it, and do not repeat the search."),
    _startup_failure("V6608-X1-N010", "startup-guessed-an-absent-owner-validation-receipt-path", "Retain the absent-path lookup at zero credit and use bounded filename inventory to resolve the exact external receipt."),
    _startup_failure("V6608-X1-N011", "combined-source-cleanliness-wrapper-yielded-no-final-projection", "Retain the blank wrapper at zero credit and prove staged, unstaged, and untracked cleanliness with separate scalar probes."),
    _startup_failure("V6608-X1-N012", "first-four-manifest-batch-produced-no-result-and-left-two-object-readers", "Retain the blank batch at zero credit, verify the exact process command lines, stop only those readers, and replay each immutable manifest through one bounded object reader."),
    _startup_failure("V6608-X1-N013", "native-python-argument-quoting-stripped-required-path-quotes", "Retain the syntax error at zero credit and pass the bounded verifier through literal UTF-8 standard input."),
    _startup_failure("V6608-X1-N014", "evidence-replay-used-an-illegal-assignment-expression-rebind", "Retain the syntax error at zero credit and recover with an explicit deterministic loop."),
    _startup_failure("V6608-X1-N015", "post-create-parallel-cleanliness-audit-returned-only-one-projection", "Retain the incomplete audit at zero credit, prove checkout-process quiescence, and run each missing scalar probe separately."),
    _startup_failure("V6608-X1-N016", "broad-post-copy-status-projection-returned-blank", "Retain the blank projection at zero credit and list the exact five expected x1 template paths."),
    _startup_failure("V6608-X1-N017", "direct-official-laws-page-open-timed-out", "Retain the timeout at zero credit and recover only the official laws page and status through a bounded official-domain search."),
    _startup_failure("V6608-X1-N018", "broad-stale-token-search-truncated-before-an-attributable-result", "Retain the truncated search at zero credit and use per-token counts plus bounded literal line windows."),
    _startup_failure("V6608-X1-N019", "source-review-found-a-draft-framework-described-as-current", "Retain the status mismatch at zero credit and preserve the draft and unapproved status alongside the latest approved-edition boundary."),
    _startup_failure("V6608-X1-N020", "first-bounded-novelty-receipt-refused-two-titles-at-or-above-the-declared-threshold", "Retain the two refused rows at zero credit, revise only their current titles to distinguish mechanism and review scope, and rerun only the isolated title screen."),
    _startup_failure("V6608-X1-N021", "powershell-pipeline-display-degraded-one-maori-character-in-the-read-only-novelty-receipt", "Retain the display corruption at zero credit, persist none of that output, and run the isolated verifier in one UTF-8 Python process."),
    _startup_failure("V6608-X1-N022", "first-intentional-workflow-rejection-also-found-an-unintended-duplicate-sable-seat-and-missing-lyren-seat", "Retain the two-issue rejecting witness at zero credit, restore the exact fifteen-main-task cycle, and rerun only the intentional invalid fixture before validating the corrected request."),
    _startup_failure("V6608-X1-N023", "workflow-refinement-runner-returned-exit-one-for-a-written-invalid-packet-where-the-selected-skill-described-exit-two", "Retain the documented-exit mismatch at zero credit, use the written validation and issue receipts as the bounded witness, and require exit zero for the corrected request."),
    _startup_failure("V6608-X1-N024", "combined-artifact-audit-dropped-the-long-running-porcelain-status-session-before-its-count-projection", "Retain the missing projection at zero credit, prove the orphaned status process is absent, and rerun one direct bounded porcelain status probe to attributable completion."),
]

# X2 failures may be appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
