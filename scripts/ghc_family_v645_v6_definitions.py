#!/usr/bin/env python3
"""Frozen definitions for Orin Thale v645-v6.

This module is data-only phase configuration. Importing it performs no I/O.
"""

from __future__ import annotations

from typing import Any


PHASE = "v645-gmut-thos-v6-x1-x2"
PHASE_SHORT = "v645-v6"
OWNER = "Orin Thale"
SLUG = "orin-thale"
PRONOUNS = "they/them"
ROLE = "evidence cartographer and boundary steward"
HOPE = "leave each successor a cleaner, truer path whose failures remain findable"
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = "maritime bridge-resource management and near-miss review"
SOURCE_PHASE = "v645-gmut-thos-v5-x1-x2"
SOURCE_REVISION = "f17246d4f5eb9ea68706479bf5d7c9e4923c22e6"
SOURCE_SEAL_REVISION = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
SOURCE_X1_REVISION = "2e330ab76f03c05ff556c484c22851d682b0ac7b"
SOURCE_EVIDENCE_REVISION = "658466909006bf4403e8a346d8b7320d956a42b1"
PRIOR_FROZEN_PROPOSALS = 360
INHERITED_EFFECTIVE_NEGATIVES = 2172
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Orin Thale, their role, hope, pronouns, and family language are relational working "
    "labels only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, professional qualification, or independent authority."
)

TRUTH_BOUNDARY = (
    "Software, official or primary sources, and synthetic fixtures establish bounded structural "
    "behavior only. They do not establish empirical GMUT confirmation, a likelihood result, "
    "THOS effectiveness, maritime competence, production identity assurance, CBR legitimacy, "
    "Maori authority, legal or cultural ratification, independent-team reproduction, AGI or ASI, "
    "consciousness or personhood, complete accessibility, exhaustive security, a Theory of "
    "Everything, or Stage 20 readiness."
)


def proposal(
    number: int,
    title: str,
    mission_surface: str,
    hypothesis: str,
    null_or_failure: str,
    approval_class: str,
    execution_lane: str,
    source_needs: list[str],
    deliverables: list[str],
    acceptance_gate: str,
    rollback: str,
    protected_gates: list[str],
    expected: str,
    novelty: str,
) -> dict[str, Any]:
    return {
        "proposal_id": f"V6456-P{number:02d}",
        "title": title,
        "mission_surface": mission_surface,
        "hypothesis": hypothesis,
        "null_or_failure": null_or_failure,
        "approval_class": approval_class,
        "execution_lane": execution_lane,
        "current_primary_or_official_source_needs": source_needs,
        "concrete_artifacts": deliverables,
        "test_falsifier_or_acceptance_gate": acceptance_gate,
        "rollback_or_recovery": rollback,
        "protected_gates": protected_gates,
        "expected_disposition": expected,
        "novelty_against_360_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Method Flow rollback-witness, side-effect budget, and compensating-action recovery ledger",
        "failed procedure, side effects, rollback completeness, compensating action, witness credit, recurrence guard, and append-only negative retention",
        "A method ledger can require an explicit side-effect budget and a passing rollback or compensating-action witness before a recovery becomes preferred.",
        "A method is promoted without a passing witness, unobserved side effects are declared absent, rollback is asserted but untested, or a failed witness is erased.",
        "safe_now_owner_scoped_workflow",
        "x2_build_task",
        ["S01", "S18"],
        ["method-flow/rollback-budget-contract.json", "method-flow/method-flow-state.json"],
        "Synthetic incidents must retain failed and passing witnesses, enumerate bounded side effects, and reject promotion when rollback evidence is absent.",
        "Keep the method candidate or observed, preserve the negative, stop the retry, and restore only the last owner-scoped state.",
        ["destructive_action", "sibling_lane", "unbounded_retry", "independent_reproduction"],
        "completed",
        "Prior Method Flow titles cover failure signatures, invalidation, child starts, retry clusters, and causal graphs; none makes rollback witnessing and side-effect budgeting the central promotion gate.",
    ),
    proposal(
        2,
        "GMUT eikonal characteristic transport, mode-conversion, and caustic obligation tribunal",
        "typed scalar-tensor principal modes, eikonal ordering, eigenvectors, transport amplitudes, mode conversion, caustics, gauge obligations, and regime refusal",
        "A symbolic obligation checker can keep phase, amplitude, polarization, transport, coupling, and caustic assumptions typed without treating geometric optics as a proof of physical stability.",
        "The checker conflates principal and transport order, loses a coupled mode, divides through a caustic, treats a gauge component as an observable, or promotes a WKB fixture to physical truth.",
        "safe_now_symbolic_research_only",
        "x2_build_task",
        ["S02", "S03"],
        ["gmut/eikonal-transport-contract.json", "gmut/eikonal-mode-mutation-vectors.json"],
        "Positive and negative symbolic fixtures must enforce order separation, mode inventory, coupling declarations, caustic refusal, gauge boundaries, and no empirical promotion.",
        "Quarantine the invalid expansion, restore unreduced coupled equations and declared order, retain the counterexample, and make no force, prediction, constraint, or stability claim.",
        ["empirical_confirmation", "physical_stability_proof", "force_claim", "likelihood", "theory_of_everything"],
        "completed",
        "Earlier GMUT work covers principal symbols, causal cones, characteristics, gauge, screening, scalarization, and quasi-static ordering; none centers eikonal amplitude transport, coupled-mode conversion, and caustic refusal together.",
    ),
    proposal(
        3,
        "GMUT EHT black-hole shadow ring-diameter and calibration blind public-data protocol",
        "EHT calibrated visibilities, imaging choices, angular scale, ring diameter, mass-distance nuisance, calibration covariance, blind adapter, real-row stop, and likelihood nonclaim",
        "A zero-row adapter contract can enumerate EHT provenance, calibration, imaging, nuisance, blinding, and likelihood requirements without downloading observations or producing constraints.",
        "The adapter ingests a real row, assumes an image pixel is an independent datum, omits calibration or mass-distance nuisance, chooses an outcome-aware pipeline, evaluates a likelihood, or reports a GMUT constraint.",
        "real_data_and_independent_review_required",
        "x2_open_gap",
        ["S04", "S05"],
        ["gmut/eht-shadow-study-contract.json", "gmut/eht-shadow-zero-row-receipt.json"],
        "The phase must retain zero real rows, zero likelihood evaluations, and zero constraints; real execution needs a frozen analysis, uncertainty treatment, authorized data handling, and appropriate independent review.",
        "Stop before download or fit, retain the zero-row receipt, and route any real-data study through a separately authorized preregistration and review process.",
        ["real_data", "likelihood", "constraints", "empirical_confirmation", "independent_review"],
        "open_gap",
        "The frozen chain covers gravitational waves, pulsars, ranging, lensing, ephemerides, RSD, ISW, SLR, standard sirens, and DESI BAO; no prior proposal names EHT calibrated shadow data or ring-diameter inference.",
    ),
    proposal(
        4,
        "THOS maritime bridge-team challenge-response, authority-gradient, and watch-handover matched-budget protocol",
        "bridge-team challenge response, closed-loop communication, authority gradient, watch handover, matched budget, fatigue, safety events, blinding, and operator reservation",
        "A synthetic schedule can represent matched-budget bridge-team communication and handover obligations while exposing authority-gradient and fatigue risks.",
        "A fixture uses real seafarers, scores an operational incident, rewards unsafe challenge behavior, omits fatigue or harm monitoring, breaks matched budgets or blinding, or claims effectiveness.",
        "safe_now_proxy_protocol_no_people",
        "x2_proxy_protocol",
        ["S06", "S07"],
        ["thos/maritime-bridge-protocol.json", "thos/challenge-response-proxy-vectors.json"],
        "Synthetic vectors may pass, but THOS remains represented until preregistered blind matched-budget real arms, authorized participants or operators, safety monitoring, appropriate statistics, and independent review exist.",
        "Retain the synthetic schedule and failures, void promoted comparisons, and require competent maritime, workplace, ethics, statistics, and affected-party processes outside the repository.",
        ["participants", "operator_safety", "maritime_authority", "deployment", "effectiveness", "independent_review"],
        "represented",
        "Prior THOS titles cover crossover, handover, alarms, fatigue, learning, response shift, and many estimands; none centers maritime bridge-team challenge-response and authority gradients under matched budgets.",
    ),
    proposal(
        5,
        "Freed ID key-attestation, hardware-binding, and attestation-downgrade profile",
        "OpenID4VCI key attestation, attested key set, storage claims, user-authentication claims, freshness, proof binding, trust source, downgrade refusal, minimization, and synthetic nonproduction",
        "A synthetic profile can reject untyped, stale, unbound, overbroad, or downgraded key-attestation claims without asserting that hardware or a trust chain is real.",
        "A vector accepts alg none, an empty or mismatched attested-key set, stale freshness, unsupported storage claims, self-declared certification as trust, proof-key mismatch, real secret material, or production assurance wording.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["S08", "S09"],
        ["freed-id/key-attestation-profile.json", "freed-id/key-attestation-mutation-vectors.json"],
        "Synthetic vectors must reject type, algorithm, freshness, key-set, proof-binding, storage-claim, trust-source, privacy, and downgrade failures; real assurance remains externally gated.",
        "Reject the synthetic transaction, retain the vector, disclose no real key or device data, and restore the strictest declared policy.",
        ["real_keys", "hardware_assurance", "production_identity", "interoperability", "privacy_review", "trust_governance"],
        "represented",
        "Prior Freed ID titles cover proof purpose, holder binding, status, issuance, federation, verifier attestation, and wallet flows; none makes OpenID4VCI key-attestation storage claims and downgrade refusal the central surface.",
    ),
    proposal(
        6,
        "CBR fisheries-observer data, quota-sanction separation, customary harvest, and Maori-authority reservation matrix",
        "observer data purpose, employment and safety, compliance use, quota sanction separation, customary harvest, collective data governance, affected parties, remedy, legal interpretation, and Maori authority",
        "A refusal-first matrix can expose unresolved purpose, disclosure, sanction, remedy, customary-harvest, governance, and authority questions without deciding a fishery case or appropriating Maori authority.",
        "The matrix identifies a real observer or vessel, treats observer data as a sanction finding, interprets fisheries law, decides customary rights, asserts Maori authority, reallocates quota, or prescribes remedy.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["S10", "S11", "S12", "S13"],
        ["cbr/fisheries-authority-reservation.json", "cbr/observer-customary-harvest-matrix.md"],
        "Only competent fisheries, employment, safety, privacy, legal, affected-party, tangata whenua, and Maori authorities can close their respective gates; repository software must stop at unknown or reserved.",
        "Stop before any case conclusion, preserve refusals and unknowns, minimize data, and route only through authorized processes outside the repository.",
        ["fisheries_authority", "observer_privacy", "affected_party_authority", "maori_authority", "legal_interpretation", "remedy_decision"],
        "exact_gate",
        "Earlier CBR titles cover general authority, remedy funds, protected disclosure, utilities, cadastral change, museums, and aviation occurrences; none addresses fisheries-observer purpose separation and customary-harvest authority together.",
    ),
    proposal(
        7,
        "Offline Git bundle prerequisite graph, thin-object refusal, and advertised-ref closure tribunal",
        "Git bundle headers, prerequisites, advertised references, object closure, thin-pack refusal, recipient inventory, verification, disposable repositories, and recovery",
        "A disposable local tribunal can verify advertised refs and prerequisite closure before a bundle receives evidence credit.",
        "A recipient lacks a prerequisite, a hidden or unadvertised tip receives credit, a thin or incomplete object set passes, a bundle mutates a sibling lane, or bounded verification is called exhaustive security.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["S14", "S15"],
        ["security/git-bundle-contract.json", "security/git-bundle-mutation-vectors.json"],
        "Disposable fixtures must cover complete, missing-prerequisite, unadvertised-ref, and malformed-header cases without touching another worktree or remote.",
        "Discard only the disposable fixture, retain its manifest and failure, and keep production-migration and exhaustive-security claims false.",
        ["destructive_filesystem", "sibling_lane", "remote_mutation", "exhaustive_security"],
        "completed",
        "Prior Git tribunals cover filters, replacements, partial clone, configuration, submodules, LFS, index stages, and pack indexes; none centers offline bundle prerequisites and advertised-ref closure.",
    ),
    proposal(
        8,
        "Details-summary disclosure, expanded-state, and print-linearization static-report audit",
        "HTML details and summary semantics, open state, accessible name, grouping, hidden content, keyboard reservation, print visibility, and linearized report order",
        "A structural audit can flag missing summaries, nested interactive names, ambiguous grouped disclosures, and print-hidden evidence while reserving manual behavior evaluation.",
        "The audit accepts a details element without a usable summary, nested interactive ambiguity, contradictory open state, evidence omitted from print, inferred keyboard success, or complete-accessibility wording.",
        "safe_now_structural_only",
        "x2_build_task",
        ["S16", "S17"],
        ["accessibility/disclosure-contract.json", "accessibility/details-summary-audit.json"],
        "Generated positive and negative fixtures must cover summary presence, interactive nesting, grouping, state, print linearization, and boundary language while manual assistive-technology and affected-user evaluation remain reserved.",
        "Restore a semantic summary and printable evidence order, retain each failure, and request qualified manual and affected-user evaluation for broader conclusions.",
        ["complete_accessibility", "manual_keyboard_evaluation", "assistive_technology", "affected_user_acceptance"],
        "completed",
        "Earlier accessibility titles cover landmarks, tables, forms, language, links, figures, focus, color, time, maps, generated content, and inert subtrees; none centers details-summary state and print linearization.",
    ),
    proposal(
        9,
        "Clausius inequality, cyclic heat integral, and psyche-justice nonconversion classifier",
        "cyclic thermodynamic path, signed heat transfer, reservoir temperature, reversible equality case, irreversible inequality, dimensional typing, and psyche category barrier",
        "A typed synthetic classifier can evaluate a declared cyclic Clausius inequality while rejecting conversion of thermodynamic irreversibility into psychological or social justice claims.",
        "The classifier drops sign conventions, accepts nonpositive absolute temperature, treats a noncycle as a cycle, asserts equality for an irreversible fixture, maps the integral to fairness or justice, or calls synthetic rows participant evidence.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["S19"],
        ["thermo-psyche/clausius-contract.json", "thermo-psyche/cyclic-integral-mutation-vectors.json"],
        "Fixtures must enforce path closure, heat sign, positive temperature, reversible-case declarations, inequality direction, units, and the psyche-justice nonconversion barrier.",
        "Quarantine the analogy, restore dimensioned heat, temperature, sign, and path declarations, retain failures, and require independent validated social constructs for any human inference.",
        ["participant_inference", "social_justice_claim", "empirical_psychology", "fundamental_law", "consciousness"],
        "completed",
        "The chain covers entropy categories, fluctuation relations, detailed balance, exergy, response, heat capacity, thermodynamic length, and uncertainty relations; no prior title centers the cyclic Clausius integral or justice nonconversion.",
    ),
    proposal(
        10,
        "Stage 20 positive-control, negative-control, and validator-calibration nonpromotion board",
        "known-pass control, known-fail control, mutation sensitivity, validator calibration, false acceptance, false rejection, retained controls, evidence credit, and terminal abstention",
        "A fail-closed board can withhold validator evidence credit unless bounded positive and negative controls behave as preregistered.",
        "A known-pass control fails, a known-fail control passes, controls are changed after outcomes, calibration drift is ignored, failed controls are erased, or Stage 20 advances despite open external gates.",
        "safe_now_structural_only",
        "x2_build_task",
        ["S20", "S21"],
        ["stage20/control-calibration-contract.json", "stage20/control-mutation-vectors.json"],
        "Mutations must reject failed positive or negative controls, post-outcome control edits, unrecorded calibration drift, erased failures, and Stage 20 promotion.",
        "Withdraw only unsupported validator credit, preserve the run and controls, repair and rerun bounded checks when appropriate, and abstain.",
        ["independent_reproduction", "authority_substitution", "proof_or_canon", "stage20_promotion", "history_rewrite"],
        "completed",
        "Earlier Stage 20 boards cover contradiction, expiry, independence, multiplicity, budgets, analytic choice, stopping, tamper challenge, Goodhart, e-values, common cause, and carry-forward; none requires paired validator controls as a calibration gate.",
    ),
]


SOURCES = [
    {"source_id": "S01", "title": "GHC Family Method Flow State schema and runner", "authority": "family-current local skill", "url": None, "status": "current", "checked_on": "2026-07-16", "use": "append-only method records, witnesses, transitions, privacy, and truth boundaries"},
    {"source_id": "S02", "title": "Scalar and tensor gravitational waves", "authority": "Dalang, Fleury, and Lombriser primary research", "url": "https://arxiv.org/abs/2009.11827", "status": "stable", "checked_on": "2026-07-16", "use": "eikonal scalar-tensor propagation and mode separation only"},
    {"source_id": "S03", "title": "Eikonal quasinormal modes beyond general relativity II", "authority": "Silva and Glampedakis primary research", "url": "https://arxiv.org/abs/1912.09286", "status": "stable", "checked_on": "2026-07-16", "use": "coupled scalar-tensor eikonal ordering and mode obligations only"},
    {"source_id": "S04", "title": "EHT Data Products", "authority": "Event Horizon Telescope Collaboration", "url": "https://eventhorizontelescope.org/for-astronomers/data", "status": "current", "checked_on": "2026-07-16", "use": "public release inventory and provenance; zero rows ingested"},
    {"source_id": "S05", "title": "First M87 EHT Results III: Data Processing and Calibration", "authority": "Event Horizon Telescope Collaboration primary research", "url": "https://arxiv.org/abs/1906.11240", "status": "stable", "checked_on": "2026-07-16", "use": "calibration and visibility-product obligations; no likelihood"},
    {"source_id": "S06", "title": "Bridge Resource Management, 2023 Edition", "authority": "International Maritime Organization", "url": "https://www.imo.org/en/publications/pages/currentpublications.aspx", "status": "current", "checked_on": "2026-07-16", "use": "bounded maritime practice context, never competence or authority"},
    {"source_id": "S07", "title": "HTW 12 STCW review gap compilation", "authority": "International Maritime Organization", "url": "https://wwwcdn.imo.org/localresources/en/MediaCentre/Documents/HTW%2012-6.pdf", "status": "draft", "checked_on": "2026-07-16", "use": "watchkeeping and human-element review context only"},
    {"source_id": "S08", "title": "OpenID for Verifiable Credential Issuance 1.0", "authority": "OpenID Foundation", "url": "https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html", "status": "current", "checked_on": "2026-07-16", "use": "key-attestation structure and proof-binding requirements"},
    {"source_id": "S09", "title": "OpenID4VC High Assurance Interoperability Profile 1.0", "authority": "OpenID Foundation", "url": "https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-final.html", "status": "current", "checked_on": "2026-07-16", "use": "profile-level key-attestation expectations; no assurance certification"},
    {"source_id": "S10", "title": "Fisheries observer services", "authority": "Fisheries New Zealand, Ministry for Primary Industries", "url": "https://www.mpi.govt.nz/fishing-aquaculture/commercial-fishing/operating-as-a-commercial-fisher/fisheries-observer-services", "status": "current", "checked_on": "2026-07-16", "use": "observer role and data-purpose context; no case authority"},
    {"source_id": "S11", "title": "Review of bullying and harassment of fisheries observers", "authority": "Ministry for Primary Industries", "url": "https://www.mpi.govt.nz/fishing-aquaculture/commercial-fishing/operating-as-a-commercial-fisher/fisheries-observer-services/review-of-bullying-and-harassment-of-fisheries-observers-and-supervisors", "status": "current", "checked_on": "2026-07-16", "use": "worker-safety and use-separation questions only"},
    {"source_id": "S12", "title": "Maori customary fishing information and resources", "authority": "Fisheries New Zealand, Ministry for Primary Industries", "url": "https://www.mpi.govt.nz/fishing-aquaculture/maori-customary-fishing/maori-customary-fishing-information-and-resources", "status": "current", "checked_on": "2026-07-16", "use": "authority reservation and legal-context questions; never delegated Maori authority"},
    {"source_id": "S13", "title": "Principles of Maori Data Sovereignty", "authority": "Te Mana Raraunga Maori Data Sovereignty Network", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "current", "checked_on": "2026-07-16", "use": "data-governance reservation; never delegated authority"},
    {"source_id": "S14", "title": "git-bundle documentation", "authority": "Git project", "url": "https://git-scm.com/docs/git-bundle", "status": "current", "checked_on": "2026-07-16", "use": "bundle creation, verification, refs, and prerequisites"},
    {"source_id": "S15", "title": "Git bundle format", "authority": "Git project", "url": "https://git-scm.com/docs/bundle-format", "status": "current", "checked_on": "2026-07-16", "use": "header, prerequisite, reference, and pack structure"},
    {"source_id": "S16", "title": "HTML Standard: interactive elements", "authority": "WHATWG", "url": "https://html.spec.whatwg.org/multipage/interactive-elements.html", "status": "current", "checked_on": "2026-07-16", "use": "details, summary, open state, grouping, and structural semantics"},
    {"source_id": "S17", "title": "Web Content Accessibility Guidelines 2.2", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/WCAG22/", "status": "stable", "checked_on": "2026-07-16", "use": "structural accessibility criteria with manual evaluation reserved"},
    {"source_id": "S18", "title": "GHC Family Index routing and closeout guidance", "authority": "family-current local skill", "url": None, "status": "current", "checked_on": "2026-07-16", "use": "tool selection, route states, family naming, and closeout boundaries"},
    {"source_id": "S19", "title": "Clausius inequality in phenomenological thermodynamics", "authority": "primary scholarly source", "url": "https://link.aps.org/accepted/10.1103/PhysRevB.93.224305", "status": "stable", "checked_on": "2026-07-16", "use": "cyclic inequality and reversible equality boundary only"},
    {"source_id": "S20", "title": "Control glossary entry", "authority": "United States National Institute of Standards and Technology", "url": "https://www.nist.gov/glossary-term/36276", "status": "current", "checked_on": "2026-07-16", "use": "positive and negative control distinction"},
    {"source_id": "S21", "title": "Software Verification and Validation Part I and II", "authority": "United States National Institute of Standards and Technology", "url": "https://www.nist.gov/pml/owm/software-verification-and-validation-part-i-ii", "status": "current", "checked_on": "2026-07-16", "use": "bounded software validation and ongoing evaluation context"},
    {"source_id": "S22", "title": "Codex CLI 0.144.4 release", "authority": "OpenAI", "url": "https://github.com/openai/codex/releases/tag/rust-v0.144.4", "status": "current", "checked_on": "2026-07-16", "use": "installed CLI version correlation only; no update action"},
]


def packet(number: int, title: str, kind: str) -> dict[str, Any]:
    prefix = "SAFE" if kind == "safe" else "CANDIDATE"
    return {
        "packet_id": f"V6456-{prefix}-{number:02d}",
        "owner": OWNER,
        "origin_phase": PHASE,
        "origin": "new_orin_portfolio",
        "title": title,
        "approval_class": "safe_now_owner_scoped" if kind == "safe" else "bounded_candidate_prototype",
        "hypothesis": f"A bounded owner-scoped implementation of {title.casefold()} can yield an auditable structural witness without crossing protected gates.",
        "null_or_failure": "The artifact or witness is missing, a failure is erased, a private or authority boundary is crossed, or a structural result is overstated.",
        "artifact": f"portfolios/{kind}/{kind}-{number:02d}.json",
        "acceptance_gate": "A phase-local runner must produce a passing witness, retain every failed assumption, and keep protected external gates open.",
        "rollback_or_recovery": "Retain the negative, restore the last bounded owner state, and reclassify unavailable evidence or authority as open_gap or exact_gate.",
        "protected_gates": ["private_material", "sibling_lane", "real_data_or_participants", "authority", "independent_reproduction", "stage20_promotion"],
        "x2_execution": "preregistered_for_bounded_execution",
        "completion_credit": "none_until_v645_v6_x2_witness",
        "novelty": "New Orin-owned v645-v6 surface; inherited evidence receives no Orin completion credit.",
    }


SAFE_NOW_TITLES = [
    "Rollback-witness and side-effect-budget integrity checker",
    "Three-hundred-sixty-title mission-falsifier novelty explainer",
    "Current primary-source status and use-boundary verifier",
    "Eikonal order and coupled-mode inventory checker",
    "EHT shadow zero-row and likelihood-nonclaim guard",
    "Maritime challenge-response matched-budget protocol checker",
    "Key-attestation type freshness and proof-binding minimizer",
    "Fisheries observer purpose and authority refusal worksheet",
    "Git bundle prerequisite and advertised-ref fixture builder",
    "Details-summary and print-linearization structural auditor",
    "Clausius cycle typing and psyche-justice barrier checker",
    "Validator control-calibration nonpromotion gate",
    "Append-only rollback-event transition checker",
    "Inherited plus external negative preservation checker",
    "Open-gap and exact-gate freshness verifier",
    "Named-lane exact-final replay preflight contract",
    "Five-class phase-blob privacy scanner",
    "Commit-local three-manifest parity verifier",
    "Orin-generated footprint threshold counter",
    "One-baton claim and privacy-boundary linter",
]
SAFE_NOW = [packet(i, title, "safe") for i, title in enumerate(SAFE_NOW_TITLES, 1)]

CANDIDATE_TITLES = [
    "Rollback side-effect graph renderer",
    "Coupled-mode caustic mutation explorer",
    "EHT visibility schema-only adapter prototype",
    "Maritime watch challenge-response schedule generator",
    "Key-attestation downgrade mutation fuzzer",
    "Fisheries purpose-separation unknown-state renderer",
    "Git bundle prerequisite graph visualizer",
    "Disclosure-state print mutation generator",
    "Clausius cyclic-integral boundary explorer",
    "Validator-control drift dashboard",
    "Evidence-scope and authority-reservation matrix renderer",
    "Method rollback recurrence-cluster reporter",
]
CANDIDATES = [packet(i, title, "candidate") for i, title in enumerate(CANDIDATE_TITLES, 1)]

SKILLS = [
    ("ghc-family-witness-rollback-budgets", "Require bounded rollback and side-effect witnesses before method promotion."),
    ("ghc-family-audit-v6456-novelty", "Audit exact, token, mission, falsifier, evidence, and recovery novelty against 360 frozen proposals."),
    ("ghc-family-screen-eikonal-transport", "Check eikonal order, coupled modes, caustics, gauge boundaries, and nonpromotion."),
    ("ghc-family-reserve-eht-shadow-data", "Keep the EHT adapter at zero rows and zero likelihood until exact evidence exists."),
    ("ghc-family-preregister-maritime-thos", "Check bridge-team challenge-response, budgets, safety, and participant reservations."),
    ("ghc-family-profile-key-attestations", "Test synthetic key-attestation binding, freshness, trust, privacy, and downgrade refusal."),
    ("ghc-family-reserve-fisheries-authority", "Keep observer data, customary harvest, legal, remedy, and Maori gates under authority."),
    ("ghc-family-test-git-bundles", "Test disposable Git bundle prerequisite and advertised-ref closure vectors."),
    ("ghc-family-audit-disclosure-structure", "Audit details-summary state and print linearization while reserving human evaluation."),
    ("ghc-family-classify-clausius-cycles", "Check cyclic heat-integral assumptions and block psyche-justice conversion."),
    ("ghc-family-calibrate-stage20-controls", "Reject validator credit when positive or negative controls fail."),
    ("ghc-family-preserve-v6456-negatives", "Validate inherited, synthetic, operational, and failed-witness retention."),
]

RUNNERS = [
    ("ghc_family_v645_v6_portfolio_runner.py", "Execute every Orin safe-now and bounded candidate packet with owner witnesses."),
    ("ghc_family_v645_v6_core_runner.py", "Execute the ten bounded core proposal surfaces and retain truth labels."),
    ("ghc_family_v645_v6_skill_runner.py", "Build, validate, register, and invoke every v645-v6 phase skill."),
    ("ghc_family_v645_v6_boundary_runner.py", "Exercise Git, accessibility, identity, authority, thermo, and control boundaries."),
    ("ghc_family_v645_v6_method_flow_runner.py", "Validate and append Method Flow failures, passes, rollback budgets, and guards."),
    ("ghc_family_v645_v6_validation_runner.py", "Run scoped tests, JSON, privacy, manifests, ancestry, exact-head, and equality checks."),
]

CLEAN_TITLES = [
    "Canonicalize Orin v645-v6 generated bytes to UTF-8 LF",
    "Lint Orin v645-v6 published paths against private-location leakage",
    "Measure per-document word ceilings with explicit exceptions prohibited",
    "Measure overview page-equivalent density without padding",
    "Reject any v645-v6 disposition outside the frozen four-class vocabulary",
    "Reject any v645-v6 source status outside the family four-state vocabulary",
    "Demonstrate Orin portfolio title and mission distinctness from predecessor portfolios",
    "Quarantine predecessor portfolio completion credit from Orin outcomes",
    "Validate trigger and protected-gate declarations across every proposed Orin skill",
    "Cross-link each Orin runner registration to one actual execution witness",
    "Record the Sandbox elevation gate as unchanged host-state evidence",
    "Qualify structural accessibility findings and reserve human evaluation",
    "Label canonical and named replays as same-owner shared-infrastructure evidence",
    "Force the v645-v6 terminal board to abstain while external gates remain",
    "Diff the inherited ten exact and five blocked packets for meaning preservation",
    "Reconcile repository, external, synthetic, and current operational negative classes",
    "Reconcile inherited and current gate counts without closure inference",
    "Measure only v645-v6 owner additions against the rotation threshold",
    "Prove the x1 tree lacks phase-truth and x2 outcome artifacts",
    "Block route SENT state until exact-final replay and remote equality",
]


def clean_task(number: int, title: str) -> dict[str, Any]:
    return {
        "task_id": f"V6456-CLEAN-{number:02d}",
        "owner": OWNER,
        "origin": "new_orin_task",
        "title": title,
        "destructive": False,
        "execution": "preregistered_owner_scoped_safe_now",
        "acceptance": "Emit a bounded x2 receipt, preserve failures, and make no destructive or authority-crossing change.",
        "rollback": "Restore the last owner-scoped generated artifact and retain the failed witness.",
    }


CLEAN_TASKS = [clean_task(i, title) for i, title in enumerate(CLEAN_TITLES, 1)]
