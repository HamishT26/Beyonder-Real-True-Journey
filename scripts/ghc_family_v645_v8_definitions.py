#!/usr/bin/env python3
"""Frozen data-only definitions for Sylven Arc v645-v8 x1.

Importing this module performs no I/O and grants no x2 evidence credit.
"""

from __future__ import annotations

from typing import Any


PHASE = "v645-gmut-thos-v8-x1-x2"
PHASE_SHORT = "v645-v8"
OWNER = "Sylven Arc"
SLUG = "sylven-arc"
PRONOUNS = "they/them"
ROLE = "constraint-cartographer and falsifier-keeper"
HOPE = "make unresolved boundaries legible without turning uncertainty into authority"
PRIMARY_FOCUS = "GMUT Mind"
BOUNDED_PRACTICE = "railway traffic control and speed-restriction handover"
SOURCE_PHASE = "v645-gmut-thos-v7-x1-x2"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
SOURCE_REVISION = "96cbc8c71defbdfcb3ec58bd445e78e8274e95f7"
SOURCE_INHERITED_REVISION = "39f472c6c83509bc7448129008d5244cef1441f6"
SOURCE_SEAL_REVISION = "96cbc8c71defbdfcb3ec58bd445e78e8274e95f7"
SOURCE_X1_REVISION = "1b2a056b25b4cf91f521eea03cbadfee56a7b41c"
SOURCE_EVIDENCE_REVISION = "f8b28fda63884d0e89ad212d0c2974bbf0e87a63"
PRIOR_FROZEN_PROPOSALS = 380
BATON_TIME_INHERITED_NEGATIVES = 2353
POST_BATON_INHERITED_NEGATIVES = 0
INHERITED_EFFECTIVE_NEGATIVES = 2353
PREREGISTERED_SYNTHETIC_NEGATIVES = 70
OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Sylven Arc, their role, hope, pronouns, and family language are relational working labels only. "
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
        "proposal_id": f"V6458-P{number:02d}",
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
        "novelty_against_380_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Method Flow process-tree cancellation, orphan-child quiescence, and teardown-evidence ledger",
        "parent and child command aliases, declared cancellation scope, timeout, cooperative stop, forced stop reservation, quiescence witness, exit evidence, partial output, and append-only recovery",
        "A method ledger can distinguish parent completion from process-tree quiescence, refuse orphan-child or partial-output credit, and require a bounded teardown witness before a timed-out command is considered recovered.",
        "A parent timeout is treated as full teardown, an unobserved child is assumed gone, captured output is credited before quiescence, a retry creates overlapping children, or termination crosses the owner-scoped process boundary.",
        "safe_now_owner_scoped_workflow",
        "x2_build_task",
        ["V6458-S01", "V6458-S21", "V6458-S22"],
        ["method-flow/process-tree-quiescence-contract.json", "method-flow/teardown-trace-mutation-vectors.json"],
        "Synthetic traces must account for every declared child alias, retain timeout and teardown events, require observed quiescence or a fail-closed unknown, reject overlapping retries, and preserve all partial output as noncompletion evidence.",
        "Withdraw unsupported completion credit, retain the timeout and child-state uncertainty, stop owner-local retries, and resume only through a narrower bounded witness that cannot affect sibling or host processes.",
        ["unbounded_retry", "orphan_process", "destructive_process_action", "sibling_process", "host_change", "independent_reproduction"],
        "completed",
        "Earlier Method Flow proposals cover child starts, deadline envelopes, recurrence clusters, causal graphs, and rollback budgets; none centers cancellation scope plus orphan-child quiescence and teardown evidence before recovery credit.",
    ),
    proposal(
        2,
        "GMUT BRST nilpotency, Slavnov-Taylor hierarchy, and gauge-parameter-independence obligation tribunal",
        "typed fields and antifields, ghost number, BRST differential, nilpotency domain, gauge-fixing fermion, Slavnov-Taylor functional, loop order, anomaly obstruction, on-shell qualification, and claim boundary",
        "A symbolic obligation checker can distinguish a declared nilpotent BRST differential from a loop-order Slavnov-Taylor statement and can require anomaly, regularization, and on-shell qualifications before any gauge-parameter-independence claim.",
        "Ghost numbers are inconsistent, nilpotency is asserted outside its assumptions, the Slavnov-Taylor hierarchy skips an order, a regulator or anomaly obstruction is omitted, on-shell independence becomes an off-shell theorem, or a symbolic fixture becomes physical evidence.",
        "safe_now_symbolic_research_only",
        "x2_build_task",
        ["V6458-S03", "V6458-S04"],
        ["gmut/brst-slavnov-contract.json", "gmut/brst-slavnov-mutation-vectors.json"],
        "Positive and negative fixtures must type fields, ghost numbers, differential action, nilpotency scope, gauge fixing, functional identity, perturbative order, regulator, anomaly status, on-shell condition, and nonpromotion boundary.",
        "Quarantine the unsupported identity, restore explicit field and order declarations, retain the counterexample, and make no quantum-completeness, force, stability, likelihood, empirical, proof, canon, or Theory-of-Everything claim.",
        ["quantum_completeness", "physical_stability", "empirical_confirmation", "force_claim", "proof_or_canon", "theory_of_everything"],
        "completed",
        "The frozen chain covers Noether identities, gauge generators, gauge fixing, Ward anomalies, constraint algebra, and operator bases; none makes BRST nilpotency, the Slavnov-Taylor hierarchy, and qualified gauge-parameter independence the central scalar-tensor obligation surface.",
    ),
    proposal(
        3,
        "GMUT Euclid Q1 shear-product absence, photometric-selection, and covariance-ready zero-row protocol",
        "Euclid Q1 provenance, delivered-product inventory, absent SHE processing, photometric-redshift selection, visibility masks, future shear calibration, covariance, blinding, likelihood reservation, and zero-row stop",
        "A zero-row contract can verify that Q1 does not supply the required shear analysis products, enumerate future selection and covariance obligations, and prevent an imaging catalogue from being promoted into a GMUT weak-lensing result.",
        "The phase ingests a real row, fabricates or infers shear from Q1 imaging, ignores the documented absent processing, tunes selection after an outcome, evaluates a likelihood, reports a constraint or force, or treats public availability as independent reproduction.",
        "real_data_and_independent_review_required",
        "x2_open_gap",
        ["V6458-S05", "V6458-S06", "V6458-S07"],
        ["empirical/euclid-q1-study-contract.json", "empirical/euclid-q1-zero-row-receipt.json"],
        "The phase must retain zero downloaded rows, zero inferred shear values, zero likelihoods, and zero constraints; real execution requires an appropriate released shear product, frozen selection and nuisance models, calibration and covariance review, and separately authorized independent scrutiny.",
        "Stop before archive query or fit, retain the documented product-absence receipt, and route any future real study through a new preregistration, data handling plan, statistical review, and independent scientific review.",
        ["real_data", "shear_inference", "likelihood", "constraints", "empirical_confirmation", "independent_review", "detected_force"],
        "open_gap",
        "Earlier empirical proposals cover lensing, EHT, waves, pulsars, ranging, ephemerides, BAO, SLR, sirens, ISW, and Gaia binaries; none centers Euclid Q1's documented shear-product absence together with photometric selection and covariance-ready refusal.",
    ),
    proposal(
        4,
        "THOS railway speed-restriction communication, control-room handover, and matched-budget proxy protocol",
        "temporary and emergency speed restrictions, source confirmation, readback, route and time scope, control-room handover, matched budget, workload, fatigue, blinding, escalation, and safety reservation",
        "A synthetic schedule can represent matched-budget railway control handovers and speed-restriction communication checks while exposing ambiguity, workload, fatigue, and authority-gradient risks.",
        "A fixture uses real workers, trains, routes, or incidents; issues an operational instruction; rewards bypassing a safety control; omits scope or readback; breaks matched budgets or blinding; hides workload or fatigue; or claims THOS effectiveness.",
        "safe_now_proxy_protocol_no_people",
        "x2_proxy_protocol",
        ["V6458-S08", "V6458-S09"],
        ["thos/rail-restriction-handover-protocol.json", "thos/rail-handover-proxy-vectors.json"],
        "Synthetic vectors may pass, but THOS remains represented until preregistered blind matched-budget real arms, authorized organizations and participants, rail-safety and workplace review, workload and harm monitoring, appropriate statistics, and independent review exist.",
        "Retain the proxy schedule and failures, void promoted comparisons, and require qualified rail operations, safety, human-factors, workplace, ethics, statistics, and affected-party processes outside the repository.",
        ["participants", "rail_safety", "workplace_safety", "operational_instruction", "professional_competence", "effectiveness", "deployment", "independent_review"],
        "represented",
        "Prior THOS proposals cover clinical, aviation, maritime, maintenance, alarm, fatigue, allocation, and preservation handovers; none centers railway speed-restriction communication and control-room handover under matched budgets.",
    ),
    proposal(
        5,
        "Freed ID Bitstring Status List index-allocation, purpose-separation, and herd-privacy profile",
        "status-list index allocation, minimum bitstring length, status purpose, multiple entries, issuer separation, validity interval, caching, stapling, correlation risk, decoys, fetch minimization, and nonproduction",
        "A synthetic Bitstring Status List profile can reject undersized, correlating, purpose-confused, duplicate-index, stale, or overfetching status designs without asserting real issuance, revocation, privacy, or interoperability.",
        "A vector accepts a below-minimum list, unique list per credential, reused index, purpose mismatch, unbounded freshness claim, hidden issuer separation, verifier tracking, real keys or holder data, or production assurance wording.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["V6458-S10", "V6458-S11"],
        ["freed-id/bitstring-status-privacy-profile.json", "freed-id/bitstring-status-mutation-vectors.json"],
        "Synthetic vectors must enforce minimum herd size, noncorrelating allocation, index and purpose consistency, validity and cache policy, issuer disclosure, fetch minimization, stapling boundaries, and fail-closed processing errors.",
        "Reject the synthetic status transaction, retain the vector, disclose no real key or holder data, separate status purposes, and restore the strictest noncorrelating owner-local fixture policy.",
        ["real_keys", "live_issuance", "resolution_and_status", "revocation", "interoperability", "privacy_review", "security_review", "trust_governance"],
        "represented",
        "Earlier Freed ID proposals cover generic status cache age, epoch rollback, revocation windows, batch issuance, offers, presentations, federation, and migration; none centers index allocation, purpose separation, and herd-privacy correlation resistance in the final Bitstring Status List Recommendation.",
    ),
    proposal(
        6,
        "CBR managed-retreat valuation, tenancy, confidentiality, and Maori-land authority reservation matrix",
        "community-led relocation, hazard and option evidence, valuation, owner and tenant interests, affordability, compensation, confidentiality, collective and cultural sites, remedy, legal status, affected parties, and Maori land authority",
        "A refusal-first matrix can expose unresolved valuation, tenancy, confidentiality, compensation, collective-interest, cultural-site, and Maori-land questions without deciding a real relocation, legal status, remedy, or authority issue.",
        "The matrix names a real household, sets a valuation, recommends compulsory relocation, ranks cultural loss, discloses protected information, decides tenancy or compensation law, prescribes remedy, asserts Maori authority, or treats policy material as enacted law.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["V6458-S12", "V6458-S13"],
        ["cbr/managed-retreat-authority-reservation.json", "cbr/retreat-valuation-tenancy-matrix.md"],
        "Only authorized affected people and communities, owners and tenants, relevant institutions, local and central authorities, privacy and legal authorities, tangata whenua, iwi, hapu, and Maori authorities can close their respective gates; software must stop at unknown or reserved.",
        "Stop before relocation, valuation, compensation, disclosure, or remedy conclusions, preserve refusals and unknowns, minimize data, and route only through authorized affected-party, legal, institutional, cultural, and Maori processes outside the repository.",
        ["affected_party_authority", "housing_and_tenancy", "valuation", "privacy", "legal_interpretation", "cultural_ratification", "maori_authority", "remedy_decision"],
        "exact_gate",
        "Earlier CBR proposals cover remedy funds, water hardship, fisheries, archives, museums, cadastral records, litigation holds, aviation evidence, and data stewardship; none centers managed-retreat valuation, tenancy, confidentiality, and Maori-land authority together.",
    ),
    proposal(
        7,
        "Git sparse-index, skip-worktree, cone-pattern, and omitted-path manifest tribunal",
        "disposable repository, sparse checkout, cone mode, sparse directory entry, skip-worktree state, tracked but absent paths, HEAD tree manifest, working-tree omission, vivification, cleanup, and nonsecurity boundary",
        "A disposable Git tribunal can distinguish a tracked path omitted by sparse checkout from a deletion and can require manifests to enumerate canonical HEAD content rather than only populated working-tree paths.",
        "An omitted path is classified as deleted, a working-tree-only manifest is called complete, cone changes go unrecorded, sparse-index state is assumed from absence alone, the fixture touches the canonical repository, or bounded replay is called exhaustive security.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["V6458-S14", "V6458-S15"],
        ["security/git-sparse-index-contract.json", "security/git-sparse-index-mutation-vectors.json"],
        "A disposable no-network fixture must cover cone setup, sparse-index state, tracked omitted paths, canonical-tree manifest parity, skip-worktree evidence, a rejected working-tree-only manifest, and automatic cleanup outside the canonical repository.",
        "Discard only the disposable fixture, retain the failure receipt, rebuild the manifest from the declared Git object domain, and keep production, supply-chain, and exhaustive-security claims false.",
        ["canonical_repository", "destructive_filesystem", "sibling_lane", "remote_change", "production", "exhaustive_security"],
        "completed",
        "Prior Git proposals cover replacement refs, alternate stores, index stages, LFS pointers, object formats, manifests, and borrowed objects; none centers sparse-index directory entries, skip-worktree omissions, cone patterns, and manifest-domain refusal.",
    ),
    proposal(
        8,
        "ARIA live-region politeness, atomicity, and duplicate-announcement structural audit",
        "live-region role, aria-live politeness, aria-atomic, aria-relevant, aria-busy, status versus alert semantics, update ownership, duplicate channels, printable fallback, and manual evaluation reservation",
        "A structural auditor can flag contradictory live-region semantics, missing update ownership, duplicate announcement channels, and unsafe alert promotion while reserving runtime browser and assistive-technology behavior.",
        "The audit accepts duplicate live surfaces for one update, a routine status promoted to alert, invalid politeness, contradictory atomicity, a permanently busy region, missing fallback text, infers actual announcement order, or claims complete accessibility.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6458-S16", "V6458-S17"],
        ["accessibility/live-region-contract.json", "accessibility/live-region-structural-audit.json"],
        "Positive and negative fixtures must cover role and politeness alignment, atomicity, relevance, busy lifecycle, one update owner, duplicate-channel refusal, printable fallback, and explicit manual and affected-user reservations.",
        "Restore the least disruptive semantic role, one declared update owner, stable fallback text, and retain every failure; require qualified browser, keyboard, assistive-technology, language, and affected-user evaluation for broader conclusions.",
        ["complete_accessibility", "runtime_announcement_behavior", "manual_keyboard_evaluation", "assistive_technology", "affected_user_acceptance"],
        "completed",
        "Earlier accessibility work covers form status messages, alerts, inertness, focus, dialogs, maps, language, reflow, and print; no frozen proposal centers live-region politeness, atomicity, busy lifecycle, and duplicate-announcement ownership.",
    ),
    proposal(
        9,
        "Gibbs-Duhem intensive-variable dependency, extensivity-domain, and psyche-autonomy nonconversion classifier",
        "homogeneous thermodynamic potential, extensive variables, intensive variables, composition, phase domain, Gibbs-Duhem constraint, unit typing, degrees of freedom, and psyche category barrier",
        "A typed synthetic classifier can check the Gibbs-Duhem dependency within a declared equilibrium phase and extensivity domain while rejecting conversion of thermodynamic variable dependence into psychological or civic autonomy claims.",
        "The classifier treats all intensive variables as independent, mixes molar and extensive units, crosses phase domains, assumes extensivity where it is undeclared, drops composition, maps dependence to human autonomy, or calls synthetic rows participant evidence.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["V6458-S18"],
        ["thermo-psyche/gibbs-duhem-contract.json", "thermo-psyche/gibbs-duhem-mutation-vectors.json"],
        "Fixtures must enforce potential and phase declarations, extensive and intensive typing, composition and unit consistency, the dependency count only inside an equilibrium extensivity domain, phase-boundary refusal, and the psyche-autonomy category barrier.",
        "Quarantine the analogy, restore the declared phase, variables, units, composition, and extensivity assumptions, retain failures, and require independently validated human constructs and participant evidence for any human inference.",
        ["participant_inference", "empirical_psychology", "human_autonomy_claim", "fundamental_law", "consciousness"],
        "completed",
        "The chain covers chemical potentials, zeroth-law equilibration, Maxwell relations, Onsager reciprocity, free energies, phase transitions, and ensemble limits; no prior title centers Gibbs-Duhem intensive-variable dependency and extensivity-domain refusal.",
    ),
    proposal(
        10,
        "Stage 20 entity-duplication, near-neighbor leakage, and preprocessing-fit quarantine board",
        "entity identity, group-aware split, exact duplicate, near-neighbor threshold, augmentation ancestry, preprocessing fit scope, feature selection, train and evaluation lineage, evidence credit, and terminal abstention",
        "A fail-closed board can quarantine Stage 20 evidence credit when entities or near-neighbors cross evaluation boundaries or preprocessing and feature selection are fit using evaluation information.",
        "A duplicate remains credited, related entities cross splits, augmentation lineage is hidden, a near-neighbor threshold is tuned on evaluation results, preprocessing sees evaluation data, feature selection leaks labels, failures are erased, or Stage 20 advances.",
        "safe_now_structural_only",
        "x2_build_task",
        ["V6458-S19", "V6458-S20"],
        ["stage20/split-leakage-contract.json", "stage20/entity-leakage-mutation-vectors.json"],
        "Mutations must reject exact and near-duplicate cross-split entities, hidden augmentation ancestry, evaluation-fitted preprocessing or feature selection, threshold tuning on outcomes, erased leakage events, unsupported independence, and Stage 20 promotion.",
        "Withdraw only affected evidence credit, preserve the leakage event and lineage, freeze further evaluation use, require a newly governed group-aware split where appropriate, and abstain.",
        ["stage20", "independent_reproduction", "benchmark_authority", "deployment", "proof_or_canon", "exhaustive_validation"],
        "completed",
        "Earlier proposals cover cross-release leakage, generic deduplication, holdout disclosure, adaptive reuse, multiplicity, and carry-forward invalidation; none centers entity-group identity, near-neighbor lineage, and preprocessing-fit isolation as one Stage 20 refusal board.",
    ),
]


SOURCES = [
    {"source_id": "V6458-S01", "status": "current", "title": "GHC Family Method Flow State schema and runner", "authority": "family-current local skill", "url": None, "use": "append-only cancellation, failure, witness, transition, privacy, and recovery records"},
    {"source_id": "V6458-S02", "status": "current", "title": "GHC Family Index routing and closeout guidance", "authority": "family-current local skill", "url": None, "use": "tool selection, ownership, route state, naming, and closeout boundaries"},
    {"source_id": "V6458-S03", "status": "stable", "title": "The Cosmological Slavnov-Taylor Identity from BRST Symmetry in Single-Field Inflation", "authority": "Binosi and Quadri primary research", "url": "https://arxiv.org/abs/1511.09309", "use": "BRST and Slavnov-Taylor obligation structure in a gravity and scalar setting only"},
    {"source_id": "V6458-S04", "status": "stable", "title": "Slavnov-Taylor Identities for Primordial Perturbations", "authority": "Berezhiani and Khoury primary research", "url": "https://arxiv.org/abs/1309.4461", "use": "hierarchy, analyticity, and assumption inventory without result adoption"},
    {"source_id": "V6458-S05", "status": "stable", "title": "Euclid Explanatory Supplement Data Release Q1 documentation release 1", "authority": "European Space Agency and Euclid Consortium", "url": "https://euclid.esac.esa.int/dr/q1/expsup/master.html", "use": "Q1 provenance and delivered-product inventory; zero rows ingested"},
    {"source_id": "V6458-S06", "status": "stable", "title": "Euclid Q1 photometric-redshift processing introduction", "authority": "European Space Agency Euclid Science Ground Segment", "url": "https://euclid.esac.esa.int/dr/q1/dpdd/phzdpd/phzintro.html", "use": "document that SHE processing was omitted for Q1 and reserve shear inference"},
    {"source_id": "V6458-S07", "status": "stable", "title": "Euclid Q1 LE3 data-product introduction", "authority": "European Space Agency Euclid Science Ground Segment", "url": "https://euclid.esac.esa.int/dr/q1/dpdd/le3dpd/le3intro.html", "use": "selection-function and covariance-ready product planning without likelihood execution"},
    {"source_id": "V6458-S08", "status": "current", "title": "Summary of learning 11: Overspeeding version 1 June 2026", "authority": "United Kingdom Rail Accident Investigation Branch", "url": "https://www.gov.uk/government/publications/summary-of-learning-11-overspeeding-v1-june-2026/summary-of-learning-11-overspeeding-v1-june-2026", "use": "speed-restriction communication and handover risk context; never operational instruction"},
    {"source_id": "V6458-S09", "status": "current", "title": "Working patterns and fatigue guidance", "authority": "United Kingdom Office of Rail and Road", "url": "https://www.orr.gov.uk/guidance-compliance/rail/health-safety/strategy/human-factors/working-hours-fatigue", "use": "workload and fatigue reservation for synthetic protocol design only"},
    {"source_id": "V6458-S10", "status": "current", "title": "Bitstring Status List version 1.0", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/vc-bitstring-status-list/", "use": "minimum length, index, purpose, validity, caching, stapling, and privacy obligations"},
    {"source_id": "V6458-S11", "status": "current", "title": "Verifiable Credentials Data Model version 2.0", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "use": "credential and status data-model context without production assurance"},
    {"source_id": "V6458-S12", "status": "watch", "title": "Managed retreat", "authority": "Aotearoa New Zealand Ministry for the Environment", "url": "https://environment.govt.nz/what-government-is-doing/areas-of-work/climate-change/adapting-to-climate-change/managed-retreat/", "use": "relocation, community, cost, Maori-land, and policy questions only; no legal interpretation"},
    {"source_id": "V6458-S13", "status": "stable", "title": "Principles of Maori Data Sovereignty", "authority": "Te Mana Raraunga Maori Data Sovereignty Network", "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf", "use": "Maori data-governance and confidentiality reservation; never delegated authority"},
    {"source_id": "V6458-S14", "status": "current", "title": "Git sparse-checkout documentation", "authority": "Git project", "url": "https://git-scm.com/docs/sparse-checkout", "use": "cone mode, skip-worktree, sparse specification, tracked omission, and behavior boundaries"},
    {"source_id": "V6458-S15", "status": "current", "title": "Git sparse-index documentation", "authority": "Git project", "url": "https://git-scm.com/docs/sparse-index.html", "use": "sparse directory entries, index domain, and compatibility obligations"},
    {"source_id": "V6458-S16", "status": "stable", "title": "Accessible Rich Internet Applications version 1.2", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/wai-aria-1.2/", "use": "live-region roles, politeness, atomicity, relevance, and busy semantics"},
    {"source_id": "V6458-S17", "status": "stable", "title": "Understanding WCAG 2.2 status messages", "authority": "World Wide Web Consortium Web Accessibility Initiative", "url": "https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html", "use": "status-message intent with manual and affected-user evaluation reserved"},
    {"source_id": "V6458-S18", "status": "current", "title": "Gibbs-Duhem equation in the IUPAC Gold Book fifth edition", "authority": "International Union of Pure and Applied Chemistry", "url": "https://goldbook.iupac.org/terms/view/15329", "use": "intensive-variable dependency and phase-domain context only"},
    {"source_id": "V6458-S19", "status": "stable", "title": "Deduplicating Training Data Makes Language Models Better", "authority": "Lee and collaborators primary research", "url": "https://arxiv.org/abs/2107.06499", "use": "near-duplicate and train-test overlap risk inventory; no model result adoption"},
    {"source_id": "V6458-S20", "status": "stable", "title": "Do We Train on Test Data: Purging CIFAR of Near-Duplicates", "authority": "Barz and Denzler primary research", "url": "https://arxiv.org/abs/1902.00423", "use": "entity duplication and evaluation-bias obligation inventory"},
    {"source_id": "V6458-S21", "status": "current", "title": "Python subprocess management documentation", "authority": "Python Software Foundation", "url": "https://docs.python.org/3/library/subprocess.html", "use": "timeout, child completion, captured output, and cleanup semantics"},
    {"source_id": "V6458-S22", "status": "current", "title": "Windows Job Objects", "authority": "Microsoft", "url": "https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects", "use": "process-tree scope and quiescence boundaries; no host process action"},
    {"source_id": "V6458-S23", "status": "current", "title": "Codex CLI 0.144.4 package and release", "authority": "OpenAI", "url": "https://github.com/openai/codex/releases/tag/rust-v0.144.4", "use": "installed CLI version correlation only; no update action"},
]


SAFE_NOW = [
    {"packet_id": f"V6458-SAFE-{i:02d}", "title": title, "approval_class": "safe_now_owner_scoped", "completion_credit_before_x2": 0}
    for i, title in enumerate(
        [
            "Sylven process-tree quiescence and teardown refusal fixtures",
            "Sylven BRST and Slavnov-Taylor typed-obligation fixtures",
            "Sylven Euclid Q1 product-absence zero-row contract",
            "Sylven railway restriction-handover matched-budget proxy",
            "Sylven Bitstring Status List herd-privacy vectors",
            "Sylven managed-retreat refusal-first authority matrix",
            "Sylven sparse-index omitted-path disposable tribunal plan",
            "Sylven live-region duplicate-announcement structural audit plan",
            "Sylven Gibbs-Duhem nonconversion fixtures",
            "Sylven split-leakage fail-closed board",
            "Sylven five-class privacy and raw-identifier scan",
            "Sylven exact staged-file and canonical-blob manifest review",
        ],
        1,
    )
]

CANDIDATES = [
    {"packet_id": f"V6458-CAND-{i:02d}", "title": title, "approval_class": "candidate_requires_x2_witness", "completion_credit_before_x2": 0}
    for i, title in enumerate(
        [
            "Sylven reusable BRST and Gibbs-Duhem typed-obligation runner",
            "Sylven Euclid product-absence adapter readiness surface",
            "Sylven railway restriction-handover proxy scheduler",
            "Sylven Bitstring Status List privacy profile runner",
            "Sylven sparse-index manifest-domain runner",
            "Sylven live-region and split-leakage structural validation runner",
        ],
        1,
    )
]

SKILLS = [
    ("ghc-family-account-process-tree-quiescence", "Record bounded cancellation, child quiescence, teardown, and partial-output refusal."),
    ("ghc-family-screen-brst-identities", "Check typed BRST, ghost-number, Slavnov-Taylor, anomaly, and gauge-dependence obligations."),
    ("ghc-family-reserve-euclid-shear-data", "Keep the Euclid Q1 study zero-row while required shear products and review are absent."),
    ("ghc-family-preregister-rail-handover-thos", "Represent railway restriction handovers without participant, safety, or competence claims."),
    ("ghc-family-profile-bitstring-status-privacy", "Validate synthetic status-list allocation while reserving production assurance."),
    ("ghc-family-reserve-managed-retreat-authority", "Stop relocation and remedy decisions at affected-party and Maori authority gates."),
    ("ghc-family-test-sparse-index-manifests", "Exercise sparse-index omission and canonical-tree manifests in a disposable repository."),
    ("ghc-family-audit-live-region-structure", "Audit live-region structure while reserving runtime and affected-user evaluation."),
    ("ghc-family-classify-gibbs-duhem", "Check thermodynamic dependency without psyche-autonomy conversion."),
    ("ghc-family-quarantine-split-leakage", "Withdraw duplicate or preprocessing-leaked evidence credit and preserve lineage."),
]

RUNNERS = [
    ("ghc_family_v645_v8_core_runner.py", "Execute bounded symbolic, synthetic, proxy, disposable, and fail-closed proposal fixtures."),
    ("ghc_family_v645_v8_boundary_runner.py", "Check empirical, participant, professional, identity, authority, and Stage 20 reservations."),
    ("ghc_family_v645_v8_method_flow_runner.py", "Validate Method Flow state and retained failed-witness links."),
    ("ghc_family_v645_v8_skill_runner.py", "Exercise phase-local skill prototypes without promoting them globally."),
    ("ghc_family_v645_v8_validation_runner.py", "Run bounded recent-round and current-packet checks without Eiren's full suite."),
    ("build_ghc_family_v645_v8_evidence.py", "Materialize x2 outcomes only after the frozen x1 commit is remote-equal."),
]

CLEAN_TASKS = [
    {"task_id": f"V6458-CLEAN-{i:02d}", "title": title, "scope": "owner_generated_v645_v8_only", "destructive": False, "completion_credit_before_x2": 0}
    for i, title in enumerate(
        [
            "Sylven separate parent exit from process-tree quiescence labels",
            "Sylven normalize BRST ghost numbers and perturbative orders",
            "Sylven isolate Euclid product absence from future adapter rows",
            "Sylven separate rail safety gates from proxy schedule scores",
            "Sylven minimize status-list example claims and holder data",
            "Sylven reserve managed-retreat household and case facts",
            "Sylven confine sparse-index fixtures to disposable owner roots",
            "Sylven linearize live-region evidence for print fallback",
            "Sylven type Gibbs-Duhem phases, units, and dependency domains",
            "Sylven quarantine split leakage from completion credit",
            "Sylven reconcile owner manifests in canonical Git-blob domain",
            "Sylven review stale labels and terminal route truth before freeze",
        ],
        1,
    )
]
