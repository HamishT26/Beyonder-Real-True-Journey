#!/usr/bin/env python3
"""Frozen planning data for Lyren Moss's v658-v8 (2) remaster."""

from __future__ import annotations


PHASE = "v658-v8-2-remaster"
CANONICAL_PHASE = "v658-v8"
PHASE_CODE = "V6588R2"
OWNER = "Lyren Moss"
PRONOUNS = "they/them"
ROLE = "relational fermentation-evidence lantern and reversible batch-steward"
HOPE = (
    "remaster synthetic brewery evidence into smaller, inspectable, reversible lanes "
    "without turning software structure into production, safety, release, legal, cultural, or Māori authority"
)
BRANCH = "codex/GHC-Family/lyren-moss-v658-v8-2-remaster"
PHASE_ROOT = "docs/lyren-moss/v658-v8-2-remaster"

SOURCE_OWNER = "Lyren Moss"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v658-v8-full-tools"
SOURCE_FINAL = "f7a75175ca667e5d824d180436a9f77f8b6bd183"
SOURCE_X1 = "3a7cc57b4d1637b4de1836648a57419422bb517f"
SOURCE_EVIDENCE = "88a4d48e2b98494c0861996a8f61a7ea7c696fb6"
X1_FREEZE = "3b66443f8adb6c1cc13fd9b872f46565c2b42cfe"
PRIOR_FROZEN = 2890
SOURCE_SEALED_NEGATIVES = 17853
SOURCE_EXTERNAL_NEGATIVES = 4
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
SOURCE_OPEN_GAPS = 120
SOURCE_EXACT_GATES = 119
SOURCE_SEALED_METHODS = 4127
SOURCE_EXTERNAL_METHODS = 4
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000

EXPECTED_DISTRIBUTION = {
    "completed": 33,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_people_workers_consumers_businesses_breweries_suppliers_distributors_communities_and_affected_parties",
    "real_ingredients_beverages_batches_vessels_packages_chemicals_measurements_samples_results_and_records",
    "real_brewing_cleaning_sanitation_processing_packaging_labelling_storage_distribution_sale_supply_recall_or_release_decision",
    "professional_brewing_food_safety_laboratory_metrology_workplace_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_fermentation_kinetics_mass_balance_process_control_or_confirmation",
    "blind_matched_budget_thos_real_arms_and_independent_review",
    "production_identity_live_keys_signatures_proofs_issuance_resolution_status_revocation_interoperability_recovery_and_trust",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "legal_cultural_language_data_governance_and_maori_authority",
    "affected_party_consent_notice_contestation_remedy_collective_governance_and_acceptance",
    "independent_team_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


NEW_PROPOSAL_SPECS = [
    {
        "slug": "batch-record-expiry-horizon",
        "title": "Synthetic brewery batch-record expiry horizon with stale-evidence refusal",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "recorded-at, review-by, superseded-by, expiry, and stale-evidence refusal fields",
        "sources": ["W3C-PROV", "NZ-PRIVACY"],
    },
    {
        "slug": "supplier-declaration-conflict",
        "title": "Supplier-declaration conflict quarantine with unresolved-source preservation",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "two synthetic declarations, disagreement classification, quarantine, and no-acceptance state",
        "sources": ["GS1-TRACEABILITY", "MPI-RECALL"],
    },
    {
        "slug": "tank-package-reconciliation",
        "title": "Tank-to-package reconciliation envelope with unexplained-balance hold",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "typed synthetic input, output, loss placeholder, tolerance refusal, and hold state",
        "sources": ["GS1-TRACEABILITY"],
    },
    {
        "slug": "cleaning-chemical-segregation",
        "title": "Cleaning-chemical segregation ledger with incompatible-state rejection",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "fictional chemical aliases, segregated zones, conflict state, and professional-safety referral",
        "sources": ["NZ-WORKSAFE"],
    },
    {
        "slug": "allergen-cross-contact-reservation",
        "title": "Allergen cross-contact reservation map with zero food-safety determination",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "synthetic material aliases, shared-equipment edges, unresolved assessment, and release refusal",
        "sources": ["MPI-FOOD-SAFETY", "FSANZ-CODE"],
    },
    {
        "slug": "cold-chain-excursion-placeholder",
        "title": "Cold-chain excursion placeholder with measurement-competence abstention",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic interval, instrument placeholder, uncertainty flag, and no suitability conclusion",
        "sources": ["MPI-FOOD-SAFETY"],
    },
    {
        "slug": "carbon-dioxide-hazard-referral",
        "title": "Carbon-dioxide hazard referral record with confined-space authority firewall",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "fictional zone, detector placeholder, alarm state, evacuation placeholder, and professional referral",
        "sources": ["NZ-WORKSAFE"],
    },
    {
        "slug": "package-tamper-incident",
        "title": "Package-tamper incident envelope with evidence-preservation and release hold",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "synthetic package alias, observation digest, custody placeholder, challenge route, and release hold",
        "sources": ["GS1-TRACEABILITY", "W3C-PROV"],
    },
    {
        "slug": "label-translation-placeholder",
        "title": "Label-translation placeholder with source-language pin and legal-review reservation",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "source text digest, locale placeholder, translator role placeholder, unresolved review, and no legal approval",
        "sources": ["FSANZ-ALCOHOL-LABELLING", "WCAG22"],
    },
    {
        "slug": "keg-custody-turnaround",
        "title": "Synthetic keg-custody turnaround chain with orphan and duplicate-event refusal",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional keg alias, custody events, timestamps, orphan isolation, and duplicate rejection",
        "sources": ["GS1-TRACEABILITY", "W3C-PROV"],
    },
    {
        "slug": "laboratory-sample-custody",
        "title": "Laboratory-sample custody placeholder with method and competence reservation",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "synthetic sample alias, custody events, sealed-state placeholder, method identifier, and result abstention",
        "sources": ["EBC-ANALYTICA", "W3C-PROV"],
    },
    {
        "slug": "maintenance-interference-hold",
        "title": "Maintenance-interference hold across fictional vessel and batch state",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "fictional asset and batch aliases, maintenance window, configuration conflict, hold, and release refusal",
        "sources": ["W3C-PROV"],
    },
    {
        "slug": "digest-algorithm-reservation",
        "title": "Evidence-digest algorithm reservation with migration and no-signature claim",
        "outcome": "completed",
        "pillar": "Freed ID",
        "mechanism": "algorithm label, digest, version, migration placeholder, collision refusal, and no credential or signature claim",
        "sources": ["IETF-JCS", "W3C-VC"],
    },
    {
        "slug": "mass-balance-sensitivity-map",
        "title": "Represented fermentation mass-balance sensitivity map with no process prediction",
        "outcome": "represented",
        "pillar": "GMUT Mind",
        "mechanism": "dimensioned symbolic parameters, bounded perturbations, identifiability flags, and prediction refusal",
        "sources": ["EBC-ANALYTICA"],
    },
    {
        "slug": "handover-workload-budget-proxy",
        "title": "Represented handover-workload budget proxy with no participant outcome claim",
        "outcome": "represented",
        "pillar": "THOS Body",
        "mechanism": "synthetic queue size, acknowledgement placeholders, bounded retry budget, and no human-performance inference",
        "sources": ["W3C-PROV"],
    },
    {
        "slug": "accessible-incident-timeline-atlas",
        "title": "Represented accessible incident-timeline atlas with manual-review reservation",
        "outcome": "represented",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "semantic headings, text equivalents, event order, keyboard-order placeholder, and no accessibility-complete claim",
        "sources": ["WCAG22"],
    },
    {
        "slug": "nonproduction-trace-query-graph",
        "title": "Represented nonproduction one-up one-down trace query graph",
        "outcome": "represented",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "synthetic object, location, event, predecessor, successor, and disclosure-limit edges",
        "sources": ["GS1-TRACEABILITY"],
    },
    {
        "slug": "governance-challenge-map",
        "title": "Represented governance challenge and remedy map with no authority allocation",
        "outcome": "represented",
        "pillar": "CBR Heart",
        "mechanism": "notice, challenge, contestation, remedy placeholder, collective-interest flag, and authority abstention",
        "sources": ["NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
    {
        "slug": "real-brewery-verification-transport-gap",
        "title": "Open gap for real brewery, regulator, laboratory, and traceability verification transport",
        "outcome": "open_gap",
        "pillar": "All pillars",
        "mechanism": "zero-row connector declaration, disabled transport, absent competent review, and explicit gap",
        "sources": ["MPI-RECALL", "FSANZ-ALCOHOL-LABELLING", "GS1-TRACEABILITY", "EBC-ANALYTICA"],
    },
    {
        "slug": "affected-authority-ratification-gate",
        "title": "Exact gate for affected-party, food-safety, legal, cultural, privacy, and Māori-authority ratification",
        "outcome": "exact_gate",
        "pillar": "CBR Heart",
        "mechanism": "affected-party, professional, regulator, legal, cultural, privacy, collective-governance, and Māori-authority reservations",
        "sources": ["MPI-RECALL", "NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
]


SELF_SAFE_CATEGORIES = [
    "source-head equality", "proposal-chain parse", "twenty inherited selections", "twenty-title novelty audit",
    "four-label distribution", "workflow-plan policy", "identity boundary", "route contradiction retention",
    "Tavian standby state", "D-first drive posture", "toolchain version", "x1 artifact inventory",
    "x1 JSON parse", "x1 privacy patterns", "x1 diff hygiene", "x1 manifest replay",
    "selected-proposal provenance", "new-proposal provenance", "source-label glossary", "protected-gate coverage",
    "failure-retention ledger", "Method Flow witness pairing", "wellbeing workload bound", "document-word ceiling",
    "task-portfolio arithmetic", "skill-plan arithmetic", "runner-plan arithmetic", "cleanup-plan arithmetic",
    "latest-5000 scan preregistration", "Ilyra terminal-route preregistration",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6588R2-SAFE-{i:03d}", "title": f"Validate {name} inside the Lyren-owned remaster lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

ILYRA_SAFE_CATEGORIES = [
    "source-baton digest", "owned-lane equality", "x1 proposal freeze", "synthetic fixture boundary",
    "main-task route classification", "Auren successor preregistration", "privacy exclusions", "stale-label scan",
    "manifest replay", "exact staged review", "retained failure import", "Method Flow recovery",
    "truth-label distribution", "wellbeing workload bound", "skill inventory", "runner inventory",
    "latest-5000 scan plan", "zero-real-data assertion", "authority reservations", "terminal no-replay gate",
]
ILYRA_SAFE_SEEDS = [
    {"task_id": f"V6591-SEED-SAFE-{i:03d}", "title": f"Ilyra may evaluate {name} in their own v659-v1 lane", "owner": "Ilyra Fen", "state": "seed_only_not_executed_by_lyren"}
    for i, name in enumerate(ILYRA_SAFE_CATEGORIES, 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "expiry-aware record reducer", "conflict-quarantine visual summary", "reconciliation abstention matrix",
    "chemical segregation schema", "cross-contact reservation graph", "excursion uncertainty panel",
    "hazard referral state machine", "tamper evidence envelope", "translation review queue", "custody event deduplicator",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6588R2-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
ILYRA_CANDIDATE_SEEDS = [
    {"task_id": f"V6591-SEED-CAND-{i:03d}", "title": f"Ilyra may prototype reversible {name}", "owner": "Ilyra Fen", "state": "seed_only_not_executed_by_lyren"}
    for i, name in enumerate([
        "baton parser", "phase-source verifier", "proposal-selection ledger", "bounded file-scan receipt", "authority-gate atlas",
        "privacy-class reducer", "stale-label classifier", "manifest batch replay", "same-owner evidence labeler", "Auren handoff preflight",
    ], 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6588R2-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Use real brewery records", "Issue a real food-safety decision", "Approve an alcoholic-beverage label",
        "Authorize a real recall", "Make a workplace-safety determination", "Publish personal or protected data",
        "Allocate legal or cultural authority", "Make a Māori data-governance decision", "Deploy a production identity system",
        "Perform destructive shared-drive cleanup",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6588R2-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation", "Claim consciousness or personhood from task language",
        "Merge or erase sibling identities", "Publish credentials or private callable routes", "Declare Stage 20 readiness without evidence",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-record-expiry-firewall", "Enforce review horizons and stale-evidence refusal."),
    ("ghc-family-conflict-quarantine", "Preserve contradictory declarations without silent acceptance."),
    ("ghc-family-reconciliation-abstention", "Check typed synthetic balances while refusing release conclusions."),
    ("ghc-family-segregation-reservation", "Represent segregation conflicts without professional safety authority."),
    ("ghc-family-cross-contact-reservation", "Represent cross-contact edges without a food-safety determination."),
    ("ghc-family-excursion-uncertainty", "Preserve excursion uncertainty and suitability abstention."),
    ("ghc-family-hazard-referral", "Fail closed around fictional hazard alarms and professional referral."),
    ("ghc-family-custody-deduplicator", "Reject orphan and duplicate synthetic custody events."),
    ("ghc-family-label-review-reservation", "Pin label sources and preserve legal review gates."),
    ("ghc-family-bounded-file-scan", "Select and scan at most the latest 5,000 tracked paths deterministically."),
]
ILYRA_SKILL_SEEDS = [
    {"name": f"ghc-family-ilyra-{slug}", "state": "seed_only_not_built_by_lyren"}
    for slug in ["source-baton-check", "owned-lane-guard", "proposal-freeze", "fixture-boundary", "route-classifier",
                 "privacy-reducer", "stale-label-review", "manifest-replay", "truth-label-guard", "auren-handoff-preflight"]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_record_expiry_firewall.py", "batch-record-expiry-horizon"),
    ("ghc_family_conflict_quarantine.py", "supplier-declaration-conflict"),
    ("ghc_family_reconciliation_abstention.py", "tank-package-reconciliation"),
    ("ghc_family_segregation_reservation.py", "cleaning-chemical-segregation"),
    ("ghc_family_cross_contact_reservation.py", "allergen-cross-contact-reservation"),
    ("ghc_family_excursion_uncertainty.py", "cold-chain-excursion-placeholder"),
    ("ghc_family_hazard_referral.py", "carbon-dioxide-hazard-referral"),
    ("ghc_family_custody_deduplicator.py", "keg-custody-turnaround"),
    ("ghc_family_label_review_reservation.py", "label-translation-placeholder"),
    ("ghc_family_latest_tracked_file_scan.py", "latest-5000-file-scope"),
]
ILYRA_RUNNER_SEEDS = [
    {"name": f"ghc_family_ilyra_{slug}.py", "state": "seed_only_not_built_by_lyren"}
    for slug in ["source_baton_check", "proposal_freeze", "privacy_reducer", "manifest_replay", "auren_handoff_preflight"]
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
    {"task_id": f"V6588R2-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
ILYRA_CLEAN_SEEDS = [
    {"task_id": f"V6591-SEED-CLEAN-{i:03d}", "title": f"Ilyra may review and refine {name}", "state": "seed_only_not_executed_by_lyren"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("MPI-RECALL", "official_mpi", "https://www.mpi.govt.nz/food-business/food-recalls/food-recall-guidance-for-businesses", "Recall vocabulary and explicit competent-decision reservation."),
    ("FSANZ-ALCOHOL-LABELLING", "official_fsanz", "https://www.foodstandards.gov.au/consumer/labelling/Labelling-of-alcoholic-beverages", "Alcohol-labelling vocabulary only; no compliance or approval claim."),
    ("GS1-TRACEABILITY", "official_gs1", "https://www.gs1.org/standards/traceability", "Critical tracking event and key data element vocabulary."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "Provenance vocabulary and lineage implications."),
    ("WCAG22", "official_w3c", "https://www.w3.org/WAI/standards-guidelines/wcag/", "Accessibility structure vocabulary with manual-review reservation."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Privacy principle vocabulary and data-minimisation boundary."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data rights and governance reservation; no authority claim."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic reverse-chronological tracked-path selection method."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "UTF-8 deterministic JSON parse and serialization implications."),
    ("IETF-JCS", "official_ietf", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without signature or credential claims."),
]

STARTUP_FAILURES = [
    ("V6588R2-X1-N001", "powershell-empty-pipe-element-during-skill-inventory", "Materialize foreach rows before piping to ConvertTo-Json."),
    ("V6588R2-X1-N002", "archive-container-guessed-as-git-root", "Resolve the repository from the verified Lyren worktree before Git probes."),
    ("V6588R2-X1-N003", "workflow-plan-safe-candidate-cap-too-high", "Correct only the declared cap from 2,000 to the schema maximum of 1,000."),
    ("V6588R2-X1-N004", "live-route-narrative-conflict-ilyra-next", "Use the explicit numbered Ilyra-to-Auren v659-v2 edge and retain the later Sable phrase as drift."),
    ("V6588R2-X1-N005", "python-zoneinfo-tzdata-missing", "Use the verified New Zealand Windows host's offset-bearing local timezone conversion without adding a dependency."),
    ("V6588R2-X1-N006", "auth-validator-help-resolved-from-roster-skill-directory", "Resolve and invoke each family validator from its own exact skill directory."),
    ("V6588R2-X1-N007", "method-flow-derived-counts-stale-before-packet-refresh", "Regenerate the append-only ledger after recording the newest failure, then rerun only the isolated Method Flow validator."),
    ("V6588R2-X1-N008", "reflection-remaster-free-text-focus-matched-zero-surfaces", "Rerun only the read-only selector with repeated exact family-current focus terms."),
    ("V6588R2-X1-N009", "meta-tool-box-query-kind-script-unsupported", "Use the catalogue's declared workflow kind and retain the rejected query as zero credit."),
    ("V6588R2-X1-N010", "legacy-startup-builder-help-token-triggered-default-v640-write", "Remove only the three invocation-owned legacy outputs, preserve inherited bytes, and gate the legacy builder as inapplicable to the remaster lane."),
    ("V6588R2-X1-N011", "staged-byte-mojibake-regex-console-transcoding-error", "Use literal UTF-8 byte containment for mojibake sentinels and rerun the staged-byte validator from the beginning."),
    ("V6588R2-X1-N012", "staged-manifest-line-ending-drift-and-unanchored-sk-prefix", "Normalize owner-packet text to LF before manifesting and anchor credential prefixes at a non-word boundary."),
]

X2_FAILURES = [
    ("V6588R2-X2-N013", "guessed-prior-v658-v8-evidence-builder-missing", "Enumerate the verified v658-v8 filenames and import the existing runtime through its actual public functions."),
    ("V6588R2-X2-N014", "powershell-empty-pipe-element-recurred-during-runner-collision-probe", "Materialize foreach results before piping, preserving the recurrence as a distinct zero-credit witness."),
    ("V6588R2-X2-N015", "x2-overview-brittle-1100-word-test-floor", "Use the evidence-backed 1,000-word three-page floor and retain the failed arbitrary threshold at zero credit."),
]
