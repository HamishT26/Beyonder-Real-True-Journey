#!/usr/bin/env python3
"""Frozen planning data for Auren Lark's v659-v2 phase."""

from __future__ import annotations


PHASE = "v659-v2"
CANONICAL_PHASE = "v659-v2"
PHASE_CODE = "V6592"
OWNER = "Auren Lark"
PRONOUNS = "they/them"
ROLE = "relational evidence-path cartographer and repair-traceability steward"
HOPE = (
    "keep every evidence path legible, recoverable, and honest while every failed "
    "witness and authority-sensitive boundary remains visible"
)
BRANCH = "codex/GHC-Family/auren-lark-v659-v2-full-tools"
PHASE_ROOT = "docs/auren-lark/v659-v2"

SOURCE_OWNER = "Ilyra Fen"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v659-v1-full-tools"
SOURCE_FINAL = "ab753c3449836e292d6219b478e9ed9146530c92"
SOURCE_X1 = "3406580c1bd9c3bb525125b885216df3c414fef7"
SOURCE_EVIDENCE = "88f4734cda8049c887ad7ba12df088e63737c929"
X1_FREEZE = "78b0cb714b8c0d0c86aaf2fd0503a9a3d4db5f01"
PRIOR_FROZEN = 2930
SOURCE_SEALED_NEGATIVES = 18317
SOURCE_EXTERNAL_NEGATIVES = 6
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
SOURCE_OPEN_GAPS = 122
SOURCE_EXACT_GATES = 121
SOURCE_SEALED_METHODS = 4591
SOURCE_EXTERNAL_METHODS = 6
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "THOS Body"
PRACTICE_LENS = (
    "bounded synthetic fountain-pen service intake, component provenance, "
    "material-compatibility holds, condition correction, and accessible return handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 33,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_people_owners_customers_technicians_conservators_communities_affected_parties_and_authorities",
    "real_fountain_pens_inks_tools_fluids_parts_records_images_measurements_writing_trials_or_identifiers",
    "real_authentication_valuation_treatment_repair_release_chemical_safety_privacy_or_heritage_decision",
    "professional_pen_repair_conservation_materials_science_chemical_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_fluid_prediction_likelihood_parameter_constraint_observational_confirmation_or_physical_discovery",
    "blind_matched_budget_thos_real_arms_real_participants_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_language_naming_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


NEW_PROPOSAL_SPECS = [
    {
        "slug": "intake-custody-passport",
        "title": "Fountain-pen service intake and custody passport with presented-owner placeholder, accessory inventory, condition note, and work-start hold",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic intake alias, presented-owner placeholder, accessory inventory, condition note, custody event, scope acknowledgement, and work-start refusal",
        "sources": ["W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "component-topology-quarantine",
        "title": "Fountain-pen nib, feed, section, housing, and collar topology with orphan-part quarantine and assembly abstention",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional component aliases, typed attachment edges, parent conflicts, orphan-part quarantine, topology challenge, and assembly refusal",
        "sources": ["W3C-PROV", "IETF-JCS"],
    },
    {
        "slug": "filling-system-state",
        "title": "Fountain-pen cartridge, converter, piston, vacuum, lever, and sac filling-system state graph with actuation refusal",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "declared filling-system type, synthetic component state, compatible transition map, missing-evidence hold, and physical actuation abstention",
        "sources": ["W3C-PROV"],
    },
    {
        "slug": "material-compatibility-reservation",
        "title": "Fountain-pen ink residue, flush medium, seal, and material-compatibility reservation with chemical-safety referral",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "declared residue and material placeholders, unknown-contact flag, compatibility challenge, flush hold, and competent chemical-safety referral",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "W3C-PROV"],
    },
    {
        "slug": "cap-barrel-seal-condition",
        "title": "Fountain-pen cap, barrel, section thread, inner cap, and seal condition ledger with pressure-test abstention",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic cap, barrel, thread, inner-cap, and seal observations, uncertainty flags, correction history, and pressure-test refusal",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "W3C-PROV"],
    },
    {
        "slug": "trim-corrosion-observation",
        "title": "Fountain-pen clip, band, plating, trim, and corrosion observation record with conservation-verdict refusal",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "fictional trim locations, visible-condition vocabulary, lighting and viewpoint pins, observation uncertainty, and conservation-verdict abstention",
        "sources": ["CCI-METALS", "W3C-PROV"],
    },
    {
        "slug": "nib-visual-envelope",
        "title": "Fountain-pen nib tine, slit, breather, tipping, and alignment visual envelope with writing-quality abstention",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic nib regions, declared viewpoint, scale-cue placeholder, visible alignment envelope, uncertainty note, and writing-quality refusal",
        "sources": ["W3C-PROV", "WCAG22"],
    },
    {
        "slug": "feed-flow-firewall",
        "title": "Fountain-pen feed channel, fin, collector, and air-return schematic with flow-prediction firewall",
        "outcome": "completed",
        "pillar": "THOS Body and GMUT Mind",
        "mechanism": "fictional feed geometry labels, directional channel graph, unknown-dimension flags, zero fluid rows, and physical flow-prediction abstention",
        "sources": ["NIST-SI", "W3C-PROV"],
    },
    {
        "slug": "cleaning-provenance",
        "title": "Fountain-pen cleaning tool, fluid lot, contact interval, rinse state, and waste-route placeholder with use hold",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "synthetic tool and fluid aliases, lot and interval provenance, rinse-state transition, waste-route placeholder, and real-use hold",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "W3C-PROV"],
    },
    {
        "slug": "replacement-provenance",
        "title": "Fountain-pen replacement component provenance and interchangeability challenge ledger with authenticity refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional replacement-part alias, source and fit claims, competing compatibility assertions, challenge state, and authenticity abstention",
        "sources": ["W3C-PROV", "IETF-JCS"],
    },
    {
        "slug": "condition-image-lineage",
        "title": "Fountain-pen condition-image viewpoint, illumination, scale cue, rights, and redaction lineage with diagnosis abstention",
        "outcome": "completed",
        "pillar": "Freed ID, THOS Body, and CBR Heart",
        "mechanism": "synthetic image alias, viewpoint and illumination labels, scale-cue placeholder, rights and redaction events, and diagnosis refusal",
        "sources": ["W3C-PROV", "NZ-PRIVACY", "WCAG22"],
    },
    {
        "slug": "work-order-deviation-lifecycle",
        "title": "Fountain-pen work-order deviation, scope correction, supersession, and readback lifecycle with release refusal",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic requested scope, deviation record, correction candidate, supersession edge, readback placeholder, and release refusal",
        "sources": ["W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "accessible-return-handover",
        "title": "Fountain-pen return package, cap state, accessory reconciliation, moisture-control placeholder, and accessible handover hold",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "fictional return package, cap-state declaration, accessory reconciliation, moisture-control placeholder, structured text alternative, and handover hold",
        "sources": ["WCAG22", "W3C-PROV"],
    },
    {
        "slug": "gmut-capillary-flow-proxy",
        "title": "Represented fountain-pen capillary-flow dimension matrix with zero ink measurements and physical-prediction refusal",
        "outcome": "represented",
        "pillar": "GMUT Mind",
        "mechanism": "dimensioned symbolic channel and fluid placeholders, bounded proxy states, identifiability flags, zero measurement rows, and physical-inference refusal",
        "sources": ["NIST-SI"],
    },
    {
        "slug": "dryout-seal-maintenance-proxy",
        "title": "Represented fountain-pen dry-out interval and seal-state maintenance proxy with zero durability claim",
        "outcome": "represented",
        "pillar": "THOS Body",
        "mechanism": "synthetic interval labels, cap and seal proxy states, maintenance placeholder, unresolved observations, zero physical tests, and durability abstention",
        "sources": ["CCI-PLASTICS", "W3C-PROV"],
    },
    {
        "slug": "accessible-service-history",
        "title": "Represented fountain-pen service-history table with text chronology and manual accessibility-review reservation",
        "outcome": "represented",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "caption, scoped headers, service-event links, text chronology, keyboard-order placeholder, and no accessibility-complete claim",
        "sources": ["WCAG22"],
    },
    {
        "slug": "nonproduction-component-lineage",
        "title": "Represented nonproduction fountain-pen component-lineage query with disclosure-depth ceiling and credential abstention",
        "outcome": "represented",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "synthetic component and service nodes, predecessor and replacement edges, role placeholders, depth ceiling, disclosure refusal, and no credential claim",
        "sources": ["W3C-PROV", "IETF-JCS"],
    },
    {
        "slug": "maker-model-annotation-challenge",
        "title": "Represented contested fountain-pen maker, model, inscription, and ownership annotation trail with undecided remedy jurisdiction",
        "outcome": "represented",
        "pillar": "CBR Heart",
        "mechanism": "maker, model, inscription, and ownership annotations, notice, counterstatement, correction candidate, remedy-jurisdiction placeholder, and authority abstention",
        "sources": ["NZ-PRIVACY", "TE-MANA-RARAUNGA", "W3C-PROV"],
    },
    {
        "slug": "real-pen-evidence-gap",
        "title": "Open gap for real fountain pens, inks, material identification, dimensional measurements, writing trials, manufacturer documentation, and professional review",
        "outcome": "open_gap",
        "pillar": "All pillars",
        "mechanism": "zero real-object and ink rows, absent dimensional and writing tests, absent manufacturer records, absent competent review, and explicit empirical gap",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "NIST-SI"],
    },
    {
        "slug": "pen-authority-ratification-gate",
        "title": "Exact decision-rights gate for fountain-pen authentication, valuation, treatment, chemical safety, customer privacy, heritage claims, remedy, and Māori authority",
        "outcome": "exact_gate",
        "pillar": "CBR Heart",
        "mechanism": "authentication, valuation, treatment, chemical-safety, privacy, heritage, and remedy placeholders plus legal, cultural, collective-governance, and Māori-authority reservations",
        "sources": ["CCI-PLASTICS", "CCI-METALS", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
]


SELF_SAFE_CATEGORIES = [
    "source-head and live equality", "activation packet raw digest", "proposal-chain parse", "twenty inherited selections",
    "twenty-title novelty audit", "four-label distribution", "workflow-plan policy", "identity boundary",
    "Auren-to-Sable route state", "Tavian standby state", "D-first drive posture", "toolchain versions",
    "x1 artifact inventory", "x1 JSON parse", "x1 privacy classes", "x1 stale-label scan",
    "x1 diff hygiene", "x1 manifest replay", "selected-proposal provenance", "new-proposal provenance",
    "source-label glossary", "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing",
    "wellbeing workload bound", "document-word ceiling", "task-portfolio arithmetic", "skill-plan arithmetic",
    "runner-plan arithmetic", "cleanup-plan arithmetic",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6592-SAFE-{i:03d}", "title": f"Validate {name} inside the Auren-owned v659-v2 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

SABLE_SAFE_CATEGORIES = [
    "source-baton digest", "owned-lane equality", "x1 proposal freeze", "synthetic fixture boundary",
    "main-task route classification", "Caelen successor preregistration", "privacy exclusions", "stale-label scan",
    "manifest replay", "exact staged review", "retained failure import", "Method Flow recovery",
    "truth-label distribution", "wellbeing workload bound", "skill inventory", "runner inventory",
    "latest-5000 scan plan", "zero-real-data assertion", "authority reservations", "terminal no-replay gate",
]
SABLE_SAFE_SEEDS = [
    {"task_id": f"V6593-SEED-SAFE-{i:03d}", "title": f"Sable may evaluate {name} in their own v659-v3 lane", "owner": "Sable Rook", "state": "seed_only_not_executed_by_auren"}
    for i, name in enumerate(SABLE_SAFE_CATEGORIES, 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "intake custody passport", "component topology quarantine", "filling-system state graph",
    "material-compatibility reservation", "cap and barrel condition ledger", "trim corrosion observation",
    "nib visual envelope", "feed flow-prediction firewall", "cleaning provenance ledger",
    "replacement interchangeability challenge",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6592-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
SABLE_CANDIDATE_SEEDS = [
    {"task_id": f"V6593-SEED-CAND-{i:03d}", "title": f"Sable may prototype reversible {name}", "owner": "Sable Rook", "state": "seed_only_not_executed_by_auren"}
    for i, name in enumerate([
        "baton parser", "phase-source verifier", "proposal-selection ledger", "bounded file-scan receipt", "authority-gate atlas",
        "privacy-class reducer", "stale-label classifier", "manifest batch replay", "same-owner evidence labeler", "Caelen handoff preflight",
    ], 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6592-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Use real fountain pens, inks, images, records, or measurements", "Issue a real treatment or release decision",
        "Approve a chemical-safety or conservation action", "Publish an authentication or valuation conclusion",
        "Make a professional repair or material-compatibility determination", "Publish personal or protected data",
        "Allocate legal, cultural, or heritage authority", "Make a Māori data-governance decision",
        "Deploy a production identity or service system", "Perform destructive shared-drive cleanup",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6592-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation", "Claim consciousness or personhood from task language",
        "Merge or erase sibling identities", "Publish credentials or private callable routes",
        "Declare Stage 20 readiness without evidence",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-fountain-pen-intake-custody", "Preserve synthetic intake, custody, accessory, scope, and work-start holds."),
    ("ghc-family-fountain-pen-component-topology", "Quarantine contradictory and orphan component attachments without assembly authority."),
    ("ghc-family-fountain-pen-filling-system-state", "Represent filling-system transitions while refusing physical actuation."),
    ("ghc-family-fountain-pen-material-compatibility", "Reserve material and fluid compatibility plus chemical-safety decisions."),
    ("ghc-family-fountain-pen-condition-observation", "Record bounded visible condition without diagnosis, valuation, or treatment conclusions."),
    ("ghc-family-fountain-pen-cleaning-provenance", "Preserve synthetic tool, fluid, interval, rinse, and waste-route provenance."),
    ("ghc-family-fountain-pen-substitution-challenge", "Retain replacement-source and interchangeability conflicts without authenticity claims."),
    ("ghc-family-fountain-pen-accessible-handover", "Expose structured return history while reserving manual accessibility review."),
    ("ghc-family-fountain-pen-gmut-flow-firewall", "Keep capillary-flow proxies dimensioned and zero-row without physical prediction."),
    ("ghc-family-fountain-pen-authority-reservation", "Fail closed around authentication, treatment, privacy, heritage, remedy, and Māori authority."),
]
SABLE_SKILL_SEEDS = [
    {"name": f"ghc-family-sable-{slug}", "state": "seed_only_not_built_by_auren"}
    for slug in [
        "source-baton-check", "owned-lane-guard", "proposal-freeze", "fixture-boundary", "route-classifier",
        "privacy-reducer", "stale-label-review", "manifest-replay", "truth-label-guard", "caelen-handoff-preflight",
    ]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_fountain_pen_intake_custody.py", "intake-custody-passport"),
    ("ghc_family_fountain_pen_component_topology.py", "component-topology-quarantine"),
    ("ghc_family_fountain_pen_filling_system_state.py", "filling-system-state"),
    ("ghc_family_fountain_pen_material_compatibility.py", "material-compatibility-reservation"),
    ("ghc_family_fountain_pen_condition_observation.py", "cap-barrel-seal-condition"),
    ("ghc_family_fountain_pen_cleaning_provenance.py", "cleaning-provenance"),
    ("ghc_family_fountain_pen_substitution_challenge.py", "replacement-provenance"),
    ("ghc_family_fountain_pen_accessible_handover.py", "accessible-return-handover"),
    ("ghc_family_fountain_pen_gmut_flow_firewall.py", "gmut-capillary-flow-proxy"),
    ("ghc_family_fountain_pen_authority_reservation.py", "pen-authority-ratification-gate"),
]
SABLE_RUNNER_SEEDS = [
    {"name": f"ghc_family_sable_{slug}.py", "state": "seed_only_not_built_by_auren"}
    for slug in ["source_baton_check", "proposal_freeze", "privacy_reducer", "manifest_replay", "caelen_handoff_preflight"]
]

SELF_CLEAN_CATEGORIES = [
    "versioned-name inventory", "family-name preference", "compatibility wrapper retention", "caller evidence",
    "trigger collision review", "stale owner label review", "stale phase label review", "stale route title review",
    "absolute-path privacy review", "raw identifier privacy review", "credential-pattern review", "transcript-pattern review",
    "duplicate proposal review", "duplicate task review", "duplicate skill review", "duplicate runner review",
    "JSON formatting", "Markdown heading order", "source-label consistency", "truth-label consistency",
    "rollback coverage", "protected-gate coverage", "failure-credit consistency", "same-owner labelling",
    "manifest exclusions", "file-cap posture", "document-cap posture", "commit-cap posture",
    "D-first storage posture", "non-destructive cleanup boundary",
]
SELF_CLEAN_TASKS = [
    {"task_id": f"V6592-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
SABLE_CLEAN_SEEDS = [
    {"task_id": f"V6593-SEED-CLEAN-{i:03d}", "title": f"Sable may review and refine {name}", "state": "seed_only_not_executed_by_auren"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("CCI-PLASTICS", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/caring-plastics-rubbers.html", "Plastic and rubber material-care vocabulary only; no treatment, compatibility, safety, or conservation conformance claim."),
    ("CCI-METALS", "official_canadian_conservation_institute", "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html", "Metal condition and corrosion-care vocabulary only; no diagnosis, treatment, safety, or conservation conformance claim."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/pml/special-publication-811", "SI quantity, unit, symbol, and measurement-uncertainty vocabulary."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "General provenance entity, activity, agent, and lineage vocabulary only."),
    ("WCAG22", "official_w3c", "https://www.w3.org/WAI/standards-guidelines/wcag/", "Accessible structure vocabulary with manual and affected-user review reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle and data-minimisation vocabulary; no legal conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty reservation; no Māori authority claim."),
    ("IETF-JCS", "official_ietf", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without signature or credential claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic reverse-chronological tracked-path selection method."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "UTF-8 deterministic JSON parse and serialization implications."),
]

STARTUP_FAILURES = [
    {
        "negative_id": "V6592-X1-N001",
        "signature": "first-tool-call-assumed-unavailable-shell-command-surface",
        "recovery": "Use the installed exec-command surface and keep subsequent repository probes bounded and literal.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X1-N002",
        "signature": "first-activation-baton-read-truncated-after-line-180",
        "recovery": "Read the exact Git object contiguously in bounded forty-line windows through EOF and verify total line and word counts.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X1-N003",
        "signature": "parallel-three-window-baton-render-exceeded-model-context",
        "recovery": "Stop parallel rendering and complete the same immutable baton sequentially with nonoverlapping bounded windows.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X1-N004",
        "signature": "broad-repository-path-discovery-returned-truncated-historical-listing",
        "recovery": "Restrict path discovery to the current v659 source owner, exact phase, and named activation artifacts.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X1-N005",
        "signature": "backend-rejected-write-stdin-control-c-on-noninteractive-session",
        "recovery": "Do not inject control bytes; poll the yielded command with the supported wait surface and inspect its terminal result.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X1-N006",
        "signature": "powershell-materialized-statistics-probe-used-an-empty-pipe-element",
        "recovery": "Materialize the foreach results into a task-specific variable before sorting and projecting bounded scalar output.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X1-N007",
        "signature": "broad-receipt-filename-search-exceeded-useful-owner-local-bound",
        "recovery": "Stop the broad search, inspect the exact owner and phase receipt directory, and verify the successful receipt by supplied SHA-256.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X1-N008",
        "signature": "first-owned-lane-absence-preflight-had-powershell-cast-and-semicolon-parse-error",
        "recovery": "Capture each Git exit code separately, resolve literal branch and path targets, then create one additive Auren-owned worktree from the verified immutable source.",
        "recovery_passed": True,
    },
]

X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6592-X2-N001",
        "signature": "combined-post-x1-equality-wrapper-returned-no-usable-receipt",
        "recovery": "Retain the wrapper failure at zero credit, then split local, upstream, tracking, fresh-live, divergence, ancestry, commit-delta, and cleanliness checks into bounded literal probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X2-N002",
        "signature": "initial-x2-build-wrapper-returned-before-original-child-reached-terminal-state",
        "recovery": "Do not launch a duplicate build or scan; retain the wrapper failure and monitor the exact original Python PID plus declared scan and truth paths until the original process exits.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X2-N003",
        "signature": "bounded-wait-process-wrapper-returned-no-usable-probe-output",
        "recovery": "Retain the wait-wrapper failure, avoid replay, and use direct short PID and exact-artifact probes until the original process exits with one complete scan and truth packet.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X2-N004",
        "signature": "combined-governance-probe-assumed-nonexistent-skill-state-subdirectories",
        "recovery": "Use the exact references/current-roster.json and references/current-state.json locations declared by the fully read roster and authorization skills, then validate them read-only.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X2-N005",
        "signature": "windows-rg-rejected-literal-wildcard-reference-paths",
        "recovery": "Search each exact skill root with a -g '*.md' filter or read the declared reference paths literally; do not pass wildcard text as a Windows path.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6592-X2-N006",
        "signature": "method-flow-validator-and-summary-stdout-exceeded-wrapper-output-budget",
        "recovery": "Keep the complete on-disk receipts, update the changed-input ledger for this retained failure, suppress bulk stdout on the isolated validation and summary commands, and read only exact scalar counts.",
        "recovery_passed": True,
    },
]
