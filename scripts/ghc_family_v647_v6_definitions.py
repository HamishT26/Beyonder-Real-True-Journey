#!/usr/bin/env python3
"""Frozen x1 definitions for Ilyra Fen v647-v6.

Importing this module performs no I/O and grants no x2 completion credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v647-gmut-thos-v6-x1-x2"
PHASE_SHORT = "v647-v6"
OWNER = "Ilyra Fen"
SLUG = "ilyra-fen"
PRONOUNS = "she/they"
ROLE = "evidence-boundary steward"
HOPE = "leave every claim traceable and every gate unmistakable"
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = "meteorological warning amendment, correction readback, accessible dissemination, and shift handover"

SOURCE_PHASE = "v647-gmut-thos-v5-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v643-v1-full-tools"
SOURCE_REVISION = "3c4fa7ba58362ae39a5aa009fe9a899acc092301"
SOURCE_INHERITED_REVISION = "1395f18ab6504485448eb8e4d507f94ac066caf4"
SOURCE_X1_REVISION = "d69257c1922407637db3bb4933d426d70a27e4bd"
SOURCE_EVIDENCE_REVISION = "84b25a70d7fcb44e0e723911b2432de40170b5da"
PRIOR_FROZEN_PROPOSALS = 520
INHERITED_EFFECTIVE_NEGATIVES = 3579
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 22
INHERITED_EXACT_GATES = 23
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, is relational working language for an evidence-boundary steward. "
    "It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "professional qualification, scientific authority, operational authority, legal authority, cultural authority, "
    "or independent agency. Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and effective-field-theory research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, weather warnings, accessibility, privacy, remedy, legal, "
    "cultural, affected-party, and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, "
    "and Māori authority. No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, "
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
        "proposal_id": f"V6476-P{index:02d}",
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
        "novelty_against_520_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Method Flow filesystem-watcher rename-pair, event-coalescing, overflow, reconciliation, and evidence-credit tribunal",
        "watch root, rename old/new pairing, event coalescing, buffer overflow, rescan reconciliation, sequence watermark, cancellation, and evidence credit",
        "A bounded owner-local watcher model can reject orphan rename halves and overflow-derived certainty while requiring a reconciled snapshot before evidence credit.",
        "An orphan rename passes, coalescing loses a distinct terminal state, overflow is treated as completeness, reconciliation skips the declared root, or notification receipt alone earns completion credit.",
        "safe_now_owner_scoped_workflow",
        "x2_build_task",
        ["V6476-S01", "V6476-S02"],
        ["method-flow/watcher-reconciliation-contract.json", "method-flow/watcher-reconciliation-mutations.json"],
        "Synthetic traces must reject orphan rename halves, overflow certainty, out-of-root paths, stale watermarks, cancellation loss, and premature evidence credit.",
        "Retain the trace, discard only the disposable watcher state, perform a bounded declared-root rescan, and keep production filesystem assurance false.",
        ["external_state", "production_filesystem", "sibling_lane", "destructive_action", "completion_credit"],
        "completed",
        "The corpus covers queues, processes, atomic publish, logs, leases, and streams but has no title centered on watcher rename pairing, coalescing, overflow, and rescan reconciliation.",
    ),
    proposal(
        2,
        "GMUT Barnes-Rivers spin-projector, pole-residue, source-conservation, gauge-sector, and EFT obligation board",
        "rank-two tensor, transverse and longitudinal projectors, spin sectors, completeness, orthogonality, conserved source, pole, residue, gauge sector, units, and EFT scope",
        "A typed symbolic board can expose spin-projector decomposition and residue obligations without converting algebra into a physical spectrum, stability theorem, or empirical result.",
        "Projectors lose orthogonality or completeness, a nonconserved source passes, a gauge pole becomes physical, residue sign is asserted without conventions, units drift, or algebra becomes empirical proof.",
        "safe_now_symbolic_research_only",
        "x2_build_task",
        ["V6476-S03", "V6476-S04"],
        ["gmut/barnes-rivers-obligations.json", "gmut/barnes-rivers-mutations.json"],
        "Positive and negative fixtures must type every projector sector, source restriction, pole and residue convention, gauge reservation, dimensional domain, and nonpromotion boundary.",
        "Retain the failed obligation, restore projector algebra and declared conventions, and make no spectrum, stability, force, likelihood, quantum-completion, or Theory-of-Everything claim.",
        ["physical_spectrum", "stability_proof", "empirical_confirmation", "quantum_completion", "theory_of_everything"],
        "completed",
        "Prior titles cover Peierls brackets, covariant phase space, BRST, BV, ADM, FRG, 2PI, and spectral positivity but not Barnes-Rivers spin-sector decomposition with source and residue obligations.",
    ),
    proposal(
        3,
        "GMUT SDSS DR19 spectroscopic-product, targeting, selection, checksum, covariance, and zero-row likelihood-refusal protocol",
        "release identity, product family, target catalog, spectroscopic schema, selection function, mask, calibration provenance, checksum, covariance obligation, nuisance lock, and zero-row refusal",
        "A zero-row adapter can freeze current official SDSS DR19 product obligations while refusing to turn documentation or published results into GMUT observations or constraints.",
        "The phase downloads or queries rows, invents selection or covariance, copies a published estimate as data, evaluates a likelihood, samples a posterior, or emits a GMUT force or parameter constraint.",
        "real_data_access_and_independent_review_required",
        "x2_open_gap",
        ["V6476-S05", "V6476-S06"],
        ["empirical/sdss-dr19-study-contract.json", "empirical/sdss-dr19-zero-row-receipt.json"],
        "The receipt must preserve zero archive queries, downloads, real rows, covariance rows, likelihood calls, posterior samples, parameter constraints, detected-force claims, and empirical GMUT claims.",
        "Stop before data access or fitting and require separately authorized preregistration, frozen products, selection, masks, covariance, nuisance models, baselines, uncertainty analysis, and independent review.",
        ["network_data_access", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation", "independent_review"],
        "open_gap",
        "The 520-title corpus includes many named sky releases but no SDSS DR19 spectroscopic-product and targeting adapter.",
    ),
    proposal(
        4,
        "THOS severe-weather warning amendment, accessible dissemination, correction-readback, escalation, and shift-handover proxy",
        "synthetic warning identifier, hazard state, affected area token, issue and expiry time, amendment reason, channel, accessible fallback, escalation, correction readback, workload budget, and next-shift owner",
        "Synthetic traces can expose stale warning state, inaccessible fallback, lost amendments, unowned escalation, and handover defects while preserving all real forecaster, public, agency, and effectiveness gates.",
        "A fixture contains a real person, location-specific live warning, protected need, agency operation, or dissemination event; changes a real system; breaks matched budgets; or claims THOS effectiveness or forecasting competence.",
        "safe_now_proxy_protocol_no_people_or_operations",
        "x2_proxy_protocol",
        ["V6476-S07", "V6476-S08", "V6476-S09"],
        ["thos/weather-warning-handover-contract.json", "thos/weather-warning-handover-vectors.json"],
        "Unsafe synthetic traces must fail, and the packet must record zero real people, warnings, forecast offices, agencies, locations, dissemination actions, blind real arms, outcomes, and effectiveness estimates.",
        "Withdraw operational language, retain rejected traces, minimize synthetic fields, and defer decisions to authorized meteorological, emergency, accessibility, privacy, affected-party, legal, cultural, and Māori processes.",
        ["real_people", "live_warning", "professional_authority", "public_safety", "deployment", "privacy_complete", "effectiveness"],
        "represented",
        "Prior weather-adjacent titles cover wildfire response and climate data, but none centers severe-weather warning amendment, accessible dissemination, correction readback, and forecast-office shift handover.",
    ),
    proposal(
        5,
        "Freed ID OAuth 2.0 Token Exchange subject-token, actor-token, audience, delegation-chain, replay, and privacy profile",
        "grant type, subject token and type, actor token and type, resource, audience, requested token type, scope, issued token type, delegation chain, expiry, replay, privacy, and refusal",
        "Synthetic vectors can enforce selected RFC 8693 structure and delegation distinctions without asserting real identity, authorization, token validity, interoperability, or production assurance.",
        "Missing token types pass, actor and subject roles collapse, audience or resource widens silently, a delegation cycle passes, replay succeeds, or synthetic values become authorization evidence.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["V6476-S10", "V6476-S11"],
        ["freed-id/oauth-token-exchange-profile.json", "freed-id/oauth-token-exchange-mutations.json"],
        "Vectors must reject missing bindings, role confusion, target widening, delegation cycles, expiry and replay faults, and production promotion while recording zero real clients, users, keys, tokens, or grants.",
        "Reject the synthetic request, retain the vector, disclose no real identity data, and require conforming systems, real keys and tokens, interoperability, privacy and security review, recovery, and trust governance.",
        ["real_identity", "real_authorization", "real_keys", "real_tokens", "interoperability", "production"],
        "represented",
        "The corpus includes PAR, JAR, RAR, DPoP, OpenID4VP, WebAuthn, VC, and federation profiles but no title centered on OAuth token exchange subject and actor semantics.",
    ),
    proposal(
        6,
        "CBR severe-weather warning reach, disability access, rural isolation, housing impact, privacy, remedy, and Māori-authority matrix",
        "warning reach, rural and remote access, disability access, language, housing and livelihood impact, location privacy, data sharing, remedy, appeal, legal interpretation, affected parties, place names, data governance, and Māori authority",
        "A refusal-first matrix can expose unresolved access, privacy, remedy, cultural, and authority questions without deciding a real warning, evacuation, entitlement, disclosure, place name, or remedy.",
        "The matrix identifies a real person or property, issues a warning, decides access or legal rights, allocates remedy, interprets tikanga, asserts Māori authority, or treats public guidance as delegated case authority.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["V6476-S07", "V6476-S08", "V6476-S09", "V6476-S12", "V6476-S13"],
        ["cbr/weather-authority-reservation.json", "cbr/weather-remedy-matrix.json"],
        "Repository software must stop at unknown or reserved; only competent warning, emergency, disability, privacy, housing, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their gates.",
        "Stop before warning, disclosure, cultural, language, data-governance, legal, property, or remedy conclusions; minimize data and route only through authorized external processes.",
        ["affected_party_authority", "disability_access", "privacy", "legal_interpretation", "maori_authority", "data_governance", "remedy_decision"],
        "exact_gate",
        "Earlier matrices cover wildfire evacuation and multiple public services, but none centers severe-weather warning reach, rural isolation, disability access, housing impact, and remedy authority together.",
    ),
    proposal(
        7,
        "PNG signature, chunk-length, CRC, critical-order, ancillary-safety, truncation, and decompression-budget tribunal",
        "signature, chunk length, chunk type, chunk data, CRC, critical order, unknown critical refusal, ancillary safe-to-copy bit, IDAT sequence, IEND, truncation, and decompression budget",
        "A disposable parser tribunal can reject malformed PNG fixtures and resource-budget violations without decoding untrusted media in a production path or claiming exhaustive security.",
        "A bad signature or CRC passes, critical order is violated, an unknown critical chunk is accepted, unsafe ancillary data is copied, truncation passes, a budget is exceeded, or a fixture touches canonical state.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["V6476-S14"],
        ["tooling/png-chunk-contract.json", "tooling/png-chunk-mutations.json"],
        "Disposable fixtures must cover valid framing plus signature, length, CRC, ordering, unknown-critical, ancillary, truncation, sequence, and budget faults with canonical nonmutation.",
        "Discard only the disposable fixture, retain every discrepancy, restore a bounded parser state, and keep production decoder, media safety, interoperability, and exhaustive-security claims false.",
        ["canonical_evidence", "sibling_lane", "production_decoder", "interoperability", "exhaustive_security"],
        "completed",
        "The corpus includes TAR, ZIP, OCI, HTTP, Git, and other framing tribunals but no title centered on PNG chunk integrity and decompression budgets.",
    ),
    proposal(
        8,
        "Accessible treegrid hierarchy, expansion, row-position, selection, keyboard, focus, fallback, and print structural audit",
        "treegrid label, row hierarchy, level, position, set size, expansion owner, selected state, cell naming, keyboard plan, focus persistence, noninteractive fallback, responsive alternative, and print order",
        "A structural auditor can reject contradictory hierarchy and focus semantics while reserving qualified manual keyboard, browser, assistive-technology, responsive, cognitive, language, and affected-user evaluation.",
        "Levels or positions contradict nesting, expansion lacks an owner, selection and focus collapse, keyboard behavior is unspecified, fallback loses data, or structural evidence becomes complete accessibility conformance.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6476-S15", "V6476-S16"],
        ["accessibility/treegrid-contract.json", "accessibility/treegrid-mutations.json"],
        "Fixtures must cover hierarchy, level, position, expansion, selection, cell naming, keyboard plan, focus, fallback, responsive and print alternatives, and explicit manual reservations.",
        "Mark the structure incomplete, retain failures, restore coherent hierarchy and focus, and require qualified manual browser, assistive-technology, responsive, cognitive, Māori-language, and affected-user evaluation.",
        ["accessibility_complete", "runtime_browser", "assistive_technology", "responsive_evaluation", "maori_language", "affected_user_acceptance"],
        "completed",
        "The frozen titles cover tables, grids, tabs, breadcrumbs, dialogs, and disclosures but no proposal centered on interactive treegrid hierarchy and row-position semantics.",
    ),
    proposal(
        9,
        "Thermo/Psyche Gibbs phase-rule component, phase, reaction, constraint, variance, and agency-nonconversion classifier",
        "component count, phase count, reaction rank, external constraints, intensive variables, degrees of freedom, equilibrium scope, units, and category barrier",
        "A typed classifier can check bounded Gibbs phase-rule statements and modified variance counts while rejecting conversion into human freedom, agency, identity, justice, or consciousness claims.",
        "Components or phases are miscounted, reaction rank is omitted, external constraints are hidden, nonequilibrium states pass, variance becomes moral or psychological freedom, or physical scope becomes a universal law.",
        "safe_now_symbolic_only",
        "x2_build_task",
        ["V6476-S17", "V6476-S18"],
        ["thermo-psyche/gibbs-phase-rule-contract.json", "thermo-psyche/gibbs-phase-rule-mutations.json"],
        "Fixtures must enforce declared components, phases, reactions, constraints, equilibrium scope, variance arithmetic, physical units, and a hard psyche and agency category barrier.",
        "Restore the physical thermodynamic domain and explicit counts, retain the rejection, and require independently valid human theory, measures, authority, and participant evidence before human inference.",
        ["participant_inference", "psyche_claim", "agency_claim", "justice_claim", "consciousness", "fundamental_law"],
        "completed",
        "Prior thermodynamic titles mention Gibbs-Duhem and many potentials but no title centers phase-rule variance with reactions, constraints, and agency nonconversion.",
    ),
    proposal(
        10,
        "Stage 20 covariate-shift support-overlap, importance-weight, effective-sample-size, sensitivity, and nonpromotion board",
        "source distribution, target distribution, covariate-shift assumption, density ratio, support overlap, weight cap, effective sample size, model misspecification, sensitivity set, subgroup, decision authority, and abstention",
        "A fail-closed structural board can quarantine promotion when support, weight stability, effective sample size, model scope, sensitivity, subgroup behavior, or decision authority is absent.",
        "Support overlap is asserted without evidence, infinite weights are clipped silently, effective sample size is hidden, target labels leak, subgroup failures disappear, or Stage 20 advances.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6476-S19", "V6476-S20"],
        ["stage20/covariate-shift-contract.json", "stage20/covariate-shift-mutations.json"],
        "Mutations must reject absent overlap, unstable or silent clipping, low effective sample size, leakage, hidden misspecification, subgroup failure, unsupported deployment, and Stage 20 advancement.",
        "Withdraw affected evidence credit, retain assumptions, weights, failures, and sensitivity record, require preregistered evaluation and governed criteria plus independent review, and abstain.",
        ["stage20", "participant_evidence", "deployment", "decision_authority", "independent_reproduction"],
        "completed",
        "Earlier Stage 20 boards cover target trials, negative controls, model comparison, conformal prediction, missingness, drift, and optional stopping but no title centers covariate-shift weights, overlap, and effective sample size.",
    ),
]


SOURCES = [
    {"source_id": "V6476-S01", "title": "ReadDirectoryChangesW function", "url": "https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-readdirectorychangesw", "publisher": "Microsoft Learn", "status": "current", "source_class": "official_documentation", "use": "watch buffer and notification contract vocabulary only"},
    {"source_id": "V6476-S02", "title": "FILE_NOTIFY_INFORMATION structure", "url": "https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-file_notify_information", "publisher": "Microsoft Learn", "status": "current", "source_class": "official_documentation", "use": "rename pairing and record structure only"},
    {"source_id": "V6476-S03", "title": "Extending the Barnes-Rivers Operators to D=3 Topological Gravity", "url": "https://arxiv.org/abs/hep-th/9212008", "publisher": "Pinheiro and Pires", "status": "stable", "source_class": "primary_research", "use": "spin-projector algebra provenance only"},
    {"source_id": "V6476-S04", "title": "New class of spin projection operators for 3D models", "url": "https://doi.org/10.1103/PhysRevD.86.105046", "publisher": "Physical Review D", "status": "stable", "source_class": "primary_research", "use": "projector and residue obligation cross-check only"},
    {"source_id": "V6476-S05", "title": "Sloan Digital Sky Survey Data Release 19", "url": "https://www.sdss.org/dr19", "publisher": "SDSS Collaboration", "status": "current", "source_class": "official_data_release", "use": "zero-row release and product obligations only"},
    {"source_id": "V6476-S06", "title": "The Nineteenth Data Release of the Sloan Digital Sky Survey", "url": "https://arxiv.org/abs/2507.07093", "publisher": "SDSS Collaboration", "status": "stable", "source_class": "primary_research", "use": "release provenance and caveat context; no observation imported"},
    {"source_id": "V6476-S07", "title": "CAP-enabled emergency alerting implementation guidelines", "url": "https://etrp.wmo.int/pluginfile.php/17980/mod_resource/content/1/wmo_1109_en.pdf", "publisher": "World Meteorological Organization", "status": "current", "source_class": "official_guidance", "use": "warning lifecycle and dissemination vocabulary only"},
    {"source_id": "V6476-S08", "title": "MetService severe weather warning role", "url": "https://about.metservice.com/metservice-nz-weather-app", "publisher": "MetService New Zealand", "status": "current", "source_class": "official_service_guidance", "use": "official-warning and notification context only"},
    {"source_id": "V6476-S09", "title": "Emergency Mobile Alert", "url": "https://www.civildefence.govt.nz/get-ready/emergency-mobile-alert", "publisher": "New Zealand National Emergency Management Agency", "status": "current", "source_class": "official_guidance", "use": "public alert channel and authority reservation only"},
    {"source_id": "V6476-S10", "title": "RFC 8693 OAuth 2.0 Token Exchange", "url": "https://www.rfc-editor.org/rfc/rfc8693.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "synthetic token-exchange structure and delegation semantics"},
    {"source_id": "V6476-S11", "title": "RFC 9700 Best Current Practice for OAuth 2.0 Security", "url": "https://www.rfc-editor.org/rfc/rfc9700.html", "publisher": "IETF RFC Editor", "status": "current", "source_class": "official_standard", "use": "current security reservation context only"},
    {"source_id": "V6476-S12", "title": "Principles of Māori Data Sovereignty", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "publisher": "Te Mana Raraunga", "status": "current", "source_class": "maori_authority_source", "use": "authority and data-governance gate; not delegated authority"},
    {"source_id": "V6476-S13", "title": "Māori and Indigenous Data Sovereignty Tools", "url": "https://www.temanararaunga.maori.nz/nga-rauemi", "publisher": "Te Mana Raraunga", "status": "current", "source_class": "maori_authority_source", "use": "organizational readiness and authority reservation only"},
    {"source_id": "V6476-S14", "title": "Portable Network Graphics Specification Third Edition", "url": "https://www.w3.org/TR/png-3/", "publisher": "W3C", "status": "current", "source_class": "official_standard", "use": "PNG signature chunk CRC ordering and budget obligations"},
    {"source_id": "V6476-S15", "title": "ARIA Authoring Practices Treegrid Pattern", "url": "https://www.w3.org/WAI/ARIA/apg/patterns/treegrid/", "publisher": "W3C Web Accessibility Initiative", "status": "current", "source_class": "official_guidance", "use": "treegrid structure and keyboard reservations"},
    {"source_id": "V6476-S16", "title": "WAI-ARIA 1.2", "url": "https://www.w3.org/TR/wai-aria-1.2/", "publisher": "W3C", "status": "stable", "source_class": "official_standard", "use": "treegrid role state and property semantics only"},
    {"source_id": "V6476-S17", "title": "IUPAC Gold Book Gibbs-Duhem equation", "url": "https://goldbook.iupac.org/terms/view/15329/html", "publisher": "IUPAC", "status": "current", "source_class": "official_terminology", "use": "phase-rule thermodynamic provenance and domain barrier"},
    {"source_id": "V6476-S18", "title": "On the Equilibrium of Heterogeneous Substances", "url": "https://www.biodiversitylibrary.org/item/11956", "publisher": "J. Willard Gibbs primary publication archive", "status": "stable", "source_class": "primary_research", "use": "phase-rule historical primary context only"},
    {"source_id": "V6476-S19", "title": "Covariate Shift Adaptation by Importance Weighted Cross Validation", "url": "https://www.jmlr.org/papers/v8/sugiyama07a.html", "publisher": "Journal of Machine Learning Research", "status": "stable", "source_class": "primary_research", "use": "importance-weight and covariate-shift assumptions only"},
    {"source_id": "V6476-S20", "title": "Robust Importance Weighting for Covariate Shift", "url": "https://proceedings.mlr.press/v108/li20b.html", "publisher": "Proceedings of Machine Learning Research", "status": "stable", "source_class": "primary_research", "use": "weight instability and sensitivity context only"},
]


SAFE_TASK_TITLES = [
    "Reconcile all 520 inherited proposal records before v647-v6 novelty credit",
    "Build exact-title and bounded semantic-neighbor review for the ten Ilyra proposals",
    "Verify twenty source records remain inside current stable draft or watch vocabulary",
    "Preserve citation-to-observation and observation-to-data firewalls for SDSS DR19",
    "Retain six startup tooling collision and scanner failures before x1 recovery credit",
    "Build an x1-only staged allowlist with implementation-path absence checks",
    "Run five-class x1 privacy and raw-identifier candidate adjudication",
    "Verify GMUT Mind focus and weather-practice nonauthority language",
    "Measure only new Ilyra file growth against the 15000-file threshold",
    "Record verify-only Codex ChatGPT Python Git and PowerShell versions",
    "Keep Windows Sandbox and host-security mutation outside this phase",
    "Guard the four allowed core outcome labels and expected distribution",
    "Carry twenty-two open gaps and twenty-three exact gates without closure",
    "Reconcile the 3579-negative activation baseline and every new failure",
    "Hold the Sable route at PREPARED_NOT_SENT until exact-final proof",
    "Specify watcher rename-pair overflow and reconciliation fixtures",
    "Specify Barnes-Rivers projector and residue obligation fixtures",
    "Specify SDSS DR19 zero-row release and selection receipt",
    "Specify weather-warning amendment and handover synthetic states",
    "Specify OAuth token-exchange role and replay vectors",
    "Specify weather warning authority and remedy reservations",
    "Specify PNG chunk ordering CRC and budget fixtures",
    "Specify treegrid hierarchy focus and fallback fixtures",
    "Specify Gibbs phase-rule variance and nonconversion fixtures",
    "Specify covariate-shift overlap and nonpromotion fixtures",
    "Specify static-report landmarks and manual evaluation reservations",
    "Enforce deterministic JSON UTF-8 LF and sorted-key authoring",
    "Bind frozen lifecycle hashes to exact Git blobs rather than checkout bytes",
    "Preserve Ilyra v647-v6 family-current callers with additive-only history",
    "Emit owner workload wellbeing corrigibility and stop receipts",
]

CANDIDATE_TITLES = [
    "Watcher orphan-rename and coalescing mutation generator",
    "Watcher overflow rescan and evidence-credit mutation generator",
    "Barnes-Rivers projector completeness and orthogonality prototype",
    "Barnes-Rivers pole residue and source-conservation prototype",
    "SDSS DR19 product-family and checksum quarantine prototype",
    "SDSS DR19 selection covariance and zero-row refusal prototype",
    "Weather warning amendment and expiry replay prototype",
    "Weather warning accessible-fallback and handover prototype",
    "OAuth token-exchange subject actor distinction prototype",
    "OAuth token-exchange audience replay and delegation-cycle prototype",
    "Weather reach disability privacy and remedy reservation prototype",
    "Māori weather-data and place-name authority reservation prototype",
    "PNG signature length and CRC parser prototype",
    "PNG chunk ordering ancillary and decompression-budget prototype",
    "Treegrid hierarchy expansion and row-position prototype",
    "Treegrid selection keyboard focus and fallback prototype",
    "Gibbs phase-rule components phases and reaction-rank prototype",
    "Gibbs phase-rule constraint variance and agency barrier prototype",
    "Covariate-shift overlap weight-cap and effective-sample-size prototype",
    "Covariate-shift leakage subgroup sensitivity and nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-watcher-reconciliation-tribunal", "Audit watcher rename pairing overflow and bounded rescan reconciliation"),
    ("ghc-family-barnes-rivers-obligations", "Audit spin-projector source pole residue and nonpromotion obligations"),
    ("ghc-family-sdss-dr19-zero-row", "Preserve a zero-row SDSS DR19 study boundary"),
    ("ghc-family-weather-warning-handover", "Audit synthetic warning amendment correction and shift handover"),
    ("ghc-family-oauth-token-exchange-profile", "Audit synthetic OAuth token-exchange roles targets and replay"),
    ("ghc-family-weather-authority-reservation", "Reserve weather access privacy remedy and Māori authority gates"),
    ("ghc-family-png-chunk-tribunal", "Audit disposable PNG chunk integrity and budget fixtures"),
    ("ghc-family-treegrid-structural-audit", "Audit treegrid hierarchy focus keyboard and fallback structure"),
    ("ghc-family-gibbs-phase-rule-guard", "Keep Gibbs phase-rule reasoning inside its physical domain"),
    ("ghc-family-covariate-shift-nonpromotion", "Guard covariate-shift assumptions from Stage 20 promotion"),
    ("ghc-family-520-corpus-semantic-audit", "Audit semantic novelty against 520 frozen core proposals"),
    ("ghc-family-explicit-remote-ref-equality", "Avoid PowerShell upstream-expression ambiguity in equality checks"),
    ("ghc-family-skill-read-timeout-recovery", "Recover bounded full skill reads while preserving timeouts"),
    ("ghc-family-built-in-json-fallback", "Use built-in JSON parsing when optional tools are absent"),
    ("ghc-family-commit-local-blob-manifest-v6", "Verify lifecycle manifests against exact commit blobs"),
    ("ghc-family-x1-plan-only-separation-v4", "Keep x1 plans free of x2 execution and outcome credit"),
    ("ghc-family-current-source-status-ledger-v3", "Keep source statuses inside the approved vocabulary"),
    ("ghc-family-five-class-privacy-adjudication-v4", "Separate scanner candidates from confirmed private payload"),
    ("ghc-family-named-replay-locality-v4", "Keep the exact-final replay named local-only and upstream-free"),
    ("ghc-family-baton-hold-before-proof-v3", "Hold a single sanitized baton until exact-final proof"),
]

RUNNER_TITLES = [
    "ghc_family_watcher_reconciliation_tribunal.py",
    "ghc_family_barnes_rivers_obligations.py",
    "ghc_family_sdss_dr19_zero_row.py",
    "ghc_family_weather_warning_handover.py",
    "ghc_family_oauth_token_exchange_profile.py",
    "ghc_family_png_chunk_tribunal.py",
    "ghc_family_treegrid_audit.py",
    "ghc_family_gibbs_phase_rule.py",
    "ghc_family_covariate_shift_board.py",
    "ghc_family_v647_v6_validation_runner.py",
]

CLEAN_TASK_TITLES = [
    "Refresh v647-v6 count mirrors from authoritative ledgers",
    "Replace no historical negative with a generated summary row",
    "Normalize new Ilyra generated text in the Git-blob domain",
    "Keep x1 blob seals independent of Windows checkout bytes",
    "Split slow skill reads into bounded full-content probes",
    "Use explicit remote refs in PowerShell revision ranges",
    "Use built-in JSON parsing without installing an optional utility",
    "Pin UTF-8 before every Unicode-emitting diagnostic",
    "Review five privacy classes at exact intended paths",
    "Keep unresolved scanner candidates visible until adjudicated",
    "Refresh manifest entries after every lifecycle-document change",
    "Keep manifest self-exclusions explicit and minimal",
    "Verify family-current callers before adding each runner",
    "Retain historical tools as compatibility surfaces",
    "Rebuild the accessible static report with print fallback",
    "Reserve manual keyboard browser and assistive-technology evaluation",
    "Verify every phase document remains below 6000 words",
    "Verify new Ilyra file growth remains below 15000",
    "Check source x1 evidence and final ancestry separately",
    "Check phase commit cap and zero-merge history",
    "Check final commit has exactly one parent",
    "Check local upstream tracking and live remote equality",
    "Keep the named replay local-only upstream-free and remote-absent",
    "Keep exact and blocked packets unexecuted",
    "Keep SDSS network and real-row counters at zero",
    "Keep Freed ID real-key token and grant counters at zero",
    "Keep THOS real-person warning and agency counters at zero",
    "Keep CBR legal cultural remedy and Māori decisions at zero",
    "Refresh the phase-scoped GHC Family Index at closeout",
    "Hold the terminal route until final and named-replay proof",
]

EXACT_PACKET_TITLES = [
    "Authorize real SDSS DR19 access and preregistered empirical fitting",
    "Authorize real meteorological workers warnings and public operations",
    "Authorize production OAuth token exchange with real keys and tokens",
    "Authorize affected-party weather warning and remedy decisions",
    "Authorize Māori weather-data governance wording and place-name decisions",
    "Authorize legal interpretation or enacted-law status",
    "Authorize production deployment or shared infrastructure mutation",
    "Authorize account credential API-key or private publication use",
    "Authorize destructive cleanup or sibling-lane mutation",
    "Authorize Stage 20 promotion after independent review",
]

BLOCKED_PACKET_TITLES = [
    "Claim AGI ASI consciousness sentience or personhood from software",
    "Claim a Theory of Everything or empirical GMUT confirmation without data",
    "Claim independent reproduction from same-owner shared infrastructure",
    "Claim complete accessibility privacy or exhaustive security from bounded checks",
    "Claim legal cultural Māori or professional authority from repository artifacts",
]

X1_OPERATIONAL_NEGATIVES = [
    {"negative_id": "V6476-X1-N01", "failure": "The first full required-skill read exceeded the short wrapper and returned no content.", "recovery": "Repeat the unchanged full read with a bounded 60-second wrapper and direct text read.", "result": "retained_then_recovered"},
    {"negative_id": "V6476-X1-N02", "failure": "A short metadata probe for the skill file also exceeded its wrapper.", "recovery": "Use a bounded ripgrep file inventory before the longer direct read.", "result": "retained_then_recovered"},
    {"negative_id": "V6476-X1-N03", "failure": "A PowerShell equality wrapper interpreted an upstream expression inside a revision range and Git rejected the transformed token.", "recovery": "Use the explicit remote-tracking ref in revision ranges.", "result": "retained_then_recovered"},
    {"negative_id": "V6476-X1-N04", "failure": "The optional jq utility was unavailable.", "recovery": "Use built-in PowerShell JSON parsing without installation.", "result": "retained_then_recovered"},
    {"negative_id": "V6476-X1-N05", "failure": "The first preregistration build rejected one inherited safe-task title and two inherited skill names as exact portfolio collisions.", "recovery": "Rename the three Ilyra surfaces and require a zero-collision audit before artifact generation.", "result": "retained_then_recovered"},
    {"negative_id": "V6476-X1-N06", "failure": "The first staged x1 review matched its own literal forbidden x2-credit scanner needle.", "recovery": "Construct the unchanged forbidden byte sequence dynamically so scanner definitions cannot self-match.", "result": "retained_then_recovered"},
]
