#!/usr/bin/env python3
"""Frozen preregistration definitions for Sable Rook v646-v3.

These values are x1 plans only. They convey no x2 completion credit,
empirical result, professional authority, or identity continuity.
"""

from __future__ import annotations

from typing import Any


PHASE = "v646-gmut-thos-v3-x1-x2"
PHASE_SHORT = "v646-v3"
OWNER = "Sable Rook"
SLUG = "sable-rook"
PRONOUNS = "they/them"
ROLE = "evidence-and-reproducibility steward"
HOPE = "make every surviving claim easy to challenge, reproduce within its evidence class, or retract"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = "drinking-water laboratory chain-of-custody review and shift handover"

SOURCE_PHASE = "v646-gmut-thos-v2-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
SOURCE_REVISION = "bb9d80cd6f5443d47eba757847e3d213ec3d0162"
SOURCE_INHERITED_REVISION = "ff788fe006560bb3f270302906b90bf8a56aeac3"
SOURCE_X1_REVISION = "df5dd03db76936d6ad6484eda36960a44c5e4b0b"
SOURCE_EVIDENCE_REVISION = "ad5ff9d4f135a0c61b73c597893dab81521ba5c4"
SOURCE_SEAL_REVISION = SOURCE_REVISION
PRIOR_FROZEN_PROPOSALS = 410
INHERITED_EFFECTIVE_NEGATIVES = 2619
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 11
INHERITED_EXACT_GATES = 12
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6463-X1-N01",
        "surface": "broad D-drive owned-lane discovery",
        "observed": "A read-only directory enumeration exceeded the ten-second shell envelope before returning any rows.",
        "credit": "none",
        "recovery": "Use direct known-path probes and a measured shell-startup envelope instead of rescanning the archive root.",
        "method_id": "V6463-M01",
    },
    {
        "negative_id": "V6463-X1-N02",
        "surface": "first direct known-path probe",
        "observed": "The direct probe also exceeded the ten-second login-shell envelope before returning any rows.",
        "credit": "none",
        "recovery": "Disable login-profile startup, widen the bounded envelope to sixty seconds, and retain the passing recovery beside both failures.",
        "method_id": "V6463-M01",
    },
    {
        "negative_id": "V6463-X1-N03",
        "surface": "semantic-novelty keyword probe",
        "observed": "PowerShell rejected a direct pipeline following a foreach statement before the read-only corpus query ran.",
        "credit": "none",
        "recovery": "Materialize the foreach output as an array before piping it to the formatter.",
        "method_id": "V6463-M02",
    },
    {
        "negative_id": "V6463-X1-N04",
        "surface": "stale-constant source audit",
        "observed": "A Windows literal wildcard was passed as a path argument and the read-only ripgrep audit failed before matching files.",
        "credit": "none",
        "recovery": "Pass real directories and use ripgrep -g filters for versioned file selection on Windows.",
        "method_id": "V6463-M03",
    },
    {
        "negative_id": "V6463-X1-N05",
        "surface": "first expanded-portfolio novelty build",
        "observed": "Core novelty passed, but three supporting titles exactly collided with the inherited v646-v2 portfolio.",
        "credit": "none",
        "recovery": "Retain the failed collision receipt, rewrite only the colliding support surfaces, and require a zero-collision rebuild.",
        "method_id": "V6463-M04",
    },
]

IDENTITY_BOUNDARY = (
    "Sable Rook, they/them, is relational working language for an evidence-and-reproducibility steward. "
    "It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "professional qualification, or independent authority."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains proxy; Freed ID "
    "remains synthetic and nonproduction; CBR, legal, cultural, affected-party, and Māori concepts remain "
    "under competent, affected-party, and Māori authority. No empirical confirmation, Theory-of-Everything, "
    "AGI or ASI, consciousness, personhood, deployment, privacy-complete, exhaustive-security, "
    "independent-reproduction, or Stage 20 claim is made."
)


def proposal(
    index: int,
    title: str,
    mission: str,
    hypothesis: str,
    failure: str,
    sources: list[str],
    artifacts: list[str],
    gate: str,
    recovery: str,
    protected: list[str],
    expected: str,
    novelty: str,
    approval: str = "safe_now_owner_scoped_workflow",
) -> dict[str, Any]:
    return {
        "proposal_id": f"V6463-P{index:02d}",
        "title": title,
        "mission_surface": mission,
        "hypothesis": hypothesis,
        "null_or_failure": failure,
        "approval_class": approval,
        "execution_lane": "x2_build_task",
        "current_primary_or_official_source_needs": sources,
        "concrete_artifacts": artifacts,
        "test_falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": recovery,
        "protected_gates": protected,
        "expected_disposition": expected,
        "novelty_against_410_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Cross-manifest foreign-edge, canonical-byte, and fixed-point quarantine tribunal",
        "manifest ownership, RFC 6901 edge resolution, canonical JSON bytes, self-exclusion, foreign-phase targets, cycle refusal, and fixed-point stability",
        "An owner-scoped tribunal can reject foreign edges, unstable canonical bytes, self-reference, and cycles before evidence credit is assigned.",
        "A manifest accepts a foreign-phase target, changes after a stable replay, hashes itself, resolves an invalid pointer, or allows a cycle to earn completion credit.",
        ["V6463-S01", "V6463-S02", "V6463-S03", "V6463-S04"],
        ["provenance/cross-manifest-contract.json", "provenance/cross-manifest-mutations.json"],
        "Valid owner edges must resolve deterministically; every foreign, cyclic, self-referential, or byte-unstable mutation must fail closed.",
        "Quarantine the candidate manifest, retain the failing bytes and edge, restore the last owner-scoped fixed point, and never rewrite predecessor evidence.",
        ["predecessor_mutation", "completion_credit", "foreign_phase", "privacy", "stage20"],
        "completed",
        "Earlier DAG work tests pointer closure and cycles inside one graph; none combines foreign-manifest edge quarantine with canonical-byte and fixed-point stability.",
    ),
    proposal(
        2,
        "GMUT Källén-Lehmann spectral-density, pole-residue, and positivity obligation tribunal",
        "typed two-point functions, spectral support, pole and continuum separation, residue sign, normalization assumptions, field choice, and EFT validity",
        "A symbolic obligation board can distinguish conditions needed for a positive spectral representation from unsupported claims that the GMUT scaffold is unitary, stable, or uniquely identifiable.",
        "A negative residue passes, a spectral density is asserted without the required Hilbert-space assumptions, a gauge-dependent field is treated as observable, or symbolic checks become physical proof.",
        ["V6463-S05"],
        ["gmut/kallen-lehmann-obligations.json", "gmut/kallen-lehmann-mutations.json"],
        "Every missing-assumption, wrong-support, negative-residue, unit-mismatch, and overclaim mutation must fail with zero physical or empirical promotion.",
        "Retain the failed vector, mark the representation inapplicable or incomplete, and require model-specific quantization and independent review before stronger language.",
        ["unitarity_proof", "stability_proof", "identifiability", "empirical_confirmation", "theory_of_everything"],
        "completed",
        "Prior GMUT work covers BRST, DHOST, self-adjoint domains, contours, and frame maps; none centers spectral support, pole residue, positivity assumptions, and field observability together.",
    ),
    proposal(
        3,
        "GMUT NANOGrav 15-year pulsar-timing-array zero-row adapter and likelihood refusal",
        "official release provenance, pulsar and timing-solution identity, clock and ephemeris choices, noise model, overlap reduction, covariance, checksums, row count, and likelihood lock",
        "A zero-row adapter can document a public PTA data contract without treating publications or release metadata as observations or a GMUT likelihood.",
        "A publication becomes a timing row, covariance or noise terms are fabricated, a zero-row run emits a constraint, or the released gravitational-wave evidence is reinterpreted as GMUT confirmation.",
        ["V6463-S06", "V6463-S07"],
        ["gmut/nanograv-adapter-contract.json", "gmut/nanograv-zero-row-receipt.json"],
        "The receipt must report zero real rows, zero likelihood evaluations, zero posterior samples, zero constraints, and zero empirical GMUT claims.",
        "Keep the study open, retain the absence, and require a frozen authorized data snapshot, checksums, timing/noise model, covariance, preregistered likelihood, and independent review.",
        ["real_data", "likelihood", "parameter_constraint", "force_claim", "empirical_confirmation"],
        "open_gap",
        "Earlier adapters cover BAO, lensing, Solar-System, binaries, MICROSCOPE, and ground-based gravitational waves; none targets a PTA timing release with a mandatory zero-row likelihood refusal.",
    ),
    proposal(
        4,
        "THOS drinking-water laboratory chain-of-custody, duplicate-sample, and correction-replay proxy",
        "sample identity, collection and receipt times, preservation, duplicate association, result version, nonconformance notification, correction replay, role separation, blind matched-budget arms, and handover ownership",
        "Synthetic event traces can expose broken sample lineage, conflicting duplicate results, stale corrections, and incomplete shift handovers while preserving matched-budget participant gates.",
        "A synthetic trace becomes a real sample or safety decision, a correction is lost, blinded arms are claimed without participants, or professional competence and operational effectiveness are inferred.",
        ["V6463-S08", "V6463-S09"],
        ["thos/water-lab-handover-contract.json", "thos/water-lab-proxy-vectors.json"],
        "Unsafe synthetic traces must fail; the packet must record zero real samples, laboratories, workers, suppliers, blind arms, safety events, and effectiveness estimates.",
        "Withdraw effectiveness language, retain rejected traces, and defer real workflow design to authorized laboratories, suppliers, workers, safety monitors, regulators, and independent reviewers.",
        ["real_participants", "real_samples", "public_health", "professional_authority", "deployment"],
        "represented",
        "Prior THOS work covers transport, observatory, clinical, electrical, archive, and geodetic handovers; none models drinking-water laboratory chain of custody, duplicates, and result correction replay.",
    ),
    proposal(
        5,
        "Freed ID VC 2.0 related-resource digest, media-type, and availability-failure profile",
        "relatedResource identity, digestSRI or digestMultibase, media type, retrieval refusal, cache provenance, correlation minimization, unavailable-resource handling, and trust boundaries",
        "Synthetic vectors can distinguish VC 2.0 related-resource integrity obligations from production identity assurance or truth of credential claims.",
        "A missing digest passes, a media-type mismatch is ignored, remote availability becomes mandatory disclosure, a resource URL leaks holder data, or synthetic hashes become production proofs.",
        ["V6463-S10", "V6463-S11"],
        ["freed-id/related-resource-contract.json", "freed-id/related-resource-vectors.json"],
        "Vectors must reject absent digests, mismatched media types, unsupported algorithms, correlation leakage, and unavailable vital resources while recording zero real keys or proofs.",
        "Downgrade to structural representation, retain the failed vector, and require real conforming keys, proofs, resolution, status, interoperability, privacy/security review, recovery, and trust governance.",
        ["real_keys", "live_resolution", "interoperability", "production", "privacy_complete", "security_certification"],
        "represented",
        "Prior Freed ID work covers contexts, status, HAIP, SD-JWT, federation, DCQL, and attestation; none centers VC 2.0 related-resource digest and media-type failure semantics.",
    ),
    proposal(
        6,
        "CBR boil-water-notice reach, household privacy, accessibility, remedy, and Māori-authority matrix",
        "notice reach, channel exclusions, language and disability access, household and location privacy, correction, hardship, remedy, supplier and regulator roles, affected-party participation, and Māori authority",
        "A structural matrix can expose missing authority and affected-party gates without issuing or interpreting a real drinking-water notice.",
        "The matrix gives public-health advice, adjudicates harm or remedy, exposes household data, claims accessibility, or speaks for affected communities or Māori authorities.",
        ["V6463-S12", "V6463-S13"],
        ["cbr/boil-water-authority-matrix.json", "cbr/boil-water-exact-gate.json"],
        "Every real decision path must remain exact-gated to affected people, suppliers, regulators, public-health and accessibility expertise, competent legal authorities, and Māori authority.",
        "Retain the unresolved class, remove decision language, and defer to authorized public-health, supplier, regulatory, legal, privacy, accessibility, affected-community, and Māori processes.",
        ["public_health", "legal_advice", "affected_party", "household_privacy", "accessibility_complete", "remedy", "maori_authority"],
        "exact_gate",
        "Earlier CBR work covers drinking-water affordability and other infrastructure remedies; none centers boil-water notice reach, household privacy, accessibility, correction, and Māori authority.",
        approval="exact_authority_required",
    ),
    proposal(
        7,
        "SQLite schema-migration lock, user-version, rollback, and path-confinement tribunal",
        "application identity, user_version, expected schema, immediate write lock, ordered migrations, rollback, newer-version refusal, crash reopen, and foreign-path confinement",
        "A disposable fixture can reject partial schema upgrades, concurrent migration assumptions, version rollback, and path escape without touching canonical state.",
        "A failed migration advances user_version, two writers receive credit, a newer schema is downgraded, rollback leaves partial objects, or a database path escapes the fixture.",
        ["V6463-S14", "V6463-S15"],
        ["tooling/sqlite-migration-tribunal.json", "tooling/sqlite-migration-mutations.json"],
        "Every partial, locked, wrong-version, downgrade, crash, and confinement mutation must fail or recover as preregistered inside one disposable owner-local fixture.",
        "Retain the fixture receipt, close handles, roll back the transaction, and retry teardown only inside the verified disposable root; never touch repository or sibling databases.",
        ["foreign_path", "canonical_state", "sibling_state", "destructive_cleanup", "production_database"],
        "completed",
        "Earlier SQLite work covers WAL snapshots and busy-state recovery; none centers ordered schema migration, user_version atomicity, newer-version refusal, and migration-lock ownership.",
    ),
    proposal(
        8,
        "Accessible chart data-download, sonification-alternative, and modality-parity audit",
        "downloadable table identity, units, series order, missing values, keyboard path, sonification transcript, pause control, equivalent summary, and manual reservation",
        "A structural auditor can reject missing or divergent downloadable and auditory alternatives without claiming complete accessibility or prescribing one sensory mode.",
        "A visual series diverges from the table, sonification lacks a transcript or control, keyboard behavior is inferred, or automated structure becomes affected-user conformance evidence.",
        ["V6463-S16", "V6463-S17"],
        ["accessibility/chart-alternative-contract.json", "accessibility/chart-alternative-mutations.json"],
        "Mutations for missing units, mismatched series, absent transcript, missing pause control, and inaccessible download labeling must fail; manual and affected-user evaluation remains reserved.",
        "Mark the report structurally incomplete, retain failures, synchronize text and downloadable alternatives, and schedule qualified manual, assistive-technology, and affected-user evaluation.",
        ["accessibility_complete", "assistive_technology", "browser_behavior", "affected_user_evaluation", "maori_language_review"],
        "completed",
        "Earlier accessibility work covers SVG naming and tabular fallbacks; none tests data-download and sonification alternatives as synchronized, independently optional modalities.",
    ),
    proposal(
        9,
        "Thermo/Psyche Harada-Sasa response-violation and dissipation-domain classifier",
        "nonequilibrium Langevin assumptions, velocity correlation, linear response, bath temperature, frequency integration, dissipation rate, and typed-domain refusal",
        "A typed classifier can represent Harada-Sasa obligations in their physical domain while rejecting conversion into psyche, effort, autonomy, justice, consciousness, or universal law.",
        "The Langevin and steady-state assumptions are omitted, response and correlation units differ, the integral is generalized without conditions, or a physical equality becomes a human claim.",
        ["V6463-S18"],
        ["thermo-psyche/harada-sasa-contract.json", "thermo-psyche/harada-sasa-rejections.json"],
        "All missing-assumption, unit, and cross-domain mutations must be rejected with no psyche, participant, consciousness, justice, or fundamental-law result.",
        "Restore physical-domain labels, retain the rejection, and require domain-specific theory and empirical evidence before any cross-domain hypothesis.",
        ["psyche_claim", "consciousness", "human_inference", "fundamental_law", "empirical_confirmation"],
        "completed",
        "Earlier classifiers cover Hatano-Sasa, Crooks, Jarzynski, Onsager, Landauer, and uncertainty relations; none centers fluctuation-response violation and dissipation-rate equality.",
    ),
    proposal(
        10,
        "Stage 20 Registered-Report deviation-checksum, outcome-blind file, and nonpromotion board",
        "Stage 1 protocol checksum, outcome-file access state, in-principle acceptance, deviation lineage, exploratory labels, quality checks, and terminal abstention",
        "A structural board can detect post-acceptance protocol drift and outcome access while preserving deviations and negative results without authorizing Stage 20.",
        "A checksum mismatch passes, outcome access precedes Stage 1 lock, a deviation is hidden, exploratory work becomes confirmatory, or local structure is called peer review.",
        ["V6463-S19"],
        ["stage20/deviation-checksum-contract.json", "stage20/deviation-checksum-mutations.json"],
        "All checksum drift, outcome leakage, hidden-deviation, and label-substitution mutations must fail while terminal truth remains NOT_READY_FOR_STAGE_20.",
        "Withdraw promotion credit, retain protocol and deviation history, seek genuine outcome-blind review where authorized, and keep Stage 20 closed.",
        ["stage20", "peer_review_claim", "statistical_promotion", "proof_or_canon", "empirical_confirmation"],
        "completed",
        "Earlier Registered-Report work covers workflow and outcome blindness; none binds protocol bytes, outcome-file access, and deviation lineage through a checksum nonpromotion board.",
    ),
]


SOURCES = [
    {"source_id":"V6463-S01","status":"current","title":"GHC Family Method Flow State schema and runner","authority":"family-current local skill","url":None,"checked_on":"2026-07-16","use":"append-only failures, witnesses, recovery, and recurrence guards"},
    {"source_id":"V6463-S02","status":"current","title":"GHC Family Index routing and closeout guidance","authority":"family-current local skill","url":None,"checked_on":"2026-07-16","use":"ownership, source precedence, route state, and closeout boundaries"},
    {"source_id":"V6463-S03","status":"stable","title":"RFC 6901 JSON Pointer","authority":"RFC Editor and IETF","url":"https://www.rfc-editor.org/rfc/rfc6901.html","checked_on":"2026-07-16","use":"pointer syntax, escaping, evaluation, and error semantics"},
    {"source_id":"V6463-S04","status":"stable","title":"RFC 8785 JSON Canonicalization Scheme","authority":"RFC Editor","url":"https://www.rfc-editor.org/rfc/rfc8785.html","checked_on":"2026-07-16","use":"canonical JSON bytes, deterministic sorting, and verified errata awareness"},
    {"source_id":"V6463-S05","status":"stable","title":"Properties of propagators and renormalization constants of quantized fields","authority":"Lehmann primary research","url":"https://doi.org/10.1007/BF02783624","checked_on":"2026-07-16","use":"spectral-representation assumptions and pole or residue obligations only"},
    {"source_id":"V6463-S06","status":"current","title":"NANOGrav public data releases","authority":"NANOGrav Collaboration","url":"https://nanograv.org/science/data","checked_on":"2026-07-16","use":"official public-release inventory; zero rows downloaded or ingested"},
    {"source_id":"V6463-S07","status":"stable","title":"NANOGrav 15-year observations and timing of 68 millisecond pulsars","authority":"NANOGrav Collaboration primary research","url":"https://doi.org/10.3847/2041-8213/acda9a","checked_on":"2026-07-16","use":"published product and field context only; no refit or likelihood"},
    {"source_id":"V6463-S08","status":"current","title":"For laboratories","authority":"Water Services Authority - Taumata Arowai","url":"https://www.taumataarowai.govt.nz/drinking-water-suppliers-and-operators/for-laboratories","checked_on":"2026-07-16","use":"official laboratory role and notification context; zero real samples"},
    {"source_id":"V6463-S09","status":"current","title":"Drinking Water Quality Assurance Rules reporting guidance","authority":"Water Services Authority - Taumata Arowai","url":"https://www.taumataarowai.govt.nz/assets/Portal/Drinking-Water-Quality-Assurance-Rules-Reporting-Guidance.pdf","checked_on":"2026-07-16","use":"sample identifier and reporting lineage context only"},
    {"source_id":"V6463-S10","status":"stable","title":"Verifiable Credentials Data Model v2.0","authority":"World Wide Web Consortium","url":"https://www.w3.org/TR/vc-data-model-2.0/","checked_on":"2026-07-16","use":"Recommendation requirements for related resources, privacy, security, and validation"},
    {"source_id":"V6463-S11","status":"current","title":"IANA Media Types registry","authority":"Internet Assigned Numbers Authority","url":"https://www.iana.org/assignments/media-types/media-types.xhtml","checked_on":"2026-07-16","use":"current media-type registry context; no production interoperability claim"},
    {"source_id":"V6463-S12","status":"current","title":"Types of drinking water notices","authority":"Water Services Authority - Taumata Arowai","url":"https://www.taumataarowai.govt.nz/for-the-public/drinking-water-in-an-emergency/drinking-water-notices","checked_on":"2026-07-16","use":"official notice categories and public-facing context; no advice generated"},
    {"source_id":"V6463-S13","status":"stable","title":"Principles of Māori Data Sovereignty","authority":"Te Mana Raraunga Māori Data Sovereignty Network","url":"https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty","checked_on":"2026-07-16","use":"Māori authority and data-governance reservation; never delegated authority"},
    {"source_id":"V6463-S14","status":"current","title":"SQLite transaction documentation","authority":"SQLite project","url":"https://www.sqlite.org/lang_transaction.html","checked_on":"2026-07-16","use":"transaction and single-writer semantics for a disposable fixture"},
    {"source_id":"V6463-S15","status":"current","title":"SQLite PRAGMA documentation","authority":"SQLite project","url":"https://www.sqlite.org/pragma.html","checked_on":"2026-07-16","use":"user_version and locking-mode semantics for synthetic migration tests"},
    {"source_id":"V6463-S16","status":"current","title":"WAI Complex Images Tutorial","authority":"World Wide Web Consortium Web Accessibility Initiative","url":"https://www.w3.org/WAI/tutorials/images/complex/","checked_on":"2026-07-16","use":"current chart description and text-alternative guidance"},
    {"source_id":"V6463-S17","status":"stable","title":"Web Content Accessibility Guidelines 2.2","authority":"World Wide Web Consortium","url":"https://www.w3.org/TR/WCAG22/","checked_on":"2026-07-16","use":"normative text-alternative and structural requirements; complete conformance reserved"},
    {"source_id":"V6463-S18","status":"stable","title":"Equality connecting energy dissipation with violation of fluctuation-response relation","authority":"Harada and Sasa primary research","url":"https://doi.org/10.1103/PhysRevLett.95.130602","checked_on":"2026-07-16","use":"physical-domain assumptions and equality only"},
    {"source_id":"V6463-S19","status":"current","title":"Registered Reports","authority":"Center for Open Science","url":"https://www.cos.io/initiatives/registered-reports","checked_on":"2026-07-16","use":"outcome-blind Stage 1, in-principle acceptance, and deviation context only"},
]


SAFE_REVIEWED_TITLES = [
    "Source-status drift and watch-state audit",
    "Four-hundred-ten-proposal semantic-neighbor quarantine",
    "Exact staged-file allowlist and lifecycle review",
    "Deterministic JSON and UTF-8 verification",
    "Scanner implementation self-hit versus confirmed content-hit separation",
    "Exact manifest fixed-point guard",
    "Family-current compatibility caller audit",
    "SVG and table-alternative mutation review",
    "Method Flow terminal-state preflight",
    "Bounded subprocess timeout receipt",
    "Null-safe four-way equality wrapper",
    "Stale lifecycle-label audit",
    "External-negative reconciliation",
    "PREPARED_NOT_SENT terminal-route guard",
    "Workload, rotation, and wellbeing receipt",
]

SAFE_NEW_TITLES = [
    "Cross-manifest foreign-edge and self-reference preflight",
    "Canonical-byte and negative-zero manifest check",
    "Official-source checked-date and redirect receipt",
    "Owner-generated file-footprint threshold check",
    "Inherited open-gap and exact-gate nonclosure audit",
    "Zero-row PTA likelihood refusal invariant",
    "Zero-sample and zero-participant THOS boundary invariant",
    "Zero production-key-and-proof Freed ID boundary invariant",
    "Boil-water authority-vocabulary nonexecution lint",
    "Disposable SQLite path-confinement preflight",
    "Chart modality-parity structural check",
    "Thermo/Psyche classification-vocabulary lint",
    "Immutable x1-tree no-outcome audit",
    "Named replay branch no-upstream locality preflight",
    "Commit-cap, single-parent, and zero-merge contract",
]

CANDIDATE_REVIEWED_TITLES = [
    "Cross-manifest foreign-edge evidence-DAG quarantine",
    "GMUT spectral sign and pole-residue mutation board",
    "NANOGrav official-data zero-row adapter",
    "Water-laboratory correction-replay proxy",
    "VC related-resource correlation and algorithm-agility model",
    "Boil-water notice reach and authority matrix",
    "SQLite migration-lock and schema-version tribunal",
    "Accessible chart data-download and sonification prototype",
    "Registered-Report deviation-checksum board",
    "Bounded shell-startup envelope estimator",
]

CANDIDATE_NEW_TITLES = [
    "Canonical JSON negative-zero rejection fixture",
    "Källén-Lehmann gauge-field observability classifier",
    "PTA noise-model and ephemeris refusal contract",
    "Duplicate-sample conflict ownership state machine",
    "Vital-related-resource availability failure simulator",
    "Household-location privacy minimization matrix",
    "SQLite newer-schema downgrade refusal fixture",
    "Chart modality transcript and pause-control auditor",
    "Harada-Sasa unit and domain guard",
    "Outcome-file access and protocol-byte lock board",
]

SKILLS = [
    ("ghc-family-external-negative-reconciler", "Reconcile sealed and externally retained negatives without rewriting predecessor counts."),
    ("ghc-family-phase-local-test-quarantine", "Quarantine predecessor tests whose assertions are intentionally phase-local."),
    ("ghc-family-exact-revision-credit", "Bind validation credit to the exact revision actually invoked."),
    ("ghc-family-windows-refspec-guard", "Brace variables and validate Windows PowerShell refspec construction."),
    ("ghc-family-shell-summary-sequencer", "Evaluate native commands before constructing PowerShell summary objects."),
    ("ghc-family-manifest-fixed-point", "Require stable self-excluding manifest replay before credit."),
    ("ghc-family-svg-alternative-audit", "Audit chart names, tables, downloads, and optional auditory alternatives structurally."),
    ("ghc-family-authority-matrix-lint", "Keep public-health, legal, affected-party, accessibility, and Māori authority exact-gated."),
    ("ghc-family-zero-row-likelihood-refusal", "Enforce zero-row empirical adapters with zero likelihood or constraint output."),
    ("ghc-family-named-lane-locality-proof", "Verify one validation lane remains local-only, named, clean, and noncanonical."),
    ("ghc-family-cross-manifest-edge-quarantine", "Reject foreign, cyclic, dangling, self-referential, and unstable manifest edges."),
    ("ghc-family-kallen-lehmann-obligations", "Classify spectral support, pole, residue, positivity, and field-observability obligations."),
    ("ghc-family-pta-zero-row-adapter", "Describe a NANOGrav PTA product contract while refusing data and likelihood credit."),
    ("ghc-family-water-lab-handover-proxy", "Validate synthetic sample-lineage, duplicate, correction, and handover traces."),
    ("ghc-family-vc-related-resource-integrity", "Validate VC related-resource digests and media-type failure semantics structurally."),
    ("ghc-family-boil-water-authority-reservation", "Reserve boil-water notice, remedy, privacy, accessibility, and Māori authority."),
    ("ghc-family-sqlite-migration-lock", "Run a confined schema-version, lock, rollback, and downgrade-refusal fixture."),
    ("ghc-family-chart-modality-parity", "Audit downloadable, textual, visual, and optional auditory alternatives for structural parity."),
    ("ghc-family-harada-sasa-domain", "Reject cross-domain conversion of Harada-Sasa physical relations."),
    ("ghc-family-registered-report-checksum", "Validate protocol bytes, outcome access, deviations, and nonpromotion structurally."),
]

RUNNERS = [
    ("ghc_family_external_negative_reconciler.py", "Reconcile sealed, external, and current negative counts."),
    ("ghc_family_phase_local_test_quarantine.py", "Select eligible scoped tests with explicit phase-local exclusions."),
    ("ghc_family_exact_revision_credit.py", "Bind receipts to an exact Git revision."),
    ("ghc_family_manifest_fixed_point.py", "Check self-excluding staged-manifest fixed points."),
    ("ghc_family_named_lane_locality_proof.py", "Verify local-only named validation-lane boundaries."),
    ("ghc_family_v646_v3_core_runner.py", "Execute the ten bounded core surfaces."),
    ("ghc_family_v646_v3_portfolio_runner.py", "Execute safe-now and candidate portfolios."),
    ("ghc_family_v646_v3_skill_runner.py", "Build, validate, and smoke-use the phase skill pack."),
    ("ghc_family_v646_v3_staged_review.py", "Review exact staged paths, JSON, privacy patterns, and manifests."),
    ("ghc_family_v646_v3_validation_runner.py", "Run scoped, detailed, minimal, privacy, manifest, and lifecycle checks."),
]

CLEAN_REVIEWED_TITLES = [
    "Reconcile sealed and external negative counts",
    "Refresh every count-dependent assertion",
    "Preserve additive stale-label corrections",
    "Audit compatibility callers before consolidation",
    "Exclude all sibling and user paths from cleanup",
    "Require deterministic JSON order",
    "Preserve UTF-8 Māori text",
    "Review responsive report overflow structurally",
    "Keep lifecycle manifest inclusion consistent",
    "Brace PowerShell variables adjacent to colons",
    "Use null-safe expected-empty remote checks",
    "Keep validation branches local-only",
    "Verify commit cap and single-parent history",
    "Confirm exact and blocked packets gained no execution credit",
    "Refresh Family Index and Method Flow recommendations",
]

CLEAN_NEW_TITLES = [
    "Synchronize 410-to-420 proposal counts across validators",
    "Separate inherited external negatives from Sable operational failures",
    "Normalize canonical JSON without changing array order",
    "Retain verified RFC 8785 negative-zero erratum awareness",
    "Check every source checked-on date and status",
    "Keep NANOGrav release metadata separate from observations",
    "Keep laboratory fixtures free of real sample identifiers",
    "Check chart downloads expose units and missing-value labels",
    "Reserve manual keyboard and assistive-technology evaluation",
    "Keep vital-resource failure distinct from trust decisions",
    "Verify SQLite teardown remains inside the disposable root",
    "Check all Thermo/Psyche labels use declared classification classes",
    "Verify final manifests exclude only their own self-reference",
    "Preserve post-final faults externally after the commit cap seals",
    "Refresh terminal route state without claiming an unacknowledged send",
]


def support_item(prefix: str, index: int, title: str, origin: str, approval_class: str) -> dict[str, Any]:
    return {
        "packet_id": f"V6463-{prefix}-{index:02d}",
        "title": title,
        "owner": OWNER,
        "origin": origin,
        "approval_class": approval_class,
        "hypothesis": f"A bounded owner-scoped implementation of {title.lower()} can produce auditable structural evidence without crossing protected gates.",
        "null_or_failure": "The artifact is absent, privacy is crossed, a structural result is overstated, a failure is erased, or a protected gate is silently closed.",
        "acceptance_gate": "The x2 artifact, bounded witness, and privacy-safe receipt must all pass before completion credit.",
        "rollback_or_recovery": "Retain the negative, restore the last validated owner-scoped state, and leave unavailable evidence or authority explicitly open.",
        "protected_gates": ["authority", "real_data_or_participants", "production", "sibling_lane", "independent_reproduction", "stage20"],
        "x1_state": "preregistered_no_completion_credit",
    }


SAFE_NOW = [
    *[support_item("REVIEW-SAFE", i, title, "ilyra_baton_seed_rewritten_after_review", "safe_now_owner_scoped_structural") for i, title in enumerate(SAFE_REVIEWED_TITLES, 1)],
    *[support_item("NEW-SAFE", i, title, "sable_new_x1", "safe_now_owner_scoped_structural") for i, title in enumerate(SAFE_NEW_TITLES, 1)],
]
CANDIDATES = [
    *[support_item("REVIEW-CAND", i, title, "ilyra_baton_seed_rewritten_after_review", "candidate_bounded_prototype") for i, title in enumerate(CANDIDATE_REVIEWED_TITLES, 1)],
    *[support_item("NEW-CAND", i, title, "sable_new_x1", "candidate_bounded_prototype") for i, title in enumerate(CANDIDATE_NEW_TITLES, 1)],
]
CLEAN_TASKS = [
    *[support_item("REVIEW-CLEAN", i, title, "ilyra_baton_seed_rewritten_after_review", "safe_now_owner_scoped_additive_cleanup") for i, title in enumerate(CLEAN_REVIEWED_TITLES, 1)],
    *[support_item("NEW-CLEAN", i, title, "sable_new_x1", "safe_now_owner_scoped_additive_cleanup") for i, title in enumerate(CLEAN_NEW_TITLES, 1)],
]
