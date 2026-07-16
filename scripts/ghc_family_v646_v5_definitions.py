#!/usr/bin/env python3
"""Frozen x1 definitions for Tamar Vey v646-v5.

Importing this module performs no I/O and grants no x2 completion credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v646-gmut-thos-v5-x1-x2"
PHASE_SHORT = "v646-v5"
OWNER = "Tamar Vey"
SLUG = "tamar-vey"
PRONOUNS = "they/them"
ROLE = "evidence-systems cartographer and boundary keeper"
HOPE = "keep every decision legible, every failure recoverable, and every authority boundary intact"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = "veterinary diagnostic-laboratory accession, amended-result, and shift-handover review"

SOURCE_PHASE = "v646-gmut-thos-v4-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
SOURCE_REVISION = "d970dbc12cd0ded0d6790454491fa45d3012aa86"
SOURCE_INHERITED_REVISION = "c45aba6c9c2fee5d60e1fcde9f0de849290cfc96"
SOURCE_X1_REVISION = "8b63d3f65f9fe9909da71eeb1171e3b5cf86768a"
SOURCE_EVIDENCE_REVISION = "3aa962ee71ed087d1ef44311b11be80b47ba6a0e"
SOURCE_SEAL_REVISION = SOURCE_REVISION
PRIOR_FROZEN_PROPOSALS = 430
BATON_TIME_INHERITED_NEGATIVES = 2799
POST_BATON_INHERITED_NEGATIVES = 1
INHERITED_EFFECTIVE_NEGATIVES = 2800
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 13
INHERITED_EXACT_GATES = 14
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Tamar Vey, they/them, is relational working language for an evidence-systems cartographer "
    "and boundary keeper. It is not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, professional qualification, or independent authority. "
    "Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, veterinary, biosecurity, legal, cultural, "
    "affected-party, and Māori concepts remain under competent, affected-party, and Māori authority. "
    "No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, "
    "deployment, privacy-complete, exhaustive-security, independent-reproduction, accessibility-complete, "
    "professional, emergency, public-health, proof or canon, or Stage 20 claim is made."
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
        "proposal_id": f"V6465-P{index:02d}",
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
        "novelty_against_430_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Method Flow compare-and-swap revision, lost-update, conflict-rebase, and evidence-credit ledger",
        "expected revision, observed revision, compare-and-swap, read set, proposed write set, lost update, conflict receipt, bounded rebase, evidence credit, and side-effect refusal",
        "An append-only ledger can refuse stale-revision writes and separate a bounded conflict rebase from silent lost-update promotion.",
        "A stale expected revision writes, a conflict is hidden, a rebase changes protected intent, partial output receives completion credit, or an external side effect is retried automatically.",
        "safe_now_owner_scoped_workflow",
        "x2_build_task",
        ["V6465-S01", "V6465-S02"],
        ["method-flow/optimistic-concurrency-contract.json", "method-flow/lost-update-mutation-vectors.json"],
        "Synthetic revision traces must reject stale writes, hidden conflicts, write-set drift, unbounded rebases, partial-output promotion, and automatic external side effects while retaining both versions.",
        "Quarantine the write, preserve both revisions and the conflict, re-read the bounded owner state, and require fresh authority for any external side effect.",
        ["external_state", "destructive_action", "credentials", "sibling_lane", "completion_credit", "stage20"],
        "completed",
        "Earlier Method Flow proposals cover retries, checkpoints, leases, cancellation, partial output, and idempotency; none makes compare-and-swap revision conflict and lost-update evidence credit the central surface.",
    ),
    proposal(
        2,
        "GMUT Peierls bracket, advanced-retarded support, and gauge-observable obligation tribunal",
        "linearized Euler-Lagrange operator, advanced and retarded Green operators, causal propagator, support, functional derivative, gauge invariance, antisymmetry, Jacobi scope, units, and observable algebra",
        "A typed symbolic tribunal can check Peierls-bracket obligations and causal support without asserting that a physical GMUT observable algebra or quantization is established.",
        "Advanced and retarded support is swapped, the Green operator is used outside its domain, a gauge-variant functional is promoted, antisymmetry or units drift, or a symbolic bracket becomes physical proof.",
        "safe_now_symbolic_research_only",
        "x2_build_task",
        ["V6465-S03", "V6465-S04"],
        ["gmut/peierls-bracket-contract.json", "gmut/peierls-bracket-mutations.json"],
        "Positive and negative fixtures must type the operator, Green functions, causal support, functional derivatives, gauge scope, antisymmetry, Jacobi assumptions, units, and nonpromotion boundary.",
        "Retain the counterexample, mark the bracket unavailable or incomplete, restore explicit domain and gauge assumptions, and make no force, prediction, likelihood, constraint, quantization, or Theory-of-Everything claim.",
        ["observable_algebra_proof", "quantization", "stability_proof", "empirical_confirmation", "theory_of_everything"],
        "completed",
        "The frozen chain covers covariant phase space, BRST, Hadamard states, Schwinger-Keldysh contours, and propagators; no prior proposal centers the Peierls advanced-minus-retarded bracket and gauge-observable support obligations.",
    ),
    proposal(
        3,
        "GMUT Rubin DP1 object-shape, calibration-provenance, and shear-readiness zero-row protocol",
        "DP1 release identity, data-rights access, Object catalog, image provenance, PSF and calibration flags, shape parameterization, known-issue version, selection lock, covariance, shear calibration, and zero-row likelihood refusal",
        "A zero-row adapter can enumerate Rubin DP1 provenance and known limitations while refusing to treat commissioning catalogs or citations as a GMUT weak-lensing dataset or likelihood.",
        "The phase accesses a protected account, downloads a row, treats best-effort shape columns as calibrated shear, ignores known issues, fabricates covariance, evaluates a likelihood, or emits a force or constraint.",
        "real_data_access_and_independent_review_required",
        "x2_open_gap",
        ["V6465-S05", "V6465-S06", "V6465-S07", "V6465-S08"],
        ["empirical/rubin-dp1-study-contract.json", "empirical/rubin-dp1-zero-row-receipt.json"],
        "The receipt must preserve zero account use, zero downloads, zero real rows, zero shear estimates, zero likelihoods, zero fits, zero constraints, and zero empirical GMUT claims.",
        "Stop before access or fit, retain the zero-row receipt, and require separately authorized data access, a frozen product snapshot, calibration and selection treatment, covariance, likelihood, uncertainty analysis, and independent review.",
        ["account_access", "real_data", "likelihood", "parameter_constraint", "force_claim", "empirical_confirmation"],
        "open_gap",
        "Earlier adapters cover Euclid, ACT, DESI, Gaia, EHT, pulsars, binaries, sirens, and ranging; none targets Rubin Data Preview 1 object-shape limitations and shear-readiness refusal.",
    ),
    proposal(
        4,
        "THOS veterinary-laboratory accession, amended-result, escalation, and shift-handover proxy",
        "synthetic submission identity, accession, specimen condition, custody event, test-method version, duplicate result, amendment reason, reviewer separation, exotic-disease escalation, matched budget, blind arm label, workload, and next-shift ownership",
        "Synthetic traces can expose accession, custody, amendment, escalation, and handover failures while preserving every animal, client, worker, professional, biosecurity, and effectiveness gate.",
        "A fixture contains a real animal, client, farm, worker, specimen, or result; decides diagnosis or notification; breaks matched budgets or blinding; omits workload monitoring; or claims THOS effectiveness or veterinary competence.",
        "safe_now_proxy_protocol_no_people_or_animals",
        "x2_proxy_protocol",
        ["V6465-S09", "V6465-S10", "V6465-S11"],
        ["thos/veterinary-lab-handover-contract.json", "thos/veterinary-lab-proxy-vectors.json"],
        "Unsafe synthetic traces must fail, and the packet must record zero real animals, clients, farms, workers, laboratories, specimens, diagnoses, notifications, blind real arms, safety events, and effectiveness estimates.",
        "Withdraw operational language, retain rejected traces, and defer real workflow decisions to authorized veterinary, laboratory, worker, client, biosecurity, legal, Māori, and independent-review processes.",
        ["real_animals", "real_participants", "professional_authority", "biosecurity_decision", "deployment", "effectiveness"],
        "represented",
        "No frozen proposal centers veterinary diagnostic-laboratory accession, amended results, exotic-disease escalation, and matched-budget shift handover as one THOS proxy.",
    ),
    proposal(
        5,
        "Freed ID OpenID4VP transaction-data, credential-ID, and holder-binding profile",
        "transaction-data type, collision-resistant identifier, DCQL credential IDs, recognized type, holder-binding requirement, nonce and client binding, hash algorithm, processed-data claim, response encryption, minimization, and refusal",
        "Synthetic vectors can enforce OpenID4VP transaction-data and credential-query binding without asserting a real wallet, credential, transaction authorization, or cryptographic assurance.",
        "An unknown type passes, credential IDs are unbound, multiple credentials are silently used, holder binding is disabled, nonce or client binding drifts, transaction data is over-disclosed, or synthetic bytes become production assurance.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["V6465-S12", "V6465-S13"],
        ["freed-id/transaction-data-profile.json", "freed-id/transaction-data-mutations.json"],
        "Vectors must reject unknown types, empty or mismatched credential IDs, disabled holder binding, nonce or client drift, unsupported hash algorithms, response leakage, and unsupported authorization claims while recording zero real keys, credentials, wallets, or transactions.",
        "Reject the synthetic request, retain the vector, disclose no real identity or transaction data, and require conforming real keys, credentials, wallet and verifier flows, privacy/security review, interoperability, recovery, and trust governance.",
        ["real_keys", "real_credentials", "transaction_authority", "interoperability", "production", "privacy_complete", "security_certification"],
        "represented",
        "Prior Freed ID work covers OpenID4VP request objects, DCQL, Digital Credentials API, presentation binding, status, and batch issuance; none centers final-spec transaction_data credential-ID and cryptographic-holder-binding semantics.",
    ),
    proposal(
        6,
        "CBR exotic-animal-disease notification, farm privacy, response, remedy, and Māori-authority matrix",
        "suspected exotic disease, laboratory result, notification duty, farm and client privacy, animal welfare, worker safety, movement or response action, trade impact, public communication, remedy, data governance, legal interpretation, affected parties, and Māori authority",
        "A refusal-first matrix can expose unresolved notification, privacy, response, remedy, and authority questions without deciding a real disease, farm, laboratory, animal, or response case.",
        "The matrix contains real protected data, diagnoses or notifies a disease, orders movement controls, identifies a farm, allocates remedy, interprets law, asserts cultural or Māori authority, or treats software as emergency or public authority.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["V6465-S09", "V6465-S10", "V6465-S14"],
        ["cbr/animal-disease-authority-reservation.json", "cbr/notification-privacy-remedy-matrix.md"],
        "Repository software must stop at unknown or reserved; only competent veterinary, laboratory, biosecurity, animal-welfare, worker-safety, privacy, legal, emergency, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their gates.",
        "Stop before diagnosis, notification, control, disclosure, communication, or remedy conclusions; minimize data and route only through authorized external processes.",
        ["biosecurity_authority", "emergency_authority", "affected_party_authority", "privacy", "legal_interpretation", "cultural_ratification", "maori_authority", "remedy_decision"],
        "exact_gate",
        "Earlier CBR gates cover water notices, medicine recalls, aviation evidence, electricity care, earthquakes, fisheries, and archives; none centers exotic animal disease, farm privacy, response action, and Māori authority.",
    ),
    proposal(
        7,
        "Git reftable header, update-index, stack-order, compaction, and reflog tribunal",
        "REFT magic, format version, hash identifier, block size, minimum and maximum update index, footer CRC, ref uniqueness, log reverse ordering, tables-list stack, deletion records, compaction, and disposable confinement",
        "A disposable parser and fixture tribunal can validate selected reftable invariants and reject corrupt or misordered stacks without touching the canonical repository.",
        "Bad magic, version, update bounds, CRC, duplicate keys, reversed stack order, malformed deletion, or unconfined fixture passes, or bounded checks become exhaustive Git security assurance.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["V6465-S15", "V6465-S16"],
        ["security/reftable-contract.json", "security/reftable-mutation-vectors.json"],
        "Disposable fixtures must cover header and footer integrity, update-index ranges, unique keys, reverse reflog ordering, stack order, deletion and compaction semantics, cleanup, and canonical-repository nonmutation.",
        "Discard only the disposable fixture, retain the failed vector, and keep production, compatibility, supply-chain, and exhaustive-security claims false.",
        ["canonical_repository", "sibling_lane", "destructive_filesystem", "production", "exhaustive_security"],
        "completed",
        "Earlier Git tribunals cover MIDX, commit graphs, bundles, alternates, replacement refs, promisor objects, config, and object formats; none centers reftable update-index and stack/reflog invariants.",
    ),
    proposal(
        8,
        "HTML popover target, mode, light-dismiss, reading-order, and focus structural audit",
        "popover state, auto manual and hint modes, popovertarget, target action, same-tree relation, trigger, close request, light dismiss, top layer, reading order, accessible name, focus declaration, and manual evaluation reservation",
        "A structural auditor can reject malformed popover relationships and mode assumptions while reserving runtime pointer, keyboard, browser, assistive-technology, and affected-user evaluation.",
        "A broken target passes, manual mode is called light-dismissible, hint and auto stacks are conflated, a tooltip substitutes for interactive content, reading order or focus is inferred, or structural evidence becomes complete accessibility.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6465-S17", "V6465-S18", "V6465-S19"],
        ["accessibility/popover-contract.json", "accessibility/popover-structural-mutations.json"],
        "Positive and negative fixtures must cover modes, target/action validity, same-tree binding, close and light-dismiss expectations, reading order, accessible naming, focus declarations, tooltip non-substitution, and explicit manual reservations.",
        "Mark the structure incomplete, retain failures, restore native relationships and a visible close path, and require qualified manual browser, keyboard, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation.",
        ["accessibility_complete", "runtime_focus_behavior", "manual_keyboard_evaluation", "assistive_technology", "affected_user_acceptance"],
        "completed",
        "Earlier accessibility proposals cover dialogs, live regions, forms, tables, details, inertness, focus traps, and tooltips only indirectly; none centers native popover modes, target binding, and light-dismiss semantics.",
    ),
    proposal(
        9,
        "Thermo/Psyche Clapeyron coexistence-slope, latent-heat, and psyche-transition nonconversion classifier",
        "two-phase coexistence, pressure-temperature slope, entropy change, enthalpy or latent heat, molar volume change, units, sign, first-order domain, critical endpoint, approximation status, and category barrier",
        "A typed classifier can check a declared Clapeyron relation inside its thermodynamic domain while rejecting conversion of phase-transition language into human, social, psyche, justice, or consciousness claims.",
        "The phases are undeclared, units or signs drift, a zero volume change is divided through, a critical endpoint is crossed, a Clausius approximation is mislabeled exact, or transition language becomes participant or psyche evidence.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["V6465-S20", "V6465-S21"],
        ["thermo-psyche/clapeyron-contract.json", "thermo-psyche/clapeyron-mutation-vectors.json"],
        "Fixtures must enforce phase identity, coexistence, slope equals entropy over volume change or latent heat over temperature-volume change, units, signs, nonzero denominators, critical-domain refusal, approximation labels, and the psyche category barrier.",
        "Restore thermodynamic labels and domain assumptions, retain the rejection, and require independently valid human theory and participant evidence before any cross-domain hypothesis.",
        ["participant_inference", "psyche_claim", "social_transition_claim", "consciousness", "fundamental_law"],
        "completed",
        "The chain covers Gibbs-Duhem, Maxwell relations, Onsager, Crooks, Clausius cycles, Landauer, and phase-transition analogies; no prior title centers the Clapeyron coexistence slope and critical-domain refusal.",
    ),
    proposal(
        10,
        "Stage 20 metric-version, label-order, score-direction, and confusion-matrix nonpromotion board",
        "metric identifier and version, label vocabulary and order, positive class, score direction, averaging rule, threshold, confusion-matrix orientation, missing class, uncertainty target, comparison scope, and terminal abstention",
        "A fail-closed board can quarantine evaluation credit when metric semantics, label order, score direction, or confusion-matrix orientation drift between runs.",
        "A metric version changes silently, labels are permuted, positive class or score direction flips, averaging rules differ, missing classes disappear, uncertainty is unspecified, or a corrected score promotes Stage 20.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6465-S22", "V6465-S23"],
        ["stage20/metric-semantics-contract.json", "stage20/metric-semantics-mutations.json"],
        "Mutations must reject version drift, label permutation, positive-class inversion, score-direction reversal, averaging or threshold changes, matrix transposition, missing classes, unsupported uncertainty, and Stage 20 promotion.",
        "Withdraw only affected evidence credit, retain both metric definitions and matrices, freeze comparisons, require governed re-evaluation, and abstain.",
        ["stage20", "benchmark_authority", "independent_reproduction", "deployment", "proof_or_canon", "exhaustive_validation"],
        "completed",
        "Earlier Stage 20 boards cover contamination, optional stopping, environment locks, preregistration, independence, controls, and multiplicity; none centers metric-version and label-orientation semantic drift.",
    ),
]


SOURCES = [
    {"source_id":"V6465-S01","status":"current","title":"GHC Family Method Flow State schema and runner","authority":"family-current local skill","url":None,"checked_on":"2026-07-16","use":"append-only conflict, witness, recovery, rollback, and recurrence-guard requirements"},
    {"source_id":"V6465-S02","status":"current","title":"GHC Family Index routing and closeout guidance","authority":"family-current local skill","url":None,"checked_on":"2026-07-16","use":"source precedence, ownership, x1/x2 separation, truth labels, route state, and closeout"},
    {"source_id":"V6465-S03","status":"stable","title":"On Covariant Poisson Brackets in Classical Field Theory","authority":"Forger and Salles primary research","url":"https://arxiv.org/abs/1501.03780","checked_on":"2026-07-16","use":"Peierls-DeWitt bracket and functional-observable context only"},
    {"source_id":"V6465-S04","status":"stable","title":"Covariant phase space, constraints, gauge and the Peierls formula","authority":"Khavkine primary research","url":"https://arxiv.org/abs/1402.1282","checked_on":"2026-07-16","use":"gauge, support, Green-function, and covariant-phase-space obligations only"},
    {"source_id":"V6465-S05","status":"current","title":"Rubin Data Preview 1 overview","authority":"Vera C. Rubin Observatory","url":"https://dp1.lsst.io/overview/index.html","checked_on":"2026-07-16","use":"official DP1 scope and commissioning provenance; zero access or rows"},
    {"source_id":"V6465-S06","status":"current","title":"Rubin DP1 catalogs","authority":"Vera C. Rubin Observatory","url":"https://dp1.lsst.io/products/catalogs/index.html","checked_on":"2026-07-16","use":"catalog and field inventory only; zero ingestion"},
    {"source_id":"V6465-S07","status":"watch","title":"Rubin DP1 known issues and subtleties","authority":"Vera C. Rubin Observatory","url":"https://dp1.lsst.io/products/known_issues_and_subtleties.html","checked_on":"2026-07-16","use":"shape, calibration, uncertainty, and version limitations; no result adoption"},
    {"source_id":"V6465-S08","status":"current","title":"Rubin DP1 data access","authority":"Vera C. Rubin Observatory","url":"https://dp1.lsst.io/access/index.html","checked_on":"2026-07-16","use":"data-rights account boundary; no account or protected access used"},
    {"source_id":"V6465-S09","status":"current","title":"Surveillance for veterinary professionals","authority":"New Zealand Ministry for Primary Industries","url":"https://www.mpi.govt.nz/biosecurity/how-to-find-report-and-prevent-pests-and-diseases/surveillance-for-veterinary-professionals","checked_on":"2026-07-16","use":"laboratory-submission and reporting context; no diagnosis, report, or authority exercised"},
    {"source_id":"V6465-S10","status":"current","title":"Report a pest or disease","authority":"New Zealand Ministry for Primary Industries","url":"https://www.mpi.govt.nz/biosecurity/how-to-find-report-and-prevent-pests-and-diseases/report-a-pest-or-disease","checked_on":"2026-07-16","use":"official notification boundary; legal interpretation and real reporting reserved"},
    {"source_id":"V6465-S11","status":"current","title":"Veterinary Code changes under the care","authority":"Veterinary Council of New Zealand","url":"https://www.vetcouncil.org.nz/Web/3.About/Current%20Projects/Under-the-care-of-a-veterinarian.aspx","checked_on":"2026-07-16","use":"current professional-role context only; no competence or authority claimed"},
    {"source_id":"V6465-S12","status":"current","title":"OpenID for Verifiable Presentations 1.0","authority":"OpenID Foundation","url":"https://openid.net/specs/openid-4-verifiable-presentations-1_0.html","checked_on":"2026-07-16","use":"transaction_data, credential IDs, holder binding, nonce, client, and response rules"},
    {"source_id":"V6465-S13","status":"current","title":"Formal Security Analysis of OpenID for Verifiable Presentations","authority":"OpenID Foundation commissioned analysis","url":"https://openid.net/wp-content/uploads/2025/08/Report-Deliverable-A_1_B_.pdf","checked_on":"2026-07-16","use":"security-boundary context only; no production assurance"},
    {"source_id":"V6465-S14","status":"stable","title":"Principles of Māori Data Sovereignty","authority":"Te Mana Raraunga Māori Data Sovereignty Network","url":"https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty","checked_on":"2026-07-16","use":"Māori data-governance and authority reservation; never delegated authority"},
    {"source_id":"V6465-S15","status":"current","title":"Git reftable documentation","authority":"Git project","url":"https://git-scm.com/docs/reftable","checked_on":"2026-07-16","use":"format, blocks, update indices, log order, footer, and stack semantics"},
    {"source_id":"V6465-S16","status":"current","title":"Git refs verification documentation","authority":"Git project","url":"https://git-scm.com/docs/git-refs","checked_on":"2026-07-16","use":"reference backend verification and compatibility context"},
    {"source_id":"V6465-S17","status":"current","title":"HTML Standard popover model","authority":"WHATWG","url":"https://html.spec.whatwg.org/multipage/popover.html","checked_on":"2026-07-16","use":"popover modes, targets, top-layer, close, reading-order, and light-dismiss structure"},
    {"source_id":"V6465-S18","status":"stable","title":"Accessible Rich Internet Applications 1.2","authority":"World Wide Web Consortium","url":"https://www.w3.org/TR/wai-aria/","checked_on":"2026-07-16","use":"popup role and focus relationship context; tooltip non-substitution"},
    {"source_id":"V6465-S19","status":"stable","title":"Web Content Accessibility Guidelines 2.2","authority":"World Wide Web Consortium","url":"https://www.w3.org/TR/WCAG22/","checked_on":"2026-07-16","use":"accessibility context while manual and complete-conformance claims remain reserved"},
    {"source_id":"V6465-S20","status":"stable","title":"Melting Is Well-Known, but Is It Also Well-Understood?","authority":"Müller and collaborators primary review","url":"https://doi.org/10.1021/acs.chemrev.3c00489","checked_on":"2026-07-16","use":"Clapeyron coexistence and domain context only"},
    {"source_id":"V6465-S21","status":"current","title":"NIST Thermodynamics research","authority":"United States National Institute of Standards and Technology","url":"https://www.nist.gov/thermodynamics","checked_on":"2026-07-16","use":"thermodynamic measurement context; no psyche conversion"},
    {"source_id":"V6465-S22","status":"current","title":"NIST AI 800-3 evaluation statistical models report","authority":"United States National Institute of Standards and Technology","url":"https://www.nist.gov/news-events/news/2026/02/new-report-expanding-ai-evaluation-toolbox-statistical-models","checked_on":"2026-07-16","use":"explicit estimand, uncertainty, and metric-definition context"},
    {"source_id":"V6465-S23","status":"current","title":"NIST AI RMF Measure playbook","authority":"United States National Institute of Standards and Technology","url":"https://airc.nist.gov/airmf-resources/playbook/measure/","checked_on":"2026-07-16","use":"metric selection, limitation, and nonmeasurement documentation context"},
]


SAFE_TITLES = [
    "Tamar exact source-head four-way equality gate", "Tamar frozen 430-proposal count and identifier audit",
    "Tamar baton-time and post-baton negative reconciliation", "Tamar x1 companion immutability boundary",
    "Tamar current source-status and watch audit", "Tamar successor-scoped test exclusion allowlist guard",
    "Tamar exact staged Git-blob review", "Tamar five-class candidate-versus-confirmed privacy separator",
    "Tamar commit-cap and single-parent proof", "Tamar owner-footprint rotation threshold receipt",
    "Tamar manual accessibility reservation lint", "Tamar protected-packet nonexecution audit",
    "Tamar one-shot terminal-route state guard", "Tamar UTF-8 JSON and LF document guard",
    "Tamar Method Flow append-only state validation", "Tamar compare-and-swap revision preflight",
    "Tamar lost-update mutation rejection", "Tamar Peierls causal-support obligation lint",
    "Tamar Rubin DP1 zero-row invariant", "Tamar veterinary zero-animal and zero-specimen boundary invariant",
    "Tamar OpenID transaction-data credential-ID binding lint", "Tamar biosecurity authority vocabulary gate",
    "Tamar reftable header-footer integrity preflight", "Tamar reftable stack-order and update-index audit",
    "Tamar popover target and light-dismiss structural check", "Tamar Clapeyron units and domain classifier",
    "Tamar metric label-order and score-direction lock", "Tamar citation-to-observation nonconversion guard",
    "Tamar named validation lane locality preflight", "Tamar post-final external-negative carry-forward guard",
]

CANDIDATE_TITLES = [
    "Optimistic-concurrency evidence-credit prototype", "Peierls gauge-observable obligation board",
    "Rubin DP1 shear-readiness zero-row adapter", "Veterinary laboratory handover proxy",
    "OpenID4VP transaction-data synthetic profile", "Exotic-animal-disease authority matrix",
    "Git reftable disposable tribunal", "HTML popover structural auditor",
    "Clapeyron domain nonconversion classifier", "Metric-semantics Stage 20 board",
    "Conflict-rebase write-set mutation simulator", "Peierls advanced-retarded support mutation set",
    "Rubin calibration-issue provenance lock", "Veterinary amended-result ownership state machine",
    "Transaction-data hash and response-leakage fixture", "Farm-privacy minimization refusal matrix",
    "Reftable reflog reverse-order and compaction fixture", "Popover mode and target-action mutation set",
    "Critical-endpoint and latent-heat sign fixture", "Confusion-matrix orientation and averaging-rule fixture",
]

SKILLS = [
    ("ghc-family-optimistic-concurrency-credit", "Refuse stale-revision evidence writes and preserve conflict receipts."),
    ("ghc-family-conflict-rebase-guard", "Bound rebases to reviewed write sets and protected intent."),
    ("ghc-family-peierls-obligations", "Audit Peierls Green-function, support, gauge, and bracket obligations."),
    ("ghc-family-rubin-dp1-zero-row", "Describe Rubin DP1 while enforcing zero access, rows, and likelihood."),
    ("ghc-family-veterinary-handover-proxy", "Validate synthetic accession, amendment, escalation, and handover traces."),
    ("ghc-family-openid4vp-transaction-data", "Validate synthetic transaction-data and credential-ID binding."),
    ("ghc-family-animal-disease-authority", "Reserve veterinary, biosecurity, privacy, remedy, legal, and Māori authority."),
    ("ghc-family-reftable-tribunal", "Validate bounded reftable headers, update indices, stacks, logs, and CRC fixtures."),
    ("ghc-family-popover-structure", "Audit popover modes, targets, light dismiss, reading order, and reservations."),
    ("ghc-family-clapeyron-domain", "Check Clapeyron units and domain while blocking psyche conversion."),
    ("ghc-family-metric-semantics-lock", "Bind metric versions, labels, score direction, averaging, and matrix orientation."),
    ("ghc-family-x1-companion-immutability", "Keep frozen x1 credit separate from later companion artifacts."),
    ("ghc-family-external-negative-reconcile", "Separate sealed, baton-time, post-baton, and current negative totals."),
    ("ghc-family-source-citation-observation-barrier", "Keep source status and citations separate from observation credit."),
    ("ghc-family-staged-blob-self-exclusion", "Review staged Git blobs with explicit self-excluding manifest domains."),
    ("ghc-family-tamar-footprint-threshold", "Apply rotation only to the current Tamar-generated addition."),
    ("ghc-family-validation-lane-no-upstream", "Prove the sole named validation lane has no upstream or remote ref."),
    ("ghc-family-single-parent-phase-budget", "Bind source ancestry, parent count, zero merges, and phase-commit budget."),
    ("ghc-family-static-report-reservations", "Separate structural accessibility from manual and affected-user evaluation."),
    ("ghc-family-existing-task-one-shot-baton", "Keep route prepared until one acknowledged existing-task delivery."),
]

RUNNERS = [
    ("ghc_family_v646_v5_runtime.py", "Execute bounded core surface fixtures."),
    ("ghc_family_v646_v5_core_runner.py", "Invoke and summarize all ten frozen core surfaces."),
    ("ghc_family_v646_v5_portfolio_runner.py", "Execute thirty safe, twenty candidate, and thirty cleanup tasks."),
    ("ghc_family_v646_v5_skill_runner.py", "Build, validate, and smoke-use twenty phase-local skills."),
    ("ghc_family_v646_v5_staged_review.py", "Review exact staged paths, privacy classes, JSON, and manifests."),
    ("ghc_family_v646_v5_validation_runner.py", "Run current, eligible scoped, detailed, minimal, JSON, and privacy checks."),
    ("ghc_family_v646_v5_optimistic_concurrency.py", "Run compare-and-swap and lost-update fixtures."),
    ("ghc_family_v646_v5_reftable_tribunal.py", "Run disposable reftable format and stack fixtures."),
    ("ghc_family_v646_v5_source_gate.py", "Check source status, zero-row, proxy, and authority boundaries."),
    ("ghc_family_v646_v5_named_lane_audit.py", "Verify exact-head local-only named-lane conditions."),
]

CLEAN_TITLES = [
    "Reconcile 2799 baton and one post-baton inherited negative", "Synchronize 430-to-440 proposal counts",
    "Preserve exact x1 paths across x2", "Map v646-v5 callers to current and compatibility surfaces",
    "Constrain v646-v5 cleanup to Tamar-owned generated paths", "Canonicalize v646-v5 JSON with deterministic UTF-8 key order",
    "Preserve te reo Māori diacritics with authority reservations", "Test v646-v5 report overflow without claiming responsive conformance",
    "Declare evidence and final manifest lifecycle membership", "Treat absent named-lane remote output as expected empty state",
    "Prove v646-v5 validation branch local-only without deletion", "Bind v646-v5 commit cap to source and parent count",
    "Re-audit inherited exact and blocked packet nonexecution", "Publish phase-local index and Method Flow successor recommendations",
    "Label canonical plus replay as same-owner shared-infrastructure evidence", "Record full-checkout and owner counts separately",
    "Keep Rubin access metadata separate from observations", "Keep veterinary fixtures free of real protected data",
    "Keep transaction data synthetic and minimized", "Reserve biosecurity and notification decisions",
    "Keep reftable fixture teardown inside disposable root", "Compare reftable stack order without canonical mutation",
    "Associate every popover with an exact target", "Reserve manual browser and assistive evaluation",
    "Require declared Clapeyron phases and units", "Retain critical-domain refusals",
    "Freeze metric labels and score direction", "Retain both matrices on semantic divergence",
    "Preserve post-final faults after cap seals", "Keep terminal route state prepared until acknowledgement",
]


def support_item(prefix: str, index: int, title: str, approval_class: str) -> dict[str, Any]:
    return {
        "packet_id": f"V6465-{prefix}-{index:02d}",
        "title": title,
        "owner": OWNER,
        "origin": "tamar_new_x1_after_430_surface_audit",
        "approval_class": approval_class,
        "hypothesis": f"A bounded owner-scoped implementation of {title.lower()} can produce auditable structural evidence without crossing protected gates.",
        "null_or_failure": "The artifact is absent, privacy is crossed, a structural result is overstated, a failure is erased, or a protected gate is silently closed.",
        "acceptance_gate": "The x2 artifact, bounded witness, privacy-safe receipt, and caller-compatibility check must pass before completion credit.",
        "rollback_or_recovery": "Retain the negative, restore the last validated owner-scoped state, and leave unavailable evidence or authority explicitly open.",
        "protected_gates": ["authority", "real_data_or_participants", "production", "sibling_lane", "independent_reproduction", "stage20"],
        "x1_state": "preregistered_no_completion_credit",
    }


SAFE_NOW = [support_item("SAFE", i, title, "safe_now_owner_scoped_structural") for i, title in enumerate(SAFE_TITLES, 1)]
CANDIDATES = [support_item("CAND", i, title, "candidate_bounded_prototype") for i, title in enumerate(CANDIDATE_TITLES, 1)]
CLEAN_TASKS = [support_item("CLEAN", i, title, "safe_now_owner_scoped_additive_cleanup") for i, title in enumerate(CLEAN_TITLES, 1)]
