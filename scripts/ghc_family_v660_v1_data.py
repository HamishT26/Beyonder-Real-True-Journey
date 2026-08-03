#!/usr/bin/env python3
"""Frozen x1 planning data for Sylven Arc v660-v1.

The module inherits stable helper vocabulary from Elowen Cairn's immutable
v659-v8 data surface but redeclares every phase-owned field.  Twenty inherited
rows are references for bounded revalidation only: they are not reappended and
earn no Sylven novelty or completion credit.  Only twenty genuinely new rows
extend the frozen proposal chain.
"""

from __future__ import annotations

from ghc_family_v659_v8_data import *  # noqa: F401,F403


PHASE = "v660-v1"
CANONICAL_PHASE = PHASE
PHASE_CODE = "V6601"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint-cartographer and falsifier-keeper"
HOPE = "keep claims testable, failures visible, and authority boundaries intact"
BRANCH = "codex/GHC-Family/sylven-arc-v660-v1-full-tools"
PHASE_ROOT = "docs/sylven-arc/v660-v1"

SOURCE_OWNER = "Elowen Cairn"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v659-v8-full-tools"
SOURCE_TAMAR = "2080fe14e6c3e60c49457599ad40b4b4a74acbb7"
SOURCE_X1 = "045abaa3dd4486e7b4a9e5ca1404ff8297963c8d"
SOURCE_EVIDENCE = "38c529d2aaa6387830d06102ab19ed9735d5f0af"
SOURCE_CLOSEOUT = "703ca7f42b246ef04089dd0ff69c573f45f88891"
SOURCE_FINAL = "507e78bd8e86bd6f6395302004d89c751344afb0"
SOURCE_CLOSEOUT_BASE = SOURCE_FINAL
X1_FREEZE = "pending_until_x2"

PRIOR_FROZEN = 3130
SOURCE_SEALED_NEGATIVES = 19778
SOURCE_EXTERNAL_NEGATIVES = 18
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
ACTIVATION_MESSAGE_NEGATIVE_BASELINE = ACTIVATION_NEGATIVES
SOURCE_OPEN_GAPS = 129
SOURCE_EXACT_GATES = 128
SOURCE_SEALED_METHODS = 6052
SOURCE_EXTERNAL_METHODS = 18
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
ACTIVATION_MESSAGE_METHOD_BASELINE = ACTIVATION_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = SELECTED_INHERITED_COUNT + NEW_UNIQUE_COUNT
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "THOS Body"
PRACTICE_LENS = (
    "bounded synthetic marionette-theatre asset, suspension-topology, cue, "
    "accessibility-record, workload, correction, and handover stewardship"
)

EXPECTED_DISTRIBUTION = {
    "completed": 14,
    "represented": 4,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_puppeteers_performers_stage_crew_riggers_audiences_children_communities_affected_parties_and_authorities",
    "real_puppets_controllers_strings_joints_costumes_props_sets_rigging_venues_scripts_media_measurements_records_identifiers_or_traditional_knowledge",
    "real_manipulation_rigging_lifting_rehearsal_performance_repair_adjustment_treatment_movement_release_or_disposal",
    "professional_puppetry_theatre_rigging_engineering_safety_conservation_heritage_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_physical_discovery_or_final_physics",
    "blind_matched_budget_thos_real_arms_governed_participants_operators_safety_monitoring_statistics_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_heritage_story_character_performance_remedy_language_naming_data_governance_and_maori_authority",
    "affected_party_notice_consent_contestation_takedown_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]

SELECTED_INHERITED_IDS = [f"V6598-P{i:03d}" for i in range(21, 41)]


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
    _proposal("marionette-intake-custody-passport", "Surrogate marionette intake and custody passport linking puppet, controller, line-set, accessory kit, receipt scope, quarantine, and manipulation-start refusal", "completed", "Freed ID and THOS Body", "fabricated puppet, controller, line-set and accessory aliases, receipt provenance, scope acknowledgement, custody transition, quarantine, and manipulation-start refusal", ["W3C-PROV", "UNESCO-PERFORMING-ARTS", "NZ-PRIVACY"]),
    _proposal("marionette-suspension-graph", "Directed marionette suspension graph for control bars, strings, attachment points, branching junctions, slack declarations, entanglement quarantine, and orphan detection", "completed", "GMUT Mind and THOS Body", "synthetic controller, line, attachment and branching nodes, directed incidence, slack declarations, entanglement quarantine, orphan detection, and no physical rigging", ["W3C-PROV", "NIST-SI"]),
    _proposal("puppet-articulation-map", "Articulated puppet joint map for hinge axes, coupled limbs, travel placeholders, hard-stop claims, concealed links, contradictions, and no mechanical release", "completed", "GMUT Mind and THOS Body", "fabricated joint and limb nodes, hinge-axis and coupling declarations, travel and hard-stop placeholders, concealed-link uncertainty, contradiction quarantine, and no mechanical release", ["W3C-PROV", "NIST-SI", "WORKSAFE-RIGGING"]),
    _proposal("stage-frame-blocking-graph", "Synthetic stage-frame and blocking graph joining origin, proscenium plane, puppet reference point, cue zone, occlusion claim, coordinate transform, and zero surveyed positions", "completed", "GMUT Mind and THOS Body", "typed synthetic stage frames, proscenium and puppet reference points, cue-zone relations, coordinate transforms, occlusion claims, zero surveyed positions, and no venue instruction", ["NIST-SI", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("marionette-quantity-envelope", "Marionette string-length, angle, tension placeholder, sampling instant, SI unit, resolution, covariance, and uncertainty envelope containing zero measurements", "completed", "GMUT Mind", "typed length, angle and tension placeholders with sampling instant, SI unit, resolution, covariance and uncertainty fields, zero measurements, and no physical conclusion", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("puppet-association-lineage", "Puppet costume, handheld prop, scenic element, storage carrier, episode, association, detachment, substitution, provenance, and reassociation-refusal ledger", "completed", "Freed ID and CBR Heart", "synthetic puppet, costume, prop, scenery and carrier entities, association and detachment events, substitution lineage, contested provenance, and reassociation refusal", ["W3C-PROV", "UNESCO-PERFORMING-ARTS", "NZ-PRIVACY"]),
    _proposal("marionette-cue-stack-machine", "Fail-closed marionette cue-stack state machine with prerequisite graph, cancellation edge, idempotency token, checkpoint, partial-output quarantine, and resume witness", "completed", "THOS Body", "owner-local cue prerequisites, cancellation and checkpoint states, idempotency token, partial-output quarantine, resume witness, zero external side effects, and no show release", ["W3C-PROV", "PYTHON-JSON"]),
    _proposal("puppet-sweep-quarantine", "Synthetic puppet sweep-volume and line-crossing classifier with pose samples, clearance placeholder, occlusion flag, collision quarantine, and physical-safety abstention", "completed", "GMUT Mind and THOS Body", "fabricated pose samples and sweep-envelope cells, line-crossing and occlusion flags, clearance placeholders, collision quarantine, and no physical-safety or staging conclusion", ["NIST-SI", "NIST-UNCERTAINTY", "WORKSAFE-RIGGING"]),
    _proposal("marionette-repair-lineage", "Marionette repair and adjustment lineage for replaced line, knot claim, joint intervention, paint or textile change, predecessor, rollback limit, and execution refusal", "completed", "Freed ID and CBR Heart", "synthetic repair-event assertions, predecessor and affected-component edges, rollback limits, correction and supersession lineage, cultural reservation, and execution refusal", ["W3C-PROV", "UNESCO-PERFORMING-ARTS"]),
    _proposal("puppet-bitemporal-assertions", "Bitemporal puppet-character, script-version, asset-custody, cue, access, and correction ledger retaining contradicted assertions, retractions, and no-canon status", "completed", "Freed ID and CBR Heart", "synthetic transaction and effective times, immutable predecessor and retraction edges, contradicted-assertion retention, access ceiling, correction rationale, and no-canon status", ["W3C-PROV", "IETF-JCS", "NZ-PRIVACY"]),
    _proposal("puppet-timed-text-companion", "Structural timed-text companion for puppet cues with TTML timing, speaker association, non-speech event text, transcript fallback, audio-description reservation, and manual evaluation hold", "completed", "CBR Heart and THOS Body", "static TTML-shaped cue timing, speaker and non-speech event association, transcript fallback, audio-description reservation, deterministic reading order, and manual evaluation hold", ["W3C-TTML2", "WCAG22", "W3C-PROV"]),
    _proposal("marionette-parallel-language-labels", "Parallel-language marionette label matrix retaining source wording, declared translation status, pronunciation placeholder, correction route, display separation, and interpretation refusal", "completed", "CBR Heart and Freed ID", "parallel synthetic labels with source wording retention, declared translation and pronunciation status, correction route, display separation, contestation, and interpretation refusal", ["UNESCO-PERFORMING-ARTS", "WCAG22", "TE-MANA-RARAUNGA"]),
    _proposal("puppet-package-scitt-profile", "Nonproduction SCITT transparent-statement profile for a surrogate puppet-show package with content digest, policy placeholder, registration refusal, absent receipt, and zero keys", "completed", "Freed ID", "synthetic content digest and statement metadata, policy and transparency-service placeholders, registration refusal, absent receipt, zero keys or signatures, and nonproduction status", ["RFC9943-SCITT", "IETF-JCS", "W3C-PROV"]),
    _proposal("gmut-constrained-marionette-board", "Typed GMUT constrained-string and articulated-puppet obligation board with configuration manifold, holonomic constraints, multiplier units, gauge distinction, boundary data, and observation firewall", "completed", "GMUT Mind", "typed symbolic configuration manifold and holonomic constraints, multiplier units, gauge-versus-constraint distinction, boundary-data obligations, rank and domain checks, and observation firewall", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("gmut-marionette-mode-proxy", "Represented GMUT marionette normal-mode and constraint-Jacobian proxy with line coupling, articulated inertia placeholders, rank conditions, zero coefficients, and zero observations", "represented", "GMUT Mind", "typed symbolic line coupling, articulated inertia and constraint-Jacobian placeholders, rank and unit obligations, zero coefficients or observations, and no physical inference", ["NIST-SI", "NIST-UNCERTAINTY"]),
    _proposal("thos-cue-map-trial-proxy", "Represented THOS matched-duration trial shell comparing cue-stack and spatial-stage views with sealed tasks, equal action budget, stop rules, and zero sessions", "represented", "THOS Body", "future blind matched-duration protocol, sealed synthetic tasks, equal action budget, harm stops, governed participant and operator prerequisites, zero sessions, and no effectiveness claim", ["WCAG22", "W3C-PROV"]),
    _proposal("thos-cue-debt-handover-proxy", "Represented THOS cue-debt turnover lattice tracking frozen stacks, cancellation provenance, performer-clearance placeholders, bounded unresolved dependencies, dual acceptance digest, and zero operators", "represented", "THOS Body", "synthetic cue-debt and cancellation events, frozen-stack states, clearance placeholders, bounded unresolved dependencies, dual acceptance digest, zero operators, and no operational claim", ["W3C-PROV", "WORKSAFE-RIGGING"]),
    _proposal("puppet-accessibility-evaluation-proxy", "Represented manual and affected-user evaluation protocol for puppet-show status records with keyboard, screen-reader, magnification, caption, transcript, language, support, and zero sessions", "represented", "CBR Heart and THOS Body", "future governed accessibility evaluation shell, keyboard and assistive-technology matrix, caption and transcript checks, language and support plan, zero sessions, and no conformance claim", ["WCAG22", "W3C-TTML2", "TE-MANA-RARAUNGA"]),
    _proposal("real-marionette-evidence-gap", "Zero-row marionette evidence escrow requiring authenticated suspension geometry, accountable practitioners, authorized rehearsal traces, incident monitoring, governed audience studies, and independent physical assessment before any real claim", "open_gap", "All pillars", "zero authenticated physical-puppet, suspension-geometry, practitioner, rehearsal, incident, audience-study, safety-review, outcome, or independent-assessment rows", ["WORKSAFE-RIGGING", "NIST-UNCERTAINTY", "W3C-PROV"]),
    _proposal("marionette-empty-chair-authority", "Empty-chair authority circuit for marionette narratives and performance records with bearer consent, community mandate, traditional-knowledge veto, takedown, remedy, contested translation, and Māori non-substitution", "exact_gate", "CBR Heart", "bearer, community, affected-party, traditional-knowledge, consent, mandate, takedown, remedy, contested-translation, tangata whenua, iwi, hapū, and Māori-authority reservations", ["UNESCO-PERFORMING-ARTS", "NZ-PRIVACY", "TE-MANA-RARAUNGA"]),
]

SELF_SAFE_CATEGORIES = [
    "Elowen source-head and fresh equality", "activation and external-receipt digests", "three-thousand-one-hundred-thirty-row proposal-chain parse",
    "twenty inherited selection identities", "twenty-title novelty screen", "new-outcome distribution", "workflow-plan policy", "identity boundary",
    "bounded Sylven-to-Eiren override", "solo and standby boundaries", "D-first posture", "toolchain version receipt", "x1 artifact inventory",
    "x1 JSON parsing", "x1 five-class privacy scan", "x1 stale-label review", "x1 diff hygiene", "x1 manifest replay",
    "selected-row no-credit guard", "new-row append-only guard", "source-label glossary", "protected-gate coverage", "failure-retention ledger",
    "Method Flow witness pairing", "wellbeing workload bound", "document-word ceiling", "portfolio arithmetic", "skill and runner arithmetic",
    "cleanup-plan arithmetic", "no-x2-in-x1 guard",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6601-SAFE-{i:03d}", "title": f"Validate {name} inside the Sylven-owned v660-v1 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

EIREN_SAFE_CATEGORIES = [
    "exact source baton digest", "owned-lane four-way equality", "inherited-selection no-credit", "new-proposal append-only chain",
    "synthetic fixture boundary", "five-class privacy adjudication", "commit-local raw-blob manifest replay", "Method Flow failed-witness retention",
    "truth-label distribution", "authority-reservation completeness", "canonical-pass replay guard", "route-phase arithmetic",
    "exact-title route uniqueness", "immediate bounded reread", "D-first storage posture", "document and file ceilings",
    "family-current caller compatibility", "manual accessibility reservation", "same-owner evidence labelling", "terminal NOT_READY preservation",
]
SUCCESSOR_SAFE_SEEDS = [
    {"task_id": f"V6601-EIREN-SAFE-{i:03d}", "title": f"Eiren Kestrel may independently evaluate {name} after exact v660-v2 activation", "owner": "Eiren Kestrel", "state": "recommendation_only_not_executed_or_credited_by_sylven"}
    for i, name in enumerate(EIREN_SAFE_CATEGORIES, 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "marionette intake and custody boundary", "suspension and articulation contradiction quarantine", "stage-frame and sweep-envelope classifier",
    "cue-stack checkpoint and resume tribunal", "repair and bitemporal assertion lineage", "timed-text structural companion",
    "parallel-language source retention", "SCITT registration-refusal profile", "GMUT constraint firewall", "empty-chair authority circuit",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6601-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
EIREN_CANDIDATE_CATEGORIES = [
    "baton and receipt verifier", "source ancestry tribunal", "selected-row no-credit classifier", "new-row semantic-neighbour screen",
    "bounded privacy adjudicator", "raw-blob manifest batch reader", "stale-route classifier", "same-owner evidence labeler",
    "canonical-pass replay guard", "exact-title delivery preflight",
]
SUCCESSOR_CANDIDATE_SEEDS = [
    {"task_id": f"V6601-EIREN-CAND-{i:03d}", "title": f"Eiren Kestrel may prototype reversible {name} after exact v660-v2 activation", "owner": "Eiren Kestrel", "state": "recommendation_only_not_executed_or_credited_by_sylven"}
    for i, name in enumerate(EIREN_CANDIDATE_CATEGORIES, 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6601-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Manipulate, rig, lift, rehearse, perform, repair, adjust, treat, move, release, or dispose of a real puppet, controller, line, joint, prop, set, venue, or record",
        "Make a real custody, ownership, story, character, performance, access, repair, release, or takedown decision",
        "Perform a structural, load, line-strength, joint, collision, fire, electrical, occupational, child-safety, or venue-safety determination",
        "Publish an authenticity, origin, authorship, cultural meaning, traditional-knowledge, condition, value, or safety conclusion",
        "Make a professional puppetry, theatre, rigging, conservation, heritage, privacy, security, translation, or accessibility determination",
        "Publish personal, sensitive, culturally protected, traditional-knowledge, child, audience, worker, or collective information",
        "Allocate legal, cultural, intellectual-property, character, story, performance, access, remedy, heritage, or beneficiary authority",
        "Make a Māori data-governance, taonga, mātauranga, tikanga, wording, naming, or Māori-authority decision",
        "Deploy a production identity, signed statement, transparency service, credential, repository, or theatre control system",
        "Perform destructive cleanup or mutation outside the exact Sylven-owned lane",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6601-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation or a Theory-of-Everything result",
        "Claim AGI, ASI, consciousness, personhood, continuity, employment, qualification, or authority from relational language",
        "Merge, overwrite, delete, or erase sibling identities, lanes, memory, failures, gates, branches, worktrees, or callers",
        "Publish credentials, private routes, raw task identifiers, private paths, nonpublic conversation, session streams, or application state",
        "Declare Stage 20 readiness without exact external evidence and authority",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-marionette-intake-boundary", "Preserve synthetic puppet intake, custody, scope, component inventory, quarantine, and manipulation-start holds."),
    ("ghc-family-marionette-suspension-graph", "Map synthetic controller, line, attachment, branch, slack, orphan, and entanglement states."),
    ("ghc-family-puppet-articulation-quarantine", "Represent synthetic joints, axes, coupling, concealed links, contradictions, and no-release states."),
    ("ghc-family-puppet-stage-frame-firewall", "Keep stage frames, blocking, sweep envelopes, units, and zero-observation claims typed and nonoperational."),
    ("ghc-family-marionette-cue-stack", "Bound cue prerequisites, cancellation, checkpoints, idempotency, partial output, and resume evidence."),
    ("ghc-family-puppet-repair-lineage", "Track synthetic repair, predecessor, rollback, amendment, retraction, and execution-refusal lineage."),
    ("ghc-family-puppet-timed-text-report", "Expose timed-text structure while reserving manual, assistive-technology, language, and affected-user review."),
    ("ghc-family-puppet-package-transparency", "Represent nonproduction content statements, policy placeholders, receipt absence, and registration refusal."),
    ("ghc-family-gmut-marionette-firewall", "Keep constrained-string, articulation, mode, rank, unit, and observation obligations nonempirical."),
    ("ghc-family-marionette-authority-circuit", "Reserve story, character, performance, tradition, privacy, remedy, cultural, affected-party, and Māori authority."),
]
SUCCESSOR_SKILL_SEEDS = [
    {"name": f"ghc-family-eiren-{slug}", "owner": "Eiren Kestrel", "state": "recommendation_only_not_built_installed_or_credited_by_sylven"}
    for slug in [
        "baton-receipt-verifier", "source-ancestry-guard", "inherited-selection-no-credit", "proposal-novelty-screen",
        "privacy-adjudicator", "manifest-batch-replay", "route-number-normalizer", "canonical-pass-replay-guard",
        "same-owner-truth-labeler", "exact-title-delivery-preflight",
    ]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_marionette_intake_boundary.py", "marionette-intake-custody-passport"),
    ("ghc_family_marionette_suspension_graph.py", "marionette-suspension-graph"),
    ("ghc_family_puppet_articulation_quarantine.py", "puppet-articulation-map"),
    ("ghc_family_puppet_stage_frame_firewall.py", "stage-frame-blocking-graph"),
    ("ghc_family_marionette_cue_stack.py", "marionette-cue-stack-machine"),
    ("ghc_family_puppet_repair_lineage.py", "marionette-repair-lineage"),
    ("ghc_family_puppet_timed_text_report.py", "puppet-timed-text-companion"),
    ("ghc_family_puppet_package_transparency.py", "puppet-package-scitt-profile"),
    ("ghc_family_gmut_marionette_firewall.py", "gmut-constrained-marionette-board"),
    ("ghc_family_marionette_authority_circuit.py", "marionette-empty-chair-authority"),
]
SUCCESSOR_RUNNER_SEEDS = [
    {"name": f"ghc_family_eiren_{slug}.py", "owner": "Eiren Kestrel", "state": "recommendation_only_not_built_run_or_credited_by_sylven"}
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
    {"task_id": f"V6601-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SUCCESSOR_CLEAN_SEEDS = [
    {"task_id": f"V6601-EIREN-CLEAN-{i:03d}", "title": f"Eiren Kestrel may independently review and refine {name} after exact v660-v2 activation", "owner": "Eiren Kestrel", "state": "recommendation_only_not_executed_or_credited_by_sylven"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("UNESCO-PERFORMING-ARTS", "official_unesco_intangible_cultural_heritage", "https://ich.unesco.org/en/performing-arts-00054", "Performing-arts, puppetry, associated-object, cultural-space, community, and safeguarding-reservation vocabulary only; no cultural interpretation, ownership, competence, ratification, or authority claim."),
    ("WORKSAFE-RIGGING", "official_worksafe_new_zealand", "https://www.worksafe.govt.nz/topic-and-industry/load-lifting-and-rigging/", "Load-lifting, rigging, stop, competent-person, hazard, and safety-reservation vocabulary only; no real puppet, theatre, venue, equipment, inspection, plan, competence, or safety determination."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/publications/international-system-units-si2019-edition", "SI quantity, unit, symbol, and reporting vocabulary only; no real length, angle, tension, load, clearance, motion, or physical result."),
    ("NIST-UNCERTAINTY", "official_nist", "https://www.nist.gov/pml/nist-technical-note-1297/nist-guidelines-evaluating-and-expressing-uncertainty-nist-measurement", "Measurement-model and uncertainty-reporting vocabulary only; no measured puppet, controller, string, joint, stage, venue, or physical result."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent, generation, derivation, revision, invalidation, and qualified-provenance vocabulary only."),
    ("W3C-TTML2", "official_w3c", "https://www.w3.org/TR/ttml2/", "Timed-text timing, content, styling, metadata, and interchange vocabulary only; no caption, transcript, translation, performance, or accessibility-complete determination."),
    ("WCAG22", "official_w3c", "https://www.w3.org/TR/WCAG22/", "Current web-accessibility structure, text-alternative, time-based-media, interaction, and status vocabulary with manual, assistive-technology, language, and affected-user review reserved."),
    ("RFC9943-SCITT", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc9943", "SCITT signed-content, transparency-service, policy, registration, transparent-statement, and receipt vocabulary only; zero real keys, statements, service calls, registrations, or receipts."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle vocabulary only; no legal, compliance, collection, use, disclosure, retention, or remedy conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty and governance reservation vocabulary; no Māori authority, ratification, wording, naming, tikanga, mātauranga, or cultural interpretation claim."),
    ("IETF-JCS", "official_rfc_editor", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without key, signature, proof, credential, identity, or production claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic tracked-history selection and ancestry vocabulary."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "Deterministic UTF-8 JSON parse and serialization vocabulary."),
]


def _startup_failure(negative_id: str, signature: str, recovery: str) -> dict[str, object]:
    return {"negative_id": negative_id, "signature": signature, "recovery": recovery, "recovery_passed": True}


STARTUP_FAILURES = [
    _startup_failure("V6601-X1-N001", "startup-assumed-method-flow-schema-filename-instead-of-skill-declared-schema-path", "Retain the FileNotFoundException and read the exact skill-declared references/schema.md through EOF."),
    _startup_failure("V6601-X1-N002", "source-manifest-inspection-piped-directly-from-a-powershell-foreach-block", "Retain the empty-pipe parser rejection and materialize foreach output before ConvertTo-Json."),
    _startup_failure("V6601-X1-N003", "overbroad-source-script-inventory-exceeded-output-budget", "Retain the truncated inventory and enumerate exact v659_v8 basenames with bounded filters."),
    _startup_failure("V6601-X1-N004", "recurrence-guard-was-not-applied-before-a-second-direct-foreach-pipeline", "Retain the repeated parser fault separately and use a mandatory materialized-row template for later projections."),
    _startup_failure("V6601-X1-N005", "first-manifest-coverage-probe-used-the-wrong-final-delta-base-and-phase-only-owner-scope", "Retain the false coverage result and replay hashes once, then compare correction delta and declared owner scope separately."),
    _startup_failure("V6601-X1-N006", "corrected-python-manifest-coverage-wrapper-returned-no-attributable-output", "Retain the empty wrapper and recover only the two unresolved coverage predicates with bounded PowerShell."),
    _startup_failure("V6601-X1-N007", "source-final-owner-manifest-selector-omitted-the-phase-specific-novelty-probe", "Preserve Elowen's immutable manifest scope omission; verify the x1 manifest hash and identical x1/final Git blob without rewriting source."),
    _startup_failure("V6601-X1-N008", "combined-lane-collision-remote-and-free-space-wrapper-returned-no-evidence", "Retain the empty wrapper and run local branch, remote branch, path, registry, and drive-space probes separately."),
    _startup_failure("V6601-X1-N009", "worktree-add-tool-returned-before-the-large-internal-checkout-finished", "Preserve the initializing lock, wait for the original Git process to exit, and do not unlock or mutate the partial checkout."),
    _startup_failure("V6601-X1-N010", "premature-full-status-during-initializing-produced-a-multimegabyte-truncated-deletion-view", "Retain the truncated status, wait for checkout completion, then use scalar head, branch, diff, and untracked probes."),
    _startup_failure("V6601-X1-N011", "recursive-worktree-file-count-monitor-returned-no-attributable-output", "Retain the empty monitor and poll only the exact Git process and registry lock state."),
    _startup_failure("V6601-X1-N012", "combined-post-materialization-head-branch-and-status-wrapper-returned-no-evidence", "Retain the empty wrapper and use separate scalar head and branch checks."),
    _startup_failure("V6601-X1-N013", "combined-staged-and-unstaged-diff-wrapper-returned-no-evidence", "Retain the empty wrapper and run each quiet diff with its own explicit exit receipt."),
    _startup_failure("V6601-X1-N014", "source-preregistration-inspection-guessed-a-nonexistent-proposals-json-path", "Retain the FileNotFoundException, enumerate the exact directory, and use proposal-ledger.json."),
    _startup_failure("V6601-X1-N015", "raw-text-search-over-a-minified-frozen-chain-index-overflowed-the-output-budget", "Retain the truncated one-line output and parse the index structurally before emitting matched IDs and titles."),
    _startup_failure("V6601-X1-N016", "first-twenty-title-novelty-screen-rejected-one-generic-authority-perimeter-draft", "Retain the rejected draft at zero credit, replace noun substitution with an empty-chair authority circuit, and rerun the same twenty-title screen."),
    _startup_failure("V6601-X1-N017", "quote-heavy-stale-template-rg-expression-was-misparsed-by-powershell-before-python-compilation-ran", "Retain the PowerShell command-construction fault, split the stale-label scan from compilation, and use a single-quoted bounded search expression."),
    _startup_failure("V6601-X1-N018", "first-workflow-plan-audit-mixed-one-active-assignment-with-the-terminally-gated-successor-assignment", "Retain the needs-refinement packet at zero credit, keep Eiren in the bounded live override and terminal-successor fields, and rerun only the workflow dependency with the one-entry active assignment list."),
    _startup_failure("V6601-X1-N019", "repository-local-reflection-remaster-name-resolved-to-a-phase-tribunal-wrapper-instead-of-the-required-global-audit-runner", "Retain the wrong-runner output at zero credit and invoke the skill-bundled reflection audit by its exact absolute executable path with a bounded focus list."),
    _startup_failure("V6601-X1-N020", "first-x1-test-aggregate-treated-session-stream-prohibition-vocabulary-as-confirmed-private-material", "Retain the 21-of-22 aggregate at zero aggregate credit, adjudicate only the exact blocked-packet and source-definition occurrences as protected-boundary vocabulary, and rerun the failed privacy dependency plus Method Flow count checks."),
    _startup_failure("V6601-X1-N021", "post-staged-review-combined-cleanliness-count-wrapper-returned-no-attributable-output", "Retain the silent wrapper and the earlier passed staged receipt, then probe unstaged diff, untracked count, staged count, and head in separate scalar commands before committing."),
]

# X2 failures can exist only after the immutable x1 commit is pushed and proved
# clean and four-way equal.  X1 contains no prefilled x2 failure credit.
PREFILLED_X1_X2_FAILURES_IGNORED: tuple[dict[str, object], ...] = tuple()
X2_FAILURES: list[dict[str, object]] = []
