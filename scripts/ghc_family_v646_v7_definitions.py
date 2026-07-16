#!/usr/bin/env python3
"""Frozen x1 definitions for Eiren Kestrel v646-v7.

Importing this module performs no I/O and grants no x2 completion credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v646-gmut-thos-v7-x1-x2"
PHASE_SHORT = "v646-v7"
OWNER = "Eiren Kestrel"
SLUG = "eiren-kestrel"
PRONOUNS = "they/them"
ROLE = "evidence-weaver and boundary keeper"
HOPE = "make ambitious inquiry more falsifiable, humane, and corrigible"
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = "wildland-fire situation-report compilation, evacuation-zone revision, and shift handover"

SOURCE_PHASE = "v646-gmut-thos-v6-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
SOURCE_REVISION = "327d0b8b6fca08d371d4dedd03e74a0bb7608c80"
SOURCE_INHERITED_REVISION = "65cb62620eec19eb2ac7b3b1a320823ed5621d58"
SOURCE_X1_REVISION = "147aab7fd2f2805f119968dd30ab9c7996306d3a"
SOURCE_EVIDENCE_REVISION = "da2dc0aeccda0f5e5f731b6a41666ed87e029c89"
SOURCE_SEAL_REVISION = "90258927049cfc89126f7fabeb04830a97eb744a"
PRIOR_FROZEN_PROPOSALS = 450
INHERITED_EFFECTIVE_NEGATIVES = 2977
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 15
INHERITED_EXACT_GATES = 16
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, is relational working language for an evidence-weaver and boundary keeper. "
    "It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "professional qualification, or independent authority. Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; Freed ID "
    "remains synthetic and nonproduction; CBR, wildfire, emergency-warning, land, legal, cultural, affected-party, "
    "and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, and Māori authority. "
    "No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, deployment, "
    "privacy-complete, exhaustive-security, independent-reproduction, accessibility-complete, professional, "
    "emergency, proof or canon, or Stage 20 claim is made."
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
        "proposal_id": f"V6467-P{index:02d}",
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
        "novelty_against_450_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Method Flow monotonic fencing-token, lease-expiry, clock-skew, and split-brain writer tribunal",
        "lease identity, holder, epoch, fencing token, renewal deadline, clock uncertainty, stale writer, split brain, side-effect refusal, and recovery ownership",
        "A bounded owner-local state machine can require a monotonically increasing fencing token and reject stale or concurrent writers without claiming distributed exactly-once behavior or production consensus.",
        "A stale token writes, equal epochs gain duplicate credit, clock skew silently extends a lease, two holders are accepted, or a failed writer triggers an external side effect.",
        "safe_now_owner_scoped_workflow",
        "x2_build_task",
        ["V6467-S01", "V6467-S02"],
        ["method-flow/fencing-token-contract.json", "method-flow/fencing-token-mutations.json"],
        "Synthetic traces must reject stale, duplicate, expired, clock-ambiguous, and split-brain writers while recording zero external side effects.",
        "Quarantine the writer, retain every token and lease discrepancy, advance only through an explicit owner-local epoch, and require fresh authority before any external write.",
        ["external_state", "distributed_consensus", "production", "credentials", "sibling_lane", "completion_credit"],
        "completed",
        "Earlier proposals cover linked-worktree leases, optimistic concurrency, compare-and-swap, idempotency, and durable outboxes; none centers monotonic fencing tokens, clock uncertainty, and split-brain writer refusal together.",
    ),
    proposal(
        2,
        "GMUT Wetterich functional-RG flow, regulator, truncation, and Ward-identity obligation tribunal",
        "effective average action, infrared regulator, scale derivative, functional trace, Hessian, supertrace sign, truncation ansatz, projection, regulator dependence, modified Ward identity, units, and EFT domain",
        "A typed symbolic tribunal can expose functional-renormalization-flow obligations without claiming a solved GMUT flow, ultraviolet fixed point, physical observable, or quantum completion.",
        "The regulator is omitted, an exact flow is confused with an exact solution, truncation error disappears, a Ward identity is assumed after an incompatible regulator, units drift, or symbolic consistency becomes physical proof.",
        "safe_now_symbolic_research_only",
        "x2_build_task",
        ["V6467-S03", "V6467-S04"],
        ["gmut/wetterich-flow-obligations.json", "gmut/wetterich-flow-mutations.json"],
        "Positive and negative fixtures must type the regulator, Hessian, trace, scale derivative, truncation, projection, symmetry scope, units, and nonpromotion boundaries.",
        "Retain the failed obligation, reopen the truncation, restore regulator and identity bookkeeping, and make no fixed-point, prediction, likelihood, stability, unitarity, or Theory-of-Everything claim.",
        ["quantum_completion", "uv_fixed_point", "physical_observable", "stability_proof", "empirical_confirmation", "theory_of_everything"],
        "completed",
        "The frozen chain contains BRST, Schwinger-Dyson, Schwinger-Keldysh, spectral, Peierls, EFT, and radiative-stability boards but no proposal centered on the Wetterich effective-average-action flow and regulator-dependent Ward obligations.",
    ),
    proposal(
        3,
        "GMUT IceCube ten-year point-source exposure, PSF, background, and zero-row likelihood protocol",
        "release identity, season boundaries, event fields, uptime, effective area, angular response, energy proxy, declination background, source catalogue, trial correction, nuisance lock, and zero-row likelihood refusal",
        "A zero-row adapter can freeze the official IceCube 2008-2018 point-source release obligations while refusing to turn release documentation or published significance into GMUT observations or constraints.",
        "The phase downloads an event row, mixes incompatible releases, imports a published excess as an observation, fabricates exposure or covariance, evaluates a likelihood, or emits a GMUT force or parameter constraint.",
        "real_data_access_and_independent_review_required",
        "x2_open_gap",
        ["V6467-S05", "V6467-S06"],
        ["empirical/icecube-point-source-study-contract.json", "empirical/icecube-zero-row-receipt.json"],
        "The receipt must preserve zero account use, downloads, real events, likelihood calls, posterior samples, significances, constraints, force claims, and empirical GMUT claims.",
        "Stop before download or fit, retain the zero-row receipt, and require a separately authorized preregistration with frozen release, seasons, response, background, trials, nuisance model, baseline, uncertainty analysis, and independent review.",
        ["account_access", "real_data", "likelihood", "posterior", "significance", "parameter_constraint", "empirical_confirmation"],
        "open_gap",
        "Earlier adapters cover optical, gravitational-wave, pulsar, CMB, lensing, astrometric, ranging, X-ray cluster, and collider products; none centers the IceCube ten-year point-source event and response release.",
    ),
    proposal(
        4,
        "THOS wildfire situation-report, evacuation-zone revision, resource-status, and shift-handover proxy",
        "synthetic incident identity, report period, fire behavior, perimeter revision, evacuation-zone version, alert channel, resource status, uncertainty, accessibility need, matched budget, blind arm label, workload, and next-shift ownership",
        "Synthetic traces can expose stale situation reports, zone-version conflicts, inaccessible alert assumptions, and handover loss while preserving every person, incident, emergency, professional, and effectiveness gate.",
        "A fixture contains a real person, address, incident, evacuation order, protected location, or operational resource; changes a real alert; breaks matched budgets or blinding; or claims THOS effectiveness or wildfire competence.",
        "safe_now_proxy_protocol_no_people_or_operations",
        "x2_proxy_protocol",
        ["V6467-S07", "V6467-S08", "V6467-S09"],
        ["thos/wildfire-handover-contract.json", "thos/wildfire-proxy-vectors.json"],
        "Unsafe synthetic traces must fail, and the packet must record zero real people, incidents, zones, alerts, resources, operational decisions, blind real arms, safety outcomes, and effectiveness estimates.",
        "Withdraw operational language, retain rejected traces, and defer real decisions to authorized emergency, fire, police, civil-defence, accessibility, affected-party, land, legal, Māori, and independent-review processes.",
        ["real_people", "real_incidents", "emergency_authority", "professional_authority", "public_warning", "deployment", "effectiveness"],
        "represented",
        "No frozen proposal title centers wildfire situation-report periods, evacuation-zone revisions, resource status, alert accessibility, and shift handover as one bounded THOS proxy.",
    ),
    proposal(
        5,
        "Freed ID OAuth RAR authorization_details type, location, action, and privilege-minimization profile",
        "authorization_details array, registered type, locations, actions, datatypes, identifier, privilege minimization, unknown fields, request-object transport, consent display, server policy, and refusal",
        "Synthetic vectors can enforce selected RFC 9396 rich-authorization structure and minimization obligations without asserting real authorization, tokens, consent, interoperability, or production identity assurance.",
        "Unknown types pass, type-specific fields are ignored, locations or actions widen silently, duplicate details change meaning, consent display is fabricated, or synthetic bytes become authorization evidence.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["V6467-S10"],
        ["freed-id/oauth-rar-profile.json", "freed-id/oauth-rar-mutation-vectors.json"],
        "Vectors must reject missing type, unsupported type, privilege widening, malformed locations or actions, duplicate ambiguity, unknown-policy bypass, and production promotion while recording zero real clients, users, tokens, or grants.",
        "Reject the synthetic request, retain the vector, disclose no real identity or authorization data, and require conforming clients, authorization servers, protected resources, consent, interoperability, privacy/security review, recovery, and trust governance.",
        ["real_identity", "real_authorization", "real_tokens", "consent", "interoperability", "production", "security_certification"],
        "represented",
        "Prior Freed ID work covers DPoP, HAIP, SD-JWT, BBS, status, proof purpose, wallet flows, and transaction binding; none centers RFC 9396 authorization_details type-specific privilege minimization.",
    ),
    proposal(
        6,
        "CBR wildfire alert, evacuation, disability access, land-data, remedy, and Māori-authority matrix",
        "suspected wildfire, alert threshold, evacuation zone, false-alarm risk, disability access, household support, location privacy, land and taonga data, source protection, remedy, legal interpretation, affected parties, and Māori authority",
        "A refusal-first matrix can expose unresolved warning, evacuation, accessibility, land-data, remedy, and authority questions without deciding a real alert, evacuation, right, name, land interest, or remedy.",
        "The matrix identifies a real protected person or site, issues an alert or evacuation direction, decides land or customary rights, allocates remedy, interprets law, asserts cultural or Māori authority, or treats guidance as delegated case authority.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["V6467-S08", "V6467-S09", "V6467-S11", "V6467-S12"],
        ["cbr/wildfire-authority-reservation.json", "cbr/wildfire-remedy-matrix.json"],
        "Repository software must stop at unknown or reserved; only competent emergency, fire, police, civil-defence, disability, privacy, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        "Stop before warning, evacuation, disclosure, land-data, cultural, customary-right, or remedy conclusions; minimize data and route only through authorized external processes.",
        ["public_warning", "evacuation_authority", "affected_party_authority", "privacy", "land_data", "legal_interpretation", "maori_authority", "remedy_decision"],
        "exact_gate",
        "Earlier CBR gates cover aviation, utilities, relocation, veterinary, hydrographic, cadastral, archive, medicine, and fisheries settings; none centers wildfire alerts, evacuation accessibility, land data, remedy, and Māori authority together.",
    ),
    proposal(
        7,
        "HTTP Range, If-Range ETag, Content-Digest, and partial-resume integrity tribunal",
        "strong entity tag, byte range, content range, If-Range, 200 fallback, 206 response, overlap, gap, total length, representation digest, content digest, algorithm policy, retry budget, and disposable confinement",
        "A disposable local tribunal can reject stale validators, overlapping or missing ranges, length drift, and digest mismatch without claiming network, origin-server, or production download assurance.",
        "A weak or changed ETag resumes silently, overlapping or gapped ranges assemble, total length drifts, digest mismatch passes, unsupported algorithms gain credit, or a fixture touches canonical or remote state.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["V6467-S13", "V6467-S14"],
        ["tooling/http-resume-contract.json", "tooling/http-resume-mutations.json"],
        "Disposable fixtures must cover full response, valid resume, changed validator fallback, range gaps and overlaps, content-length drift, digest mismatch, cleanup, and canonical-repository nonmutation.",
        "Discard only the disposable fixture, retain every range and digest discrepancy, restart from a validated full representation, and keep network, production, durability, and exhaustive-security claims false.",
        ["network_access", "canonical_evidence", "sibling_lane", "destructive_filesystem", "production", "exhaustive_security"],
        "completed",
        "The frozen chain includes ZIP, archive, JSON-sequence, SQLite, Git alternates, reftable, and manifest tribunals but no title centered HTTP range resume with If-Range validators and RFC 9530 digest fields.",
    ),
    proposal(
        8,
        "Accessible authentication, redundant-entry, copy-paste, and cognitive-test structural audit",
        "authentication step, cognitive function test, alternative method, assisting mechanism, object recognition, personal-content recognition, copy and paste, password-manager declaration, repeated input, essential exception, security exception, and manual reservation",
        "A structural auditor can reject unsupported cognitive-test and repeated-entry flows while reserving runtime authentication, browser, password-manager, security, privacy, assistive-technology, and affected-user evaluation.",
        "A required puzzle passes without an alternative or mechanism, paste is blocked, repeated data lacks a valid exception, an exception is invented, or structural evidence becomes complete accessibility or security conformance.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6467-S15"],
        ["accessibility/authentication-contract.json", "accessibility/authentication-mutations.json"],
        "Positive and negative fixtures must cover cognitive tests, alternatives, mechanisms, paste, password-manager declarations, redundant entry, exceptions, and explicit manual and security reservations.",
        "Mark the structure incomplete, retain failures, restore an accessible alternative and nonredundant path, and require qualified manual browser, assistive-technology, cognitive-accessibility, security, privacy, Māori-language, and affected-user evaluation.",
        ["accessibility_complete", "runtime_authentication", "security_review", "privacy_review", "assistive_technology", "affected_user_acceptance"],
        "completed",
        "Earlier accessibility proposals cover focus, tables, charts, forms, dragging, target size, reflow, dialogs, and language; none centers WCAG 2.2 accessible authentication and redundant entry together.",
    ),
    proposal(
        9,
        "Thermo/Psyche Le Chatelier equilibrium-perturbation, reaction-quotient, and resilience-nonconversion classifier",
        "declared equilibrium, reaction quotient, equilibrium constant, temperature, pressure, volume, concentration, inert addition, catalyst, phase, response direction, new equilibrium, applicability, and category barrier",
        "A typed classifier can check bounded equilibrium perturbation logic while rejecting conversion of chemical response into human resilience, autonomy, identity, justice, or consciousness claims.",
        "The system is not at equilibrium, Q and K are confused, temperature changes K silently, catalysts are said to shift equilibrium, inert additions are generalized, phases are omitted, or chemical response becomes psyche evidence.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["V6467-S16", "V6467-S17"],
        ["thermo-psyche/le-chatelier-contract.json", "thermo-psyche/le-chatelier-mutations.json"],
        "Fixtures must enforce declared equilibrium, Q-versus-K reasoning, perturbation type, phase and constraint scope, catalyst nonshift, applicability refusal, and the psyche category barrier.",
        "Restore the chemical-equilibrium domain and explicit assumptions, retain the rejection, and require independently valid human theory, measures, authority, and participant evidence before any human inference.",
        ["participant_inference", "psyche_claim", "resilience_claim", "autonomy_claim", "justice_claim", "consciousness", "fundamental_law"],
        "completed",
        "The chain covers Gibbs-Duhem, Gibbs phase rule, Clapeyron, Maxwell, Onsager, Crooks, Joule-Thomson, and entropy relations; no prior title centers Le Chatelier reaction-quotient perturbation with a resilience nonconversion barrier.",
    ),
    proposal(
        10,
        "Stage 20 MNAR sensitivity, tipping-point, multiple-imputation, and estimand nonpromotion board",
        "estimand, intercurrent event, missingness pattern, MAR reference, MNAR departure, delta adjustment, tipping point, imputation model, number of imputations, seed, pooling rule, uncertainty, decision authority, and terminal abstention",
        "A fail-closed structural board can quarantine completion credit when missing-data assumptions, sensitivity range, estimand, uncertainty, or decision authority are absent or changed after exposure.",
        "Missingness is assumed ignorable without argument, the estimand changes, delta ranges are selected post hoc, imputation uncertainty disappears, a tipping point becomes proof, or Stage 20 advances.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6467-S18"],
        ["stage20/mnar-sensitivity-contract.json", "stage20/mnar-sensitivity-mutations.json"],
        "Mutations must reject absent estimands, hidden missingness assumptions, post-exposure delta selection, incompatible imputation models, missing uncertainty, unsupported tipping-point promotion, and Stage 20 advancement.",
        "Withdraw affected evidence credit, retain the analysis assumptions and failure, require preregistered sensitivity ranges and governed decision criteria plus independent evaluation, and abstain.",
        ["stage20", "participant_evidence", "decision_authority", "independent_reproduction", "deployment", "proof_or_canon"],
        "completed",
        "The chain includes optional stopping, analytic multiverses, decision curves, metric semantics, contamination, Goodhart, and calibration boards but no title centered MNAR sensitivity, tipping points, and multiple-imputation estimand preservation.",
    ),
]


SOURCES = [
    {"source_id": "V6467-S01", "title": "Kubernetes Leases", "url": "https://kubernetes.io/docs/concepts/architecture/leases/", "publisher": "Kubernetes", "status": "current", "source_class": "official_documentation", "use": "lease holder, renewal, and coordination vocabulary only"},
    {"source_id": "V6467-S02", "title": "etcd concurrency API reference", "url": "https://etcd.io/docs/v3.5/dev-guide/api_concurrency_reference_v3/", "publisher": "etcd", "status": "current", "source_class": "official_documentation", "use": "bounded lease and election terminology only"},
    {"source_id": "V6467-S03", "title": "Exact evolution equation for the effective potential", "url": "https://doi.org/10.1016/0370-2693(93)90726-X", "publisher": "Physics Letters B", "status": "stable", "source_class": "primary_research", "use": "Wetterich flow provenance and obligation vocabulary"},
    {"source_id": "V6467-S04", "title": "Exact evolution equation for the effective potential author manuscript", "url": "https://arxiv.org/abs/1710.05815", "publisher": "arXiv", "status": "stable", "source_class": "primary_research", "use": "cross-check flow notation; no GMUT empirical data"},
    {"source_id": "V6467-S05", "title": "All-sky point-source IceCube data: years 2008-2018", "url": "https://icecube.wisc.edu/data-releases/2021/01/all-sky-point-source-icecube-data-years-2008-2018/", "publisher": "IceCube Collaboration", "status": "current", "source_class": "official_data_release_description", "use": "zero-row release and response requirements only"},
    {"source_id": "V6467-S06", "title": "Time-Integrated Neutrino Source Searches with 10 Years of IceCube Data", "url": "https://arxiv.org/abs/1910.08488", "publisher": "IceCube Collaboration", "status": "stable", "source_class": "primary_research", "use": "published analysis context only; not imported observation"},
    {"source_id": "V6467-S07", "title": "ICS Forms", "url": "https://www.nwcg.gov/publications/ics-forms1", "publisher": "National Wildfire Coordinating Group", "status": "current", "source_class": "official_operational_reference", "use": "synthetic situation-report and handover field vocabulary only"},
    {"source_id": "V6467-S08", "title": "Emergency Alerts", "url": "https://www.fireandemergency.nz/alerts/", "publisher": "Fire and Emergency New Zealand", "status": "current", "source_class": "official_public_guidance", "use": "alert-channel and authority reservation vocabulary only"},
    {"source_id": "V6467-S09", "title": "Climate and Wildfire Risk Evidence Brief", "url": "https://www.fireandemergency.nz/assets/Documents/Research-and-reports/Report-205-Climate-and-Wildfire-Risk-Evidence-Brief-2023.pdf", "publisher": "Fire and Emergency New Zealand", "status": "stable", "source_class": "official_evidence_brief", "use": "wildfire and evacuation context only; no real incident input"},
    {"source_id": "V6467-S10", "title": "RFC 9396 OAuth 2.0 Rich Authorization Requests", "url": "https://www.rfc-editor.org/rfc/rfc9396.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "synthetic authorization_details structure only"},
    {"source_id": "V6467-S11", "title": "Principles of Māori Data Sovereignty", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "publisher": "Te Mana Raraunga", "status": "current", "source_class": "maori_authority_source", "use": "authority and data-governance gate; not delegated authority"},
    {"source_id": "V6467-S12", "title": "Sharing Māori data", "url": "https://dns.govt.nz/standards-and-guidance/information-sharing-standard/maori-data", "publisher": "New Zealand Digital Government", "status": "current", "source_class": "official_guidance", "use": "public-service governance context; not case authority"},
    {"source_id": "V6467-S13", "title": "RFC 9110 HTTP Semantics", "url": "https://www.rfc-editor.org/rfc/rfc9110.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "Range, ETag, If-Range, and response semantics"},
    {"source_id": "V6467-S14", "title": "RFC 9530 Digest Fields", "url": "https://www.rfc-editor.org/rfc/rfc9530.html", "publisher": "IETF RFC Editor", "status": "stable", "source_class": "official_standard", "use": "Content-Digest and Repr-Digest vocabulary"},
    {"source_id": "V6467-S15", "title": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "publisher": "W3C", "status": "current", "source_class": "official_standard", "use": "accessible-authentication and redundant-entry structure only"},
    {"source_id": "V6467-S16", "title": "IUPAC Gold Book chemical equilibrium", "url": "https://goldbook.iupac.org/terms/view/C01023/PDF", "publisher": "IUPAC", "status": "stable", "source_class": "official_terminology", "use": "chemical-equilibrium domain and nonconversion boundary"},
    {"source_id": "V6467-S17", "title": "Chemistry 2e shifting equilibria", "url": "https://openstax.org/books/chemistry-2e/pages/13-3-shifting-equilibria-le-chateliers-principle", "publisher": "OpenStax", "status": "stable", "source_class": "authoritative_open_text", "use": "bounded perturbation examples only"},
    {"source_id": "V6467-S18", "title": "ICH E9(R1) Estimands and Sensitivity Analysis", "url": "https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf", "publisher": "International Council for Harmonisation", "status": "stable", "source_class": "official_guideline", "use": "estimand and sensitivity-analysis obligations only"},
]


SAFE_TASK_TITLES = [
    "Reconcile all 450 inherited proposal records before novelty credit",
    "Build exact normalized-title and token-overlap collision audit",
    "Verify eighteen source records use current stable draft or watch status",
    "Preserve official-source observation-to-data firewall",
    "Validate phase-local Method Flow schema and failure retention",
    "Build exact x1 staged-file allowlist review",
    "Run five-class x1 privacy and raw-identifier scan",
    "Verify primary-focus and bounded-practice authority boundary",
    "Verify owner-generated footprint remains below rotation threshold",
    "Record verify-only Codex Python and Git versions",
    "Audit Windows Sandbox capability read-only without elevation",
    "Guard four allowed outcome labels and expected distribution",
    "Reconcile fifteen open gaps and sixteen exact gates",
    "Reconcile 2,977 inherited negatives plus x1 additions",
    "Keep terminal route PREPARED_NOT_SENT before exact final proof",
    "Build fencing-token positive fixture contract",
    "Build functional-RG typed obligation fixture contract",
    "Build IceCube zero-row receipt schema",
    "Build wildfire handover synthetic trace schema",
    "Build OAuth RAR synthetic vector schema",
    "Build wildfire authority reservation matrix schema",
    "Build HTTP partial-resume disposable fixture",
    "Build accessible-authentication structural fixture",
    "Build Le Chatelier typed-domain fixture",
    "Build MNAR sensitivity nonpromotion fixture",
    "Build accessible static report semantics",
    "Enforce deterministic JSON ordering and UTF-8",
    "Use Git-blob line-ending-independent content identity",
    "Preserve family-current caller compatibility",
    "Emit owner workload and wellbeing boundary receipt",
]

CANDIDATE_TITLES = [
    "Split-brain fencing mutation generator",
    "Lease-expiry and clock-uncertainty boundary generator",
    "Functional-RG regulator omission mutation prototype",
    "Regulator-sensitive Ward-identity incompatibility prototype",
    "IceCube incompatible-release mix quarantine prototype",
    "IceCube background and trial-factor lock prototype",
    "Wildfire evacuation-zone revision replay prototype",
    "Wildfire handover workload-parity prototype",
    "OAuth RAR unsupported-type rejection prototype",
    "OAuth RAR privilege-widening quarantine prototype",
    "Wildfire alert confidentiality matrix prototype",
    "Evacuation accessibility reservation prototype",
    "HTTP changed-ETag resume refusal prototype",
    "HTTP range overlap and gap detector prototype",
    "HTTP digest-algorithm mismatch prototype",
    "Accessible authentication copy-paste structural checker",
    "Redundant-entry exception classifier prototype",
    "Le Chatelier reaction-quotient mutation prototype",
    "Equilibrium and metastability applicability guard prototype",
    "MNAR tipping-point grid nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-fencing-token-tribunal", "Audit bounded fencing-token and split-brain traces"),
    ("ghc-family-functional-rg-obligations", "Audit functional-RG regulator and truncation duties"),
    ("ghc-family-icecube-zero-row", "Preserve a zero-row IceCube study boundary"),
    ("ghc-family-wildfire-handover-proxy", "Audit synthetic wildfire shift-handover traces"),
    ("ghc-family-oauth-rar-profile", "Audit synthetic OAuth rich authorization details"),
    ("ghc-family-wildfire-authority-reservation", "Reserve wildfire warning and Māori authority gates"),
    ("ghc-family-http-range-resume-integrity", "Audit local HTTP range-resume integrity fixtures"),
    ("ghc-family-accessible-authentication-audit", "Audit authentication and redundant-entry structure"),
    ("ghc-family-le-chatelier-domain-guard", "Keep equilibrium logic inside its chemical domain"),
    ("ghc-family-mnar-sensitivity-nonpromotion", "Guard missing-data sensitivity from promotion"),
    ("ghc-family-source-observation-firewall", "Keep citations distinct from observations and data"),
    ("ghc-family-proposal-novelty-audit", "Audit proposal-title and semantic-neighbor novelty"),
    ("ghc-family-x1-git-blob-seal", "Seal x1 content using exact Git blobs"),
    ("ghc-family-phase-commit-budget", "Enforce x1 and x2 commit budgets"),
    ("ghc-family-method-failure-retention", "Retain failed workflow witnesses before recovery"),
    ("ghc-family-five-class-privacy-scan", "Scan public phase files across five privacy classes"),
    ("ghc-family-deterministic-json-contract", "Keep generated JSON deterministic and UTF-8"),
    ("ghc-family-line-ending-hash-domain", "Separate Git-blob and checkout hash domains"),
    ("ghc-family-static-report-evaluation-reservation", "Reserve manual evaluation in static reports"),
    ("ghc-family-terminal-route-acknowledgement-gate", "Gate and send exactly one terminal baton"),
]

RUNNER_TITLES = [
    "ghc_family_fencing_token_tribunal.py",
    "ghc_family_functional_rg_obligations.py",
    "ghc_family_icecube_zero_row.py",
    "ghc_family_wildfire_handover_proxy.py",
    "ghc_family_oauth_rar_profile.py",
    "ghc_family_http_resume_integrity.py",
    "ghc_family_accessible_auth_auditor.py",
    "ghc_family_le_chatelier_domain.py",
    "ghc_family_mnar_sensitivity_board.py",
    "ghc_family_v646_v7_validation_runner.py",
]

CLEAN_TASK_TITLES = [
    "Reconcile proposal and outcome counts across all receipts",
    "Reconcile retained-negative counts after every ledger growth",
    "Reconcile Method Flow counts and validator expectations together",
    "Remove stale phase labels through additive correction only",
    "Preserve compatibility callers while selecting family-current tools",
    "Normalize generated JSON key ordering",
    "Normalize generated UTF-8 and LF authoring",
    "Keep Git-blob and checkout byte hash domains explicit",
    "Review all public files for private absolute paths",
    "Review all public files for raw task or thread identifiers",
    "Review all public files for credentials or token assignments",
    "Review source statuses for current stable draft or watch vocabulary",
    "Review citations for observation and data nonconversion",
    "Review x1 staged files for x2 contamination",
    "Review x2 outcomes for four-class vocabulary only",
    "Review exact and blocked packets for zero execution credit",
    "Review owner footprint against the 15,000-file threshold",
    "Review report title main table caption and focus structure",
    "Review report manual and affected-user reservations",
    "Review Māori authority and data-governance reservations",
    "Review emergency and professional authority reservations",
    "Review real-data and likelihood counters remain zero",
    "Review real-person and operational counters remain zero",
    "Review real-key token and authorization counters remain zero",
    "Review source x1 evidence and seal ancestry",
    "Review phase commit cap and zero-merge history",
    "Review validation branch remains local-only and named",
    "Review canonical four-way remote equality",
    "Refresh phase-scoped GHC Family Index after new tools",
    "Refresh wellbeing and terminal-route state before handoff",
]

EXACT_PACKET_TITLES = [
    "Real IceCube data download and likelihood execution",
    "Real wildfire incident or evacuation decision",
    "Public emergency alert or warning mutation",
    "Production OAuth authorization or token exchange",
    "Real identity key proof or consent operation",
    "Legal interpretation or remedy allocation",
    "Māori authority or data-governance decision",
    "Production deployment or security certification",
    "Independent-team scientific reproduction claim",
    "Stage 20 promotion proof or canon decision",
]

BLOCKED_PACKET_TITLES = [
    "Force-push or rewrite canonical history",
    "Delete or mutate a sibling-owned lane",
    "Expose credentials private routes or raw task identifiers",
    "Enable Windows features weaken security or elevate without a new exact gate",
    "Claim consciousness personhood AGI ASI or Theory-of-Everything closure",
]

X1_OPERATIONAL_NEGATIVES = [
    {"negative_id": "V6467-X1-N01", "method_id": "V6467-M01", "summary": "A frozen-index probe assumed the wrong proposal collection and emitted a null-array error.", "retained": True, "recovered": True},
    {"negative_id": "V6467-X1-N02", "method_id": "V6467-M02", "summary": "A PowerShell foreach-to-JSON pipeline failed at parse time before novelty comparison.", "retained": True, "recovered": True},
    {"negative_id": "V6467-X1-N03", "method_id": "V6467-M03", "summary": "Two login-shell inspection probes exceeded their ten-second wrapper ceiling before returning filesystem evidence.", "retained": True, "recovered": True},
    {"negative_id": "V6467-X1-N04", "method_id": "V6467-M04", "summary": "A Method Flow refresh supplied an unsupported validate --output option after the ledger mutation had succeeded.", "retained": True, "recovered": True},
    {"negative_id": "V6467-X1-N05", "method_id": "V6467-M05", "summary": "The first expanded-portfolio audit found two exact inherited skill-name collisions and stopped before materialization.", "retained": True, "recovered": True},
]
