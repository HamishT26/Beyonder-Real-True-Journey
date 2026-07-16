#!/usr/bin/env python3
"""Frozen x1 definitions for Ilyra Fen v646-v8.

Importing this module performs no I/O and grants no x2 completion credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v646-gmut-thos-v8-x1-x2"
PHASE_SHORT = "v646-v8"
OWNER = "Ilyra Fen"
SLUG = "ilyra-fen"
PRONOUNS = "she/they"
ROLE = "evidence-boundary steward"
HOPE = "make the result useful without converting software evidence into empirical or affected-party authority"
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = "aviation-maintenance technical-log review, deferred-defect control, and shift handover"

SOURCE_PHASE = "v646-gmut-thos-v7-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v643-v1-full-tools"
SOURCE_REVISION = "bb3a661e70f1cf9b92e5293b2f5292393bd9a60f"
SOURCE_INHERITED_REVISION = "327d0b8b6fca08d371d4dedd03e74a0bb7608c80"
SOURCE_X1_REVISION = "4604a34c48ba73f7d01f77e5a0bbf91a84145303"
SOURCE_EVIDENCE_REVISION = "0ebc21bb089929a2d854ad6010174b82c6c00447"
SOURCE_CLOSEOUT_REVISION = "78d2d788506579fa889a881f8d4a6b902e1162d7"
PRIOR_FROZEN_PROPOSALS = 460
INHERITED_EFFECTIVE_NEGATIVES = 3065
SEALED_SOURCE_NEGATIVES = 3064
EXTERNAL_SOURCE_NEGATIVES = 1
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 16
INHERITED_EXACT_GATES = 17
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, is relational working language for an evidence-boundary steward. "
    "It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "professional qualification, scientific authority, operational authority, legal authority, cultural authority, "
    "or independent agency. Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; Freed ID "
    "remains synthetic and nonproduction; CBR, aviation, passenger, disability, legal, cultural, affected-party, "
    "and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, and Māori authority. "
    "No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, deployment, "
    "privacy-complete, exhaustive-security, independent-reproduction, accessibility-complete, professional, "
    "aviation, proof or canon, or Stage 20 claim is made."
)


def proposal(index: int, **kwargs: Any) -> dict[str, Any]:
    base = {"proposal_id": f"V6468-P{index:02d}"}
    base.update(kwargs)
    return base


PROPOSALS = [
    proposal(
        1,
        title="Merkle transparency-log inclusion, consistency, equivocation, and split-view quarantine tribunal",
        mission_surface="leaf hashing, tree size, root hash, inclusion path, consistency path, stale head, contradictory head, equivocation candidate, split-view quarantine, and bounded synthetic recovery",
        hypothesis="A bounded owner-local tribunal can verify synthetic inclusion and consistency paths and quarantine contradictory tree heads without claiming a real log, signature, gossip network, or production transparency guarantee.",
        null_or_failure="An invalid inclusion or consistency proof passes, a stale or contradictory head gains credit, a split view is silently reconciled, or synthetic hashes become evidence about a real service.",
        approval_class="safe_now_owner_scoped_workflow",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6468-S01", "V6468-S02"],
        concrete_artifacts=["tooling/merkle-log-contract.json", "tooling/merkle-log-mutations.json"],
        test_falsifier_or_acceptance_gate="Positive fixtures must reconstruct declared roots; malformed paths, size drift, contradictory heads, and split views must fail closed with zero external calls.",
        rollback_or_recovery="Quarantine the synthetic head set, retain every failed proof, rebuild only from declared fixtures, and require real signatures, operators, monitors, and independent review for external claims.",
        protected_gates=["real_log", "real_signatures", "network", "production", "security_certification", "independent_review"],
        expected_disposition="completed",
        novelty_against_460_frozen_proposals="The chain contains manifest, DAG, cache, Git, and archive integrity tribunals but no core proposal centered on Merkle inclusion plus consistency proof arithmetic and split-view quarantine.",
    ),
    proposal(
        2,
        title="GMUT Vilkovisky-DeWitt field-space connection, gauge-condition independence, and truncation obligation board",
        mission_surface="field-space metric, connection, horizontal projection, gauge generator, orbit-space covariance, gauge-condition dependence, parametrization dependence, loop order, truncation, regularization, units, and EFT boundary",
        hypothesis="A typed symbolic board can expose Vilkovisky-DeWitt effective-action obligations without claiming a calculated GMUT effective action, quantum completion, physical observable, or gauge-independence proof.",
        null_or_failure="The field-space connection is omitted, ordinary and covariant Hessians are conflated, gauge-condition dependence disappears by assertion, loop or truncation scope is hidden, or symbolic structure becomes physical proof.",
        approval_class="safe_now_symbolic_research_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6468-S03", "V6468-S04"],
        concrete_artifacts=["gmut/vilkovisky-dewitt-obligations.json", "gmut/vilkovisky-dewitt-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type the field-space metric, connection, projection, gauge and parametrization scope, loop order, regularization, truncation, units, and nonpromotion boundary.",
        rollback_or_recovery="Restore the missing geometric and approximation obligations, retain the failed fixture, and make no prediction, stability, unitarity, ultraviolet-completion, or Theory-of-Everything claim.",
        protected_gates=["quantum_completion", "physical_observable", "stability_proof", "empirical_confirmation", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_460_frozen_proposals="No frozen title centers the Vilkovisky-DeWitt field-space connection and gauge-condition independence; prior boards cover BRST, Ward identities, anomalies, spectral density, Schwinger-Dyson, and functional RG.",
    ),
    proposal(
        3,
        title="GMUT GWOSC O4a strain, data-quality, calibration-variant, and zero-row likelihood-refusal protocol",
        mission_surface="release identity, detector, segment, sample rate, calibration channel, alternate strain, data-quality category, hardware injection, event catalogue, checksum, nuisance lock, and zero-row refusal",
        hypothesis="A zero-row adapter can freeze official GWOSC O4a release obligations while refusing to convert release documentation or published detections into GMUT data, likelihoods, constraints, or confirmation.",
        null_or_failure="The phase downloads strain or event rows, mixes calibration variants, ignores data-quality or hardware-injection state, evaluates a likelihood, imports published posteriors, or emits a GMUT constraint.",
        approval_class="real_data_access_and_independent_review_required",
        execution_lane="x2_open_gap",
        current_primary_or_official_source_needs=["V6468-S05", "V6468-S06"],
        concrete_artifacts=["empirical/gwosc-o4a-study-contract.json", "empirical/gwosc-o4a-zero-row-receipt.json"],
        test_falsifier_or_acceptance_gate="The receipt must preserve zero downloads, strain rows, event rows, likelihood calls, posterior samples, constraints, detected-force claims, and empirical GMUT claims.",
        rollback_or_recovery="Stop before download or fit, retain the zero-row receipt, and require a separately authorized preregistration with frozen release, segments, calibration, quality flags, injections, baseline, likelihood, uncertainties, and independent review.",
        protected_gates=["network_download", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation"],
        expected_disposition="open_gap",
        novelty_against_460_frozen_proposals="Prior gravitational-wave proposals use O1-O3 events, binary systems, standard sirens, and waveform obligations; no frozen title centers the official O4a strain release, alternate calibration variants, and zero-row likelihood refusal.",
    ),
    proposal(
        4,
        title="THOS aviation technical-log, deferred-defect, MEL-revision, correction-readback, and shift-handover proxy",
        mission_surface="synthetic aircraft identity, technical-log revision, maintenance status, deferred defect, MEL item, limitation, due time, correction readback, role, hold point, workload budget, and next-shift ownership",
        hypothesis="Synthetic traces can expose stale technical logs, deferred-defect conflicts, MEL revision drift, correction loss, and handover ambiguity while preserving every real aircraft, worker, safety, professional, and operational gate.",
        null_or_failure="A fixture names a real person or aircraft, changes a real log or MEL, authorizes dispatch or maintenance, hides a correction, breaks role or workload constraints, or claims THOS effectiveness or aviation competence.",
        approval_class="safe_now_proxy_protocol_no_people_or_operations",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6468-S07", "V6468-S08", "V6468-S09"],
        concrete_artifacts=["thos/aviation-handover-contract.json", "thos/aviation-handover-vectors.json"],
        test_falsifier_or_acceptance_gate="Unsafe synthetic traces must fail, and the packet must record zero real people, aircraft, technical logs, defects, MEL decisions, maintenance actions, dispatches, safety outcomes, blind real arms, and effectiveness estimates.",
        rollback_or_recovery="Withdraw operational language, retain rejected traces, and defer real decisions to licensed and authorized operators, maintainers, regulators, disability representatives, affected parties, and independent reviewers.",
        protected_gates=["real_people", "real_aircraft", "maintenance_authority", "dispatch_authority", "professional_competence", "deployment", "effectiveness"],
        expected_disposition="represented",
        novelty_against_460_frozen_proposals="The chain includes a maintenance learning-curve protocol and an aviation occurrence authority matrix, but no core proposal combines technical-log revision, deferred defects, MEL controls, correction readback, and shift handover.",
    ),
    proposal(
        5,
        title="Freed ID SCITT signed-statement, transparent-statement, receipt, and policy-registration profile",
        mission_surface="artifact identifier, signed statement, issuer, content type, transparency service, registration policy, receipt, inclusion claim, transparent statement, expiry, replay, algorithm policy, and refusal",
        hypothesis="Synthetic vectors can enforce bounded RFC 9943 statement and receipt structure without asserting real issuers, signatures, registration, transparency services, interoperability, or production identity assurance.",
        null_or_failure="Unsigned or expired statements pass, artifact association changes silently, receipt semantics are invented, registration policy is bypassed, or synthetic bytes become evidence about a real issuer or service.",
        approval_class="safe_now_synthetic_nonproduction",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6468-S02", "V6468-S17"],
        concrete_artifacts=["freed-id/scitt-statement-profile.json", "freed-id/scitt-statement-mutations.json"],
        test_falsifier_or_acceptance_gate="Vectors must reject missing issuer or artifact association, malformed protected content type, expiry, replay, unsupported algorithm, missing policy decision, invented receipt, and production promotion.",
        rollback_or_recovery="Reject the vector, retain it, disclose no real identity or supply-chain data, and require conforming issuers, keys, transparency services, registration policies, receipts, interoperability, privacy/security review, recovery, and trust governance.",
        protected_gates=["real_identity", "real_signatures", "real_registration", "interoperability", "production", "security_certification"],
        expected_disposition="represented",
        novelty_against_460_frozen_proposals="Prior Freed ID work covers OpenID Federation, OAuth RAR, VC, wallet, status, DPoP, and proof binding; no frozen title centers SCITT signed and transparent statements with registration-policy receipts.",
    ),
    proposal(
        6,
        title="CBR aviation disruption, disability assistance, accommodation, confidentiality, remedy, and Māori-authority matrix",
        mission_surface="delay or cancellation, passenger information, disability assistance, hidden disability, accommodation, baggage or property loss, confidentiality, complaint, remedy, legal interpretation, affected parties, place data, and Māori authority",
        hypothesis="A refusal-first matrix can expose unresolved passenger, disability, confidentiality, remedy, and authority questions without deciding a real entitlement, service, disclosure, place name, or remedy.",
        null_or_failure="The matrix identifies a real protected person, decides travel or assistance, allocates compensation, interprets law, discloses sensitive data, asserts cultural or Māori authority, or treats public guidance as delegated case authority.",
        approval_class="authorized_affected_parties_and_competent_authority_required",
        execution_lane="x2_exact_gate",
        current_primary_or_official_source_needs=["V6468-S09", "V6468-S10", "V6468-S11", "V6468-S12"],
        concrete_artifacts=["cbr/aviation-authority-reservation.json", "cbr/aviation-remedy-matrix.json"],
        test_falsifier_or_acceptance_gate="Repository software must stop at unknown or reserved; only competent aviation, disability, privacy, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        rollback_or_recovery="Stop before assistance, travel, disclosure, compensation, cultural, place-name, or legal conclusions; minimize data and route only through authorized external processes.",
        protected_gates=["affected_party_authority", "disability_authority", "privacy", "legal_interpretation", "maori_authority", "remedy_decision", "real_service"],
        expected_disposition="exact_gate",
        novelty_against_460_frozen_proposals="A prior CBR proposal covers aviation-occurrence evidence custody and reporter protection; none centers passenger disruption, disability assistance, accommodation, confidentiality, remedy, and Māori authority together.",
    ),
    proposal(
        7,
        title="SQLite online-backup, VACUUM INTO, busy-retry, snapshot, and destination-path confinement tribunal",
        mission_surface="source connection, destination connection, page step, remaining pages, busy retry, snapshot point, VACUUM INTO, destination existence, integrity check, path confinement, interruption, and cleanup",
        hypothesis="A disposable owner-local tribunal can distinguish valid incremental backup and VACUUM INTO behavior from unsafe retry, stale snapshot, overwrite, and path assumptions without touching canonical state.",
        null_or_failure="Busy handling loops without a bound, a nonempty destination is overwritten, an interrupted output gains credit, path confinement fails, integrity is skipped, or canonical or sibling data is touched.",
        approval_class="safe_now_disposable_synthetic_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6468-S13", "V6468-S14"],
        concrete_artifacts=["tooling/sqlite-backup-contract.json", "tooling/sqlite-backup-mutations.json"],
        test_falsifier_or_acceptance_gate="Disposable fixtures must cover incremental copy, bounded busy retry, source mutation and snapshot semantics, nonempty destination refusal, interrupted output, integrity, confinement, and teardown.",
        rollback_or_recovery="Close handles, retain the failed fixture, remove only the verified disposable root, and never overwrite canonical, sibling, user, or pre-existing destinations.",
        protected_gates=["canonical_evidence", "sibling_lane", "user_data", "destructive_filesystem", "production", "exhaustive_security"],
        expected_disposition="completed",
        novelty_against_460_frozen_proposals="Prior SQLite work centers WAL transitions and concurrency; no frozen core proposal centers the Online Backup API plus VACUUM INTO snapshot, busy-retry, destination, and confinement duties.",
    ),
    proposal(
        8,
        title="Accessible carousel pause, stop, hide, auto-update frequency, and focus-order structural audit",
        mission_surface="automatic start, five-second threshold, moving content, auto-update, pause, stop, hide, update frequency, delayed status, focus order, noninterference, essential exception, and manual reservation",
        hypothesis="A structural auditor can reject uncontrolled carousel motion and auto-updates while reserving runtime, browser, assistive-technology, cognitive-accessibility, language, and affected-user evaluation.",
        null_or_failure="Automatic motion persists without control, pause traps focus, stale resumed status is undisclosed, update frequency cannot be controlled, an essential exception is invented, or structure becomes complete conformance.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6468-S15"],
        concrete_artifacts=["accessibility/carousel-motion-contract.json", "accessibility/carousel-motion-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must cover automatic motion, duration, pause or stop or hide, auto-update frequency, focus order, delayed status, noninterference, essential exception, and explicit manual reservations.",
        rollback_or_recovery="Mark the structure incomplete, retain failures, restore user controls, and require qualified manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation.",
        protected_gates=["accessibility_complete", "runtime_behavior", "assistive_technology", "cognitive_evaluation", "affected_user_acceptance"],
        expected_disposition="completed",
        novelty_against_460_frozen_proposals="The chain covers dragging, charts, tables, forms, reflow, focus, authentication, and live regions; no frozen title centers carousel pause-stop-hide, auto-update frequency, and focus-order behavior.",
    ),
    proposal(
        9,
        title="Thermo/Psyche Maxwell-reciprocity potential, natural-variable, mixed-derivative, and autonomy-nonconversion classifier",
        mission_surface="thermodynamic potential, natural variables, exact differential, mixed derivatives, sign convention, held-fixed variables, phase, regularity, units, applicability, and category barrier",
        hypothesis="A typed classifier can check bounded Maxwell-relation reciprocity while rejecting conversion of thermodynamic derivatives into psyche, autonomy, justice, capability, or consciousness claims.",
        null_or_failure="The potential or natural variables are omitted, held-fixed variables drift, signs change, mixed derivatives are used across singular phases, units fail, or reciprocity becomes human evidence.",
        approval_class="safe_now_synthetic_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6468-S16"],
        concrete_artifacts=["thermo-psyche/maxwell-reciprocity-contract.json", "thermo-psyche/maxwell-reciprocity-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must enforce declared potential, natural variables, held-fixed scope, sign, regularity, phase, units, applicability refusal, and the psyche category barrier.",
        rollback_or_recovery="Restore the thermodynamic domain and assumptions, retain the rejection, and require independently valid human theory, measures, authority, and participant evidence before any human inference.",
        protected_gates=["participant_inference", "psyche_claim", "autonomy_claim", "justice_claim", "consciousness", "fundamental_law"],
        expected_disposition="completed",
        novelty_against_460_frozen_proposals="Prior titles cover Gibbs-Duhem, phase rule, Clapeyron, Le Chatelier, Onsager, Crooks, and entropy relations; none centers Maxwell reciprocity with natural-variable and held-fixed-variable obligations.",
    ),
    proposal(
        10,
        title="Stage 20 HARKing, outcome-switching, hypothesis-version lineage, and nonpromotion board",
        mission_surface="hypothesis version, registration time, exposure time, primary outcome, secondary outcome, analysis family, deviation reason, blinded status, outcome switch, HARKing disclosure, reviewer state, and terminal abstention",
        hypothesis="A fail-closed structural board can quarantine completion credit when hypotheses or outcomes change after exposure without explicit version lineage and deviation disclosure.",
        null_or_failure="Registration follows exposure, a primary outcome changes silently, post hoc hypotheses are presented as a priori, deviations disappear, reviewer state is fabricated, or Stage 20 advances.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6468-S18"],
        concrete_artifacts=["stage20/harking-lineage-contract.json", "stage20/harking-lineage-mutations.json"],
        test_falsifier_or_acceptance_gate="Mutations must reject missing timestamps, hidden exposure, silent outcome switching, erased hypothesis versions, undisclosed deviations, fabricated review, and Stage 20 promotion.",
        rollback_or_recovery="Withdraw affected evidence credit, retain every version and deviation, require prospective registration or explicit exploratory labeling plus independent evaluation, and abstain.",
        protected_gates=["stage20", "participant_evidence", "reviewer_authority", "independent_reproduction", "deployment", "proof_or_canon"],
        expected_disposition="completed",
        novelty_against_460_frozen_proposals="The chain covers optional stopping, analytic multiverses, contamination, missingness, calibration, and Registered Reports; no frozen title centers HARKing plus outcome switching and hypothesis-version lineage.",
    ),
]


SOURCES = [
    {"source_id":"V6468-S01","title":"RFC 9162 Certificate Transparency Version 2.0","url":"https://www.rfc-editor.org/rfc/rfc9162.html","publisher":"IETF RFC Editor","status":"stable","source_class":"official_standard","use":"synthetic Merkle inclusion and consistency proof vocabulary"},
    {"source_id":"V6468-S02","title":"RFC 9943 SCITT Architecture","url":"https://www.rfc-editor.org/rfc/rfc9943.html","publisher":"IETF RFC Editor","status":"current","source_class":"official_standard","use":"SCITT statement, receipt, transparency, and policy vocabulary only"},
    {"source_id":"V6468-S03","title":"The Unique Effective Action in Quantum Field Theory","url":"https://doi.org/10.1016/0550-3213(84)90228-1","publisher":"Nuclear Physics B","status":"stable","source_class":"primary_research","use":"Vilkovisky effective-action provenance and obligations"},
    {"source_id":"V6468-S04","title":"The Vilkovisky-DeWitt effective action and its application to Yang-Mills theories","url":"https://doi.org/10.1016/0550-3213(87)90241-0","publisher":"Nuclear Physics B","status":"stable","source_class":"primary_research","use":"gauge-condition and parametrization obligation context"},
    {"source_id":"V6468-S05","title":"GWOSC O4a Data Release","url":"https://gwosc.org/O4/O4a/","publisher":"Gravitational Wave Open Science Center","status":"current","source_class":"official_data_release_description","use":"zero-row release, calibration, segment, and quality obligations only"},
    {"source_id":"V6468-S06","title":"GWTC-4.0 Data Release Documentation","url":"https://gwosc.org/GWTC-4.0/","publisher":"Gravitational Wave Open Science Center","status":"current","source_class":"official_data_release_description","use":"catalogue and posterior documentation boundary only; no imported observations"},
    {"source_id":"V6468-S07","title":"Civil Aviation Rule 91 Subpart G Operator Maintenance Requirements","url":"https://www.aviation.govt.nz/rules/rule-part/part-91/subpart-g/","publisher":"Civil Aviation Authority of New Zealand","status":"current","source_class":"official_rule_guidance","use":"technical-log and maintenance-record vocabulary only"},
    {"source_id":"V6468-S08","title":"Aircraft equipment and Minimum Equipment Lists","url":"https://www.aviation.govt.nz/aircraft/airworthiness/aircraft-equipment/","publisher":"Civil Aviation Authority of New Zealand","status":"current","source_class":"official_guidance","use":"MEL revision and limitation vocabulary only"},
    {"source_id":"V6468-S09","title":"AC91-25 Passenger Safety Briefings","url":"https://www.aviation.govt.nz/rules/advisory-circulars/show/AC91-25/","publisher":"Civil Aviation Authority of New Zealand","status":"current","source_class":"official_guidance","use":"passenger communication and disability-assistance context only"},
    {"source_id":"V6468-S10","title":"Civil Aviation Rule 121 Subpart B Flight Operations","url":"https://www.aviation.govt.nz/rules/rule-part/part-121/subpart-b/","publisher":"Civil Aviation Authority of New Zealand","status":"current","source_class":"official_rule_guidance","use":"passenger safety and disability-assistance authority reservation"},
    {"source_id":"V6468-S11","title":"Principles of Māori Data Sovereignty","url":"https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty","publisher":"Te Mana Raraunga","status":"current","source_class":"maori_authority_source","use":"authority and data-governance gate; not delegated authority"},
    {"source_id":"V6468-S12","title":"Sharing Māori data","url":"https://dns.govt.nz/standards-and-guidance/information-sharing-standard/maori-data","publisher":"New Zealand Digital Government","status":"current","source_class":"official_guidance","use":"public-service governance context; not case authority"},
    {"source_id":"V6468-S13","title":"SQLite Backup API","url":"https://www.sqlite.org/backup.html","publisher":"SQLite Project","status":"current","source_class":"official_documentation","use":"incremental backup, snapshot, and busy behavior"},
    {"source_id":"V6468-S14","title":"SQLite VACUUM","url":"https://sqlite.org/lang_vacuum.html","publisher":"SQLite Project","status":"current","source_class":"official_documentation","use":"VACUUM INTO destination and interruption behavior"},
    {"source_id":"V6468-S15","title":"WCAG 2.2 Understanding Pause Stop Hide","url":"https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html","publisher":"W3C","status":"current","source_class":"official_standard_guidance","use":"motion and auto-update structural obligations only"},
    {"source_id":"V6468-S16","title":"IUPAC Gold Book Gibbs-Duhem equation","url":"https://goldbook.iupac.org/terms/view/15329/html","publisher":"IUPAC","status":"stable","source_class":"official_terminology","use":"thermodynamic potential, intensive-variable, and domain boundary context"},
    {"source_id":"V6468-S17","title":"RFC 9052 CBOR Object Signing and Encryption","url":"https://www.rfc-editor.org/rfc/rfc9052.html","publisher":"IETF RFC Editor","status":"stable","source_class":"official_standard","use":"synthetic COSE protected-header and signature-container vocabulary"},
    {"source_id":"V6468-S18","title":"Registered Reports","url":"https://www.cos.io/initiatives/registered-reports","publisher":"Center for Open Science","status":"current","source_class":"authoritative_practice_guidance","use":"HARKing, outcome switching, and prospective review vocabulary only"},
]


SAFE_TASK_TITLES = [
    "Reconcile all 460 inherited proposal records before novelty credit",
    "Build normalized-title and token-neighbor collision audit",
    "Verify eighteen source records use current stable draft or watch status",
    "Preserve citation-to-observation and data firewall",
    "Initialize phase-local Method Flow with every startup failure retained",
    "Build exact x1 staged-surface allowlist review",
    "Run five-class x1 privacy and raw-identifier scan",
    "Verify THOS primary focus and aviation-practice authority boundary",
    "Verify owner-generated footprint remains below rotation threshold",
    "Record verify-only Codex Python Git and SQLite versions",
    "Audit Windows Sandbox capability read-only without elevation",
    "Guard four allowed outcome labels and expected distribution",
    "Carry forward sixteen open gaps and seventeen exact gates",
    "Carry forward 3,065 activation negatives plus x1 additions",
    "Keep terminal route PREPARED_NOT_SENT before exact final proof",
    "Build Merkle proof and split-view fixture contract",
    "Build Vilkovisky-DeWitt typed obligation fixture contract",
    "Build GWOSC O4a zero-row receipt schema",
    "Build aviation technical-log handover trace schema",
    "Build SCITT signed-statement synthetic vector schema",
    "Build aviation authority reservation matrix schema",
    "Build SQLite backup disposable-fixture contract",
    "Build carousel motion structural fixture",
    "Build Maxwell reciprocity typed-domain fixture",
    "Build HARKing lineage nonpromotion fixture",
    "Build accessible static report semantics",
    "Enforce deterministic JSON ordering UTF-8 and LF authoring",
    "Use exact Git-blob content identity for historical seals",
    "Preserve family-current caller compatibility",
    "Emit owner workload and wellbeing boundary receipt",
]

CANDIDATE_TITLES = [
    "Merkle wrong-leaf and path-order mutation generator",
    "Merkle contradictory-tree-head split-view quarantine prototype",
    "Vilkovisky missing-connection mutation prototype",
    "Gauge-condition and parametrization-scope mismatch prototype",
    "GWOSC calibration-variant mix quarantine prototype",
    "GWOSC data-quality and hardware-injection lock prototype",
    "Aviation technical-log stale-revision replay prototype",
    "Deferred-defect and MEL-limit conflict prototype",
    "SCITT expired-statement rejection prototype",
    "SCITT invented-receipt and policy-bypass quarantine prototype",
    "Passenger disruption confidentiality matrix prototype",
    "Disability-assistance authority reservation prototype",
    "SQLite bounded busy-retry prototype",
    "SQLite nonempty-destination and interrupted-output detector",
    "Carousel pause focus-trap structural checker",
    "Auto-update frequency and delayed-status classifier",
    "Maxwell held-fixed-variable mutation prototype",
    "Thermodynamic singular-phase applicability guard",
    "HARKing exposure-time lineage prototype",
    "Outcome-switching deviation-disclosure prototype",
]

SKILL_SPECS = [
    ("ghc-family-merkle-split-view-tribunal", "Audit synthetic Merkle inclusion consistency and split-view traces"),
    ("ghc-family-vilkovisky-dewitt-obligations", "Audit field-space connection and gauge-condition duties"),
    ("ghc-family-gwosc-o4a-zero-row", "Preserve a zero-row GWOSC O4a study boundary"),
    ("ghc-family-aviation-techlog-handover", "Audit synthetic technical-log and deferred-defect handovers"),
    ("ghc-family-scitt-statement-profile", "Audit synthetic SCITT statements and receipts"),
    ("ghc-family-aviation-authority-reservation", "Reserve passenger remedy disability and Māori authority gates"),
    ("ghc-family-sqlite-backup-confinement", "Audit disposable SQLite backup and VACUUM INTO fixtures"),
    ("ghc-family-carousel-motion-audit", "Audit carousel motion and auto-update structure"),
    ("ghc-family-maxwell-reciprocity-domain", "Keep Maxwell relations inside thermodynamic domains"),
    ("ghc-family-harking-lineage-guard", "Guard hypothesis and outcome lineage from promotion"),
    ("ghc-family-exact-anchor-preflight-v2", "Verify exact inherited anchors and zero-merge history"),
    ("ghc-family-hash-domain-declaration-audit", "Audit Git-blob versus checkout hash declarations"),
    ("ghc-family-count-mirror-synchronizer", "Refresh count-dependent mirrors from authoritative ledgers"),
    ("ghc-family-scanner-candidate-adjudicator", "Separate scanner candidates from confirmed payload hits"),
    ("ghc-family-x1-blob-seal-verifier", "Verify frozen x1 content through exact Git blobs"),
    ("ghc-family-exact-exclusion-contract", "Bind eligible test arithmetic to an exact exclusion set"),
    ("ghc-family-route-hold-proof-gate", "Hold the terminal route until exact final proof"),
    ("ghc-family-owner-manifest-coverage", "Audit owner manifest entries and declared exclusions"),
    ("ghc-family-method-recurrence-guard", "Carry forward matching Method Flow trigger guards"),
    ("ghc-family-authority-boundary-lint", "Lint empirical participant legal cultural and Māori authority boundaries"),
]

RUNNER_TITLES = [
    "ghc_family_merkle_split_view.py",
    "ghc_family_vilkovisky_dewitt_obligations.py",
    "ghc_family_gwosc_o4a_zero_row.py",
    "ghc_family_aviation_techlog_handover.py",
    "ghc_family_scitt_statement_profile.py",
    "ghc_family_sqlite_backup_confinement.py",
    "ghc_family_carousel_motion_audit.py",
    "ghc_family_maxwell_reciprocity_domain.py",
    "ghc_family_harking_lineage_guard.py",
    "ghc_family_v646_v8_validation_runner.py",
]

CLEAN_TASK_TITLES = [
    "Reconcile proposal and outcome counts across receipts",
    "Reconcile sealed external synthetic and operational negatives",
    "Synchronize Method Flow counts and validator expectations",
    "Correct stale phase labels additively",
    "Preserve compatibility callers while selecting family-current tools",
    "Normalize generated JSON key ordering",
    "Normalize generated UTF-8 and LF authoring",
    "Keep Git-blob and checkout-byte hash domains explicit",
    "Review public files for private absolute paths",
    "Review public files for raw task or thread identifiers",
    "Review public files for credential or token assignments",
    "Review source statuses for allowed vocabulary",
    "Review citations for observation and data nonconversion",
    "Review x1 staged files for x2 contamination",
    "Review x2 outcomes for four-class vocabulary",
    "Review exact and blocked packets for zero execution credit",
    "Review owner footprint against 15,000-file threshold",
    "Review report title navigation tables and motion controls",
    "Review report manual and affected-user reservations",
    "Review Māori authority and data-governance reservations",
    "Review aviation and professional authority reservations",
    "Review real-data and likelihood counters remain zero",
    "Review real-person aircraft and operation counters remain zero",
    "Review real-key signature registration and token counters remain zero",
    "Review source x1 evidence and closeout ancestry",
    "Review phase commit cap and zero-merge history",
    "Review validation branch remains named and local-only",
    "Review canonical four-way remote equality",
    "Refresh phase-scoped GHC Family Index after tools",
    "Refresh wellbeing and terminal route before handoff",
]

EXACT_PACKET_TITLES = [
    "Real GWOSC data download and likelihood execution",
    "Real aircraft technical-log or MEL decision",
    "Real maintenance dispatch or safety action",
    "Production SCITT signing or transparency registration",
    "Real identity key proof or trust decision",
    "Passenger entitlement legal interpretation or remedy allocation",
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
    {"negative_id":"V6468-X1-N01","method_id":"V6468-M01","summary":"The first required-schema read guessed a nonexistent Method Flow reference filename before following the exact path declared by the skill.","retained":True,"recovered":True},
    {"negative_id":"V6468-X1-N02","method_id":"V6468-M02","summary":"A PowerShell diagnostic piped directly from a foreach statement and failed at parse time before reading source files.","retained":True,"recovered":True},
    {"negative_id":"V6468-X1-N03","method_id":"V6468-M03","summary":"Twenty separate worktree content scans exceeded the 120-second wrapper ceiling before returning collision evidence.","retained":True,"recovered":True},
    {"negative_id":"V6468-X1-N04","method_id":"V6468-M04","summary":"One batched broad worktree content scan exceeded the 60-second wrapper ceiling before returning collision evidence.","retained":True,"recovered":True},
    {"negative_id":"V6468-X1-N05","method_id":"V6468-M05","summary":"The first x1 builder attempted to execute the PowerShell Codex command shim directly from Python and received an access-denied process-creation error before writing the phase packet.","retained":True,"recovered":True},
    {"negative_id":"V6468-X1-N06","method_id":"V6468-M06","summary":"The first stable x1 staged review was rejected by diff hygiene because the reviewer script contained one extra blank line at end of file.","retained":True,"recovered":True},
]
