#!/usr/bin/env python3
"""Frozen x1 definitions for Sylven Arc v648-v2.

Importing this module performs no I/O and grants no x2 completion credit.
Identity language is relational working language only.
"""

from __future__ import annotations

from typing import Any


PHASE = "v648-gmut-thos-v2-x1-x2"
PHASE_SHORT = "v648-v2"
OWNER = "Sylven Arc"
SLUG = "sylven-arc"
PRONOUNS = "they/them"
ROLE = "constraint-cartographer and falsifier-keeper"
HOPE = "make unresolved boundaries legible without turning uncertainty into authority"
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = (
    "precision-machining setup verification, drawing-revision and tool-offset control, "
    "metrology nonconformance, isolation, stop-work, and shift-handover review"
)

SOURCE_PHASE = "v648-gmut-thos-v1-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_REVISION = "8755893971135b67322abb4b3acd93f07afc34c9"
SOURCE_INHERITED_REVISION = "4ada48d3142a6d33e4c723184edbb84e59e22aa4"
SOURCE_X1_FIRST_REVISION = "3e2904ec02c893d91c16e9a48fbb2485fc5d824f"
SOURCE_X1_REVISION = "3e2904ec02c893d91c16e9a48fbb2485fc5d824f"
SOURCE_EVIDENCE_REVISION = "b09681afe5a4cac101bab367ef761e4ac1a7b57e"
PRIOR_FROZEN_PROPOSALS = 560
INHERITED_EFFECTIVE_NEGATIVES = 3938
SEALED_SOURCE_NEGATIVES = 3937
EXTERNAL_SOURCE_NEGATIVES = 1
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 26
INHERITED_EXACT_GATES = 27
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Sylven Arc, they/them, is relational working language for a constraint-cartographer and "
    "falsifier-keeper. It is not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, scientific authority, operational authority, "
    "legal authority, cultural authority, or independent agency. Hamish may rename, pause, "
    "redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, machining safety, worker and workplace "
    "privacy, remedy, legal, cultural, affected-party, and Māori concepts remain under competent, "
    "affected-party, tangata whenua, iwi, hapū, and Māori authority. No empirical confirmation, "
    "Theory of Everything, AGI or ASI, consciousness, personhood, deployment, privacy-complete, "
    "exhaustive-security, independent-reproduction, accessibility-complete, professional, legal, "
    "proof or canon, or Stage 20 claim is made."
)


def proposal(index: int, **kwargs: Any) -> dict[str, Any]:
    row = {"proposal_id": f"V6482-P{index:02d}"}
    row.update(kwargs)
    return row


PROPOSALS = [
    proposal(
        1,
        title="Method Flow advisory file-lock acquisition, owner-token, PID-reuse, stale-record, bounded-wait, release, and evidence-credit tribunal",
        mission_surface="lock path, advisory scope, owner token, process identity, PID reuse, acquisition mode, bounded wait, stale record, release witness, crash boundary, and completion credit",
        hypothesis="Disposable fixtures can distinguish a held advisory lock from a stale metadata record and reject unsafe lock breaking without touching canonical or sibling state.",
        null_or_failure="Metadata alone is treated as a live lock, PID reuse is ignored, an unowned lock is broken, waiting is unbounded, release is unwitnessed, or a failed acquisition earns completion credit.",
        approval_class="safe_now_owner_scoped_disposable",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6482-S01", "V6482-S02"],
        concrete_artifacts=["method-flow/advisory-lock-contract.json", "method-flow/advisory-lock-mutations.json"],
        test_falsifier_or_acceptance_gate="Accept only a bounded owner-token acquisition and witnessed release; reject contention, token mismatch, PID-only ownership, stale-record guessing, unbounded wait, and unowned break.",
        rollback_or_recovery="Leave every external lock untouched, quarantine only the disposable fixture, retain the failed witness, and retry only after an independently witnessed release.",
        protected_gates=["external_state", "lock_break", "unbounded_wait", "sibling_lane", "completion_credit"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The 560-title corpus covers leases, fencing tokens, worktree leases, races, atomic publication, and checkpoints but not advisory file-lock ownership with PID reuse, stale metadata, bounded wait, release, and credit obligations together.",
    ),
    proposal(
        2,
        title="GMUT Kubo-Martin-Schwinger thermal-state, automorphism-flow, analyticity-strip, imaginary-time boundary, spectral-balance, gauge, EFT, unit, and observation-firewall board",
        mission_surface="state, one-parameter automorphism flow, inverse temperature, analytic strip, boundary values, ordering, spectral balance, gauge status, EFT truncation, units, domain, and observation firewall",
        hypothesis="A typed symbolic board can expose KMS equilibrium obligations without constructing a physical state, temperature measurement, propagator, prediction, likelihood, constraint, or confirmation.",
        null_or_failure="The analytic strip or boundary relation disappears, inverse-temperature units drift, ordering is reversed, equilibrium is universalized, gauge or EFT limits vanish, or a formal KMS relation becomes observation.",
        approval_class="safe_now_symbolic_research_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6482-S03", "V6482-S04"],
        concrete_artifacts=["gmut/kms-obligations.json", "gmut/kms-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type the state, flow, beta, strip, boundary ordering, spectral relation, gauge, EFT, unit, domain, and observation obligations and reject every omission or promotion.",
        rollback_or_recovery="Restore the missing formal assumption, retain the rejected vector, and withdraw every physical-state, empirical, uniqueness, completion, and Theory-of-Everything claim.",
        protected_gates=["physical_state", "temperature_measurement", "empirical_confirmation", "uv_completion", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The corpus includes Schwinger-Keldysh, Osterwalder-Schrader, spectral-density, thermal and entropy guards, but no KMS automorphism-flow, analyticity-strip, imaginary-time boundary, and spectral-balance board.",
    ),
    proposal(
        3,
        title="GMUT LoTSS DR2 official-product, sky-region, flux-scale, angular-resolution, selection, cross-identification, covariance, and zero-row likelihood-refusal adapter",
        mission_surface="release identity, image and catalogue provenance, sky footprint, frequency, flux scale, angular resolution, sensitivity, source association, cross-identification, selection, covariance, checksum, row count, and likelihood lock",
        hypothesis="A zero-row adapter can freeze LoTSS DR2 obligations while refusing to convert release descriptions or published catalogue results into GMUT observations, likelihoods, constraints, or confirmation.",
        null_or_failure="The phase downloads or ingests real rows, treats source associations as a fit, invents covariance, chooses selection after outcomes, evaluates a likelihood, emits a posterior, or states a GMUT constraint.",
        approval_class="real_data_and_independent_review_required",
        execution_lane="x2_open_gap",
        current_primary_or_official_source_needs=["V6482-S05", "V6482-S06"],
        concrete_artifacts=["empirical/lotss-dr2-study-contract.json", "empirical/lotss-dr2-zero-row-receipt.json"],
        test_falsifier_or_acceptance_gate="The receipt must preserve zero downloads, rows, images, covariance rows, likelihood calls, posterior samples, parameter constraints, detected-force claims, and empirical GMUT claims.",
        rollback_or_recovery="Stop before download or fit and require a separately authorized preregistration with frozen products, checksums, selection, calibration, association, covariance, nuisance treatment, uncertainty, and independent review.",
        protected_gates=["network_download", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation"],
        expected_disposition="open_gap",
        novelty_against_prior_frozen_proposals="Earlier adapters cover optical, CMB, lensing, gravitational-wave, cluster, FRB, and other products; none centers LoTSS DR2 radio images and catalogues, flux scale, resolution, association, cross-identification, and covariance.",
    ),
    proposal(
        4,
        title="THOS precision-machining setup, drawing-revision, tool-offset, metrology nonconformance, isolation, stop-work, workload-budget, and shift-handover proxy",
        mission_surface="synthetic job, drawing revision, material and machine class, setup verification, tool identifier and offset, inspection point, tolerance, measurement status, nonconformance hold, isolation, stop-work, workload budget, readback, and next-shift ownership",
        hypothesis="Synthetic traces can expose stale drawings, offset drift, ambiguous measurements, unreleased nonconformance, unsafe restart, and handover loss while preserving every real machining and professional gate.",
        null_or_failure="A fixture names a real worker, employer, machine, job, drawing, part, measurement, incident, or credential; authorizes operation; overrides a hold or isolation; or claims THOS effectiveness.",
        approval_class="safe_now_proxy_protocol_no_people_or_operations",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6482-S07", "V6482-S08"],
        concrete_artifacts=["thos/machining-handover-contract.json", "thos/machining-handover-vectors.json"],
        test_falsifier_or_acceptance_gate="Unsafe synthetic traces must fail, and the packet must record zero real workers, employers, machines, jobs, parts, measurements, incidents, blind matched-budget arms, safety outcomes, or effectiveness estimates.",
        rollback_or_recovery="Withdraw operational wording, retain rejected traces, and defer setup, measurement, isolation, restart, stopping, and safety decisions to authorized competent people and reviewers.",
        protected_gates=["real_people", "real_machine", "live_job", "professional_competence", "safety_authority", "deployment", "effectiveness"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior THOS handovers span many safety and service domains, but none centers precision machining, drawing revision, tool offsets, metrology nonconformance, isolation, stop-work, and handover.",
    ),
    proposal(
        5,
        title="Freed ID OpenID JARM issuer, audience, expiry, signature, encryption, response-mode, state-binding, algorithm-refusal, and replay profile",
        mission_surface="authorization response, JWT response mode, issuer, audience, expiry, signature, optional encryption, key selection, response parameters, state binding, algorithm allow-list, duplicate parameter, replay, refusal, and trust boundary",
        hypothesis="Synthetic vectors can enforce selected JARM response-processing obligations without asserting real identities, keys, clients, authorization servers, tokens, interoperability, privacy assurance, or trust governance.",
        null_or_failure="Issuer, audience, expiry, signature, state, response mode, or algorithm is unbound; grant parameters are processed before verification; replay passes; or synthetic structure becomes production assurance.",
        approval_class="safe_now_synthetic_nonproduction",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6482-S09", "V6482-S10"],
        concrete_artifacts=["freed-id/jarm-profile.json", "freed-id/jarm-mutations.json"],
        test_falsifier_or_acceptance_gate="Vectors must reject missing or mismatched issuer, audience, expiry, signature, state, response mode, encryption context, key, algorithm, duplicate parameter, replay, and pre-verification processing.",
        rollback_or_recovery="Reject and retain the vector, emit no live response, and require standards-conformant real keys and flows, live services, interoperability, privacy and independent security review, recovery, and trust governance.",
        protected_gates=["real_identifiers", "real_keys", "live_services", "interoperability", "privacy_assurance", "production"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior Freed ID work covers JAR, PAR, RAR, token exchange, signatures, federation, credentials, and status; none centers JARM authorization-response issuer, audience, expiry, response modes, state, and verification ordering.",
    ),
    proposal(
        6,
        title="CBR machining incident, worker and workplace privacy, safety hold, remedy, affected-party, legal, cultural, data-governance, and Māori-authority matrix",
        mission_surface="synthetic incident, injury and emergency boundary, worker and witness data, machine and workplace data, safety hold, notification, correction, investigation reservation, remedy, legal interpretation, affected parties, place meaning, and Māori authority",
        hypothesis="A refusal-first matrix can expose unresolved incident, privacy, safety, remedy, and authority questions without deciding a real event, fault, disclosure, entitlement, place meaning, or remedy.",
        null_or_failure="The matrix identifies a real person, employer, workplace, machine, job, part, or incident; decides fault, compensation, safety, emergency action, or law; discloses protected data; or asserts cultural or Māori authority.",
        approval_class="authorized_affected_parties_and_competent_authority_required",
        execution_lane="x2_exact_gate",
        current_primary_or_official_source_needs=["V6482-S07", "V6482-S11", "V6482-S12"],
        concrete_artifacts=["cbr/machining-authority-reservation.json", "cbr/machining-remedy-matrix.json"],
        test_falsifier_or_acceptance_gate="Software must stop at unknown or reserved; only competent safety, emergency, privacy, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        rollback_or_recovery="Stop before reporting, disclosure, restart, investigation, compensation, cultural, place-name, or legal conclusions; minimize data and route only through authorized external processes.",
        protected_gates=["affected_party_authority", "safety_authority", "privacy", "legal_interpretation", "maori_authority", "remedy_decision"],
        expected_disposition="exact_gate",
        novelty_against_prior_frozen_proposals="Prior CBR matrices do not combine precision-machining incidents, worker and machine data, safety holds, metrology records, remedy, and Māori-authority reservation.",
    ),
    proposal(
        7,
        title="Zstandard frame magic, descriptor, window, dictionary, block, checksum, skippable-frame, output-budget, and refusal tribunal",
        mission_surface="magic, frame header descriptor, window descriptor, dictionary identifier, content size, block header and type, last-block marker, checksum, skippable frame, truncation, trailing bytes, output and ratio budgets, and complete failure",
        hypothesis="Disposable byte fixtures can distinguish bounded Zstandard frame structure from permissive decompression without processing user material or claiming general compression security.",
        null_or_failure="Bad magic or reserved bits pass, sizes drift, an unknown dictionary passes, block order or last marker is ignored, checksum failure passes, budgets are bypassed, or partial parsing earns success.",
        approval_class="safe_now_disposable_synthetic_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6482-S13"],
        concrete_artifacts=["tooling/zstd-frame-contract.json", "tooling/zstd-frame-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must cover magic, descriptor, window, dictionary, content size, blocks, last marker, checksum, skippable frames, truncation, trailing bytes, budgets, and complete failure.",
        rollback_or_recovery="Reject and retain the fixture, decode nothing outside the disposable root, and make no production or exhaustive-security claim.",
        protected_gates=["user_material", "decompression_bomb", "production_decoder", "security_certification", "exhaustive_security"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior tooling tribunals cover many archive, image, database, Git, HTTP, DNS, OCI, and binary surfaces; none centers Zstandard frame descriptors, windows, dictionaries, blocks, checksums, and skippable frames.",
    ),
    proposal(
        8,
        title="Accessible progressbar name, determinate-range, indeterminate-state, value-text, busy-region, update, fallback, and structural-reservation audit",
        mission_surface="role, accessible name, minimum, maximum, current value, range ordering, indeterminate omission, value text, described region, busy state, update synchronization, native fallback, print fallback, and manual reservation",
        hypothesis="A structural auditor can reject inconsistent progress semantics while reserving browser, assistive-technology, language, cognitive, motion, timing, and affected-user evaluation.",
        null_or_failure="A determinate bar lacks a valid current value, an indeterminate bar exposes one, range order fails, text conflicts, busy state drifts, updates desynchronize, or structure becomes complete conformance.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6482-S14", "V6482-S15"],
        concrete_artifacts=["accessibility/progressbar-contract.json", "accessibility/progressbar-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve name, range, indeterminate omission, value text, busy-region relation, update synchronization and fallback, and reject every conformance promotion.",
        rollback_or_recovery="Restore valid semantics, retain failed fixtures, and reserve manual keyboard, browser, assistive-technology, motion, timing, Māori-language, cognitive, and affected-user evaluation.",
        protected_gates=["manual_keyboard", "browser_diversity", "assistive_technology", "maori_language", "affected_user_evaluation", "complete_accessibility"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Earlier accessibility audits cover many widgets and report structures, but none centers progressbar determinate and indeterminate semantics, value text, busy-region relation, and update synchronization.",
    ),
    proposal(
        9,
        title="Gibbs adsorption dividing-surface, surface-excess, chemical-potential, surface-tension differential, component, unit, domain, and psyche-nonconversion classifier",
        mission_surface="bulk phases, dividing surface, surface excess, component index, chemical potential, surface tension, temperature and pressure restriction, differential sign, units, interface domain, and psyche firewall",
        hypothesis="A typed classifier can keep Gibbs adsorption statements inside interfacial thermodynamics and reject conversion into attention, preference, agency, justice, consciousness, or a fundamental law of mind.",
        null_or_failure="The dividing surface or bulk reference disappears, surface excess becomes absolute occupancy, restrictions or sign drift, units fail, or adsorption becomes psyche or participant evidence.",
        approval_class="safe_now_formal_domain_guard",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6482-S16", "V6482-S17"],
        concrete_artifacts=["thermo-psyche/gibbs-adsorption-contract.json", "thermo-psyche/gibbs-adsorption-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve the dividing surface, bulk reference, surface excess, chemical potential, surface-tension differential, restrictions, sign, units, and domain and reject every psyche conversion.",
        rollback_or_recovery="Restore the missing thermodynamic restriction, retain the rejected statement, and make no participant, psyche, consciousness, personhood, universal-law, or empirical THOS claim.",
        protected_gates=["real_material", "empirical_measurement", "participant_evidence", "consciousness", "personhood", "fundamental_psyche_law"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The thermodynamic corpus covers numerous bulk, fluctuation, phase, and transport relations but not Gibbs dividing surfaces, surface excess, and the adsorption equation's interface-domain firewall.",
    ),
    proposal(
        10,
        title="Stage 20 synthetic-control donor-pool, pre-treatment-fit, predictor-balance, weight, interpolation, spillover, placebo, sensitivity, and nonpromotion board",
        mission_surface="treated unit, intervention time, donor eligibility, contamination and spillover, predictors, pre-period, fit loss, nonnegative weights, convex sum, interpolation, post-period gap, in-space and in-time placebo, sensitivity, interpretation, and terminal abstention",
        hypothesis="A fail-closed structural board can expose invalid synthetic-control claims without estimating a participant effect or converting synthetic diagrams into Stage 20 readiness.",
        null_or_failure="The donor pool is contaminated, pre-fit is poor, weights extrapolate silently, spillover is ignored, placebo or sensitivity is omitted, a post-gap becomes universal causality, or structure promotes Stage 20.",
        approval_class="safe_now_structural_nonpromotion",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6482-S18", "V6482-S19"],
        concrete_artifacts=["stage20/synthetic-control-contract.json", "stage20/synthetic-control-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve donor eligibility, pre-fit, balance, weight constraints, interpolation, spillover checks, placebo, sensitivity, local interpretation, and terminal abstention.",
        rollback_or_recovery="Withdraw causal and promotion credit, retain failed vectors, require preregistered real data and independent review, and keep Stage 20 not ready.",
        protected_gates=["real_data", "participant_effect", "causal_identification", "independent_review", "stage20", "proof_or_canon"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior Stage 20 boards cover many causal and validation designs, but none centers synthetic-control donor construction, pre-treatment fit, constrained weights, spillover, placebos, and sensitivity.",
    ),
]


SOURCES = [
    {"source_id":"V6482-S01","title":"fcntl — file and I/O control","url":"https://docs.python.org/3/library/fcntl.html","publisher":"Python Software Foundation","status":"current","source_class":"official_documentation","use":"advisory lock vocabulary and platform boundary only"},
    {"source_id":"V6482-S02","title":"LockFileEx function","url":"https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex","publisher":"Microsoft Learn","status":"current","source_class":"official_documentation","use":"Windows byte-range locking and release context only"},
    {"source_id":"V6482-S03","title":"Statistical-mechanical theory of irreversible processes I","url":"https://doi.org/10.1143/JPSJ.12.570","publisher":"Journal of the Physical Society of Japan","status":"stable","source_class":"primary_research","use":"Kubo equilibrium correlation provenance only"},
    {"source_id":"V6482-S04","title":"Theory of many-particle systems I","url":"https://doi.org/10.1103/PhysRev.115.1342","publisher":"Physical Review","status":"stable","source_class":"primary_research","use":"Martin-Schwinger thermal Green-function boundary provenance only"},
    {"source_id":"V6482-S05","title":"LoTSS Data Release 2","url":"https://lofar-surveys.org/dr2_release.html","publisher":"LOFAR Surveys","status":"current","source_class":"official_data_release_description","use":"release and product provenance with zero-row gate only"},
    {"source_id":"V6482-S06","title":"The LOFAR Two-metre Sky Survey V: Second data release","url":"https://doi.org/10.1051/0004-6361/202142484","publisher":"Astronomy and Astrophysics","status":"stable","source_class":"primary_research","use":"survey footprint calibration resolution and selection obligations only"},
    {"source_id":"V6482-S07","title":"Safe use of machinery","url":"https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/","publisher":"WorkSafe New Zealand","status":"current","source_class":"official_regulator_guidance","use":"guarding stop and competent-person boundary vocabulary only"},
    {"source_id":"V6482-S08","title":"Keeping workers safe with machine lockouts","url":"https://www.worksafe.govt.nz/topic-and-industry/machinery/keeping-workers-safe-with-machine-lockouts/","publisher":"WorkSafe New Zealand","status":"current","source_class":"official_regulator_guidance","use":"isolation restart and shift-change boundary vocabulary only"},
    {"source_id":"V6482-S09","title":"JWT Secured Authorization Response Mode for OAuth 2.0 Final","url":"https://openid.net/specs/oauth-v2-jarm-final.html","publisher":"OpenID Foundation","status":"current","source_class":"official_final_specification","use":"JARM response and verification obligations"},
    {"source_id":"V6482-S10","title":"JARM first errata public review","url":"https://openid.net/public-review-jwt-secured-authorization-response-mode-oauth-2-0/","publisher":"OpenID Foundation","status":"watch","source_class":"official_errata_review","use":"watch-only errata context; no final promotion"},
    {"source_id":"V6482-S11","title":"Privacy Act 2020 information privacy principles","url":"https://www.privacy.org.nz/privacy-principles/","publisher":"Office of the Privacy Commissioner New Zealand","status":"current","source_class":"official_regulator_material","use":"current privacy and IPP 3A reservation; not legal interpretation"},
    {"source_id":"V6482-S12","title":"Principles of Māori Data Sovereignty","url":"https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf","publisher":"Te Mana Raraunga","status":"stable","source_class":"maori_authority_source","use":"Māori data-governance and authority gate; never delegated authority"},
    {"source_id":"V6482-S13","title":"RFC 8878 Zstandard Compression and application/zstd","url":"https://www.rfc-editor.org/rfc/rfc8878.html","publisher":"RFC Editor / IETF","status":"stable","source_class":"official_rfc","use":"Zstandard frame and bounded refusal obligations"},
    {"source_id":"V6482-S14","title":"Accessible Rich Internet Applications 1.2","url":"https://www.w3.org/TR/wai-aria-1.2/","publisher":"W3C","status":"current","source_class":"official_recommendation","use":"progressbar role state and value obligations"},
    {"source_id":"V6482-S15","title":"WAI-ARIA Authoring Practices 1.2","url":"https://www.w3.org/TR/wai-aria-practices-1.2/","publisher":"W3C","status":"stable","source_class":"official_working_group_note","use":"structural author guidance with manual evaluation reserved"},
    {"source_id":"V6482-S16","title":"IUPAC Gold Book: Gibbs adsorption","url":"https://goldbook.iupac.org/terms/view/G02627","publisher":"IUPAC","status":"current","source_class":"official_terminology","use":"surface-excess and dividing-surface definition"},
    {"source_id":"V6482-S17","title":"IUPAC Gold Book: surface excess","url":"https://goldbook.iupac.org/terms/view/S06171","publisher":"IUPAC","status":"current","source_class":"official_terminology","use":"interface reference-system and unit context only"},
    {"source_id":"V6482-S18","title":"Synthetic Control Methods for Comparative Case Studies","url":"https://www.nber.org/papers/w12831","publisher":"NBER","status":"stable","source_class":"primary_research","use":"donor-pool weighting pre-fit and placebo provenance"},
    {"source_id":"V6482-S19","title":"Comparative Politics and the Synthetic Control Method","url":"https://doi.org/10.1111/ajps.12116","publisher":"American Journal of Political Science","status":"stable","source_class":"primary_research","use":"interpretation and design limitations only"},
]


SAFE_TASK_TITLES = [
    "Verify Tamar source anchors manifests history and four-way equality before mutation",
    "Fast-forward only the clean Sylven canonical lane and prove equality",
    "Reconcile all 560 frozen proposal titles before novelty credit",
    "Quarantine lock KMS LoTSS machining JARM Zstandard progressbar adsorption and synthetic-control collisions",
    "Review current stable and watch source statuses",
    "Record LoTSS DR2 provenance without downloading data",
    "Declare commit-blob and working-tree hash domains separately",
    "Separate scanner definitions from confirmed privacy incidents",
    "Measure inherited checkout and Sylven-generated footprints separately",
    "Initialize Method Flow with every observed x1 failure retained",
    "Build advisory-lock disposable-fixture contract",
    "Build KMS typed obligation contract",
    "Build LoTSS DR2 zero-row receipt schema",
    "Build machining handover synthetic trace schema",
    "Build JARM synthetic profile schema",
    "Build machining incident authority reservation schema",
    "Build Zstandard disposable-byte contract",
    "Build progressbar structural fixture",
    "Build Gibbs adsorption domain classifier fixture",
    "Build synthetic-control nonpromotion fixture",
    "Preserve citation-to-observation and authority firewalls",
    "Carry forward 26 open gaps and 27 exact gates",
    "Carry forward the 3938-negative activation continuity",
    "Keep terminal route PREPARED_NOT_SENT before proof",
    "Verify Codex versions without updating desktop",
    "Audit Windows Sandbox availability without elevation or feature change",
    "Audit family-current callers and historical compatibility aliases",
    "Freeze exact x1 staged surface with no x2 implementation",
    "Emit owner-scoped x1 wellbeing source and route receipts",
    "Validate every portfolio floor and protected packet count",
]

CANDIDATE_TITLES = [
    "Advisory-lock owner-token and bounded-contention prototype",
    "Stale-record PID-reuse release and credit prototype",
    "KMS state flow beta and analytic-strip prototype",
    "KMS boundary ordering spectral balance and observation-firewall prototype",
    "LoTSS release footprint flux and resolution provenance prototype",
    "LoTSS association selection covariance and zero-row prototype",
    "Machining drawing setup offset and tolerance prototype",
    "Machining nonconformance isolation workload and handover prototype",
    "JARM issuer audience expiry and signature prototype",
    "JARM encryption response-mode state replay and refusal prototype",
    "Machining incident worker machine privacy and hold matrix prototype",
    "Machining remedy affected-party legal and Māori-authority prototype",
    "Zstandard magic descriptor window and dictionary prototype",
    "Zstandard block checksum skippable frame and budget prototype",
    "Progressbar name range and determinate-value checker",
    "Progressbar indeterminate busy update and fallback classifier",
    "Gibbs dividing-surface excess and component prototype",
    "Gibbs chemical-potential tension unit and psyche-firewall prototype",
    "Synthetic-control donor pre-fit weight and interpolation prototype",
    "Synthetic-control spillover placebo sensitivity and nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-advisory-lock-tribunal", "Audit owner token contention stale metadata PID reuse release and credit"),
    ("ghc-family-kms-obligations", "Audit KMS flow strip boundary spectral gauge EFT and unit obligations"),
    ("ghc-family-lotss-dr2-zero-row", "Preserve a zero-row LoTSS DR2 likelihood boundary"),
    ("ghc-family-machining-handover-proxy", "Audit synthetic machining setup offset hold isolation and handover"),
    ("ghc-family-jarm-profile", "Audit synthetic JARM response verification and refusal obligations"),
    ("ghc-family-machining-authority-reservation", "Reserve machining incident privacy remedy legal cultural and Māori gates"),
    ("ghc-family-zstd-frame-tribunal", "Audit Zstandard frame header block checksum dictionary and budget obligations"),
    ("ghc-family-progressbar-audit", "Audit progressbar range indeterminate busy update and fallback structure"),
    ("ghc-family-gibbs-adsorption-domain", "Keep Gibbs adsorption claims inside interfacial thermodynamics"),
    ("ghc-family-synthetic-control-nonpromotion", "Guard donor fit weights spillover placebos and sensitivity from promotion"),
    ("ghc-family-corpus-560-collision-gate", "Audit exact and semantic novelty against 560 frozen proposals"),
    ("ghc-family-source-status-watch-v3", "Record current stable and watch source status without promotion"),
    ("ghc-family-x1-x2-byte-separation-v3", "Prove x1 contains no x2 implementation outcome or completion bytes"),
    ("ghc-family-named-replay-locality-v4", "Verify one named replay remains local clean unpushed and without upstream"),
    ("ghc-family-commit-cap-single-parent-v4", "Verify phase commit cap zero merges and single-parent final history"),
    ("ghc-family-five-class-privacy-adjudication-v4", "Separate scanner definitions candidates incidents and confirmed payload hits"),
    ("ghc-family-commit-manifest-parity-v5", "Audit exact commit-local manifests with declared self-exclusions"),
    ("ghc-family-stage-label-lifecycle-lint-v4", "Reject stale prepared sent evidence closeout seal and final labels"),
    ("ghc-family-authority-reservation-matrix-v4", "Prevent software evidence from compensating for professional or authority gaps"),
    ("ghc-family-baton-ack-one-shot-v4", "Count one existing-task baton only after acknowledged send"),
]

RUNNER_TITLES = [
    "ghc_family_advisory_lock_tribunal.py",
    "ghc_family_kms_obligations.py",
    "ghc_family_lotss_dr2_zero_row.py",
    "ghc_family_machining_handover.py",
    "ghc_family_jarm_profile.py",
    "ghc_family_machining_authority.py",
    "ghc_family_zstd_frame_tribunal.py",
    "ghc_family_progressbar_audit.py",
    "ghc_family_gibbs_adsorption.py",
    "ghc_family_synthetic_control_board.py",
]

CLEAN_TASK_TITLES = [
    "Reconcile proposal and expected-outcome counts across x1 receipts",
    "Reconcile inherited sealed external synthetic and operational negatives",
    "Synchronize Method Flow method witness and validator expectations",
    "Correct stale phase labels additively",
    "Preserve compatibility callers while selecting family-current tools",
    "Normalize generated JSON key ordering",
    "Normalize generated UTF-8 and LF authoring",
    "Keep commit-blob and working-tree hash domains explicit",
    "Review public files for private absolute paths",
    "Review public files for raw task or thread identifiers",
    "Review public files for credential token or private-key assignments",
    "Review source statuses for allowed vocabulary",
    "Review LoTSS sources for zero-row nonconversion",
    "Review citations for observation and authority nonconversion",
    "Review x1 staged files for x2 contamination",
    "Review expected dispositions without granting outcome credit",
    "Review exact and blocked packets for zero execution credit",
    "Review owner footprint against the 15000-file threshold",
    "Review progressbar report structure and manual reservations",
    "Review report assistive-technology motion cognitive and affected-user reservations",
    "Review Māori authority and data-governance reservations",
    "Review machining professional operational emergency and legal reservations",
    "Review real-data download query and likelihood counters remain zero",
    "Review real-worker employer machine job part measurement and incident counters remain zero",
    "Review real-key client server token and interoperability counters remain zero",
    "Review source and all phase-anchor ancestry",
    "Review phase commit cap zero merges and one final parent",
    "Review validation branch remains named and local-only",
    "Review canonical four-way remote equality",
    "Refresh phase-scoped index wellbeing and terminal route before handoff",
]

EXACT_PACKET_TITLES = [
    "Real LoTSS download likelihood posterior or parameter inference",
    "Real machining setup operation measurement isolation restart or stop-work action",
    "Real workplace incident investigation or safety decision",
    "Production JARM key response client authorization-server or token operation",
    "Real identity interoperability recovery or trust-governance decision",
    "Protected worker witness employer workplace machine or job information disclosure",
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
    {"negative_id":"V6482-X1-N01","method_id":"V6482-M01","summary":"The first combined read of both required skills and references exceeded its bounded tool envelope before returning content; exact sequential reads with a longer bounded envelope recovered every required file without mutation.","retained":True,"recovered":True},
    {"negative_id":"V6482-X1-N02","method_id":"V6482-M02","summary":"A combined newest-note read and MEMORY registry search returned nonzero because the registry had no match even though the targeted note read succeeded; separating no-match from execution failure recovered the bounded memory decision.","retained":True,"recovered":True},
    {"negative_id":"V6482-X1-N03","method_id":"V6482-M03","summary":"The first parallel owned-lane and proposal-discovery envelope timed out before returning its component results; decomposed read-only checks completed under bounded per-command envelopes and made no mutation.","retained":True,"recovered":True},
    {"negative_id":"V6482-X1-N04","method_id":"V6482-M04","summary":"The first family-current preregistration adapter rewrote its inherited-source directory into the new owner directory and failed before writing any packet; a final explicit source-path pin separated inherited reads from owner outputs.","retained":True,"recovered":True},
    {"negative_id":"V6482-X1-N05","method_id":"V6482-M05","summary":"The first successful template generation retained three predecessor literals: a 560 after-freeze count, v648-v1 core-surface prose, and a Sylven route target; exact pre-commit review rejected the generation and explicit lifecycle substitutions recovered it.","retained":True,"recovered":True},
    {"negative_id":"V6482-X1-N06","method_id":"V6482-M06","summary":"The staged reviewer received relative output paths and raised the same absolute-root relative_to error three times while the command chain continued to a final diff check; no review output or commit was produced, and internal path resolution recovered the exact review.","retained":True,"recovered":True,"recurrences":3},
    {"negative_id":"V6482-X1-N07","method_id":"V6482-M07","summary":"A read-only x1 summary assumed a Method Flow validation receipt existed before the family runner had materialized the prepared records; bounded enumeration exposed the runner-pending state and the required runner sequence recovered a validated ledger.","retained":True,"recovered":True},
]

METHOD_SPECS = [
    {
        "method_id":"V6482-M01","title":"Decompose exact skill reads after a content-free aggregate timeout",
        "failure_signature":"A combined exact read exceeded its bounded tool envelope before returning content.",
        "trigger_preconditions":["Multiple required instruction files are exact and known but an aggregate read expires."],
        "candidate_workaround":"Read each exact required file sequentially with a longer bounded envelope and stop only after complete content is returned.",
        "recurrence_guard":"Do not infer absence or partial compliance from an aggregate read timeout.",
        "rollback":"Discard the timeout result; it changed no repository or external state.",
        "protected_gates":["skill_completeness","routing_precedence","method_flow_schema","no_repository_mutation"],
        "retained_negative_ids":["V6482-X1-N01"],
        "failed_observed":"The first aggregate skill read returned no content before its tool envelope expired.",
        "pass_observed":"All four exact skill and required-reference files completed under separate bounded reads before task mutation.",
    },
    {
        "method_id":"V6482-M02","title":"Treat registry search exit one as a no-match state rather than a failed exact note read",
        "failure_signature":"A combined command returned nonzero solely because a bounded registry search found no matching line after the targeted note read had succeeded.",
        "trigger_preconditions":["A targeted newest memory note is readable and a supplemental rg lookup may legitimately find no match."],
        "candidate_workaround":"Preserve the successful targeted read, classify rg exit one as no match, and let the live verified baton outrank older memory.",
        "recurrence_guard":"Capture exact-read and optional-search outcomes separately when no match is allowed.",
        "rollback":"Discard only the overstrict combined status; no file or ref changed.",
        "protected_gates":["newest_memory","live_baton_precedence","privacy","no_repository_mutation"],
        "retained_negative_ids":["V6482-X1-N02"],
        "failed_observed":"The combined wrapper reported failure despite a complete targeted note read because rg returned its documented no-match code.",
        "pass_observed":"The targeted note was retained as feeder continuity and the live v648-v2 baton supplied authoritative Tamar source truth.",
    },
    {
        "method_id":"V6482-M03","title":"Decompose slow Git and proposal discovery into bounded witnesses",
        "failure_signature":"A parallel discovery envelope timed out before returning component results.",
        "trigger_preconditions":["A large Windows worktree makes status and broad proposal scans slower than a shared aggregate timeout."],
        "candidate_workaround":"Run clean-state, ancestry, equality, schema, and concept searches as separate bounded commands and retain each completed witness.",
        "recurrence_guard":"Avoid broad worktree enumeration inside a short shared timeout; bound each required witness independently.",
        "rollback":"Discard the timed-out aggregate; it issued read-only commands and made no mutation.",
        "protected_gates":["clean_state","ancestry","novelty","remote_equality","no_repository_mutation"],
        "retained_negative_ids":["V6482-X1-N03"],
        "failed_observed":"The initial parallel envelope expired at twenty seconds without returning its component outputs.",
        "pass_observed":"Decomposed commands proved the clean ancestor lane, safe fast-forward path, exact four-way equality, proposal schema, and candidate novelty space.",
    },
    {
        "method_id":"V6482-M04","title":"Pin inherited read paths after owner-phase template substitution",
        "failure_signature":"A family-current builder adapter transformed its inherited-source directory into the new owner output directory and raised FileNotFoundError before writing output.",
        "trigger_preconditions":["A successor adapts a prior builder whose owner and phase strings occur in both output paths and inherited-source paths."],
        "candidate_workaround":"Apply owner and phase substitutions, then explicitly restore the exact inherited source directory and proposal-ledger path as the final transformation step.",
        "recurrence_guard":"Keep inherited read roots and current owner write roots in distinct explicit domains after every template transformation.",
        "rollback":"No rollback was required because the failure preceded every packet write and changed no ref.",
        "protected_gates":["source_provenance","owner_scope","x1_only","no_sibling_mutation"],
        "retained_negative_ids":["V6482-X1-N04"],
        "failed_observed":"The adapter sought the prior proposal index under the absent new owner phase directory and stopped before writes.",
        "pass_observed":"The corrected adapter read all 560 frozen proposals from Tamar v648-v1 while writing only Sylven v648-v2 owner-scoped x1 artifacts.",
    },
    {
        "method_id":"V6482-M05","title":"Review every hardcoded lifecycle and narrative literal after family-template adaptation",
        "failure_signature":"A structurally valid generated packet retained predecessor after-freeze, core-surface, and terminal-route literals.",
        "trigger_preconditions":["A versioned builder contains arithmetic and narrative literals that are not derived from imported definitions."],
        "candidate_workaround":"Reject the generated packet before staging, add exact substitutions for the lifecycle count, core surfaces, practice vocabulary, and successor route, then regenerate deterministically.",
        "recurrence_guard":"Run stale-topic, count, owner, source, and route scans before any x1 staged review or commit.",
        "rollback":"Overwrite only the uncommitted owner-generated packet from frozen definitions; retain this failed generation as an operational negative.",
        "protected_gates":["semantic_novelty","lifecycle_truth","route_truth","x1_freeze"],
        "retained_negative_ids":["V6482-X1-N05"],
        "failed_observed":"Exact review found frozen_after_x1 560, predecessor core topics, and a Sylven successor target in the first generated packet.",
        "pass_observed":"Regeneration reports 570 frozen proposals, only v648-v2 core surfaces, and PREPARED_NOT_SENT routing to Eiren v648-v3.",
    },
    {
        "method_id":"V6482-M06","title":"Resolve staged-review output paths before repository-relative classification",
        "failure_signature":"Path.relative_to rejected a relative output path against an absolute repository root; the signature recurred three times in one non-stop chain.",
        "trigger_preconditions":["The staged reviewer is invoked from the repository root with relative review, manifest, and privacy output arguments."],
        "candidate_workaround":"Resolve each output path to an absolute path before deriving its repository-relative self-exclusion.",
        "recurrence_guard":"Make the reviewer normalize paths internally and stop chained lifecycle commands on the first failed review.",
        "rollback":"No review outputs or commit existed; retain the staged owner files and rerun only after regenerating the expanded negative ledger.",
        "protected_gates":["exact_staged_review","manifest_parity","privacy_scan","x1_commit"],
        "retained_negative_ids":["V6482-X1-N06"],
        "failed_observed":"Three identical relative_to failures occurred and their following git-add calls found no output paths; the final diff check masked the chain status.",
        "pass_observed":"The normalized reviewer generated deterministic x1 review, manifest, and five-class privacy receipts from the exact Git index.",
    },
    {
        "method_id":"V6482-M07","title":"Materialize prepared Method Flow records with the family runner before reading derived receipts",
        "failure_signature":"A read-only summary sought a derived Method Flow validation receipt while only runner-pending method records and witnesses existed.",
        "trigger_preconditions":["The preregistration builder has prepared records and witnesses but has not invoked init, record, witness, set-state, validate, and summarize."],
        "candidate_workaround":"Enumerate the bounded Method Flow directory, run the required family runner sequence for every prepared record and witness, then read the explicitly named validation receipt.",
        "recurrence_guard":"Treat generated record files as runner input, not as a validated ledger; require the runner receipt before x1 freeze.",
        "rollback":"Discard the null summary field; it changed no repository data beyond the already staged owner packet.",
        "protected_gates":["method_flow","failed_witness_retention","preferred_state","x1_freeze"],
        "retained_negative_ids":["V6482-X1-N07"],
        "failed_observed":"The assumed method-flow-validation.json path did not exist and the summary emitted a null Method Flow state.",
        "pass_observed":"The family runner materialized seven methods, seven failed witnesses, seven passing witnesses, preferred transitions, validation, and summary receipts.",
    },
]
