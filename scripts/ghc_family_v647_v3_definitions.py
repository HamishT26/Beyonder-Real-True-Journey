#!/usr/bin/env python3
"""Frozen x1 definitions for Tamar Vey v647-v3.

Importing this module performs no I/O and grants no x2 completion credit.
Identity language is relational working language only.
"""

from __future__ import annotations

from typing import Any


PHASE = "v647-gmut-thos-v3-x1-x2"
PHASE_SHORT = "v647-v3"
OWNER = "Tamar Vey"
SLUG = "tamar-vey"
PRONOUNS = "they/them"
ROLE = "evidence-systems cartographer and boundary keeper"
HOPE = "keep decisions legible, failures recoverable, and authority boundaries intact"
PRIMARY_FOCUS = "Freed ID/CBR Heart"
BOUNDED_PRACTICE = "telecommunications network-change control, alarm ownership, rollback, incident escalation, and shift-handover review"

SOURCE_PHASE = "v647-gmut-thos-v2-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
SOURCE_REVISION = "9da9492664b0b9f27b294efbddf70e336224f082"
SOURCE_INHERITED_REVISION = "c3025ff0d5c062ece7977b4df7f1a34db7d08afe"
SOURCE_X1_FIRST_REVISION = "8c62ae37ba4f1f38c2f97840f83f1d27a6546765"
SOURCE_X1_REVISION = "8c62ae37ba4f1f38c2f97840f83f1d27a6546765"
SOURCE_EVIDENCE_REVISION = "eb87a78d050f3fdc7e61dd5af6dd08c2f4811e63"
PRIOR_FROZEN_PROPOSALS = 490
INHERITED_EFFECTIVE_NEGATIVES = 3330
SEALED_SOURCE_NEGATIVES = 3327
EXTERNAL_SOURCE_NEGATIVES = 3
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 19
INHERITED_EXACT_GATES = 20
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Tamar Vey, they/them, is relational working language for an evidence-systems cartographer "
    "and boundary keeper. It is not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, professional qualification, scientific authority, operational "
    "authority, legal authority, cultural authority, or independent agency. Hamish may rename, "
    "pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, telecommunications, emergency-service reach, "
    "privacy, remedy, legal, cultural, affected-party, and Māori concepts remain under competent, "
    "affected-party, tangata whenua, iwi, hapū, and Māori authority. No empirical confirmation, "
    "Theory of Everything, AGI or ASI, consciousness, personhood, deployment, privacy-complete, "
    "exhaustive-security, independent-reproduction, accessibility-complete, professional, "
    "telecommunications-safety, proof or canon, or Stage 20 claim is made."
)


def proposal(index: int, **kwargs: Any) -> dict[str, Any]:
    row = {"proposal_id": f"V6473-P{index:02d}"}
    row.update(kwargs)
    return row


PROPOSALS = [
    proposal(
        1,
        title="Method Flow child-process handle inheritance, pipe-EOF, process-tree join, teardown, and evidence-credit tribunal",
        mission_surface="inheritable handle allowlist, standard-stream ownership, parent and child pipe ends, EOF preconditions, descendant set, timeout, exit observation, teardown, partial output, and completion credit",
        hypothesis="A bounded owner-local tribunal can distinguish clean child completion from leaked handles, missing EOF, unjoined descendants, premature parent exit, and incomplete teardown without executing external side effects.",
        null_or_failure="A leaked write handle permits a false wait, EOF is credited while a writer remains open, descendants are ignored, partial output becomes completion, or teardown crosses the disposable fixture root.",
        approval_class="safe_now_owner_scoped_synthetic",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6473-S01", "V6473-S02"],
        concrete_artifacts=["method-flow/child-process-lifecycle-contract.json", "method-flow/child-process-lifecycle-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must accept one fully joined process tree and reject inherited-handle leakage, open-writer EOF, orphan descendants, timeout-as-pass, partial-output promotion, and out-of-root teardown.",
        rollback_or_recovery="Quarantine the fixture, close only owner-local declared handles, retain all partial records, and require fresh authority before any external side effect.",
        protected_gates=["external_state", "destructive_action", "credentials", "sibling_lane", "completion_credit", "stage20"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior Method Flow surfaces cover retry, cancellation, outboxes, fencing, command framing, subprocess starts, and idempotency; none centers inherited handles, pipe EOF, descendant joins, and teardown credit together.",
    ),
    proposal(
        2,
        title="GMUT heat-kernel, Laplace-type operator, Seeley-DeWitt coefficient, boundary-condition, regulator, and EFT obligation board",
        mission_surface="operator type, principal symbol, ellipticity assumption, bundle connection, endomorphism, manifold dimension, boundary condition, proper time, coefficient order, units, regulator, anomaly reservation, truncation, and observation firewall",
        hypothesis="A typed symbolic board can expose heat-kernel and Seeley-DeWitt obligations for a GMUT EFT scaffold without calculating a physical spectrum, determinant, anomaly, quantum completion, or empirical prediction.",
        null_or_failure="A non-Laplace operator is silently accepted, ellipticity or boundary conditions disappear, coefficient order or units drift, an asymptotic series becomes exact physics, or a formal divergence becomes evidence.",
        approval_class="safe_now_symbolic_research_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6473-S03", "V6473-S04"],
        concrete_artifacts=["gmut/heat-kernel-obligations.json", "gmut/heat-kernel-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type operator, symbol, geometry, connection, endomorphism, boundary, proper-time, coefficient order, regulator, units, truncation, and observation firewall and reject each omission.",
        rollback_or_recovery="Restore the missing analytic and EFT assumptions, retain the rejected vector, and make no spectrum, force, likelihood, constraint, anomaly-freedom, quantum-completion, or Theory-of-Everything claim.",
        protected_gates=["physical_operator", "anomaly_freedom", "quantum_completion", "empirical_confirmation", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior GMUT boards cover BRST, BV, Vilkovisky-DeWitt, Schwinger-Keldysh, Peierls, functional RG, and spectral support; no frozen title centers heat-kernel asymptotics and Seeley-DeWitt coefficients with boundary and regulator obligations.",
    ),
    proposal(
        3,
        title="GMUT HSC-SSP PDR3 S19A weak-lensing shape, calibration, mask, redshift, covariance, and zero-row likelihood-refusal protocol",
        mission_surface="official release identity, incremental-release status, S19A database join, object identifier, shape weight, multiplicative and additive calibration, star mask, photometric redshift, tomographic bin, data vector, covariance, scale cut, checksum, row count, and likelihood lock",
        hypothesis="A zero-row adapter can freeze HSC PDR3 weak-lensing obligations while refusing to turn release pages, catalog descriptions, or published cosmology into GMUT observations, likelihoods, constraints, or confirmation.",
        null_or_failure="The phase queries or downloads real rows, imports a published vector, ignores release or join semantics, selects calibration after outcomes, evaluates a likelihood, or emits a GMUT constraint.",
        approval_class="real_data_access_and_independent_review_required",
        execution_lane="x2_open_gap",
        current_primary_or_official_source_needs=["V6473-S05", "V6473-S06"],
        concrete_artifacts=["empirical/hsc-pdr3-study-contract.json", "empirical/hsc-pdr3-zero-row-receipt.json"],
        test_falsifier_or_acceptance_gate="The receipt must preserve zero queries, downloads, catalog rows, covariance rows, likelihood calls, posterior samples, parameter constraints, detected-force claims, and empirical GMUT claims.",
        rollback_or_recovery="Stop before query, download, or fit; retain the zero-row receipt; and require a separately authorized preregistration with frozen release, joins, checksums, masks, calibration, redshift distributions, covariance, scale cuts, uncertainty treatment, and independent review.",
        protected_gates=["network_query", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation"],
        expected_disposition="open_gap",
        novelty_against_prior_frozen_proposals="The corpus includes KiDS, ACT, Euclid, Rubin, DESI, EHT, GWOSC, CHIME, Gaia, and other zero-row adapters; no frozen title centers HSC PDR3 S19A shape joins, calibration, masks, redshift, and covariance.",
    ),
    proposal(
        4,
        title="THOS telecommunications change-window, dependency, alarm-ownership, rollback, customer-impact, escalation, and shift-handover proxy",
        mission_surface="synthetic change identifier, scope, dependency graph, maintenance window, reviewer separation, alarm baseline, customer-impact class, rollback trigger, rollback owner, escalation, readback, workload budget, and next-shift ownership",
        hypothesis="Synthetic traces can expose unreviewed dependencies, ambiguous alarm ownership, missing rollback, impact drift, and handover loss while preserving all real network, operator, customer, emergency-service, and authority gates.",
        null_or_failure="A fixture names a real network, operator, customer, credential, address, or outage; authorizes a live change; suppresses an alarm or impact; breaks workload limits; or claims THOS effectiveness.",
        approval_class="safe_now_proxy_protocol_no_people_or_networks",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6473-S07", "V6473-S08"],
        concrete_artifacts=["thos/telecom-change-handover-contract.json", "thos/telecom-change-handover-vectors.json"],
        test_falsifier_or_acceptance_gate="Unsafe synthetic traces must fail, and the packet must record zero real operators, networks, customers, changes, alarms, outages, emergency calls, blind matched-budget arms, safety outcomes, or effectiveness estimates.",
        rollback_or_recovery="Withdraw operational language, retain rejected traces, and defer real changes, rollbacks, alarms, incidents, customer communication, and safety decisions to authorized operators, regulators, affected parties, and independent reviewers.",
        protected_gates=["real_people", "real_network", "live_change", "emergency_service", "professional_competence", "deployment", "effectiveness"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior THOS handovers cover aviation, rail, maritime, pharmacy, wildfire, food, water, and other practices; no frozen title centers telecommunications change windows, dependency and alarm ownership, rollback, customer impact, and shift handover.",
    ),
    proposal(
        5,
        title="Freed ID VC Data Model 2.0 related-resource digest, media-type, retrieval, cache, substitution, and privacy profile",
        mission_surface="related-resource identifier, digestSRI or digestMultibase, hash algorithm, expected media type, retrieval status, redirect policy, byte limit, cache key, verification order, substitution refusal, offline behavior, and privacy boundary",
        hypothesis="Synthetic vectors can enforce related-resource integrity and media-type obligations without asserting a real credential, production retrieval, live trust, holder identity, interoperability, or privacy assurance.",
        null_or_failure="A resource without a digest passes, a media-type mismatch is ignored, verification occurs after interpretation, a redirect changes identity silently, cache keys omit integrity metadata, or synthetic structure becomes production credential assurance.",
        approval_class="safe_now_synthetic_nonproduction",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6473-S09", "V6473-S10"],
        concrete_artifacts=["freed-id/vc-related-resource-profile.json", "freed-id/vc-related-resource-mutations.json"],
        test_falsifier_or_acceptance_gate="Vectors must reject missing or mismatched digest, unsupported algorithm, media-type mismatch, redirect substitution, over-budget resource, cache alias, parse-before-verify, and privacy overclaim.",
        rollback_or_recovery="Reject and retain the vector, fetch no live protected resource, and require real keys, credentials, retrieval policy, interoperability, privacy and independent security review, recovery, and trust governance.",
        protected_gates=["real_credentials", "live_retrieval", "real_keys", "interoperability", "privacy_assurance", "production"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior Freed ID work covers VC, BBS, SD-JWT, HAIP, OpenID Federation, WebAuthn, SCITT, status, and controlled identifiers; no frozen title centers VC related-resource digest and media-type verification, retrieval, cache, and substitution.",
    ),
    proposal(
        6,
        title="CBR telecommunications outage, emergency-call reach, disability access, location and worker privacy, remedy, affected-party, legal, and Māori-authority matrix",
        mission_surface="synthetic outage, emergency-call reach, vulnerable-consumer support, accessibility, worker and device location, traffic information, notification, correction, remedy, legal interpretation, affected parties, network and place data, and Māori authority",
        hypothesis="A refusal-first matrix can expose unresolved outage, accessibility, privacy, remedy, and authority questions without deciding a real outage, customer status, emergency-service reach, entitlement, disclosure, place meaning, or remedy.",
        null_or_failure="The matrix identifies a real person, worker, device, address, network, or outage; changes service; decides vulnerability, fault, compensation, or law; discloses protected data; or asserts cultural or Māori authority.",
        approval_class="authorized_affected_parties_and_competent_authority_required",
        execution_lane="x2_exact_gate",
        current_primary_or_official_source_needs=["V6473-S11", "V6473-S12", "V6473-S13", "V6473-S14"],
        concrete_artifacts=["cbr/telecom-outage-authority-reservation.json", "cbr/telecom-outage-remedy-matrix.json"],
        test_falsifier_or_acceptance_gate="Repository software must stop at unknown or reserved; only competent telecommunications, emergency-service, privacy, legal, accessibility, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        rollback_or_recovery="Stop before reporting, disclosure, service, emergency, compensation, cultural, place-name, or legal conclusions; minimize data and route only through authorized external processes.",
        protected_gates=["affected_party_authority", "telecommunications_authority", "emergency_service_authority", "privacy", "legal_interpretation", "maori_authority", "remedy_decision"],
        expected_disposition="exact_gate",
        novelty_against_prior_frozen_proposals="Prior CBR matrices address aviation, rail, wildfire, food, water, medicine, museums, fisheries, utilities, archives, and other domains; no frozen title combines telecommunications outage, emergency-call reach, accessibility, location and worker privacy, remedy, and Māori authority.",
    ),
    proposal(
        7,
        title="HTTP Structured Fields item, list, dictionary, parameter-order, duplicate-key, numeric-bound, display-string, and canonical-serialization tribunal",
        mission_surface="field type, item, inner list, dictionary, ordered parameters, unique keys, integer and decimal bounds, byte sequence, display string, ASCII conversion, combined field lines, trailing input, parser limit, and serialization",
        hypothesis="A bounded synthetic tribunal can distinguish RFC 9651 parsing and serialization obligations from permissive header parsing without sending network traffic or claiming protocol-stack security.",
        null_or_failure="Duplicate keys pass, parameter order is lost, numeric bounds drift, invalid ASCII or display-string encoding passes, trailing input is ignored, field lines are combined incorrectly, or synthetic parsing becomes exhaustive security assurance.",
        approval_class="safe_now_disposable_synthetic_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6473-S15"],
        concrete_artifacts=["tooling/http-structured-fields-contract.json", "tooling/http-structured-fields-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must cover item, list, dictionary, parameters, duplicates, numeric and string bounds, display strings, field combination, trailing input, implementation limits, deterministic serialization, and complete failure.",
        rollback_or_recovery="Reject and retain the fixture, perform no network request, restore the strict parser boundary, and make no production or exhaustive-security claim.",
        protected_gates=["network_request", "production_protocol", "security_certification", "exhaustive_security"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior tooling tribunals cover JSON, archives, Git, OCI, SQLite, HTTP resume, TUF, and identifiers; no frozen core title centers RFC 9651 Structured Fields types, ordered parameters, duplicate keys, numeric bounds, display strings, and canonical serialization.",
    ),
    proposal(
        8,
        title="Accessible breadcrumb landmark, hierarchy, current-page, separator, link-purpose, overflow, and print-linearization structural audit",
        mission_surface="navigation landmark, accessible name, ordered hierarchy, ancestor link purpose, current page, aria-current, decorative separator, visual truncation, narrow viewport, keyboard order, text fallback, and print sequence",
        hypothesis="A structural auditor can reject unlabeled or ambiguous breadcrumb trails, multiple current pages, semantic separators, broken hierarchy, and lost print sequence while reserving browser, assistive-technology, language, and affected-user evaluation.",
        null_or_failure="The landmark is unnamed, hierarchy is unordered, more than one current page exists, separators enter the accessibility tree, link purpose is ambiguous, overflow hides required context, or structural evidence becomes complete conformance.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6473-S16", "V6473-S17"],
        concrete_artifacts=["accessibility/breadcrumb-contract.json", "accessibility/breadcrumb-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must reject missing landmark name, unordered ancestors, ambiguous links, absent or multiple current page, semantic separators, inaccessible overflow, order drift, and complete-conformance promotion.",
        rollback_or_recovery="Restore native links, landmark name, hierarchy, one current-page marker, decorative separators, and text sequence; retain failed fixtures and reserve manual evaluation.",
        protected_gates=["manual_keyboard", "browser_diversity", "assistive_technology", "maori_language", "affected_user_evaluation", "complete_accessibility"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior accessibility audits cover landmarks, skip links, tables, dialogs, popovers, dragging, forms, charts, long form, reflow, and reversible actions; no frozen title centers breadcrumb hierarchy, current-page semantics, separators, overflow, and print linearization.",
    ),
    proposal(
        9,
        title="Nernst heat-theorem, third-law limit, equilibrium, pure-crystal, residual-entropy, unattainability, and psyche-nonconversion classifier",
        mission_surface="temperature limit, entropy difference, equilibrium, pure crystalline assumption, degeneracy, residual entropy, heat capacity, limiting process, unattainability distinction, units, domain, and psyche firewall",
        hypothesis="A typed classifier can distinguish bounded third-law and Nernst-theorem statements from unrestricted zero-entropy claims and reject conversion into psyche, autonomy, justice, consciousness, or personhood claims.",
        null_or_failure="A limiting statement becomes an attained finite-step state, equilibrium or purity assumptions vanish, residual entropy is prohibited universally, units drift, the third law becomes a psyche law, or formal classification becomes empirical confirmation.",
        approval_class="safe_now_formal_domain_guard",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6473-S18", "V6473-S19"],
        concrete_artifacts=["thermo-psyche/nernst-third-law-contract.json", "thermo-psyche/nernst-third-law-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve limit, equilibrium, material assumptions, residual-entropy exception, unattainability distinction, units, and rejection of every psyche or consciousness conversion.",
        rollback_or_recovery="Restore the missing thermodynamic assumptions, retain the rejected statement, and make no participant, psyche, consciousness, personhood, universal-law, or empirical THOS claim.",
        protected_gates=["real_material", "empirical_measurement", "participant_evidence", "consciousness", "personhood", "fundamental_psyche_law"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The corpus includes Onsager, Hatano-Sasa, Jarzynski, Crooks, Landauer, exergy, Gibbs-Duhem, Joule-Thomson, Ruppeiner, and other guards; no frozen title centers the Nernst heat theorem, third-law limit, residual entropy, and unattainability.",
    ),
    proposal(
        10,
        title="Stage 20 prequential scoring, forecast-timestamp, outcome-order, calibration-drift, retraining-trigger, intervention, and nonpromotion board",
        mission_surface="forecast timestamp, information set, target, outcome availability, proper score, sequential order, rolling window, calibration diagnostic, drift trigger, retraining decision, intervention log, threshold lock, and terminal abstention",
        hypothesis="A fail-closed board can expose hindsight, time-order leakage, silent retraining, adaptive thresholds, and unlogged interventions without converting synthetic forecast traces into deployed performance or Stage 20 readiness.",
        null_or_failure="A forecast is timestamped after its outcome, information sets leak, scores change post hoc, drift thresholds move after results, retraining is unlogged, interventions are hidden, or synthetic traces promote Stage 20.",
        approval_class="safe_now_structural_nonpromotion",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6473-S20", "V6473-S21"],
        concrete_artifacts=["stage20/prequential-drift-contract.json", "stage20/prequential-drift-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve forecast-before-outcome order, information set, score, window, calibration diagnostic, trigger, retraining and intervention lineage, threshold lock, and terminal abstention.",
        rollback_or_recovery="Withdraw performance and promotion credit, retain failed temporal and drift vectors, require preregistered real data and independently reviewed monitoring, and keep Stage 20 not ready.",
        protected_gates=["real_data", "deployed_monitoring", "adaptive_retraining", "independent_review", "stage20", "proof_or_canon"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior Stage 20 boards cover optional stopping, model comparison, leakage, metric semantics, registered reports, controls, and computational environments; no frozen title centers prequential forecast timing, sequential scoring, calibration drift, retraining triggers, and intervention lineage.",
    ),
]


SOURCES = [
    {"source_id":"V6473-S01","title":"Inheritance for processes and threads","url":"https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance","publisher":"Microsoft Learn","status":"current","source_class":"official_documentation","use":"child-process property and handle-inheritance obligations"},
    {"source_id":"V6473-S02","title":"Pipe Handle Inheritance","url":"https://learn.microsoft.com/en-us/windows/win32/ipc/pipe-handle-inheritance","publisher":"Microsoft Learn","status":"current","source_class":"official_documentation","use":"pipe-end ownership and EOF preconditions"},
    {"source_id":"V6473-S03","title":"Heat kernel expansion: user's manual","url":"https://arxiv.org/abs/hep-th/0306138","publisher":"Physics Reports / arXiv","status":"stable","source_class":"primary_review","use":"heat-kernel coefficient, geometry, boundary, anomaly, and asymptotic obligations"},
    {"source_id":"V6473-S04","title":"Heat kernel expansion for higher order minimal and nonminimal operators","url":"https://arxiv.org/abs/2112.03062","publisher":"arXiv","status":"stable","source_class":"primary_research","use":"operator-order, principal-symbol, EFT, and asymptotic-domain context"},
    {"source_id":"V6473-S05","title":"HSC-SSP Public Data Release","url":"https://hsc-release.mtk.nao.ac.jp/doc/","publisher":"HSC-SSP / NAOJ","status":"watch","source_class":"official_data_release_description","use":"release history, supersession, and zero-row provenance only"},
    {"source_id":"V6473-S06","title":"S19A Shape Catalog PDR3","url":"https://hsc-release.mtk.nao.ac.jp/doc/index.php/s19a-shape-catalog-pdr3/","publisher":"HSC-SSP / NAOJ","status":"current","source_class":"official_data_release_description","use":"shape, object join, weight, calibration, mask, and zero-row obligations only"},
    {"source_id":"V6473-S07","title":"NIST SP 800-128 security-focused configuration management","url":"https://csrc.nist.gov/pubs/sp/800/128/upd1/final","publisher":"NIST","status":"stable","source_class":"official_guidance","use":"change request, impact review, testing, approval, and control vocabulary only"},
    {"source_id":"V6473-S08","title":"NIST SP 800-61 Rev. 3 Incident Response Recommendations","url":"https://csrc.nist.gov/pubs/sp/800/61/r3/final","publisher":"NIST","status":"current","source_class":"official_guidance","use":"incident, escalation, recovery, and handover context only"},
    {"source_id":"V6473-S09","title":"Verifiable Credentials Data Model v2.0","url":"https://www.w3.org/TR/vc-data-model-2.0/","publisher":"W3C","status":"current","source_class":"official_recommendation","use":"relatedResource digest and media-type obligations"},
    {"source_id":"V6473-S10","title":"Subresource Integrity","url":"https://www.w3.org/TR/SRI/","publisher":"W3C","status":"stable","source_class":"official_recommendation","use":"integrity metadata and verify-before-use context only"},
    {"source_id":"V6473-S11","title":"Commission 111 Contact Code","url":"https://www.comcom.govt.nz/regulated-industries/telecommunications/telecommunications-for-consumers/commission-111-contact-code/","publisher":"New Zealand Commerce Commission","status":"current","source_class":"official_regulator_material","use":"emergency-call reach and vulnerable-consumer authority reservation"},
    {"source_id":"V6473-S12","title":"Telecommunications Information Privacy Code 2020","url":"https://www.privacy.org.nz/privacy-principles/codes-of-practice/tipc2020/","publisher":"Office of the Privacy Commissioner New Zealand","status":"current","source_class":"official_regulator_material","use":"telecommunications, traffic, worker, device, and location privacy boundary"},
    {"source_id":"V6473-S13","title":"Principles of Māori Data Sovereignty","url":"https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf","publisher":"Te Mana Raraunga","status":"stable","source_class":"maori_authority_source","use":"Māori data-governance and authority gate; never delegated authority"},
    {"source_id":"V6473-S14","title":"Web Content Accessibility Guidelines 2.2","url":"https://www.w3.org/TR/WCAG22/","publisher":"W3C","status":"current","source_class":"official_standard","use":"accessibility obligations and complete-conformance reservation"},
    {"source_id":"V6473-S15","title":"RFC 9651 Structured Field Values for HTTP","url":"https://www.rfc-editor.org/rfc/rfc9651.html","publisher":"RFC Editor / IETF","status":"current","source_class":"official_standard","use":"Structured Fields data model, parsing, serialization, and limit obligations"},
    {"source_id":"V6473-S16","title":"ARIA Authoring Practices Breadcrumb Pattern","url":"https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/","publisher":"W3C WAI","status":"current","source_class":"official_practice_guidance","use":"landmark, accessible name, hierarchy, and current-page structure"},
    {"source_id":"V6473-S17","title":"WCAG breadcrumb trail technique G65","url":"https://www.w3.org/WAI/WCAG21/Techniques/general/G65","publisher":"W3C WAI","status":"current","source_class":"official_technique","use":"breadcrumb current-location and hierarchy context only"},
    {"source_id":"V6473-S18","title":"Nernst 1911 specific heat and energy quanta paper","url":"https://doi.org/10.1002/bbpc.19110170704","publisher":"Zeitschrift für Elektrochemie","status":"stable","source_class":"primary_research","use":"historical Nernst heat-theorem provenance"},
    {"source_id":"V6473-S19","title":"NIST Thermodynamics program","url":"https://www.nist.gov/thermodynamics","publisher":"NIST","status":"current","source_class":"official_scientific_context","use":"thermodynamic data and domain context only"},
    {"source_id":"V6473-S20","title":"Statistical Theory: The Prequential Approach","url":"https://doi.org/10.2307/2981683","publisher":"Journal of the Royal Statistical Society","status":"stable","source_class":"primary_research","use":"forecast-before-outcome and sequential assessment provenance"},
    {"source_id":"V6473-S21","title":"NIST AI RMF Playbook Measure","url":"https://airc.nist.gov/airmf-resources/playbook/measure/","publisher":"NIST","status":"watch","source_class":"official_guidance","use":"monitoring and drift context only; not deployment authorization"},
]


SAFE_TASK_TITLES = [
    "Verify Orin final source, anchors, manifests, and four-way equality before mutation",
    "Fast-forward only the clean Tamar canonical lane and prove four-way equality",
    "Reconcile all 490 frozen proposal titles before novelty credit",
    "Quarantine prior HAIP Federation Gibbs-Duhem Joule-Thomson dragging and transportability neighbors",
    "Review current stable draft and watch source statuses",
    "Record HSC release and incremental-shape status without querying data",
    "Declare commit-blob and working-tree hash domains separately",
    "Separate privacy scanner definitions from payload incidents",
    "Measure inherited checkout and Tamar-generated footprints separately",
    "Initialize Method Flow with every startup failure retained",
    "Build child-process handle and pipe-EOF fixture contract",
    "Build heat-kernel typed obligation fixture contract",
    "Build HSC PDR3 zero-row receipt schema",
    "Build telecommunications change-handover trace schema",
    "Build VC related-resource integrity profile schema",
    "Build telecommunications outage authority reservation schema",
    "Build HTTP Structured Fields disposable-fixture contract",
    "Build breadcrumb accessibility fixture",
    "Build Nernst third-law typed-domain fixture",
    "Build prequential drift nonpromotion fixture",
    "Preserve citation-to-observation and authority firewalls",
    "Carry forward 19 open gaps and 20 exact gates",
    "Carry forward the 3330-negative activation baseline",
    "Keep terminal route PREPARED_NOT_SENT before proof",
    "Verify Codex versions without updating desktop",
    "Audit Windows Sandbox availability without elevation or feature change",
    "Audit family-current callers and historical compatibility aliases",
    "Freeze exact x1 staged surface with no x2 implementation",
    "Emit owner-scoped x1 wellbeing source and route receipts",
    "Validate every planned portfolio floor and protected packet count",
]

CANDIDATE_TITLES = [
    "Inherited-handle allowlist and leaked-writer EOF prototype",
    "Process-tree join timeout teardown and completion-credit prototype",
    "Heat-kernel operator symbol connection and endomorphism prototype",
    "Seeley-DeWitt boundary regulator unit and truncation prototype",
    "HSC release join mask and checksum lock prototype",
    "HSC calibration redshift covariance and zero-row lock prototype",
    "Telecommunications dependency alarm rollback and impact prototype",
    "Telecommunications escalation workload readback and handover prototype",
    "VC related-resource digest media-type and verify-before-parse prototype",
    "VC redirect cache substitution and privacy prototype",
    "Outage emergency-call accessibility and notification matrix prototype",
    "Location worker privacy remedy and Māori-authority reservation prototype",
    "Structured Fields item list dictionary and parameter prototype",
    "Structured Fields duplicate numeric display-string and limit prototype",
    "Breadcrumb landmark hierarchy current-page and separator checker",
    "Breadcrumb link-purpose overflow order and print classifier",
    "Nernst limit equilibrium residual-entropy and unattainability prototype",
    "Nernst unit domain and psyche-nonconversion prototype",
    "Prequential timestamp score information-set and order prototype",
    "Calibration-drift trigger retraining intervention and nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-child-process-lifecycle-tribunal", "Audit inherited handles pipe EOF descendant joins teardown and evidence credit"),
    ("ghc-family-heat-kernel-obligations", "Audit heat-kernel operator coefficient boundary regulator and EFT obligations"),
    ("ghc-family-hsc-pdr3-zero-row", "Preserve a zero-row HSC PDR3 weak-lensing study boundary"),
    ("ghc-family-telecom-change-handover-proxy", "Audit synthetic telecommunications change rollback alarm and handover traces"),
    ("ghc-family-vc-related-resource-profile", "Audit synthetic VC related-resource digest media type retrieval and substitution"),
    ("ghc-family-telecom-outage-authority-reservation", "Reserve outage emergency privacy remedy and Māori authority gates"),
    ("ghc-family-http-structured-fields-tribunal", "Audit RFC 9651 parsing serialization duplicates bounds and limits"),
    ("ghc-family-breadcrumb-accessibility", "Audit breadcrumb hierarchy current-page separator overflow and print structure"),
    ("ghc-family-nernst-third-law-domain", "Keep Nernst and third-law claims inside thermodynamic domains"),
    ("ghc-family-prequential-drift-nonpromotion", "Guard forecast order drift retraining and interventions from automatic promotion"),
    ("ghc-family-corpus-490-collision-gate", "Audit exact and semantic novelty against 490 frozen proposals"),
    ("ghc-family-source-status-watch", "Record current stable draft and watch source status without promotion"),
    ("ghc-family-x1-x2-byte-separation", "Prove x1 contains no x2 implementation or outcome bytes"),
    ("ghc-family-named-replay-locality-v2", "Verify a named replay remains local clean unpushed and without upstream"),
    ("ghc-family-commit-cap-single-parent-v2", "Verify phase commit cap zero merges and single-parent closeout"),
    ("ghc-family-five-class-privacy-adjudication-v2", "Separate scanner definitions candidates incidents and payload hits"),
    ("ghc-family-commit-manifest-parity-v3", "Audit exact commit-local manifests with declared self-exclusions"),
    ("ghc-family-stage-label-lifecycle-lint-v2", "Reject stale prepared sent evidence closeout and seal labels"),
    ("ghc-family-authority-reservation-matrix-v2", "Prevent software evidence from compensating for authority gaps"),
    ("ghc-family-baton-ack-one-shot-v2", "Count one existing-task baton only after acknowledged send"),
]

RUNNER_TITLES = [
    "ghc_family_child_process_lifecycle_tribunal.py",
    "ghc_family_heat_kernel_obligations.py",
    "ghc_family_hsc_pdr3_zero_row.py",
    "ghc_family_telecom_change_handover.py",
    "ghc_family_vc_related_resource_profile.py",
    "ghc_family_telecom_outage_authority.py",
    "ghc_family_http_structured_fields_tribunal.py",
    "ghc_family_breadcrumb_audit.py",
    "ghc_family_nernst_third_law_domain.py",
    "ghc_family_prequential_drift_board.py",
]

CLEAN_TASK_TITLES = [
    "Reconcile proposal and outcome counts across receipts",
    "Reconcile inherited sealed external synthetic and operational negatives",
    "Synchronize Method Flow counts and validator expectations",
    "Correct stale phase labels additively",
    "Preserve compatibility callers while selecting family-current tools",
    "Normalize generated JSON key ordering",
    "Normalize generated UTF-8 and LF authoring",
    "Keep commit-blob and working-tree hash domains explicit",
    "Review public files for private absolute paths",
    "Review public files for raw task or thread identifiers",
    "Review public files for credential token or private-key assignments",
    "Review source statuses for allowed vocabulary",
    "Review HSC release sources for zero-row nonconversion",
    "Review citations for observation and authority nonconversion",
    "Review x1 staged files for x2 contamination",
    "Review x2 outcomes for four-class vocabulary",
    "Review exact and blocked packets for zero execution credit",
    "Review owner footprint against the 15000-file threshold",
    "Review breadcrumb report structure and manual reservations",
    "Review report manual assistive-technology and affected-user reservations",
    "Review Māori authority and data-governance reservations",
    "Review telecommunications professional operational and legal reservations",
    "Review real-data query and likelihood counters remain zero",
    "Review real-operator network customer outage and emergency-call counters remain zero",
    "Review real-key credential retrieval and interoperability counters remain zero",
    "Review source and all phase-anchor ancestry",
    "Review phase commit cap zero merges and one final parent",
    "Review validation branch remains named and local-only",
    "Review canonical four-way remote equality",
    "Refresh phase-scoped index wellbeing and terminal route before handoff",
]

EXACT_PACKET_TITLES = [
    "Real HSC data query download likelihood or parameter inference",
    "Real telecommunications network change rollback alarm or outage action",
    "Real emergency-call reach or public-safety decision",
    "Production credential related-resource retrieval key or verification operation",
    "Real identity interoperability recovery or trust-governance decision",
    "Protected location traffic worker or customer information disclosure",
    "Legal interpretation remedy allocation or vulnerability determination",
    "Māori authority or data-governance decision",
    "Production deployment security certification or exhaustive-security claim",
    "Independent-team reproduction Stage 20 proof or canon decision",
]

BLOCKED_PACKET_TITLES = [
    "Force-push rewrite or merge canonical history",
    "Delete reuse or mutate a sibling-owned lane",
    "Expose credentials private routes private state or raw task identifiers",
    "Enable Windows features weaken security elevate or install unrelated software",
    "Claim consciousness personhood AGI ASI or Theory-of-Everything closure",
]

X1_OPERATIONAL_NEGATIVES = [
    {"negative_id":"V6473-X1-N01","method_id":"V6473-M01","summary":"The first complete-skill read wrapper assumed positional PowerShell arguments were passed by the shell interface and received a null LiteralPath before any repository action.","retained":True,"recovered":True},
    {"negative_id":"V6473-X1-N02","method_id":"V6473-M02","summary":"The first combined worktree drive and status probe exceeded its bounded timeout and produced no usable witness; narrower lightweight probes later passed without mutation.","retained":True,"recovered":True},
    {"negative_id":"V6473-X1-N03","method_id":"V6473-M03","summary":"The valid fast-forward printed an overlarge inherited path inventory that was truncated by the tool display; independent exact hashes and remote equality remained available and passed.","retained":True,"recovered":True},
    {"negative_id":"V6473-X1-N04","method_id":"V6473-M04","summary":"The first multi-surface official-source search returned standards sources but omitted HSC; a bounded HSC-specific search found the official release and S19A shape pages without querying data.","retained":True,"recovered":True},
    {"negative_id":"V6473-X1-N05","method_id":"V6473-M05","summary":"The first stale-label scan used a double-quoted PowerShell pattern whose embedded quote split the expression into invalid path arguments; the single-quoted literal-pattern recovery passed without mutation.","retained":True,"recovered":True},
    {"negative_id":"V6473-X1-N06","method_id":"V6473-M06","summary":"The first Method Flow build predeclared witness IDs and the family runner appended the same IDs again; validation passed but the duplicate derived list was rejected and rebuilt from an empty initial list.","retained":True,"recovered":True},
    {"negative_id":"V6473-X1-N07","method_id":"V6473-M07","summary":"The first exact-surface stale-label scan passed shell wildcard paths literally to ripgrep on Windows; repository status and diff hygiene remained valid, and ripgrep-owned glob filters provided the bounded recovery.","retained":True,"recovered":True},
    {"negative_id":"V6473-X1-N08","method_id":"V6473-M08","summary":"The first staged-review invocation supplied repository-relative receipt paths to a reviewer that requires absolute paths before relativization; it failed before emitting receipts, and the absolute-path recovery preserved the same uncommitted staged surface.","retained":True,"recovered":True},
    {"negative_id":"V6473-X1-N09","method_id":"V6473-M09","summary":"The first absolute-path staged review rejected three adapted Python files for one surplus blank line at EOF; zero privacy or x1-contamination hits occurred, the failed receipt was retained, and only EOF whitespace was corrected.","retained":True,"recovered":True},
]

METHOD_SPECS = [
    {
        "method_id":"V6473-M01","title":"Use literal paths when the shell interface has no positional argument channel",
        "failure_signature":"PowerShell LiteralPath received null from an unavailable positional argument.",
        "trigger_preconditions":["A nested shell call needs to read an exact local instruction file."],
        "candidate_workaround":"Embed the already-known literal path in the bounded read command and avoid interpolating private data.",
        "recurrence_guard":"Do not assume shell positional arguments exist unless the tool schema explicitly provides them.",
        "rollback":"Discard the failed read-only wrapper; no repository action occurred.",
        "protected_gates":["skill_first","privacy","no_repository_mutation"],
        "retained_negative_ids":["V6473-X1-N01"],
        "failed_observed":"Get-Content rejected a null LiteralPath.",
        "pass_observed":"Literal-path reads returned both complete skills and both required references to EOF.",
    },
    {
        "method_id":"V6473-M02","title":"Split large-checkout startup probes into lightweight bounded witnesses",
        "failure_signature":"A combined worktree drive and status probe timed out with no usable output.",
        "trigger_preconditions":["A large inherited checkout makes status and worktree inventory slow."],
        "candidate_workaround":"Run worktree and drive inventory first, then exact branch, status, ancestry, and live-remote checks separately with a longer bound.",
        "recurrence_guard":"Do not bundle multiple large-checkout status scans behind the shortest timeout.",
        "rollback":"Discard the timeout result; it made no mutation.",
        "protected_gates":["clean_state","exact_head","remote_equality","no_sibling_mutation"],
        "retained_negative_ids":["V6473-X1-N02"],
        "failed_observed":"The combined probe exceeded its timeout and returned no evidence.",
        "pass_observed":"Narrow probes established D-drive posture, clean source and owner lanes, exact ancestry, and four-way equality.",
    },
    {
        "method_id":"V6473-M03","title":"Use quiet fast-forward plus exact-hash proofs for artifact-heavy ancestry",
        "failure_signature":"A successful fast-forward emitted a path inventory larger than the display budget.",
        "trigger_preconditions":["The sequential branch advances across several artifact-heavy phases."],
        "candidate_workaround":"Treat path output as nonauthoritative and prove head, upstream, tracking, fresh live remote, status, ancestry, commit count, and merge count separately.",
        "recurrence_guard":"Use quiet Git output where practical and always retain independent exact-hash receipts.",
        "rollback":"No rollback; exact proofs confirmed the authorized fast-forward and push.",
        "protected_gates":["fast_forward_only","exact_head","remote_equality","zero_merges"],
        "retained_negative_ids":["V6473-X1-N03"],
        "failed_observed":"The tool display truncated the verbose inherited path list.",
        "pass_observed":"Local, upstream, tracking, and fresh live remote all equalled the exact Orin final head with a clean Tamar lane.",
    },
    {
        "method_id":"V6473-M04","title":"Split official-source discovery by evidence surface",
        "failure_signature":"A broad multi-topic query omitted the HSC release surface.",
        "trigger_preconditions":["One search spans unrelated science, standards, accessibility, and tooling topics."],
        "candidate_workaround":"Run a bounded domain-specific official-source query and retain the incomplete search as a negative.",
        "recurrence_guard":"Require at least one directly reviewed official or primary source for each material proposal surface.",
        "rollback":"Do not infer absence from the broad search and do not query or download data.",
        "protected_gates":["primary_sources","zero_row","no_citation_as_observation"],
        "retained_negative_ids":["V6473-X1-N04"],
        "failed_observed":"The first source result set had no HSC release page.",
        "pass_observed":"The HSC-specific search found the official PDR3 and S19A shape pages while preserving zero queries and downloads.",
    },
    {
        "method_id":"V6473-M05","title":"Use single-quoted literal patterns for PowerShell stale-label scans",
        "failure_signature":"An embedded quote split a ripgrep pattern into invalid path arguments.",
        "trigger_preconditions":["A PowerShell wrapper passes one alternation pattern containing quote-sensitive text."],
        "candidate_workaround":"Place the complete bounded ripgrep alternation in one PowerShell single-quoted literal and keep file paths as separate arguments.",
        "recurrence_guard":"Do not mix embedded double quotes with a double-quoted native-command pattern.",
        "rollback":"Discard the failed read-only scan; it changed no file or ref.",
        "protected_gates":["stale_label_review","privacy","no_repository_mutation"],
        "retained_negative_ids":["V6473-X1-N05"],
        "failed_observed":"Ripgrep treated pattern fragments as invalid Windows paths.",
        "pass_observed":"The single-quoted pattern returned only the expected current labels and no stale source or route claims.",
    },
    {
        "method_id":"V6473-M06","title":"Let the Method Flow runner append witness identifiers from an empty initial list",
        "failure_signature":"Predeclared witness identifiers were appended a second time during witness recording.",
        "trigger_preconditions":["A generated method record is about to be ingested by the family Method Flow runner."],
        "candidate_workaround":"Initialize validation_witness_ids as an empty list and let each witness command append its stable identifier exactly once.",
        "recurrence_guard":"Inspect the first summary for duplicate witness IDs before x1 staging.",
        "rollback":"Discard only the uncommitted owner-generated derived ledger and rebuild it from corrected records; retain the first summary as a negative description.",
        "protected_gates":["append_only_evidence","failed_witness_retention","x1_only"],
        "retained_negative_ids":["V6473-X1-N06"],
        "failed_observed":"Each preferred method summary listed its failed and passing witness IDs twice.",
        "pass_observed":"The rebuilt ledger lists each failed and passing witness exactly once and validates with every failed witness retained.",
    },
    {
        "method_id":"V6473-M07","title":"Use ripgrep-owned glob filters instead of PowerShell wildcard path expansion",
        "failure_signature":"Wildcard file arguments reached ripgrep as invalid literal Windows paths.",
        "trigger_preconditions":["A native ripgrep command needs to scan version-patterned files on Windows."],
        "candidate_workaround":"Pass stable directories as paths and use ripgrep -g filters for version-patterned filenames.",
        "recurrence_guard":"Do not rely on PowerShell to expand native-command wildcard path arguments.",
        "rollback":"Discard the failed read-only scan; no file was staged or changed.",
        "protected_gates":["stale_label_review","exact_surface","no_repository_mutation"],
        "retained_negative_ids":["V6473-X1-N07"],
        "failed_observed":"Ripgrep reported the literal wildcard arguments as invalid Windows paths.",
        "pass_observed":"Directory paths plus ripgrep -g filters completed the exact bounded stale-label scan with zero stale hits.",
    },
    {
        "method_id":"V6473-M08","title":"Pass absolute receipt paths to staged reviewers that relativize against the repository root",
        "failure_signature":"Path.relative_to rejected a repository-relative receipt argument.",
        "trigger_preconditions":["The staged reviewer computes public receipt paths relative to its absolute repository root."],
        "candidate_workaround":"Resolve each owner-scoped receipt to an absolute path before invoking the reviewer while keeping the staged surface unchanged.",
        "recurrence_guard":"Inspect reviewer path semantics before the first lifecycle invocation and use absolute receipt paths consistently.",
        "rollback":"Retain the same uncommitted staged set; the failed invocation emitted no receipt and changed no ref.",
        "protected_gates":["exact_staged_surface","x1_only","no_history_rewrite"],
        "retained_negative_ids":["V6473-X1-N08"],
        "failed_observed":"The reviewer raised ValueError before scanning or writing its lifecycle receipts.",
        "pass_observed":"Absolute owner-lane receipt paths produced a valid exact staged review, privacy receipt, and manifest for the same x1 surface.",
    },
    {
        "method_id":"V6473-M09","title":"Run staged diff hygiene before fixed-point manifest credit",
        "failure_signature":"Three adapted Python files had one surplus blank line at EOF.",
        "trigger_preconditions":["Compatibility-preserving source adaptation creates new Python files."],
        "candidate_workaround":"Retain the failed staged receipt, remove only surplus terminal blank lines, restage the same owned surface, and rerun the reviewer.",
        "recurrence_guard":"Require git diff --cached --check before fixed-point manifest or commit credit.",
        "rollback":"Keep all substantive staged bytes, withdraw the failed review's pass credit, and apply only bounded EOF whitespace correction.",
        "protected_gates":["diff_hygiene","exact_staged_surface","x1_only","no_history_rewrite"],
        "retained_negative_ids":["V6473-X1-N09"],
        "failed_observed":"The staged reviewer reported new blank line at EOF for the staged reviewer, x1 reviewer, and x1 test.",
        "pass_observed":"The same substantive x1 surface passed diff hygiene after only the three surplus EOF blank lines were removed.",
    },
]
