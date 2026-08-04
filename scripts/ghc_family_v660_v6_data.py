#!/usr/bin/env python3
"""Frozen x1 planning data for Lyren Moss v660-v6.

Vesper Arlen's immutable v660-v5 surface supplies compatibility vocabulary
only. Twenty inherited rows are selected for bounded revalidation with zero
Vesper novelty or completion credit. Only the twenty new rows below extend the
append-only proposal chain. Real-world connectors and authority rows remain empty.
"""

from __future__ import annotations

from ghc_family_v660_v5_data import *  # noqa: F401,F403


PHASE = "v660-v6"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6606"
OWNER = "Lyren Moss"
PRONOUNS = "they/them"
ROLE = "relational fold-state cartographer and contradiction keeper"
HOPE = (
    "make synthetic crease graphs, layer states, diagrams, instruction provenance, "
    "and correction boundaries inspectable without converting software structure into "
    "physical proof, authorship, licensing, cultural, educational, or Māori authority"
)
BRANCH = "codex/GHC-Family/lyren-moss-v660-v6-full-tools"
PHASE_ROOT = "docs/lyren-moss/v660-v6"

SOURCE_OWNER = "Vesper Arlen"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v660-v5-full-tools"
SOURCE_BASE = "3616ca214e6fa411330c56e73b3d095e5c9a79e1"
SOURCE_X1 = "38ed87786c89c77b9b78b5ad520828ba8a02982e"
SOURCE_EVIDENCE = "f5d09a8f1b69a54e335db1da0531d0bd560d5c03"
SOURCE_CLOSEOUT = SOURCE_EVIDENCE
SOURCE_FINAL = "050fd7559df40bc08f990fc26a8636636e520a3a"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "cefd1995d5d4dc2aeb05061cc50026153197d9ebe6a81eebde5cd4c912f77bcd"
)
SOURCE_LIVE_ACTIVATION_STATE = "SENT_ONCE_ACKNOWLEDGED"
ACTIVATION_PACKET_SHA256 = (
    "79ba2ac956aaec7b7aa7c47f7bc543eb0b2f793226aa754c37bc2028374a5955"
)
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3230
SOURCE_SEALED_NEGATIVES = 20446
SOURCE_EXTERNAL_NEGATIVES = 16
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = 20460
SOURCE_OPEN_GAPS = 134
SOURCE_EXACT_GATES = 133
SOURCE_SEALED_METHODS = 6320
SOURCE_EXTERNAL_METHODS = 16
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = 6334
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "THOS Body"
PRACTICE_LENS = (
    "bounded synthetic origami-model documentation: sheet identity, crease and face "
    "topology, fold-state lineage, diagram provenance, uncertainty, accessible review, "
    "rights and cultural-authority reservation, and handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_paper_models_artworks_crease_patterns_diagrams_photographs_videos_instructions_classes_events_measurements_designs_or_publications",
    "real_designers_artists_authors_teachers_students_participants_communities_indigenous_rights_holders_affected_parties_and_authorities",
    "real_folding_unfolding_cutting_scoring_gluing_wetting_treatment_display_sale_licensing_publication_teaching_transfer_return_or_deaccession",
    "professional_origami_design_mathematics_education_conservation_museum_curation_metrology_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "sensitive_authorship_copyright_licensing_provenance_heritage_indigenous_or_traditional_knowledge_attribution_permission_and_benefit_obligations",
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

SELECTED_INHERITED_IDS = [f"V6605-P{i:03d}" for i in range(1, 21)]


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
        "origami-sheet-identity-capsule",
        "Surrogate paper-sheet and model identity capsule with source dimensions, orientation, grain placeholder, revision, and folding refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic sheet and model tokens, source dimensions, orientation, grain placeholder, frame lineage, correction, tombstone, and zero-physical-folding states",
        ["FOLD-SPEC", "W3C-PROV", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "origami-crease-face-topology",
        "Origami vertex, edge, crease, boundary, face, hole, and incidence topology graph",
        "completed",
        "GMUT Mind and Freed ID",
        "typed synthetic vertex, edge, crease, boundary, face, hole, and incidence relations with orphan, duplicate, contradiction, unknown, and nonidentity guards",
        ["FOLD-SPEC", "JSON-SCHEMA-2020-12", "W3C-PROV"],
    ),
    _proposal(
        "origami-assignment-contradiction-ledger",
        "Mountain, valley, flat, boundary, unassigned, cut, join, and assignment-contradiction ledger",
        "completed",
        "GMUT Mind and CBR Heart",
        "synthetic edge assignment, declared source, unknown and unassigned distinction, contradiction, correction, supersession, and foldability-conclusion abstention states",
        ["FOLD-SPEC", "JSON-SCHEMA-2020-12", "W3C-PROV"],
    ),
    _proposal(
        "origami-layer-order-frame",
        "Folded-frame face-overlap and layer-order relation board with cycle quarantine",
        "completed",
        "GMUT Mind and Freed ID",
        "synthetic frame, overlapping-face pair, above-below relation, unknown ordering, cycle detection, contradiction retention, and geometric-realizability refusal",
        ["FOLD-SPEC", "JSON-SCHEMA-2020-12", "IETF-JCS"],
    ),
    _proposal(
        "origami-coordinate-uncertainty",
        "Vertex coordinate, sheet dimension, fold-angle placeholder, unit, precision, and uncertainty envelope",
        "completed",
        "GMUT Mind",
        "typed synthetic coordinate and dimension fields, SI units, frame and method placeholders, precision, uncertainty, missingness, zero observations, and physical-accuracy firewall",
        ["FOLD-SPEC", "BIPM-SI", "W3C-PROV"],
    ),
    _proposal(
        "origami-fold-sequence-lineage",
        "Fold-step dependency, prerequisite, branch, checkpoint, reversal, and correction lineage",
        "completed",
        "THOS Body and Freed ID",
        "synthetic fold step, prerequisite graph, alternative branch, checkpoint, reversal claim, partial-state quarantine, correction, and physical-execution refusal",
        ["FOLD-SPEC", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "origami-material-intervention-firewall",
        "Cut, score, wet-fold, adhesive, tool, and material-intervention authorization firewall",
        "completed",
        "CBR Heart and THOS Body",
        "synthetic intervention request, tool and material placeholders, reversibility declaration, safety and rights holds, competent-practitioner placeholder, conflict retention, and execution refusal",
        ["ICOM-CC-TERMINOLOGY", "W3C-PROV", "CREATIVE-COMMONS"],
    ),
    _proposal(
        "origami-diagram-symbol-grammar",
        "Instruction diagram arrow, line style, viewpoint, inset, repetition, and ambiguity grammar",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic diagram step, arrow, line style, viewpoint, inset, repetition, reference, ambiguity, correction, and interpretation-refusal states",
        ["W3C-SVG2", "W3C-PROV", "WCAG22"],
    ),
    _proposal(
        "origami-rights-attribution-braid",
        "Designer, folder, diagrammer, photographer, source, license, attribution, and permission assertion braid",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic role and source assertions, license and permission placeholders, attribution string, disagreement, supersession, correction, and rights-conclusion abstention",
        ["CREATIVE-COMMONS", "W3C-PROV", "C2PA-22"],
    ),
    _proposal(
        "origami-local-fold-obligation-board",
        "Local vertex parity and alternating-sector-angle obligation board with theorem-application refusal",
        "completed",
        "GMUT Mind",
        "synthetic vertex sector sequence, assignment counts, symbolic angle placeholders, parity predicates, missingness, counterexample slot, and no-universal-foldability or proof claim",
        ["FOLD-SPEC", "BIPM-SI", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "origami-face-orientation-transform",
        "Face orientation, affine-transform, normal placeholder, coordinate-frame, and reflection-parity ledger",
        "completed",
        "GMUT Mind and THOS Body",
        "synthetic face, coordinate frame, affine transform, orientation and normal placeholders, reflection parity, unknown state, contradiction, and 3D-embedding refusal",
        ["FOLD-SPEC", "W3C-SVG2", "JSON-SCHEMA-2020-12"],
    ),
    _proposal(
        "origami-diagram-media-provenance",
        "Instruction diagram, image, animation, annotation, crop, derivative, and correction provenance covenant",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic diagram and media assets, ingredient and action lineage, annotation target, crop and transform declarations, correction, disclosure mask, and authenticity refusal",
        ["IIIF-PRESENTATION-3", "C2PA-22", "W3C-PROV"],
    ),
    _proposal(
        "origami-language-notation-circuit",
        "Multilingual fold instruction and notation register with source pin, translation status, glossary, and interpretation refusal",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic source wording, language tag, notation token, glossary relation, translation and review status, correction route, and no-authoritative-interpretation declaration",
        ["W3C-SVG2", "WCAG22", "W3C-PROV"],
    ),
    _proposal(
        "origami-record-tombstone-ledger",
        "Bitemporal model-frame, diagram revision, retraction, supersession, tombstone, and non-erasure memory",
        "completed",
        "Freed ID and CBR Heart",
        "synthetic model frame, diagram revision, assertion interval, retraction, supersession, contradiction, correction, tombstone, and record-erasure refusal states",
        ["FOLD-SPEC", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "gmut-origami-constraint-rank-proxy",
        "GMUT symbolic crease-constraint rank, branch-consistency, and self-contact obligation proxy",
        "represented",
        "GMUT Mind",
        "typed symbolic crease constraints, branch variables, rank and dependency placeholders, self-contact boundary, units, zero coefficients, zero likelihood rows, and geometry-solution abstention",
        ["FOLD-SPEC", "BIPM-SI", "IETF-JCS"],
    ),
    _proposal(
        "thos-origami-diagram-queue",
        "THOS diagram-production, ambiguity-debt, review-hold, and handover queue proxy",
        "represented",
        "THOS Body",
        "synthetic diagram and review queues, ambiguity and contradiction debt, workload ceilings, stop tokens, escalation clocks, readback, handover, and zero designers or instructors",
        ["W3C-SVG2", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "origami-comprehension-protocol",
        "Counterbalanced empty-session comprehension protocol comparing crease-first and step-first synthetic instructions",
        "represented",
        "THOS Body",
        "future matched-budget protocol, randomized synthetic instruction dossiers, sealed scoring, equal actions, stop and withdrawal rules, zero participants, and no learning or effectiveness claim",
        ["WCAG22", "W3C-PROV", "IETF-JCS"],
    ),
    _proposal(
        "origami-access-companion",
        "Nonvisual crease-network companion with linear relations, tactile reservation, text alternatives, keyboard path, and print fallback",
        "represented",
        "CBR Heart and THOS Body",
        "structural headings, vertex-edge-face relations, linear text, noncolour assignments, keyboard and speech order, tactile reservation, print fallback, and reservations for manual and affected-user evaluation",
        ["WCAG22", "W3C-SVG2", "W3C-PROV"],
    ),
    _proposal(
        "real-origami-evidence-vault",
        "Real origami artwork, fold-state, instruction, participant, and independent-review evidence vault with zero-row refusal",
        "open_gap",
        "All pillars",
        "zero authenticated artworks or designs, governed physical folds, traceable measurements, accountable specialists, affected-user outcomes, adverse controls, or independent-review rows",
        ["FOLD-SPEC", "ICOM-CC-TERMINOLOGY", "WCAG22"],
    ),
    _proposal(
        "origami-rights-cultural-authority-register",
        "Unoccupied mandate circuit for authorship, licensing, teaching, provenance, traditional knowledge, cultural protocol, and Māori decision non-substitution",
        "exact_gate",
        "CBR Heart",
        "unoccupied authorship, copyright, licensing, attribution, teaching, community, Indigenous-knowledge, cultural-protocol, takedown, remedy, tangata whenua, iwi, hapū, and Māori-authority reservations",
        ["CREATIVE-COMMONS", "UNESCO-1970", "TE-MANA-RARAUNGA", "NZ-PRIVACY"],
    ),
]

SELF_SAFE_CATEGORIES = [
    "Vesper source head and fresh equality",
    "activation packet and external receipt digests",
    "three-thousand-two-hundred-thirty-row proposal-chain parse",
    "twenty inherited selection identities",
    "twenty-title novelty screen",
    "new-outcome distribution",
    "workflow-plan policy",
    "identity boundary",
    "Hamish-authorized Vesper-to-Lyren live edge",
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
        "task_id": f"V6606-SAFE-{i:03d}",
        "title": f"Validate {name} inside the Lyren-owned v660-v6 lane",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]
SUCCESSOR_SAFE_SEEDS = [
    {
        "task_id": f"V6607-REC-SAFE-{i:03d}",
        "title": f"Reassess {name} for Ilyra-only v660-v7",
        "recipient": "Ilyra Fen",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_SAFE_CATEGORIES[:20], 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "origami sheet and model identity capsule",
    "crease and face topology graph",
    "assignment contradiction ledger",
    "face-overlap and layer-order board",
    "coordinate and fold-angle uncertainty envelope",
    "fold-step dependency lineage",
    "material intervention firewall",
    "diagram symbol grammar",
    "GMUT crease-constraint rank obligations",
    "origami rights and cultural-authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {
        "task_id": f"V6606-CAND-{i:03d}",
        "title": f"Build and test reversible {name}",
        "owner": OWNER,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {
        "task_id": f"V6607-REC-CAND-{i:03d}",
        "title": f"Consider a distinct Ilyra-owned refinement of {name}",
        "recipient": "Ilyra Fen",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6606-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate(
        [
            "Fold, unfold, cut, score, wet, glue, treat, display, sell, license, publish, teach, transfer, return, or deaccession any real paper model, artwork, pattern, diagram, photograph, video, or instruction set",
            "Make a real authorship, originality, foldability, geometric-validity, safety, conservation, educational-effectiveness, cultural, or accessibility determination",
            "Use real artworks, collections, classrooms, events, tools, blades, adhesives, materials, imaging equipment, measuring instruments, transport, occupational, or public-safety systems",
            "Disclose protected designs, unpublished diagrams, private learner records, precise collection locations, rights disputes, beneficiary data, or restricted cultural knowledge",
            "Make a professional origami-design, mathematics, teaching, conservation, museum-curation, privacy, security, translation, or accessibility determination",
            "Publish a production design assertion, identifier, credential, signed statement, proof, license decision, or interoperable artwork record",
            "Allocate authorship, copyright, license, attribution, teaching, ownership, custody, artwork access, legal, heritage, takedown, remedy, or beneficiary authority",
            "Make a mātauranga, tikanga, wording, naming, tangata whenua, iwi, hapū, Māori data-governance, cultural-protocol, or Māori-authority decision",
            "Run a real participant study, operator trial, workplace workflow, professional review, or independent reproduction",
            "Perform destructive cleanup or any mutation outside the exact Lyren-owned lane",
        ],
        1,
    )
]
BLOCKED_QUEUE = [
    {"task_id": f"V6606-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
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
    ("ghc-family-origami-sheet-identity", "Preserve surrogate sheet, model, frame, dimension, orientation, grain placeholder, correction, tombstone, and folding-refusal states."),
    ("ghc-family-origami-crease-topology", "Represent typed synthetic vertex, edge, crease, boundary, face, hole, incidence, orphan, contradiction, and nonidentity states."),
    ("ghc-family-origami-assignment-ledger", "Keep mountain, valley, flat, boundary, unassigned, cut, join, contradiction, correction, and foldability-abstention terms explicit."),
    ("ghc-family-origami-layer-order", "Bind synthetic frame, overlap, above-below relation, unknown order, cycle quarantine, correction, and realizability refusal."),
    ("ghc-family-origami-coordinate-uncertainty", "Keep coordinate, dimension, angle placeholder, unit, method, precision, uncertainty, missingness, zero-row, and accuracy-refusal obligations typed."),
    ("ghc-family-origami-fold-sequence", "Track fold step, prerequisite, branch, checkpoint, reversal, partial state, correction, and zero-execution lineage."),
    ("ghc-family-origami-intervention-firewall", "Reserve cut, score, wet-fold, adhesive, tool, safety, rights, competence, conflict, and zero-execution gates."),
    ("ghc-family-origami-diagram-grammar", "Track arrows, line styles, viewpoints, insets, repetition, source, ambiguity, correction, and interpretation abstention."),
    ("ghc-family-gmut-origami-constraint-obligations", "Keep symbolic crease constraints, rank, branch, dependency, self-contact, units, covariance, boundary, and likelihood obligations nonempirical."),
    ("ghc-family-origami-rights-cultural-authority", "Reserve authorship, copyright, licensing, attribution, teaching, traditional knowledge, remedy, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {
        "name": f"ghc-family-ilyra-v660-v7-recommendation-{i:02d}",
        "purpose": purpose,
        "recipient": "Ilyra Fen",
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
    ("ghc_family_origami_sheet_identity.py", "origami-sheet-identity-capsule"),
    ("ghc_family_origami_crease_topology.py", "origami-crease-face-topology"),
    ("ghc_family_origami_assignment_ledger.py", "origami-assignment-contradiction-ledger"),
    ("ghc_family_origami_layer_order.py", "origami-layer-order-frame"),
    ("ghc_family_origami_coordinate_uncertainty.py", "origami-coordinate-uncertainty"),
    ("ghc_family_origami_fold_sequence.py", "origami-fold-sequence-lineage"),
    ("ghc_family_origami_intervention_firewall.py", "origami-material-intervention-firewall"),
    ("ghc_family_origami_diagram_grammar.py", "origami-diagram-symbol-grammar"),
    ("ghc_family_gmut_origami_constraint_obligations.py", "gmut-origami-constraint-rank-proxy"),
    ("ghc_family_origami_rights_cultural_authority.py", "origami-rights-cultural-authority-register"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {
        "name": f"ghc_family_ilyra_v660_v7_recommendation_{i:02d}.py",
        "purpose": purpose,
        "recipient": "Ilyra Fen",
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
        "task_id": f"V6606-CLEAN-{i:03d}",
        "title": f"Review and refine {name}",
        "state": "planned_x2_additive_only",
    }
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {
        "task_id": f"V6607-REC-CLEAN-{i:03d}",
        "title": f"Reassess {name} additively in Ilyra v660-v7",
        "recipient": "Ilyra Fen",
        "completion_credit": 0,
    }
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    (
        "ICOM-CC-TERMINOLOGY",
        "official_icom_conservation_committee",
        "https://www.icom-cc.org/en/terminology-for-conservation",
        "Preventive conservation, remedial conservation, restoration, material-significance, accessibility, and qualified-professional boundary vocabulary only; no treatment advice, condition judgment, or conservation authority.",
    ),
    (
        "FOLD-SPEC",
        "primary_fold_format_project",
        "https://github.com/edemaine/fold",
        "Evolving FOLD mesh, frame, vertex, edge, face, assignment, geometry, and face-order vocabulary only; no endorsement, universal conformance, foldability proof, geometry solution, or physical-model result.",
    ),
    (
        "JSON-SCHEMA-2020-12",
        "primary_json_schema_project",
        "https://json-schema.org/draft/2020-12",
        "JSON Schema Core and Validation vocabulary for typed synthetic contracts only; no claim that a phase-local checker is a complete or certified implementation.",
    ),
    (
        "ICOM-ETHICS",
        "official_international_council_of_museums",
        "https://icom.museum/en/resources/standards-guidelines/code-of-ethics/",
        "Due diligence, provenance, acquisition, collections stewardship, security, return, restitution, professional practice, and public-trust boundary vocabulary only; no ethical, legal, ownership, or restitution decision.",
    ),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent-placeholder, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("W3C-SVG2", "official_w3c", "https://www.w3.org/TR/SVG2/", "SVG element, path, line, polygon, group, transform, title, description, metadata, and rendering vocabulary only; no visual correctness or accessibility-complete claim."),
    (
        "IIIF-PRESENTATION-3",
        "official_iiif_consortium",
        "https://iiif.io/api/presentation/3.0/",
        "Collection, Manifest, Canvas, Range, Annotation, ordered-view, rights-placeholder, language, accessibility-companion, and compound-object presentation vocabulary only.",
    ),
    (
        "C2PA-22",
        "official_c2pa_joint_development_foundation",
        "https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html",
        "Digital-asset provenance, assertion, ingredient, update, validation-status, privacy-control, and no-truth-from-provenance boundary vocabulary only; no signature, credential, or authenticity claim.",
    ),
    ("CREATIVE-COMMONS", "primary_creative_commons", "https://creativecommons.org/share-your-work/cclicenses/", "License-name, attribution, adaptation, ShareAlike, NonCommercial, NoDerivatives, and public-domain-tool reservation vocabulary only; no license is selected, applied, interpreted, or enforced."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Accessible structure, text alternative, noncolour, navigation, status, target, and interaction vocabulary with manual, assistive-technology, Māori-language, and affected-user evaluation reserved."),
    ("BIPM-SI", "official_bipm", "https://www.bipm.org/en/publications/si-brochure", "SI length, plane-angle context, time, quantity, unit, symbol, traceability-context, and reporting vocabulary only; no measurement, calibration, fold-angle accuracy, or physical result."),
    ("UNESCO-1970", "official_unesco", "https://www.unesco.org/en/legal-affairs/convention-means-prohibiting-and-preventing-illicit-import-export-and-transfer-ownership-cultural", "Cultural-property import, export, transfer, due-diligence, inventory, return, and international-cooperation reservation vocabulary only; no legal interpretation, ownership finding, export decision, or restitution authority."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary, including indirect-collection notification context, only; no legal, compliance, collection, disclosure, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority, ratification, wording, naming, tikanga, or mātauranga claim."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]
SOURCE_STATUS = {
    "ICOM-CC-TERMINOLOGY": "stable_2008",
    "FOLD-SPEC": "evolving_primary_project",
    "JSON-SCHEMA-2020-12": "current_2020_12",
    "ICOM-ETHICS": "current_2026",
    "W3C-PROV": "stable",
    "W3C-SVG2": "candidate_recommendation",
    "IIIF-PRESENTATION-3": "stable_3_0",
    "C2PA-22": "current_2_2",
    "CREATIVE-COMMONS": "current",
    "WCAG22": "current",
    "BIPM-SI": "current_2026",
    "UNESCO-1970": "current_official_text",
    "NZ-PRIVACY": "current",
    "TE-MANA-RARAUNGA": "stable",
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
    _startup_failure("V6606-X1-N001", "prospective-lane-collision-audit-used-a-semicolon-delimited-git-show-ref-expression-inside-a-powershell-hashtable", "Retain the parser rejection at zero credit, read each Git exit code into a scalar first, and construct the collision receipt only after every isolated read."),
    _startup_failure("V6606-X1-N002", "auth-validation-projection-counted-a-missing-issues-property-as-one-through-array-wrapping", "Retain the false issue count at zero credit and use an explicit null guard before materializing the optional issues array."),
    _startup_failure("V6606-X1-N003", "initial-current-authorization-state-display-was-truncated-before-eof", "Retain the incomplete display at zero credit and reread only the missing bounded line windows through EOF before mutation."),
    _startup_failure("V6606-X1-N004", "first-post-create-audit-wrapper-projected-output-only-and-lost-the-running-session-id", "Retain the blank receipt at zero credit, inspect the exact lingering Git processes, wait for the original diff to finish, and run one smaller attributable audit."),
    _startup_failure("V6606-X1-N005", "worktree-registration-path-comparer-treated-git-forward-slashes-as-a-missing-windows-path", "Retain the false zero match at zero credit and compare the exact normalized Git porcelain path before awarding unique-registration credit."),
    _startup_failure("V6606-X1-N006", "broad-repository-file-enumeration-overflowed-the-output-budget", "Retain the truncated listing at zero credit and constrain later searches to explicit script, test, and owner directories."),
    _startup_failure("V6606-X1-N007", "historical-lyren-data-probe-guessed-a-nonexistent-versioned-script-path", "Retain the path miss at zero credit and locate the committed Lyren owner directory before reading its exact overview."),
    _startup_failure("V6606-X1-N008", "versioned-data-search-passed-a-square-bracket-pseudo-glob-as-a-literal-windows-path", "Retain the path error at zero credit and use rg over the scripts directory with an explicit -g filter."),
    _startup_failure("V6606-X1-N009", "raw-git-blob-reader-used-processstartinfo-argumentlist-unavailable-in-the-host-dotnet-runtime", "Retain the compatibility error at zero credit and pass only the verified hexadecimal object id through the supported Arguments property."),
    _startup_failure("V6606-X1-N010", "raw-git-blob-sha-projection-used-convert-tohexstring-unavailable-in-the-host-dotnet-runtime", "Retain the null digest at zero credit and convert the recomputed SHA-256 bytes with the supported BitConverter path."),
    _startup_failure("V6606-X1-N011", "first-identity-constant-patch-expected-mojibake-instead-of-the-utf8-maori-source-text", "Retain the verification failure at zero credit and patch against the actual UTF-8 text read through the Python UTF-8 boundary."),
    _startup_failure("V6606-X1-N012", "first-monolithic-proposal-patch-carried-one-stale-expected-pillar-value", "Retain the verification failure at zero credit and apply four bounded reviewed proposal hunks against the exact current data file."),
    _startup_failure("V6606-X1-N013", "checked-out-activation-packet-filesystem-sha-differed-from-the-immutable-git-blob-under-line-ending-conversion", "Retain both byte-domain witnesses at zero credit and bind the activation digest to bytes streamed directly from the exact committed Git blob."),
    _startup_failure("V6606-X1-N014", "git-hash-object-normalized-the-checked-out-activation-packet-and-masked-the-filesystem-byte-difference", "Retain the misleading equality at zero credit and use git cat-file standard-output bytes, size-check them, and hash that raw immutable stream."),
    _startup_failure("V6606-X1-N015", "first-docstring-edit-appended-a-replacement-sentence-without-removing-the-stale-sentence", "Retain the transient review defect at zero credit and replace the two contradictory lines with one reviewed boundary sentence before any builder execution."),
    _startup_failure("V6606-X1-N016", "first-bounded-novelty-screen-rejected-five-template-adjacent-titles", "Retain the five title-level rejections at zero novelty credit, revise only their wording while preserving mechanisms and gates, and rerun the isolated read-only screen against all 3230 inherited titles."),
    _startup_failure("V6606-X1-N017", "mechanism-review-found-an-earlier-thirty-row-timepiece-domain-despite-the-retitled-token-screen-passing", "Retain the title-screen pass as useful but insufficient evidence, award no genuine-novelty credit, discard the horology plan before materialization, and replace it with a mechanism-reviewed origami documentation domain absent from inherited titles."),
    _startup_failure("V6606-X1-N018", "first-scoped-x1-suite-passed-twenty-one-of-twenty-three-and-exposed-two-unmaterialized-family-current-receipt-groups", "Retain the first scoped invocation and both missing-receipt errors at zero credit, invoke only the current family receipt builders, refresh the x1 manifest, and rerun only the isolated scoped suite."),
    _startup_failure("V6606-X1-N019", "combined-multi-skill-argument-search-exceeded-the-bounded-display", "Retain the oversized search as zero-credit method evidence and inspect one literal current skill script or help surface at a time before invoking it."),
    _startup_failure("V6606-X1-N020", "workflow-receipt-validator-was-first-addressed-by-a-guessed-nonexistent-filename", "Retain the missing-file error at zero credit, enumerate only the literal current skill scripts, and invoke the discovered validator name without modifying the skill package."),
    _startup_failure("V6606-X1-N021", "first-workflow-receipt-request-declared-the-one-hundred-twenty-seven-row-overlay-but-submitted-only-the-current-lyren-row", "Retain the fail-closed normalization rejection at zero credit and rebuild the submitted assignments from the exact authorized Eiren v660-v2 through Auren v675-v8 overlay, with Lyren v660-v6 explicitly marked as the current row."),
    _startup_failure("V6606-X1-N022", "broad-workflow-validator-text-search-matched-a-large-single-line-retained-negative-artifact", "Retain the oversized display at zero credit and constrain later evidence discovery to literal script listings, bounded help output, and exact expected files."),
    _startup_failure("V6606-X1-N023", "installed-workflow-skill-validator-expected-its-demonstration-raw-audit-directory-layout-rather-than-the-phase-local-receipt-layout", "Retain the FileNotFoundError at zero credit, preserve the installed skill package read-only, and use the current runner's valid and rejecting receipts plus the isolated phase assertions as the attributable structural evidence."),
    _startup_failure("V6606-X1-N024", "first-authorization-validation-receipt-used-a-descriptive-but-noncanonical-phase-local-filename", "Retain the filename mismatch as zero-credit method evidence, write the same current-state validation to the exact preregistered auth-validation-x1 path, and omit the redundant alias from the frozen packet."),
    _startup_failure("V6606-X1-N025", "first-stale-label-probe-expanded-the-large-single-line-inherited-proposal-index-and-truncated-its-display", "Retain the truncated scan at zero credit, classify exact inherited, route-overlay, family-index, and scaffold-transform path families structurally, and inspect only unexpected current-owner tokens with bounded output."),
]

# X2 failures may be appended only after the immutable x1 commit is pushed and
# proved clean and four-way equal.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
