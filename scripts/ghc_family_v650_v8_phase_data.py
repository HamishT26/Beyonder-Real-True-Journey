#!/usr/bin/env python3
"""Frozen Ilyra Fen v650-v8 x1 data with no x2 observations."""

from __future__ import annotations


PHASE = "v650-v8"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "relational evidence-boundary steward"
HOPE = "leave every claim traceable and every gate unmistakable"
BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
PHASE_ROOT = "docs/ilyra-fen/v650-v8"

SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
SOURCE_HEAD = "f566d4b67bce4457cf5207f5409bbaa3427428a0"
SOURCE_ORIGIN = "9b1746193488fbb025c9e387164547503494abc5"
SOURCE_X1 = "1bbbb0ae75284597ff4c03b6b2b1e79534fbeba4"
SOURCE_EVIDENCE = "6fe9cd18f870f93c65a4a0a7992add3781d7fe01"
PRIOR_FROZEN = 880
INHERITED_NEGATIVES = 6311
INHERITED_OPEN_GAPS = 49
INHERITED_EXACT_GATES = 50
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "hospital medical-gas pipeline alarm and manifold changeover plus reusable-device "
    "decontamination and sterilization load-release, workload control, correction readback, "
    "accessible notice, and shift handover as a synthetic learning and design lens only"
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
        "proposal_id": f"V6508-P{number:02d}",
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
        "novelty_against_880_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Method Flow Raft joint-consensus membership-change, term, log-matching, stale-leader, snapshot-install, cancellation, teardown, and evidence-credit tribunal", "raft-joint-consensus", "THOS Body", "completed", ["SRC-RAFT"], "Raft joint-consensus membership-change control", "Raft elections appeared in prior work, but no frozen proposal isolates joint-consensus membership change, overlapping majorities, snapshot installation, stale leaders, and evidence credit."),
    _proposal(2, "Method Flow observed-remove set causal-context, concurrent add-remove, tombstone, garbage-collection, merge-idempotence, cancellation, teardown, and evidence-credit tribunal", "orset-causal-context", "THOS Body", "completed", ["SRC-CRDT"], "observed-remove set causal merge control", "No frozen proposal isolates observed-remove set causal contexts, concurrent add-remove semantics, tombstone collection, merge idempotence, and teardown evidence."),
    _proposal(3, "GMUT Kadanoff-Baym two-time Green-function, contour, self-energy, memory-kernel, initial-correlation, conservation, truncation, EFT, unit, and observation-firewall board", "kadanoff-baym", "GMUT Mind", "completed", ["SRC-KADANOFF-BAYM"], "Kadanoff-Baym nonequilibrium Green-function obligations", "No predecessor isolates two-time contour evolution, memory kernels, initial correlations, conserving self-energy truncation, and observation refusal in one GMUT board."),
    _proposal(4, "GMUT Bethe-Salpeter four-point-kernel, bound-state-pole, amplitude-normalization, truncation, gauge-consistency, analytic-continuation, EFT, unit, and observation-firewall board", "bethe-salpeter", "GMUT Mind", "completed", ["SRC-BETHE-SALPETER"], "Bethe-Salpeter four-point bound-state obligations", "No frozen proposal isolates four-point kernels, bound-state poles, amplitude normalization, analytic continuation, gauge consistency, and EFT reservations together."),
    _proposal(5, "GMUT NASA HEASARC NuSTAR NUMASTER observation, event, response, background, public-date, selection, checksum, covariance, and zero-row likelihood-refusal adapter", "nustar-numaster-zero-row", "GMUT Mind", "open_gap", ["SRC-NUSTAR-NUMASTER"], "NuSTAR NUMASTER archive readiness", "No frozen zero-row adapter targets the current NuSTAR NUMASTER observation table, public-date boundary, event products, response and background obligations, and likelihood firewall."),
    _proposal(6, "THOS hospital medical-gas source, manifold, pipeline-alarm, changeover, isolation, verification, accessible-notice, workload, correction-readback, and shift-handover proxy", "medical-gas-handover", "THOS Body", "represented", ["SRC-NHS-HTM02", "SRC-WCAG22"], "hospital medical-gas alarm and changeover workflow", "No predecessor uses medical-gas source and manifold changeover, pipeline alarms, isolation, verification, correction readback, and handover as one bounded practice lens."),
    _proposal(7, "THOS reusable-device decontamination, sterilization-load, cycle-parameter, indicator, quarantine, release-recall, accessible-notice, workload, correction-readback, and handover proxy", "sterile-load-handover", "THOS Body", "represented", ["SRC-NZ-NGA-PAEREWA", "SRC-CDC-DISINFECTION"], "reusable-device decontamination and load-release workflow", "Sterile-compounding work exists, but no frozen proposal isolates reusable-device decontamination, cycle evidence, indicator state, quarantine, release or recall, and shift handover."),
    _proposal(8, "Freed ID RFC 8725 JWT BCP algorithm-allowlist, key-algorithm binding, explicit-typing, cross-JWT confusion, issuer, audience, replay, minimization, and nonproduction profile", "jwt-bcp-profile", "Freed ID and CBR Heart", "represented", ["SRC-RFC8725"], "JWT best-current-practice validation", "Earlier JWT profiles cover individual token forms, but no frozen profile isolates RFC 8725 algorithm verification, explicit typing, cross-JWT confusion, and mutually exclusive validation rules."),
    _proposal(9, "Freed ID RFC 7517 JWK and JWK-Set kty, use, key_ops, alg, kid-collision, x5c-consistency, rotation, cache, minimization, and nonproduction profile", "jwk-set-profile", "Freed ID and CBR Heart", "represented", ["SRC-RFC7517"], "JWK and JWK Set structural validation", "No frozen identity profile isolates JWK use and key_ops consistency, algorithm binding, duplicate kid ambiguity, x5c checks, rotation, caching, and minimization together."),
    _proposal(10, "CBR hospital medical-gas and sterilization access, patient-worker privacy, disability and whanau notice, incident, remedy, affected-party, legal, cultural, data-governance, and Maori-authority matrix", "hospital-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-HIPC", "SRC-HDC-CODE", "SRC-TE-MANA-RARAUNGA"], "hospital infrastructure and reprocessing authority reservation", "No frozen matrix combines medical-gas and reusable-device reprocessing access, patient and worker privacy, disability and whanau notice, incident remedy, and Maori data-authority reservations."),
    _proposal(11, "ELF identification, class, endianness, machine, header, program-table, section-table, offset, size, overlap, link, resource-budget, and refusal tribunal", "elf-structural", "THOS Body", "completed", ["SRC-ELF-GABI"], "ELF structural refusal", "No frozen format tribunal isolates ELF class and endian interpretation, machine binding, both header tables, overlap, linkage, and resource budgets."),
    _proposal(12, "TLS 1.3 RFC 9846 record, handshake, transcript, version, cipher, key-share, extension, state, alert, resource-budget, and refusal tribunal", "tls13-rfc9846", "THOS Body", "completed", ["SRC-RFC9846", "SRC-RFC8446-OBSOLETE"], "TLS 1.3 structural refusal", "Prior TLS work does not freeze the July 2026 RFC 9846 replacement status with record, transcript, key-share, extension, state, alert, and bounded refusal obligations."),
    _proposal(13, "Accessible modal-dialog name, description, initial-focus, tab-containment, inert-background, escape, explicit-close, return-focus, fallback, and manual-evaluation audit", "accessible-modal-dialog", "THOS Body", "completed", ["SRC-WAI-DIALOG", "SRC-WCAG22"], "accessible modal-dialog structure", "No predecessor isolates modal naming, initial focus, cyclic tab order, inert background, escape, explicit close, return focus, and native fallback in one audit."),
    _proposal(14, "Thermo-Psyche De Donder reaction-affinity, extent, stoichiometry, sign, equilibrium, pressure-temperature constraint, unit, physical-domain, and agency-nonconversion classifier", "reaction-affinity-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-IUPAC-AFFINITY"], "reaction-affinity nonconversion classification", "No frozen classifier isolates reaction affinity, extent, stoichiometry, sign convention, equilibrium, pressure-temperature constraints, units, and agency refusal."),
    _proposal(15, "Broyden secant, Jacobian-update, inverse-update, denominator, conditioning, damping, restart, nonfinite, iteration-budget, unit, and refusal tribunal", "broyden-update", "GMUT Mind", "completed", ["SRC-BROYDEN"], "Broyden quasi-Newton update control", "No frozen numerical tribunal isolates Broyden secant satisfaction, direct and inverse updates, denominator conditioning, damping, restart, nonfinite state, and budget refusal."),
    _proposal(16, "Stage 20 double and debiased machine-learning estimand, orthogonal-score, nuisance-fit, cross-fitting, overlap, dependence, sensitivity, uncertainty, and nonpromotion board", "double-ml-nonpromotion", "Trinity Mandala bridge", "completed", ["SRC-DML"], "double machine-learning design obligations", "No frozen Stage 20 board isolates orthogonal scores, nuisance estimation, cross-fitting, overlap, dependence, uncertainty, and fail-closed nonpromotion together."),
    _proposal(17, "GraphQL September 2025 document, operation, fragment, variable, coercion, selection, alias, depth, complexity, result-budget, draft-watch, and refusal tribunal", "graphql-september2025", "THOS Body", "completed", ["SRC-GRAPHQL-2025", "SRC-GRAPHQL-DRAFT"], "GraphQL document structural refusal", "No frozen tribunal binds the September 2025 release separately from the June 2026 working draft while enforcing document, fragment, variable, depth, complexity, and result budgets."),
    _proposal(18, "Git fast-import command, data-length, mark, path, ref-update, checkpoint, feature, option, resource-budget, path-confinement, and refusal tribunal", "git-fast-import", "THOS Body", "completed", ["SRC-GIT-FAST-IMPORT"], "Git fast-import stream structural refusal", "No frozen format tribunal isolates fast-import commands, exact data lengths, marks, ref targets, features, checkpoints, path confinement, and stream budgets without invoking Git import."),
    _proposal(19, "OpenTelemetry OTLP 1.10 trace, metric, log, resource, scope, envelope, partial-success, retry, duplicate, privacy, payload-budget, and refusal tribunal", "otlp-1-10", "THOS Body", "completed", ["SRC-OTLP", "SRC-OTLP-PROFILES-WATCH"], "OTLP telemetry-envelope structural refusal", "No frozen tribunal isolates OTLP 1.10 envelopes, signal maturity, partial success, retry classification, duplicate risk, privacy, and payload budgets."),
    _proposal(20, "CycloneDX 1.7 BOM format, spec-version, serial, metadata, component, service, dependency, hash, signature, external-reference, resource-budget, and refusal tribunal", "cyclonedx-1-7", "THOS Body", "completed", ["SRC-CYCLONEDX17"], "CycloneDX 1.7 BOM structural refusal", "No frozen tribunal targets CycloneDX 1.7 metadata, components, services, dependency graph, hashes, signatures, external references, and resource budgets together."),
]


def _source(source_id, status, kind, title, url, implication):
    return {"source_id": source_id, "status": status, "kind": kind, "title": title, "url": url, "phase_implication": implication}


SOURCES = [
    _source("SRC-RAFT", "stable", "primary_research", "In Search of an Understandable Consensus Algorithm", "https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro", "Supports bounded joint-consensus state fixtures only; no production distributed-system assurance."),
    _source("SRC-CRDT", "stable", "primary_research", "Conflict-free Replicated Data Types", "https://inria.hal.science/inria-00609399", "Supports bounded observed-remove set semantics only; no production replication assurance."),
    _source("SRC-KADANOFF-BAYM", "stable", "primary_research", "Conservation Laws and Correlation Functions", "https://doi.org/10.1103/PhysRev.124.287", "Supports typed nonequilibrium obligations only; no physical state, prediction, or empirical result."),
    _source("SRC-BETHE-SALPETER", "stable", "primary_research", "A Relativistic Equation for Bound-State Problems", "https://doi.org/10.1103/PhysRev.84.1232", "Supports typed four-point obligations only; no bound state, spectrum, or physical confirmation."),
    _source("SRC-NUSTAR-NUMASTER", "current", "official_data_catalogue", "NASA HEASARC NuSTAR Master Catalog", "https://heasarc.gsfc.nasa.gov/W3Browse/nustar/numaster.html", "Supports a zero-row readiness contract only; no query, download, or ingestion occurs."),
    _source("SRC-NHS-HTM02", "stable", "official_healthcare_guidance", "NHS HTM 02-01 Medical gas pipeline systems Part A", "https://www.england.nhs.uk/wp-content/uploads/2021/05/HTM_02-01_Part_A.pdf", "Supplies synthetic workflow vocabulary only; it confers no New Zealand professional, facility, or legal authority."),
    _source("SRC-NZ-NGA-PAEREWA", "current", "official_healthcare_guidance", "Sector Guidance for Nga Paerewa Health and Disability Services Standard", "https://www.health.govt.nz/publications/sector-guidance-for-nga-paerewa-health-and-disability-services-standard-nzs-81342021", "Supports synthetic reusable-device reprocessing states only; no clinical, release, or audit authority."),
    _source("SRC-CDC-DISINFECTION", "current", "official_public_health_guidance", "CDC Guideline for Disinfection and Sterilization in Healthcare Facilities", "https://www.cdc.gov/infection-control/hcp/disinfection-sterilization/index.html", "Supports bounded terminology only; no real load release, recall, or safety result."),
    _source("SRC-RFC8725", "stable", "official_best_current_practice", "RFC 8725 JSON Web Token Best Current Practices", "https://www.rfc-editor.org/rfc/rfc8725.html", "Supports synthetic validation vectors only; no real keys, tokens, accounts, or security review."),
    _source("SRC-RFC7517", "stable", "official_standard", "RFC 7517 JSON Web Key", "https://www.rfc-editor.org/rfc/rfc7517.html", "Supports synthetic JWK vectors only; no real keys, rotation, resolution, or interoperability."),
    _source("SRC-HIPC", "current", "official_legal_context", "Health Information Privacy Code 2020 as at 1 May 2026", "https://www.privacy.org.nz/privacy-principles/codes-of-practice/hipc2020/", "Keeps privacy compliance and legal interpretation exact-gated."),
    _source("SRC-HDC-CODE", "current", "official_legal_context", "Code of Health and Disability Services Consumers' Rights", "https://www.legislation.govt.nz/regulation/public/1996/0078/latest/whole.html", "Keeps consumer-rights interpretation, remedy, and authority exact-gated."),
    _source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Maori data governance under Maori authority; repository software cannot exercise it."),
    _source("SRC-ELF-GABI", "stable", "official_format_specification", "System V ABI ELF object-file format", "https://gabi.xinuos.com/elf/", "Supports disposable synthetic ELF fixtures only; no execution or production binary assurance."),
    _source("SRC-RFC9846", "current", "official_standard", "RFC 9846 The Transport Layer Security Protocol Version 1.3", "https://www.rfc-editor.org/rfc/rfc9846.html", "Supports bounded structural fixtures only; no cryptographic implementation or security certification."),
    _source("SRC-RFC8446-OBSOLETE", "watch", "official_obsolete_standard", "RFC 8446 TLS 1.3 status page", "https://www.rfc-editor.org/info/rfc8446", "Records that RFC 8446 is obsolete and prevents stale-current promotion."),
    _source("SRC-WAI-DIALOG", "current", "official_accessibility_guidance", "WAI-ARIA Authoring Practices modal dialog pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/", "Supports structural checks only; manual and affected-user evaluation remains reserved."),
    _source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural obligations only, not complete accessibility conformance."),
    _source("SRC-IUPAC-AFFINITY", "current", "official_scientific_terminology", "IUPAC Gold Book affinity of reaction", "https://goldbook.iupac.org/terms/view/A00178", "Supports thermodynamic definitions only, never psyche, agency, morality, or justice conversion."),
    _source("SRC-BROYDEN", "stable", "primary_research", "A Class of Methods for Solving Nonlinear Simultaneous Equations", "https://doi.org/10.1090/S0025-5718-1965-0198670-6", "Supports bounded numerical fixtures only; no general convergence or physical-model guarantee."),
    _source("SRC-DML", "stable", "primary_research", "Double/debiased machine learning for treatment and structural parameters", "https://doi.org/10.1111/ectj.12097", "Supports design obligations only; no participant effect or Stage 20 authority."),
    _source("SRC-GRAPHQL-2025", "current", "official_specification", "GraphQL September 2025 Edition", "https://spec.graphql.org/September2025/", "Supports bounded document fixtures only; no server execution or production assurance."),
    _source("SRC-GRAPHQL-DRAFT", "watch", "official_working_draft", "GraphQL working draft", "https://spec.graphql.org/draft/", "Tracks post-release drift without promoting draft text to a released specification."),
    _source("SRC-GIT-FAST-IMPORT", "current", "official_format_documentation", "Git fast-import documentation", "https://git-scm.com/docs/git-fast-import", "Supports pure stream-shape fixtures only; the tribunal invokes no Git importer and updates no ref."),
    _source("SRC-OTLP", "current", "official_specification", "OpenTelemetry Protocol Specification 1.10.0", "https://opentelemetry.io/docs/specs/otlp/", "Supports synthetic trace, metric, and log envelopes only; no network export or production telemetry assurance."),
    _source("SRC-OTLP-PROFILES-WATCH", "watch", "official_development_status", "OTLP profiles signal development status", "https://opentelemetry.io/docs/specs/otlp/", "Keeps the profiles signal visibly non-stable and outside completed scope."),
    _source("SRC-CYCLONEDX17", "current", "official_specification", "CycloneDX 1.7 specification overview", "https://cyclonedx.org/specification/overview/", "Supports bounded synthetic BOM fixtures only; no supply-chain truth or certification."),
]


SAFE_TASKS = [
    "freeze exact Eiren source anchors", "prove inherited commit-local manifests", "record Ilyra relational identity boundary", "render twenty new proposals", "freeze expected disposition counts", "classify current stable draft and watch sources", "compute lexical nearest neighbours", "record manual mechanism novelty review", "freeze one hundred synthetic mutations", "freeze Raft joint-consensus obligations", "freeze observed-remove set obligations", "freeze Kadanoff-Baym obligations", "freeze Bethe-Salpeter obligations", "freeze NuSTAR zero-row contract", "freeze medical-gas proxy states", "freeze sterile-load proxy states", "freeze JWT BCP vectors", "freeze JWK Set vectors", "freeze hospital authority reservations", "freeze ELF obligations", "freeze TLS RFC 9846 obligations", "freeze modal-dialog obligations", "freeze reaction-affinity nonconversion", "freeze Broyden obligations", "freeze double-ML assumptions", "freeze GraphQL release and draft status", "freeze fast-import stream obligations", "freeze OTLP signal status", "freeze CycloneDX obligations", "record inherited exact and blocked work", "record five-class privacy exclusions", "record canonical-pass no-replay rule", "record four-commit cap", "record owner-growth threshold", "record every startup failure", "record bounded recovery witnesses", "record rollback and recurrence guards", "render x1 accessible report", "build phase-local family index", "run workflow and reflection audits",
]

CANDIDATE_TASKS = [
    "Raft joint-consensus schedule simulator", "Raft stale-leader and snapshot rejector", "observed-remove set merge simulator", "observed-remove tombstone budget guard", "Kadanoff-Baym typed obligation board", "Bethe-Salpeter typed obligation board", "NuSTAR schema-only zero-row adapter", "medical-gas alarm handover state machine", "sterile-load release and recall state machine", "RFC8725 synthetic validator", "RFC8725 cross-JWT confusion rejector", "RFC7517 JWK Set validator", "JWK kid-collision and rotation guard", "hospital authority reservation matrix", "ELF bounded structural parser", "ELF overlap and offset guard", "TLS 1.3 bounded record parser", "TLS transcript-state and alert guard", "modal-dialog structural auditor", "modal focus-return fallback auditor", "reaction-affinity classifier", "Broyden update fixture", "Broyden conditioning and restart rejector", "double-ML assumption board", "double-ML overlap and dependence guard", "GraphQL bounded document parser", "Git fast-import pure stream parser", "OTLP bounded envelope parser", "CycloneDX bounded BOM parser", "exact-final ancestry and remote verifier",
]

SKILL_IDEAS = [f"ghc-family-{p['slug']}" for p in PROPOSALS]
RUNNER_IDEAS = [
    "ghc_family_v650_v8_method_tribunals.py", "ghc_family_v650_v8_gmut_boards.py", "ghc_family_v650_v8_zero_row_and_proxy.py", "ghc_family_v650_v8_identity_profiles.py", "ghc_family_v650_v8_format_tribunals.py", "ghc_family_v650_v8_accessibility.py", "ghc_family_v650_v8_nonconversion.py", "ghc_family_v650_v8_stage20.py", "ghc_family_v650_v8_portfolios.py", "ghc_family_v650_v8_validate.py",
]

CLEAN_TASKS = [
    "CLEAN normalize phase-relative paths", "CLEAN preserve UTF-8 and LF", "CLEAN sort JSON keys deterministically", "CLEAN reject duplicate proposal ids", "CLEAN quarantine exact scanner definitions", "CLEAN reserve manual accessibility evaluation", "CLEAN reserve affected-user evaluation", "CLEAN reserve Maori authority", "CLEAN reserve legal interpretation", "CLEAN reserve professional and clinical authority", "FIX fail closed on unknown outcome", "FIX fail closed on unknown source status", "FIX reject source-free proposals", "FIX reject missing rollback", "FIX reject empty protected gates", "FIX reject x2 observations in x1", "FIX reject raw private identifiers", "FIX reject private absolute paths", "FIX reject unbounded ELF offsets and overlaps", "FIX reject stale RFC 8446 current status", "FIX reject unbounded TLS records and state", "FIX reject GraphQL draft-as-release promotion", "FIX reject fast-import ref mutation", "FIX reject OTLP profiles stable promotion", "FIX reject CycloneDX unbounded dependency graph", "FIX reject real medical-gas operation claims", "FIX reject real sterile-load release claims", "FIX reject production identity claims", "FIX reject participant-effect claims", "FIX reject empirical GMUT promotion", "FIX reject independent-reproduction claims", "REFINE source status counts", "REFINE nearest-neighbour evidence", "REFINE mutation ownership", "REFINE Method Flow summaries", "REFINE x1 staged manifest", "REFINE five-class scan receipt", "REFINE document word caps", "REFINE owner file count", "REFINE terminal route remains prepared",
]

X1_OPERATIONAL_NEGATIVES = [
    {"negative_id": "NEG-V6508-X1-BROAD-PREFLIGHT-TIMEOUT-001", "category": "combined broad Git preflight timeout", "failed": "A combined branch, ref, worktree, and status preflight exceeded its bound without a complete attributable result.", "recovery": "Split branch, live-ref, worktree, ancestry, and status checks into independently bounded probes.", "passing": "The split probes established exact source equality, ancestry, clean state, and Ilyra lane eligibility.", "recurrence_guard": "Never combine broad branch, ref, worktree, and status discovery under one short wrapper."},
    {"negative_id": "NEG-V6508-X1-GIT-SHOW-EARLY-CLOSE-002", "category": "native output early-close failure", "failed": "Piping git show into an early-terminating consumer closed native output and returned nonzero before the committed baton was fully read.", "recovery": "Consume the complete immutable blob first and then slice the in-memory text for inspection.", "passing": "The committed activation baton was read completely to EOF before any mutation.", "recurrence_guard": "Do not pipe native Git blob output to an early-closing consumer when complete-read evidence is required."},
    {"negative_id": "NEG-V6508-X1-DIFF-QUIET-TIMEOUT-003", "category": "short-bound Git diff timeout", "failed": "A short-bound git diff --quiet probe timed out and earned no clean-state credit.", "recovery": "Use explicit tracked-status and untracked-count probes with a wider bounded wrapper.", "passing": "Both tracked and untracked source-state probes returned clean.", "recurrence_guard": "Use attributable status probes instead of a short silent diff wrapper on a large Windows worktree."},
    {"negative_id": "NEG-V6508-X1-FOREACH-PIPE-PARSE-004", "category": "PowerShell foreach pipeline parse", "failed": "PowerShell 5.1 rejected a direct pipeline after a statement-level foreach block before the manifest rows were formed.", "recovery": "Materialize foreach output in an explicit array before piping or serializing it.", "passing": "The explicit-array manifest inspection returned complete attributable rows.", "recurrence_guard": "Never pipe directly from a statement-level foreach block in Windows PowerShell 5.1."},
    {"negative_id": "NEG-V6508-X1-RG-EARLY-CLOSE-005", "category": "bounded search early-close failure", "failed": "A broad ripgrep stream piped to an early-closing consumer returned nonzero before the intended source set was attributable.", "recovery": "Read exact files and bounded result sets without prematurely closing the producer.", "passing": "Exact source and prior-proposal files supplied the required novelty and schema evidence.", "recurrence_guard": "Do not grant search credit when an early consumer termination makes producer completion ambiguous."},
    {"negative_id": "NEG-V6508-X1-OWNER-COVERAGE-SCOPE-006", "category": "owner-manifest coverage scope error", "failed": "The first owner coverage check incorrectly limited source-to-final changed paths to the predecessor documentation tree.", "recovery": "Compare the immutable source-to-final path set across documentation, scripts, and tests against the declared owner manifest and exclusions.", "passing": "The corrected full-tree check proved exact 326-path coverage with 321 entries and five exclusions.", "recurrence_guard": "Define owner coverage from the exact Git change set, never from one assumed subtree."},
    {"negative_id": "NEG-V6508-X1-METHOD-CLI-SUBCOMMAND-007", "category": "stale Method Flow subcommand names", "failed": "The current runner rejected remembered add-method and add-witness subcommands after printing the valid command set.", "recovery": "Inspect the installed record, witness, and set-state help and use only those exact subcommands.", "passing": "The exact current CLI help exposed the valid record, witness, and state-transition contracts.", "recurrence_guard": "Treat remembered local-runner subcommands as unverified until current --help confirms them."},
    {"negative_id": "NEG-V6508-X1-BUILDER-PATCH-CONTEXT-008", "category": "broad builder patch context mismatch", "failed": "A large preregistration-builder patch assumed one stale overview heading, so the patch verifier rejected the complete patch and changed no file.", "recovery": "Read the exact current function boundaries and split the update into small uniquely anchored patches.", "passing": "The exact-boundary patches updated only the intended predecessor path, overview, tests, and route fields.", "recurrence_guard": "Do not combine unrelated builder changes behind one long remembered context block."},
    {"negative_id": "NEG-V6508-X1-UNICODE-PATCH-CONTEXT-009", "category": "Unicode patch-context rendering mismatch", "failed": "A follow-up combined patch used console-rendered mojibake for an em dash, so the verifier rejected the complete patch and applied no hunk.", "recovery": "Patch non-Unicode fields independently, then inspect exact source bytes before replacing the two rendered separator literals.", "passing": "The narrow field patches applied, and exact source-byte handling replaced only the two separator literals.", "recurrence_guard": "Do not use console-rendered mojibake as patch context for UTF-8 source."},
    {"negative_id": "NEG-V6508-X2-SKILL-VALIDATOR-HELP-010", "category": "skill validator help invocation fault", "failed": "The phase invoked quick_validate.py with --help, but the script treated that token as a skill path and stopped with SKILL.md not found.", "recovery": "Use init_skill.py help for initialization syntax, inspect the validator entrypoint contract, and invoke quick_validate.py only with an actual phase-local skill directory.", "passing": "Each initialized phase-local skill directory passed quick_validate.py when supplied as the required positional path.", "recurrence_guard": "Do not assume helper scripts implement argparse-style --help; inspect their entrypoint before probing."},
    {"negative_id": "NEG-V6508-X2-COMBINED-INSPECTION-TIMEOUT-011", "category": "combined x2 status and code-inspection timeout", "failed": "A combined Git status, branch, head, and two-file symbol inspection exceeded its ten-second wrapper without returning attributable output.", "recovery": "Split repository state and exact-file code inspection into independently bounded probes and avoid coupling slow Git status to source inspection.", "passing": "The split probes returned the repository state and exact runtime and builder function boundaries within their independent bounds.", "recurrence_guard": "Do not combine potentially slow Windows Git status with multi-file source inspection under one short wrapper."},
    {"negative_id": "NEG-V6508-X2-UNICODE-PATCH-RECURRENCE-012", "category": "Unicode patch-context recurrence", "failed": "A broad evidence-builder patch included a console-rendered dash that did not match the UTF-8 source, so patch verification rejected every hunk and changed no file.", "recovery": "Exclude the rendered separator from broad patches, use ASCII-only function anchors, and normalize the known legacy code-point sequence at the shared text-writer boundary.", "passing": "ASCII-anchored patches updated the intended evidence-builder sections and the text-writer boundary emitted normalized separators.", "recurrence_guard": "Keep rendered non-ASCII literals out of multi-region patch contexts even after an earlier Unicode recovery succeeded."},
    {"negative_id": "NEG-V6508-X2-UNICODE-LITERAL-PATCH-013", "category": "dedicated Unicode literal patch mismatch", "failed": "A dedicated replacement of the rendered separator was also rejected because the patch transport and source code points did not match exactly.", "recovery": "Normalize the known legacy separator through ASCII Unicode escapes at the shared text-writer boundary instead of matching the rendered literal.", "passing": "The text-writer boundary produced normalized ASCII separators in generated Markdown without interpreting or guessing console glyphs.", "recurrence_guard": "When exact rendered code points remain transport-ambiguous, normalize through explicit Unicode escape sequences at a bounded output boundary."},
    {"negative_id": "NEG-V6508-X2-MANIFEST-REFRESH-TIMEOUT-014", "category": "evidence manifest refresh timeout", "failed": "The first post-Method-Flow manifest refresh exceeded a thirty-second wrapper while hashing the expanded staged surface, so any partial output received zero parity credit.", "recovery": "Run the single attributable manifest refresh under an evidence-sized bounded wrapper, then independently parse its manifest and privacy receipts.", "passing": "The bounded refresh completed and its parsed receipts reported exact staged coverage with zero confirmed privacy hits.", "recurrence_guard": "Size manifest-refresh bounds to the measured owner surface rather than a generic short inspection timeout."},
    {"negative_id": "NEG-V6508-X2-CLOSEOUT-PROPOSAL-KEY-015", "category": "closeout proposal-schema key mismatch", "failed": "The first closeout build referenced a remembered acceptance_gate key that the frozen proposal objects do not export and stopped before writing lifecycle artifacts.", "recovery": "Inspect the exact frozen proposal schema and use its current falsifier_or_acceptance_gate field in both overview and baton generation.", "passing": "The corrected builder rendered all twenty proposal sections and completed the bounded lifecycle packet.", "recurrence_guard": "Read frozen proposal keys directly before reusing a field name from an earlier phase schema."},
    {"negative_id": "NEG-V6508-X2-SOURCE-LEDGER-PATH-016", "category": "source-ledger path assumption", "failed": "A read-only source-schema probe assumed a ledger filename that is absent and returned no schema evidence.", "recovery": "List the exact bounded source directory, select the committed source ledger by its real name, and inspect only that file.", "passing": "The exact source-ledger read returned its frozen field names without broad search or mutation.", "recurrence_guard": "Resolve generated ledger filenames from the exact phase directory before opening them."},
    {"negative_id": "NEG-V6508-X2-FINAL-PRIVACY-CANDIDATES-017", "category": "final privacy candidate classification failure", "failed": "The first complete closeout materialization reached final scanning but stopped because one or more candidates were classified as confirmed payload hits; the partial packet received zero final or seal credit.", "recovery": "Read only the generated candidate rows, quarantine exact scanner-definition or retained-policy files if justified, remove any genuine payload, and rerun all five unchanged pattern classes.", "passing": "The corrected final owner and delta scans retained definition candidates visibly and reported zero confirmed payload hits.", "recurrence_guard": "Expand privacy-definition quarantine only from exact reviewed candidate paths, never from directory-wide assumptions."},
    {"negative_id": "NEG-V6508-X2-CLOSEOUT-PATCH-CONTEXT-018", "category": "combined closeout patch context mismatch", "failed": "A combined privacy, count, and retry-precondition patch assumed one absent insertion anchor, so patch verification rejected every hunk and changed no file.", "recovery": "Read exact local anchors and apply the privacy definition, counts, retry allowlist, and validator updates as independent patches.", "passing": "All narrow patches applied to their exact intended sections and the corrected closeout builder compiled.", "recurrence_guard": "Do not couple generated-list insertion to unrelated count and precondition changes in one patch."},
]

REJECTED_COLLISIONS = [
    {"seed": "saga compensation tribunal", "reason": "already frozen in v650-v7"},
    {"seed": "MVCC write-skew tribunal", "reason": "already frozen in v650-v7"},
    {"seed": "Tomonaga-Schwinger board", "reason": "already frozen in v650-v7"},
    {"seed": "Bogoliubov causality board", "reason": "already frozen in v650-v7"},
    {"seed": "4XMM-DR14 adapter", "reason": "already frozen in v650-v7"},
    {"seed": "aquatic-centre handover", "reason": "already frozen in v650-v7"},
    {"seed": "RFC 7662 introspection profile", "reason": "already frozen in v650-v7"},
    {"seed": "RFC 7800 cnf profile", "reason": "already frozen in v650-v7"},
    {"seed": "Git packfile tribunal", "reason": "already frozen in v650-v7"},
    {"seed": "DWARF refusal tribunal", "reason": "already frozen in v650-v7"},
    {"seed": "accessible search audit", "reason": "already frozen in v650-v7"},
    {"seed": "Gouy-Stodola classifier", "reason": "already frozen in v650-v7"},
    {"seed": "complex-step differentiation", "reason": "already frozen in v650-v7"},
    {"seed": "negative-control board", "reason": "already frozen in v650-v7"},
    {"seed": "COSE-HPKE draft board", "reason": "already frozen in v650-v7"},
    {"seed": "Bundle Protocol v7 tribunal", "reason": "already frozen in v650-v7"},
    {"seed": "DNS master-file tribunal", "reason": "already frozen in v650-v7"},
    {"seed": "JSON Lines tribunal", "reason": "already frozen in v650-v7"},
    {"seed": "sterile compounding handover", "reason": "already frozen in an earlier practice lane; reusable-device reprocessing is the distinct v650-v8 mechanism"},
    {"seed": "medical-device authorization profile", "reason": "already frozen; v650-v8 keeps JWK and JWT BCP semantics distinct"},
]
