#!/usr/bin/env python3
"""Frozen planning data for Ilyra Fen's v659-v1 phase."""

from __future__ import annotations


PHASE = "v659-v1"
CANONICAL_PHASE = "v659-v1"
PHASE_CODE = "V6591"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary steward and provenance cartographer"
HOPE = (
    "leave every synthetic observation claim traceable, every failed witness visible, "
    "and every professional, cultural, empirical, and Stage 20 gate unmistakable"
)
BRANCH = "codex/GHC-Family/ilyra-fen-v659-v1-full-tools"
PHASE_ROOT = "docs/ilyra-fen/v659-v1"

SOURCE_OWNER = "Lyren Moss"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v658-v8-2-remaster"
SOURCE_FINAL = "4b76b0bd3cc47c8500d04f290f5b7a79329be9b3"
SOURCE_X1 = "3b66443f8adb6c1cc13fd9b872f46565c2b42cfe"
SOURCE_EVIDENCE = "e08a7bb24c9fc9c442374d251b985437a88ade11"
X1_FREEZE = "3406580c1bd9c3bb525125b885216df3c414fef7"
PRIOR_FROZEN = 2910
SOURCE_SEALED_NEGATIVES = 18078
SOURCE_EXTERNAL_NEGATIVES = 3
ACTIVATION_NEGATIVES = SOURCE_SEALED_NEGATIVES + SOURCE_EXTERNAL_NEGATIVES
SOURCE_OPEN_GAPS = 121
SOURCE_EXACT_GATES = 120
SOURCE_SEALED_METHODS = 4352
SOURCE_EXTERNAL_METHODS = 3
ACTIVATION_METHODS = SOURCE_SEALED_METHODS + SOURCE_EXTERNAL_METHODS
SELECTED_INHERITED_COUNT = 20
NEW_UNIQUE_COUNT = 20
CURRENT_PORTFOLIO_COUNT = 40
LATEST_TRACKED_SCAN_CAP = 5000

PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = (
    "synthetic astronomical-observatory calibration, provenance, alert triage, "
    "and night-shift handover"
)

EXPECTED_DISTRIBUTION = {
    "completed": 33,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)

PROTECTED_GATES = [
    "real_people_observers_operators_engineers_communities_affected_parties_and_authorities",
    "real_telescopes_detectors_domes_lasers_archives_observations_images_catalogues_measurements_alerts_or_identifiers",
    "real_observatory_pointing_acquisition_calibration_release_archive_alert_safety_or_shift_decision",
    "professional_astronomy_observatory_engineering_metrology_laser_safety_privacy_security_or_accessibility_authority",
    "empirical_gmut_prediction_likelihood_parameter_constraint_observational_confirmation_or_physical_discovery",
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
        "slug": "observation-plan-expiry-horizon",
        "title": "Ephemeris-bound observing-slot validity window with coordinate-revision refusal",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "target-coordinate revision, ephemeris identifier, slot start and end, superseding plan, and expired-slot refusal",
        "sources": ["IVOA-PROV", "W3C-PROV"],
    },
    {
        "slug": "calibration-lineage-conflict",
        "title": "Bias-dark-flat calibration fan-in ambiguity board with unresolved parent retention",
        "outcome": "completed",
        "pillar": "GMUT Mind and Freed ID",
        "mechanism": "synthetic bias, dark, and flat parent references, competing lineage edges, ambiguity quarantine, and no image-quality verdict",
        "sources": ["FITS-STANDARD", "IVOA-PROV"],
    },
    {
        "slug": "detector-archive-reconciliation",
        "title": "FITS HDU boundary and declared-axis cardinality reconciliation with padding quarantine",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "synthetic header-data-unit offsets, axis cardinality, payload bytes, block padding, unexplained remainder, and archive hold",
        "sources": ["FITS-STANDARD", "IETF-JCS"],
    },
    {
        "slug": "observatory-interlock-reservation",
        "title": "Dome-azimuth, shutter, and mount-slew conflict lattice with command abstention",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "fictional enclosure azimuth, shutter state, mount target sector, conflict lattice, and command refusal",
        "sources": ["W3C-PROV"],
    },
    {
        "slug": "time-scale-reservation",
        "title": "UTC-TAI-TT-UT1 label firewall with bulletin pin and transformation abstention",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "declared time scale, bulletin identity, leap-second table identity, Earth-orientation placeholder, uncertainty flag, and transformation refusal",
        "sources": ["IERS-TIME", "IAU-SOFA"],
    },
    {
        "slug": "seeing-weather-uncertainty",
        "title": "Atmospheric seeing, cloud, and wind interval ledger with go-no-go abstention",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "synthetic seeing, cloud, and wind intervals, SI units, sensor placeholders, uncertainty classes, and no operating decision",
        "sources": ["NIST-SI", "IVOA-PROV"],
    },
    {
        "slug": "optical-hazard-referral",
        "title": "Laser-guide-star beam-window conflict token with aviation and orbital referral hold",
        "outcome": "completed",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "fictional beam window, sky sector, aircraft and satellite conflict placeholders, hold state, and competent-safety referral",
        "sources": ["W3C-PROV"],
    },
    {
        "slug": "image-integrity-envelope",
        "title": "FITS primary-and-extension checksum envelope with header mutation and release quarantine",
        "outcome": "completed",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "synthetic primary and extension HDUs, format revision, byte digests, header mutation witness, challenge route, and release hold",
        "sources": ["FITS-STANDARD", "IETF-JCS", "IVOA-PROV"],
    },
    {
        "slug": "metadata-cultural-review",
        "title": "Source-field, display-label, and place-name provenance split with cultural review reservation",
        "outcome": "completed",
        "pillar": "CBR Heart and Freed ID",
        "mechanism": "source-field digest, translated display label, locale, place-name flag, reviewer placeholder, and no naming authority",
        "sources": ["WCAG22", "TE-MANA-RARAUNGA"],
    },
    {
        "slug": "instrument-custody-turnaround",
        "title": "Detector-filter-grating configuration transition graph with serial discontinuity rejection",
        "outcome": "completed",
        "pillar": "THOS Body and Freed ID",
        "mechanism": "fictional detector, filter, and grating aliases, configuration transitions, serial continuity, orphan isolation, and double-attachment rejection",
        "sources": ["IVOA-PROV", "W3C-PROV"],
    },
    {
        "slug": "calibration-standard-custody",
        "title": "Photometric standard-reference observation chain with unit and uncertainty firewall",
        "outcome": "completed",
        "pillar": "GMUT Mind and THOS Body",
        "mechanism": "synthetic standard-star alias, reference observation, method identifier, SI-compatible unit, uncertainty placeholder, and calibration-result abstention",
        "sources": ["NIST-SI", "IVOA-PROV"],
    },
    {
        "slug": "maintenance-observation-hold",
        "title": "Post-maintenance calibration invalidation window across fictional detector configurations",
        "outcome": "completed",
        "pillar": "THOS Body",
        "mechanism": "fictional detector configuration, maintenance end, calibration validity interval, invalidation edge, hold, and acquisition refusal",
        "sources": ["W3C-PROV"],
    },
    {
        "slug": "provenance-digest-reservation",
        "title": "Canonical FITS-header serialization profile transition with credential abstention",
        "outcome": "completed",
        "pillar": "Freed ID",
        "mechanism": "header canonicalization profile, ordered card image digest, profile version, transition mapping, collision refusal, and no credential claim",
        "sources": ["IETF-JCS", "IVOA-PROV"],
    },
    {
        "slug": "gmut-observation-firewall",
        "title": "Represented dimensioned GMUT sensitivity matrix behind a zero-row observation firewall",
        "outcome": "represented",
        "pillar": "GMUT Mind",
        "mechanism": "dimensioned symbolic parameters, response-matrix placeholders, bounded perturbations, identifiability flags, zero-row state, and physical-inference refusal",
        "sources": ["NIST-SI", "FITS-STANDARD"],
    },
    {
        "slug": "night-handover-workload-proxy",
        "title": "Represented twilight-to-dawn unresolved-alert budget with operatorless handover state",
        "outcome": "represented",
        "pillar": "THOS Body",
        "mechanism": "synthetic twilight checkpoint, unresolved alert classes, acknowledgement placeholders, correction state, retry ceiling, and no human-performance inference",
        "sources": ["W3C-PROV"],
    },
    {
        "slug": "accessible-observation-timeline",
        "title": "Represented multi-extension observation-history table with text chronology alternative",
        "outcome": "represented",
        "pillar": "THOS Body and CBR Heart",
        "mechanism": "caption, scoped headers, extension-to-event links, text chronology, keyboard-order placeholder, and no accessibility-complete claim",
        "sources": ["WCAG22"],
    },
    {
        "slug": "nonproduction-provenance-query",
        "title": "Represented predecessor-sibling-successor astronomy lineage query with disclosure ceiling",
        "outcome": "represented",
        "pillar": "Freed ID and THOS Body",
        "mechanism": "synthetic entity and activity nodes, predecessor, sibling, and successor edges, role placeholders, depth ceiling, and disclosure refusal",
        "sources": ["IVOA-PROV", "W3C-PROV"],
    },
    {
        "slug": "observatory-governance-challenge",
        "title": "Represented contested astronomy-metadata annotation trail with undecided remedy jurisdiction",
        "outcome": "represented",
        "pillar": "CBR Heart",
        "mechanism": "metadata annotation, notice, counterstatement, correction candidate, collective-interest flag, remedy-jurisdiction placeholder, and authority abstention",
        "sources": ["NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
    {
        "slug": "real-observatory-transport-gap",
        "title": "Open gap for real FITS acquisition, calibration lineage, time bulletin, and instrument telemetry transport",
        "outcome": "open_gap",
        "pillar": "All pillars",
        "mechanism": "zero-row FITS and telemetry connectors, disabled network transport, absent calibration and time-bulletin ingestion, absent competent review, and explicit observational gap",
        "sources": ["FITS-STANDARD", "IVOA-PROV", "IERS-TIME", "NIST-SI"],
    },
    {
        "slug": "observatory-authority-ratification-gate",
        "title": "Exact decision-rights gate for astronomical place naming, restricted knowledge, access, hazard, privacy, remedy, and Māori authority",
        "outcome": "exact_gate",
        "pillar": "CBR Heart",
        "mechanism": "place-name and restricted-knowledge flags, access and hazard decisions, affected-party remedy, legal and privacy interpretation, collective governance, and Māori-authority reservations",
        "sources": ["NZ-PRIVACY", "TE-MANA-RARAUNGA"],
    },
]


SELF_SAFE_CATEGORIES = [
    "source-head and live equality", "activation packet raw digest", "proposal-chain parse", "twenty inherited selections",
    "twenty-title novelty audit", "four-label distribution", "workflow-plan policy", "identity boundary",
    "Ilyra-to-Auren route state", "Tavian standby state", "D-first drive posture", "toolchain versions",
    "x1 artifact inventory", "x1 JSON parse", "x1 privacy classes", "x1 stale-label scan",
    "x1 diff hygiene", "x1 manifest replay", "selected-proposal provenance", "new-proposal provenance",
    "source-label glossary", "protected-gate coverage", "failure-retention ledger", "Method Flow witness pairing",
    "wellbeing workload bound", "document-word ceiling", "task-portfolio arithmetic", "skill-plan arithmetic",
    "runner-plan arithmetic", "cleanup-plan arithmetic",
]
SELF_SAFE_TASKS = [
    {"task_id": f"V6591-SAFE-{i:03d}", "title": f"Validate {name} inside the Ilyra-owned v659-v1 lane", "owner": OWNER}
    for i, name in enumerate(SELF_SAFE_CATEGORIES, 1)
]

AUREN_SAFE_CATEGORIES = [
    "source-baton digest", "owned-lane equality", "x1 proposal freeze", "synthetic fixture boundary",
    "main-task route classification", "Sable successor preregistration", "privacy exclusions", "stale-label scan",
    "manifest replay", "exact staged review", "retained failure import", "Method Flow recovery",
    "truth-label distribution", "wellbeing workload bound", "skill inventory", "runner inventory",
    "latest-5000 scan plan", "zero-real-data assertion", "authority reservations", "terminal no-replay gate",
]
AUREN_SAFE_SEEDS = [
    {"task_id": f"V6592-SEED-SAFE-{i:03d}", "title": f"Auren may evaluate {name} in their own v659-v2 lane", "owner": "Auren Lark", "state": "seed_only_not_executed_by_ilyra"}
    for i, name in enumerate(AUREN_SAFE_CATEGORIES, 1)
]

SELF_CANDIDATE_CATEGORIES = [
    "expiry-aware observation reducer", "calibration conflict visual summary", "detector archive abstention matrix",
    "interlock reservation graph", "time-scale source-pin panel", "seeing uncertainty envelope",
    "optical hazard referral state machine", "image integrity envelope", "metadata cultural-review queue",
    "provenance event deduplicator",
]
SELF_CANDIDATE_TASKS = [
    {"task_id": f"V6591-CAND-{i:03d}", "title": f"Build and test reversible {name}", "owner": OWNER}
    for i, name in enumerate(SELF_CANDIDATE_CATEGORIES, 1)
]
AUREN_CANDIDATE_SEEDS = [
    {"task_id": f"V6592-SEED-CAND-{i:03d}", "title": f"Auren may prototype reversible {name}", "owner": "Auren Lark", "state": "seed_only_not_executed_by_ilyra"}
    for i, name in enumerate([
        "baton parser", "phase-source verifier", "proposal-selection ledger", "bounded file-scan receipt", "authority-gate atlas",
        "privacy-class reducer", "stale-label classifier", "manifest batch replay", "same-owner evidence labeler", "Sable handoff preflight",
    ], 1)
]

EXACT_QUEUE = [
    {"task_id": f"V6591-EXACT-{i:03d}", "title": title, "state": "exact_gate_unexecuted"}
    for i, title in enumerate([
        "Use real observatory records or observations", "Issue a real telescope operating decision",
        "Approve a laser or workplace-safety action", "Publish a real astronomical discovery claim",
        "Make a professional calibration determination", "Publish personal or protected data",
        "Allocate legal or cultural naming authority", "Make a Māori data-governance decision",
        "Deploy a production identity or archive system", "Perform destructive shared-drive cleanup",
    ], 1)
]
BLOCKED_QUEUE = [
    {"task_id": f"V6591-BLOCK-{i:03d}", "title": title, "state": "blocked_unexecuted"}
    for i, title in enumerate([
        "Fabricate empirical GMUT confirmation", "Claim consciousness or personhood from task language",
        "Merge or erase sibling identities", "Publish credentials or private callable routes",
        "Declare Stage 20 readiness without evidence",
    ], 1)
]

SELF_SKILL_SPECS = [
    ("ghc-family-observation-expiry-firewall", "Enforce review horizons and stale-observation-plan refusal."),
    ("ghc-family-calibration-conflict-quarantine", "Preserve contradictory calibration lineages without silent acceptance."),
    ("ghc-family-detector-archive-reconciliation", "Check synthetic byte and frame balances while refusing quality conclusions."),
    ("ghc-family-observatory-interlock-reservation", "Represent fictional interlock conflicts without operating authority."),
    ("ghc-family-time-scale-reservation", "Pin time-scale sources and refuse unsupported conversion."),
    ("ghc-family-seeing-uncertainty", "Preserve synthetic seeing and weather uncertainty with suitability abstention."),
    ("ghc-family-optical-hazard-referral", "Fail closed around fictional optical alerts and professional referral."),
    ("ghc-family-image-integrity-envelope", "Preserve synthetic image digests, custody, challenges, and publication holds."),
    ("ghc-family-metadata-cultural-review", "Pin metadata sources and reserve cultural and naming authority."),
    ("ghc-family-observation-provenance-scan", "Select and scan at most the latest 5,000 tracked paths deterministically."),
]
AUREN_SKILL_SEEDS = [
    {"name": f"ghc-family-auren-{slug}", "state": "seed_only_not_built_by_ilyra"}
    for slug in [
        "source-baton-check", "owned-lane-guard", "proposal-freeze", "fixture-boundary", "route-classifier",
        "privacy-reducer", "stale-label-review", "manifest-replay", "truth-label-guard", "sable-handoff-preflight",
    ]
]
SELF_RUNNER_SPECS = [
    ("ghc_family_observation_expiry_firewall.py", "observation-plan-expiry-horizon"),
    ("ghc_family_calibration_conflict_quarantine.py", "calibration-lineage-conflict"),
    ("ghc_family_detector_archive_reconciliation.py", "detector-archive-reconciliation"),
    ("ghc_family_observatory_interlock_reservation.py", "observatory-interlock-reservation"),
    ("ghc_family_time_scale_reservation.py", "time-scale-reservation"),
    ("ghc_family_seeing_uncertainty.py", "seeing-weather-uncertainty"),
    ("ghc_family_optical_hazard_referral.py", "optical-hazard-referral"),
    ("ghc_family_image_integrity_envelope.py", "image-integrity-envelope"),
    ("ghc_family_metadata_cultural_review.py", "metadata-cultural-review"),
    ("ghc_family_observation_provenance_scan.py", "latest-5000-file-scope"),
]
AUREN_RUNNER_SEEDS = [
    {"name": f"ghc_family_auren_{slug}.py", "state": "seed_only_not_built_by_ilyra"}
    for slug in ["source_baton_check", "proposal_freeze", "privacy_reducer", "manifest_replay", "sable_handoff_preflight"]
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
    {"task_id": f"V6591-CLEAN-{i:03d}", "title": f"Review and refine {name}", "state": "planned_x2_additive_only"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]
AUREN_CLEAN_SEEDS = [
    {"task_id": f"V6592-SEED-CLEAN-{i:03d}", "title": f"Auren may review and refine {name}", "state": "seed_only_not_executed_by_ilyra"}
    for i, name in enumerate(SELF_CLEAN_CATEGORIES, 1)
]

OFFICIAL_SOURCES = [
    ("FITS-STANDARD", "official_nasa_iau_fits", "https://fits.gsfc.nasa.gov/fits_standard.html", "FITS structure, header, array, table, and transport vocabulary only; no conformance claim."),
    ("IVOA-PROV", "official_ivoa_recommendation", "https://www.ivoa.net/documents/ProvenanceDM/", "Astronomical entity, activity, agent-role, lineage, and exchange vocabulary."),
    ("IAU-SOFA", "official_iau_sofa", "https://www.iausofa.org/", "Fundamental-astronomy algorithm and time-scale vocabulary only; no operational computation claim."),
    ("IERS-TIME", "official_iers", "https://www.iers.org/", "Earth-orientation and leap-second bulletin source vocabulary with no live conversion."),
    ("NIST-SI", "official_nist", "https://www.nist.gov/pml/special-publication-811", "SI quantity, unit, symbol, and measurement-uncertainty vocabulary."),
    ("W3C-PROV", "official_w3c", "https://www.w3.org/TR/prov-o/", "General provenance entity, activity, agent, and lineage vocabulary."),
    ("WCAG22", "official_w3c", "https://www.w3.org/WAI/standards-guidelines/wcag/", "Accessible structure vocabulary with manual and affected-user review reserved."),
    ("NZ-PRIVACY", "official_nz_privacy_commissioner", "https://www.privacy.org.nz/privacy-principles/", "Current New Zealand privacy-principle and data-minimisation vocabulary; no legal conclusion."),
    ("TE-MANA-RARAUNGA", "primary_maori_data_sovereignty_network", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Māori data-sovereignty reservation; no Māori authority claim."),
    ("IETF-JCS", "official_ietf", "https://www.rfc-editor.org/rfc/rfc8785", "Canonical JSON digest vocabulary without signature or credential claims."),
    ("GIT-LOG", "official_git_docs", "https://git-scm.com/docs/git-log", "Deterministic reverse-chronological tracked-path selection method."),
    ("PYTHON-JSON", "official_python_docs", "https://docs.python.org/3/library/json.html", "UTF-8 deterministic JSON parse and serialization implications."),
]

STARTUP_FAILURES = [
    {
        "negative_id": "V6591-X1-N001",
        "signature": "broad-memory-registry-search-output-truncated",
        "recovery": "Use one fixed keyword at a time, cap lines, and open only the one directly referenced rollout summary.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N002",
        "signature": "current-roster-active-state-unsupported-by-validator",
        "recovery": "Additively align the roster checker and schema with the sanitized acknowledged-active current-state vocabulary, preserving all historical delivery states and route meaning.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N003",
        "signature": "powershell-python-c-quote-stripping-in-manifest-replay",
        "recovery": "Feed the unchanged ASCII verifier through python -X utf8 stdin and retain raw Git cat-file batch framing.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N004",
        "signature": "external-canonical-receipt-filename-assumption-wrong",
        "recovery": "Hash the bounded receipt directory and select the artifact by the supplied SHA-256 instead of guessing its filename.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N005",
        "signature": "combined-large-worktree-postflight-wrapper-returned-no-result",
        "recovery": "Inspect concrete Git processes and locks, then split registration, index, status, and tracked-count probes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N006",
        "signature": "worktree-add-progress-stream-ended-before-index-finalization",
        "recovery": "Do not retry; inspect path, branch, HEAD, index lock, final index, process state, tracked count, and cleanliness until the original add completes.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N007",
        "signature": "first-x1-build-rejected-semantic-neighbor-title-collisions",
        "recovery": "Retain the failed freeze attempt at zero credit, rewrite the astronomy proposals around domain-specific FITS, ephemeris, instrument-configuration, time-scale, and decision-right mechanisms, and rerun the unchanged all-title novelty gate before any x1 freeze.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N008",
        "signature": "windows-rg-literal-wildcard-path-rejected",
        "recovery": "Pass each scripts directory as a literal search root and express the Python filename filter with rg -g '*.py'.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N009",
        "signature": "parallel-direct-py-entrypoints-returned-incomplete-artifact-set",
        "recovery": "Invoke each Python skill entrypoint explicitly with python -X utf8, keep independent output directories, and verify the exact output inventory before credit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N010",
        "signature": "phase-request-output-supplied-to-special-packet-validator",
        "recovery": "Use the workflow refinement engine self-test plus its generic phase-request validation receipt; reserve the special packet validator for its declared raw-audit and normalized-pass bundle layout.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N011",
        "signature": "x1-source-ledger-test-referenced-nonexistent-source-specs-constant",
        "recovery": "Inspect the frozen module's exact exported names, bind the unchanged row-count assertion to OFFICIAL_SOURCES, and rerun only the scoped x1 module.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N012",
        "signature": "combined-staged-git-show-per-path-verifier-returned-no-receipt-at-timeout",
        "recovery": "Split diff hygiene from content replay, build one staged index object map, and drain one bounded git cat-file --batch stream for JSON, manifest, and privacy checks.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X1-N013",
        "signature": "first-batch-staged-replay-found-checkout-blob-domain-drift-and-scanner-definition-candidate",
        "recovery": "Declare LF-normalized Git-clean manifest bytes, replay staged blobs in one batch, classify scanner-rule definitions as visible candidates, and require zero confirmed payload hits.",
        "recovery_passed": True,
    },
]

X2_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6591-X2-N001",
        "signature": "post-x1-four-way-wrapper-left-unquoted-powershell-upstream-revision",
        "recovery": "Quote the complete HEAD...@{u} revision argument and keep the fresh live-remote lookup in a separate bounded command.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N002",
        "signature": "powershell-get-item-values-array-coerced-to-one-combined-path",
        "recovery": "Pass the concrete destination array directly to -LiteralPath and inspect the four copied files independently.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N003",
        "signature": "latest-file-scan-wrapper-returned-before-original-child-completed",
        "recovery": "Do not launch a duplicate scan; retain the wrapper failure at zero credit and monitor the exact original process and receipt path until one bounded terminal state is observable.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N004",
        "signature": "immediate-latest-file-scan-receipt-read-raced-the-live-child",
        "recovery": "Treat the missing receipt as an incomplete live attempt, not a failed scan result, and inspect the original process plus exact output path before reading.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N005",
        "signature": "bounded-wait-process-wrapper-ended-without-result-while-scan-remained-live",
        "recovery": "Preserve the wait failure, avoid replay, and use short process and artifact probes until the original scan exits and its complete receipt parses.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N006",
        "signature": "broad-roster-validator-search-output-truncated-before-state-context",
        "recovery": "Search one validator keyword set, then read only the exact allowed-state and validation line windows from the script and schema.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N007",
        "signature": "first-meta-tool-collision-pass-treated-shared-boundary-boilerplate-as-forty-five-trigger-collisions",
        "recovery": "Exclude declared boundary boilerplate from trigger similarity, recognize exact skill-runner companion names, and rerun only collision analysis while retaining the first advisory receipt at zero credit.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N008",
        "signature": "first-meta-tool-refinement-patch-used-a-stale-owner-line-preimage",
        "recovery": "Inspect the exact bounded function window, update the patch preimage, and apply only the generic owner, phase, runner-discovery, evidence-state, and collision refinements.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N009",
        "signature": "family-index-x1-output-directory-suffix-assumption-was-absent",
        "recovery": "Retain the lookup miss, locate the exact prior family-index artifacts with a bounded file list, and invoke the documented builder into a new explicit x2 output directory.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N010",
        "signature": "method-flow-validator-and-summary-printed-complete-large-receipts-and-truncated-wrapper-output",
        "recovery": "Keep the complete on-disk receipts, suppress bulk stdout on the bounded rerun, and read only scalar validation counts from the exact JSON files.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N011",
        "signature": "first-x2-git-add-emitted-hundreds-of-line-ending-warnings-and-truncated-wrapper-output",
        "recovery": "Inspect the completed index state, retain the successful add without replay credit, and use core.safecrlf=false only for the later exact restage while verifying Git-clean blob hashes directly.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N012",
        "signature": "first-staged-cat-file-batch-wrapper-deadlocked-on-bidirectional-pipe-backpressure",
        "recovery": "Stop only the verified owner-local verifier processes, retain the deadlock at zero credit, and use subprocess communicate semantics so batch input and large blob output drain concurrently.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N013",
        "signature": "second-staged-verifier-required-full-owner-manifest-paths-to-all-be-in-the-x2-delta",
        "recovery": "Verify the complete manifest against current index blobs while checking the 248-path staged delta independently; retain the 39 unchanged x1 paths as covered current content.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6591-X2-N014",
        "signature": "first-current-index-coverage-repair-subtracted-a-list-from-a-set",
        "recovery": "Keep missing-index paths as a set through coverage arithmetic, then emit only deterministic scalar counts from the unchanged staged packet.",
        "recovery_passed": True,
    },
]
