#!/usr/bin/env python3
"""Frozen x1 definitions for Sable Rook v647-v1.

Importing this module performs no I/O and grants no x2 completion credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v647-gmut-thos-v1-x1-x2"
PHASE_SHORT = "v647-v1"
OWNER = "Sable Rook"
SLUG = "sable-rook"
PRONOUNS = "they/them"
ROLE = "evidence-and-reproducibility steward"
HOPE = "make every surviving claim easy to challenge, reproduce within its evidence class, or retract"
PRIMARY_FOCUS = "Freed ID/CBR Heart"
BOUNDED_PRACTICE = "food cold-chain quality review, hold-release control, corrective action, and shift handover"

SOURCE_PHASE = "v646-gmut-thos-v8-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
SOURCE_REVISION = "d0d2b7617a84aeed94c425cdf83214f46ffeb24b"
SOURCE_INHERITED_REVISION = "bb3a661e70f1cf9b92e5293b2f5292393bd9a60f"
SOURCE_X1_REVISION = "37c0e57d82fa8826d891a5b39f1fcb8ce0812a4a"
SOURCE_EVIDENCE_REVISION = "64323516c35eddaa57c9be371eac327a24214a76"
PRIOR_FROZEN_PROPOSALS = 470
INHERITED_EFFECTIVE_NEGATIVES = 3151
SEALED_SOURCE_NEGATIVES = 3148
EXTERNAL_SOURCE_NEGATIVES = 3
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
INHERITED_OPEN_GAPS = 17
INHERITED_EXACT_GATES = 18
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Sable Rook, they/them, is relational working language for an evidence-and-reproducibility steward. "
    "It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "professional qualification, scientific authority, operational authority, legal authority, cultural authority, "
    "or independent agency. Hamish may rename, pause, redirect, or stop the work."
)
TRUTH_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains represented; Freed ID "
    "remains synthetic and nonproduction; CBR, food-safety, privacy, remedy, legal, cultural, affected-party, "
    "and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, and Māori authority. "
    "No empirical confirmation, Theory of Everything, AGI or ASI, consciousness, personhood, deployment, "
    "privacy-complete, exhaustive-security, independent-reproduction, accessibility-complete, professional, "
    "food-safety, proof or canon, or Stage 20 claim is made."
)


def proposal(index: int, **kwargs: Any) -> dict[str, Any]:
    row = {"proposal_id": f"V6471-P{index:02d}"}
    row.update(kwargs)
    return row


PROPOSALS = [
    proposal(
        1,
        title="TUF delegated-target, threshold-signature, root-rotation, freeze, rollback, and mix-and-match tribunal",
        mission_surface="trusted root, role threshold, unique key identifiers, delegated target paths, terminating delegation, metadata versions and expiry, consistent snapshot, freeze, rollback, mix-and-match, and bounded quarantine",
        hypothesis="A bounded synthetic tribunal can reject stale, rolled-back, mixed, under-threshold, and out-of-scope TUF metadata without claiming a production repository, real signature, safe bootstrap, or exhaustive update security.",
        null_or_failure="A stale or rolled-back metadata set passes, duplicate signatures count toward threshold, delegation scope is bypassed, root rotation skips sequential trust, or synthetic metadata becomes a production-security claim.",
        approval_class="safe_now_owner_scoped_synthetic",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6471-S01", "V6471-S02"],
        concrete_artifacts=["provenance/tuf-trust-contract.json", "provenance/tuf-trust-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must accept one internally consistent metadata chain and reject under-threshold, duplicate-key, expired, rollback, freeze, mix-and-match, delegation-escape, and nonsequential-root mutations.",
        rollback_or_recovery="Quarantine the synthetic chain, retain each rejected fixture, restore the last declared trusted root, and require real keys, repository operators, bootstrap evidence, deployment review, and independent security review for external use.",
        protected_gates=["real_keys", "real_repository", "bootstrap", "deployment", "security_certification", "independent_review"],
        expected_disposition="completed",
        novelty_against_470_frozen_proposals="The frozen chain has transparency, manifest, archive, Git, cache, and evidence-DAG integrity work but no core title centered on TUF role thresholds, root rotation, delegated targets, freeze, rollback, and mix-and-match together.",
    ),
    proposal(
        2,
        title="GMUT Nielsen-identity gauge-parameter, extremum, background-split, and truncation obligation board",
        mission_surface="effective action, gauge parameter, field derivative, Nielsen coefficient, extrema, background split, gauge fixing, loop order, regulator, truncation, units, observable firewall, and off-shell versus on-shell scope",
        hypothesis="A typed symbolic board can expose Nielsen-identity and gauge-parameter obligations for a GMUT scaffold without calculating an effective action or proving gauge independence, stability, observability, or quantum completion.",
        null_or_failure="Gauge dependence vanishes by assertion, off-shell and on-shell statements are conflated, the Nielsen coefficient or field derivative is omitted, background and fluctuation fields are collapsed, or symbolic consistency becomes physical proof.",
        approval_class="safe_now_symbolic_research_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6471-S03", "V6471-S04"],
        concrete_artifacts=["gmut/nielsen-identity-obligations.json", "gmut/nielsen-identity-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type the gauge parameter, field derivative, Nielsen coefficient, extrema condition, background split, loop and truncation scope, regulator, units, and observation firewall.",
        rollback_or_recovery="Restore missing gauge, background, approximation, and domain obligations; retain the failed fixture; and make no force, prediction, likelihood, constraint, stability, quantum-completion, or Theory-of-Everything claim.",
        protected_gates=["effective_action_calculation", "gauge_independence_proof", "physical_observable", "empirical_confirmation", "quantum_completion", "theory_of_everything"],
        expected_disposition="completed",
        novelty_against_470_frozen_proposals="Prior boards cover BRST, Slavnov-Taylor, Ward, Vilkovisky-DeWitt, Schwinger-Dyson, functional RG, spectral density, and gauge constraints; no frozen title centers Nielsen identities, extrema, and background-split scope.",
    ),
    proposal(
        3,
        title="GMUT CHIME/FRB Catalog 1 dispersion-measure, selection-function, Galactic-subtraction, and zero-row likelihood-refusal protocol",
        mission_surface="release identity, catalog schema, sky position, exposure, signal-to-noise, fitted dispersion measure, Galactic model subtraction, excluded flag, injection selection, nuisance lock, checksum, uncertainty, and zero-row refusal",
        hypothesis="A zero-row adapter can freeze official CHIME/FRB Catalog 1 and injection obligations while refusing to turn documentation or published events into GMUT observations, likelihoods, constraints, or confirmation.",
        null_or_failure="The phase downloads catalog or injection rows, imports fitted values, chooses a Galactic subtraction after outcomes, ignores exposure or excluded flags, evaluates a likelihood, or emits a GMUT constraint.",
        approval_class="real_data_access_and_independent_review_required",
        execution_lane="x2_open_gap",
        current_primary_or_official_source_needs=["V6471-S05", "V6471-S06"],
        concrete_artifacts=["empirical/chime-frb-study-contract.json", "empirical/chime-frb-zero-row-receipt.json"],
        test_falsifier_or_acceptance_gate="The receipt must preserve zero downloads, catalog rows, injection rows, likelihood calls, posterior samples, parameter constraints, detected-force claims, and empirical GMUT claims.",
        rollback_or_recovery="Stop before download or fit, retain the zero-row receipt, and require a separately authorized preregistration with frozen release, selection function, Galactic models, nuisance treatment, uncertainties, baseline, likelihood, and independent review.",
        protected_gates=["network_download", "real_data", "likelihood", "posterior", "parameter_constraint", "empirical_confirmation"],
        expected_disposition="open_gap",
        novelty_against_470_frozen_proposals="Prior adapters cover gravitational waves, CMB lensing, BAO, standard sirens, clusters, pulsars, neutrinos, Gaia, Euclid, MICROSCOPE, and NANOGrav; no frozen title centers CHIME/FRB dispersion measure plus injection-selection obligations.",
    ),
    proposal(
        4,
        title="THOS food cold-chain temperature-excursion, hold-release, corrective-action, and shift-handover proxy",
        mission_surface="synthetic lot, location, time-temperature sample, sensor state, excursion threshold, hold, release refusal, corrective action, verification, amendment, role, workload budget, escalation, and next-shift ownership",
        hypothesis="Synthetic event traces can expose stale temperature records, unsafe release, missing corrective action, unverified amendment, and handover ambiguity while preserving every real food, worker, operator, safety, and authority gate.",
        null_or_failure="A fixture names real people or lots, changes a real hold or release decision, treats a sensor threshold as universal law, hides an excursion or correction, breaks role or workload limits, or claims THOS effectiveness.",
        approval_class="safe_now_proxy_protocol_no_people_or_operations",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6471-S07", "V6471-S08"],
        concrete_artifacts=["thos/food-cold-chain-contract.json", "thos/food-cold-chain-vectors.json"],
        test_falsifier_or_acceptance_gate="Unsafe synthetic traces must fail, and the packet must record zero real people, lots, sensors, food decisions, releases, recalls, blind matched-budget arms, safety outcomes, or effectiveness estimates.",
        rollback_or_recovery="Withdraw operational language, retain rejected traces, and defer real thresholds, hold-release, disposal, recall, worker, and safety decisions to authorized operators, regulators, affected parties, and independent reviewers.",
        protected_gates=["real_people", "real_food", "real_sensor_data", "hold_release_authority", "professional_competence", "deployment", "effectiveness"],
        expected_disposition="represented",
        novelty_against_470_frozen_proposals="The chain includes drinking-water and veterinary laboratories, electrical switching, rail, maritime, wildfire, aviation, and other handovers; no frozen core title centers food cold-chain excursions, hold-release control, corrective action, and shift handover.",
    ),
    proposal(
        5,
        title="Freed ID Controlled Identifiers verification-method binding, relationship, expiry, and revocation profile",
        mission_surface="controlled identifier document, controller, verification method identifier, type, material, authentication, assertion, capability invocation, capability delegation, key agreement, expiry, revocation, retrieval, ambiguity, and privacy refusal",
        hypothesis="Synthetic vectors can enforce bounded W3C Controlled Identifiers structure and binding rules without asserting a real controller, identifier, key, proof, relationship, resolution, interoperability, or physical-identity binding.",
        null_or_failure="A method lacks an explicit controller, conflicting material passes, a revoked or expired method verifies, a relationship is inferred rather than declared, retrieval crosses controller scope, or synthetic structure becomes real identity assurance.",
        approval_class="safe_now_synthetic_nonproduction",
        execution_lane="x2_proxy_protocol",
        current_primary_or_official_source_needs=["V6471-S12", "V6471-S13"],
        concrete_artifacts=["freed-id/controlled-identifier-profile.json", "freed-id/controlled-identifier-mutations.json"],
        test_falsifier_or_acceptance_gate="Vectors must reject missing controller, duplicate or conflicting material, undeclared relationships, expired or revoked methods, ambiguous retrieval, physical-identity promotion, and production promotion.",
        rollback_or_recovery="Reject and retain the vector, publish no real identifier or key data, and require conforming controllers, real keys and proofs, resolution, relationship processing, interoperability, privacy/security review, recovery, and trust governance.",
        protected_gates=["real_identity", "real_keys", "real_proofs", "live_resolution", "interoperability", "production", "security_review"],
        expected_disposition="represented",
        novelty_against_470_frozen_proposals="Prior Freed ID work covers VC, OpenID4VC, mdoc, DPoP, federation, status, cryptosuite agility, and SCITT; no frozen title centers Controlled Identifiers method-controller binding plus declared relationships, expiry, and revocation.",
    ),
    proposal(
        6,
        title="CBR food-recall reach, allergen disclosure, supplier confidentiality, remedy, and Māori-authority matrix",
        mission_surface="recall trigger, product and lot scope, allergen or contaminant notice, distribution reach, supplier confidentiality, personal information, disposal or refund, remedy, legal interpretation, affected parties, place and provenance data, and Māori authority",
        hypothesis="A refusal-first matrix can expose unresolved recall, disclosure, privacy, remedy, and authority questions without deciding a real recall, safety finding, entitlement, disclosure, place meaning, or remedy.",
        null_or_failure="The matrix identifies a real protected person or lot, orders a recall, decides safety or compensation, interprets law, discloses confidential data, asserts cultural or Māori authority, or treats guidance as delegated case authority.",
        approval_class="authorized_affected_parties_and_competent_authority_required",
        execution_lane="x2_exact_gate",
        current_primary_or_official_source_needs=["V6471-S08", "V6471-S09", "V6471-S10", "V6471-S11"],
        concrete_artifacts=["cbr/food-recall-authority-reservation.json", "cbr/food-recall-remedy-matrix.json"],
        test_falsifier_or_acceptance_gate="Repository software must stop at unknown or reserved; only competent food-safety, privacy, legal, affected-party, tangata whenua, iwi, hapū, and Māori authorities can close their respective gates.",
        rollback_or_recovery="Stop before recall, disclosure, disposal, compensation, cultural, provenance, place-name, or legal conclusions; minimize data and route only through authorized external processes.",
        protected_gates=["affected_party_authority", "food_safety_authority", "privacy", "legal_interpretation", "maori_authority", "remedy_decision", "real_recall"],
        expected_disposition="exact_gate",
        novelty_against_470_frozen_proposals="Prior CBR matrices address medicine recalls, museums, fisheries, utilities, archives, aviation, wildfire, and other domains; no frozen title combines food recall reach, allergen disclosure, supplier confidentiality, remedy, and Māori authority.",
    ),
    proposal(
        7,
        title="SQLite session changeset, patchset, schema-match, conflict-callback, and rebase tribunal",
        mission_surface="session table filter, primary key, changeset, patchset, schema match, conflict class, omit, replace, abort, inversion, concatenation, rebase, transaction, path confinement, and teardown",
        hypothesis="A disposable owner-local tribunal can distinguish valid synthetic SQLite changeset application from schema drift, conflict misclassification, unsafe replacement, and partial-credit assumptions without touching canonical state.",
        null_or_failure="A schema mismatch applies, a table without a primary key gains change credit, a conflict callback chooses an undeclared action, an aborted application is treated as complete, or canonical or sibling data is touched.",
        approval_class="safe_now_disposable_synthetic_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6471-S14"],
        concrete_artifacts=["tooling/sqlite-session-contract.json", "tooling/sqlite-session-mutations.json"],
        test_falsifier_or_acceptance_gate="Disposable fixtures must cover changeset and patchset distinction, primary-key requirements, schema mismatch, all declared conflict actions, abort rollback, inversion, concatenation, rebase, confinement, and teardown.",
        rollback_or_recovery="Abort the disposable transaction, retain the failed fixture, close every handle, remove only the verified owner-local root, and never apply to canonical, sibling, user, or production data.",
        protected_gates=["canonical_evidence", "sibling_lane", "user_data", "destructive_filesystem", "production", "exhaustive_security"],
        expected_disposition="completed",
        novelty_against_470_frozen_proposals="Prior SQLite work covers WAL, migrations, backup, VACUUM INTO, busy state, and crash recovery; no frozen core title centers the Session extension, changesets, patchsets, conflict callbacks, and rebase.",
    ),
    proposal(
        8,
        title="Accessible long-form heading outline, meaningful sequence, footnote backlink, and print-pagination structural audit",
        mission_surface="document title, landmark, heading rank, section label, reading order, footnote reference, footnote backlink, duplicate anchor, page-break marker, print pagination, focus target, table of contents, and manual reservation",
        hypothesis="A structural auditor can reject broken long-form reading order, heading hierarchy, and footnote navigation while reserving browser, print, assistive-technology, cognitive, language, and affected-user evaluation.",
        null_or_failure="Heading rank conveys false structure, DOM and visual sequence conflict, a footnote lacks a unique return path, print markers replace semantic structure, focus is lost, or structure becomes complete conformance.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6471-S15", "V6471-S16"],
        concrete_artifacts=["accessibility/long-form-structure-contract.json", "accessibility/long-form-structure-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must cover titles, landmarks, heading ranks, meaningful sequence, unique references, backlinks, focus targets, table-of-contents links, print markers, and explicit manual reservations.",
        rollback_or_recovery="Mark structure incomplete, retain failures, restore semantic order and navigation, and require qualified manual keyboard, print, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation.",
        protected_gates=["accessibility_complete", "runtime_behavior", "print_behavior", "assistive_technology", "cognitive_evaluation", "affected_user_acceptance"],
        expected_disposition="completed",
        novelty_against_470_frozen_proposals="The chain covers tables, charts, figures, forms, reflow, focus, drag, authentication, carousels, language, and details-summary; no frozen title centers long-form heading outline, reading sequence, footnote backlinks, and print pagination.",
    ),
    proposal(
        9,
        title="Thermo/Psyche Clausius-Clapeyron coexistence-slope, latent-heat, molar-volume, and psyche-nonconversion classifier",
        mission_surface="coexisting phases, pressure, temperature, coexistence slope, latent heat or enthalpy, molar or specific volume difference, sign, units, single-component scope, equilibrium, triple point, critical point, approximation, and category barrier",
        hypothesis="A typed classifier can check bounded Clausius-Clapeyron domain obligations while rejecting conversion of phase-boundary quantities into psyche, autonomy, justice, capability, consciousness, or personhood claims.",
        null_or_failure="Phases are unlabeled, latent heat or volume difference is missing, units or sign drift, a critical or nonequilibrium point is silently used, an approximation is hidden, or a thermodynamic slope becomes a human or fundamental-mind claim.",
        approval_class="safe_now_formal_classifier_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6471-S17"],
        concrete_artifacts=["thermo-psyche/clausius-clapeyron-contract.json", "thermo-psyche/clausius-clapeyron-mutations.json"],
        test_falsifier_or_acceptance_gate="Fixtures must type phases, slope, latent heat, volume difference, sign, units, equilibrium, component count, critical and triple-point scope, approximations, and a hard psyche nonconversion barrier.",
        rollback_or_recovery="Restore the thermodynamic domain and assumptions, retain the rejection, and require independently valid human theory, measures, authority, and participant evidence before any human inference.",
        protected_gates=["empirical_law", "psyche_law", "autonomy_inference", "participant_inference", "consciousness", "personhood"],
        expected_disposition="completed",
        novelty_against_470_frozen_proposals="Prior classifiers cover Clausius inequality, phase critical scaling, Maxwell relations, Onsager, Crooks, Jarzynski, Hatano-Sasa, and other identities; no frozen title centers the Clausius-Clapeyron coexistence slope and latent-heat-volume domain.",
    ),
    proposal(
        10,
        title="Stage 20 negative-control outcome, positive-control calibration, sham-endpoint, and nonpromotion board",
        mission_surface="target estimand, negative-control exposure, negative-control outcome, positive control, sham endpoint, shared causes, expected direction, calibration model, prespecification, multiplicity, deviation, result, and terminal abstention",
        hypothesis="A structural board can require explicit control assumptions and prevent favorable or null control results from automatically promoting GMUT, THOS, Freed ID, CBR, or Stage 20 claims.",
        null_or_failure="A control is selected after results, shared-cause assumptions are absent, control failure is hidden, control success is treated as validation, calibration is improvised, multiplicity disappears, or Stage 20 advances.",
        approval_class="safe_now_structural_only",
        execution_lane="x2_build_task",
        current_primary_or_official_source_needs=["V6471-S18", "V6471-S19"],
        concrete_artifacts=["stage20/control-outcome-contract.json", "stage20/control-outcome-mutations.json"],
        test_falsifier_or_acceptance_gate="Mutations must reject post hoc controls, absent shared-cause reasoning, hidden failures, unregistered calibration, multiplicity omission, fabricated review, and any automatic Stage 20 promotion.",
        rollback_or_recovery="Withdraw affected evidence credit, retain every control result and deviation, require prospective registration and appropriate independent review, and abstain from promotion.",
        protected_gates=["stage20", "participant_evidence", "empirical_confirmation", "reviewer_authority", "independent_reproduction", "deployment", "proof_or_canon"],
        expected_disposition="completed",
        novelty_against_470_frozen_proposals="Prior Stage 20 boards cover optional stopping, multiverses, HARKing, registered reports, missingness, thresholds, contamination, and selective reporting; no frozen title centers negative and positive controls plus sham endpoints and calibration nonpromotion.",
    ),
]


SOURCES = [
    {"source_id":"V6471-S01","title":"The Update Framework Specification 1.0.35","url":"https://theupdateframework.github.io/specification/latest/","publisher":"The Update Framework","status":"current","source_class":"official_specification","use":"role, threshold, delegation, root rotation, expiry, consistent snapshot, rollback, freeze, and mix-and-match obligations"},
    {"source_id":"V6471-S02","title":"TUF Security","url":"https://theupdateframework.io/docs/security/","publisher":"The Update Framework","status":"current","source_class":"official_security_guidance","use":"attack-model and explicit non-goal boundary only"},
    {"source_id":"V6471-S03","title":"On the Gauge Dependence of Spontaneous Symmetry Breaking in Gauge Theories","url":"https://doi.org/10.1016/0550-3213(75)90301-6","publisher":"Nuclear Physics B","status":"stable","source_class":"primary_research","use":"Nielsen-identity provenance and gauge-parameter obligation context"},
    {"source_id":"V6471-S04","title":"Removing the gauge parameter dependence of the effective potential by a field redefinition","url":"https://arxiv.org/abs/1406.0788","publisher":"arXiv","status":"stable","source_class":"primary_research","use":"field-redefinition and effective-potential scope context"},
    {"source_id":"V6471-S05","title":"CHIME/FRB Open Data Catalog","url":"https://chime-frb-open-data.github.io/catalog/","publisher":"CHIME/FRB Collaboration","status":"current","source_class":"official_data_release_description","use":"zero-row catalog schema and field obligations only"},
    {"source_id":"V6471-S06","title":"CHIME/FRB Open Data Injections","url":"https://chime-frb-open-data.github.io/injections/","publisher":"CHIME/FRB Collaboration","status":"current","source_class":"official_data_release_description","use":"selection-function and injection obligations only; no rows imported"},
    {"source_id":"V6471-S07","title":"General Principles of Food Hygiene CXC 1-1969","url":"https://www.fao.org/fao-who-codexalimentarius/publications/en/","publisher":"FAO/WHO Codex Alimentarius","status":"current","source_class":"official_intergovernmental_standard","use":"food hygiene, monitoring, corrective action, verification, and documentation vocabulary only"},
    {"source_id":"V6471-S08","title":"New Zealand Food Safety recalled food products and business guidance","url":"https://www.mpi.govt.nz/food-safety-home/food-recalls-and-complaints/recalled-food-products","publisher":"Ministry for Primary Industries","status":"current","source_class":"official_guidance","use":"recall reach and communication context only; not case authority"},
    {"source_id":"V6471-S09","title":"Food Act 2014","url":"https://www.legislation.govt.nz/act/public/2014/0032/latest/DLM2996092.html","publisher":"New Zealand Legislation","status":"current","source_class":"official_legislation","use":"legal and recall authority reservation; no legal interpretation"},
    {"source_id":"V6471-S10","title":"Privacy Act 2020 privacy principles","url":"https://www.privacy.org.nz/privacy-principles/","publisher":"Office of the Privacy Commissioner","status":"current","source_class":"official_regulator_guidance","use":"personal-information and current IPP 3A privacy boundary"},
    {"source_id":"V6471-S11","title":"Principles of Māori Data Sovereignty","url":"https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf","publisher":"Te Mana Raraunga","status":"stable","source_class":"maori_authority_source","use":"Māori data-governance and authority gate; never delegated authority"},
    {"source_id":"V6471-S12","title":"Controlled Identifiers v1.0","url":"https://www.w3.org/TR/controller-document/","publisher":"W3C","status":"current","source_class":"official_standard","use":"controller, verification-method, relationship, expiry, revocation, and retrieval obligations"},
    {"source_id":"V6471-S13","title":"Verifiable Credential Data Integrity 1.0","url":"https://www.w3.org/TR/vc-data-integrity/","publisher":"W3C","status":"current","source_class":"official_standard","use":"synthetic proof and verification-method binding context only"},
    {"source_id":"V6471-S14","title":"SQLite Session Extension","url":"https://www.sqlite.org/sessionintro.html","publisher":"SQLite Project","status":"current","source_class":"official_documentation","use":"changeset, patchset, conflict, rebase, and schema obligations"},
    {"source_id":"V6471-S15","title":"Web Content Accessibility Guidelines 2.2","url":"https://www.w3.org/TR/WCAG22/","publisher":"W3C","status":"current","source_class":"official_standard","use":"structural accessibility requirements and complete-conformance reservation"},
    {"source_id":"V6471-S16","title":"G57 Ordering content in a meaningful sequence","url":"https://www.w3.org/WAI/WCAG22/Techniques/general/G57","publisher":"W3C WAI","status":"current","source_class":"official_standard_guidance","use":"meaningful sequence technique context only"},
    {"source_id":"V6471-S17","title":"NIST Chemistry WebBook SRD 69","url":"https://webbook.nist.gov/chemistry/","publisher":"National Institute of Standards and Technology","status":"current","source_class":"official_reference_data_service","use":"thermodynamic property vocabulary and data-boundary context; no values imported"},
    {"source_id":"V6471-S18","title":"Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/","publisher":"Epidemiology","status":"stable","source_class":"primary_research","use":"negative-control assumptions, limitations, and prespecification context"},
    {"source_id":"V6471-S19","title":"Registered Reports","url":"https://www.cos.io/initiatives/registered-reports","publisher":"Center for Open Science","status":"current","source_class":"authoritative_practice_guidance","use":"prospective review and nonpromotion context only"},
]


SAFE_TASK_TITLES = [
    "Verify exact inherited source x1 evidence ancestry and zero-merge history",
    "Reconcile all 470 inherited proposal records before novelty credit",
    "Build normalized-title and token-neighbor collision audit",
    "Review current stable draft and watch source statuses",
    "Declare Git-blob Git-index clean-filter and checkout hash domains",
    "Build exact x1 staged-surface allowlist with historical protection",
    "Enforce deterministic JSON ordering UTF-8 and LF authoring",
    "Separate scanner candidates from confirmed payload hits",
    "Audit family-current callers and historical aliases",
    "Initialize Method Flow with every preflight failure retained",
    "Record bounded subprocess timeout cancellation teardown and quiescence rules",
    "Prove null-safe four-way branch equality",
    "Review stale lifecycle labels and count-dependent mirrors",
    "Lint boundary vocabulary and noncompensation rules",
    "Record workload wellbeing document length and owner footprint",
    "Build TUF threshold root-rotation and rollback fixture contract",
    "Build Nielsen-identity typed obligation fixture contract",
    "Build CHIME FRB zero-row receipt schema",
    "Build food cold-chain handover trace schema",
    "Build Controlled Identifiers synthetic vector schema",
    "Build food-recall authority reservation matrix schema",
    "Build SQLite session disposable-fixture contract",
    "Build long-form accessibility structural fixture",
    "Build Clausius-Clapeyron typed-domain fixture",
    "Build Stage 20 control-outcome nonpromotion fixture",
    "Preserve citation-to-observation and authority firewalls",
    "Carry forward 17 open gaps and 18 exact gates",
    "Carry forward the 3,151-negative activation baseline",
    "Keep terminal route PREPARED_NOT_SENT before proof",
    "Emit owner-scoped x1 wellbeing and source receipts",
]

CANDIDATE_TITLES = [
    "TUF duplicate-key threshold and delegation-escape mutation prototype",
    "TUF root-rotation freeze rollback and mix-and-match quarantine prototype",
    "Nielsen missing-coefficient and off-shell promotion mutation prototype",
    "Nielsen background-split and truncation-scope mismatch prototype",
    "CHIME FRB Galactic-subtraction post-selection quarantine prototype",
    "CHIME FRB exposure excluded-flag and injection-selection lock prototype",
    "Food cold-chain stale-temperature and unsafe-release replay prototype",
    "Food corrective-action amendment and handover-conflict prototype",
    "Controlled Identifier controller-binding and relationship prototype",
    "Controlled Identifier expiry revocation and ambiguous-retrieval prototype",
    "Food-recall allergen reach and confidentiality matrix prototype",
    "Food-remedy and Māori-authority reservation prototype",
    "SQLite changeset schema-conflict and abort-rollback prototype",
    "SQLite patchset inversion concatenation and rebase prototype",
    "Long-form heading reading-order and duplicate-anchor checker",
    "Footnote backlink focus-target and print-pagination classifier",
    "Clausius-Clapeyron phase-label and unit-sign mutation prototype",
    "Thermodynamic critical-point and approximation applicability guard",
    "Negative-control shared-cause and post-selection prototype",
    "Positive-control calibration sham-endpoint and nonpromotion prototype",
]

SKILL_SPECS = [
    ("ghc-family-tuf-trust-tribunal", "Audit synthetic TUF role threshold rotation rollback and delegation traces"),
    ("ghc-family-nielsen-identity-obligations", "Audit Nielsen identity gauge and truncation obligations"),
    ("ghc-family-chime-frb-zero-row", "Preserve a zero-row CHIME FRB study boundary"),
    ("ghc-family-food-cold-chain-handover", "Audit synthetic cold-chain excursion and handover traces"),
    ("ghc-family-controlled-identifier-profile", "Audit synthetic controller method and relationship bindings"),
    ("ghc-family-food-recall-authority-reservation", "Reserve recall privacy remedy and Māori authority gates"),
    ("ghc-family-sqlite-session-tribunal", "Audit disposable SQLite changeset and conflict fixtures"),
    ("ghc-family-long-form-accessibility-audit", "Audit heading sequence footnote and print structure"),
    ("ghc-family-clausius-clapeyron-domain", "Keep coexistence relations inside thermodynamic domains"),
    ("ghc-family-control-outcome-nonpromotion", "Guard negative and positive controls from automatic promotion"),
    ("ghc-family-exact-anchor-preflight-v3", "Verify exact inherited anchors single-parent history and zero merges"),
    ("ghc-family-clean-filter-blob-parity", "Compare clean-filter bytes with exact commit blobs"),
    ("ghc-family-count-mirror-closure", "Refresh count-dependent mirrors from authoritative ledgers"),
    ("ghc-family-scanner-incident-adjudication", "Separate scanner candidates incidents and confirmed payload hits"),
    ("ghc-family-x1-immutable-blob-seal", "Verify frozen x1 content through exact Git blobs"),
    ("ghc-family-exact-exclusion-arithmetic", "Bind eligible test credit to exact inclusion and exclusion sets"),
    ("ghc-family-route-hold-acknowledgement-gate", "Hold routing until proof and count a send only after acknowledgement"),
    ("ghc-family-owner-manifest-self-exclusion", "Audit owner manifests with declared self-exclusions"),
    ("ghc-family-method-trigger-recurrence", "Match Method Flow triggers to recurrence guards"),
    ("ghc-family-authority-noncompensation-lint", "Prevent software evidence from compensating for authority gaps"),
]

RUNNER_TITLES = [
    "ghc_family_tuf_trust_tribunal.py",
    "ghc_family_nielsen_identity_obligations.py",
    "ghc_family_chime_frb_zero_row.py",
    "ghc_family_food_cold_chain_handover.py",
    "ghc_family_controlled_identifier_profile.py",
    "ghc_family_sqlite_session_tribunal.py",
    "ghc_family_long_form_accessibility_audit.py",
    "ghc_family_clausius_clapeyron_domain.py",
    "ghc_family_control_outcome_nonpromotion.py",
    "ghc_family_v647_v1_validation_runner.py",
]

CLEAN_TASK_TITLES = [
    "Reconcile proposal and outcome counts across receipts",
    "Reconcile sealed external synthetic and operational negatives",
    "Synchronize Method Flow counts and validator expectations",
    "Correct stale phase labels additively",
    "Preserve compatibility callers while selecting family-current tools",
    "Normalize generated JSON key ordering",
    "Normalize generated UTF-8 and LF authoring",
    "Keep Git-blob Git-index clean-filter and checkout domains explicit",
    "Review public files for private absolute paths",
    "Review public files for raw task or thread identifiers",
    "Review public files for credential token or key assignments",
    "Review source statuses for allowed vocabulary",
    "Review citations for observation and data nonconversion",
    "Review x1 staged files for x2 contamination",
    "Review x2 outcomes for four-class vocabulary",
    "Review exact and blocked packets for zero execution credit",
    "Review owner footprint against the 15,000-file threshold",
    "Review long-form report headings sequence footnotes and print structure",
    "Review report manual and affected-user reservations",
    "Review Māori authority and data-governance reservations",
    "Review food-safety professional and legal authority reservations",
    "Review real-data and likelihood counters remain zero",
    "Review real-person lot sensor and operation counters remain zero",
    "Review real-key proof resolution and identity counters remain zero",
    "Review source x1 evidence and final ancestry",
    "Review phase commit cap and zero-merge history",
    "Review validation branch remains named and local-only",
    "Review canonical four-way remote equality",
    "Refresh phase-scoped GHC Family Index after tools",
    "Refresh wellbeing and terminal route before handoff",
]

EXACT_PACKET_TITLES = [
    "Real CHIME FRB data download and likelihood execution",
    "Real food lot sensor hold release or disposal decision",
    "Real recall allergen disclosure or public-safety action",
    "Production identifier controller key proof or resolution operation",
    "Real identity interoperability recovery or trust-governance decision",
    "Supplier confidentiality legal interpretation or remedy allocation",
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
    {"negative_id":"V6471-X1-N01","method_id":"V6471-M01","summary":"A JavaScript orchestration cell used PowerShell here-string syntax directly and was rejected by the JavaScript parser before any Git or filesystem command ran.","retained":True,"recovered":True},
    {"negative_id":"V6471-X1-N02","method_id":"V6471-M02","summary":"A read batch assumed an older root proposal-ledger filename that does not exist in v646-v8 before exact phase paths were enumerated.","retained":True,"recovered":True},
    {"negative_id":"V6471-X1-N03","method_id":"V6471-M03","summary":"The Method Flow runner auto-promoted a method to validated after a passing witness, then an unnecessary duplicate validated transition was correctly rejected.","retained":True,"recovered":True},
    {"negative_id":"V6471-X1-N04","method_id":"V6471-M04","summary":"The first staged privacy review treated the x1 reviewer's embedded private-path detection pattern as a confirmed payload hit instead of a scanner definition.","retained":True,"recovered":True},
    {"negative_id":"V6471-X1-N05","method_id":"V6471-M05","summary":"A rerun of the preregistration builder restored the rotation receipt template value, so a patch expecting the earlier measured owner-file count found no matching line.","retained":True,"recovered":True},
    {"negative_id":"V6471-X1-N06","method_id":"V6471-M06","summary":"A PowerShell backtick used inside a JavaScript template string terminated the orchestration source before the commit or any nested Git command could run.","retained":True,"recovered":True},
    {"negative_id":"V6471-X1-N07","method_id":"V6471-M07","summary":"The first post-commit exact-byte verifier assumed ProcessStartInfo.ArgumentList was available, but that property was null on this Windows PowerShell host before any manifest entry was read.","retained":True,"recovered":True},
]

METHOD_SPECS = [
    {
        "method_id":"V6471-M01",
        "title":"Separate orchestration and shell language syntax before execution",
        "failure_signature":"JavaScript parser rejected a PowerShell here-string token before nested commands ran.",
        "trigger_preconditions":["A JavaScript tool-orchestration cell must carry a multiline PowerShell program."],
        "candidate_workaround":"Represent PowerShell as a JavaScript template string and keep native commands inside that string.",
        "recurrence_guard":"Before execution, check that shell-only here-string tokens never appear at JavaScript top level.",
        "rollback":"Discard the rejected orchestration cell; no repository rollback is required because no nested command ran.",
        "protected_gates":["owned_lane_only","no_destructive_git","no_sibling_mutation","privacy_exclusions"],
        "retained_negative_ids":["V6471-X1-N01"],
        "failed_observed":"The orchestration parser rejected the mixed-language cell before command execution.",
        "pass_observed":"The same read-only Git probes ran from JavaScript template strings and returned exact clean ancestry and equality receipts.",
    },
    {
        "method_id":"V6471-M02",
        "title":"Enumerate exact phase paths before reading inherited artifacts",
        "failure_signature":"A batch read failed because an inherited phase used x1-proposals.json rather than the assumed older proposal-ledger filename.",
        "trigger_preconditions":["Inherited phases may preserve different compatibility filenames."],
        "candidate_workaround":"Run a bounded rg --files enumeration under the exact phase root, then read only discovered paths.",
        "recurrence_guard":"Never infer a current artifact filename solely from an older sibling phase.",
        "rollback":"Discard the failed read assumption; no file mutation occurred.",
        "protected_gates":["historical_compatibility","owned_lane_only","privacy_exclusions"],
        "retained_negative_ids":["V6471-X1-N02"],
        "failed_observed":"The assumed root ledger path was absent and the read batch returned no artifact content.",
        "pass_observed":"Bounded path enumeration found x1-proposals.json, the frozen-chain index, collision audit, source ledger, and Method Flow ledger before exact reads.",
    },
    {
        "method_id":"V6471-M03",
        "title":"Inspect Method Flow state after witnesses before explicit transitions",
        "failure_signature":"A passing witness auto-promoted a candidate method to validated, and a duplicate validated transition was rejected.",
        "trigger_preconditions":["The family Method Flow runner may perform an automatic state transition after a passing witness."],
        "candidate_workaround":"After each passing witness, read the resulting method state and transition directly from validated to preferred only once.",
        "recurrence_guard":"Do not assume a method remains candidate after the runner accepts a passing witness.",
        "rollback":"Keep the valid ledger state and discard only the rejected duplicate transition command.",
        "protected_gates":["append_only_failures","state_transition_integrity","no_evidence_erasure"],
        "retained_negative_ids":["V6471-X1-N03"],
        "failed_observed":"The runner rejected validated to validated while preserving the already valid method and witnesses.",
        "pass_observed":"The corrected workflow inspected state, promoted validated methods directly to preferred, and validated the append-only ledger.",
    },
    {
        "method_id":"V6471-M04",
        "title":"Adjudicate explicit scanner-definition files before confirming privacy hits",
        "failure_signature":"The staged scanner classified a second validation script's embedded private-path pattern as payload.",
        "trigger_preconditions":["A staged validation script contains the same byte patterns it is designed to detect."],
        "candidate_workaround":"Maintain an exact phase-local scanner-definition path set and still report every candidate with its disposition.",
        "recurrence_guard":"Never suppress a candidate globally; definition status must match one exact reviewed script path.",
        "rollback":"Keep the failed privacy receipt, patch only the exact definition adjudication, and rerun the same staged blobs.",
        "protected_gates":["privacy_scan_integrity","exact_path_scope","no_global_suppression"],
        "retained_negative_ids":["V6471-X1-N04"],
        "failed_observed":"The first review reported four candidates and one confirmed hit in the x1 reviewer's scanner definition.",
        "pass_observed":"The corrected exact-path adjudication retained all definition candidates and reported zero confirmed payload hits.",
    },
    {
        "method_id":"V6471-M05",
        "title":"Bind measured rotation counts in the deterministic preregistration builder",
        "failure_signature":"A regenerated receipt replaced an ad hoc measured count with its original template value before a later patch.",
        "trigger_preconditions":["A generated receipt is rerun after an out-of-band patch to one of its derived fields."],
        "candidate_workaround":"Move the verified inherited and owner-generated counts into the builder source, regenerate, and review the deterministic output.",
        "recurrence_guard":"Never patch a generated count without updating its authoritative builder in the same lifecycle.",
        "rollback":"Discard the failed patch attempt; it changed no file, then regenerate from the corrected builder.",
        "protected_gates":["deterministic_generation","owner_file_threshold","no_history_rewrite"],
        "retained_negative_ids":["V6471-X1-N05"],
        "failed_observed":"The patch expected 51 but the regenerated receipt truthfully contained the template value 0.",
        "pass_observed":"The corrected builder emitted the measured inherited tracked baseline and owner-generated x1 count from its authoritative source, below threshold.",
    },
    {
        "method_id":"V6471-M06",
        "title":"Build Git revision-path specifications without cross-language escape characters",
        "failure_signature":"A PowerShell escape backtick inside a JavaScript template string ended the outer string before nested execution.",
        "trigger_preconditions":["A JavaScript template carries PowerShell that needs a Git revision:path argument."],
        "candidate_workaround":"Construct the revision and path with PowerShell string concatenation and pass the resulting variable to Git.",
        "recurrence_guard":"Do not embed PowerShell backtick escapes inside JavaScript template strings.",
        "rollback":"Discard the rejected orchestration cell; no commit or Git command ran.",
        "protected_gates":["no_unreviewed_commit","exact_revision_credit","no_history_rewrite"],
        "retained_negative_ids":["V6471-X1-N06"],
        "failed_observed":"JavaScript returned an unexpected-colon syntax error before calling the shell tool.",
        "pass_observed":"A read-only concatenated revision-path specification retrieved the exact staged manifest without parser ambiguity.",
    },
    {
        "method_id":"V6471-M07",
        "title":"Verify exact Git blob bytes through a Python subprocess runner",
        "failure_signature":"PowerShell ProcessStartInfo.ArgumentList was null before the exact-byte loop could launch Git.",
        "trigger_preconditions":["Exact manifest parity requires byte-preserving Git blob reads on a host with inconsistent ProcessStartInfo APIs."],
        "candidate_workaround":"Use Python subprocess.check_output with an argument list for git cat-file blob and hash the returned bytes directly.",
        "recurrence_guard":"Prefer the repository's byte-preserving manifest runner over host-specific PowerShell process APIs.",
        "rollback":"Keep the already-created x1 commit, add one bounded x1 repair commit, and do not rewrite history.",
        "protected_gates":["exact_blob_parity","x1_commit_cap","no_history_rewrite","no_x2_before_push"],
        "retained_negative_ids":["V6471-X1-N07"],
        "failed_observed":"The verifier stopped on a null ArgumentList before checking the first manifest entry; no push occurred.",
        "pass_observed":"The Python runner hashed every exact x1 commit blob and reported zero manifest mismatches.",
    },
]
