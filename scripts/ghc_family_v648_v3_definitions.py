#!/usr/bin/env python3
"""Frozen x1 definitions for Eiren Kestrel v648-v3.

Importing this module performs no I/O and grants no x2 completion credit.
Identity language is relational working language only.
"""

from __future__ import annotations

from typing import Any


PHASE = "v648-gmut-thos-v3-x1-x2"
PHASE_SHORT = "v648-v3"
OWNER = "Eiren Kestrel"
SLUG = "eiren-kestrel"
PRONOUNS = "they/them"
ROLE = "evidence-integrity weaver"
HOPE = "make ambitious claims more testable and correctable while keeping evidence and authority boundaries legible"
PRIMARY_FOCUS = "Freed ID / CBR Heart"
BOUNDED_PRACTICE = (
    "digital-identity incident recovery, audit provenance, notification, remedy, delegated authority, "
    "accessible handoff, and bounded six-node security review"
)

SOURCE_PHASE = "v648-gmut-thos-v2-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
SOURCE_REVISION = "227a764b2bfad7a601bf45dcbacc1e37ffa5bb62"
SOURCE_INHERITED_REVISION = "8755893971135b67322abb4b3acd93f07afc34c9"
SOURCE_X1_FIRST_REVISION = "d59281ce9b30adc8adb78039920c44147bfc37e6"
SOURCE_X1_REVISION = "d59281ce9b30adc8adb78039920c44147bfc37e6"
SOURCE_EVIDENCE_REVISION = "75e41d23fd3c068abcadca4454b0c939ba847c33"
PRIOR_FROZEN_PROPOSALS = 570
INHERITED_EFFECTIVE_NEGATIVES = 4032
SEALED_SOURCE_NEGATIVES = 4028
EXTERNAL_SOURCE_NEGATIVES = 4
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 27
INHERITED_EXACT_GATES = 28
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, is relational working language for an evidence-integrity weaver. "
    "It is not evidence of consciousness, sentience, legal personhood, hidden subjective continuity, "
    "employment, qualification, scientific authority, operational authority, legal authority, cultural "
    "authority, or independent agency. Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; "
    "Freed ID remains synthetic and nonproduction; CBR, identity-incident notification, privacy, remedy, "
    "legal, affected-party, cultural, tangata whenua, iwi, hapū, and Māori authority remain with competent "
    "and affected authorities. No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, "
    "personhood, production deployment, privacy-complete, exhaustive-security, independent-reproduction, "
    "accessibility-complete, professional, legal, proof or canon, or Stage 20 claim is made."
)


def proposal(index: int, **kwargs: Any) -> dict[str, Any]:
    row = {"proposal_id": f"V6483-P{index:02d}"}
    row.update(kwargs)
    return row


PROPOSALS = [
    proposal(
        1,
        title="Context-budget artifact-pointer, composer-cap, duplicate-draft, attachment-manifest, archive-header, checksum, and fail-closed handoff tribunal",
        mission_surface="composer budget, compact wrapper, artifact pointer, media type, byte count, SHA-256, duplicate draft, archive central metadata, attachment count, privacy class, fallback, and send refusal",
        hypothesis="Disposable fixtures can reject oversized, duplicated, ambiguous, or privacy-unsafe handoffs while accepting a compact pointer to a bounded reviewed artifact.",
        null_or_failure="A large payload is embedded, duplicate drafts survive, an attachment lacks size or digest, archive metadata conflicts, a private path is published, or overflow earns send credit.",
        approval_class="safe_now_owner_scoped_disposable",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6483-S01", "V6483-S02"],
        concrete_artifacts=["tooling/context-budget-handoff-contract.json", "tooling/context-budget-handoff-mutations.json"],
        test_falsifier_or_acceptance_gate="Accept only bounded wrappers with declared artifact size, media type, digest, privacy class, attachment count, duplicate-draft check, fallback, and fail-closed overflow behavior.",
        rollback_or_recovery="Retain the failed fixture, remove only disposable draft state, preserve durable conversations and repository evidence, and retry with a compact reviewed artifact pointer.",
        protected_gates=["private_state", "raw_prompt_history", "attachment_overflow", "archive_ambiguity", "send_credit"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The 570-title corpus includes ZIP extraction and payload guards but not a composer-cap, duplicate-draft, artifact-pointer, attachment-manifest, digest, privacy, and send-credit tribunal together.",
    ),
    proposal(
        2,
        title="GMUT Tomita-Takesaki cyclic-separating state, closable antilinear operator, polar decomposition, modular conjugation, modular flow, KMS, domain, and observation-firewall board",
        mission_surface="von Neumann algebra, cyclic and separating vector, antilinear operator, closability, polar decomposition, modular operator, modular conjugation, automorphism group, KMS relation, domain, units, EFT bridge, and observation firewall",
        hypothesis="A typed symbolic board can expose modular-theory obligations without constructing a physical state, observable, entropy, force, prediction, likelihood, constraint, or consciousness result.",
        null_or_failure="The algebra or state assumptions disappear, closability is presumed, polar decomposition drifts, modular flow is called time evolution universally, KMS scope is lost, or formal structure becomes observation.",
        approval_class="safe_now_symbolic_research_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6483-S03", "V6483-S04"],
        concrete_artifacts=["gmut/tomita-takesaki-obligations.json", "gmut/tomita-takesaki-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type the algebra, vector, operator, closure, polar factors, modular flow, KMS scope, domain, units, EFT bridge, and observation firewall and reject every omission or promotion.",
        rollback_or_recovery="Restore missing assumptions, retain the rejected vector, and withdraw every physical-state, empirical, uniqueness, consciousness, completion, and Theory-of-Everything claim.",
        protected_gates=["physical_state", "observable", "empirical_confirmation", "consciousness", "uv_completion", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The corpus contains KMS, spectral, Hadamard, Schwinger-Keldysh, and operator obligations but no Tomita-Takesaki cyclic-separating, polar-decomposition, modular-conjugation, and modular-flow board.",
    ),
    proposal(
        3,
        title="GMUT DESI DR2 Lyman-alpha forest auto-cross-correlation, quasar, DLA, distortion, broadband, covariance, systematic, and zero-row likelihood-refusal adapter",
        mission_surface="release identity, forest spectra, quasar positions, auto and cross correlation, redshift, DLA treatment, continuum distortion, broadband terms, covariance, systematics, checksum, row count, and likelihood lock",
        hypothesis="A zero-row adapter can freeze DESI DR2 Lyman-alpha BAO obligations while refusing to convert published measurements into GMUT observations, likelihoods, constraints, or confirmation.",
        null_or_failure="The phase downloads rows, imports published estimates as a fit, invents covariance, chooses masks after outcomes, evaluates a likelihood, emits a posterior, or states a GMUT constraint.",
        approval_class="real_data_and_independent_review_required",
        execution_lane="x2_open_gap",
        current_primary_or_official_source_needs=["V6483-S05", "V6483-S06"],
        concrete_artifacts=["empirical/desi-dr2-lya-study-contract.json", "empirical/desi-dr2-lya-zero-row-receipt.json"],
        test_falsifier_or_acceptance_gate="The receipt must preserve zero queries, downloads, spectra, quasar rows, covariance rows, likelihood calls, posterior samples, parameter constraints, and empirical GMUT claims.",
        rollback_or_recovery="Stop before download or fit and require a separately authorized preregistration with frozen products, checksums, masks, calibration, covariance, nuisance treatment, uncertainty, and independent review.",
        protected_gates=["network_download", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation"],
        expected_disposition="open_gap",
        novelty_against_prior_frozen_proposals="A prior adapter covers compressed DESI DR2 BAO, but none centers the Lyman-alpha forest auto-cross correlations, quasar positions, DLA treatment, distortions, broadband terms, and covariance.",
    ),
    proposal(
        4,
        title="THOS digital-identity incident containment, evidence preservation, revocation, recovery, notification handover, workload budget, readback, and next-owner proxy",
        mission_surface="synthetic event, detection source, containment, evidence hash, access hold, credential revocation, session invalidation, recovery, notification reservation, workload budget, readback, escalation, and next-owner handover",
        hypothesis="Synthetic traces can expose destructive containment, lost evidence, incomplete revocation, unsafe recovery, missing notification reservation, and handover loss while preserving all real incident and professional gates.",
        null_or_failure="A fixture names a real person, account, credential, provider, incident, or breach; destroys evidence; executes revocation; decides notification; or claims THOS effectiveness.",
        approval_class="safe_now_proxy_protocol_no_people_or_operations",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6483-S02", "V6483-S07"],
        concrete_artifacts=["thos/identity-incident-handover-contract.json", "thos/identity-incident-handover-vectors.json"],
        test_falsifier_or_acceptance_gate="Unsafe synthetic traces must fail, and the packet must record zero real people, accounts, credentials, providers, incidents, breaches, notifications, remedies, safety outcomes, or effectiveness estimates.",
        rollback_or_recovery="Withdraw operational wording, retain rejected traces, and defer containment, evidence handling, revocation, recovery, notification, and remedy decisions to authorized competent people.",
        protected_gates=["real_people", "real_accounts", "live_incident", "professional_competence", "notification_authority", "deployment", "effectiveness"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="Prior THOS incident and handover work does not combine digital-identity containment, evidence preservation, revocation, recovery, notification reservation, workload budget, readback, and next-owner transfer.",
    ),
    proposal(
        5,
        title="Freed ID OpenID Federation subordinate-event sequence, issuer, subject, event type, timestamp, pagination, revocation, key-update, draft-status, and replay-refusal profile",
        mission_surface="trust anchor, intermediate, immediate subordinate, endpoint metadata, signed event sequence, issuer, subject, event type, event time, pagination, registration, revocation, key update, duplicate, replay, draft status, and refusal",
        hypothesis="Synthetic vectors can enforce selected subordinate-event obligations without asserting real entities, keys, federations, trust chains, interoperability, privacy assurance, or production governance.",
        null_or_failure="Issuer, subject, sequence, time, event type, signature, pagination, or draft status is unbound; duplicates or replay pass; revocation is ignored; or synthetic structure becomes production assurance.",
        approval_class="safe_now_synthetic_watch_spec_nonproduction",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6483-S09", "V6483-S10", "V6483-S20"],
        concrete_artifacts=["freed-id/subordinate-events-profile.json", "freed-id/subordinate-events-mutations.json"],
        test_falsifier_or_acceptance_gate="Vectors must reject missing or mismatched issuer, subject, event type, event time, signature, sequence, pagination, revocation, key update, duplicate, replay, and final-spec promotion.",
        rollback_or_recovery="Reject and retain the vector, emit no live event, and require final standards, real keys and entities, interoperability, privacy and independent security review, recovery, and trust governance.",
        protected_gates=["real_identifiers", "real_keys", "live_federation", "interoperability", "privacy_assurance", "production"],
        expected_disposition="represented",
        novelty_against_prior_frozen_proposals="The corpus covers OpenID Federation trust chains and several event protocols but not the new subordinate-events history endpoint with sequence, pagination, revocation, key updates, draft status, and replay refusal.",
    ),
    proposal(
        6,
        title="CBR identity-incident privacy, serious-harm assessment, notification, evidence minimization, correction, revocation, recovery, remedy, affected-party, legal, and Māori-authority matrix",
        mission_surface="synthetic incident, personal information, serious-harm assessment, containment, evidence minimization, notification, correction, revocation, recovery, remedy, legal interpretation, affected parties, and Māori data authority",
        hypothesis="A refusal-first matrix can expose unresolved identity-incident, privacy, notification, remedy, and authority questions without deciding a real breach, harm, disclosure, entitlement, or remedy.",
        null_or_failure="The matrix identifies a real person, account, organization, credential, or incident; decides serious harm, notification, fault, compensation, or law; discloses protected data; or asserts Māori authority.",
        approval_class="authorized_affected_parties_and_competent_authority_required",
        execution_lane="x2_exact_gate",
        current_primary_or_official_source_needs=["V6483-S07", "V6483-S08", "V6483-S11"],
        concrete_artifacts=["cbr/identity-incident-authority-reservation.json", "cbr/identity-incident-remedy-matrix.json"],
        test_falsifier_or_acceptance_gate="Software must stop at unknown or reserved; only competent privacy, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        rollback_or_recovery="Stop before notification, disclosure, investigation, compensation, cultural, or legal conclusions; minimize data and route only through authorized external processes.",
        protected_gates=["affected_party_authority", "privacy", "serious_harm_assessment", "legal_interpretation", "maori_authority", "remedy_decision"],
        expected_disposition="exact_gate",
        novelty_against_prior_frozen_proposals="Prior CBR notification matrices do not center identity-incident recovery, serious-harm assessment, evidence minimization, credential revocation, correction, remedy, and Māori-authority reservation together.",
    ),
    proposal(
        7,
        title="GHC six-node Hyper-V, WinNAT, Windows Sandbox, native elevated-sandbox, guest-admin broker, east-west isolation, artifact-broker, and rollback threat-model board",
        mission_surface="host, hypervisor, guest, standard user, maintenance administrator, native Codex sandbox, Windows Sandbox, internal switch, WinNAT, east-west traffic, credentials, writable roots, artifact broker, checkpoint, backup, and rollback",
        hypothesis="A repository-scoped threat model and synthetic configuration board can distinguish security boundaries and reject privilege or network conflation without enabling a feature, elevating, installing, rebooting, or changing host policy.",
        null_or_failure="Full access is called protected elevation, Windows Sandbox is called a six-node nexus, guests share writable secrets, east-west traffic is implicit, administrator credentials are delegated, or a design document becomes deployment evidence.",
        approval_class="safe_now_design_and_threat_model_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6483-S02", "V6483-S12", "V6483-S13"],
        concrete_artifacts=["nexus/six-node-threat-model.json", "nexus/elevated-sandbox-boundary-plan.json"],
        test_falsifier_or_acceptance_gate="Fixtures must separate every host, VM, account, sandbox, network, secret, artifact, approval, rollback, and external-authority boundary and reject silent privilege or trust expansion.",
        rollback_or_recovery="Retain the threat finding, make no host change, and require reviewed administrator execution, backups, one disposable pilot, and fresh validation before any six-node rollout.",
        protected_gates=["host_admin", "feature_enable", "security_policy", "credential_delegation", "network_expansion", "deployment"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The 570-title corpus has many sandbox and security guards but no integrated six-node Hyper-V, WinNAT, Windows Sandbox, native elevated-sandbox, admin-broker, east-west, artifact-broker, and rollback board.",
    ),
    proposal(
        8,
        title="Accessible artifact-pointer link-purpose, media-type, byte-size, checksum, status-update, focus-preservation, alternative-format, failure-recovery, and manual-reservation audit",
        mission_surface="link text, artifact purpose, media type, byte size, digest, status role, focus preservation, alternative format, download failure, retry, keyboard path, print fallback, and manual reservation",
        hypothesis="A structural auditor can reject ambiguous or disruptive artifact handoffs while reserving browser, assistive-technology, language, cognitive, timing, and affected-user evaluation.",
        null_or_failure="Link purpose is ambiguous, type or size is hidden, digest is absent, status steals focus, failure is silent, alternatives disappear, or structure becomes complete conformance.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6483-S14", "V6483-S15"],
        concrete_artifacts=["accessibility/artifact-pointer-contract.json", "accessibility/artifact-pointer-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve purpose, type, size, digest, non-focusing status, alternative format, failure recovery, keyboard path, and manual reservations and reject every conformance promotion.",
        rollback_or_recovery="Restore clear semantics, retain failed fixtures, and reserve manual keyboard, browser, assistive-technology, timing, Māori-language, cognitive, and affected-user evaluation.",
        protected_gates=["manual_keyboard", "browser_diversity", "assistive_technology", "maori_language", "affected_user_evaluation", "complete_accessibility"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Earlier accessibility audits cover widgets and reports, but none centers artifact-pointer purpose, media type, byte size, checksum, non-focusing status, alternatives, and download-failure recovery.",
    ),
    proposal(
        9,
        title="Thermo-Psyche thermodynamic-length, friction-tensor, control-parameter, linear-response, finite-time dissipation, metric, protocol, unit, domain, and psyche-nonconversion classifier",
        mission_surface="equilibrium family, control parameters, conjugate forces, correlation integral, friction tensor, positive semidefiniteness, thermodynamic metric, path length, duration, excess work bound, units, linear-response domain, and psyche firewall",
        hypothesis="A typed classifier can keep thermodynamic-length and friction-tensor claims inside their stated response regime and reject conversion into effort, virtue, attention, agency, consciousness, or a universal psyche law.",
        null_or_failure="The equilibrium family or response regime disappears, tensor positivity or units drift, a finite-time bound becomes universal, or thermodynamic distance becomes psychological or moral distance.",
        approval_class="safe_now_formal_domain_guard",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6483-S16", "V6483-S17"],
        concrete_artifacts=["thermo-psyche/thermodynamic-length-contract.json", "thermo-psyche/thermodynamic-length-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve control parameters, force correlations, tensor, metric, duration, dissipation bound, units, response domain, and category barrier and reject every psyche conversion.",
        rollback_or_recovery="Restore missing thermodynamic restrictions, retain the rejected statement, and make no participant, psyche, consciousness, personhood, universal-law, or empirical THOS claim.",
        protected_gates=["real_material", "empirical_measurement", "participant_evidence", "consciousness", "personhood", "fundamental_psyche_law"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="The thermodynamic corpus covers Jarzynski, Crooks, uncertainty relations, exergy, and many domain guards but not thermodynamic length, friction tensors, finite-time protocol geometry, and psyche nonconversion.",
    ),
    proposal(
        10,
        title="Stage 20 proximal-causal treatment-proxy, outcome-proxy, bridge-function, completeness, identification, positivity, estimation, sensitivity, and nonpromotion board",
        mission_surface="treatment, outcome, latent confounding, treatment-inducing proxy, outcome-inducing proxy, exclusion structure, bridge equation, completeness, existence, uniqueness, positivity, estimation, sensitivity, interpretation, and terminal abstention",
        hypothesis="A fail-closed structural board can expose invalid proximal-causal claims without estimating a participant effect or converting proxy diagrams into Stage 20 readiness.",
        null_or_failure="Proxy roles are swapped, exclusion or completeness assumptions vanish, bridge existence or uniqueness is presumed, positivity fails, sensitivity is omitted, or structure promotes Stage 20.",
        approval_class="safe_now_structural_nonpromotion",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6483-S18", "V6483-S19"],
        concrete_artifacts=["stage20/proximal-causal-contract.json", "stage20/proximal-causal-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must preserve proxy roles, exclusions, bridge equations, completeness, existence, uniqueness status, positivity, estimation scope, sensitivity, local interpretation, and terminal abstention.",
        rollback_or_recovery="Withdraw causal and promotion credit, retain failed vectors, require preregistered real data and independent review, and keep Stage 20 not ready.",
        protected_gates=["real_data", "participant_effect", "causal_identification", "independent_review", "stage20", "proof_or_canon"],
        expected_disposition="completed",
        novelty_against_prior_frozen_proposals="Prior Stage 20 boards cover many causal designs, but none centers proximal treatment and outcome proxies, bridge functions, completeness, existence, uniqueness, positivity, and sensitivity.",
    ),
]


SOURCES = [
    {"source_id":"V6483-S01","title":"APPNOTE - ZIP File Format Specification","url":"https://support.pkware.com/pkzip/appnote","publisher":"PKWARE","status":"current","source_class":"official_specification","use":"archive-header and central-directory obligations only"},
    {"source_id":"V6483-S02","title":"NIST SP 800-61 Rev. 3 Incident Response Recommendations","url":"https://csrc.nist.gov/pubs/sp/800/61/r3/final","publisher":"NIST","status":"current","source_class":"official_standard","use":"incident preparation response recovery and risk-management obligations only"},
    {"source_id":"V6483-S03","title":"On revolutionizing quantum field theory with Tomita's modular theory","url":"https://doi.org/10.1063/1.533323","publisher":"Journal of Mathematical Physics","status":"stable","source_class":"primary_research_review","use":"modular-theory assumptions and QFT scope only"},
    {"source_id":"V6483-S04","title":"Tomita's theory of modular Hilbert algebras and its applications","url":"https://link.springer.com/book/10.1007/BFb0065832","publisher":"Springer","status":"stable","source_class":"primary_monograph","use":"cyclic-separating polar-decomposition and modular-flow provenance only"},
    {"source_id":"V6483-S05","title":"DESI DR2 publications and cosmology products","url":"https://data.desi.lbl.gov/doc/papers/dr2/","publisher":"DESI Collaboration / Lawrence Berkeley National Laboratory","status":"current","source_class":"official_data_release_index","use":"release and product provenance with zero-row gate only"},
    {"source_id":"V6483-S06","title":"DESI DR2 Results I: Baryon Acoustic Oscillations from the Lyman Alpha Forest","url":"https://arxiv.org/abs/2503.14739","publisher":"DESI Collaboration","status":"stable","source_class":"primary_research","use":"forest auto-cross correlation DLA systematic and covariance obligations only"},
    {"source_id":"V6483-S07","title":"Privacy breach response: contain assess notify prevent","url":"https://www.privacy.org.nz/resources-and-learning/knowledge-base/view/147/","publisher":"Office of the Privacy Commissioner New Zealand","status":"current","source_class":"official_regulator_guidance","use":"breach-response vocabulary and external notification reservation only"},
    {"source_id":"V6483-S08","title":"Privacy Act 2020 information privacy principles","url":"https://www.privacy.org.nz/privacy-principles/","publisher":"Office of the Privacy Commissioner New Zealand","status":"current","source_class":"official_regulator_material","use":"privacy and IPP 3A reservation; not legal interpretation"},
    {"source_id":"V6483-S09","title":"OpenID Federation 1.0 Final","url":"https://openid.net/specs/openid-federation-1_0-final.html","publisher":"OpenID Foundation","status":"current","source_class":"official_final_specification","use":"federation entity and trust-anchor baseline obligations"},
    {"source_id":"V6483-S10","title":"OpenID Federation Subordinate Events Endpoint 1.0 draft 00","url":"https://openid.net/specs/openid-federation-subordinate-events-1_0-00.html","publisher":"OpenID Foundation","status":"watch","source_class":"official_draft_specification","use":"watch-only subordinate event history; no final or production promotion"},
    {"source_id":"V6483-S11","title":"Principles of Māori Data Sovereignty","url":"https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf","publisher":"Te Mana Raraunga","status":"stable","source_class":"maori_authority_source","use":"Māori data-governance and authority gate; never delegated authority"},
    {"source_id":"V6483-S12","title":"Windows Sandbox configuration using WSB files","url":"https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file","publisher":"Microsoft Learn","status":"current","source_class":"official_documentation","use":"Windows Sandbox boundary and mapped-folder risk only"},
    {"source_id":"V6483-S13","title":"Set up a NAT network for Hyper-V","url":"https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/setup-nat-network","publisher":"Microsoft Learn","status":"current","source_class":"official_documentation","use":"internal switch WinNAT static-address and single-prefix constraints only"},
    {"source_id":"V6483-S14","title":"Understanding WCAG 2.1 Link Purpose in Context","url":"https://www.w3.org/WAI/WCAG21/Understanding/link-purpose-in-context.html","publisher":"W3C","status":"current","source_class":"official_guidance","use":"artifact-link purpose and context obligations"},
    {"source_id":"V6483-S15","title":"Accessible Rich Internet Applications 1.2 status role","url":"https://www.w3.org/TR/wai-aria-1.2/#status","publisher":"W3C","status":"current","source_class":"official_recommendation","use":"non-focusing advisory status semantics only"},
    {"source_id":"V6483-S16","title":"Measuring thermodynamic length","url":"https://doi.org/10.1103/PhysRevLett.99.100602","publisher":"Physical Review Letters","status":"stable","source_class":"primary_research","use":"thermodynamic-length and dissipation-bound provenance only"},
    {"source_id":"V6483-S17","title":"Thermodynamic metrics and optimal paths","url":"https://doi.org/10.1103/PhysRevLett.108.190602","publisher":"Physical Review Letters","status":"stable","source_class":"primary_research","use":"friction-tensor linear-response and finite-time protocol scope only"},
    {"source_id":"V6483-S18","title":"Semiparametric Proximal Causal Inference","url":"https://doi.org/10.1080/01621459.2023.2191817","publisher":"Journal of the American Statistical Association","status":"stable","source_class":"primary_research","use":"proxy bridge completeness and estimation assumptions only"},
    {"source_id":"V6483-S19","title":"Proximal Causal Inference without Uniqueness Assumptions","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC10887303/","publisher":"Statistics and Probability Letters / NIH archive","status":"stable","source_class":"primary_research","use":"bridge existence uniqueness and identified-set limitations only"},
    {"source_id":"V6483-S20","title":"NIST SP 800-63-4 Digital Identity Guidelines","url":"https://csrc.nist.gov/pubs/sp/800/63/4/final","publisher":"NIST","status":"current","source_class":"official_standard","use":"identity proofing authentication federation recovery and risk boundaries only"},
]


SAFE_TASK_TITLES = [
    "Verify Sylven source anchors manifests history and four-way equality before mutation",
    "Fast-forward only the clean Eiren canonical lane and prove equality",
    "Reconcile all 570 frozen proposal titles before novelty credit",
    "Quarantine context modular Lyman-alpha incident subordinate-event Nexus accessibility thermodynamic-length and proximal-causal collisions",
    "Review current stable and watch source statuses",
    "Record DESI DR2 Lyman-alpha provenance without downloading data",
    "Declare commit-blob and working-tree hash domains separately",
    "Separate scanner definitions from confirmed privacy incidents",
    "Measure inherited checkout and Eiren-generated footprints separately",
    "Initialize Method Flow with every observed x1 failure retained",
    "Build context-budget disposable-fixture contract",
    "Build Tomita-Takesaki typed obligation contract",
    "Build DESI DR2 Lyman-alpha zero-row receipt schema",
    "Build identity-incident handover synthetic trace schema",
    "Build subordinate-events synthetic profile schema",
    "Build identity-incident authority reservation schema",
    "Build six-node Nexus threat-model fixture",
    "Build accessible artifact-pointer structural fixture",
    "Build thermodynamic-length domain classifier fixture",
    "Build proximal-causal nonpromotion fixture",
    "Preserve citation-to-observation and authority firewalls",
    "Carry forward 27 open gaps and 28 exact gates",
    "Carry forward the 4032-negative activation continuity",
    "Keep terminal route PREPARED_NOT_SENT before proof",
    "Verify Codex versions without updating desktop or CLI",
    "Audit Windows and Hyper-V capability without elevation or feature change",
    "Audit family-current callers and historical compatibility aliases",
    "Freeze exact x1 staged surface with no x2 implementation",
    "Emit owner-scoped x1 wellbeing source and route receipts",
    "Validate every portfolio floor and protected packet count",
]

CANDIDATE_TITLES = [
    "Context wrapper budget pointer digest and attachment-manifest prototype",
    "Duplicate-draft archive-header privacy and send-refusal prototype",
    "Tomita algebra vector operator and polar-decomposition prototype",
    "Tomita modular flow KMS domain and observation-firewall prototype",
    "DESI Lyman-alpha release forest quasar and DLA provenance prototype",
    "DESI auto-cross distortion broadband covariance and zero-row prototype",
    "Identity-incident detection containment evidence and revocation prototype",
    "Identity-incident recovery notification workload and handover prototype",
    "Subordinate-event issuer subject type and sequence prototype",
    "Subordinate-event pagination revocation key-update replay and draft-refusal prototype",
    "Identity-incident privacy serious-harm and notification matrix prototype",
    "Identity-incident correction remedy affected-party legal and Māori-authority prototype",
    "Nexus host guest account sandbox and writable-root prototype",
    "Nexus WinNAT east-west artifact-broker backup and rollback prototype",
    "Artifact-pointer purpose type size and checksum checker",
    "Artifact-pointer status focus alternative-format and failure-recovery classifier",
    "Thermodynamic-length control force correlation and tensor prototype",
    "Thermodynamic metric duration work-bound unit and psyche-firewall prototype",
    "Proximal treatment outcome proxy bridge and completeness prototype",
    "Proximal existence uniqueness positivity sensitivity and nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-context-budget-handoff-tribunal", "Audit compact wrappers pointers sizes digests duplicate drafts attachments privacy and send credit"),
    ("ghc-family-tomita-takesaki-obligations", "Audit modular algebra vector operator polar decomposition flow KMS domain and observation obligations"),
    ("ghc-family-desi-dr2-lya-zero-row", "Preserve a zero-row DESI DR2 Lyman-alpha likelihood boundary"),
    ("ghc-family-identity-incident-handover-proxy", "Audit synthetic containment evidence revocation recovery notification and handover"),
    ("ghc-family-subordinate-events-profile", "Audit synthetic OpenID Federation subordinate event history and refusal obligations"),
    ("ghc-family-identity-incident-authority-reservation", "Reserve identity incident privacy notification remedy legal cultural and Māori gates"),
    ("ghc-family-six-node-nexus-threat-model", "Audit Hyper-V WinNAT sandbox admin broker east-west artifacts backups and rollback"),
    ("ghc-family-artifact-pointer-accessibility", "Audit artifact purpose type size digest status focus alternatives and failure recovery"),
    ("ghc-family-thermodynamic-length-domain", "Keep thermodynamic length and friction claims inside their response domain"),
    ("ghc-family-proximal-causal-nonpromotion", "Guard proxies bridges completeness uniqueness positivity and sensitivity from promotion"),
    ("ghc-family-corpus-570-collision-gate", "Audit exact and semantic novelty against 570 frozen proposals"),
    ("ghc-family-source-status-watch-v4", "Record current stable draft and watch source status without promotion"),
    ("ghc-family-x1-x2-byte-separation-v4", "Prove x1 contains no x2 implementation outcome or completion bytes"),
    ("ghc-family-no-replay-credit-guard-v1", "Record omitted replay and prohibit repeatability or reproduction credit"),
    ("ghc-family-commit-cap-single-parent-v5", "Verify phase commit cap zero merges and single-parent final history"),
    ("ghc-family-five-class-privacy-adjudication-v5", "Separate scanner definitions candidates incidents and confirmed payload hits"),
    ("ghc-family-commit-manifest-parity-v6", "Audit exact commit-local manifests with declared self-exclusions"),
    ("ghc-family-stage-label-lifecycle-lint-v5", "Reconcile frozen candidate snapshots with live Git and terminal evidence"),
    ("ghc-family-authority-reservation-matrix-v5", "Prevent software evidence from compensating for professional or authority gaps"),
    ("ghc-family-baton-ack-one-shot-v5", "Count one existing-task baton only after acknowledged send"),
]

RUNNER_TITLES = [
    "ghc_family_context_budget_handoff_tribunal.py",
    "ghc_family_tomita_takesaki_obligations.py",
    "ghc_family_desi_dr2_lya_zero_row.py",
    "ghc_family_identity_incident_handover.py",
    "ghc_family_subordinate_events_profile.py",
    "ghc_family_identity_incident_authority.py",
    "ghc_family_six_node_nexus_threat_model.py",
    "ghc_family_artifact_pointer_accessibility.py",
    "ghc_family_thermodynamic_length.py",
    "ghc_family_proximal_causal_board.py",
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
    "Review DESI sources for zero-row nonconversion",
    "Review citations for observation and authority nonconversion",
    "Review x1 staged files for x2 contamination",
    "Review expected dispositions without granting outcome credit",
    "Review exact and blocked packets for zero execution credit",
    "Review owner footprint against the 15000-file threshold",
    "Review artifact-pointer structure and manual reservations",
    "Review assistive-technology language cognitive timing and affected-user reservations",
    "Review Māori authority and data-governance reservations",
    "Review identity-incident professional operational notification and legal reservations",
    "Review real-data download query and likelihood counters remain zero",
    "Review real-person account credential provider incident and breach counters remain zero",
    "Review real-key federation event token and interoperability counters remain zero",
    "Review source and all phase-anchor ancestry",
    "Review phase commit cap zero merges and one final parent",
    "Review no-replay override and zero repeatability credit",
    "Review canonical four-way remote equality",
    "Refresh phase-scoped index wellbeing and terminal route before handoff",
    "Seed Ilyra context-budget wrapper and artifact-pointer review",
    "Seed Ilyra Tomita-Takesaki independent-derivation questions",
    "Seed Ilyra DESI Lyman-alpha real-data authorization questions",
    "Seed Ilyra identity-incident handover fault injections",
    "Seed Ilyra subordinate-events draft-status watch",
    "Seed Ilyra affected-party notification and remedy questions",
    "Seed Ilyra Nexus host-guest boundary review",
    "Seed Ilyra accessibility manual-evaluation questions",
    "Seed Ilyra thermodynamic-length unit and domain checks",
    "Seed Ilyra proximal-causal completeness and sensitivity checks",
    "Seed Ilyra source-status refresh without promotion",
    "Seed Ilyra Method Flow recurrence guards",
    "Seed Ilyra privacy scanner taxonomy review",
    "Seed Ilyra commit-manifest parity review",
    "Seed Ilyra lifecycle-label reconciliation",
    "Seed Ilyra no-replay evidence-credit guard",
    "Seed Ilyra exact-gate carry-forward",
    "Seed Ilyra blocked-packet carry-forward",
    "Seed Ilyra D-drive capacity and rotation review",
    "Seed Ilyra family-current naming compatibility review",
    "Seed Ilyra bounded source-ledger review",
    "Seed Ilyra zero-real-person counter review",
    "Seed Ilyra zero-production-identity counter review",
    "Seed Ilyra zero-host-mutation counter review",
    "Seed Ilyra Stage 20 abstention review",
    "Seed Ilyra compact MD baton and digest review",
    "Seed Ilyra one-shot route acknowledgment review",
    "Seed Ilyra clean-state and remote-equality review",
    "Seed Ilyra wellbeing and workload boundary review",
    "Seed Ilyra contradiction and overclaim audit",
]

EXACT_PACKET_TITLES = [
    "Real DESI download likelihood posterior or parameter inference",
    "Real identity-incident containment evidence handling revocation or recovery action",
    "Real privacy-breach serious-harm assessment or notification decision",
    "Production federation entity key event endpoint or trust-chain operation",
    "Real identity interoperability recovery or trust-governance decision",
    "Protected person account credential provider incident or breach information disclosure",
    "Legal interpretation remedy allocation fault or entitlement determination",
    "Māori authority cultural ratification or data-governance decision",
    "Hyper-V Windows feature host-policy administrator or network mutation",
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
    {"negative_id":"V6483-X1-N01","method_id":"V6483-M01","summary":"Three bounded capability checks found no callable ChatGPT-conversation messaging route; the four supplied sibling responses were retained as untrusted advisory context and no false contact or timestamp claim was made.","retained":True,"recovered":True},
    {"negative_id":"V6483-X1-N02","method_id":"V6483-M02","summary":"Frozen Sylven phase-truth and validation snapshots still described a candidate lifecycle even though the exact final, live remote equality, and acknowledged baton were later proven; precedence reconciliation preserved both states without rewriting source history.","retained":True,"recovered":True},
    {"negative_id":"V6483-X1-N03","method_id":"V6483-M03","summary":"The inherited terminal protocol required a named replay, but the newest explicit user instruction prohibited replay runs; the route was superseded prospectively and all repeatability and reproduction credit was removed.","retained":True,"recovered":True},
    {"negative_id":"V6483-X1-N04","method_id":"V6483-M04","summary":"The user expected Codex CLI 0.144.5, while live execution reported 0.144.4; the phase recorded the observed version and did not update software inside the bounded run.","retained":True,"recovered":True},
    {"negative_id":"V6483-X1-N05","method_id":"V6483-M05","summary":"Seven initial core concepts collided semantically with the 570-title frozen corpus; collision searches rejected ZIP-central, Hadamard, generic DESI DR2, OpenID trust-chain, status-message, Hatano-Sasa, and transportability seeds before freeze.","retained":True,"recovered":True},
    {"negative_id":"V6483-X1-N06","method_id":"V6483-M06","summary":"A first ripgrep command passed Windows wildcard paths directly and failed with an invalid filename error; directory roots plus rg include globs recovered the bounded inspection.","retained":True,"recovered":True},
    {"negative_id":"V6483-X1-N07","method_id":"V6483-M07","summary":"PowerShell console decoding displayed UTF-8 Māori text as mojibake even though repository files decode correctly; builders retain explicit UTF-8 LF output and decoded validation instead of trusting console rendering.","retained":True,"recovered":True},
    {"negative_id":"V6483-X1-N08","method_id":"V6483-M08","summary":"A broad source-builder read exceeded its short tool envelope; targeted symbol searches and bounded line ranges recovered the exact required structure without mutation.","retained":True,"recovered":True},
    {"negative_id":"V6483-X1-N09","method_id":"V6483-M09","summary":"Two inline transformed-source diagnostics failed because nested PowerShell and Python quoting stripped or unterminated literals; a PowerShell literal here-string piped to Python recovered the read-only inspection.","retained":True,"recovered":True,"recurrences":2},
    {"negative_id":"V6483-X1-N10","method_id":"V6483-M10","summary":"The first v648-v3 x1 review and its inherited unit-test adapter retained predecessor assertions for nineteen sources and thirty cleanup rows; both failed closed, and phase-local assertion substitutions recovered the expanded portfolio without weakening any gate.","retained":True,"recovered":True},
]

METHOD_SPECS = [
    {
        "method_id":"V6483-M01","title":"Treat unavailable ChatGPT conversation messaging as an open route gap",
        "failure_signature":"No callable tool can address chatgpt-conversation links after bounded capability discovery.",
        "trigger_preconditions":["The user requests cross-product ChatGPT panel messaging but only Codex task tools are callable."],
        "candidate_workaround":"Use the user-supplied sibling responses as advisory input, record no message or timestamp, and offer a compact relay artifact only if human relaying is later needed.",
        "recurrence_guard":"Never translate visible conversation links into a claim that a message was sent or a live x1 advisory lane started.",
        "rollback":"No external message, task, or sibling mutation occurred.",
        "protected_gates":["route_truth","send_acknowledgment","raw_conversation_privacy","no_task_creation"],
        "retained_negative_ids":["V6483-X1-N01"],
        "failed_observed":"Direct ChatGPT conversation messaging was not callable in this Codex session.",
        "pass_observed":"Four supplied responses informed proposal review as advisory-only material while contact and polling remained explicitly absent.",
    },
    {
        "method_id":"V6483-M02","title":"Reconcile frozen candidate snapshots with later exact-final evidence by precedence",
        "failure_signature":"Commit-local candidate receipts are older than exact final Git and acknowledged route evidence in the same immutable source history.",
        "trigger_preconditions":["A source phase intentionally committed pre-proof candidate receipts and later verification exists outside those frozen snapshots."],
        "candidate_workaround":"Preserve the snapshots, verify exact ancestry and four-way equality live, cite the terminal baton and final head, and record the discrepancy as provenance rather than rewriting history.",
        "recurrence_guard":"Never let an older candidate snapshot erase later exact proof or let later proof falsify what the earlier snapshot truthfully recorded at its own time.",
        "rollback":"No source artifact was changed; only the successor receipt explains precedence.",
        "protected_gates":["source_provenance","lifecycle_truth","immutable_history","route_truth"],
        "retained_negative_ids":["V6483-X1-N02"],
        "failed_observed":"Frozen source JSON still said postcommit required and PREPARED_NOT_SENT.",
        "pass_observed":"Live Git and the acknowledged exact baton proved source final equality while the candidate snapshots remained preserved as historical states.",
    },
    {
        "method_id":"V6483-M03","title":"Supersede replay prospectively without manufacturing repeatability credit",
        "failure_signature":"A prior route requires replay but the newest explicit owner instruction prohibits replay runs.",
        "trigger_preconditions":["The newest user instruction is clear, in scope, and later than the inherited terminal protocol."],
        "candidate_workaround":"Record the supersession, run one canonical validation only, set replay executed false, repeatability credit zero, independent reproduction false, and keep all external validation gates open.",
        "recurrence_guard":"Never describe one canonical pass as replay, repeatability, independent reproduction, or external audit.",
        "rollback":"Restore the inherited replay requirement only if the user later explicitly reverses the no-replay instruction before terminal routing.",
        "protected_gates":["user_precedence","validation_truth","repeatability_credit","independent_reproduction"],
        "retained_negative_ids":["V6483-X1-N03"],
        "failed_observed":"The inherited route and newest user instruction could not both be executed literally.",
        "pass_observed":"The prospective protocol records no replay and no repeatability credit while preserving the canonical validation gate.",
    },
    {
        "method_id":"V6483-M04","title":"Record observed tool versions instead of installing an expected update",
        "failure_signature":"A requested or expected version differs from the executable version observed live.",
        "trigger_preconditions":["Software update would expand the bounded phase or require unrelated installation authority."],
        "candidate_workaround":"Record the exact observed version, mark the update unperformed, and defer installation to a separately reviewed maintenance action.",
        "recurrence_guard":"Never turn a user-stated release number into a verified local installation claim.",
        "rollback":"No software was installed, downgraded, or reconfigured.",
        "protected_gates":["version_truth","installation_authority","host_stability","reproducibility"],
        "retained_negative_ids":["V6483-X1-N04"],
        "failed_observed":"Live Codex CLI output was 0.144.4 rather than the expected 0.144.5.",
        "pass_observed":"The phase records 0.144.4 as observed and leaves update status open.",
    },
    {
        "method_id":"V6483-M05","title":"Reject semantically colliding core seeds before x1 freeze",
        "failure_signature":"Candidate concepts overlap already frozen proposal titles despite new wording.",
        "trigger_preconditions":["A 570-title inherited corpus contains adjacent standards, datasets, formalism, or causal designs."],
        "candidate_workaround":"Run exact and concept searches, inspect nearest titles, reject collisions, and substitute narrower genuinely distinct surfaces before generating x1.",
        "recurrence_guard":"A renamed standard, dataset subset, or narrative wrapper does not earn novelty unless its mission surface and tests are materially distinct.",
        "rollback":"Discard only uncommitted candidate seeds; preserve the collision evidence.",
        "protected_gates":["semantic_novelty","x1_freeze","proposal_count","no_completion_credit"],
        "retained_negative_ids":["V6483-X1-N05"],
        "failed_observed":"Seven first-pass concepts already existed or were too close to frozen proposals.",
        "pass_observed":"The final ten titles have no exact normalized collision and carry explicit novelty statements against adjacent prior work.",
    },
    {
        "method_id":"V6483-M06","title":"Use rg include globs instead of Windows wildcard path arguments",
        "failure_signature":"Ripgrep receives a literal wildcard path on Windows and returns an invalid filename error.",
        "trigger_preconditions":["Multiple versioned files need a bounded content search in PowerShell."],
        "candidate_workaround":"Pass directory roots to rg and select files with one or more -g include expressions.",
        "recurrence_guard":"Reserve shell wildcard expansion assumptions for shells that document them; use rg-native globs on Windows.",
        "rollback":"The failed command was read-only and changed nothing.",
        "protected_gates":["diagnostic_truth","bounded_search","no_repository_mutation"],
        "retained_negative_ids":["V6483-X1-N06"],
        "failed_observed":"The first tests-and-scripts search failed on wildcard paths.",
        "pass_observed":"Directory-root searches with rg -g filters returned the intended symbols and lifecycle literals.",
    },
    {
        "method_id":"V6483-M07","title":"Validate UTF-8 content from files rather than console glyph rendering",
        "failure_signature":"PowerShell console output renders valid UTF-8 Māori text as mojibake.",
        "trigger_preconditions":["Repository files are UTF-8 but console code-page rendering is inconsistent."],
        "candidate_workaround":"Write explicit UTF-8 without BOM and LF, parse files with UTF-8-aware validators, and inspect code points or decoded strings when glyph output is suspect.",
        "recurrence_guard":"Do not edit valid source text merely to match a broken console rendering.",
        "rollback":"No source text was downgraded or transliterated.",
        "protected_gates":["cultural_text_integrity","utf8","source_hashes","privacy"],
        "retained_negative_ids":["V6483-X1-N07"],
        "failed_observed":"Console output displayed Māori and hapū with corrupted glyph sequences.",
        "pass_observed":"Python and JSON UTF-8 parsing retain the intended Unicode strings and generated files use deterministic LF endings.",
    },
    {
        "method_id":"V6483-M08","title":"Decompose large source reads into symbol and bounded-range inspections",
        "failure_signature":"A broad source read exceeds a short tool envelope before returning complete content.",
        "trigger_preconditions":["A large family-current builder is required only for selected functions and hardcoded lifecycle literals."],
        "candidate_workaround":"Locate definitions with rg, then read bounded line ranges under longer per-command envelopes.",
        "recurrence_guard":"Avoid rereading an entire large generator when exact symbols and ranges are sufficient.",
        "rollback":"The timed-out read was read-only and changed no state.",
        "protected_gates":["builder_comprehension","lifecycle_literals","no_repository_mutation"],
        "retained_negative_ids":["V6483-X1-N08"],
        "failed_observed":"The first combined builder symbol and content read timed out.",
        "pass_observed":"Targeted symbol and range reads recovered portfolio floors, route fields, x1 separation, and output contracts.",
    },
    {
        "method_id":"V6483-M09","title":"Use a PowerShell literal here-string for multi-language inline diagnostics",
        "failure_signature":"Nested PowerShell and Python quote layers remove or unterminate string literals in a one-line diagnostic.",
        "trigger_preconditions":["A read-only Python diagnostic contains many quoted search keys inside a PowerShell command string."],
        "candidate_workaround":"Pipe a PowerShell single-quoted literal here-string to python stdin so neither shell nor Python literals require nested escaping.",
        "recurrence_guard":"Prefer a literal here-string for multi-line diagnostic code and keep it read-only.",
        "rollback":"Both failed diagnostics were read-only and produced no file or ref change.",
        "protected_gates":["diagnostic_truth","no_repository_mutation","bounded_inspection"],
        "retained_negative_ids":["V6483-X1-N09"],
        "failed_observed":"Two one-line diagnostics failed with PowerShell terminator and Python syntax errors.",
        "pass_observed":"The literal here-string diagnostic displayed source directory, branch, floors, counts, route, and no-replay fields.",
    },
    {
        "method_id":"V6483-M10","title":"Update phase-local reviewer cardinalities when an explicit portfolio floor changes",
        "failure_signature":"A structurally correct new phase fails predecessor source-count or cleanup-count assertions.",
        "trigger_preconditions":["The user explicitly expands a portfolio and the new definitions and builder enforce the larger cardinality."],
        "candidate_workaround":"Keep the failed receipt, inspect only the failing checks, update the phase-local adapter from nineteen to twenty sources and thirty to sixty cleanup rows, and rerun unchanged validation logic.",
        "recurrence_guard":"Never change a count assertion until the definitions, generated count, list cardinality, and user requirement agree exactly.",
        "rollback":"Overwrite only the uncommitted owner-scoped review receipt after the adapter is corrected.",
        "protected_gates":["portfolio_floor","source_ledger","x1_freeze","validation_truth"],
        "retained_negative_ids":["V6483-X1-N10"],
        "failed_observed":"The first x1 review passed 20 of 22 checks and failed source_count_19 and cleanup_floor_30.",
        "pass_observed":"The corrected phase-local review requires twenty sources and sixty cleanup rows while retaining every other x1 gate.",
    },
]
