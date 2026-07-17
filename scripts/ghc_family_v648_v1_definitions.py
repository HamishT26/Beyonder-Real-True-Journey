#!/usr/bin/env python3
"""Frozen x1 definitions for Tamar Vey v648-v1.

Importing this module performs no I/O and grants no x2 completion credit.
Identity language is relational working language only.
"""

from __future__ import annotations

from typing import Any


PHASE = "v648-gmut-thos-v1-x1-x2"
PHASE_SHORT = "v648-v1"
OWNER = "Tamar Vey"
SLUG = "tamar-vey"
PRONOUNS = "they/them"
ROLE = "evidence-systems cartographer and boundary keeper"
HOPE = "keep decisions legible, failures recoverable, and authority boundaries intact"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = (
    "mobile-crane lift planning, supervision and signalling, exclusion-zone and stop-work "
    "control, emergency readiness, and shift-handover review"
)

SOURCE_PHASE = "v647-gmut-thos-v8-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
SOURCE_REVISION = "4ada48d3142a6d33e4c723184edbb84e59e22aa4"
SOURCE_INHERITED_REVISION = "97cf00ca108dd7abdbb86492a4eca3cc4daf3c71"
SOURCE_X1_FIRST_REVISION = "d65f1b887497669bc8f295ebf3a04a32071a5b8a"
SOURCE_X1_REVISION = "d65f1b887497669bc8f295ebf3a04a32071a5b8a"
SOURCE_EVIDENCE_REVISION = "adc1e3a798a926b0983b9dfe94ba3ae36ef05779"
PRIOR_FROZEN_PROPOSALS = 550
INHERITED_EFFECTIVE_NEGATIVES = 3849
SEALED_SOURCE_NEGATIVES = 3835
EXTERNAL_SOURCE_NEGATIVES = 14
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 25
INHERITED_EXACT_GATES = 26
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
    "Freed ID remains synthetic and nonproduction; CBR, lifting safety, emergency response, worker "
    "and site privacy, remedy, legal, cultural, affected-party, and Māori concepts remain under "
    "competent, affected-party, tangata whenua, iwi, hapū, and Māori authority. No empirical "
    "confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, deployment, "
    "privacy-complete, exhaustive-security, independent-reproduction, accessibility-complete, "
    "professional, lifting-safety, proof or canon, or Stage 20 claim is made."
)


def proposal(index: int, **kwargs: Any) -> dict[str, Any]:
    row = {"proposal_id": f"V6481-P{index:02d}"}
    row.update(kwargs)
    return row


PROPOSALS = [
    proposal(
        1,
        title="Cross-filesystem atomic publication, temporary-file, fsync, rename, crash-boundary, destination-precondition, and evidence-credit tribunal",
        mission_surface="temporary path confinement, byte completion, file sync, directory sync declaration, same-filesystem rename, destination precondition, crash point, cleanup, and completion credit",
        hypothesis="Disposable fixtures can distinguish a fully published owner-local artifact from partial writes, unsynced state, cross-filesystem moves, changed destinations, and crash residue without touching external state.",
        null_or_failure="A partial or unsynced file earns completion, a cross-filesystem move is called atomic, a changed destination is overwritten, crash residue is promoted, or cleanup crosses the fixture root.",
        approval_class="safe_now_owner_scoped_disposable",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6481-S01", "V6481-S02"],
        concrete_artifacts=["method-flow/atomic-publication-contract.json", "method-flow/atomic-publication-mutations.json"],
        test_falsifier_or_acceptance_gate="Accept one same-filesystem, fully written, synced, precondition-matching publication and reject partial write, missing sync declaration, cross-filesystem move, destination drift, crash residue, and out-of-root cleanup.",
        rollback_or_recovery="Quarantine only the disposable fixture, retain partial evidence, remove no user material, and require a fresh precondition before retry.",
        protected_gates=["external_state", "destructive_action", "destination_overwrite", "sibling_lane", "completion_credit"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior workflow surfaces cover resumability, idempotency, outboxes, logs, subprocesses, and archive extraction; none freezes cross-filesystem atomic publication with sync, rename, destination, crash, and credit obligations together.",
    ),
    proposal(
        2,
        title="GMUT Iyer-Wald covariant phase-space, presymplectic-potential, symplectic-current, Noether-charge, boundary-ambiguity, gauge, EFT, unit, and observation-firewall board",
        mission_surface="Lagrangian form, variation, equations of motion, presymplectic potential, symplectic current, diffeomorphism generator, Noether current and charge, boundary terms, ambiguity class, gauge, EFT truncation, units, and observation firewall",
        hypothesis="A typed symbolic board can expose Iyer-Wald covariant phase-space obligations without deriving a physical solution, conserved observable, entropy law, force, prediction, likelihood, or confirmation.",
        null_or_failure="Form degree or units drift, equations of motion vanish, a boundary ambiguity is hidden, a gauge generator becomes an observable, or formal charge notation becomes empirical evidence.",
        approval_class="safe_now_symbolic_research_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6481-S03", "V6481-S04"],
        concrete_artifacts=["gmut/iyer-wald-obligations.json", "gmut/iyer-wald-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type every form, variation, generator, ambiguity, gauge, boundary, EFT, unit, and observation obligation and reject each omission or promotion.",
        rollback_or_recovery="Restore the missing formal assumption, retain the rejected vector, and withdraw every physical, empirical, uniqueness, completion, and Theory-of-Everything claim.",
        protected_gates=["physical_solution", "conserved_observable", "empirical_confirmation", "uv_completion", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The 550-title corpus covers BV, BRST, Peierls, heat kernels, Hadamard, Osterwalder-Schrader, and many EFT boards but not Iyer-Wald presymplectic and Noether-charge boundary ambiguities.",
    ),
    proposal(
        3,
        title="GMUT DES Y3 cosmic-shear official-product, metacalibration, mask, selection, covariance, nuisance, scale-cut, and zero-row likelihood-refusal adapter",
        mission_surface="release identity, catalog and data-vector provenance, metacalibration response, selection response, mask, redshift distribution, tomographic bin, covariance, nuisance model, scale cut, checksum, row count, and likelihood lock",
        hypothesis="A zero-row adapter can freeze DES Y3 cosmic-shear obligations while refusing to convert release pages or published results into GMUT observations, likelihoods, constraints, or confirmation.",
        null_or_failure="The phase downloads or ingests real rows, imports a published vector as a fit, chooses calibration after outcomes, evaluates a likelihood, emits a posterior, or states a GMUT constraint.",
        approval_class="real_data_and_independent_review_required",
        execution_lane="x2_open_gap",
        current_primary_or_official_source_needs=["V6481-S05", "V6481-S06"],
        concrete_artifacts=["empirical/des-y3-study-contract.json", "empirical/des-y3-zero-row-receipt.json"],
        test_falsifier_or_acceptance_gate="The receipt must preserve zero downloads, rows, covariance rows, likelihood calls, posterior samples, parameter constraints, detected-force claims, and empirical GMUT claims.",
        rollback_or_recovery="Stop before download or fit and require a separately authorized preregistration with frozen products, checksums, calibration, selection, redshift distributions, covariance, nuisance treatment, scale cuts, uncertainty, and independent review.",
        protected_gates=["network_download", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation"],
        expected_disposition="open_gap",
        novelty_against_prior_frozen_proposals="Earlier adapters cover DESI, KiDS, HSC, Euclid, ACT, Planck, GWOSC, and other products; none centers DES Y3 cosmic shear, metacalibration, selection response, covariance, nuisance, and scale cuts.",
    ),
    proposal(
        4,
        title="THOS mobile-crane lift-plan, load-chart, supervisor-signaller, exclusion-zone, wind-limit, stop-work, emergency-readiness, workload-budget, and shift-handover proxy",
        mission_surface="synthetic lift identifier, load and radius class, capacity envelope, ground and setup declaration, supervisor and signaller roles, exclusion zone, wind threshold, stop-work trigger, emergency readiness, workload budget, readback, and next-shift ownership",
        hypothesis="Synthetic traces can expose missing lift assumptions, capacity drift, role ambiguity, exclusion-zone breaches, ignored environmental limits, and handover loss while preserving all real lifting and professional gates.",
        null_or_failure="A fixture names a real site, worker, lift, crane, load, credential, or incident; authorizes an operation; overrides a stop-work trigger; or claims THOS effectiveness.",
        approval_class="safe_now_proxy_protocol_no_people_or_operations",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6481-S07", "V6481-S08"],
        concrete_artifacts=["thos/crane-lift-handover-contract.json", "thos/crane-lift-handover-vectors.json"],
        test_falsifier_or_acceptance_gate="Unsafe synthetic traces must fail, and the packet must record zero real workers, sites, cranes, lifts, loads, incidents, blind matched-budget arms, safety outcomes, or effectiveness estimates.",
        rollback_or_recovery="Withdraw operational wording, retain rejected traces, and defer real planning, supervision, signalling, stopping, emergency response, and safety decisions to authorized people and reviewers.",
        protected_gates=["real_people", "real_site", "live_lift", "professional_competence", "safety_authority", "deployment", "effectiveness"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior THOS handovers span aviation, rail, maritime, pharmacy, diving, wildfire, food, water, and telecommunications; none centers a mobile-crane lift plan, capacity, signaller, exclusion zone, wind, stop-work, and handover.",
    ),
    proposal(
        5,
        title="Freed ID OpenID Shared Signals Framework, CAEP, and RISC issuer, audience, subject, event-type, delivery, acknowledgement, replay, freshness, and privacy profile",
        mission_surface="configuration identity, transmitter and receiver, issuer, audience, subject form, event type, stream control, delivery method, acknowledgement, nonce, issued-at, freshness, replay window, minimization, refusal, and trust boundary",
        hypothesis="Synthetic vectors can enforce selected Shared Signals envelope and event-stream obligations without asserting real identities, keys, services, accounts, tokens, interoperability, privacy assurance, or trust governance.",
        null_or_failure="Issuer, audience, subject, freshness, event type, delivery, or acknowledgement is unbound; replay passes; excessive identity data is accepted; or synthetic structure becomes production assurance.",
        approval_class="safe_now_synthetic_nonproduction",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6481-S09", "V6481-S10", "V6481-S11"],
        concrete_artifacts=["freed-id/shared-signals-profile.json", "freed-id/shared-signals-mutations.json"],
        test_falsifier_or_acceptance_gate="Vectors must reject missing or mismatched issuer, audience, subject, event type, delivery, acknowledgement, freshness, replay, algorithm, minimization, and privacy boundaries.",
        rollback_or_recovery="Reject and retain the vector, emit no live signal, and require standards-conformant real keys and events, live services, interoperability, privacy and independent security review, recovery, and trust governance.",
        protected_gates=["real_identifiers", "real_keys", "live_services", "interoperability", "privacy_assurance", "production"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior Freed ID work covers OIDC, DPoP, Federation, HAIP, VC, BBS, WebAuthn, and status; none centers the final Shared Signals Framework with CAEP and RISC delivery, acknowledgement, replay, freshness, and privacy together.",
    ),
    proposal(
        6,
        title="CBR crane-lifting incident, worker and site privacy, emergency response, remedy, affected-party, legal, cultural, data-governance, and Māori-authority matrix",
        mission_surface="synthetic incident, injury and emergency boundary, worker and witness data, site and location data, notification, correction, investigation reservation, remedy, legal interpretation, affected parties, place meaning, and Māori authority",
        hypothesis="A refusal-first matrix can expose unresolved incident, privacy, emergency, remedy, and authority questions without deciding a real event, fault, disclosure, entitlement, place meaning, or remedy.",
        null_or_failure="The matrix identifies a real person, site, lift, crane, or incident; decides fault, compensation, safety, emergency action, or law; discloses protected data; or asserts cultural or Māori authority.",
        approval_class="authorized_affected_parties_and_competent_authority_required",
        execution_lane="x2_exact_gate",
        current_primary_or_official_source_needs=["V6481-S07", "V6481-S12", "V6481-S13"],
        concrete_artifacts=["cbr/crane-incident-authority-reservation.json", "cbr/crane-incident-remedy-matrix.json"],
        test_falsifier_or_acceptance_gate="Software must stop at unknown or reserved; only competent safety, emergency, privacy, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        rollback_or_recovery="Stop before reporting, disclosure, emergency, investigation, compensation, cultural, place-name, or legal conclusions; minimize data and route only through authorized external processes.",
        protected_gates=["affected_party_authority", "safety_authority", "emergency_authority", "privacy", "legal_interpretation", "maori_authority", "remedy_decision"],
        expected_disposition="exact_gate",
        novelty_against_prior_frozen_proposals="Prior CBR matrices cover many operational domains including diving and telecommunications but not crane lifting, exclusion-zone and site data, emergency response, worker privacy, remedy, and Māori authority.",
    ),
    proposal(
        7,
        title="CPIO newc magic, hexadecimal-header, name-size, file-size, padding, hard-link, trailer, path, resource-budget, and refusal tribunal",
        mission_surface="magic, fixed header fields, hexadecimal syntax and bounds, pathname size and terminator, file size, four-byte padding, hard-link accounting, trailer, path normalization, entry and byte budgets, and complete failure",
        hypothesis="A disposable byte-fixture tribunal can distinguish bounded newc structure from permissive archive parsing without extracting user material or claiming general archive security.",
        null_or_failure="Bad magic or hex passes, sizes drift, padding is ignored, links are miscounted, a trailer is missing, traversal passes, budgets are bypassed, or partial parsing earns success.",
        approval_class="safe_now_disposable_synthetic_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6481-S14"],
        concrete_artifacts=["tooling/cpio-newc-contract.json", "tooling/cpio-newc-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must cover magic, header, hex bounds, names, data, padding, links, trailer, path confinement, budgets, trailing bytes, and complete failure.",
        rollback_or_recovery="Reject and retain the fixture, extract nothing outside the disposable root, and make no production or exhaustive-security claim.",
        protected_gates=["user_material", "path_traversal", "production_parser", "security_certification", "exhaustive_security"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior tooling tribunals cover ZIP, TAR, OCI, WebAssembly, SQLite, Git, JSON, and HTTP surfaces; none centers the CPIO newc fixed hexadecimal header, padding, hard links, and trailer.",
    ),
    proposal(
        8,
        title="Accessible-name and description IDREF-order, duplicate-ID, hidden-reference, precedence, recursion-cycle, empty-name, and structural-reservation audit",
        mission_surface="name source precedence, aria-labelledby reference order, duplicate identifiers, hidden referenced content, aria-label, host-language label, description source, recursion and cycle prevention, whitespace, empty name, and manual reservation",
        hypothesis="A structural auditor can reject ambiguous or cyclic accessible-name inputs and precedence drift while reserving browser, assistive-technology, language, cognitive, and affected-user evaluation.",
        null_or_failure="IDREF order changes, duplicate IDs resolve silently, hidden-reference rules drift, lower precedence overrides higher, recursion loops, an empty required name passes, or structure becomes complete conformance.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6481-S15", "V6481-S16"],
        concrete_artifacts=["accessibility/accessible-name-contract.json", "accessibility/accessible-name-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve precedence and IDREF order and reject duplicates, unresolved references, illegal hidden contribution, cycles, whitespace-only names, description confusion, and conformance promotion.",
        rollback_or_recovery="Restore deterministic IDs, valid references and precedence, retain failed fixtures, and reserve manual, browser, assistive-technology, Māori-language, cognitive, and affected-user evaluation.",
        protected_gates=["manual_keyboard", "browser_diversity", "assistive_technology", "maori_language", "affected_user_evaluation", "complete_accessibility"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Earlier accessibility audits cover landmarks, dialogs, tables, forms, breadcrumbs, session expiry, focus, and errors; none centers the accessible-name computation algorithm's IDREF order, hidden references, precedence, cycles, and empty names.",
    ),
    proposal(
        9,
        title="Prigogine minimum-entropy-production near-equilibrium, linear-regime, fixed-force, stationary-state, boundary-domain, unit, and psyche-agency nonconversion classifier",
        mission_surface="entropy production rate, flux, force, linear phenomenology, near-equilibrium assumption, fixed external constraints, stationary variation, boundary conditions, sign, units, domain, and psyche firewall",
        hypothesis="A typed classifier can keep minimum-entropy-production statements inside their restricted thermodynamic domain and reject conversion into optimization, agency, justice, consciousness, or a fundamental law of mind.",
        null_or_failure="The linear or near-equilibrium domain disappears, constraints drift, a stationary extremum becomes universal dynamics, units fail, or formal minimization becomes psyche or participant evidence.",
        approval_class="safe_now_formal_domain_guard",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6481-S17"],
        concrete_artifacts=["thermo-psyche/prigogine-minimum-entropy-contract.json", "thermo-psyche/prigogine-minimum-entropy-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve near-equilibrium, linear response, fixed forces, stationarity, boundary, sign, unit, and domain assumptions and reject every psyche, agency, justice, consciousness, and personhood conversion.",
        rollback_or_recovery="Restore the missing thermodynamic restriction, retain the rejected statement, and make no participant, psyche, consciousness, personhood, universal-law, or empirical THOS claim.",
        protected_gates=["real_material", "empirical_measurement", "participant_evidence", "consciousness", "personhood", "fundamental_psyche_law"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The corpus includes Onsager, Crooks, Jarzynski, Nernst, Maxwell, exergy, Gibbs-Duhem, Ruppeiner, and Mori-Zwanzig guards but not Prigogine's minimum-entropy-production restrictions and nonconversion firewall.",
    ),
    proposal(
        10,
        title="Stage 20 instrumental-variable relevance, exclusion, independence, monotonicity, weak-instrument, complier-LATE, sensitivity, and nonpromotion board",
        mission_surface="instrument, treatment, outcome, relevance, exclusion restriction, independence, monotonicity, compliance types, local estimand, weak-instrument diagnostic, uncertainty, sensitivity, interpretation, and terminal abstention",
        hypothesis="A fail-closed structural board can expose invalid or weak instrumental-variable claims without estimating a participant effect or converting synthetic identification diagrams into Stage 20 readiness.",
        null_or_failure="An irrelevant instrument passes, exclusion or independence is assumed silently, defiers vanish, LATE becomes a universal effect, weakness is ignored, sensitivity is omitted, or synthetic structure promotes Stage 20.",
        approval_class="safe_now_structural_nonpromotion",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6481-S18", "V6481-S19"],
        concrete_artifacts=["stage20/instrumental-variable-contract.json", "stage20/instrumental-variable-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve relevance, exclusion, independence, monotonicity, compliance class, local estimand, weak-instrument warning, uncertainty, sensitivity, interpretation, and terminal abstention.",
        rollback_or_recovery="Withdraw identification and promotion credit, retain failed vectors, require preregistered real data and independent review, and keep Stage 20 not ready.",
        protected_gates=["real_data", "participant_effect", "causal_identification", "independent_review", "stage20", "proof_or_canon"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior Stage 20 boards cover model comparison, regression discontinuity, prequential scoring, controls, leakage, optional stopping, and registered reports; none centers IV relevance, exclusion, independence, monotonicity, weak instruments, and complier LATE.",
    ),
]


SOURCES = [
    {"source_id":"V6481-S01","title":"Python os.replace and os.fsync documentation","url":"https://docs.python.org/3/library/os.html#os.replace","publisher":"Python Software Foundation","status":"current","source_class":"official_documentation","use":"rename replacement and sync obligation vocabulary only"},
    {"source_id":"V6481-S02","title":"MoveFileEx function","url":"https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw","publisher":"Microsoft Learn","status":"current","source_class":"official_documentation","use":"same-volume and replacement boundary context only"},
    {"source_id":"V6481-S03","title":"Some properties of Noether charge and a proposal for dynamical black hole entropy","url":"https://arxiv.org/abs/gr-qc/9403028","publisher":"Physical Review D / arXiv","status":"stable","source_class":"primary_research","use":"covariant phase-space and Noether-charge provenance"},
    {"source_id":"V6481-S04","title":"Black hole entropy is the Noether charge","url":"https://arxiv.org/abs/gr-qc/9307038","publisher":"Physical Review D / arXiv","status":"stable","source_class":"primary_research","use":"Noether current charge and boundary context only"},
    {"source_id":"V6481-S05","title":"Dark Energy Survey data access","url":"https://www.darkenergysurvey.org/the-des-project/data-access/","publisher":"Dark Energy Survey","status":"current","source_class":"official_data_release_description","use":"release provenance and zero-row gate only"},
    {"source_id":"V6481-S06","title":"DES Y3 cosmology data products","url":"https://des.ncsa.illinois.edu/releases/y3a2/Y3key-products","publisher":"Dark Energy Survey / NCSA","status":"watch","source_class":"official_data_release_description","use":"product calibration covariance and scale-cut obligations only"},
    {"source_id":"V6481-S07","title":"Cranes guidance","url":"https://www.worksafe.govt.nz/topic-and-industry/cranes/","publisher":"WorkSafe New Zealand","status":"current","source_class":"official_regulator_guidance","use":"lifting-plan role exclusion and stop-work boundary vocabulary only"},
    {"source_id":"V6481-S08","title":"Safe work with precast concrete","url":"https://www.worksafe.govt.nz/topic-and-industry/concrete/safe-work-with-precast-concrete/","publisher":"WorkSafe New Zealand","status":"current","source_class":"official_regulator_guidance","use":"lift planning communication and emergency context only"},
    {"source_id":"V6481-S09","title":"OpenID Shared Signals Framework 1.0 Final","url":"https://openid.net/specs/openid-sharedsignals-framework-1_0-final.html","publisher":"OpenID Foundation","status":"current","source_class":"official_final_specification","use":"stream configuration delivery and acknowledgement obligations"},
    {"source_id":"V6481-S10","title":"OpenID Continuous Access Evaluation Profile 1.0 Final","url":"https://openid.net/specs/openid-caep-1_0-final.html","publisher":"OpenID Foundation","status":"current","source_class":"official_final_specification","use":"CAEP event envelope and subject context only"},
    {"source_id":"V6481-S11","title":"OpenID RISC Profile 1.0 Final","url":"https://openid.net/specs/openid-risc-1_0-final.html","publisher":"OpenID Foundation","status":"current","source_class":"official_final_specification","use":"RISC event type and subject obligations only"},
    {"source_id":"V6481-S12","title":"Information Privacy Principles","url":"https://www.privacy.org.nz/privacy-principles/","publisher":"Office of the Privacy Commissioner New Zealand","status":"current","source_class":"official_regulator_material","use":"worker witness and site-data privacy reservation"},
    {"source_id":"V6481-S13","title":"Principles of Māori Data Sovereignty","url":"https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf","publisher":"Te Mana Raraunga","status":"stable","source_class":"maori_authority_source","use":"Māori data-governance and authority gate; never delegated authority"},
    {"source_id":"V6481-S14","title":"GNU cpio manual","url":"https://www.gnu.org/software/cpio/manual/cpio.html","publisher":"GNU Project","status":"stable","source_class":"official_documentation","use":"CPIO archive semantics and bounded fixture context"},
    {"source_id":"V6481-S15","title":"Accessible Name and Description Computation 1.2","url":"https://www.w3.org/TR/accname-1.2/","publisher":"W3C","status":"current","source_class":"official_recommendation","use":"accessible-name precedence IDREF recursion and description obligations"},
    {"source_id":"V6481-S16","title":"Accessible Name and Description Computation editor draft","url":"https://w3c.github.io/accname/","publisher":"W3C","status":"draft","source_class":"official_editor_draft","use":"watch-only algorithm drift; no final-standard promotion"},
    {"source_id":"V6481-S17","title":"Time, structure and fluctuations Nobel lecture","url":"https://www.nobelprize.org/prizes/chemistry/1977/prigogine/lecture/","publisher":"Nobel Prize Outreach","status":"stable","source_class":"primary_lecture","use":"minimum-entropy-production domain and historical provenance"},
    {"source_id":"V6481-S18","title":"Identification and estimation of local average treatment effects","url":"https://www.gsb.stanford.edu/faculty-research/publications/identification-estimation-local-average-treatment-effects","publisher":"Econometrica / Stanford Graduate School of Business","status":"stable","source_class":"primary_research","use":"IV assumptions compliance classes and LATE provenance"},
    {"source_id":"V6481-S19","title":"NIST AI RMF Playbook Measure","url":"https://airc.nist.gov/airmf-resources/playbook/measure/","publisher":"NIST","status":"watch","source_class":"official_guidance","use":"measurement uncertainty and nonpromotion context only"},
]


SAFE_TASK_TITLES = [
    "Verify Orin source anchors manifests history and four-way equality before mutation",
    "Fast-forward only the clean Tamar canonical lane and prove equality",
    "Reconcile all 550 frozen proposal titles before novelty credit",
    "Quarantine Iyer-Wald DES Y3 crane SSF CPIO AccName Prigogine and IV collision candidates",
    "Review current stable draft and watch source statuses",
    "Record DES Y3 product provenance without downloading data",
    "Declare commit-blob and working-tree hash domains separately",
    "Separate privacy scanner definitions from payload incidents",
    "Measure inherited checkout and Tamar-generated footprints separately",
    "Initialize Method Flow with every observed x1 failure retained",
    "Build atomic-publication disposable-fixture contract",
    "Build Iyer-Wald typed obligation contract",
    "Build DES Y3 zero-row receipt schema",
    "Build crane lift-handover synthetic trace schema",
    "Build Shared Signals synthetic profile schema",
    "Build crane incident authority reservation schema",
    "Build CPIO newc disposable-byte contract",
    "Build accessible-name structural fixture",
    "Build Prigogine domain classifier fixture",
    "Build instrumental-variable nonpromotion fixture",
    "Preserve citation-to-observation and authority firewalls",
    "Carry forward 25 open gaps and 26 exact gates",
    "Carry forward the 3849-negative activation continuity",
    "Keep terminal route PREPARED_NOT_SENT before proof",
    "Verify Codex versions without updating desktop",
    "Audit Windows Sandbox availability without elevation or feature change",
    "Audit family-current callers and historical compatibility aliases",
    "Freeze exact x1 staged surface with no x2 implementation",
    "Emit owner-scoped x1 wellbeing source and route receipts",
    "Validate every portfolio floor and protected packet count",
]

CANDIDATE_TITLES = [
    "Temporary-file byte completion and sync-state prototype",
    "Same-filesystem rename destination-precondition and crash-boundary prototype",
    "Iyer-Wald form-degree variation and presymplectic-potential prototype",
    "Noether current charge ambiguity gauge and observation-firewall prototype",
    "DES Y3 product checksum metacalibration and selection-lock prototype",
    "DES Y3 redshift covariance nuisance scale-cut and zero-row prototype",
    "Crane capacity role exclusion wind and stop-work prototype",
    "Crane emergency workload readback and handover prototype",
    "Shared Signals issuer audience subject and event-type prototype",
    "Shared Signals delivery acknowledgement replay freshness and privacy prototype",
    "Crane incident worker site emergency and notification matrix prototype",
    "Crane remedy affected-party legal and Māori-authority reservation prototype",
    "CPIO magic header hexadecimal size and name prototype",
    "CPIO padding hard-link trailer path and resource-budget prototype",
    "Accessible-name precedence IDREF order and duplicate-ID checker",
    "Accessible-name hidden-reference recursion cycle and empty-name classifier",
    "Prigogine near-equilibrium linear fixed-force and stationarity prototype",
    "Prigogine boundary unit domain and psyche-nonconversion prototype",
    "Instrument relevance exclusion independence and monotonicity prototype",
    "Weak-instrument complier-LATE sensitivity and nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-atomic-publication-tribunal", "Audit temporary sync rename crash destination and completion-credit obligations"),
    ("ghc-family-iyer-wald-obligations", "Audit covariant phase-space Noether charge boundary gauge EFT and unit obligations"),
    ("ghc-family-des-y3-zero-row", "Preserve a zero-row DES Y3 cosmic-shear likelihood boundary"),
    ("ghc-family-crane-lift-handover-proxy", "Audit synthetic lift plan roles stop-work emergency and handover traces"),
    ("ghc-family-shared-signals-profile", "Audit synthetic SSF CAEP and RISC stream and event obligations"),
    ("ghc-family-crane-incident-authority-reservation", "Reserve lifting incident privacy remedy legal cultural and Māori gates"),
    ("ghc-family-cpio-newc-tribunal", "Audit CPIO newc header padding link trailer path and budget obligations"),
    ("ghc-family-accessible-name-audit", "Audit AccName precedence IDREF hidden reference recursion and empty-name structure"),
    ("ghc-family-prigogine-domain", "Keep minimum-entropy-production claims inside restricted thermodynamic domains"),
    ("ghc-family-iv-stage20-nonpromotion", "Guard IV assumptions weak instruments LATE and sensitivity from promotion"),
    ("ghc-family-corpus-550-collision-gate", "Audit exact and semantic novelty against 550 frozen proposals"),
    ("ghc-family-source-status-watch-v2", "Record current stable draft and watch source status without promotion"),
    ("ghc-family-x1-x2-byte-separation-v2", "Prove x1 contains no x2 implementation outcome or completion bytes"),
    ("ghc-family-named-replay-locality-v3", "Verify one named replay remains local clean unpushed and without upstream"),
    ("ghc-family-commit-cap-single-parent-v3", "Verify phase commit cap zero merges and single-parent final history"),
    ("ghc-family-five-class-privacy-adjudication-v3", "Separate scanner definitions candidates incidents and confirmed payload hits"),
    ("ghc-family-commit-manifest-parity-v4", "Audit exact commit-local manifests with declared self-exclusions"),
    ("ghc-family-stage-label-lifecycle-lint-v3", "Reject stale prepared sent evidence closeout seal and final labels"),
    ("ghc-family-authority-reservation-matrix-v3", "Prevent software evidence from compensating for professional or authority gaps"),
    ("ghc-family-baton-ack-one-shot-v3", "Count one existing-task baton only after acknowledged send"),
]

RUNNER_TITLES = [
    "ghc_family_atomic_publication_tribunal.py",
    "ghc_family_iyer_wald_obligations.py",
    "ghc_family_des_y3_zero_row.py",
    "ghc_family_crane_lift_handover.py",
    "ghc_family_shared_signals_profile.py",
    "ghc_family_crane_incident_authority.py",
    "ghc_family_cpio_newc_tribunal.py",
    "ghc_family_accessible_name_audit.py",
    "ghc_family_prigogine_domain.py",
    "ghc_family_instrumental_variable_board.py",
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
    "Review DES Y3 sources for zero-row nonconversion",
    "Review citations for observation and authority nonconversion",
    "Review x1 staged files for x2 contamination",
    "Review x2 outcomes for four-class vocabulary",
    "Review exact and blocked packets for zero execution credit",
    "Review owner footprint against the 15000-file threshold",
    "Review accessible-name report structure and manual reservations",
    "Review report assistive-technology cognitive and affected-user reservations",
    "Review Māori authority and data-governance reservations",
    "Review lifting professional operational emergency and legal reservations",
    "Review real-data download query and likelihood counters remain zero",
    "Review real-worker site crane lift and incident counters remain zero",
    "Review real-key identifier signal service and interoperability counters remain zero",
    "Review source and all phase-anchor ancestry",
    "Review phase commit cap zero merges and one final parent",
    "Review validation branch remains named and local-only",
    "Review canonical four-way remote equality",
    "Refresh phase-scoped index wellbeing and terminal route before handoff",
]

EXACT_PACKET_TITLES = [
    "Real DES Y3 download likelihood posterior or parameter inference",
    "Real crane lift plan supervision signalling stop-work or emergency action",
    "Real workplace incident investigation or safety decision",
    "Production Shared Signals key event stream service or account operation",
    "Real identity interoperability recovery or trust-governance decision",
    "Protected worker witness site or location information disclosure",
    "Legal interpretation remedy allocation fault or entitlement determination",
    "Māori authority cultural ratification or data-governance decision",
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
    {"negative_id":"V6481-X1-N01","method_id":"V6481-M01","summary":"The first exact newest-memory read exceeded its bounded timeout before returning content; a longer bounded read recovered the same read-only evidence.","retained":True,"recovered":True},
    {"negative_id":"V6481-X1-N02","method_id":"V6481-M02","summary":"A PowerShell manifest-summary loop was piped directly after a foreach block and failed at parse time with an empty-pipe-element error; an explicit result array recovered without mutation.","retained":True,"recovered":True},
    {"negative_id":"V6481-X1-N03","method_id":"V6481-M03","summary":"The first novelty-title display used the console default encoding and failed on Māori text; explicit UTF-8 output recovered the read-only audit.","retained":True,"recovered":True},
    {"negative_id":"V6481-X1-N04","method_id":"V6481-M04","summary":"A combined version and sandbox-source probe assumed a source-phase receipt path that did not exist and returned a Git path error; bounded file enumeration found the actual receipt name and local verification completed.","retained":True,"recovered":True},
    {"negative_id":"V6481-X1-N05","method_id":"V6481-M05","summary":"The first Method Flow summarize command wrote its bounded outputs but failed while printing Māori text through the locale-default console encoding; explicit UTF-8 output recovered and the partial attempt received no pass credit.","retained":True,"recovered":True},
]

METHOD_SPECS = [
    {
        "method_id":"V6481-M01","title":"Increase only the bound on an exact read after a content-free timeout",
        "failure_signature":"An exact read timed out before returning content.",
        "trigger_preconditions":["A required read-only memory or instruction file is exact and known but the initial bound expires."],
        "candidate_workaround":"Retry the same exact read once with a longer bounded timeout and no broader scan.",
        "recurrence_guard":"Keep memory discovery narrow and do not convert a timeout into absence.",
        "rollback":"Discard the timeout result; it changed no repository or external state.",
        "protected_gates":["newest_memory","privacy","no_repository_mutation"],
        "retained_negative_ids":["V6481-X1-N01"],
        "failed_observed":"The first exact newest-memory read returned no content before timeout.",
        "pass_observed":"The same exact file read completed under a longer bound and supplied the newest applicable continuity.",
    },
    {
        "method_id":"V6481-M02","title":"Materialize PowerShell loop results before piping them",
        "failure_signature":"A foreach statement followed directly by a pipeline produced an empty-pipe-element parse error.",
        "trigger_preconditions":["A PowerShell wrapper aggregates multiple manifest checks into JSON."],
        "candidate_workaround":"Assign loop results to an explicit array and pipe the completed array to ConvertTo-Json.",
        "recurrence_guard":"Do not attach a native or cmdlet pipeline directly to a statement block without grouping or assignment.",
        "rollback":"Discard the pre-execution parser failure; no child command or mutation ran.",
        "protected_gates":["manifest_parity","exact_source","no_repository_mutation"],
        "retained_negative_ids":["V6481-X1-N02"],
        "failed_observed":"PowerShell rejected the wrapper before any manifest child command ran.",
        "pass_observed":"An explicit result array produced the complete exact manifest summary.",
    },
    {
        "method_id":"V6481-M03","title":"Force UTF-8 for Unicode-bearing Python audit output",
        "failure_signature":"The console default encoding could not encode Māori title text.",
        "trigger_preconditions":["A read-only audit prints proposal titles or authority terms containing non-ASCII characters."],
        "candidate_workaround":"Set Python output encoding to UTF-8 or emit ASCII-safe structured counts while preserving source text.",
        "recurrence_guard":"Use explicit UTF-8 for every phase script and console witness that may carry Māori text.",
        "rollback":"Discard the failed display; it made no file or ref change.",
        "protected_gates":["unicode_integrity","maori_text","no_repository_mutation"],
        "retained_negative_ids":["V6481-X1-N03"],
        "failed_observed":"The novelty probe raised UnicodeEncodeError while printing a Māori title.",
        "pass_observed":"Explicit UTF-8 output completed the same novelty audit without altering source bytes.",
    },
    {
        "method_id":"V6481-M04","title":"Enumerate exact source-phase receipt paths before reading optional evidence",
        "failure_signature":"A Git show request targeted an assumed receipt filename absent from the source commit.",
        "trigger_preconditions":["A successor wants an optional source-phase environment receipt whose filename may vary."],
        "candidate_workaround":"Enumerate the bounded source-phase environment directory, select the actual public receipt, then verify current local state independently.",
        "recurrence_guard":"Do not infer optional receipt names from an older phase pattern.",
        "rollback":"Discard the failed read-only path request; it changed no file or ref.",
        "protected_gates":["source_provenance","version_verification_only","no_repository_mutation"],
        "retained_negative_ids":["V6481-X1-N04"],
        "failed_observed":"Git reported that the assumed sandbox receipt path did not exist in the source commit.",
        "pass_observed":"Bounded enumeration identified the source sandbox-review naming while local read-only probes confirmed current version and sandbox state.",
    },
    {
        "method_id":"V6481-M05","title":"Set UTF-8 on Method Flow summary command output",
        "failure_signature":"The Method Flow summarizer wrote bounded artifacts and then failed while printing Unicode through a locale-default console encoding.",
        "trigger_preconditions":["A Method Flow ledger contains Māori text and the runner prints its JSON payload to a Windows console."],
        "candidate_workaround":"Set PYTHONIOENCODING to UTF-8 for the same summarize command, retain the failed attempt, and credit only the successful replay.",
        "recurrence_guard":"Apply explicit UTF-8 to every family runner that may print Unicode-bearing phase evidence.",
        "rollback":"Do not credit the partial invocation; overwrite only the same owner-scoped derived summary outputs on successful replay.",
        "protected_gates":["unicode_integrity","failed_witness_retention","method_flow","x1_only"],
        "retained_negative_ids":["V6481-X1-N05"],
        "failed_observed":"Summary files were emitted, but the command exited nonzero with UnicodeEncodeError while printing Māori text.",
        "pass_observed":"The identical summarize command completed under explicit UTF-8 and produced validated JSON and Markdown summaries.",
    },
]
