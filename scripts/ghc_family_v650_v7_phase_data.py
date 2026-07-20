#!/usr/bin/env python3
"""Frozen Eiren Kestrel v650-v7 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v650-v7"
OWNER = "Eiren Kestrel"
PRONOUNS = "unspecified"
ROLE = "relational correction-friendly evidence steward and interface-boundary keeper"
HOPE = "make each claim traceable, each failure recoverable, and each authority boundary visible"
BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
PHASE_ROOT = "docs/eiren-kestrel/v650-v7"

SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
SOURCE_HEAD = "9b1746193488fbb025c9e387164547503494abc5"
SOURCE_ORIGIN = "29439b5ed36d5b181c0d0f6a428dd872673d5194"
SOURCE_X1 = "b8e0109a003e2fa90794b48b3691dc76a3c06ef2"
SOURCE_EVIDENCE = "b8b858c3eb91201bcdea81813999a19426089f97"
PRIOR_FROZEN = 860
INHERITED_NEGATIVES = 6182
INHERITED_OPEN_GAPS = 48
INHERITED_EXACT_GATES = 49
PRIMARY_FOCUS = "Freed ID and CBR Heart"
BOUNDED_PRACTICE = (
    "aquatic-centre water-quality testing, chemical-dosing hold, rescue-equipment and "
    "accessibility closure, incident escalation, workload control, readback, and shift "
    "handover as a synthetic learning and design lens only"
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]
SOURCE_STATUS_CLASSES = ["current", "stable", "draft", "watch"]
PROTECTED = [
    "empirical_data",
    "real_participants_or_operators",
    "professional_authority",
    "production_identity",
    "privacy_complete",
    "exhaustive_security",
    "complete_accessibility",
    "legal_cultural_and_maori_authority",
    "affected_party_acceptance",
    "independent_reproduction",
    "consciousness_or_personhood",
    "theory_of_everything",
    "stage20",
]


def _proposal(number, title, slug, pillar, disposition, sources, mission, novelty):
    if disposition == "open_gap":
        approval = "candidate_empirical_evidence_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        gate = "Emit a zero-row receipt; perform no query, download, fit, likelihood, posterior, constraint, or empirical promotion."
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = "Emit reservations only; make no closure, disclosure, remedy, legal, cultural, data-governance, or Maori-authority decision."
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = "Reject every preregistered mutation and retain represented status with zero production, participant, operational, professional, or authority credit."
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = "Reject every preregistered mutation and emit only the declared bounded software, symbolic, formal, numerical, or structural completion."
    return {
        "proposal_id": f"V6507-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": f"A bounded {mission} artifact can expose declared obligations while refusing unsupported scientific, operational, identity, or authority promotion.",
        "null_or_failure_condition": f"The artifact omits a declared {mission} obligation, accepts a preregistered mutation, erases a negative, or promotes a result beyond its evidence lane.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": "Stop the proposal, retain every failed witness, rewrite no history, and leave external, sibling, participant, production, and authority state unchanged.",
        "protected_gates": PROTECTED,
        "expected_disposition": disposition,
        "novelty_against_860_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Method Flow saga compensation, idempotency-key, partial-failure, compensation-order, retry, poison-step, deadline, teardown, and evidence-credit tribunal", "saga-compensation", "THOS Body", "completed", ["SRC-SAGA"], "saga compensation and partial-failure control", "No predecessor isolates saga compensation ordering, idempotency, poison steps, deadlines, and evidence credit in one bounded tribunal."),
    _proposal(2, "Method Flow MVCC snapshot-isolation, write-skew, predicate-conflict, serialization-failure, retry, starvation, teardown, and evidence-credit tribunal", "mvcc-write-skew", "THOS Body", "completed", ["SRC-SNAPSHOT-ISOLATION"], "MVCC write-skew and serialization control", "Prior database work covers WAL and snapshots, but no frozen proposal isolates write skew, predicate conflict, serialization refusal, and retry evidence."),
    _proposal(3, "GMUT Tomonaga-Schwinger spacelike-hypersurface, local-deformation, integrability, microcausality, state-functional, gauge, EFT, unit, and observation-firewall board", "tomonaga-schwinger", "GMUT Mind", "completed", ["SRC-TOMONAGA", "SRC-SCHWINGER"], "Tomonaga-Schwinger hypersurface-evolution obligations", "No predecessor isolates hypersurface-local deformation, state-functional integrability, and microcausality under GMUT gauge and EFT reservations."),
    _proposal(4, "GMUT Bogoliubov causality, local S-matrix functional, support-ordering, factorization, unitarity-reservation, gauge, EFT, unit, and observation-firewall board", "bogoliubov-causality", "GMUT Mind", "completed", ["SRC-BOGOLIUBOV"], "Bogoliubov local S-matrix causality obligations", "No predecessor isolates functional support ordering and local S-matrix causal factorization with explicit gauge, EFT, unit, and observation firewalls."),
    _proposal(5, "GMUT ESA 4XMM-DR14 source-catalogue, detection, association, energy-band, exposure, flag, uncertainty, selection, checksum, covariance, and zero-row likelihood-refusal adapter", "xmm-4xmm-dr14-zero-row", "GMUT Mind", "open_gap", ["SRC-4XMM-DR14"], "ESA 4XMM-DR14 catalogue readiness", "An earlier XMM RGS pipeline exists, but no frozen adapter targets the 4XMM-DR14 source catalogue, quality flags, band products, and zero-row likelihood firewall."),
    _proposal(6, "THOS aquatic-centre pool-water test, disinfectant, pH, turbidity, dosing-hold, sample-custody, escalation, workload, readback, and shift-handover proxy", "aquatic-water-handover", "THOS Body", "represented", ["SRC-CDC-MAHC"], "aquatic-centre water-quality and chemical-hold workflow", "No predecessor uses aquatic-centre water testing, dosing hold, sample custody, and shift handover as a bounded synthetic practice lens."),
    _proposal(7, "THOS aquatic-centre rescue-equipment, accessibility-closure, plant-alarm, incident-isolation, patron-notice, workload, readback, and next-shift ownership proxy", "aquatic-safety-handover", "THOS Body", "represented", ["SRC-CDC-MAHC", "SRC-WCAG22"], "aquatic-centre safety and accessibility closure workflow", "No predecessor isolates rescue-equipment readiness, accessibility closure, plant alarms, accessible notice, and next-shift ownership for an aquatic venue."),
    _proposal(8, "Freed ID RFC 7662 token-introspection active-state, endpoint-authentication, audience, scope, inactive-response minimization, cache, replay, privacy, and nonproduction profile", "oauth-introspection", "Freed ID and CBR Heart", "represented", ["SRC-RFC7662"], "OAuth token-introspection validation", "No frozen profile isolates RFC 7662 active-state semantics, endpoint authorization, inactive-response minimization, caching, replay, and privacy together."),
    _proposal(9, "Freed ID RFC 7800 cnf proof-of-possession representation, single-key, key-binding, recipient, replay, correlation, minimization, and nonproduction profile", "jwt-cnf-pop", "Freed ID and CBR Heart", "represented", ["SRC-RFC7800"], "JWT confirmation-claim proof-of-possession semantics", "DPoP and other key-binding work exists, but no frozen profile isolates RFC 7800 cnf representation, single-key semantics, recipient confirmation, and correlation boundaries."),
    _proposal(10, "CBR aquatic-facility illness, injury, closure, patron and worker privacy, accessible notice, remedy, affected-party, legal, cultural, data-governance, and Maori-authority matrix", "aquatic-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-CDC-MAHC", "SRC-PRIVACY-NZ", "SRC-TE-MANA-RARAUNGA"], "aquatic-facility authority reservation", "No frozen authority matrix combines aquatic-facility closure, illness and injury notice, patron-worker privacy, accessibility, remedy, affected parties, and Maori authority."),
    _proposal(11, "Git packfile signature, version, object-count, type-size varint, base-reference, delta-depth, inflated-size, trailer-checksum, resource-budget, and refusal tribunal", "git-packfile", "THOS Body", "completed", ["SRC-GIT-PACK"], "Git packfile structural refusal", "No frozen format tribunal isolates Git packfile type-size varints, delta bases, delta-depth budgets, inflated-size budgets, and trailer checksums."),
    _proposal(12, "DWARF unit-header, abbreviation, DIE, attribute-form, string, address, range, line-program, offset, depth, resource-budget, and refusal tribunal", "dwarf", "THOS Body", "completed", ["SRC-DWARF5"], "DWARF debugging-data structural refusal", "No frozen format tribunal isolates DWARF units, abbreviation tables, DIE forms, line programs, cross-section offsets, and resource budgets."),
    _proposal(13, "Accessible search-landmark, unique-label, query-name, results-status, filter-state, focus-return, empty-state, native fallback, print, and manual-evaluation audit", "accessible-search", "THOS Body", "completed", ["SRC-WAI-SEARCH", "SRC-WCAG22"], "accessible search structure", "No predecessor isolates search landmark uniqueness, query naming, result status, filter state, focus return, empty state, and native fallback together."),
    _proposal(14, "Thermo-Psyche Gouy-Stodola ambient-temperature, entropy-generation, exergy-destruction, sign, unit, boundary, steady-unsteady-domain, and agency-nonconversion classifier", "gouy-stodola-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-GOUY-STODOLA"], "Gouy-Stodola exergy-destruction classification", "No frozen nonconversion classifier isolates ambient temperature, entropy generation, exergy destruction, boundary assumptions, units, and agency refusal."),
    _proposal(15, "Complex-step differentiation analyticity, real-valued implementation, step-size, branch-cut, nonfinite, reference-derivative, error-bound, unit, and refusal tribunal", "complex-step", "GMUT Mind", "completed", ["SRC-COMPLEX-STEP"], "complex-step numerical differentiation", "No frozen numerical proposal isolates analyticity, branch cuts, step size, reference derivatives, nonfinite behavior, and unit-aware refusal for complex-step differentiation."),
    _proposal(16, "Stage 20 negative-control exposure, negative-control outcome, shared-confounding, no-causal-effect, measurement-error, sensitivity, interpretation, falsification, and nonpromotion board", "negative-control-nonpromotion", "Trinity Mandala bridge", "completed", ["SRC-NEGATIVE-CONTROLS"], "negative-control causal-design assumptions", "No frozen Stage 20 board isolates paired negative-control exposure and outcome assumptions, measurement error, shared confounding, and bounded interpretation."),
    _proposal(17, "COSE-HPKE draft version, recipient-structure, KEM, KDF, AEAD, protected-header, external-AAD, mode, key-management, draft-status, and refusal board", "cose-hpke-draft", "Freed ID and CBR Heart", "completed", ["SRC-COSE-HPKE-DRAFT"], "draft COSE-HPKE structural obligations", "No frozen profile isolates current draft COSE-HPKE recipient structure, algorithm suite, external AAD, modes, and explicit non-final status."),
    _proposal(18, "RFC 9171 Bundle Protocol primary-block, canonical-block, endpoint, creation-time, lifetime, fragmentation, CRC, block-number, resource-budget, and refusal tribunal", "bundle-protocol", "THOS Body", "completed", ["SRC-RFC9171"], "Bundle Protocol version 7 structural refusal", "No frozen format tribunal isolates BPv7 primary and canonical blocks, lifetimes, fragmentation, CRCs, block numbering, and resource budgets."),
    _proposal(19, "RFC 1035 DNS master-file origin, include, owner inheritance, TTL, class, type, RDATA, quoting, continuation, label, resource-budget, and refusal tribunal", "dns-master-file", "THOS Body", "completed", ["SRC-RFC1035"], "DNS master-file structural refusal", "No frozen format tribunal isolates RFC 1035 master-file directives, owner inheritance, quoting, continuation, labels, RDATA, and resource budgets."),
    _proposal(20, "JSON Lines UTF-8, byte-order-mark refusal, one-value-per-line, blank-line, line-terminator, record-count, record-size, truncation, parse-error, and refusal tribunal", "json-lines", "THOS Body", "completed", ["SRC-JSON-LINES", "SRC-RFC8259"], "JSON Lines structural refusal", "No frozen format tribunal isolates JSON Lines UTF-8, BOM refusal, record boundaries, blank lines, record budgets, truncation, and per-record parse errors."),
]


def _source(source_id, status, kind, title, url, implication):
    return {"source_id": source_id, "status": status, "kind": kind, "title": title, "url": url, "phase_implication": implication}


SOURCES = [
    _source("SRC-SAGA", "stable", "primary_research", "SAGAS", "https://doi.org/10.1145/38713.38742", "Supports bounded compensation-order fixtures only; no distributed production assurance."),
    _source("SRC-SNAPSHOT-ISOLATION", "stable", "primary_research", "A Critique of ANSI SQL Isolation Levels", "https://doi.org/10.1145/223784.223785", "Supports bounded anomaly classification only; no database certification."),
    _source("SRC-TOMONAGA", "stable", "primary_research", "On a Relativistically Invariant Formulation of the Quantum Theory of Wave Fields", "https://doi.org/10.1143/PTP.1.27", "Supports typed hypersurface obligations only; no physical state or prediction."),
    _source("SRC-SCHWINGER", "stable", "primary_research", "Quantum Electrodynamics I: A Covariant Formulation", "https://doi.org/10.1103/PhysRev.74.1439", "Supports historical covariant formulation context only."),
    _source("SRC-BOGOLIUBOV", "stable", "primary_research", "Bogoliubov causality in S-matrix theory", "https://doi.org/10.1016/0550-3213(70)90183-5", "Supports typed local S-matrix causality obligations only."),
    _source("SRC-4XMM-DR14", "current", "official_data_catalogue", "ESA XMM-Newton 4XMM-DR14 catalogue", "https://xmm-tools.cosmos.esa.int/external/xmm_user_support/documentation/uhb/node140.html", "Supports a zero-row readiness contract only; no query or download occurs."),
    _source("SRC-CDC-MAHC", "current", "official_public_health_guidance", "CDC 2024 Model Aquatic Health Code fifth edition", "https://www.cdc.gov/model-aquatic-health-code/php/our-work/index.html", "Supports synthetic workflow vocabulary only; it is guidance and confers no local legal or professional authority."),
    _source("SRC-RFC7662", "stable", "official_standard", "RFC 7662 OAuth 2.0 Token Introspection", "https://www.rfc-editor.org/rfc/rfc7662.html", "Supports synthetic vectors only; no real token, endpoint, account, or network event."),
    _source("SRC-RFC7800", "stable", "official_standard", "RFC 7800 Proof-of-Possession Key Semantics for JWTs", "https://www.rfc-editor.org/rfc/rfc7800.html", "Supports synthetic claim vectors only; no real keys or possession event."),
    _source("SRC-PRIVACY-NZ", "current", "official_legal_context", "New Zealand Privacy Commissioner privacy principles", "https://www.privacy.org.nz/privacy-act-2020/privacy-principles/", "Keeps privacy review and legal interpretation exact-gated."),
    _source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Maori data-governance authority visible; repository software cannot exercise it."),
    _source("SRC-GIT-PACK", "current", "official_format_documentation", "Git pack format documentation", "https://git-scm.com/docs/gitformat-pack", "Supports disposable synthetic pack fixtures only."),
    _source("SRC-DWARF5", "stable", "official_format_standard", "DWARF Version 5 standard", "https://dwarfstd.org/doc/DWARF5.pdf", "Supports bounded synthetic debugging-data fixtures only."),
    _source("SRC-WAI-SEARCH", "current", "official_accessibility_guidance", "WAI-ARIA search landmark example", "https://www.w3.org/WAI/ARIA/apg/patterns/landmarks/examples/search.html", "Supports structural checks only; manual and affected-user evaluation remains reserved."),
    _source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural obligations only, not complete conformance."),
    _source("SRC-GOUY-STODOLA", "stable", "primary_research", "The Gouy-Stodola theorem and the derivation of exergy revised", "https://doi.org/10.1016/j.energy.2020.119046", "Supports thermodynamic definitions only, never a psyche, agency, or justice conversion."),
    _source("SRC-COMPLEX-STEP", "stable", "primary_research", "The Complex-Step Derivative Approximation", "https://doi.org/10.1145/838250.838251", "Supports bounded analytic numerical fixtures only."),
    _source("SRC-NEGATIVE-CONTROLS", "stable", "primary_research", "Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies", "https://doi.org/10.1097/EDE.0b013e3181d61eeb", "Supports design assumptions only; no participant effect is estimated."),
    _source("SRC-COSE-HPKE-DRAFT", "draft", "official_active_internet_draft", "draft-ietf-cose-hpke-25", "https://datatracker.ietf.org/doc/draft-ietf-cose-hpke/", "Supports draft-aware structural fixtures only; it is not a final RFC or production profile."),
    _source("SRC-RFC9171", "stable", "official_standard", "RFC 9171 Bundle Protocol Version 7", "https://www.rfc-editor.org/rfc/rfc9171.html", "Supports disposable synthetic bundle fixtures only."),
    _source("SRC-RFC1035", "stable", "official_standard", "RFC 1035 Domain Names Implementation and Specification", "https://www.rfc-editor.org/rfc/rfc1035.html", "Supports bounded synthetic master-file fixtures only; includes do not touch host files."),
    _source("SRC-JSON-LINES", "current", "format_specification", "JSON Lines", "https://jsonlines.org/", "Supports bounded record framing fixtures only."),
    _source("SRC-RFC8259", "stable", "official_standard", "RFC 8259 The JavaScript Object Notation Data Interchange Format", "https://www.rfc-editor.org/rfc/rfc8259.html", "Supplies JSON value syntax only; no external retrieval occurs."),
]


SAFE_TASKS = [
    "freeze exact source anchors", "prove inherited manifests", "record relational identity boundary", "render twenty proposals", "freeze expected disposition counts", "classify source statuses", "compute lexical novelty", "record manual novelty review", "freeze one hundred mutations", "freeze saga obligations", "freeze MVCC obligations", "freeze Tomonaga-Schwinger obligations", "freeze Bogoliubov causality obligations", "freeze 4XMM zero-row contract", "freeze aquatic water states", "freeze aquatic safety states", "freeze introspection states", "freeze cnf states", "freeze aquatic authority reservations", "freeze Git pack obligations", "freeze DWARF obligations", "freeze accessible search obligations", "freeze Gouy-Stodola nonconversion", "freeze complex-step obligations", "freeze negative-control assumptions", "freeze COSE-HPKE draft status", "freeze BPv7 obligations", "freeze DNS master-file obligations", "freeze JSON Lines obligations", "record inherited held work", "record five-class privacy exclusions", "record no-replay rule", "record four-commit cap", "record owner-growth threshold", "record Method Flow failures", "record recurrence guards", "record rollback paths", "render x1 accessible report", "build family tooling index", "run workflow refinement",
]

CANDIDATE_TASKS = [
    "saga schedule simulator", "saga poison-step rejector", "MVCC write-skew simulator", "MVCC predicate-conflict rejector", "Tomonaga-Schwinger type board", "Bogoliubov causality type board", "4XMM schema-only adapter", "aquatic water state machine", "aquatic safety state machine", "RFC7662 synthetic validator", "RFC7662 minimization rejector", "RFC7800 cnf validator", "RFC7800 correlation guard", "aquatic authority reservation matrix", "Git pack bounded parser", "Git delta budget guard", "DWARF unit parser", "DWARF offset-depth guard", "search landmark auditor", "search status-focus auditor", "Gouy-Stodola classifier", "complex-step analytic fixture", "complex-step branch-cut rejector", "negative-control assumption board", "negative-control measurement-error guard", "COSE-HPKE draft board", "BPv7 bounded parser", "DNS master-file bounded parser", "JSON Lines bounded parser", "exact-final ancestry verifier",
]

SKILL_IDEAS = [f"ghc-family-{p['slug']}" for p in PROPOSALS]
RUNNER_IDEAS = [
    "ghc_family_v650_v7_method_tribunals.py", "ghc_family_v650_v7_gmut_boards.py", "ghc_family_v650_v7_zero_row_and_proxy.py", "ghc_family_v650_v7_identity_profiles.py", "ghc_family_v650_v7_format_tribunals.py", "ghc_family_v650_v7_accessibility.py", "ghc_family_v650_v7_nonconversion.py", "ghc_family_v650_v7_stage20.py", "ghc_family_v650_v7_portfolios.py", "ghc_family_v650_v7_validate.py",
]

CLEAN_TASKS = [
    "CLEAN normalize phase-relative paths", "CLEAN preserve UTF-8 and LF", "CLEAN sort JSON keys", "CLEAN reject duplicate proposal ids", "CLEAN quarantine scanner definitions", "CLEAN reserve manual accessibility", "CLEAN reserve affected-user review", "CLEAN reserve Maori authority", "CLEAN reserve legal interpretation", "CLEAN reserve professional authority", "FIX fail closed on unknown outcome", "FIX fail closed on unknown source status", "FIX reject source-free proposals", "FIX reject missing rollback", "FIX reject empty protected gates", "FIX reject x2 observations in x1", "FIX reject raw private identifiers", "FIX reject private absolute paths", "FIX reject unbounded delta depth", "FIX reject unbounded DWARF offsets", "FIX reject unbounded BPv7 blocks", "FIX reject DNS host-file includes", "FIX reject JSON Lines blank records", "FIX reject RFC7662 inactive metadata", "FIX reject RFC7800 multi-key cnf", "FIX reject draft-as-RFC promotion", "FIX reject participant-effect claims", "FIX reject empirical promotion", "FIX reject independent-reproduction claims", "REFINE source status counts", "REFINE nearest-neighbor evidence", "REFINE mutation ownership", "REFINE Method Flow summaries", "REFINE x1 staged manifest", "REFINE five-class scan receipt", "REFINE stale-label review", "REFINE document word caps", "REFINE owner file count", "REFINE handoff remains prepared", "REFINE final verdict remains not ready",
]

X1_OPERATIONAL_NEGATIVES = [
    {"negative_id": "NEG-V6507-X1-QUERY-PS-PARSE-001", "category": "PowerShell foreach pipeline parse", "failed": "A direct pipeline after a statement-level foreach block raised an empty-pipe-element parser error.", "recovery": "Materialize the loop results in an array before downstream conversion.", "passing": "The explicit array query returned attributable novelty rows.", "recurrence_guard": "Never pipe directly from a statement-level foreach block in PowerShell 5.1."},
    {"negative_id": "NEG-V6507-X1-FILE-METRIC-PS-PARSE-002", "category": "recurrent PowerShell foreach pipeline parse", "failed": "A file-metric wrapper repeated the direct post-foreach pipeline error.", "recovery": "Reuse the explicit array method and retain the recurrence separately.", "passing": "The corrected wrapper returned all requested file metrics.", "recurrence_guard": "Apply the preferred array method to inspection wrappers as well as JSON conversions."},
    {"negative_id": "NEG-V6507-X1-METHOD-CLI-SCHEMA-003", "category": "stale Method Flow CLI arguments", "failed": "The validate subcommand rejected remembered arguments absent from the installed runner.", "recovery": "Read the installed subcommand help and invoke only declared arguments.", "passing": "The corrected validation emitted a valid zero-issue receipt.", "recurrence_guard": "Inspect current CLI help before constructing calls."},
    {"negative_id": "NEG-V6507-X1-HISTORICAL-PATH-004", "category": "historical artifact path assumption", "failed": "A direct read assumed a predecessor workflow-request path that did not exist.", "recovery": "Resolve the current schema or exact path before reading.", "passing": "The current schema produced a request that passed all workflow checks.", "recurrence_guard": "Do not infer phase-local paths from neighboring phases."},
    {"negative_id": "NEG-V6507-X1-BROAD-WORKFLOW-SEARCH-TIMEOUT-005", "category": "combined broad search timeout", "failed": "A repository-wide workflow search combined with a schema read exceeded its wrapper.", "recovery": "Split the exact schema read from any bounded recent-artifact query.", "passing": "The direct schema read and bounded workflow run completed independently.", "recurrence_guard": "Keep authoritative small-file reads separate from broad corpus searches."},
    {"negative_id": "NEG-V6507-X1-PATCH-CONTEXT-006", "category": "patch context mismatch", "failed": "A count-adjustment patch used an assumed long-line context and applied no change.", "recovery": "Read the exact target line and apply a smaller uniquely anchored replacement.", "passing": "The exact-context patch adjusted only the intended list entries.", "recurrence_guard": "Inspect current line context before count-sensitive patches."},
    {"negative_id": "NEG-V6507-X1-PORTFOLIO-COUNT-007", "category": "portfolio cardinality mismatch", "failed": "The first post-patch preflight returned thirty-nine refinement tasks instead of forty.", "recovery": "Restore one explicitly scoped refinement and rerun all five counts.", "passing": "The corrected preflight returned 40, 30, 20, 10, and 40.", "recurrence_guard": "Use executable counts after every list adjustment."},
    {"negative_id": "NEG-V6507-X1-NEGATIVE-MIRROR-TEST-008", "category": "retained-negative mirror test failure", "failed": "The first x1 test run found only five negatives in the generated register after later failures existed.", "recovery": "Synchronize the source list with all eight current failures, regenerate, and rerun only the x1 scope.", "passing": "The next isolated run passed the retained-negative count assertion before exposing a separate workflow-schema assertion error.", "recurrence_guard": "Refresh negative mirrors from the final pre-freeze failure set."},
    {"negative_id": "NEG-V6507-X1-WORKFLOW-TEST-SCHEMA-009", "category": "workflow result assertion path", "failed": "The second x1 test run treated requires_user_confirmation as a differently named top-level field and raised KeyError.", "recovery": "Inspect the generated schema and assert the exact requires_user_confirmation field.", "passing": "The third isolated run passed all six dedicated x1 tests.", "recurrence_guard": "Inspect generated JSON keys before asserting field placement."},
    {"negative_id": "NEG-V6507-X1-MANIFEST-HASH-DOMAIN-010", "category": "manifest hash-domain mismatch", "failed": "The first pre-commit review compared path-filtered Git-blob hashes with Windows checkout bytes and reported two tooling-index mismatches.", "recovery": "Compare manifest object ids, SHA-256 values, and sizes against exact Git-blob bytes, while reporting checkout bytes separately.", "passing": "The domain diagnosis proved both object ids and both Git-blob hashes exact; a complete corrected review remains required.", "recurrence_guard": "Validate each manifest field only in its declared hash domain."},
    {"negative_id": "NEG-V6507-X1-STAGED-UTF8-DECODE-011", "category": "staged UTF-8 decode failure", "failed": "The first exact staged review decoded Git output through the Windows default codec and failed on one Unicode byte.", "recovery": "Read staged Git output as bytes and decode explicitly with UTF-8.", "passing": "The corrected review parsed all sixty-two staged JSON blobs and passed all seventy manifest entries plus three self-exclusions.", "recurrence_guard": "Use explicit UTF-8 for every staged text blob."},
]

REJECTED_COLLISIONS = [
    {"seed": "epoch RCU tribunal", "reason": "already frozen in v649-v6"},
    {"seed": "Batalin-Vilkovisky board", "reason": "already frozen in v647-v2"},
    {"seed": "Peierls bracket board", "reason": "already represented by a frozen covariant bracket mechanism"},
    {"seed": "Fermi 4FGL adapter", "reason": "already frozen in an earlier empirical lane"},
    {"seed": "museum collection handover", "reason": "already frozen as a bounded practice"},
    {"seed": "theatre operations handover", "reason": "already frozen as a bounded practice"},
    {"seed": "OpenID Federation profile", "reason": "already frozen"},
    {"seed": "OpenID verifiable credential issuance", "reason": "already frozen"},
    {"seed": "SQLite WAL tribunal", "reason": "already frozen in v650-v6"},
    {"seed": "HTTP Message Signatures profile", "reason": "already frozen"},
    {"seed": "TIFF refusal tribunal", "reason": "already frozen"},
    {"seed": "carousel accessibility audit", "reason": "already frozen"},
    {"seed": "treegrid accessibility audit", "reason": "already frozen"},
    {"seed": "RFC 9396 authorization details", "reason": "already frozen"},
    {"seed": "SCIM profile", "reason": "already frozen"},
    {"seed": "JWT access token profile", "reason": "already frozen"},
    {"seed": "eROSITA adapter", "reason": "already frozen"},
    {"seed": "DPoP profile", "reason": "already frozen"},
    {"seed": "PCAPNG tribunal", "reason": "already frozen"},
    {"seed": "target-trial board", "reason": "already frozen"},
]
