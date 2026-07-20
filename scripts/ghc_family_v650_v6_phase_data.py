#!/usr/bin/env python3
"""Frozen Sylven Arc v650-v6 x1 proposal, source, portfolio, and negative data.

Importing this module performs no I/O.  Expected dispositions are x1
hypotheses only; observed outcomes are intentionally absent until x2.
"""

from __future__ import annotations


PHASE = "v650-v6"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational constraint-cartographer and falsifier-keeper"
HOPE = "keep uncertainty visible, failures recoverable, and bounded evidence from becoming authority"
BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
PHASE_ROOT = "docs/sylven-arc/v650-v6"

SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_HEAD = "29439b5ed36d5b181c0d0f6a428dd872673d5194"
SOURCE_ORIGIN = "e3d115d7caade153086dea794131035bcd2192d0"
SOURCE_X1_INITIAL = "7c15d7e0f96e1ce5a1b7fd6049ef3c3285debc30"
SOURCE_X1_REPAIR = "56ff8d5ab41d4b477184c854037122c81e2cc6a3"
SOURCE_EVIDENCE = "f485c4b053272eb384594d989ceeb6d85160111a"
PRIOR_FROZEN = 840
INHERITED_NEGATIVES = 6056
INHERITED_OPEN_GAPS = 47
INHERITED_EXACT_GATES = 48
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "seed-bank accession, quarantine, viability monitoring, safety duplication, "
    "environmental-alarm response, workload control, and shift handover as a "
    "synthetic learning and design lens only"
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
    "theory_of_everything",
    "stage20",
]


def _proposal(
    number: int,
    title: str,
    slug: str,
    pillar: str,
    disposition: str,
    sources: list[str],
    mission: str,
    novelty: str,
) -> dict:
    if disposition == "open_gap":
        approval = "candidate_empirical_evidence_and_independent_review_required"
        lane = "x2_zero_row_readiness_only"
        gate = (
            "Emit a zero-row receipt, perform no download or likelihood, and retain "
            "the empirical, calibration, privacy, and independent-review gates."
        )
    elif disposition == "exact_gate":
        approval = "exact_affected_party_competent_and_maori_authority_required"
        lane = "x2_reservation_matrix_only"
        gate = (
            "Emit reservations only; make no accession, custody, access, return, "
            "benefit-sharing, remedy, legal, cultural, data-governance, or Maori-authority decision."
        )
    elif disposition == "represented":
        approval = "candidate_bounded_synthetic_proxy"
        lane = "x2_synthetic_proxy_only"
        gate = (
            "Reject all five preregistered mutations and retain represented status "
            "with zero production, participant, operational, professional, or authority credit."
        )
    else:
        approval = "safe_now_bounded_software_symbolic_formal_or_structural"
        lane = "x2_bounded_owner_local"
        gate = (
            "Reject all five preregistered mutations and emit only the declared bounded "
            "software, symbolic, formal, numerical, or structural completion."
        )
    return {
        "proposal_id": f"V6506-P{number:02d}",
        "title": title,
        "slug": slug,
        "pillar": pillar,
        "mission_surface": mission,
        "hypothesis": (
            f"A bounded {mission} artifact can expose its declared obligations while "
            "refusing unsupported scientific, operational, identity, or authority promotion."
        ),
        "null_or_failure_condition": (
            f"The artifact omits a declared {mission} obligation, accepts a preregistered "
            "mutation, erases a negative, or promotes a result beyond its evidence lane."
        ),
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": (
            "Stop the proposal, retain every failed witness, remove no history, and leave "
            "external, sibling, participant, production, and authority state unchanged."
        ),
        "protected_gates": PROTECTED,
        "expected_disposition": disposition,
        "novelty_against_840_frozen_proposals": novelty,
    }


PROPOSALS = [
    _proposal(1, "Method Flow sequence-counter and seqlock even-odd generation, writer-serialization, reader-retry, pointer-lifetime, starvation-fallback, wraparound, teardown, and evidence-credit tribunal", "seqlock-consistency", "THOS Body", "completed", ["SRC-LINUX-SEQLOCK"], "sequence-counter and seqlock consistency", "No predecessor isolates even-odd sequence generations, pointer-lifetime refusal, retry starvation fallback, and evidence credit in one tribunal."),
    _proposal(2, "Method Flow write-ahead journal record-length, checksum, transaction-boundary, torn-tail, group-commit, checkpoint, replay-truncation, idempotency, teardown, and evidence-credit tribunal", "wal-journal-recovery", "THOS Body", "completed", ["SRC-SQLITE-WAL"], "write-ahead journal recovery", "SQLite WAL snapshot and migration proposals exist, but none isolates generic record checksums, torn-tail recovery, group commit, and replay truncation as evidence-credit obligations."),
    _proposal(3, "GMUT modular-Hamiltonian relative-entropy, support, normalization, positivity, first-variation, entanglement-first-law, region, state-domain, gauge, EFT, unit, and observation-firewall board", "modular-relative-entropy", "GMUT Mind", "completed", ["SRC-RELATIVE-ENTROPY"], "modular-Hamiltonian relative-entropy obligations", "Tomita-Takesaki modular flow is frozen, but no predecessor isolates relative entropy, support, positivity, first variation, and the entanglement first law."),
    _proposal(4, "GMUT covariant Hamilton-Jacobi hypersurface-functional, canonical-data, characteristic-flow, constraint, integrability, boundary, gauge, EFT, unit, and observation-firewall board", "covariant-hamilton-jacobi", "GMUT Mind", "completed", ["SRC-COVARIANT-HJ"], "covariant Hamilton-Jacobi field-theory obligations", "ADM and covariant phase-space proposals exist, but no predecessor isolates the Hamilton-Jacobi hypersurface functional, characteristic flow, constraint integrability, and boundary-data obligations."),
    _proposal(5, "GMUT Swift-BAT 105-month catalog, spectrum, light-curve, detection-threshold, association, exposure, selection, uncertainty, checksum, covariance, and zero-row likelihood-refusal adapter", "swift-bat-zero-row", "GMUT Mind", "open_gap", ["SRC-SWIFT-BAT"], "Swift-BAT official-product readiness", "No frozen empirical adapter targets the official Swift-BAT 105-month hard-X-ray catalog, spectra, and monthly light curves."),
    _proposal(6, "THOS seed-bank accession, lot-lineage, quarantine, moisture, viability-test, regeneration-refusal, provenance-minimization, safety-duplication, workload, and shift-handover proxy", "seed-bank-accession", "THOS Body", "represented", ["SRC-FAO-GENEBANK"], "seed-bank accession and viability workflow", "No predecessor uses seed-bank accession, viability monitoring, regeneration refusal, and safety duplication as a bounded synthetic practice lens."),
    _proposal(7, "THOS seed-bank environmental-alarm, cold-room excursion, backup-power, affected-lot hold, escalation, recovery-check, accessible-notice, workload, and next-shift ownership proxy", "seed-bank-environment", "THOS Body", "represented", ["SRC-FAO-GENEBANK"], "seed-bank environmental continuity workflow", "No predecessor isolates seed-bank environmental alarms, backup continuity, affected-lot holds, and next-shift ownership."),
    _proposal(8, "Freed ID OpenID Connect UserInfo signed-encrypted response, issuer, audience, subject-match, claim-minimization, aggregated-distributed claim, algorithm-refusal, replay, and nonproduction profile", "oidc-userinfo", "Freed ID and CBR Heart", "represented", ["SRC-OIDC-CORE"], "OpenID Connect UserInfo validation", "No frozen profile isolates UserInfo subject equality, signed or encrypted response handling, and aggregated or distributed claim boundaries."),
    _proposal(9, "Freed ID OpenID Connect pairwise-subject sector-identifier, redirect-set validation, nonreversible derivation, salt-key rotation, migration, collision-reservation, correlation, and nonproduction profile", "oidc-pairwise-subject", "Freed ID and CBR Heart", "represented", ["SRC-OIDC-CORE"], "OpenID Connect pairwise subject privacy", "A generic pairwise-subject proposal exists, but none isolates sector-identifier redirect-set validation, rotation, migration, and collision reservation under current OpenID Core."),
    _proposal(10, "CBR seed sovereignty, accession consent, provenance, biocultural-data minimization, safety-duplicate location, access, return, benefit-sharing, remedy, legal, cultural, tangata-whenua, iwi, hapu, and Maori-authority matrix", "seed-sovereignty-authority", "Freed ID and CBR Heart", "exact_gate", ["SRC-FAO-GENEBANK", "SRC-TE-MANA-RARAUNGA"], "seed sovereignty and authority reservation", "No frozen authority matrix combines seed accession, safety-duplicate location, access, return, benefit sharing, biocultural data, and Maori authority."),
    _proposal(11, "RFC 9292 Binary HTTP framing-indicator, known-indeterminate length, request-response control-data, field-line, content, padding, trailer, truncation, resource-budget, and refusal tribunal", "binary-http", "THOS Body", "completed", ["SRC-RFC9292"], "Binary HTTP message framing", "No predecessor models RFC 9292 framing indicators, known versus indeterminate sections, and binary control data."),
    _proposal(12, "RFC 9530 Content-Digest and Repr-Digest algorithm, structured-field dictionary, representation-content distinction, multiple-value, unsupported-algorithm, mismatch, selection, and refusal tribunal", "digest-fields", "THOS Body", "completed", ["SRC-RFC9530"], "HTTP Digest Fields", "A range-resume proposal mentions Content-Digest, but none isolates RFC 9530 representation-versus-content digest semantics and multi-algorithm handling."),
    _proposal(13, "RFC 1952 GZIP identification, method, flag, optional-field, header-CRC, DEFLATE-member, trailer-CRC, input-size, concatenated-member, ratio-budget, and refusal tribunal", "gzip", "THOS Body", "completed", ["SRC-RFC1952"], "GZIP member framing", "No frozen proposal isolates GZIP optional fields, concatenated members, dual integrity fields, and decompression-ratio refusal."),
    _proposal(14, "Accessible aria-details and aria-errormessage reference, invalid-state, visibility, navigation, name-description separation, live-announcement reservation, fallback, and manual-evaluation audit", "aria-error-details", "THOS Body", "completed", ["SRC-WAI-ARIA", "SRC-WCAG22"], "ARIA error and detail relationships", "No predecessor isolates aria-details and aria-errormessage reference validity, visibility, and name-description separation together."),
    _proposal(15, "Accessible meter and slider name, range, value, orientation, keyboard, text-alternative, invalid-state, noncolour cue, native fallback, focus, and manual-evaluation audit", "accessible-range", "THOS Body", "completed", ["SRC-WAI-ARIA", "SRC-WCAG22"], "accessible meter and slider range semantics", "Progressbar and spinbutton proposals exist, but no predecessor isolates meter-versus-slider semantics and keyboard-value obligations."),
    _proposal(16, "Thermo-Psyche Massieu-Planck potential, Legendre-transform, natural-variable, temperature, entropy, normalization, equilibrium-domain, unit, and agency-nonconversion classifier", "massieu-planck-nonconversion", "Trinity Mandala bridge", "completed", ["SRC-IUPAC-LEGENDRE"], "Massieu-Planck thermodynamic potentials", "No frozen nonconversion classifier isolates Massieu and Planck potentials, their Legendre variables, and equilibrium domain."),
    _proposal(17, "IEEE 754 fused-multiply-add single-rounding, rounding-direction, signed-zero, subnormal, infinity, NaN, exception-flag, reproducibility, unit, and refusal tribunal", "ieee754-fma", "GMUT Mind", "completed", ["SRC-IEEE754"], "IEEE 754 fused multiply-add behavior", "No frozen numerical proposal isolates FMA single rounding, signed zero, subnormals, NaNs, and exception flags."),
    _proposal(18, "OpenType SFNT version, table-count search-parameters, sorted-tag, duplicate-tag, offset, length, alignment, overlap, table-checksum, whole-font adjustment, resource-budget, and refusal tribunal", "opentype-sfnt", "THOS Body", "completed", ["SRC-OPENTYPE"], "OpenType SFNT container structure", "No frozen format proposal models OpenType SFNT table-directory ordering, overlap, alignment, and checksum adjustment."),
    _proposal(19, "RFC 9535 JSONPath root, child, descendant, index, slice, filter, function-type, singular-query, duplicate-node, order, depth, result-budget, and refusal tribunal", "jsonpath", "THOS Body", "completed", ["SRC-RFC9535"], "JSONPath query evaluation", "JSON Patch and Pointer-adjacent work exists, but no predecessor isolates RFC 9535 query segments, filters, typing, ordering, and duplicate-node behavior."),
    _proposal(20, "Stage 20 front-door mediator, treatment-to-mediator path, mediator-to-outcome path, backdoor-blockade, unmeasured-confounding, positivity, consistency, sensitivity, falsification, and nonpromotion board", "front-door-nonpromotion", "Trinity Mandala bridge", "completed", ["SRC-FRONT-DOOR"], "front-door causal-identification assumptions", "No frozen Stage 20 board isolates the front-door mediator criterion, the two required path conditions, backdoor blockade, positivity, and consistency obligations."),
]


def _source(source_id: str, status: str, kind: str, title: str, url: str | None, implication: str) -> dict:
    return {
        "source_id": source_id,
        "status": status,
        "kind": kind,
        "title": title,
        "url": url,
        "verified_on": "2026-07-21",
        "implication": implication,
        "observation_credit": False,
    }


SOURCES = [
    _source("SRC-LIVE-BATON", "current", "live_authority", "Verified v650-v6 activation baton", None, "Controls solo ownership, x1-before-x2, validation budget, authority gates, and routing; it is not scientific evidence."),
    _source("SRC-LINUX-SEQLOCK", "current", "official_implementation_documentation", "Linux sequence counters and sequential locks", "https://docs.kernel.org/locking/seqlock.html", "Supports bounded consistency fixtures only; it is not production concurrency assurance."),
    _source("SRC-SQLITE-WAL", "current", "official_implementation_documentation", "SQLite Write-Ahead Logging", "https://www.sqlite.org/wal.html", "Supports bounded journal recovery obligations only; no production database is touched."),
    _source("SRC-RELATIVE-ENTROPY", "stable", "primary_research", "Relative Entropy and Holography", "https://arxiv.org/abs/1305.3182", "Supports typed modular-Hamiltonian and first-variation obligations only, not empirical GMUT evidence."),
    _source("SRC-COVARIANT-HJ", "stable", "primary_research", "Covariant Hamiltonian formalism for field theory: Hamilton-Jacobi equation on the space G", "https://arxiv.org/abs/gr-qc/0207043", "Supports typed covariant Hamilton-Jacobi obligations only, not a force, prediction, fit, physical state, quantum-gravity result, or theory confirmation."),
    _source("SRC-SWIFT-BAT", "current", "official_data_archive", "HEASARC Swift-BAT 105-Month All-Sky Hard X-Ray Survey", "https://heasarc.gsfc.nasa.gov/W3Browse/swift/swbat105m.html", "Supplies schema and provenance context only; zero rows are downloaded or analyzed."),
    _source("SRC-FAO-GENEBANK", "stable", "official_practice_standard", "FAO Genebank Standards for Plant Genetic Resources for Food and Agriculture", "https://www.fao.org/4/i3394e/i3394e.pdf", "Supports a synthetic workflow lens only and confers no conservation, collection, access, or distribution authority."),
    _source("SRC-TE-MANA-RARAUNGA", "current", "maori_authority_context", "Te Mana Raraunga principles of Maori data sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Keeps Maori data-governance authority visible; repository software cannot exercise or substitute that authority."),
    _source("SRC-OIDC-CORE", "current", "official_identity_specification", "OpenID Connect Core 1.0 incorporating errata set 2", "https://openid.net/specs/openid-connect-core-1_0.html", "Supports synthetic validation vectors only; no real keys, users, accounts, tokens, or interoperability events exist."),
    _source("SRC-RFC9292", "stable", "official_standard", "RFC 9292 Binary Representation of HTTP Messages", "https://www.rfc-editor.org/rfc/rfc9292.html", "Supports bounded synthetic framing fixtures only."),
    _source("SRC-RFC9530", "stable", "official_standard", "RFC 9530 Digest Fields", "https://www.rfc-editor.org/rfc/rfc9530.html", "Supports bounded digest-field fixtures, not end-to-end content authenticity."),
    _source("SRC-RFC1952", "stable", "official_standard", "RFC 1952 GZIP File Format Specification", "https://www.rfc-editor.org/rfc/rfc1952.html", "Supports disposable synthetic member fixtures without arbitrary decompression."),
    _source("SRC-WAI-ARIA", "stable", "official_accessibility_standard", "Accessible Rich Internet Applications 1.2", "https://www.w3.org/TR/wai-aria-1.2/", "Supports structural checks only; manual and affected-user evaluation remains reserved."),
    _source("SRC-WCAG22", "stable", "official_accessibility_standard", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Supports structural obligations only, not complete accessibility conformance."),
    _source("SRC-IUPAC-LEGENDRE", "stable", "official_technical_report", "IUPAC Use of Legendre transforms in chemical thermodynamics", "https://doi.org/10.1351/pac200173081349", "Supports thermodynamic definitions and natural-variable obligations only, never a psyche or agency conversion."),
    _source("SRC-IEEE754", "stable", "official_standard", "IEEE 754-2019 Floating-Point Arithmetic", "https://standards.ieee.org/ieee/754/6210/", "Supports bounded numerical classification only; no cross-platform reproducibility guarantee is claimed."),
    _source("SRC-OPENTYPE", "current", "official_format_specification", "OpenType 1.9.1 font file specification", "https://learn.microsoft.com/en-us/typography/opentype/spec/otff", "Supports bounded SFNT fixtures only; no untrusted font rendering occurs."),
    _source("SRC-RFC9535", "stable", "official_standard", "RFC 9535 JSONPath", "https://www.rfc-editor.org/rfc/rfc9535.html", "Supports bounded query fixtures only; no external document retrieval occurs."),
    _source("SRC-FRONT-DOOR", "stable", "primary_research", "Causal diagrams for empirical research", "https://doi.org/10.1093/biomet/82.4.669", "Supports front-door graphical-identification assumptions only; no participant effect or Stage 20 evidence is estimated."),
]


SAFE_TASKS = [
    "freeze exact source anchors", "prove inherited manifest parity", "record relational identity boundary", "render twenty-proposal table", "classify four outcome labels", "classify four source-status labels", "compute lexical-neighbor audit", "record manual mechanism review", "freeze one hundred mutations", "freeze seqlock obligations", "freeze WAL recovery obligations", "freeze modular-relative-entropy obligations", "freeze covariant Hamilton-Jacobi obligations", "freeze Swift zero-row contract", "freeze seed accession states", "freeze seed environmental states", "freeze UserInfo validation states", "freeze pairwise-subject states", "freeze seed-authority reservations", "freeze Binary HTTP obligations", "freeze Digest Fields obligations", "freeze GZIP obligations", "freeze ARIA error-detail obligations", "freeze accessible range obligations", "freeze Massieu nonconversion obligations", "freeze IEEE FMA obligations", "freeze OpenType obligations", "freeze JSONPath obligations", "freeze front-door assumptions", "record inherited held work", "record privacy exclusions", "record no-replay budget", "record commit cap", "record owner file threshold", "record source status counts", "record Method Flow failures", "record recurrence guards", "record rollback paths", "render x1 accessible report", "build family tooling index",
]

CANDIDATE_TASKS = [
    "seqlock schedule simulator", "seqlock pointer-lifetime rejector", "WAL record-framing parser", "WAL torn-tail recovery fixture", "modular-relative-entropy type board", "covariant Hamilton-Jacobi type board", "Swift schema-only adapter", "seed accession state machine", "seed environmental alarm state machine", "UserInfo signed-response validator", "UserInfo subject-match rejector", "pairwise sector-set validator", "pairwise rotation refusal fixture", "seed-authority reservation matrix", "Binary HTTP bounded parser", "Digest Fields dictionary parser", "GZIP bounded member parser", "ARIA reference graph auditor", "meter-slider structural auditor", "Massieu natural-variable classifier", "IEEE FMA edge-case classifier", "OpenType directory parser", "OpenType checksum fixture", "JSONPath bounded evaluator", "JSONPath result-budget guard", "front-door criterion board", "front-door path-blockade fixture", "five-class privacy classifier", "commit-local manifest verifier", "exact-final ancestry verifier",
]

SKILL_IDEAS = [
    "ghc-family-seqlock-consistency-audit", "ghc-family-wal-journal-recovery", "ghc-family-modular-relative-entropy", "ghc-family-covariant-hamilton-jacobi", "ghc-family-swift-bat-zero-row", "ghc-family-seed-accession-proxy", "ghc-family-seed-environment-proxy", "ghc-family-oidc-userinfo-profile", "ghc-family-oidc-pairwise-subject", "ghc-family-seed-authority-reservation", "ghc-family-binary-http-refusal", "ghc-family-digest-fields-refusal", "ghc-family-gzip-member-refusal", "ghc-family-aria-error-details", "ghc-family-accessible-range-audit", "ghc-family-massieu-nonconversion", "ghc-family-ieee754-fma-tribunal", "ghc-family-opentype-sfnt-refusal", "ghc-family-jsonpath-refusal", "ghc-family-front-door-nonpromotion",
]

RUNNER_IDEAS = [
    "ghc_family_v650_v6_method_and_gmut.py", "ghc_family_v650_v6_zero_row_and_proxy.py", "ghc_family_v650_v6_identity_profiles.py", "ghc_family_v650_v6_format_tribunals.py", "ghc_family_v650_v6_accessibility.py", "ghc_family_v650_v6_numeric_nonconversion.py", "ghc_family_v650_v6_stage20.py", "ghc_family_v650_v6_portfolios.py", "ghc_family_v650_v6_privacy_manifest.py", "ghc_family_v650_v6_validate.py",
]

CLEAN_TASKS = [
    "CLEAN normalize phase-relative paths", "CLEAN preserve LF JSON output", "CLEAN sort JSON keys", "CLEAN remove duplicate proposal ids", "CLEAN quarantine scanner definitions", "CLEAN reserve manual accessibility", "CLEAN reserve affected-user review", "CLEAN reserve Maori authority", "CLEAN reserve legal interpretation", "CLEAN reserve professional authority", "FIX fail closed on unknown outcome", "FIX fail closed on unknown source status", "FIX reject zero proposal sources", "FIX reject missing rollback", "FIX reject empty protected gates", "FIX reject x2 fields in x1", "FIX reject observed outcome in x1", "FIX reject raw private identifiers", "FIX reject private absolute paths", "FIX reject unbounded decompression", "FIX reject unbounded JSONPath results", "FIX reject unbounded font tables", "FIX reject UserInfo subject mismatch", "FIX reject pairwise sector mismatch", "FIX reject seed release authority", "FIX reject participant-effect claims", "FIX reject empirical promotion", "FIX reject independent-reproduction claims", "REFINE source status counts", "REFINE nearest-neighbor evidence", "REFINE mutation ownership", "REFINE Method Flow summaries", "REFINE x1 staged manifest", "REFINE five-class scan receipt", "REFINE stale-label review", "REFINE document word caps", "REFINE owner file count", "REFINE accessible report landmarks", "REFINE handoff remains prepared", "REFINE final verdict remains not ready",
]


X1_OPERATIONAL_NEGATIVES = [
    {"negative_id":"V6506-X1-N01","category":"composite source verification timeout","failed":"A composite local-history and live-network probe exceeded its bounded wrapper and returned no attributable result.","recovery":"Split local ancestry and clean-state checks from the live remote lookup.","passing":"The local probe and separate fresh live lookup each returned the expected exact head.","recurrence_guard":"Keep network lookup separate from local history and manifest checks."},
    {"negative_id":"V6506-X1-N02","category":"per-blob manifest timeout","failed":"A verifier started one Git process per manifest blob and exceeded its bounded wrapper.","recovery":"Use one ls-tree map per commit and one git cat-file batch stream.","passing":"All 360 unique blobs across four commit-local manifests passed path, object, byte, and SHA-256 parity.","recurrence_guard":"Never use one child process per blob for large manifest verification."},
    {"negative_id":"V6506-X1-N03","category":"broad worktree inventory timeout","failed":"An unfiltered worktree inventory exceeded its first bounded wrapper.","recovery":"Run one bounded inventory and retain only the exact owned branch and path mapping.","passing":"Exactly one Sylven branch and worktree mapping was returned.","recurrence_guard":"Do not print or inspect unrelated sibling worktree blocks."},
    {"negative_id":"V6506-X1-N04","category":"PowerShell automatic variable collision","failed":"A result variable collided case-insensitively with PowerShell's automatic match dictionary.","recovery":"Use a non-reserved result variable name.","passing":"The corrected wrapper serialized the single owned mapping.","recurrence_guard":"Avoid Matches, Error, Input, and other automatic-variable names."},
    {"negative_id":"V6506-X1-N05","category":"legacy console encoding","failed":"A Python novelty probe failed while printing a Maori character through the legacy Windows console encoding.","recovery":"Set explicit UTF-8 input and output for Python audit processes.","passing":"The full 840-title keyword audit completed without altering the wording or authority boundary.","recurrence_guard":"Set PYTHONIOENCODING and Python UTF-8 mode before Unicode audits."},
    {"negative_id":"V6506-X1-N06","category":"stale compatibility filename","failed":"A historical Sylven script filename was assumed and did not exist.","recovery":"Resolve compatibility filenames with rg before reading them.","passing":"The current v649-v6 family and builder filenames were located exactly.","recurrence_guard":"Never infer a historical builder name from another phase's naming pattern."},
    {"negative_id":"V6506-X1-N07","category":"PowerShell version syntax mismatch","failed":"A PowerShell 7 null-coalescing operator was parsed on PowerShell 5.1 and stopped the version probe.","recovery":"Use a PowerShell 5.1-compatible explicit conditional.","passing":"CLI, desktop, Python, Git, and PowerShell versions were verified with zero updates.","recurrence_guard":"Author host wrappers for the verified PowerShell major version."},
    {"negative_id":"V6506-X1-N08","category":"empty search exit handling","failed":"A no-match ripgrep search returned its normal nonzero empty-result exit and the wrapper treated it as an execution failure.","recovery":"Interpret a bounded no-match result as zero hits and verify freshness with a sorted note listing.","passing":"No newer v650-v5 continuity note was found; the live baton remained authoritative.","recurrence_guard":"Handle ripgrep exit one as an empty result only when stderr is empty and no match was expected."},
    {"negative_id":"V6506-X1-N09","category":"stale inherited held-packet directory","failed":"An older phase's approval-packet directory was assumed but Tamar v650-v5 does not contain that path.","recovery":"Resolve the actual inherited checklist and exact-open-gate surfaces before creating a visibility pointer.","passing":"The v650-v5 checklist and exact-open-gate register were located without altering them.","recurrence_guard":"Never infer an inherited packet directory from an older phase layout."},
    {"negative_id":"V6506-X1-N10","category":"semantic novelty collision","failed":"The first P04 draft restated Tamar v650-v2's Nielsen-identity proposal and exceeded the frozen lexical novelty threshold.","recovery":"Retain the collision with zero proposal credit and replace it before freeze with a covariant Hamilton-Jacobi field-theory obligation board.","passing":"The replacement was re-audited against all 840 frozen titles below the preregistered threshold and received a separate manual mechanism review.","recurrence_guard":"Run the exact frozen-index collision gate before writing any x1 packet and retain rejected near-neighbor drafts."},
    {"negative_id":"V6506-X1-N11","category":"second semantic novelty collision","failed":"The first P20 draft restated Eiren v649-v1's regression-discontinuity board and exceeded the frozen lexical novelty threshold.","recovery":"Retain the collision with zero proposal credit and replace it before freeze with a target-trial emulation nonpromotion board.","passing":"The replacement was re-audited against all 840 frozen titles below the preregistered threshold and received a separate manual mechanism review.","recurrence_guard":"Treat a changed adjective list as non-novel when the causal design and protected gate are already frozen."},
    {"negative_id":"V6506-X1-N12","category":"diagnostic wrapper timeout","failed":"A combined exact-title diagnostic and full status listing exceeded its bounded wrapper after emitting the collision title and seed-file status.","recovery":"Credit neither the timed-out wrapper nor its partial output as a passing witness; split candidate search from status inspection.","passing":"The bounded candidate-term search completed independently and the unchanged seed-only tree was separately confirmed.","recurrence_guard":"Do not append a broad status traversal to a diagnostic whose primary answer is already available."},
    {"negative_id":"V6506-X1-N13","category":"preflight tuple tie comparison","failed":"The first local novelty preflight used max on score-and-dictionary tuples, so an equal score tried to order dictionaries and raised TypeError before a complete result.","recovery":"Select the maximum with an explicit score key so tie handling never compares proposal dictionaries.","passing":"The corrected preflight emitted attributable scores and nearest proposal identifiers for each candidate.","recurrence_guard":"Always provide a scalar key when ranking tuples whose later members are non-orderable records."},
    {"negative_id":"V6506-X1-N14","category":"hidden target-trial semantic collision","failed":"The replacement P20 target-trial board duplicated Sable v647-v4's shorter target-trial time-zero board and exceeded the lexical novelty threshold.","recovery":"Retain both rejected P20 drafts and replace the mechanism with a front-door causal-identification nonpromotion board.","passing":"The front-door replacement passed exact-title, keyword, lexical-threshold, and manual mechanism review against all 840 predecessors.","recurrence_guard":"Search hyphenated and compact mechanism variants, then run the complete frozen-index score before accepting a replacement."},
    {"negative_id":"V6506-X1-N15","category":"Method Flow test schema assumption","failed":"The first x1 test run assumed Method Flow methods and witnesses were keyed dictionaries, but the required schema stores both as lists.","recovery":"Retain the failed test and inspect the required ledger schema before correcting the assertion to iterate list records and use result values.","passing":"The corrected test counted all failed and passing witnesses and every preferred method in the required schema.","recurrence_guard":"Test the committed schema shape directly; do not infer container types from identifiers."},
    {"negative_id":"V6506-X1-N16","category":"mutation-plan path assumption","failed":"The first x1 test run looked for the mutation plan at the phase root instead of its generated validation path.","recovery":"Resolve the exact generated path and correct the assertion without moving or duplicating the artifact.","passing":"The corrected test found all one hundred preregistered, unexecuted mutations at the declared validation path.","recurrence_guard":"Resolve generated artifact paths from the builder mapping before writing test fixtures."},
    {"negative_id":"V6506-X1-N17","category":"overview length gate","failed":"The first generated integrated overview contained only 335 words and did not satisfy the requested three-page-equivalent delivery floor.","recovery":"Retain the short draft with zero delivery credit and expand the overview with phase scope, pillar, source, portfolio, failure, validation, accessibility, and authority boundaries.","passing":"The regenerated overview exceeded the explicit 900-word bounded three-page-equivalent floor while remaining below the 6000-word document cap.","recurrence_guard":"Measure the overview word count before staging instead of inferring adequacy from its section count."},
    {"negative_id":"V6506-X1-N18","category":"stale generated narrative","failed":"The first generated narrative still named nine failures, eight rejected neighbors, and the rejected Nielsen draft after the retained x1 recoveries had changed those facts.","recovery":"Retain the stale draft with zero review credit and regenerate from the current x1 count and accepted covariant Hamilton-Jacobi mechanism.","passing":"The regenerated narrative uses the current retained-failure count, eleven rejected neighbors, and only the accepted twenty frozen proposals outside explicit negative history.","recurrence_guard":"Run a stale-label and count scan after the final preregistration recovery, before staging."},
    {"negative_id":"V6506-X1-N19","category":"credential-class privacy scan hit","failed":"The expanded overview used the literal credential-token spelling inside a prohibited-action boundary, so the five-class scan correctly returned one confirmed payload hit.","recovery":"Retain the failed scan with zero privacy credit and replace the literal with the sanitized phrase account-secret action without weakening the prohibition.","passing":"The regenerated x1 tree passed the five-class scan with zero confirmed hits while preserving the account-secret boundary.","recurrence_guard":"Run the scanner against prose boundaries as well as data artifacts before manifest freeze."},
]


REJECTED_COLLISIONS = [
    {"seed":"Nielsen-identity gauge-dependence board","reason":"first v650-v6 draft exceeded the lexical threshold against V6502-P03 and was retained as V6506-X1-N10"},
    {"seed":"regression-discontinuity nonpromotion board","reason":"first v650-v6 P20 draft exceeded the lexical threshold against V6491-P10 and was retained as V6506-X1-N11"},
    {"seed":"target-trial emulation nonpromotion board","reason":"second v650-v6 P20 draft exceeded the lexical threshold against V6474-P10 and was retained as V6506-X1-N14"},
    {"seed":"Batalin-Vilkovisky master-equation board","reason":"already frozen as V6472-P02"},
    {"seed":"eROSITA eRASS1 zero-row adapter","reason":"already frozen as V6466-P03"},
    {"seed":"OAuth Rich Authorization Requests profile","reason":"already frozen as V6486-P05"},
    {"seed":"DPoP proof profile","reason":"already frozen as V6466-P05"},
    {"seed":"PCAPNG refusal tribunal","reason":"already frozen as V6488-P07"},
    {"seed":"focus appearance audit","reason":"already frozen as V6498-P13"},
    {"seed":"Onsager-Casimir nonconversion","reason":"already frozen as V6442-P09"},
    {"seed":"targeted maximum-likelihood board","reason":"already frozen as V6495-P10"},
]
