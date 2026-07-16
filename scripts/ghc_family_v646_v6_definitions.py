#!/usr/bin/env python3
"""Frozen x1 definitions for Sylven Arc v646-v6.

Importing this module performs no I/O and grants no x2 completion credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v646-gmut-thos-v6-x1-x2"
PHASE_SHORT = "v646-v6"
OWNER = "Sylven Arc"
SLUG = "sylven-arc"
PRONOUNS = "they/them"
ROLE = "constraint-cartographer and falsifier-keeper"
HOPE = "make unresolved boundaries legible without turning uncertainty into authority"
PRIMARY_FOCUS = "Freed ID/CBR Heart"
BOUNDED_PRACTICE = "hydrographic chart correction, hazard-report triage, and Notices to Mariners handover"

SOURCE_PHASE = "v646-gmut-thos-v5-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_REVISION = "65cb62620eec19eb2ac7b3b1a320823ed5621d58"
SOURCE_INHERITED_REVISION = "d970dbc12cd0ded0d6790454491fa45d3012aa86"
SOURCE_X1_REVISION = "3f6b5302e18c7828d19ffb621da153f6ae173de0"
SOURCE_EVIDENCE_REVISION = "575b8fb6c443d10be5551d57621a7cee17de751e"
SOURCE_SEAL_REVISION = SOURCE_REVISION
PRIOR_FROZEN_PROPOSALS = 440
INHERITED_EFFECTIVE_NEGATIVES = 2884
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 14
INHERITED_EXACT_GATES = 15
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Sylven Arc, they/them, is relational working language for a constraint-cartographer and "
    "falsifier-keeper. It is not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, professional qualification, or independent authority. Hamish may "
    "rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, hydrographic, maritime-safety, legal, "
    "cultural, affected-party, and Māori concepts remain under competent, affected-party, and Māori "
    "authority. No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, "
    "personhood, deployment, privacy-complete, exhaustive-security, independent-reproduction, "
    "accessibility-complete, professional, emergency, proof or canon, or Stage 20 claim is made."
)


def proposal(
    index: int,
    title: str,
    mission: str,
    hypothesis: str,
    failure: str,
    approval: str,
    lane: str,
    sources: list[str],
    artifacts: list[str],
    gate: str,
    recovery: str,
    protected: list[str],
    expected: str,
    novelty: str,
) -> dict[str, Any]:
    return {
        "proposal_id": f"V6466-P{index:02d}",
        "title": title,
        "mission_surface": mission,
        "hypothesis": hypothesis,
        "null_or_failure": failure,
        "approval_class": approval,
        "execution_lane": lane,
        "current_primary_or_official_source_needs": sources,
        "concrete_artifacts": artifacts,
        "test_falsifier_or_acceptance_gate": gate,
        "rollback_or_recovery": recovery,
        "protected_gates": protected,
        "expected_disposition": expected,
        "novelty_against_440_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Method Flow durable-outbox, acknowledgement-order, poison-item, and exactly-once nonclaim ledger",
        "prepared record, durable append, dispatch intent, acknowledgement, monotonic sequence, duplicate delivery, poison item, retry budget, dead-letter state, recovery credit, and external-side-effect refusal",
        "An append-only owner-local ledger can require durable evidence before acknowledgement credit, quarantine sequence gaps and poison items, and distinguish deduplicated replay from an unsupported exactly-once claim.",
        "Acknowledgement precedes durable recording, a duplicate or sequence gap passes, a poison item retries without budget, dead-letter evidence disappears, or an external side effect is automatically repeated.",
        "safe_now_owner_scoped_workflow",
        "x2_build_task",
        ["V6466-S01", "V6466-S02", "V6466-S12"],
        ["method-flow/durable-outbox-contract.json", "method-flow/delivery-order-mutation-vectors.json"],
        "Synthetic traces must reject pre-durable acknowledgement, sequence gaps, duplicate-credit, poison loops, missing dead-letter evidence, and automatic external side effects while preserving every attempted delivery.",
        "Quarantine the item, retain every attempt and acknowledgement discrepancy, restore the last durable owner-local sequence, and require fresh authority before any external delivery.",
        ["external_state", "destructive_action", "credentials", "sibling_lane", "completion_credit", "stage20"],
        "completed",
        "Earlier Method Flow proposals cover retries, checkpoints, child processes, rollback, idempotency, compare-and-swap, and lost updates; none centers durable outbox ordering, poison-item quarantine, dead-letter retention, and the exactly-once nonclaim together.",
    ),
    proposal(
        2,
        "GMUT Schwinger-Dyson hierarchy, truncation-closure, and renormalization-condition obligation tribunal",
        "generating functional, source derivative, one-particle-irreducible effective action, n-point hierarchy, self-energy, vertex equation, closure ansatz, truncation order, counterterm, renormalization condition, symmetry identity, units, and EFT domain",
        "A typed symbolic tribunal can expose hierarchy, closure, counterterm, and symmetry obligations without asserting that a GMUT quantum theory, solution, observable, or renormalized prediction exists.",
        "The hierarchy is silently closed, an omitted vertex is called zero, a counterterm or renormalization condition disappears, a symmetry identity is assumed after incompatible truncation, units drift, or symbolic consistency becomes physical proof.",
        "safe_now_symbolic_research_only",
        "x2_build_task",
        ["V6466-S03", "V6466-S04"],
        ["gmut/schwinger-dyson-obligations.json", "gmut/schwinger-dyson-mutations.json"],
        "Positive and negative fixtures must type hierarchy level, closure assumption, retained and omitted vertices, counterterms, renormalization conditions, symmetry scope, units, and explicit nonpromotion boundaries.",
        "Retain the failed obligation, reopen the hierarchy, restore the declared truncation and renormalization conditions, and make no quantization, unitarity, stability, prediction, likelihood, constraint, or Theory-of-Everything claim.",
        ["quantum_completion", "renormalized_prediction", "unitarity_proof", "stability_proof", "empirical_confirmation", "theory_of_everything"],
        "completed",
        "The frozen chain covers BRST, Peierls brackets, Schwinger-Keldysh contours, spectral density, operator quotients, and radiative stability; none centers Schwinger-Dyson hierarchy closure and renormalization-condition bookkeeping.",
    ),
    proposal(
        3,
        "GMUT eROSITA eRASS1 cluster-selection, mass-calibration, and covariance zero-row protocol",
        "eRASS1 release and catalogue version, sky footprint, extended-source selection, optical confirmation, redshift range, observable-mass relation, selection function, contamination, completeness, covariance, nuisance lock, baseline, and zero-row likelihood refusal",
        "A zero-row adapter can freeze official eRASS1 cluster-product and selection requirements while refusing to turn catalogue descriptions or published cosmology into GMUT observations, likelihoods, or constraints.",
        "The phase downloads a row, imports a published estimate as an observation, omits selection or mass calibration, fabricates covariance, changes nuisance assumptions after exposure, evaluates a likelihood, or emits a GMUT force or constraint.",
        "real_data_access_and_independent_review_required",
        "x2_open_gap",
        ["V6466-S05", "V6466-S06"],
        ["empirical/erosita-erass1-study-contract.json", "empirical/erosita-erass1-zero-row-receipt.json"],
        "The receipt must preserve zero account use, downloads, real catalogue rows, cluster measurements, likelihood calls, posterior samples, constraints, force claims, and empirical GMUT claims.",
        "Stop before download or fit, retain the zero-row receipt, and require a separately authorized preregistration with frozen catalogue version, selection, calibration, covariance, nuisance model, baseline, uncertainty analysis, and independent review.",
        ["account_access", "real_data", "likelihood", "posterior", "parameter_constraint", "force_claim", "empirical_confirmation"],
        "open_gap",
        "Earlier adapters cover Rubin, Euclid, DESI, ACT, PTA, EHT, Gaia, standard sirens, lensing, and ranging; none centers eROSITA eRASS1 cluster selection, mass calibration, and covariance.",
    ),
    proposal(
        4,
        "THOS hydrographic hazard-report, chart-correction, notice-lifecycle, and watch-handover proxy",
        "synthetic report identity, chart or ENC edition, datum, position-fixing method, uncertainty, hazard class, evidence source, producer-reviewer separation, correction state, notice edition, cancellation, matched budget, blind arm label, workload, and next-watch ownership",
        "Synthetic traces can expose report, correction, notice, cancellation, and handover failures while preserving every mariner, vessel, charting, safety, professional, and effectiveness gate.",
        "A fixture contains a real mariner, vessel, voyage, hazard, protected location, or operational chart update; publishes a notice; breaks matched budgets or blinding; or claims THOS effectiveness or hydrographic competence.",
        "safe_now_proxy_protocol_no_people_or_operations",
        "x2_proxy_protocol",
        ["V6466-S07", "V6466-S08"],
        ["thos/hydrographic-handover-contract.json", "thos/hydrographic-proxy-vectors.json"],
        "Unsafe synthetic traces must fail, and the packet must record zero real people, vessels, voyages, hazards, chart corrections, notices, blind real arms, safety events, operational decisions, and effectiveness estimates.",
        "Withdraw operational language, retain rejected traces, and defer real decisions to authorized hydrographic, maritime-safety, workplace, legal, affected-party, Māori, and independent-review processes.",
        ["real_people", "real_operations", "professional_authority", "maritime_safety", "publication_authority", "deployment", "effectiveness"],
        "represented",
        "No frozen proposal centers hydrographic hazard-report triage, chart-correction state, Notice to Mariners lifecycle, and matched-budget watch handover as one THOS proxy.",
    ),
    proposal(
        5,
        "Freed ID DPoP method-URI, nonce, token-hash, key-thumbprint, and replay-cache profile",
        "DPoP proof type, public JWK, algorithm, HTTP method, target URI, issue time, unique identifier, authorization-server nonce, access-token hash, key thumbprint, token type, freshness window, replay cache, error response, minimization, and refusal",
        "Synthetic vectors can enforce selected RFC 9449 request and token-binding obligations without asserting real keys, tokens, authorization, transport integrity, interoperability, or production identity assurance.",
        "Private key material appears, method or URI mismatches pass, nonce downgrade succeeds, token hash or key thumbprint is unbound, replay cache is bypassed, unsupported algorithms pass, or synthetic bytes become production assurance.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["V6466-S10"],
        ["freed-id/dpop-binding-profile.json", "freed-id/dpop-replay-mutation-vectors.json"],
        "Vectors must reject proof-type, algorithm, method, URI, time, identifier, nonce, token-hash, key-thumbprint, token-type, and replay-cache mutations while recording zero real private keys, tokens, authorizations, identities, or network exchanges.",
        "Reject the synthetic request, retain the vector, disclose no real key or identity data, and require conforming real keys, authorization servers, protected resources, TLS, interoperability, privacy/security review, recovery, and trust governance.",
        ["real_keys", "real_tokens", "authorization", "interoperability", "production", "privacy_complete", "security_certification"],
        "represented",
        "Prior Freed ID work covers proof purpose, OpenID request and transaction binding, key attestation, wallet flows, status, BBS, SD-JWT, and issuance; none centers RFC 9449 DPoP method/URI, nonce, access-token hash, key thumbprint, and replay cache.",
    ),
    proposal(
        6,
        "CBR navigation-hazard disclosure, chart-publication, place-name, remedy, and Māori-authority matrix",
        "suspected navigation hazard, report confidentiality, publication threshold, chart and notice correction, false-report risk, source protection, commercial impact, customary use, sensitive location, official and recorded place names, data governance, remedy, legal interpretation, affected parties, and Māori authority",
        "A refusal-first matrix can expose unresolved disclosure, publication, place-name, remedy, and authority questions without deciding a real hazard, chart correction, notice, name, right, or remedy.",
        "The matrix identifies a real protected reporter or site, publishes a hazard, changes a chart or place name, decides customary rights, allocates remedy, interprets law, asserts cultural or Māori authority, or treats official guidance as delegated case authority.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["V6466-S07", "V6466-S08", "V6466-S09", "V6466-S11"],
        ["cbr/navigation-chart-authority-reservation.json", "cbr/hazard-name-remedy-matrix.json"],
        "Repository software must stop at unknown or reserved; only competent hydrographic, maritime-safety, place-naming, privacy, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        "Stop before disclosure, publication, chart correction, place naming, customary-right, or remedy conclusions; minimize data and route only through authorized external processes.",
        ["publication_authority", "place_name_authority", "affected_party_authority", "privacy", "legal_interpretation", "cultural_ratification", "maori_authority", "remedy_decision"],
        "exact_gate",
        "Earlier CBR gates cover fisheries, archives, medicine recalls, aviation occurrences, utilities, cadastral change, relocation, and animal disease; none centers navigation-hazard disclosure, hydrographic publication, place-name status, remedy, and Māori authority together.",
    ),
    proposal(
        7,
        "JSON text-sequence record-separator, torn-tail, continuation, and ordinal-integrity tribunal",
        "UTF-8, record separator, JSON text, line feed, invalid record, parser continuation, torn final number, sequence ordinal, content digest, duplicate ordinal, missing ordinal, noncanonical encoding, and disposable confinement",
        "A disposable RFC 7464-oriented tribunal can distinguish recoverable invalid or torn elements from valid records and can layer explicit local ordinal and digest checks without claiming a standard canonical form.",
        "A missing record separator passes, invalid UTF-8 is normalized silently, a torn final number gains credit, an invalid element disappears without a negative, ordinal gaps or duplicates pass, or the fixture touches canonical evidence.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["V6466-S12"],
        ["tooling/json-sequence-contract.json", "tooling/json-sequence-mutation-vectors.json"],
        "Disposable fixtures must cover valid sequences, invalid-record continuation, torn tails, top-level numbers, missing separators, duplicate and missing local ordinals, digest mismatch, cleanup, and canonical-repository nonmutation.",
        "Discard only the disposable fixture, retain every failed element and ordinal discrepancy, restore the last complete record boundary, and keep canonicalization, durability, production, and exhaustive-security claims false.",
        ["canonical_evidence", "sibling_lane", "destructive_filesystem", "production", "exhaustive_security"],
        "completed",
        "Earlier work covers append-only Merkle logs, JSON canonicalization, parser disagreement, torn SQLite state, and serialization ambiguity; none centers RFC 7464 record separators, invalid-element continuation, torn-tail detection, and an explicitly nonstandard local ordinal layer.",
    ),
    proposal(
        8,
        "Accessible dragging-alternative, pointer-cancellation, and target-spacing structural audit",
        "drag operation, single-pointer alternative, keyboard alternative declaration, down-event versus up-event activation, abort or undo, target dimensions, spacing exception, overlapping target, essential exception, visible instruction, and manual-evaluation reservation",
        "A structural auditor can reject missing non-drag alternatives and unsupported target-spacing declarations while reserving runtime pointer, keyboard, browser, assistive-technology, motor-access, and affected-user evaluation.",
        "A drag-only function passes, activation is bound irreversibly to pointer-down, cancellation is absent, undersized overlapping targets pass without an exception, or structural evidence becomes complete accessibility conformance.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6466-S13"],
        ["accessibility/pointer-operation-contract.json", "accessibility/pointer-operation-mutations.json"],
        "Positive and negative fixtures must cover drag alternatives, pointer cancellation, undo, target size and spacing declarations, overlap, exceptions, instructions, and explicit manual reservations.",
        "Mark the structure incomplete, retain failures, restore an operable non-drag alternative and cancellation path, and require qualified manual browser, keyboard, assistive-technology, Māori-language, motor-access, and affected-user evaluation.",
        ["accessibility_complete", "runtime_pointer_behavior", "manual_keyboard_evaluation", "assistive_technology", "affected_user_acceptance"],
        "completed",
        "Earlier accessibility proposals cover focus, forms, tables, charts, maps, details, dialogs, popovers, language, reflow, and inertness; none centers dragging alternatives, pointer cancellation, and target spacing together.",
    ),
    proposal(
        9,
        "Thermo/Psyche Gibbs phase-rule component-count, constraint-rank, and psyche-choice nonconversion classifier",
        "equilibrium, component count, phase count, intensive variables, reactive constraints, externally fixed variables, degrees of freedom, nonnegative rank, applicability, and category barrier",
        "A typed classifier can check a declared Gibbs phase-rule count and constrained variants while rejecting conversion of thermodynamic degrees of freedom into human choice, autonomy, identity, justice, or consciousness claims.",
        "Components or phases are miscounted, equilibrium is absent, reactive or external constraints are hidden, negative freedom passes, intensive-variable assumptions drift, or phase-rule freedom becomes participant or psyche evidence.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["V6466-S14"],
        ["thermo-psyche/gibbs-phase-rule-contract.json", "thermo-psyche/gibbs-phase-rule-mutations.json"],
        "Fixtures must enforce declared components, phases, equilibrium, constraint rank, externally fixed variables, nonnegative degrees of freedom, domain refusal, and the psyche category barrier.",
        "Restore the thermodynamic domain and explicit counts, retain the rejection, and require independently valid human theory, measures, authority, and participant evidence before any human inference.",
        ["participant_inference", "psyche_claim", "autonomy_claim", "justice_claim", "consciousness", "fundamental_law"],
        "completed",
        "The chain covers Gibbs-Duhem, Clapeyron, Maxwell, Onsager, Joule-Thomson, phase-transition order, and several entropy relations; no prior title centers Gibbs phase-rule component and phase counting with explicit constraint-rank refusal.",
    ),
    proposal(
        10,
        "Stage 20 decision-curve threshold, net-benefit, prevalence-transport, and value-authority nonpromotion board",
        "prediction target, threshold probability, true and false positives, harm-benefit exchange, net benefit, treat-all and treat-none baselines, prevalence, calibration, target population, uncertainty, value authority, and terminal abstention",
        "A fail-closed structural board can quarantine decision-curve credit when threshold preferences, prevalence, calibration, target population, uncertainty, or authority are missing or transported without evidence.",
        "A threshold is invented by the technical owner, prevalence or calibration shifts silently, harms are hidden, treat-all and treat-none baselines disappear, uncertainty is omitted, net benefit is treated as universal value, or Stage 20 advances.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6466-S15", "V6466-S16"],
        ["stage20/decision-curve-contract.json", "stage20/decision-curve-mutations.json"],
        "Mutations must reject missing or unauthorized thresholds, prevalence transport, calibration drift, hidden harm weights, missing baselines, unsupported uncertainty, cross-domain value substitution, and Stage 20 promotion.",
        "Withdraw affected evidence credit, retain the curve inputs and failure, require governed target-population and value judgments plus independent evaluation, and abstain.",
        ["stage20", "value_authority", "participant_evidence", "independent_reproduction", "deployment", "proof_or_canon"],
        "completed",
        "Earlier Stage 20 boards cover metrics, optional stopping, contamination, controls, environment locks, Registered Reports, Goodhart effects, and correlated evidence; none centers decision-curve thresholds, net benefit, prevalence transport, and value-authority refusal.",
    ),
]


SOURCES = [
    {"source_id":"V6466-S01","status":"current","title":"GHC Family Method Flow State schema and runner","authority":"family-current local skill","url":None,"checked_on":"2026-07-16","use":"append-only failure, witness, recovery, rollback, and recurrence-guard requirements"},
    {"source_id":"V6466-S02","status":"current","title":"GHC Family Index routing and closeout guidance","authority":"family-current local skill","url":None,"checked_on":"2026-07-16","use":"source precedence, ownership, x1/x2 separation, truth labels, route state, and closeout"},
    {"source_id":"V6466-S03","status":"stable","title":"Renormalizing the Schwinger-Dyson equations in auxiliary-field lambda-phi-four theory","authority":"Cooper, Mihaila, and Dawson primary research","url":"https://arxiv.org/abs/hep-ph/0407119","checked_on":"2026-07-16","use":"hierarchy truncation and renormalization obligations only"},
    {"source_id":"V6466-S04","status":"stable","title":"Correlation functions of three-dimensional Yang-Mills theory from Dyson-Schwinger equations","authority":"Huber primary research","url":"https://arxiv.org/abs/1602.02038","checked_on":"2026-07-16","use":"self-consistent truncation and vertex-system context only"},
    {"source_id":"V6466-S05","status":"current","title":"eROSITA Data Release 1 catalogues","authority":"eROSITA-DE consortium official release","url":"https://erosita.mpe.mpg.de/dr1/AllSkySurveyData_dr1/Catalogues_dr1/","checked_on":"2026-07-16","use":"official eRASS1 cluster catalogue identity, version, and selection context; zero ingestion"},
    {"source_id":"V6466-S06","status":"current","title":"eROSITA Data Release 1","authority":"eROSITA-DE consortium official release","url":"https://erosita.mpe.mpg.de/dr1/","checked_on":"2026-07-16","use":"release provenance and product boundary only; no observations or published estimates adopted"},
    {"source_id":"V6466-S07","status":"current","title":"About Notices to Mariners","authority":"Toitū Te Whenua Land Information New Zealand","url":"https://www.linz.govt.nz/guidance/marine-information/charts/about-notices-mariners","checked_on":"2026-07-16","use":"official notice and chart-correction workflow context; no publication authority delegated"},
    {"source_id":"V6466-S08","status":"current","title":"Report a hazard to navigation - Hydrographic Note","authority":"Toitū Te Whenua Land Information New Zealand","url":"https://www.linz.govt.nz/products-services/maritime-safety/safety-sea/report-hazard-navigation-hydrographic-note","checked_on":"2026-07-16","use":"official report fields and handover context; no real report submitted"},
    {"source_id":"V6466-S09","status":"current","title":"New Zealand Geographic Board role and place-name guidance","authority":"Toitū Te Whenua Land Information New Zealand","url":"https://www.linz.govt.nz/our-work/new-zealand-geographic-board/about-new-zealand-geographic-board","checked_on":"2026-07-16","use":"official place-name role boundary; no naming decision or legal interpretation"},
    {"source_id":"V6466-S10","status":"stable","title":"RFC 9449 OAuth 2.0 Demonstrating Proof of Possession","authority":"Internet Engineering Task Force","url":"https://datatracker.ietf.org/doc/rfc9449/","checked_on":"2026-07-16","use":"DPoP proof, method, URI, nonce, token-hash, key-binding, replay, and downgrade obligations"},
    {"source_id":"V6466-S11","status":"current","title":"Principles of Māori Data Sovereignty","authority":"Te Mana Raraunga Māori Data Sovereignty Network","url":"https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty","checked_on":"2026-07-16","use":"Māori data-governance and authority reservation; never delegated authority"},
    {"source_id":"V6466-S12","status":"stable","title":"RFC 7464 JavaScript Object Notation Text Sequences","authority":"Internet Engineering Task Force","url":"https://www.rfc-editor.org/info/rfc7464/","checked_on":"2026-07-16","use":"record separator, UTF-8, line feed, invalid-record continuation, and truncation boundaries"},
    {"source_id":"V6466-S13","status":"stable","title":"Web Content Accessibility Guidelines 2.2","authority":"World Wide Web Consortium","url":"https://www.w3.org/TR/WCAG22/","checked_on":"2026-07-16","use":"dragging-alternative, pointer-cancellation, and target-size context while manual conformance remains reserved"},
    {"source_id":"V6466-S14","status":"current","title":"IUPAC Gold Book phase rule","authority":"International Union of Pure and Applied Chemistry","url":"https://goldbook.iupac.org/terms/view/P04533","checked_on":"2026-07-16","use":"phase-rule definition and source-domain terminology only"},
    {"source_id":"V6466-S15","status":"stable","title":"Decision Curve Analysis: A Novel Method for Evaluating Prediction Models","authority":"Vickers and Elkin primary research","url":"https://doi.org/10.1177/0272989X06295361","checked_on":"2026-07-16","use":"threshold probability and net-benefit method context only"},
    {"source_id":"V6466-S16","status":"current","title":"NIST AI RMF Measure playbook","authority":"United States National Institute of Standards and Technology","url":"https://airc.nist.gov/airmf-resources/playbook/measure/","checked_on":"2026-07-16","use":"measurement limitation and context documentation; no readiness authority"},
]


SAFE_TITLES = [
    "Sylven v646-v6 exact Tamar-source four-way gate",
    "Sylven v646-v6 frozen 440-proposal identifier census",
    "Sylven v646-v6 inherited 2884-negative conservation proof",
    "Sylven v646-v6 x1 companion immutability check",
    "Sylven v646-v6 current-source and watch-label review",
    "Sylven v646-v6 successor-test exclusion exactness guard",
    "Sylven v646-v6 staged Git-blob path review",
    "Sylven v646-v6 five-class candidate-confirmed privacy split",
    "Sylven v646-v6 phase-commit and parent-count proof",
    "Sylven v646-v6 owner-addition footprint receipt",
    "Sylven v646-v6 manual accessibility reservation lint",
    "Sylven v646-v6 protected-packet nonexecution review",
    "Sylven v646-v6 one-shot Eiren route-state guard",
    "Sylven v646-v6 UTF-8 and LF artifact guard",
    "Sylven v646-v6 Method Flow append-only schema validation",
    "Sylven v646-v6 durable-outbox ordering preflight",
    "Sylven v646-v6 poison-item retry-budget rejection",
    "Sylven v646-v6 Schwinger-Dyson hierarchy-closure lint",
    "Sylven v646-v6 eROSITA zero-row invariant",
    "Sylven v646-v6 hydrographic zero-operation boundary invariant",
    "Sylven v646-v6 DPoP method-URI-token binding lint",
    "Sylven v646-v6 navigation-publication authority vocabulary gate",
    "Sylven v646-v6 JSON-sequence separator and torn-tail audit",
    "Sylven v646-v6 JSON-sequence ordinal-integrity check",
    "Sylven v646-v6 dragging-alternative structural check",
    "Sylven v646-v6 Gibbs phase-rule domain classifier",
    "Sylven v646-v6 decision-curve threshold-authority lock",
    "Sylven v646-v6 citation-to-observation nonconversion guard",
    "Sylven v646-v6 named validation lane locality preflight",
    "Sylven v646-v6 post-final external-negative carry-forward guard",
]

CANDIDATE_TITLES = [
    "Durable-outbox acknowledgement-order prototype",
    "Poison-item dead-letter retention simulator",
    "Schwinger-Dyson hierarchy obligation board",
    "Schwinger-Dyson truncation mutation set",
    "eROSITA eRASS1 cluster zero-row adapter",
    "eROSITA selection-calibration provenance lock",
    "Hydrographic notice-lifecycle handover proxy",
    "Hydrographic correction cancellation state machine",
    "DPoP proof-binding synthetic profile",
    "DPoP nonce-downgrade and replay fixture",
    "Navigation-chart authority refusal matrix",
    "Sensitive-location place-name reservation matrix",
    "JSON text-sequence torn-tail tribunal",
    "JSON text-sequence ordinal-digest fixture",
    "Dragging-alternative structural auditor",
    "Pointer-cancellation and target-spacing fixture",
    "Gibbs phase-rule domain classifier",
    "Reactive-constraint phase-rule mutation set",
    "Decision-curve nonpromotion board",
    "Prevalence-transport and threshold-authority fixture",
]

SKILLS = [
    ("ghc-family-v646-v6-durable-outbox-credit", "Require durable owner-local evidence before acknowledgement credit."),
    ("ghc-family-v646-v6-poison-item-quarantine", "Bound retries and preserve poison-item and dead-letter evidence."),
    ("ghc-family-v646-v6-schwinger-dyson-obligations", "Audit hierarchy, closure, counterterm, and renormalization obligations."),
    ("ghc-family-v646-v6-erosita-zero-row", "Describe eRASS1 requirements while enforcing zero rows and likelihoods."),
    ("ghc-family-v646-v6-hydrographic-handover-proxy", "Validate synthetic hazard, correction, notice, and watch handovers."),
    ("ghc-family-v646-v6-dpop-binding-profile", "Validate synthetic RFC 9449 proof and token bindings."),
    ("ghc-family-v646-v6-navigation-authority-reservation", "Reserve hydrographic, place-name, legal, affected-party, and Māori authority."),
    ("ghc-family-v646-v6-json-sequence-tribunal", "Validate bounded RFC 7464-oriented sequence fixtures."),
    ("ghc-family-v646-v6-dragging-alternative-audit", "Audit non-drag alternatives, cancellation, and target declarations."),
    ("ghc-family-v646-v6-gibbs-phase-rule-domain", "Check phase-rule counts while blocking psyche conversion."),
    ("ghc-family-v646-v6-decision-curve-nonpromotion", "Bind thresholds, prevalence, baselines, uncertainty, and value authority."),
    ("ghc-family-v646-v6-x1-companion-immutability", "Keep frozen x1 paths and content separate from x2 evidence."),
    ("ghc-family-v646-v6-negative-baseline-reconcile", "Preserve inherited, x1, synthetic, x2, and post-route totals."),
    ("ghc-family-v646-v6-source-observation-firewall", "Keep source metadata separate from observation and authority credit."),
    ("ghc-family-v646-v6-staged-blob-domain", "Review exact staged Git blobs with declared self exclusions."),
    ("ghc-family-v646-v6-owner-footprint-threshold", "Apply the 15000 threshold only to Sylven-generated additions."),
    ("ghc-family-v646-v6-local-validation-lane", "Prove the sole named replay lane is local-only and unpushed."),
    ("ghc-family-v646-v6-single-parent-budget", "Bind source ancestry, parent count, zero merges, and commit cap."),
    ("ghc-family-v646-v6-static-report-reservations", "Separate structural accessibility from manual and affected-user evaluation."),
    ("ghc-family-v646-v6-one-shot-eiren-baton", "Keep the Eiren route prepared until one acknowledged existing-task send."),
]

RUNNERS = [
    ("ghc_family_v646_v6_runtime.py", "Execute all bounded core surface fixtures."),
    ("ghc_family_v646_v6_core_runner.py", "Invoke and summarize the ten frozen core surfaces."),
    ("ghc_family_v646_v6_portfolio_runner.py", "Execute thirty safe, twenty candidate, and thirty cleanup tasks."),
    ("ghc_family_v646_v6_skill_runner.py", "Build, validate, and smoke-use twenty phase-local skills."),
    ("ghc_family_v646_v6_staged_review.py", "Review exact staged paths, privacy classes, JSON, and manifest parity."),
    ("ghc_family_v646_v6_validation_runner.py", "Run current, eligible scoped, detailed, minimal, JSON, and privacy checks."),
    ("ghc_family_v646_v6_outbox_tribunal.py", "Run delivery-order, duplicate, poison-item, and dead-letter fixtures."),
    ("ghc_family_v646_v6_json_sequence_tribunal.py", "Run record-separator, torn-tail, continuation, and ordinal fixtures."),
    ("ghc_family_v646_v6_source_gate.py", "Check source status, zero-row, proxy, and authority boundaries."),
    ("ghc_family_v646_v6_named_lane_audit.py", "Verify exact-head local-only named-lane conditions."),
]

CLEAN_TITLES = [
    "Reconcile the 2884 inherited Sylven activation baseline",
    "Synchronize the v646-v6 440-to-450 proposal counts",
    "Preserve exact v646-v6 x1 paths across x2",
    "Map v646-v6 callers to family-current and compatibility surfaces",
    "Constrain cleanup to Sylven-owned generated paths",
    "Canonicalize v646-v6 JSON with deterministic UTF-8 key order",
    "Preserve Māori diacritics with explicit authority reservations",
    "Test static-report overflow without responsive-conformance claims",
    "Declare v646-v6 staged evidence and sealed manifest membership",
    "Treat absent validation-lane remote output as expected empty state",
    "Prove the v646-v6 replay branch local-only without deletion",
    "Bind the v646-v6 commit cap to source and final parent count",
    "Re-audit inherited open-gap and exact-gate packet nonexecution",
    "Publish v646-v6 Method Flow successor recommendations",
    "Qualify canonical and replay evidence as same-owner shared-infrastructure only",
    "Record inherited checkout and Sylven-added file counts separately",
    "Keep eROSITA catalogue metadata separate from observations",
    "Keep hydrographic fixtures free of real hazard and vessel data",
    "Keep DPoP fixtures free of private keys and live tokens",
    "Reserve navigation publication and place-name decisions",
    "Keep JSON-sequence teardown inside a disposable root",
    "Retain invalid JSON-sequence elements as negatives",
    "Associate every drag operation with a non-drag alternative",
    "Reserve manual pointer and assistive-technology evaluation",
    "Require declared Gibbs components, phases, and constraints",
    "Retain phase-rule domain refusals",
    "Freeze decision-curve threshold and prevalence context",
    "Retain both baseline and model curves on semantic divergence",
    "Preserve post-final faults after the phase cap seals",
    "Keep terminal Eiren route prepared until acknowledgement",
]


def support_item(prefix: str, index: int, title: str, approval_class: str) -> dict[str, Any]:
    return {
        "packet_id": f"V6466-{prefix}-{index:02d}",
        "title": title,
        "owner": OWNER,
        "origin": "sylven_new_x1_after_440_surface_audit",
        "approval_class": approval_class,
        "hypothesis": f"A bounded owner-scoped implementation of {title.lower()} can produce auditable structural evidence without crossing protected gates.",
        "null_or_failure": "The artifact is absent, privacy is crossed, a result is overstated, a failure is erased, or a protected gate is silently closed.",
        "acceptance_gate": "The x2 artifact, bounded witness, privacy-safe receipt, and compatibility check must pass before completion credit.",
        "rollback_or_recovery": "Retain the negative, restore the last validated owner-scoped state, and leave unavailable evidence or authority explicitly open.",
        "protected_gates": ["authority", "real_data_or_participants", "production", "sibling_lane", "independent_reproduction", "stage20"],
        "x1_state": "preregistered_no_completion_credit",
    }


SAFE_NOW = [support_item("SAFE", i, title, "safe_now_owner_scoped_structural") for i, title in enumerate(SAFE_TITLES, 1)]
CANDIDATES = [support_item("CAND", i, title, "candidate_bounded_prototype") for i, title in enumerate(CANDIDATE_TITLES, 1)]
CLEAN_TASKS = [support_item("CLEAN", i, title, "safe_now_owner_scoped_additive_cleanup") for i, title in enumerate(CLEAN_TITLES, 1)]
