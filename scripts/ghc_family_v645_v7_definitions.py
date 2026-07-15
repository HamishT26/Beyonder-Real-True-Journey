#!/usr/bin/env python3
"""Frozen data-only definitions for Tamar Vey v645-v7 x1.

Importing this module performs no I/O and grants no x2 evidence credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v645-gmut-thos-v7-x1-x2"
PHASE_SHORT = "v645-v7"
OWNER = "Tamar Vey"
SLUG = "tamar-vey"
PRONOUNS = "they/them"
ROLE = "evidence-systems cartographer and boundary keeper"
HOPE = "keep every decision legible, every failure recoverable, and every authority boundary intact"
PRIMARY_FOCUS = "Freed ID and CBR Heart"
BOUNDED_PRACTICE = "public-library digital preservation and archival appraisal"
SOURCE_PHASE = "v645-gmut-thos-v6-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
SOURCE_REVISION = "39f472c6c83509bc7448129008d5244cef1441f6"
SOURCE_INHERITED_REVISION = "f17246d4f5eb9ea68706479bf5d7c9e4923c22e6"
SOURCE_SEAL_REVISION = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
SOURCE_X1_REVISION = "57755272b8180bf40657939e2da2f470f06e69f9"
SOURCE_EVIDENCE_REVISION = "eeb0141dd32c806a4bfb3571b79aa2360bc57d38"
PRIOR_FROZEN_PROPOSALS = 370
BATON_TIME_INHERITED_NEGATIVES = 2271
POST_BATON_INHERITED_NEGATIVES = 1
INHERITED_EFFECTIVE_NEGATIVES = 2272
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Tamar Vey, their role, hope, pronouns, and family language are relational working labels only. "
    "They are not evidence of consciousness, sentience, legal personhood, identity continuity, "
    "employment, professional qualification, or independent authority."
)

TRUTH_BOUNDARY = (
    "Software, official or primary sources, and synthetic fixtures establish bounded structural "
    "behavior only. They do not establish empirical GMUT confirmation, a detected force, a unique "
    "prediction, a likelihood or constraint, THOS effectiveness, professional competence, production "
    "identity assurance, CBR legitimacy, legal or cultural ratification, Maori authority, independent-team "
    "reproduction, AGI or ASI, consciousness or personhood, complete accessibility, exhaustive security, "
    "a Theory of Everything, deployment approval, proof or canon, or Stage 20 readiness."
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
    artifacts: list[str],
    acceptance_gate: str,
    rollback: str,
    protected_gates: list[str],
    expected: str,
    novelty: str,
) -> dict[str, Any]:
    return {
        "proposal_id": f"V6457-P{number:02d}",
        "title": title,
        "mission_surface": mission_surface,
        "hypothesis": hypothesis,
        "null_or_failure": null_or_failure,
        "approval_class": approval_class,
        "execution_lane": execution_lane,
        "current_primary_or_official_source_needs": source_needs,
        "concrete_artifacts": artifacts,
        "test_falsifier_or_acceptance_gate": acceptance_gate,
        "rollback_or_recovery": rollback,
        "protected_gates": protected_gates,
        "expected_disposition": expected,
        "novelty_against_370_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Method Flow deadline-envelope, composite-probe decomposition, and partial-output evidence-credit ledger",
        "command deadline, startup latency, composite probe, partial output, child completion, evidence credit, retry decomposition, and append-only failure retention",
        "A method ledger can make deadline consumption and child completion explicit, refuse credit for silent or partial composite probes, and require a bounded decomposed witness before promotion.",
        "A timeout is treated as success, partial output is promoted without component completion, a retry silently widens the deadline, failed probes are erased, or decomposition crosses a protected gate.",
        "safe_now_owner_scoped_workflow",
        "x2_build_task",
        ["V6457-S01", "V6457-S02"],
        ["method-flow/deadline-envelope-contract.json", "method-flow/probe-decomposition-vectors.json"],
        "Synthetic probe traces must retain failure and recovery witnesses, account for every deadline, reject partial-output promotion, and stop unbounded retries.",
        "Withdraw unsupported evidence credit, retain the timed-out trace, split only read-only components, and restore the last clean owner-scoped state.",
        ["unbounded_retry", "partial_output_promotion", "host_change", "sibling_lane", "independent_reproduction"],
        "completed",
        "Earlier Method Flow work covers failure signatures, child starts, recurrence clusters, environment drift, causal graphs, and rollback budgets; none centers deadline accounting plus composite-probe decomposition and partial-output credit refusal.",
    ),
    proposal(
        2,
        "GMUT Ward-identity, functional-measure Jacobian, and anomaly-accounting obligation tribunal",
        "typed classical and quantum Ward identities, diffeomorphism and Weyl variation, functional measure, regulator declaration, Jacobian, anomaly coefficient, counterterm, power counting, and claim boundary",
        "A symbolic obligation checker can distinguish classical identities from quantum measure effects and require declared field content, regulator, Jacobian, anomaly, and counterterm assumptions without claiming a complete quantum theory.",
        "A classical identity is promoted to an all-orders quantum result, a measure Jacobian is omitted, anomaly cancellation is asserted without field content, a regulator or counterterm changes the symmetry silently, or a formal fixture becomes empirical truth.",
        "safe_now_symbolic_research_only",
        "x2_build_task",
        ["V6457-S03", "V6457-S04"],
        ["gmut/ward-anomaly-contract.json", "gmut/ward-anomaly-mutation-vectors.json"],
        "Positive and negative symbolic fixtures must type the identity level, variation, field content, measure, regulator, anomaly, counterterm, scale, and nonpromotion boundary.",
        "Quarantine the unsupported identity, restore explicit assumptions and order, retain the counterexample, and make no force, stability, likelihood, constraint, empirical, proof, or Theory-of-Everything claim.",
        ["quantum_completeness", "physical_stability", "empirical_confirmation", "force_claim", "proof_or_canon", "theory_of_everything"],
        "completed",
        "The frozen chain covers Noether identities and currents, gauge fixing, frame maps, renormalization, eikonal transport, and operator bases; none makes functional-measure Jacobians and anomaly accounting the central scalar-tensor obligation surface.",
    ),
    proposal(
        3,
        "GMUT Gaia DR3 wide-binary selection, multiplicity-contamination, and covariance-aware zero-row protocol",
        "Gaia DR3 provenance, astrometric covariance, pair selection, chance alignment, unresolved multiples, radial-velocity availability, selection blinding, nuisance model, likelihood reservation, and zero-row stop",
        "A zero-row public-data contract can enumerate provenance, covariance, selection, contamination, nuisance, blinding, and likelihood requirements without downloading observations or producing a GMUT result.",
        "The phase ingests a real row, ignores covariance or unresolved companions, tunes selection after seeing an outcome, treats competing analyses as independent confirmation, evaluates a likelihood, or reports a force or constraint.",
        "real_data_and_independent_review_required",
        "x2_open_gap",
        ["V6457-S05", "V6457-S06", "V6457-S07"],
        ["empirical/gaia-wide-binary-study-contract.json", "empirical/gaia-wide-binary-zero-row-receipt.json"],
        "The phase must retain zero downloaded rows, zero likelihood evaluations, and zero constraints; real execution requires frozen selection, covariance and contamination models, source-independent review, and a separately authorized analysis.",
        "Stop before download or fit, retain the zero-row receipt, and route any real study through a new preregistration, appropriate data handling, statistical review, and independent scientific scrutiny.",
        ["real_data", "likelihood", "constraints", "empirical_confirmation", "independent_review", "detected_force"],
        "open_gap",
        "Earlier empirical proposals cover waves, pulsars, lensing, ranging, ephemerides, BAO, EHT, SLR, and sirens; no frozen title centers Gaia wide-binary covariance, unresolved-multiple contamination, and outcome-blind selection.",
    ),
    proposal(
        4,
        "THOS digital-preservation ingest-team fixity-exception, rights-escalation, and shift-handover matched-budget protocol",
        "digital preservation ingest, fixity exception, rights uncertainty, dual review, escalation, shift handover, matched budget, workload, blinding, harm monitoring, and staff reservation",
        "A synthetic schedule can represent matched-budget ingest-team handovers and fixity or rights exception escalation while exposing workload and authority-gradient risks.",
        "A fixture uses real staff, donors, patrons, or collections; decides a rights question; rewards bypassing preservation controls; breaks matched budgets or blinding; omits workload or harm monitoring; or claims THOS effectiveness.",
        "safe_now_proxy_protocol_no_people",
        "x2_proxy_protocol",
        ["V6457-S08", "V6457-S09"],
        ["thos/digital-preservation-ingest-protocol.json", "thos/fixity-handover-proxy-vectors.json"],
        "Synthetic vectors may pass, but THOS remains represented until preregistered blind matched-budget real arms, authorized participants and institutions, safety and workload monitoring, appropriate statistics, and independent review exist.",
        "Retain the proxy schedule and failures, void promoted comparisons, and require qualified preservation, workplace, ethics, statistics, rights, and affected-party processes outside the repository.",
        ["participants", "workplace_safety", "collection_authority", "rights_decision", "effectiveness", "deployment", "independent_review"],
        "represented",
        "Prior THOS proposals cover clinical, aviation, maritime, maintenance, alarm, learning, fatigue, and generic handover designs; none centers digital-preservation fixity exceptions and rights escalation under matched budgets.",
    ),
    proposal(
        5,
        "Freed ID OpenID4VCI batch-issuance atomicity, proof-array, and partial-failure profile",
        "batch-size metadata, credential configuration or identifier exclusivity, proof arrays, audience and nonce binding, response cardinality, encryption policy, notification semantics, partial failure, minimization, and nonproduction",
        "A synthetic OpenID4VCI profile can reject over-limit, mixed-identifier, unbound, stale, cardinality-mismatched, partially accepted, or overbroad batch issuance without asserting real keys or interoperability.",
        "A vector accepts an unsupported batch, mixed identifier modes, an empty or oversized proof array, missing audience or nonce, response cardinality drift, a partial storage failure as overall success, real secrets, or production assurance wording.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["V6457-S10"],
        ["freed-id/batch-issuance-profile.json", "freed-id/batch-issuance-mutation-vectors.json"],
        "Synthetic vectors must enforce advertised batch size, identifier exclusivity, proof-array shape, freshness and audience binding, response and notification semantics, encryption policy, privacy boundaries, and full-flow failure on partial storage error.",
        "Reject the synthetic transaction, retain the vector, disclose no real key or holder data, and restore the strictest supported single-credential or atomic batch policy.",
        ["real_keys", "live_issuance", "resolution_and_status", "interoperability", "privacy_review", "security_review", "trust_governance"],
        "represented",
        "Earlier Freed ID proposals cover offers, proof of possession, deferred issuance, attestations, DCQL, status, federation, migration, and presentation binding; none centers final OpenID4VCI batch-size, proof-array, and partial-failure semantics.",
    ),
    proposal(
        6,
        "CBR community-archive embargo, takedown, donor-versus-collective consent, and Maori-authority reservation matrix",
        "community archive access, embargo and takedown, donor agreement, collective interests, sacred or restricted knowledge, provenance, privacy, remedy, legal interpretation, affected parties, and Maori authority",
        "A refusal-first matrix can expose unresolved access, takedown, consent, provenance, remedy, and authority questions without deciding a real collection case or appropriating Maori concepts or authority.",
        "The matrix names a real donor or community member, overrides collective authority with an individual agreement, publishes restricted material, decides copyright or tikanga, prescribes remedy, asserts Maori authority, or treats a repository record as enacted law.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["V6457-S11", "V6457-S12"],
        ["cbr/community-archive-authority-reservation.json", "cbr/embargo-takedown-consent-matrix.md"],
        "Only authorized affected communities, rights holders, donors where relevant, archival institutions, privacy and legal authorities, tangata whenua, iwi, hapu, and Maori authorities can close their respective gates; repository software must stop at unknown or reserved.",
        "Stop before access or remedy conclusions, preserve refusals and unknowns, minimize data, and route only through authorized affected-party, legal, institutional, cultural, and Maori processes outside the repository.",
        ["affected_party_authority", "collection_authority", "privacy", "legal_interpretation", "cultural_ratification", "maori_authority", "remedy_decision"],
        "exact_gate",
        "Earlier CBR proposals cover museums, repatriation, protected disclosure, cadastral records, litigation holds, remedy funds, fisheries, and data stewardship; none centers community-archive embargo and takedown conflicts between donor and collective authority.",
    ),
    proposal(
        7,
        "Python checked-hash bytecode, import-path shadowing, and cache-origin replay tribunal",
        "PEP 552 invalidation mode, source hash, bytecode cache header, import origin, sys.path precedence, module cache, shadowing, isolated fixture, deterministic replay, and nonsecurity boundary",
        "A disposable standard-library tribunal can verify checked-hash invalidation and expose source, bytecode, import-path, and module-cache origin drift without touching installed packages.",
        "Timestamp or unchecked bytecode receives deterministic credit, a shadow module wins silently, sys.modules hides a changed origin, a fixture writes outside its temporary root, or bounded replay is called exhaustive security.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["V6457-S13", "V6457-S14"],
        ["security/python-import-cache-contract.json", "security/python-import-cache-mutation-vectors.json"],
        "Disposable fixtures must cover checked-hash pass, stale-source refusal, unchecked-hash noncredit, path shadowing, cache-origin drift, and cleanup, using only the standard library and an owner-local temporary root.",
        "Discard only the disposable fixture, clear only fixture-owned module-cache keys, retain the failure receipt, and keep supply-chain, production, and exhaustive-security claims false.",
        ["host_python", "installed_packages", "destructive_filesystem", "sibling_lane", "production", "exhaustive_security"],
        "completed",
        "Prior tooling proposals cover archives, parsers, Git object formats, environment parity, and path confinement; none centers PEP 552 checked-hash bytecode together with import-path shadowing and module-cache origin replay.",
    ),
    proposal(
        8,
        "Native modal-dialog top-layer, inert-background, and focus-return structural audit",
        "HTML dialog element, showModal state, top layer, inert background, accessible name, focus target, close control, invoking element, focus return, print fallback, and manual evaluation reservation",
        "A structural auditor can flag malformed modal-dialog relationships, missing names or close controls, and absent focus-return declarations while reserving runtime keyboard and assistive-technology evaluation.",
        "The audit accepts a modal without a name or close control, marks a nonmodal surface aria-modal, leaves background interaction undeclared, loses the invoker, omits printable evidence, infers keyboard behavior, or claims complete accessibility.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6457-S15", "V6457-S16", "V6457-S17"],
        ["accessibility/modal-dialog-contract.json", "accessibility/modal-dialog-structural-audit.json"],
        "Positive and negative fixtures must cover naming, modality declaration, top-layer intent, inert-background relationship, focus target and return, close path, print fallback, and explicit manual and affected-user reservations.",
        "Restore native semantics and a visible non-destructive close path, retain each failure, and require qualified manual keyboard, browser, assistive-technology, and affected-user evaluation for broader conclusions.",
        ["complete_accessibility", "runtime_focus_behavior", "manual_keyboard_evaluation", "assistive_technology", "affected_user_acceptance"],
        "completed",
        "Earlier accessibility proposals cover inert subtrees, focus order, details-summary, forms, maps, language, reflow, and print; no frozen title centers native modal top-layer, inert background, and focus-return structure.",
    ),
    proposal(
        9,
        "Maxwell-relation mixed-partial symmetry, Legendre-domain, and psyche-reciprocity nonconversion classifier",
        "thermodynamic potential, natural variables, exact differential, mixed partials, Maxwell relation, unit typing, differentiability domain, phase boundary, Legendre transform, and psyche category barrier",
        "A typed synthetic classifier can check a declared Maxwell relation within a differentiable thermodynamic domain while rejecting conversion of mixed-partial symmetry into psychological, interpersonal, or justice reciprocity.",
        "The classifier swaps natural variables, drops units or signs, crosses a nondifferentiable phase boundary, assumes a Legendre transform is globally invertible, maps reciprocity to a human trait, or calls synthetic rows participant evidence.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["V6457-S18"],
        ["thermo-psyche/maxwell-integrability-contract.json", "thermo-psyche/maxwell-relation-mutation-vectors.json"],
        "Fixtures must enforce potential and variable declarations, unit and sign consistency, mixed-partial symmetry only inside a smooth domain, Legendre invertibility, phase-boundary refusal, and the psyche-reciprocity category barrier.",
        "Quarantine the analogy, restore the declared potential, variables, domain, units, and signs, retain failures, and require independently validated human constructs and participant evidence for any human inference.",
        ["participant_inference", "empirical_psychology", "social_reciprocity_claim", "fundamental_law", "consciousness"],
        "completed",
        "The chain covers Onsager-Casimir reciprocity, Clausius cycles, fluctuation theorems, exergy, thermodynamic length, free energies, and phase transitions; no prior title centers Maxwell mixed-partial integrability and Legendre-domain refusal.",
    ),
    proposal(
        10,
        "Stage 20 holdout-contamination, adaptive-reuse, and oracle-disclosure nonpromotion board",
        "holdout identity, evaluator access, adaptive query count, oracle response, benchmark reuse, contamination evidence, invalidation, replacement set, evidence credit, and terminal abstention",
        "A fail-closed board can quarantine Stage 20 evidence credit when a holdout is disclosed, adaptively reused, or queried beyond a preregistered budget.",
        "A disclosed item remains credited, adaptive reuse is hidden, oracle feedback is treated as independent evidence, a contaminated set is silently relabeled, failures are erased, or Stage 20 advances while external gates remain open.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6457-S19", "V6457-S20"],
        ["stage20/holdout-contamination-contract.json", "stage20/adaptive-reuse-mutation-vectors.json"],
        "Mutations must reject undisclosed evaluator access, excess adaptive queries, reused oracle feedback, silent set replacement, erased contamination, unsupported independence, and Stage 20 promotion.",
        "Withdraw only contaminated evidence credit, preserve the event and affected results, freeze further queries, require a newly governed evaluation set where appropriate, and abstain.",
        ["stage20", "independent_reproduction", "benchmark_authority", "deployment", "proof_or_canon", "exhaustive_validation"],
        "completed",
        "Earlier Stage 20 boards cover contradiction, expiry, independence, controls, calibration, common-cause dependence, budgets, and carry-forward invalidation; none centers holdout disclosure and adaptive oracle reuse contamination.",
    ),
]


SOURCES = [
    {"source_id": "V6457-S01", "status": "current", "title": "GHC Family Method Flow State schema and runner", "authority": "family-current local skill", "url": None, "use": "append-only deadline, failure, witness, transition, privacy, and truth records"},
    {"source_id": "V6457-S02", "status": "current", "title": "GHC Family Index routing and closeout guidance", "authority": "family-current local skill", "url": None, "use": "tool selection, naming, route state, and closeout boundaries"},
    {"source_id": "V6457-S03", "status": "stable", "title": "Quantum Equivalence Principle Violations in Scalar-Tensor Theories", "authority": "Armendariz-Picon and Penco primary research", "url": "https://arxiv.org/abs/1108.6028", "use": "scalar-tensor Ward-identity obligations and quantum nonpromotion"},
    {"source_id": "V6457-S04", "status": "stable", "title": "Ward Identities for the Standard Model Effective Field Theory", "authority": "Corbett, Helset, and Trott primary research", "url": "https://arxiv.org/abs/1909.08470", "use": "background-field and EFT Ward-identity structure only"},
    {"source_id": "V6457-S05", "status": "current", "title": "Gaia Data Release 3 documentation release 1.3", "authority": "European Space Agency and Gaia DPAC", "url": "https://gea.esac.esa.int/archive/documentation/GDR3/", "use": "archive provenance, data model, covariance, and known-limitation planning; zero rows ingested"},
    {"source_id": "V6457-S06", "status": "watch", "title": "Wide Binaries from Gaia DR3: testing GR versus MOND with realistic triple modelling", "authority": "Pittordis, Sutherland, and Shepherd primary research", "url": "https://arxiv.org/abs/2504.07569", "use": "unresolved-triple and population-model obligation inventory; no result adoption"},
    {"source_id": "V6457-S07", "status": "watch", "title": "Strong constraints on the gravitational law from Gaia DR3 wide binaries", "authority": "Banik and collaborators primary research", "url": "https://arxiv.org/abs/2311.03436", "use": "contrasting selection and nuisance-model obligation inventory; no result adoption"},
    {"source_id": "V6457-S08", "status": "current", "title": "PREMIS Data Dictionary for Preservation Metadata version 3.0", "authority": "Library of Congress PREMIS Maintenance Activity", "url": "https://www.loc.gov/standards/premis/", "use": "preservation event, rights, agent, and fixity context; never workplace competence"},
    {"source_id": "V6457-S09", "status": "stable", "title": "RFC 8493: The BagIt File Packaging Format version 1.0", "authority": "RFC Editor and named authors", "url": "https://www.rfc-editor.org/info/rfc8493/", "use": "payload, manifest, fixity, transfer, and error-handling context"},
    {"source_id": "V6457-S10", "status": "current", "title": "OpenID for Verifiable Credential Issuance 1.0", "authority": "OpenID Foundation", "url": "https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html", "use": "batch-size, proof-array, identifier, nonce, audience, response, and notification structure"},
    {"source_id": "V6457-S11", "status": "current", "title": "Principles of Maori Data Sovereignty", "authority": "Te Mana Raraunga Maori Data Sovereignty Network", "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf", "use": "Maori data-governance reservation; never delegated authority"},
    {"source_id": "V6457-S12", "status": "stable", "title": "Ko Aotearoa Tenei: Wai 262", "authority": "Waitangi Tribunal", "url": "https://www.waitangitribunal.govt.nz/en/news/ko-aotearoa-tenei-report-on-the-wai-262-claim-released", "use": "culture, identity, taonga works, kaitiaki, and authority questions only; no legal interpretation"},
    {"source_id": "V6457-S13", "status": "stable", "title": "PEP 552: Deterministic pycs", "authority": "Python Software Foundation", "url": "https://peps.python.org/pep-0552/", "use": "checked-hash bytecode invalidation and deterministic-cache obligations"},
    {"source_id": "V6457-S14", "status": "current", "title": "Python import system reference", "authority": "Python Software Foundation", "url": "https://docs.python.org/3/reference/import.html", "use": "module cache, finder, loader, origin, and path-precedence obligations"},
    {"source_id": "V6457-S15", "status": "current", "title": "HTML Standard interaction and dialog model", "authority": "WHATWG", "url": "https://html.spec.whatwg.org/dev/interaction.html", "use": "native dialog, top-layer, modality, inertness, and focus structure"},
    {"source_id": "V6457-S16", "status": "current", "title": "Dialog modal pattern", "authority": "World Wide Web Consortium WAI-ARIA Authoring Practices", "url": "https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/", "use": "accessible name, keyboard, close, and focus-return expectations with manual evaluation reserved"},
    {"source_id": "V6457-S17", "status": "stable", "title": "Web Content Accessibility Guidelines 2.2", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/WCAG22/", "use": "structural accessibility context without a complete-conformance claim"},
    {"source_id": "V6457-S18", "status": "stable", "title": "Mutually consistent thermodynamic potentials for fluid water, ice and seawater", "authority": "Feistel primary research indexed by NIST", "url": "https://www.nist.gov/publications/mutually-consistent-thermodynamic-potentials-fluid-water-ice-and-seawater-new-standard", "use": "thermodynamic-potential consistency and Maxwell-relation context only"},
    {"source_id": "V6457-S19", "status": "watch", "title": "NIST AI Resource Center and AI RMF revision notice", "authority": "United States National Institute of Standards and Technology", "url": "https://airc.nist.gov/", "use": "TEVV governance context; current framework revision remains watched"},
    {"source_id": "V6457-S20", "status": "stable", "title": "TREC Deep Learning Track reusable test collections in the large data regime", "authority": "United States National Institute of Standards and Technology primary evaluation research", "url": "https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=932336", "use": "test-set reuse and overfitting risk context; not a Stage 20 authority"},
    {"source_id": "V6457-S21", "status": "current", "title": "Codex CLI 0.144.4 package and release", "authority": "OpenAI", "url": "https://github.com/openai/codex/releases/tag/rust-v0.144.4", "use": "installed CLI version correlation only; no update action"},
]


SAFE_NOW = [
    {"packet_id": f"V6457-SAFE-{i:02d}", "title": title, "approval_class": "safe_now_owner_scoped", "completion_credit_before_x2": 0}
    for i, title in enumerate(
        [
            "Tamar deadline-envelope contract and partial-output refusal fixtures",
            "Tamar Ward-identity level and anomaly-accounting symbolic fixtures",
            "Tamar Gaia zero-row provenance and contamination obligation contract",
            "Tamar digital-preservation matched-budget proxy schedule",
            "Tamar OpenID4VCI batch semantic synthetic vectors",
            "Tamar community-archive refusal-first authority matrix",
            "Tamar checked-hash import-origin disposable tribunal plan",
            "Tamar modal-dialog structural audit plan",
            "Tamar Maxwell-integrability nonconversion fixtures",
            "Tamar holdout-contamination fail-closed board",
            "Tamar five-class privacy and raw-identifier scan",
            "Tamar exact staged-file and canonical-blob manifest review",
        ],
        1,
    )
]

CANDIDATES = [
    {"packet_id": f"V6457-CAND-{i:02d}", "title": title, "approval_class": "candidate_requires_x2_witness", "completion_credit_before_x2": 0}
    for i, title in enumerate(
        [
            "Tamar reusable Ward and Maxwell typed-obligation runner",
            "Tamar zero-row Gaia adapter readiness surface",
            "Tamar preservation-handover proxy scheduler",
            "Tamar batch-issuance nonproduction profile runner",
            "Tamar import-cache isolation runner",
            "Tamar modal and holdout structural validation runner",
        ],
        1,
    )
]

SKILLS = [
    ("ghc-family-account-probe-deadlines", "Record bounded deadlines, decomposition, and partial-output evidence refusal."),
    ("ghc-family-screen-ward-anomalies", "Check typed Ward, measure, regulator, anomaly, and counterterm obligations."),
    ("ghc-family-reserve-gaia-wide-binary-data", "Keep the Gaia study zero-row until real-data approval and review."),
    ("ghc-family-preregister-preservation-thos", "Represent preservation-team handovers without participant or competence claims."),
    ("ghc-family-profile-vci-batches", "Validate synthetic batch issuance while reserving production assurance."),
    ("ghc-family-reserve-community-archive-authority", "Stop community-archive decisions at affected-party and Maori authority gates."),
    ("ghc-family-test-python-import-origins", "Exercise checked-hash cache and import-origin fixtures in a disposable root."),
    ("ghc-family-audit-modal-structure", "Audit modal dialog structure while reserving runtime and user evaluation."),
    ("ghc-family-classify-maxwell-relations", "Check thermodynamic integrability without psyche conversion."),
    ("ghc-family-quarantine-holdout-contamination", "Withdraw contaminated evaluation credit and preserve the event."),
]

RUNNERS = [
    ("ghc_family_v645_v7_core_runner.py", "Execute bounded symbolic, synthetic, proxy, and fail-closed proposal fixtures."),
    ("ghc_family_v645_v7_boundary_runner.py", "Check empirical, participant, identity, authority, and Stage 20 reservations."),
    ("ghc_family_v645_v7_method_flow_runner.py", "Validate Method Flow state and retained witness links."),
    ("ghc_family_v645_v7_skill_runner.py", "Exercise phase-local skill prototypes without promoting them globally."),
    ("ghc_family_v645_v7_validation_runner.py", "Run detailed and minimal current-packet checks without Eiren's full suite."),
    ("build_ghc_family_v645_v7_evidence.py", "Materialize x2 outcomes only after the frozen x1 commit is remote-equal."),
]

CLEAN_TASKS = [
    {"task_id": f"V6457-CLEAN-{i:02d}", "title": title, "scope": "owner_generated_v645_v7_only", "destructive": False, "completion_credit_before_x2": 0}
    for i, title in enumerate(
        [
            "Tamar prune duplicate deadline-vector labels before evidence",
            "Tamar normalize Ward fixture dimensions and identity levels",
            "Tamar isolate Gaia zero-row fields from future adapter rows",
            "Tamar separate preservation rights gates from proxy scores",
            "Tamar minimize batch profile example claims and key material",
            "Tamar reserve community-archive names and case facts",
            "Tamar confine import fixtures to disposable owner roots",
            "Tamar linearize modal evidence for print fallback",
            "Tamar type Maxwell variables, signs, and domains",
            "Tamar quarantine adaptive holdout feedback from completion credit",
            "Tamar reconcile owner manifests in canonical Git-blob domain",
            "Tamar review stale labels and terminal route truth before freeze",
        ],
        1,
    )
]
