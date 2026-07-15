"""Frozen Sable Rook v645-v5 preregistration definitions.

This module contains x1 intent only. Importing it performs no repository writes.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from ghc_family_v645_v4_definitions import (
    INHERITED_BLOCKED_PACKETS as SOURCE_BLOCKED_PACKETS,
    INHERITED_EXACT_PACKETS as SOURCE_EXACT_PACKETS,
)

PHASE = "v645-gmut-thos-v5-x1-x2"
OWNER = "Sable Rook"
SOURCE_PHASE = "v645-gmut-thos-v4-x1-x2"
SOURCE_REVISION = "3e0f37ec230252776e89841f12aa31b18dc21808"
SOURCE_SEAL_REVISION = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
SOURCE_X1_REVISION = "a0c2cdfac1fee23c2f5318a148f80198d251efc6"
SOURCE_EVIDENCE_REVISION = "f7508d831736a884b4b765d54c1e3265dbb8b599"
INHERITED_EFFECTIVE_NEGATIVES = 2087
PRIOR_FROZEN_PROPOSALS = 350
PRIMARY_FOCUS = "THOS Body"
BOUNDED_PRACTICE = "aviation maintenance occurrence investigation and human-factors review"

IDENTITY_BOUNDARY = (
    "Sable Rook, they/them, is relational working language for an evidence-and-"
    "reproducibility steward. It is not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, professional qualification, or "
    "independent authority."
)

HOPE = (
    "Every retained negative stays findable, and every surviving claim remains "
    "reproducible enough to challenge or retract."
)

TRUTH_BOUNDARY = (
    "Software, official or primary sources, and synthetic fixtures establish only "
    "bounded structural behavior. They do not establish empirical GMUT confirmation, "
    "a likelihood result, THOS effectiveness, aviation competence, production identity "
    "assurance, CBR legitimacy, Maori authority, legal or cultural ratification, "
    "independent-team reproduction, AGI or ASI, consciousness or personhood, complete "
    "accessibility, exhaustive security, a Theory of Everything, or Stage 20 readiness."
)

OUTCOME_CLASSES = ["completed", "represented", "open_gap", "exact_gate"]


def proposal(
    number: int,
    title: str,
    mission_surface: str,
    hypothesis: str,
    null_or_failure: str,
    approval_class: str,
    execution_lane: str,
    sources: list[str],
    deliverables: list[str],
    gate: str,
    rollback: str,
    protected: list[str],
    disposition: str,
    novelty: str,
) -> dict[str, Any]:
    return {
        "proposal_id": f"V6455-P{number:02d}",
        "title": title,
        "mission_surface": mission_surface,
        "hypothesis": hypothesis,
        "null_or_failure": null_or_failure,
        "approval_class": approval_class,
        "execution_lane": execution_lane,
        "authoritative_source_needs": sources,
        "deliverables": deliverables,
        "test_falsifier_or_gate": gate,
        "rollback_or_recovery": rollback,
        "protected_gates": protected,
        "expected_disposition": disposition,
        "novelty_against_prior_chain": novelty,
    }


PROPOSALS = [
    proposal(
        1,
        "Stable claim-anchor remapping under line movement, content mutation, and split-merge provenance tribunal",
        "claim-bearing text spans, stable anchors, line relocation, content mutation, split and merge history, source independence, and retained counterevidence",
        "A content-aware remapping contract can distinguish a moved claim from a changed, split, merged, or deleted claim while preserving its source and negative-evidence lineage.",
        "A changed claim inherits the old anchor silently, split claims lose parent lineage, deleted counterevidence disappears, or line numbers are treated as stable semantic identity.",
        "safe_now_structural_only",
        "x2_build_task",
        ["S15"],
        ["provenance/claim-anchor-contract.json", "provenance/claim-anchor-mutation-vectors.json"],
        "Mutation vectors must reject silent semantic inheritance, ambiguous split or merge mappings, deleted-negative loss, and false source independence.",
        "Quarantine the ambiguous mapping, retain both versions and every negative, and require manual source-scope review before carry-forward.",
        ["source_independence", "counterevidence_retention", "history_rewrite", "stage20_promotion"],
        "completed",
        "Earlier provenance work covers roots, dependency graphs, transformations, withdrawals, and source overlap, but no frozen title centers stable text-span anchors across line moves and split-merge remapping.",
    ),
    proposal(
        2,
        "GMUT quasi-static ordering, effective-coupling, and gravitational-slip gauge-obligation tribunal",
        "typed scalar-tensor and EFT scaffold, scale hierarchy, time-derivative ordering, effective gravitational coupling, slip parameter, gauge dictionary, stability, and domain reservation",
        "A symbolic tribunal can require every quasi-static reduction to declare its scale ordering, gauge dictionary, denominator domain, stability assumptions, and relation to the unreduced equations.",
        "A fixture drops time derivatives without hierarchy, mixes gauges, accepts a singular denominator, omits stability assumptions, or calls a reduced parameterization a measured force or unique GMUT prediction.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["S03"],
        ["gmut/quasi-static-obligation-contract.json", "gmut/quasi-static-mutation-vectors.json"],
        "At least nine mutation classes must fail closed, including missing hierarchy, gauge mismatch, singular coupling, unstable branch, and empirical overclaim.",
        "Restore the unreduced typed scaffold, retain rejected reductions, and require model-specific analysis plus real observations before promotion.",
        ["empirical_confirmation", "new_force", "unique_prediction", "stability_proof", "theory_of_everything"],
        "completed",
        "Prior titles cover gauge fixing, constraint propagation, screening radii, background growth, and field redefinitions; none combines quasi-static ordering with effective coupling and gravitational-slip gauge obligations.",
    ),
    proposal(
        3,
        "GMUT DESI DR1 BAO window-covariance adapter and blind zero-row likelihood protocol",
        "DESI DR1 BAO measurements, window matrix, covariance, fiducial mapping, scale cuts, nuisance lock, blind analysis, and zero-row promotion barrier",
        "A preregistered adapter can identify the exact public DESI products and typed likelihood inputs needed for a future GMUT comparison while zero real rows and zero likelihood evaluations remain explicit.",
        "The protocol counts a source URL as data, ignores window or covariance structure, changes scale cuts after access, performs an unreviewed likelihood, or reports a constraint from zero rows.",
        "data_and_independent_review_required",
        "x2_empirical_gate",
        ["S01", "S02"],
        ["gmut/desi-bao-study-contract.json", "gmut/desi-bao-zero-row-receipt.json"],
        "Completion requires frozen real-data selection, ingested rows with provenance, window and covariance treatment, a computed likelihood, uncertainty analysis, and independent scientific review; otherwise the result is open_gap.",
        "Preserve the schema and zero-row receipt, run no fit, retain every adapter failure, and reopen only under a separately reviewed real-data protocol.",
        ["real_data", "likelihood_execution", "empirical_confirmation", "independent_review", "theory_of_everything"],
        "open_gap",
        "Earlier empirical titles cover gravitational waves, ranging, lensing, pulsars, ephemerides, ISW, redshift-space distortions, and standard sirens; no prior title names DESI DR1 BAO window-covariance products.",
    ),
    proposal(
        4,
        "THOS maintenance-shift learning-curve, skill-decay, and operator-crossover matched-budget protocol",
        "blind matched-budget arms, maintenance shifts, learning curve, skill decay, operator crossover, procedure exposure, fatigue, harms, and independent review",
        "A synthetic protocol can freeze time-on-task, procedure exposure, operator crossover, learning, decay, fatigue, and safety-monitoring fields before any real THOS comparison.",
        "The protocol treats training exposure as an effect, ignores crossover or fatigue, assigns unequal budgets, substitutes synthetic operators for participants, or claims safety or effectiveness without authorized real arms.",
        "participants_operators_and_independent_review_required",
        "x2_proxy_protocol",
        ["S04", "S05", "S06"],
        ["thos/maintenance-shift-protocol.json", "thos/learning-decay-proxy-vectors.json"],
        "Structural vectors may pass, but THOS remains represented until preregistered blind matched-budget real arms, authorized participants and operators, safety monitoring, statistics, and independent review exist.",
        "Retain the synthetic schedule and failures, void promoted comparisons, and require competent aviation, workplace, ethics, statistical, and affected-party review outside this repository.",
        ["participants", "operator_safety", "aviation_authority", "deployment", "effectiveness", "independent_review"],
        "represented",
        "Earlier THOS titles cover crossover carryover, learning curves, shift handover, alarm load, response shift, and fidelity; none combines maintenance-shift learning, skill decay, operator crossover, and matched budgets.",
    ),
    proposal(
        5,
        "Freed ID verifier-attestation, client-metadata integrity, and policy-source confinement profile",
        "OpenID4VP verifier identity, client metadata, request binding, trust source, policy confinement, selective disclosure, privacy, and synthetic nonproduction failures",
        "A synthetic presentation profile can reject unbound verifier metadata, unsupported trust assertions, policy fetched from an unpinned source, and requests that exceed the declared purpose.",
        "A fixture treats self-asserted metadata as trust, accepts an unbound request, retrieves mutable policy silently, overrequests claims, uses real keys, or calls structural vectors production interoperability.",
        "safe_now_synthetic_nonproduction",
        "x2_proxy_protocol",
        ["S07", "S08", "S09", "S10"],
        ["freed-id/verifier-attestation-profile.json", "freed-id/verifier-metadata-mutation-vectors.json"],
        "Synthetic vectors must reject at least nine verifier, metadata, binding, privacy, and policy-source failures; production remains open without conformant real keys, proofs, live services, interoperability, review, recovery, and trust governance.",
        "Reject the synthetic presentation, retain the vector, restore the pinned policy source, and expose no real credential or account material.",
        ["real_keys", "production_identity", "live_resolution", "status_revocation", "interoperability", "privacy_review", "trust_governance"],
        "represented",
        "Prior titles cover DCQL, browser mediation, issuer sessions, federation chains, proof purpose, status, and holder binding; none centers verifier attestation plus client-metadata integrity and policy-source confinement.",
    ),
    proposal(
        6,
        "CBR aviation-occurrence evidence custody, reporter protection, remedy, and Maori-authority reservation matrix",
        "aviation occurrence records, evidence custody, reporter confidentiality, nonpunitive safety use, remedies, jurisdiction, affected parties, Maori data, and authority refusal",
        "A refusal-first matrix can expose unanswered custody, confidentiality, remedy, jurisdiction, affected-party, and Maori-data questions without deciding an occurrence, assigning blame, or conferring authority.",
        "The matrix makes a safety finding, identifies a reporter, recommends punishment or compensation, interprets law, asserts Maori authority, or treats ICAO or FAA material as delegated case authority.",
        "authorized_affected_parties_and_competent_authority_required",
        "x2_exact_gate",
        ["S04", "S05", "S06", "S14"],
        ["cbr/aviation-occurrence-reservation.json", "cbr/occurrence-remedy-authority-matrix.md"],
        "Only competent investigation, safety, legal, privacy, employment, affected-party, and Maori authorities where applicable can close their respective gates; repository software must stop at unknown or reserved.",
        "Stop before any case conclusion, preserve the refusal and unknowns, minimize data, and route only through authorized processes outside the repository.",
        ["aviation_authority", "reporter_privacy", "affected_party_authority", "maori_authority", "legal_interpretation", "remedy_decision"],
        "exact_gate",
        "Earlier CBR titles cover protected disclosures, remedy funds, museums, utilities, cadastral changes, and evidence holds; none concerns aviation-occurrence custody, reporter protection, remedy, and Maori-data reservation together.",
    ),
    proposal(
        7,
        "ZIP central-directory duplicate, traversal-alias, and extraction-budget security tribunal",
        "ZIP member names, duplicate central-directory entries, parent traversal, separator aliases, Unicode normalization, decompression budget, quarantine, and bounded recovery",
        "A disposable archive tribunal can reject ambiguous duplicate names, traversal aliases, normalization collisions, and declared extraction-budget overruns before materialization.",
        "A fixture writes outside its root, silently selects one duplicate, conflates normalized names, expands beyond budget, mutates the canonical repository, or claims exhaustive archive security.",
        "safe_now_disposable_synthetic_only",
        "x2_build_task",
        ["S12"],
        ["security/zip-extraction-contract.json", "security/zip-extraction-mutation-vectors.json"],
        "Disposable in-memory or owner-temporary fixtures must reject duplicate, traversal, alias, collision, and budget failures without extracting into a sibling or canonical lane.",
        "Discard only the disposable fixture, retain the failing archive manifest, and keep exhaustive-security and untrusted-production processing claims false.",
        ["destructive_filesystem", "sibling_lane", "exhaustive_security", "production_untrusted_input"],
        "completed",
        "Prior titles cover decompression ceilings, archive boundaries, filesystem aliases, and Windows names; none titles ZIP central-directory duplicates together with traversal aliases and an extraction budget.",
    ),
    proposal(
        8,
        "Inert-subtree, hidden-focusable, and keyboard-trap static-report audit",
        "inert and hidden subtrees, focusable descendants, tabindex ordering, keyboard entry and exit, disclosure controls, static report structure, and manual affected-user reservation",
        "A structural audit can flag focusable content inside inert or hidden subtrees, positive tabindex ordering, and disclosure patterns without an evident keyboard exit.",
        "The audit accepts hidden focus targets, a positive tabindex sequence, a disclosure control without an exit path, infers real keyboard behavior from markup alone, or calls structural checks complete accessibility conformance.",
        "safe_now_structural_only",
        "x2_build_task",
        ["S11"],
        ["accessibility/hidden-focus-contract.json", "accessibility/keyboard-boundary-audit.json"],
        "Generated positive and negative fixtures must cover inert descendants, hidden focus targets, tabindex ordering, and disclosure entry or exit while manual keyboard and affected-user evaluation remain reserved.",
        "Remove the hidden focus target or restore a reachable exit, retain each failure, and request qualified manual keyboard and affected-user evaluation for broader conclusions.",
        ["complete_accessibility", "manual_keyboard_evaluation", "affected_user_acceptance", "runtime_behavior"],
        "completed",
        "Prior accessibility titles cover landmarks, focus sequence, links, tables, forms, maps, language, color, and generated content; none titles inert subtrees, hidden focusables, and keyboard-trap boundaries together.",
    ),
    proposal(
        9,
        "Thermodynamic uncertainty-relation, current-variance bound, and psyche-confidence nonconversion classifier",
        "stochastic thermodynamics, integrated current, variance, entropy production, observation time, bound assumptions, finite-sample fixture, and category barrier",
        "A typed synthetic classifier can evaluate a declared thermodynamic uncertainty bound only when current, variance, entropy production, time, and regime assumptions are explicit, while blocking conversion into psychological confidence.",
        "The classifier mixes current and state variables, omits observation time, accepts negative variance, applies an asymptotic bound outside its declared regime, maps precision to psyche confidence, or calls synthetic rows participant evidence.",
        "safe_now_synthetic_only",
        "x2_build_task",
        ["S13"],
        ["thermo-psyche/uncertainty-relation-contract.json", "thermo-psyche/current-variance-mutation-vectors.json"],
        "Positive and negative fixtures must distinguish current from state, enforce nonnegative variance and entropy production, declare time and regime, and reject psyche-confidence conversion.",
        "Quarantine the analogy, restore dimensioned current, variance, time, and entropy production, retain failures, and require separate validated psychological constructs for any human inference.",
        ["participant_inference", "psyche_confidence", "empirical_psychology", "fundamental_law", "consciousness"],
        "completed",
        "The chain covers fluctuation relations, detailed balance, response, thermodynamic length, exergy, and uncertainty in evidence boards; no prior title names a thermodynamic current-variance uncertainty relation or psyche-confidence barrier.",
    ),
    proposal(
        10,
        "Stage 20 cross-version evidence carry-forward, invalidation-trigger, and grandfathering-rejection board",
        "phase version, evidence scope, model and tool revisions, invalidation triggers, retained negatives, authority freshness, grandfathering refusal, and terminal abstention",
        "A fail-closed board can require explicit compatibility witnesses before prior-phase evidence is carried forward and can invalidate credit when model, data, tool, authority, or source scope changes.",
        "Old evidence is grandfathered by ancestry alone, an invalidation trigger is ignored, a failed replay is erased, same-owner continuity becomes independent reproduction, or Stage 20 advances without external gates.",
        "safe_now_structural_only",
        "x2_build_task",
        ["S15", "S16"],
        ["stage20/carry-forward-contract.json", "stage20/invalidation-trigger-vectors.json"],
        "Mutations must reject ancestry-only credit, incompatible tool or model versions, stale authority, missing negatives, and independent-reproduction overclaim; the terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "Withdraw only unsupported carry-forward credit, preserve the historical artifacts and negatives, rerun bounded checks when appropriate, and abstain.",
        ["independent_reproduction", "authority_substitution", "proof_or_canon", "stage20_promotion", "history_rewrite"],
        "completed",
        "Prior boards cover freshness, withdrawal, decision reversal, semantic versions, source retraction, and stop rules; none titles cross-version carry-forward eligibility with invalidation triggers and grandfathering rejection.",
    ),
]


SOURCES = [
    {"source_id": "S01", "title": "DESI data releases overview", "authority": "Dark Energy Spectroscopic Instrument collaboration", "url": "https://data.desi.lbl.gov/doc/releases/", "status": "current", "checked_on": "2026-07-16", "use": "DR1 provenance and public-data availability only"},
    {"source_id": "S02", "title": "DESI DR1 Full Shape and BAO clustering products", "authority": "Dark Energy Spectroscopic Instrument collaboration", "url": "https://data.desi.lbl.gov/doc/releases/dr1/vac/full-shape-bao-clustering/", "status": "current", "checked_on": "2026-07-16", "use": "BAO observable, window, covariance and likelihood-input requirements; no rows ingested"},
    {"source_id": "S03", "title": "Comparison of quasi-static approximations in Horndeski models", "authority": "Pace et al. primary research", "url": "https://arxiv.org/abs/2011.05713", "status": "stable", "checked_on": "2026-07-16", "use": "quasi-static assumptions and validity domain only"},
    {"source_id": "S04", "title": "Human Factors in Aviation Maintenance", "authority": "United States Federal Aviation Administration", "url": "https://www.faa.gov/about/initiatives/maintenance_hf", "status": "current", "checked_on": "2026-07-16", "use": "bounded aviation-maintenance learning context, never professional authority"},
    {"source_id": "S05", "title": "Procedural Non-Compliance in Aviation Maintenance", "authority": "United States Federal Aviation Administration", "url": "https://www.faa.gov/about/initiatives/maintenance_hf/procedural_non-compliance", "status": "current", "checked_on": "2026-07-16", "use": "human-factors and occurrence-review context only"},
    {"source_id": "S06", "title": "Safety data collection and processing systems", "authority": "International Civil Aviation Organization", "url": "https://www.icao.int/safety-management/SMI/SMM/Chapter%205", "status": "current", "checked_on": "2026-07-16", "use": "safety-data integrity and protection context; no delegated case authority"},
    {"source_id": "S07", "title": "OpenID for Verifiable Presentations 1.0", "authority": "OpenID Foundation", "url": "https://openid.net/specs/openid-4-verifiable-presentations-1_0.html", "status": "current", "checked_on": "2026-07-16", "use": "verifier, request, client metadata and presentation protocol requirements"},
    {"source_id": "S08", "title": "Verifiable Credential Data Integrity 1.0", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/vc-data-integrity/", "status": "stable", "checked_on": "2026-07-16", "use": "proof purpose and verification-method structural requirements; no real proof"},
    {"source_id": "S09", "title": "Verifiable Credentials Data Model v2.0", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "stable", "checked_on": "2026-07-16", "use": "credential and presentation model boundary"},
    {"source_id": "S10", "title": "NIST Special Publication 800-63A-4", "authority": "United States National Institute of Standards and Technology", "url": "https://pages.nist.gov/800-63-4/sp800-63a.html", "status": "current", "checked_on": "2026-07-16", "use": "identity evidence and invalidation governance context; no production certification"},
    {"source_id": "S11", "title": "Web Content Accessibility Guidelines 2.2", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/WCAG22/", "status": "stable", "checked_on": "2026-07-16", "use": "link purpose and structural navigation criteria with manual evaluation reserved"},
    {"source_id": "S12", "title": "Python zipfile library documentation", "authority": "Python Software Foundation", "url": "https://docs.python.org/3/library/zipfile.html", "status": "current", "checked_on": "2026-07-16", "use": "bounded disposable ZIP fixture API behavior, not exhaustive archive security"},
    {"source_id": "S13", "title": "Thermodynamic Uncertainty Relation for Biomolecular Processes", "authority": "Barato and Seifert primary research", "url": "https://doi.org/10.1103/PhysRevLett.114.158101", "status": "stable", "checked_on": "2026-07-16", "use": "stochastic-thermodynamic precision and dissipation bound only; no psyche conversion"},
    {"source_id": "S14", "title": "Principles of Maori Data Sovereignty", "authority": "Te Mana Raraunga Maori Data Sovereignty Network", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "current", "checked_on": "2026-07-16", "use": "authority reservation and data-governance boundary; never delegated authority"},
    {"source_id": "S15", "title": "Evidence Management Steering Committee Report", "authority": "NIST and NIJ Evidence Management Steering Committee", "url": "https://www.nist.gov/publications/evidence-management-steering-committee-report-opportunities-strengthen-evidence", "status": "current", "checked_on": "2026-07-16", "use": "retention, preservation, integrity and disposition context"},
    {"source_id": "S16", "title": "Codex CLI 0.144.4 release", "authority": "OpenAI", "url": "https://github.com/openai/codex/releases/tag/rust-v0.144.4", "status": "current", "checked_on": "2026-07-16", "use": "installed CLI currency receipt only; no update instruction"},
]


INHERITED_EXACT_PACKETS = deepcopy(SOURCE_EXACT_PACKETS)
INHERITED_BLOCKED_PACKETS = deepcopy(SOURCE_BLOCKED_PACKETS)


def new_packet(number: int, title: str, kind: str, novelty: str) -> dict[str, Any]:
    return {
        "packet_id": f"V6455-{kind.upper()}-{number:02d}",
        "owner": OWNER,
        "origin_phase": PHASE,
        "origin": "new_sable_proposal",
        "title": title,
        "approval_class": "safe_now_owner_scoped" if kind == "safe" else "bounded_candidate_prototype",
        "hypothesis": f"A bounded owner-scoped implementation of {title.casefold()} can yield an auditable structural witness without crossing protected gates.",
        "null_or_failure": "The artifact or witness is missing, a failure is erased, a private or authority boundary is crossed, or a structural result is overstated.",
        "artifact": f"portfolios/{kind}/{kind}-{number:02d}.json",
        "acceptance_gate": "A phase-local runner must produce a passing witness, retain every failed assumption, and keep protected external gates open.",
        "rollback_or_recovery": "Retain the negative, restore the last bounded state, and reclassify unavailable evidence or authority as open_gap or exact_gate.",
        "protected_gates": ["private_material", "sibling_lane", "real_data_or_participants", "authority", "independent_reproduction", "stage20_promotion"],
        "x2_execution": "preregistered_for_bounded_execution",
        "completion_credit": "none_until_v645_v5_x2_witness",
        "novelty": novelty,
    }


SAFE_NOW_TITLES = [
    "Content-aware claim-anchor remapping validator",
    "Three-hundred-fifty-title mission-surface novelty explainer",
    "Current-source status and checked-date verifier",
    "Quasi-static hierarchy and gauge-obligation matrix checker",
    "DESI BAO zero-row and likelihood-nonclaim guard",
    "Maintenance-shift learning and skill-decay protocol checker",
    "Verifier-attestation metadata and policy-source minimizer",
    "Aviation occurrence authority and confidentiality refusal worksheet",
    "ZIP duplicate and traversal-alias mutation builder",
    "Hidden-focusable and keyboard-boundary structural auditor",
    "Thermodynamic current-variance bound classifier",
    "Cross-version carry-forward invalidation gate",
    "Append-only Method Flow transition integrity checker",
    "Inherited and current negative-count preservation checker",
    "Open-gap and exact-gate nonclosure verifier",
    "Named-lane exact-head replay preflight builder",
    "Five-class owner-blob privacy scanner",
    "Commit-local manifest parity verifier",
    "Sable-generated footprint threshold counter",
    "Terminal baton claim and privacy boundary linter",
]

SAFE_NOW = [
    new_packet(i, title, "safe", "New v645-v5 surface tied to Sable-owned deliverables and not inherited for completion credit.")
    for i, title in enumerate(SAFE_NOW_TITLES, 1)
]

CANDIDATE_TITLES = [
    "Claim-anchor split-merge diff simulator",
    "Quasi-static regime-boundary explorer",
    "DESI HDF5 schema-only adapter prototype",
    "Maintenance learning-decay schedule generator",
    "Verifier metadata mutation fuzzer",
    "Occurrence-record de-identification field classifier",
    "ZIP central-directory ambiguity explorer",
    "Hidden-focusable subtree mutation generator",
    "Thermodynamic current-variance bound explorer",
    "Carry-forward invalidation graph renderer",
    "Evidence-scope and authority-reservation dashboard",
    "Method Flow recurrence-cluster reporter",
]

CANDIDATES = [
    new_packet(i, title, "candidate", "New bounded prototype; no inherited seed or predecessor completion credit.")
    for i, title in enumerate(CANDIDATE_TITLES, 1)
]

SKILLS = [
    ("ghc-family-remap-claim-anchors", "Remap stable claim anchors while preserving semantic-change and negative lineage."),
    ("ghc-family-audit-v6455-novelty", "Audit exact and token-level proposal and portfolio novelty against frozen predecessors."),
    ("ghc-family-screen-quasi-static-obligations", "Check scale ordering, gauge, coupling, stability, and nonpromotion obligations."),
    ("ghc-family-reserve-desi-bao-data", "Keep the DESI BAO adapter at zero rows and zero likelihood until exact evidence exists."),
    ("ghc-family-preregister-maintenance-thos", "Check maintenance-shift learning, decay, crossover, budget, and safety reservations."),
    ("ghc-family-profile-verifier-attestation", "Test verifier metadata binding and policy-source confinement with synthetic vectors."),
    ("ghc-family-reserve-aviation-authority", "Keep occurrence custody, privacy, remedy, legal, and Maori gates under authority."),
    ("ghc-family-test-zip-boundaries", "Test disposable ZIP duplicate, traversal, normalization, and budget vectors."),
    ("ghc-family-audit-hidden-focus", "Audit inert, hidden-focusable, and keyboard-boundary structure while reserving human evaluation."),
    ("ghc-family-classify-thermodynamic-uncertainty", "Check current-variance bound assumptions and block psyche conversion."),
    ("ghc-family-gate-evidence-carry-forward", "Reject cross-version evidence credit without compatibility witnesses."),
    ("ghc-family-preserve-method-failures", "Validate append-only Method Flow failures, recoveries, and recommendations."),
]

RUNNERS = [
    ("ghc_family_v645_v5_portfolio_runner.py", "Execute every Sable safe-now and bounded candidate packet with owner witnesses."),
    ("ghc_family_v645_v5_core_runner.py", "Execute the ten bounded core proposal surfaces and retain truth labels."),
    ("ghc_family_v645_v5_skill_runner.py", "Build, validate, register, and invoke every v645-v5 phase skill."),
    ("ghc_family_v645_v5_boundary_runner.py", "Exercise archive, accessibility, identity, authority, and thermo boundaries."),
    ("ghc_family_v645_v5_method_flow_runner.py", "Validate and append Method Flow methods, failed witnesses, passes, and guards."),
    ("ghc_family_v645_v5_validation_runner.py", "Run scoped tests, JSON, privacy, manifest, ancestry, and exact-head checks."),
]


def new_clean(number: int, title: str) -> dict[str, Any]:
    return {
        "task_id": f"V6455-CLEAN-{number:02d}",
        "owner": OWNER,
        "origin": "new_sable_task",
        "title": title,
        "destructive": False,
        "execution": "preregistered_owner_scoped_safe_now",
        "acceptance": "Emit a bounded x2 receipt, preserve failures, and make no destructive or authority-crossing change.",
        "rollback": "Restore the last owner-scoped generated artifact and retain the failed witness.",
    }


CLEAN_TITLES = [
    "Normalize v645-v5 generated text to UTF-8 with one LF terminator",
    "Keep every v645-v5 path repository-relative and public-safe",
    "Enforce the six-thousand-word cap on each phase document",
    "Enforce a three-page-equivalent integrated overview floor",
    "Restrict core outcomes to the four frozen truth classes",
    "Restrict source statuses to current stable draft or watch",
    "Prove all Sable portfolio titles are exact-distinct from predecessor portfolios",
    "Prove predecessor portfolio completion credit remains zero for Sable",
    "Check every phase skill states trigger scope and protected gates",
    "Check each registered runner has an actual x2 invocation witness",
    "Keep Windows Sandbox unavailable and unlaunched without elevation",
    "Reserve manual assistive-technology and affected-user accessibility review",
    "Keep same-owner named replay distinct from independent-team reproduction",
    "Keep terminal Stage 20 verdict fail-closed",
    "Verify inherited exact and blocked packets are byte-equivalent in meaning",
    "Preserve all inherited and v645-v5 operational negatives",
    "Preserve open gaps and exact gates without silent closure",
    "Check owner-generated file additions remain below fifteen thousand",
    "Check x1 artifacts contain no x2 implementation or outcome credit",
    "Keep terminal route state prepared-not-sent until final replay passes",
]

CLEAN_TASKS = [new_clean(i, title) for i, title in enumerate(CLEAN_TITLES, 1)]
