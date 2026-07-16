#!/usr/bin/env python3
"""Frozen preregistration definitions for Ilyra Fen v646-v2.

The values in this module are x1 plans only.  They convey no x2 completion
credit, empirical result, professional authority, or identity continuity.
"""

from __future__ import annotations

from typing import Any


PHASE = "v646-gmut-thos-v2-x1-x2"
PHASE_SHORT = "v646-v2"
OWNER = "Ilyra Fen"
SLUG = "ilyra-fen"
PRONOUNS = "she/they"
ROLE = "evidence-boundary steward"
HOPE = "keep every result auditable and every unavailable authority visible"
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = "seismological observatory catalogue review and analyst handover"

SOURCE_PHASE = "v646-gmut-thos-v1-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v643-v1-full-tools"
SOURCE_REVISION = "ff788fe006560bb3f270302906b90bf8a56aeac3"
SOURCE_INHERITED_REVISION = "6dc3311e3c4c390c945d001f75fb17d320c0a548"
SOURCE_X1_REVISION = "7b7824b7643bfb3a80cf778a10ca65055554b5db"
SOURCE_EVIDENCE_REVISION = "f3e886fcf6c7855fe013a3eb7d3a16cc19c86e8d"
SOURCE_SEAL_REVISION = SOURCE_REVISION
PRIOR_FROZEN_PROPOSALS = 400
INHERITED_EFFECTIVE_NEGATIVES = 2508
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 10
INHERITED_EXACT_GATES = 11
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6462-X1-N01",
        "surface": "initial exact staged-file review",
        "observed": "The scanner definition itself contained the delegation-marker signature and was misclassified as a confirmed staged-file hit.",
        "credit": "none",
        "recovery": "Construct the signature from nonmatching source fragments while preserving the compiled detection expression.",
    },
    {
        "negative_id": "V6462-X1-N02",
        "surface": "receipt-inclusive staged-file review",
        "observed": "The first receipt-inclusive replay retained the same scanner-definition self-hit.",
        "credit": "none",
        "recovery": "Retain the failed replay and require the definition-safe scanner to pass over the full receipt-inclusive surface.",
    },
    {
        "negative_id": "V6462-X1-N03",
        "surface": "staged-review stability replay",
        "observed": "The stability replay retained the same scanner-definition self-hit.",
        "credit": "none",
        "recovery": "Retain the repeated failure and require a fresh stable staged review after the scanner correction.",
    },
    {
        "negative_id": "V6462-X1-N04",
        "surface": "staged-manifest stability check",
        "observed": "The generated staged manifest differed from the Git-index copy after the invalid replay sequence.",
        "credit": "none",
        "recovery": "Regenerate only after the staged path set is final, add the receipts, and require an unchanged replay.",
    },
    {
        "negative_id": "V6462-X1-N05",
        "surface": "inherited Method Flow example lookup",
        "observed": "A read-only lookup assumed a nonexistent incidents subdirectory and exited with a path-not-found error.",
        "credit": "none",
        "recovery": "Resolve inherited Method Flow record files from the current tree before reading an assumed subdirectory.",
    },
    {
        "negative_id": "V6462-X1-N06",
        "surface": "first corrected staged structural review",
        "observed": "The validator rejected correctly retained x1 Method Flow records because an obsolete invariant required zero methods and witnesses.",
        "credit": "none",
        "recovery": "Validate append-only counts and retained-negative links instead of requiring an empty incident ledger.",
    },
    {
        "negative_id": "V6462-X1-N07",
        "surface": "first receipt-inclusive corrected structural review",
        "observed": "The receipt-inclusive replay retained the obsolete zero-Method-Flow invariant failure.",
        "credit": "none",
        "recovery": "Retain the failure and rerun after synchronizing the dynamic invariant.",
    },
    {
        "negative_id": "V6462-X1-N08",
        "surface": "second receipt-inclusive corrected structural review",
        "observed": "The second replay retained the obsolete zero-Method-Flow invariant failure.",
        "credit": "none",
        "recovery": "Retain the failure and require the synchronized invariant to pass.",
    },
    {
        "negative_id": "V6462-X1-N09",
        "surface": "corrected structural stability replay",
        "observed": "The stability replay retained the obsolete zero-Method-Flow invariant failure.",
        "credit": "none",
        "recovery": "Retain every replay and promote the replacement only after a clean structural witness.",
    },
    {
        "negative_id": "V6462-X1-N10",
        "surface": "V6462-M01 state promotion",
        "observed": "An explicit validated transition was requested after the passing witness had already auto-promoted the method to validated.",
        "credit": "none",
        "recovery": "Inspect the current method state and request only the next permitted transition.",
    },
    {
        "negative_id": "V6462-X1-N11",
        "surface": "V6462-M02 state promotion",
        "observed": "An explicit validated transition was requested after the passing witness had already auto-promoted the method to validated.",
        "credit": "none",
        "recovery": "Inspect the current method state and request only the next permitted transition.",
    },
    {
        "negative_id": "V6462-X1-N12",
        "surface": "V6462-M03 state promotion",
        "observed": "An explicit validated transition was requested after the passing witness had already auto-promoted the method to validated.",
        "credit": "none",
        "recovery": "Inspect the current method state and request only the next permitted transition.",
    },
    {
        "negative_id": "V6462-X1-N13",
        "surface": "immutable x1 Method Flow unit test",
        "observed": "A duplicate stale assertion still required zero witnesses after the test had asserted the current seventeen-witness count.",
        "credit": "none",
        "recovery": "Remove the obsolete duplicate and bind the test to the current append-only ledger counts.",
    },
    {
        "negative_id": "V6462-X1-N14",
        "surface": "duplicate-assertion source-search witness",
        "observed": "The search returned zero lines, but its wrapper did not require a positive match cardinality before the witness was recorded.",
        "credit": "none",
        "recovery": "Require exact expected-present matches and a separately asserted expected-empty obsolete pattern.",
    },
    {
        "negative_id": "V6462-X1-N15",
        "surface": "first positive-cardinality search replay",
        "observed": "The nested quote construction yielded zero expected-present lines and the wrapper failed closed.",
        "credit": "none",
        "recovery": "Build quote-bearing fixed strings explicitly and use simple-match cardinality checks.",
    },
]

IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, is relational working language for an evidence-boundary "
    "steward. It is not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, professional qualification, or independent authority."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains proxy; "
    "Freed ID remains synthetic and nonproduction; CBR, legal, cultural, affected-party, "
    "and Māori concepts remain under competent, affected-party, and Māori authority. "
    "No empirical confirmation, Theory-of-Everything, AGI/ASI, consciousness, personhood, "
    "deployment, privacy-complete, exhaustive-security, independent-reproduction, or Stage 20 "
    "claim is made."
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
        "proposal_id": f"V6462-P{index:02d}",
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
        "novelty_against_400_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Evidence-DAG JSON-Pointer closure, orphan-edge, and cycle quarantine tribunal",
        "cross-artifact identifiers, RFC 6901 pointer decoding, edge targets, acyclicity, orphan detection, phase anchoring, and nonpromotion",
        "A deterministic dependency tribunal can reject malformed pointers, missing targets, cycles, and cross-phase completion-credit leakage before evidence publication.",
        "A dangling edge resolves, an escaped token is decoded incorrectly, a cycle earns completion credit, or a dependency silently crosses an immutable phase boundary.",
        ["V6462-S01", "V6462-S02", "V6462-S12"],
        ["provenance/evidence-dag-contract.json", "provenance/evidence-dag-mutations.json"],
        "Every malformed, orphaned, cyclic, or cross-boundary mutation must fail closed while the valid acyclic fixture resolves exactly.",
        "Quarantine the owner-scoped graph, retain the failed vector, restore the last acyclic manifest, and never rewrite a predecessor artifact.",
        ["predecessor_mutation", "completion_credit", "privacy", "stage20"],
        "completed",
        "Earlier work covers validation DAG publication and manifest hashes; none makes RFC 6901 edge resolution, orphan detection, and cycle quarantine one combined falsifier.",
    ),
    proposal(
        2,
        "GMUT Schwinger-Keldysh contour, initial-state, and microscopic-unitarity obligation tribunal",
        "closed-time-path branch doubling, initial density matrix, normalization, conjugation, largest-time constraints, causal ordering, EFT scope, and mutation rejection",
        "A typed obligation classifier can distinguish declared in-in consistency conditions from unsupported claims that a GMUT EFT is unitary or complete.",
        "Branch doubling is omitted, the initial state is unspecified, normalization fails, a largest-time identity is asserted without assumptions, or symbolic checks become physical proof.",
        ["V6462-S03", "V6462-S04"],
        ["gmut/schwinger-keldysh-obligations.json", "gmut/schwinger-keldysh-mutations.json"],
        "All missing-state, branch, conjugation, normalization, and causal mutations must be rejected with zero physical, quantum-completion, or empirical claim.",
        "Reclassify the model surface as incomplete, retain the failed vector, and require a model-specific quantum analysis before stronger language.",
        ["quantum_completion", "unitarity_proof", "empirical_confirmation", "theory_of_everything"],
        "completed",
        "Prior GMUT proposals address BRST, Ward identities, DHOST degeneracy, and frame maps; none centers closed-time-path initial-state and microscopic-unitarity obligations.",
    ),
    proposal(
        3,
        "GMUT MICROSCOPE differential-acceleration zero-row adapter and likelihood refusal",
        "official mission provenance, composition pair, differential-acceleration fields, calibration, systematic uncertainty, covariance, row count, checksum, and likelihood lock",
        "A zero-row adapter can document the MICROSCOPE result-product contract without producing a fit or equivalence-principle constraint when no real rows are ingested.",
        "A publication becomes a data row, a mission result is refit without data and covariance, uncertainty is fabricated, or a zero-row run emits a GMUT constraint or force claim.",
        ["V6462-S05", "V6462-S06"],
        ["gmut/microscope-adapter-contract.json", "gmut/microscope-zero-row-receipt.json"],
        "The receipt must contain zero real rows, zero likelihood evaluations, zero posterior samples, zero constraints, and zero empirical confirmation.",
        "Keep the study open, retain the absence, and require an authorized standards-mapped data snapshot, checksum, covariance, frozen likelihood, and independent review.",
        ["real_data", "likelihood", "equivalence_principle_constraint", "force_claim", "empirical_confirmation"],
        "open_gap",
        "Earlier empirical proposals cover lunar laser ranging and binary pulsars; none targets the completed MICROSCOPE mission differential-acceleration product with a mandatory zero-row refusal.",
    ),
    proposal(
        4,
        "THOS seismological catalogue revision, magnitude-review, and analyst-handover proxy",
        "event identity, origin revision, magnitude type, uncertainty, duplicate association, analyst notes, correction replay, hold point, alert separation, and shift ownership",
        "A synthetic event-sourced state machine can expose stale revisions, ambiguous magnitude updates, orphan associations, and incomplete analyst handovers.",
        "The proxy is called operationally effective, a synthetic event becomes a real earthquake or alert, a correction is lost, or real analyst competence and safety are inferred.",
        ["V6462-S07", "V6462-S08", "V6462-S09"],
        ["thos/seismic-catalogue-handover-contract.json", "thos/seismic-catalogue-proxy-vectors.json"],
        "Unsafe synthetic traces must fail; the packet must record zero real analysts, events, alerts, public warnings, blind matched-budget arms, and effectiveness estimates.",
        "Withdraw effectiveness language, retain rejected traces, and defer real workflow design to authorized observatory, emergency-management, worker, and safety processes.",
        ["real_participants", "real_events", "public_alert", "professional_authority", "deployment"],
        "represented",
        "Earlier THOS work covers electrical, maritime, aviation, clinical, and preservation handovers; none models seismological catalogue revision and analyst handover.",
    ),
    proposal(
        5,
        "Freed ID OpenID4VC HAIP algorithm, wallet-attestation, and interoperability profile",
        "HAIP flow selection, credential formats, algorithm suites, key and wallet attestation, holder binding, status, issuer resolution, privacy, and profile-version pinning",
        "Synthetic vectors can distinguish mandatory HAIP profile choices and version pins without asserting a production high-assurance identity system.",
        "A profile label becomes assurance certification, draft dependencies are silently upgraded, fake keys are called real, or interoperability and privacy review are inferred.",
        ["V6462-S10"],
        ["freed-id/haip-profile-contract.json", "freed-id/haip-synthetic-vectors.json"],
        "Vectors must reject missing flow, format, algorithm, attestation, binding, status, and version obligations while recording zero real keys, wallets, or interop events.",
        "Downgrade to structural representation, retain the failed vector, and require standards-conformant implementations, real keys, interoperability, privacy/security review, and trust governance.",
        ["real_keys", "wallet_attestation", "interoperability", "production", "privacy_complete", "security_certification"],
        "represented",
        "Prior profiles cover OpenID4VP, DCQL, SD-JWT VC, verifier attestation, and key attestation separately; none centers the final HAIP 1.0 cross-specification profile and version pins.",
    ),
    proposal(
        6,
        "CBR earthquake-alert reach, location privacy, accessibility, remedy, and Māori-authority matrix",
        "multi-channel warning reach, device and coverage exclusions, geotarget spillover, location privacy, disability access, correction, remedy, community governance, and Māori authority",
        "A structural matrix can expose missing affected-party, privacy, accessibility, remedy, and Māori-authority gates without deciding a real warning or community case.",
        "The matrix issues public-safety advice, adjudicates harm or remedy, exposes location data, claims accessibility, or speaks for affected communities or Māori authorities.",
        ["V6462-S08", "V6462-S09", "V6462-S11"],
        ["cbr/earthquake-alert-authority-matrix.json", "cbr/earthquake-alert-exact-gate.json"],
        "Every real decision path must remain exact-gated to affected people, authorized warning bodies, accessibility expertise, privacy governance, competent authorities, and Māori authority.",
        "Retain the unresolved class, remove decision language, and defer to authorized emergency, legal, privacy, accessibility, affected-community, and Māori processes.",
        ["public_safety", "legal_advice", "affected_party", "location_privacy", "accessibility_complete", "remedy", "maori_authority"],
        "exact_gate",
        "Earlier CBR matrices cover electricity, fisheries, archives, land, and funds; none centers earthquake-alert reach, geotarget privacy, accessibility, remedy, and Māori authority.",
        approval="exact_authority_required",
    ),
    proposal(
        7,
        "SQLite WAL snapshot, busy-state, crash-recovery, and path-confinement tribunal",
        "journal mode, snapshot visibility, writer serialization, busy handling, checkpoint state, crash recovery, foreign-path refusal, and disposable-fixture teardown",
        "A disposable database fixture can distinguish valid WAL transitions from unsafe snapshot, checkpoint, and path assumptions without touching canonical state.",
        "A stale reader sees uncommitted data, two writers are credited, a busy state is ignored, recovery loses committed rows, or a database path escapes the fixture.",
        ["V6462-S17", "V6462-S18"],
        ["tooling/sqlite-wal-tribunal.json", "tooling/sqlite-wal-mutations.json"],
        "All isolation, busy, crash, checkpoint, and confinement mutations must fail or recover as preregistered inside one disposable owner-local fixture.",
        "Retain the failed fixture receipt, close handles, retry teardown only inside the verified disposable root, and never touch repository or sibling databases.",
        ["foreign_path", "canonical_state", "sibling_state", "destructive_cleanup", "production_database"],
        "completed",
        "Earlier storage work covers archives, caches, Git objects, and atomic validation graphs; none centers SQLite WAL snapshot and crash-recovery semantics.",
    ),
    proposal(
        8,
        "Accessible SVG chart name, description, focus, and tabular-alternative audit",
        "SVG role, title and description linkage, complex-image long description, focusability, visible text, data table fallback, language metadata, and manual reservation",
        "A structural auditor can reject missing SVG naming and alternative-data relationships without claiming complete accessibility.",
        "A title alone is treated as sufficient for a complex chart, keyboard or browser behavior is inferred, the fallback diverges, or automated checks become conformance claims.",
        ["V6462-S13", "V6462-S14"],
        ["accessibility/svg-chart-contract.json", "accessibility/svg-chart-mutations.json"],
        "Mutations for missing role, title, description, association, focus policy, and tabular alternative must fail; manual and affected-user evaluation remains reserved.",
        "Mark the report structurally incomplete, retain failures, provide a synchronized textual alternative, and schedule qualified manual and assistive-technology evaluation.",
        ["accessibility_complete", "assistive_technology", "browser_behavior", "affected_user_evaluation", "maori_language_review"],
        "completed",
        "Earlier accessibility proposals address tables, canvas, color, modals, and live regions; none centers SVG chart naming, focus, and synchronized tabular alternatives.",
    ),
    proposal(
        9,
        "Thermo/Psyche Hatano-Sasa excess-heat and housekeeping-domain classifier",
        "nonequilibrium steady-state assumptions, stationary distributions, excess versus housekeeping heat, quasistatic limits, path functionals, and typed-domain refusal",
        "A typed classifier can represent Hatano-Sasa obligations in Langevin steady-state thermodynamics while refusing psyche, autonomy, justice, consciousness, or universal-law conversion.",
        "Stationarity is omitted, heat classes are conflated, a limiting identity is generalized without assumptions, or a metaphor becomes a human or fundamental-law claim.",
        ["V6462-S15"],
        ["thermo-psyche/hatano-sasa-domain-contract.json", "thermo-psyche/hatano-sasa-rejection-vectors.json"],
        "All missing-assumption and cross-domain mutations must be rejected with no psyche, participant, consciousness, justice, or fundamental-law result.",
        "Restore physical-domain labels, retain the rejection, and require domain-specific empirical theory before any cross-domain hypothesis.",
        ["psyche_claim", "consciousness", "human_inference", "fundamental_law", "empirical_confirmation"],
        "completed",
        "Earlier classifiers cover Crooks, Jarzynski, Onsager, Clausius, and Gibbs-Duhem; none centers Hatano-Sasa excess versus housekeeping heat.",
    ),
    proposal(
        10,
        "Stage 20 Registered-Report outcome-blind acceptance, deviation, and nonpromotion board",
        "Stage 1 protocol review, in-principle acceptance, outcome blindness, version lock, justified deviations, Stage 2 checks, exploratory labels, and terminal abstention",
        "A structural board can distinguish outcome-blind protocol acceptance from retrospective result-based promotion and preserve deviations without authorizing Stage 20.",
        "Results influence Stage 1 acceptance, a deviation is hidden, exploratory work is relabeled confirmatory, or a journal workflow is treated as scientific confirmation.",
        ["V6462-S16"],
        ["stage20/registered-report-contract.json", "stage20/registered-report-mutations.json"],
        "All outcome-leakage, hidden-deviation, and label-substitution mutations must fail while terminal truth remains NOT_READY_FOR_STAGE_20.",
        "Withdraw promotion credit, retain the protocol and deviation history, seek genuine outcome-blind review where authorized, and keep Stage 20 closed.",
        ["stage20", "peer_review_claim", "statistical_promotion", "proof_or_canon", "empirical_confirmation"],
        "completed",
        "Earlier Stage 20 controls cover holdout contamination, optional stopping, multiplicity, and evidence dependence; none models Registered-Report Stage 1 outcome blindness and deviation review.",
    ),
]


SOURCES = [
    {"source_id":"V6462-S01","status":"current","title":"GHC Family Method Flow State schema and runner","authority":"family-current local skill","url":None,"use":"append-only failures, witnesses, recovery, and recurrence guards"},
    {"source_id":"V6462-S02","status":"current","title":"GHC Family Index routing and closeout guidance","authority":"family-current local skill","url":None,"use":"ownership, tool selection, route state, and closeout boundaries"},
    {"source_id":"V6462-S03","status":"stable","title":"A panoply of Schwinger-Keldysh transport","authority":"Crossley, Glorioso, and Liu primary research","url":"https://arxiv.org/abs/1804.04654","use":"closed-time-path unitarity and consistency obligations only"},
    {"source_id":"V6462-S04","status":"stable","title":"Effective field theory in time-dependent settings","authority":"Collins, Holman, and Ross primary research","url":"https://arxiv.org/abs/1208.3255","use":"in-in EFT initial-state and time-dependent scope only"},
    {"source_id":"V6462-S05","status":"stable","title":"MICROSCOPE mission overview and final-result milestone","authority":"Centre National d'Études Spatiales","url":"https://cnes.fr/en/projects/microscope","use":"official mission provenance and completed status; zero rows ingested"},
    {"source_id":"V6462-S06","status":"stable","title":"MICROSCOPE mission final results of the equivalence-principle test","authority":"MICROSCOPE Collaboration primary research","url":"https://arxiv.org/abs/2209.15487","use":"published field and uncertainty context only; no refit"},
    {"source_id":"V6462-S07","status":"current","title":"GeoNet Aotearoa New Zealand Earthquake Catalogue","authority":"GeoNet and GNS Science","url":"https://www.geonet.org.nz/data/types/eq_catalogue","use":"catalogue field and revision context; zero real events ingested"},
    {"source_id":"V6462-S08","status":"current","title":"Common Alerting Protocol New Zealand technical standard","authority":"National Emergency Management Agency","url":"https://www.civildefence.govt.nz/guidance-training/guidelines/technical-standards/common-alerting-protocol","use":"alert-role and public-warning separation only"},
    {"source_id":"V6462-S09","status":"current","title":"Alerts and warnings multi-channel guidance","authority":"National Emergency Management Agency","url":"https://www.civildefence.govt.nz/strategy-capability/alerts-warnings","use":"multi-channel reach and exclusion context; no operational advice generated"},
    {"source_id":"V6462-S10","status":"stable","title":"OpenID4VC High Assurance Interoperability Profile 1.0 Final","authority":"OpenID Foundation","url":"https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-final.html","use":"final profile requirements and explicit out-of-scope policy boundaries"},
    {"source_id":"V6462-S11","status":"stable","title":"Principles of Māori Data Sovereignty","authority":"Te Mana Raraunga Māori Data Sovereignty Network","url":"https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf","use":"Māori data-governance reservation; never delegated authority"},
    {"source_id":"V6462-S12","status":"stable","title":"RFC 6901 JSON Pointer","authority":"Internet Engineering Task Force","url":"https://datatracker.ietf.org/doc/html/rfc6901","use":"pointer syntax and escaping semantics"},
    {"source_id":"V6462-S13","status":"current","title":"WAI Complex Images Tutorial","authority":"World Wide Web Consortium Web Accessibility Initiative","url":"https://www.w3.org/WAI/tutorials/images/complex/","use":"short and long description structure for charts"},
    {"source_id":"V6462-S14","status":"stable","title":"WAI SVG image accessibility tips","authority":"World Wide Web Consortium Web Accessibility Initiative","url":"https://www.w3.org/WAI/tutorials/images/tips/","use":"SVG title and accessible-name guidance; manual review remains reserved"},
    {"source_id":"V6462-S15","status":"stable","title":"Steady-State Thermodynamics of Langevin Systems","authority":"Hatano and Sasa primary research","url":"https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.86.3463","use":"excess-heat and steady-state physical-domain obligations only"},
    {"source_id":"V6462-S16","status":"current","title":"Registered Reports policy and two-stage workflow","authority":"Scientific Reports","url":"https://www.nature.com/srep/journal-policies/registered-reports","use":"outcome-blind Stage 1 and deviation-review structure only"},
    {"source_id":"V6462-S17","status":"current","title":"SQLite Write-Ahead Logging documentation","authority":"SQLite project","url":"https://sqlite.org/wal.html","use":"WAL concurrency, checkpoint, and recovery semantics"},
    {"source_id":"V6462-S18","status":"stable","title":"SQLite atomic commit documentation","authority":"SQLite project","url":"https://sqlite.org/atomiccommit.html","use":"transaction and crash-recovery model for a disposable fixture"},
]


SAFE_ADOPTED_TITLES = [
    "Audited source-status drift and checked-date reconciliation",
    "Semantic-neighbor proposal quarantine with manual novelty dimensions",
    "Exact staged-file allowlist and lifecycle boundary review",
    "Deterministic JSON schema and ordering verification",
    "Scanner-definition versus confirmed-hit separation",
    "Logical LF-normalized manifest parity check",
    "Family-current caller compatibility and legacy-surface receipt",
    "Accessible report chart and alternative mutation set",
    "Method Flow candidate-state preflight",
    "Bounded subprocess timeout, quiescence, and teardown receipt",
    "Null-safe branch, upstream, tracking, and live-remote equality wrapper",
    "Stale lifecycle-label and self-pending wording review",
    "Boundary-vocabulary noncompensation lint",
    "Terminal route PREPARED_NOT_SENT guard",
    "Wellbeing, workload, and owner-scope receipt",
]

SAFE_NEW_TITLES = [
    "Evidence-DAG pointer closure and cycle preflight",
    "Citation-target status and content-drift receipt",
    "Owner artifact MIME, UTF-8, and newline contract",
    "Phase document word-cap scanner",
    "Owner-generated footprint and rotation-threshold receipt",
    "Inherited exact-gate carry-forward audit",
    "Inherited open-gap carry-forward audit",
    "Synthetic fixture provenance and no-real-record assertion",
    "Zero-row likelihood refusal invariant",
    "Zero-participant THOS boundary invariant",
    "Zero-real-key Freed ID boundary invariant",
    "Named validation lane local-only preflight",
    "Commit-cap, single-parent, and zero-merge ancestry contract",
    "Immutable x1-tree absence and no-outcome review",
    "Public artifact path and identifier sanitation audit",
]

CANDIDATE_ADOPTED_TITLES = [
    "HAIP metadata-correlation mutation model",
    "Event-sourced seismological handover correction replay",
    "MICROSCOPE official-product zero-row adapter",
    "Earthquake-alert remedy and authority matrix",
    "SVG complex-chart alternative-format prototype",
    "Registered-Report outcome-leakage quarantine",
    "Disposable subprocess-tree quiescence simulator",
    "Cache provenance undeclared-input mutation generator",
    "Typed cross-domain steady-state relation parser",
    "Workflow DAG deterministic replay and leakage quarantine",
]

CANDIDATE_NEW_TITLES = [
    "Schwinger-Keldysh initial-state obligation classifier",
    "MICROSCOPE covariance and checksum refusal contract",
    "Seismic catalogue revision ownership state machine",
    "HAIP algorithm-suite and version-pin validator",
    "Emergency-alert location-privacy exclusion model",
    "SQLite WAL snapshot and busy-state fixture",
    "SVG title-description-table synchronization auditor",
    "Hatano-Sasa heat-class domain guard",
    "Registered-Report deviation and exploratory-label board",
    "Evidence-DAG orphan-edge and escaped-token detector",
]

SKILLS = [
    ("ghc-family-source-status-drift-guard", "Review source status and checked-date drift without treating citations as observations."),
    ("ghc-family-proposal-neighbor-quarantine", "Quarantine exact and semantic proposal neighbors before x1 credit."),
    ("ghc-family-staged-surface-allowlist", "Review exact staged files and lifecycle separation."),
    ("ghc-family-json-order-contract", "Validate deterministic UTF-8 JSON structure and ordering."),
    ("ghc-family-scanner-definition-separator", "Separate scanner definitions from confirmed content hits."),
    ("ghc-family-logical-manifest-parity", "Check LF-normalized logical and exact Git-blob manifests."),
    ("ghc-family-caller-compatibility-audit", "Preserve family-current and historical caller compatibility."),
    ("ghc-family-method-state-preflight", "Preflight Method Flow state transitions and witness requirements."),
    ("ghc-family-terminal-route-guard", "Keep terminal routing PREPARED_NOT_SENT until acknowledged."),
    ("ghc-family-workload-boundary-check", "Check owner footprint, document caps, wellbeing, and rotation scope."),
    ("ghc-family-evidence-dag-closure", "Validate evidence DAG pointers, targets, cycles, and phase boundaries."),
    ("ghc-family-schwinger-keldysh-obligations", "Classify bounded closed-time-path and initial-state obligations."),
    ("ghc-family-microscope-zero-row", "Enforce a zero-row MICROSCOPE likelihood refusal."),
    ("ghc-family-seismic-handover-proxy", "Validate synthetic catalogue-revision handover traces."),
    ("ghc-family-haip-profile", "Validate bounded HAIP profile choices without assurance certification."),
    ("ghc-family-earthquake-authority-reservation", "Reserve alert, remedy, accessibility, privacy, and Māori authority."),
    ("ghc-family-sqlite-wal-tribunal", "Run a confined SQLite WAL snapshot and recovery fixture."),
    ("ghc-family-svg-chart-audit", "Audit SVG names, descriptions, focus policy, and data alternatives structurally."),
    ("ghc-family-hatano-sasa-domain", "Reject cross-domain conversion of Hatano-Sasa physical relations."),
    ("ghc-family-registered-report-lock", "Validate outcome-blind protocol and deviation labels structurally."),
]

RUNNERS = [
    ("ghc_family_source_status_drift_guard.py", "Check source statuses and checked dates."),
    ("ghc_family_proposal_neighbor_quarantine.py", "Compare frozen titles and semantic-neighbor tokens."),
    ("ghc_family_logical_manifest_parity.py", "Validate logical and exact manifest domains."),
    ("ghc_family_method_state_preflight.py", "Validate append-only Method Flow states and witnesses."),
    ("ghc_family_terminal_route_guard.py", "Validate PREPARED_NOT_SENT and privacy boundaries."),
    ("ghc_family_evidence_dag_closure.py", "Validate JSON-Pointer evidence DAG closure."),
    ("ghc_family_v646_v2_core_runner.py", "Execute the ten bounded core surfaces."),
    ("ghc_family_v646_v2_portfolio_runner.py", "Execute safe-now and candidate portfolios."),
    ("ghc_family_v646_v2_skill_runner.py", "Build, validate, and smoke-use the phase skill pack."),
    ("ghc_family_v646_v2_validation_runner.py", "Run detailed, minimal, privacy, manifest, and lifecycle checks."),
]

CLEAN_ADOPTED_TITLES = [
    "Reconcile retained-negative counts after ledger growth",
    "Refresh count-dependent validator assertions",
    "Correct stale phase labels additively",
    "Consolidate duplicate wrappers while preserving compatibility callers",
    "Verify cleanup excludes user and sibling paths",
    "Check deterministic generated JSON ordering",
    "Confirm UTF-8 for Māori and other non-ASCII authority text",
    "Review responsive report and complex-chart overflow structurally",
    "Align lifecycle-receipt manifest inclusion rules",
    "Make expected-empty remote checks null-safe",
    "Confirm validation branches remain local-only",
    "Check commit cap and single-parent ancestry",
    "Verify exact and blocked packets receive no execution credit",
    "Refresh phase-scoped GHC Family Index",
    "Update Method Flow recommendations from every witness",
]

CLEAN_NEW_TITLES = [
    "Normalize source-title Unicode without deleting culturally correct text",
    "Synchronize Method Flow ledger, tests, and summaries",
    "Bind x1 absence checks to the immutable x1 tree",
    "Refresh source status cardinalities after final source review",
    "Reconcile privacy scan file counts with exact scope",
    "Verify each manifest self-exclusion rule",
    "Check report skip link, landmarks, headings, and table captions",
    "Check SVG fallback and long-description synchronization",
    "Verify exact-gated core work has no completion credit",
    "Separate inherited post-final negatives from current owner failures",
    "Verify no detached validation worktree is used",
    "Verify exactly one additional named replay is planned",
    "Recheck remote equality with null-safe zero-line handling",
    "Verify each runner has one bounded witness",
    "Refresh memory plan without claiming terminal delivery",
]


def support_item(prefix: str, index: int, title: str, origin: str) -> dict[str, Any]:
    return {
        "packet_id": f"V6462-{prefix}-{index:02d}",
        "title": title,
        "owner": OWNER,
        "origin": origin,
        "approval_class": "safe_now_owner_scoped_structural",
        "hypothesis": f"A bounded owner-scoped implementation of {title.lower()} can produce auditable structural evidence without crossing protected gates.",
        "null_or_failure": "The artifact is absent, privacy is crossed, a structural result is overstated, a failure is erased, or a protected gate is silently closed.",
        "acceptance_gate": "The x2 artifact, bounded witness, and privacy-safe receipt must all pass before completion credit.",
        "rollback_or_recovery": "Retain the negative, restore the last validated owner-scoped state, and leave unavailable evidence or authority explicitly open.",
        "protected_gates": ["authority", "real_data_or_participants", "production", "sibling_lane", "independent_reproduction", "stage20"],
        "x1_state": "preregistered_no_completion_credit",
    }


SAFE_NOW = [
    *[support_item("ADOPT-SAFE", i, title, "eiren_baton_seed_rewritten_after_review") for i, title in enumerate(SAFE_ADOPTED_TITLES, 1)],
    *[support_item("NEW-SAFE", i, title, "ilyra_new_x1") for i, title in enumerate(SAFE_NEW_TITLES, 1)],
]
CANDIDATES = [
    *[support_item("ADOPT-CAND", i, title, "eiren_baton_seed_rewritten_after_review") for i, title in enumerate(CANDIDATE_ADOPTED_TITLES, 1)],
    *[support_item("NEW-CAND", i, title, "ilyra_new_x1") for i, title in enumerate(CANDIDATE_NEW_TITLES, 1)],
]
CLEAN_TASKS = [
    *[support_item("ADOPT-CLEAN", i, title, "eiren_baton_seed_rewritten_after_review") for i, title in enumerate(CLEAN_ADOPTED_TITLES, 1)],
    *[support_item("NEW-CLEAN", i, title, "ilyra_new_x1") for i, title in enumerate(CLEAN_NEW_TITLES, 1)],
]
