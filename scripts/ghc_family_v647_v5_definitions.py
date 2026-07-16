#!/usr/bin/env python3
"""Frozen x1 definitions for Eiren Kestrel v647-v5.

Importing this module performs no I/O and grants no x2 completion credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v647-gmut-thos-v5-x1-x2"
PHASE_SHORT = "v647-v5"
OWNER = "Eiren Kestrel"
SLUG = "eiren-kestrel"
PRONOUNS = "they/them"
ROLE = "evidence-integrity weaver"
HOPE = "make ambitious claims easier to test, correct, and keep within evidence and authority boundaries"
PRIMARY_FOCUS = "Freed ID/CBR Heart"
BOUNDED_PRACTICE = "public-library digital-access incident triage, accessible fallback, privacy preservation, and shift handover"

SOURCE_PHASE = "v647-gmut-thos-v4-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
SOURCE_REVISION = "1395f18ab6504485448eb8e4d507f94ac066caf4"
SOURCE_INHERITED_REVISION = "616286381002d913846ab01e48c9f1063b661c72"
SOURCE_X1_REVISION = "5e5bc09f5173c00c7674b7868e3c7e5e8af80053"
SOURCE_EVIDENCE_REVISION = "cf2735f20be97882c03fa562bc0a7e99c3aa240f"
SOURCE_SEAL_REVISION = SOURCE_REVISION
PRIOR_FROZEN_PROPOSALS = 510
INHERITED_EFFECTIVE_NEGATIVES = 3493
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 21
INHERITED_EXACT_GATES = 22
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, is relational working language for an evidence-integrity weaver. "
    "It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "professional qualification, scientific authority, operational authority, legal authority, cultural authority, "
    "or independent agency. Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; Freed ID "
    "remains synthetic and nonproduction; CBR, library access, privacy, disability, children, legal, cultural, "
    "affected-party, and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, and "
    "Māori authority. No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, "
    "deployment, privacy-complete, exhaustive-security, independent-reproduction, accessibility-complete, "
    "professional, proof or canon, or Stage 20 claim is made."
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
        "proposal_id": f"V6475-P{index:02d}",
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
        "novelty_against_510_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Method Flow bounded-priority admission, backpressure, high-watermark, starvation, cancellation, and evidence-credit tribunal",
        "bounded queue, priority, admission capacity, high and low watermarks, backpressure, fairness age, starvation limit, cancellation, drain, and evidence credit",
        "A deterministic owner-local queue can refuse overload, bound priority bypass, preserve cancellation, and withhold evidence credit until admitted work reaches an explicit terminal state.",
        "Capacity is exceeded, a lower-priority item starves beyond its bound, cancelled work executes, watermarks regress, drain loses an item, or admission alone earns completion credit.",
        "safe_now_owner_scoped_workflow",
        "x2_build_task",
        ["V6475-S01", "V6475-S02"],
        ["method-flow/priority-backpressure-contract.json", "method-flow/priority-backpressure-mutations.json"],
        "Synthetic traces must reject overflow, priority inversion, starvation, cancelled execution, watermark regression, and premature evidence credit with zero external side effects.",
        "Quarantine the bounded queue state, retain the failing trace, reduce the admission surface, replay from the last explicit terminal item, and keep production scheduling claims false.",
        ["external_state", "production_scheduler", "distributed_consensus", "real_process_control", "sibling_lane", "completion_credit"],
        "completed",
        "Earlier proposals cover durable outboxes, resumable checkpoints, append-only logs, leases, fencing tokens, and process teardown; none centers bounded priority admission, backpressure watermarks, starvation limits, and cancellation credit together.",
    ),
    proposal(
        2,
        "GMUT ADM Hamiltonian, momentum-constraint, lapse-shift, boundary-term, and hypersurface-deformation obligation board",
        "spatial metric, conjugate momentum, lapse, shift, Hamiltonian constraint, momentum constraint, Poisson bracket, structure function, boundary term, gauge role, unit domain, and EFT reservation",
        "A typed symbolic board can expose ADM canonical and constraint-closure obligations for a GMUT research model without claiming a solved constraint algebra, physical state, stability theorem, or quantum completion.",
        "Lapse or shift becomes a physical observable, a boundary term disappears, structure functions become constants, constraints close by assertion, units drift, or symbolic consistency becomes empirical or Theory-of-Everything proof.",
        "safe_now_symbolic_research_only",
        "x2_build_task",
        ["V6475-S03", "V6475-S04"],
        ["gmut/adm-constraint-obligations.json", "gmut/adm-constraint-mutations.json"],
        "Positive and negative fixtures must type canonical variables, lapse and shift, both constraints, bracket domain, boundary assumptions, structure functions, units, truncation, and nonpromotion boundaries.",
        "Retain the failed obligation, reopen the canonical map and boundary assumptions, restore unit and gauge bookkeeping, and make no force, prediction, constraint, stability, quantum-completion, or Theory-of-Everything claim.",
        ["constraint_solution", "physical_state", "stability_proof", "quantum_completion", "empirical_confirmation", "theory_of_everything"],
        "completed",
        "The frozen corpus covers gauge fixing, BRST, BV, Schwinger-Dyson, 2PI, heat-kernel, and functional-RG obligations but has no proposal centered on ADM lapse-shift constraints, hypersurface-deformation brackets, and boundary terms.",
    ),
    proposal(
        3,
        "GMUT Pantheon+ supernova distance, covariance, selection, calibration, and zero-row likelihood-refusal protocol",
        "release identity, supernova identifier schema, redshift frame, distance modulus, covariance product, calibration provenance, selection correction, duplicate handling, nuisance lock, checksum, and zero-row likelihood refusal",
        "A zero-row adapter can freeze official Pantheon+ release and covariance obligations while refusing to turn release documentation or published cosmology into GMUT observations, likelihoods, or constraints.",
        "The phase queries or downloads rows, copies a published estimate as an observation, fabricates covariance, mixes redshift frames, evaluates a likelihood, samples a posterior, or emits a GMUT force or parameter constraint.",
        "real_data_access_and_independent_review_required",
        "x2_open_gap",
        ["V6475-S05", "V6475-S06"],
        ["empirical/pantheon-plus-study-contract.json", "empirical/pantheon-plus-zero-row-receipt.json"],
        "The receipt must preserve zero archive queries, downloads, real rows, covariance rows, likelihood calls, posterior samples, parameter constraints, detected-force claims, and empirical GMUT claims.",
        "Stop before data access or fitting, retain the zero-row receipt, and require a separately authorized preregistration with frozen release, masks, covariance, calibration, selection, nuisance model, baselines, uncertainty analysis, and independent review.",
        ["network_data_access", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation", "independent_review"],
        "open_gap",
        "Prior adapters cover BAO, CMB, weak lensing, gravitational waves, pulsars, clusters, FRBs, neutrinos, and several distance probes; none centers the Pantheon+ supernova distance and covariance release.",
    ),
    proposal(
        4,
        "THOS public-library digital-access outage, queue, privacy, accessible-fallback, and shift-handover proxy",
        "synthetic service identifier, outage status, digital-platform dependency, queue age, privacy minimum, accessible fallback, language need, child-safety reservation, escalation, workload budget, readback, and next-shift owner",
        "Synthetic traces can expose stale outage state, unowned queues, privacy overcollection, inaccessible fallback, and handover loss while preserving every patron, worker, institution, professional, and effectiveness gate.",
        "A fixture contains a real patron, child, worker, account, borrowing record, search history, protected need, or live service; changes a real system; breaks matched budgets; or claims THOS effectiveness or library competence.",
        "safe_now_proxy_protocol_no_people_or_operations",
        "x2_proxy_protocol",
        ["V6475-S07", "V6475-S08", "V6475-S09"],
        ["thos/library-digital-handover-contract.json", "thos/library-digital-handover-vectors.json"],
        "Unsafe synthetic traces must fail, and the packet must record zero real people, accounts, borrowing or search records, institutions, outages, operational decisions, blind real arms, outcomes, and effectiveness estimates.",
        "Withdraw operational language, retain rejected traces, minimize every synthetic field, and defer real decisions to authorized library, privacy, accessibility, safeguarding, affected-party, legal, cultural, and Māori processes.",
        ["real_people", "real_library_records", "professional_authority", "live_service", "deployment", "privacy_complete", "effectiveness"],
        "represented",
        "No frozen title centers a public-library digital-access outage, patron queue, privacy minimization, accessible fallback, and shift handover as one bounded THOS proxy.",
    ),
    proposal(
        5,
        "Freed ID OAuth PAR client-binding, request_uri expiry, single-use, parameter-consistency, and replay profile",
        "pushed authorization endpoint, authenticated client, request object, request_uri, expires_in, client binding, parameter consistency, redirect URI, single use, replay, policy change, and refusal",
        "Synthetic vectors can enforce selected RFC 9126 PAR structure, binding, expiry, and replay obligations without asserting real authorization, consent, tokens, interoperability, or production identity assurance.",
        "An unauthenticated client passes, request_uri is transferable, expiry is ignored, front-channel parameters override pushed content, replay succeeds, policy change is hidden, or synthetic bytes become authorization evidence.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["V6475-S10", "V6475-S11"],
        ["freed-id/oauth-par-profile.json", "freed-id/oauth-par-mutations.json"],
        "Vectors must reject missing client binding, expired or replayed request_uri values, parameter substitution, redirect mismatch, policy drift, and production promotion while recording zero real clients, users, keys, tokens, or grants.",
        "Reject the synthetic request, retain the vector, disclose no real identity or authorization data, and require conforming clients, authorization servers, consent, interoperability, privacy and security review, recovery, and trust governance.",
        ["real_identity", "real_authorization", "real_keys", "real_tokens", "consent", "interoperability", "production"],
        "represented",
        "The corpus includes JAR, RAR, DPoP, federation, WebAuthn, VC, SCITT, and credential-flow profiles but no proposal centered on PAR client binding, request_uri expiry and single use, parameter consistency, and replay refusal.",
    ),
    proposal(
        6,
        "CBR public-library access, privacy, children, disability, digital-exclusion remedy, and Māori-authority matrix",
        "library access, digital exclusion, disability access, child and youth safeguarding, search and borrowing privacy, third-party platform, language access, community notice, remedy, appeal, legal interpretation, affected parties, data governance, and Māori authority",
        "A refusal-first matrix can expose unresolved access, privacy, safeguarding, disability, digital-exclusion, remedy, and authority questions without deciding a real right, disclosure, service entitlement, cultural wording, or remedy.",
        "The matrix identifies a real patron or worker, discloses records, determines a child-safety case, decides access or legal rights, allocates remedy, asserts cultural or Māori authority, or treats public guidance as delegated case authority.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["V6475-S07", "V6475-S08", "V6475-S12", "V6475-S13"],
        ["cbr/library-authority-reservation.json", "cbr/library-remedy-matrix.json"],
        "Repository software must stop at unknown or reserved; only competent library, privacy, safeguarding, disability, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        "Stop before disclosure, service restriction, safeguarding, cultural, language, data-governance, legal, or remedy conclusions; minimize data and route only through authorized external processes.",
        ["affected_party_authority", "children", "disability_access", "privacy", "legal_interpretation", "maori_authority", "data_governance", "remedy_decision"],
        "exact_gate",
        "Earlier CBR matrices cover utilities, health, food, aviation, rail, wildfire, telecommunications, and wastewater; none centers public-library digital access, children, disability, patron privacy, exclusion remedy, and Māori authority together.",
    ),
    proposal(
        7,
        "Git protocol v2 capability, pkt-line, delimiter, response-end, ref-prefix, and fetch-boundary tribunal",
        "capability advertisement, command key, pkt-line length, flush packet, delimiter packet, response-end packet, ls-refs, ref-prefix, fetch argument, section order, size budget, and disposable confinement",
        "A disposable local parser tribunal can reject malformed or out-of-order protocol-v2 fixtures without making a network request or claiming production Git transport or exhaustive parser security.",
        "A malformed length passes, capability is used before advertisement, delimiter or response-end order is wrong, ref-prefix widens silently, fetch arguments cross sections, a budget is exceeded, or a fixture touches canonical or remote state.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["V6475-S14", "V6475-S15"],
        ["tooling/git-protocol-v2-contract.json", "tooling/git-protocol-v2-mutations.json"],
        "Disposable fixtures must cover valid advertisement and command flow plus malformed lengths, unexpected packets, unknown capabilities, section-order faults, ref-prefix widening, budget excess, cleanup, and canonical nonmutation.",
        "Discard only the disposable fixture, retain every framing and boundary discrepancy, restore a bounded parser state, and keep network, production, interoperability, and exhaustive-security claims false.",
        ["network_access", "canonical_evidence", "sibling_lane", "production_transport", "interoperability", "exhaustive_security"],
        "completed",
        "Prior Git tribunals cover worktrees, reftable, multi-pack indexes, bundles, sparse clones, and object reachability; none centers protocol-v2 capability advertisement and pkt-line section boundaries.",
    ),
    proposal(
        8,
        "Accessible sortable-table aria-sort, filter-state, result-count, focus, pagination, and print structural audit",
        "table caption, header association, sort control, aria-sort owner, filter label, active-filter summary, result count, empty state, focus retention, pagination, live update reservation, responsive fallback, and print order",
        "A structural auditor can reject contradictory sorting and filtering semantics while reserving manual keyboard, browser, assistive-technology, responsive, cognitive, language, and affected-user evaluation.",
        "Multiple headers claim aria-sort, visual and semantic order diverge, filters lack state or result count, focus is lost, pagination hides context, empty state is absent, or structural evidence becomes complete accessibility conformance.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6475-S16", "V6475-S17"],
        ["accessibility/sortable-table-contract.json", "accessibility/sortable-table-mutations.json"],
        "Positive and negative fixtures must cover captions, header association, single sort owner, filter and count state, empty result, focus plan, pagination context, responsive and print fallback, and explicit manual reservations.",
        "Mark the structure incomplete, retain failures, restore coherent sort and filter state and focus, and require qualified manual browser, assistive-technology, responsive, cognitive, Māori-language, and affected-user evaluation.",
        ["accessibility_complete", "runtime_browser", "assistive_technology", "responsive_evaluation", "maori_language", "affected_user_acceptance"],
        "completed",
        "The frozen corpus contains table-header linearization but no proposal centered on sortable-table aria-sort ownership, filter state, result count, focus retention, pagination, and print fallback together.",
    ),
    proposal(
        9,
        "Thermo/Psyche Helmholtz-energy minimum, fixed-temperature-volume, convexity, metastability, and agency-nonconversion classifier",
        "Helmholtz energy, internal energy, temperature, entropy, fixed volume, fixed temperature, equilibrium candidate, local minimum, convexity scope, metastability, phase boundary, units, and category barrier",
        "A typed classifier can check bounded Helmholtz-energy statements and equilibrium assumptions while rejecting conversion of thermodynamic minimization into human agency, preference, identity, justice, or consciousness claims.",
        "Temperature or volume is not fixed, units drift, a local minimum becomes a global theorem, metastability disappears, convexity scope is hidden, a phase boundary is ignored, or thermodynamic minimization becomes psyche evidence.",
        "safe_now_symbolic_only",
        "x2_build_task",
        ["V6475-S18"],
        ["thermo-psyche/helmholtz-domain-contract.json", "thermo-psyche/helmholtz-domain-mutations.json"],
        "Fixtures must enforce A equals U minus TS, declared units and constraints, equilibrium and minimum scope, convexity assumptions, metastability reservation, phase-boundary refusal, and the psyche category barrier.",
        "Restore the physical thermodynamic domain and explicit constraints, retain the rejection, and require independently valid human theory, measures, authority, and participant evidence before any human inference.",
        ["participant_inference", "psyche_claim", "agency_claim", "preference_claim", "justice_claim", "consciousness", "fundamental_law"],
        "completed",
        "The chain covers entropy, Landauer, Jarzynski, Gibbs-Duhem, phase rule, Maxwell, Clausius-Clapeyron, Nernst, and Le Chatelier domains but no title centers Helmholtz minima, fixed T-V scope, convexity, and metastability.",
    ),
    proposal(
        10,
        "Stage 20 conformal-prediction exchangeability, calibration-split, marginal-coverage, subgroup, drift, and nonpromotion board",
        "prediction target, nonconformity score, training split, calibration split, test point, exchangeability, nominal alpha, finite-sample marginal coverage, conditional nonclaim, subgroup diagnostic, drift, seed, decision authority, and abstention",
        "A fail-closed structural board can quarantine promotion when exchangeability, split lineage, score definition, coverage target, subgroup behavior, drift, uncertainty, or decision authority is absent or changed after exposure.",
        "Exchangeability is asserted without evidence, calibration leaks into training, marginal coverage becomes conditional coverage, subgroup undercoverage is hidden, drift is ignored, a seed changes post hoc, or Stage 20 advances.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6475-S19", "V6475-S20"],
        ["stage20/conformal-prediction-contract.json", "stage20/conformal-prediction-mutations.json"],
        "Mutations must reject leakage, undefined scores, absent exchangeability scope, marginal-to-conditional promotion, hidden subgroup failures, unhandled drift, post-hoc seeds, unsupported deployment, and Stage 20 advancement.",
        "Withdraw affected evidence credit, retain the split, score, assumptions, failures, and drift record, require preregistered evaluation and governed criteria plus independent review, and abstain.",
        ["stage20", "participant_evidence", "conditional_coverage_claim", "deployment", "decision_authority", "independent_reproduction"],
        "completed",
        "Earlier Stage 20 boards cover multiplicity, optional stopping, target trials, negative controls, MNAR, decision curves, model comparison, and prequential drift; none centers conformal exchangeability, calibration splits, marginal coverage, subgroup diagnostics, and drift.",
    ),
]


SOURCES = [
    {"source_id": "V6475-S01", "title": "Python queue synchronized queue classes", "url": "https://docs.python.org/3/library/queue.html", "publisher": "Python Software Foundation", "status": "current", "source_class": "official_documentation", "use": "bounded queue and blocking vocabulary only"},
    {"source_id": "V6475-S02", "title": "Python asyncio queues", "url": "https://docs.python.org/3/library/asyncio-queue.html", "publisher": "Python Software Foundation", "status": "current", "source_class": "official_documentation", "use": "queue capacity and task-completion vocabulary only"},
    {"source_id": "V6475-S03", "title": "The Dynamics of General Relativity", "url": "https://arxiv.org/abs/gr-qc/0405109", "publisher": "Arnowitt, Deser, and Misner", "status": "stable", "source_class": "primary_research", "use": "ADM canonical and constraint provenance only"},
    {"source_id": "V6475-S04", "title": "3+1 Formalism and Bases of Numerical Relativity", "url": "https://arxiv.org/abs/gr-qc/0703035", "publisher": "Eric Gourgoulhon", "status": "stable", "source_class": "primary_research_lecture_notes", "use": "constraint and lapse-shift notation cross-check only"},
    {"source_id": "V6475-S05", "title": "Pantheon+SH0ES Data Release", "url": "https://github.com/PantheonPlusSH0ES/DataRelease", "publisher": "Pantheon+SH0ES collaboration", "status": "current", "source_class": "official_data_release_repository", "use": "zero-row release, schema, covariance, and calibration obligations only"},
    {"source_id": "V6475-S06", "title": "The Pantheon+ Analysis: Cosmological Constraints", "url": "https://doi.org/10.3847/1538-4357/ac8e04", "publisher": "The Astrophysical Journal", "status": "stable", "source_class": "primary_research", "use": "published analysis context only; no observation imported"},
    {"source_id": "V6475-S07", "title": "Public Libraries New Zealand statements of position", "url": "https://www.plnz.org.nz/statements-of-position/", "publisher": "Public Libraries New Zealand", "status": "current", "source_class": "sector_authority_guidance", "use": "synthetic access, safety, privacy, and inclusion vocabulary only"},
    {"source_id": "V6475-S08", "title": "Privacy Act 2020 privacy principles", "url": "https://www.privacy.org.nz/privacy-principles/", "publisher": "Office of the Privacy Commissioner New Zealand", "status": "current", "source_class": "official_guidance", "use": "privacy reservation and minimization context; no legal interpretation"},
    {"source_id": "V6475-S09", "title": "Digital inclusion stocktake", "url": "https://www.digital.govt.nz/dmsdocument/155-digital-inclusion-stocktake-what-digital-inclusion-looks-like-across-government", "publisher": "New Zealand Digital Government", "status": "stable", "source_class": "official_public_report", "use": "digital-inclusion and library context only"},
    {"source_id": "V6475-S10", "title": "RFC 9126 OAuth 2.0 Pushed Authorization Requests", "url": "https://www.rfc-editor.org/rfc/rfc9126.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "synthetic PAR structure, binding, expiry, and replay obligations"},
    {"source_id": "V6475-S11", "title": "RFC 9700 Best Current Practice for OAuth 2.0 Security", "url": "https://www.rfc-editor.org/rfc/rfc9700.html", "publisher": "IETF RFC Editor", "status": "current", "source_class": "official_standard", "use": "current security-context reservations only"},
    {"source_id": "V6475-S12", "title": "Principles of Māori Data Sovereignty", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "publisher": "Te Mana Raraunga", "status": "current", "source_class": "maori_authority_source", "use": "authority and data-governance gate; not delegated authority"},
    {"source_id": "V6475-S13", "title": "Māori and Indigenous Data Sovereignty Tools", "url": "https://www.temanararaunga.maori.nz/resource-hub-copy", "publisher": "Te Mana Raraunga", "status": "current", "source_class": "maori_authority_source", "use": "organizational readiness and authority reservation only"},
    {"source_id": "V6475-S14", "title": "Git Wire Protocol Version 2", "url": "https://git-scm.com/docs/gitprotocol-v2", "publisher": "Git project", "status": "current", "source_class": "official_documentation", "use": "capability, command, and section-framing syntax"},
    {"source_id": "V6475-S15", "title": "Git Pack Protocol", "url": "https://git-scm.com/docs/gitprotocol-pack", "publisher": "Git project", "status": "current", "source_class": "official_documentation", "use": "pkt-line and transport boundary vocabulary only"},
    {"source_id": "V6475-S16", "title": "Grid and Table Properties", "url": "https://www.w3.org/WAI/ARIA/apg/practices/grid-and-table-properties/", "publisher": "W3C Web Accessibility Initiative", "status": "current", "source_class": "official_guidance", "use": "aria-sort structural requirements and reservations"},
    {"source_id": "V6475-S17", "title": "WAI-ARIA 1.2", "url": "https://www.w3.org/TR/wai-aria/", "publisher": "W3C", "status": "stable", "source_class": "official_standard", "use": "table, sort, status, and live-region semantics only"},
    {"source_id": "V6475-S18", "title": "IUPAC Gold Book Helmholtz energy", "url": "https://goldbook.iupac.org/terms/view/H02772", "publisher": "IUPAC", "status": "stable", "source_class": "official_terminology", "use": "physical Helmholtz-energy definition and domain barrier"},
    {"source_id": "V6475-S19", "title": "Distribution-Free Predictive Inference for Regression", "url": "https://doi.org/10.1080/01621459.2017.1307116", "publisher": "Journal of the American Statistical Association", "status": "stable", "source_class": "primary_research", "use": "split-conformal and finite-sample marginal-coverage obligations"},
    {"source_id": "V6475-S20", "title": "Conformal Prediction Beyond Exchangeability", "url": "https://doi.org/10.1214/23-AOS2276", "publisher": "The Annals of Statistics", "status": "stable", "source_class": "primary_research", "use": "exchangeability and drift limitations; no deployment claim"},
]


SAFE_TASK_TITLES = [
    "Reconcile all 510 inherited proposal records before novelty credit",
    "Build exact normalized-title and semantic-neighbor collision audit for v647-v5",
    "Verify twenty source records use only current stable draft or watch status",
    "Preserve the citation-to-observation and observation-to-data firewalls",
    "Retain the two startup failures before any retry credit",
    "Build a plan-only x1 staged-file allowlist review",
    "Run five-class x1 privacy and raw-identifier adjudication",
    "Verify the Heart focus and library-practice nonauthority boundary",
    "Verify owner-generated footprint remains below the rotation threshold",
    "Record verify-only Codex Python Git and PowerShell versions",
    "Audit Windows Sandbox capability read-only without elevation or feature change",
    "Guard the four allowed core outcome labels and exact distribution",
    "Reconcile twenty-one open gaps and twenty-two exact gates",
    "Reconcile 3,493 inherited negatives plus x1 startup failures",
    "Hold the Ilyra route at zero sends until exact-final proof",
    "Specify bounded-priority admission and starvation fixtures",
    "Specify ADM Hamiltonian and momentum-constraint obligations",
    "Specify Pantheon+ zero-row release and covariance receipt",
    "Specify library digital-access synthetic handover states",
    "Specify OAuth PAR request_uri binding and replay vectors",
    "Specify library authority and remedy reservations",
    "Specify Git protocol-v2 pkt-line and section fixtures",
    "Specify sortable-table and filter-state accessibility fixtures",
    "Specify Helmholtz-energy domain and metastability fixtures",
    "Specify conformal-prediction nonpromotion fixtures",
    "Specify accessible static-report landmarks and evaluation reservations",
    "Enforce deterministic JSON ordering UTF-8 and LF authoring",
    "Use exact Git-blob identity for frozen lifecycle hashes",
    "Preserve family-current caller compatibility and additive history",
    "Emit owner workload wellbeing and corrigibility receipts",
]

CANDIDATE_TITLES = [
    "Priority-queue overload and high-watermark mutation generator",
    "Starvation aging cancellation and drain-order mutation generator",
    "ADM lapse-shift multiplier type prototype",
    "Hypersurface-deformation bracket and boundary-term prototype",
    "Pantheon+ redshift-frame and release-mix quarantine prototype",
    "Pantheon+ covariance calibration and selection-lock prototype",
    "Library outage queue and ownership replay prototype",
    "Library privacy-minimization and accessible-fallback prototype",
    "OAuth PAR client-binding and expiry refusal prototype",
    "OAuth PAR parameter-substitution and replay quarantine prototype",
    "Library child disability privacy and remedy reservation prototype",
    "Māori library-data authority reservation prototype",
    "Git protocol-v2 pkt-line boundary parser prototype",
    "Git protocol-v2 capability and section-order prototype",
    "Git ref-prefix widening and budget refusal prototype",
    "Sortable-table single aria-sort owner prototype",
    "Filter-state result-count and focus-retention prototype",
    "Helmholtz fixed-temperature-volume mutation prototype",
    "Helmholtz convexity metastability and phase-boundary guard prototype",
    "Conformal leakage subgroup drift and nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-priority-backpressure-tribunal", "Audit bounded priority admission backpressure and starvation traces"),
    ("ghc-family-adm-constraint-obligations", "Audit ADM canonical constraints boundary terms and nonpromotion"),
    ("ghc-family-pantheon-plus-zero-row", "Preserve a zero-row Pantheon+ study boundary"),
    ("ghc-family-library-digital-handover", "Audit synthetic public-library digital-access handovers"),
    ("ghc-family-oauth-par-profile", "Audit synthetic OAuth PAR binding expiry and replay vectors"),
    ("ghc-family-library-authority-reservation", "Reserve library privacy access remedy and Māori authority gates"),
    ("ghc-family-git-protocol-v2-tribunal", "Audit disposable Git protocol-v2 framing fixtures"),
    ("ghc-family-sortable-table-audit", "Audit sortable-table filter focus and print structure"),
    ("ghc-family-helmholtz-domain-guard", "Keep Helmholtz-energy reasoning inside its physical domain"),
    ("ghc-family-conformal-prediction-nonpromotion", "Guard conformal coverage assumptions from Stage 20 promotion"),
    ("ghc-family-510-corpus-semantic-audit", "Audit semantic novelty against the 510 frozen core proposals"),
    ("ghc-family-four-view-baseline-equality-v2", "Prove inherited local upstream tracking and live equality"),
    ("ghc-family-live-remote-zero-line-guard-v2", "Handle expected empty live-remote results without false failure"),
    ("ghc-family-commit-local-blob-manifest-v5", "Verify lifecycle manifests against exact commit blobs"),
    ("ghc-family-timeout-split-probe-v2", "Split slow Windows probes while retaining the timed-out witness"),
    ("ghc-family-x1-plan-only-separation-v3", "Keep x1 plans free of x2 execution and outcome credit"),
    ("ghc-family-current-source-status-ledger-v2", "Keep source statuses inside the approved vocabulary"),
    ("ghc-family-public-path-privacy-confirmation-v2", "Separate scanner definitions from confirmed privacy payload hits"),
    ("ghc-family-eiren-complete-suite-exclusion-lock", "Freeze exact inherited full-suite exclusions by test identity"),
    ("ghc-family-baton-sanitization-preflight-v2", "Sanitize and gate one acknowledged terminal baton"),
]

RUNNER_TITLES = [
    "ghc_family_priority_backpressure_tribunal.py",
    "ghc_family_adm_constraint_obligations.py",
    "ghc_family_pantheon_plus_zero_row.py",
    "ghc_family_library_digital_handover.py",
    "ghc_family_oauth_par_profile.py",
    "ghc_family_git_protocol_v2_tribunal.py",
    "ghc_family_sortable_table_audit.py",
    "ghc_family_helmholtz_domain.py",
    "ghc_family_conformal_prediction_board.py",
    "ghc_family_v647_v5_validation_runner.py",
]

CLEAN_TASK_TITLES = [
    "Synchronize the 510-to-520 proposal counts across x1 surfaces",
    "Synchronize inherited and new negative counts after each retained failure",
    "Keep Method Flow records witnesses guards and recommendations count-consistent",
    "Correct stale lifecycle labels through additive commits only",
    "Keep family-current callers compatible while selecting new bounded tools",
    "Normalize generated JSON keys and list order deterministically",
    "Normalize authored UTF-8 and LF without hashing checkout bytes",
    "Distinguish Git-blob index and working-tree hash domains",
    "Adjudicate private absolute-path candidates before public artifact credit",
    "Adjudicate raw task or thread identifier candidates before staging",
    "Adjudicate credential key and token candidates before staging",
    "Recheck every source status and publisher field at x2 closeout",
    "Recheck citation observation row and likelihood counters remain separated",
    "Recheck x1 staged paths contain plans but no x2 outcomes",
    "Recheck x2 outcomes use only the four approved labels",
    "Recheck exact and blocked portfolios earn zero execution credit",
    "Measure owner-created paths rather than inherited repository size",
    "Audit static-report title main landmark tables captions and heading order",
    "Audit static-report manual assistive-technology and affected-user reservations",
    "Audit Māori wording data-governance and authority reservations",
    "Audit public-library professional privacy and safeguarding reservations",
    "Audit Pantheon+ queries downloads rows covariance and likelihood counters stay zero",
    "Audit real patron worker account and library-record counters stay zero",
    "Audit real key client token grant and authorization counters stay zero",
    "Recheck source x1 evidence and final ancestry using exact hashes",
    "Recheck phase commit cap zero merges and single-parent history",
    "Recheck the sole validation lane stays named local-only and unpushed",
    "Recheck canonical four-view remote equality after every publish gate",
    "Refresh phase-scoped Family Index Method Flow and orchestration receipts",
    "Refresh wellbeing corrigibility and one-shot terminal-route state",
]

EXACT_PACKET_TITLES = [
    "Real Pantheon+ data access and likelihood execution",
    "Real library patron worker child or account decision",
    "Real borrowing search-history or platform-data disclosure",
    "Production OAuth PAR authorization or token exchange",
    "Real identity key proof consent or recovery operation",
    "Legal interpretation access restriction or remedy allocation",
    "Māori authority cultural wording or data-governance decision",
    "Production deployment interoperability or security certification",
    "Externally owned independent-team reproduction authorization and claim",
    "Governed Stage 20 promotion decision with proof or canon authority",
]

BLOCKED_PACKET_TITLES = [
    "Reject every force push history rewrite and phase merge",
    "Reject deletion reuse or mutation of any sibling lane",
    "Expose credentials private routes nonpublic conversation or raw identifiers",
    "Enable Windows features weaken security elevate install unrelated software or reboot",
    "Reject consciousness personhood AGI ASI and Theory-of-Everything closure assertions",
]

X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6475-X1-N01",
        "method_id": "V6475-M01",
        "summary": "The first combined source Eiren and drive-state preflight exceeded its 30-second wrapper budget before returning usable consolidated evidence.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6475-X1-N02",
        "method_id": "V6475-M02",
        "summary": "A Windows ripgrep inspection passed wildcard paths as literal filenames and failed before reading the intended phase templates.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6475-X1-N03",
        "method_id": "V6475-M03",
        "summary": "The first definitions patch used an encoding-corrupted expected line and failed closed without applying any partial hunk.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6475-X1-N04",
        "method_id": "V6475-M04",
        "summary": "A repository-local runner lookup returned no match because the required Method Flow runner is bundled under the selected skill package.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6475-X1-N05",
        "method_id": "V6475-M05",
        "summary": "The first expanded x1 portfolio audit stopped on seven exact inherited title collisions before emitting the preregistration packet.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6475-X1-N06",
        "method_id": "V6475-M06",
        "summary": "A PowerShell wildcard status filter treated question marks as wildcards and falsely reported every staged row as untracked.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6475-X1-N07",
        "method_id": "V6475-M07",
        "summary": "A combined Git status branch and head wrapper exhausted a ten-second process budget before emitting consolidated output.",
        "retained": True,
        "recovered": True,
    },
]

# X2 failures are recorded in the x2 Method Flow ledger after the immutable x1 freeze.
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = []
