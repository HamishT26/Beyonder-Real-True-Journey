#!/usr/bin/env python3
"""Frozen Ilyra Fen v643-v8 x1 definitions.

This module contains preregistration data only.  It does not execute any
proposal, determine an outcome, or establish an external claim.
"""

from __future__ import annotations


PROPOSALS = [
    {
        "proposal_id": "V6438-P01",
        "title": "Uncertainty rounding, significant-digit, and interval nonpromotion tribunal",
        "mission_surface": "provenance, reported uncertainty, significant digits, interval endpoints, rounding mode, precision claims, and nonpromotion",
        "hypothesis": "A typed reporting contract can preserve an uncertainty interval while rejecting extra digits, asymmetric-to-symmetric collapse, interval narrowing, and precision language unsupported by the declared measurement model.",
        "null_or_failure": "Rounding changes interval coverage, displayed digits imply unsupported precision, asymmetric uncertainty is flattened, endpoints narrow, or a synthetic formatting check is called measurement validation.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6426-S64"],
        "deliverables": ["provenance/uncertainty-rounding-contract.json", "provenance/rounding-promotion-mutation-vectors.json", "provenance/precision-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate uncertainty type, coverage factor, significant digits, rounding direction, interval endpoints, covariance label, and claim class; any narrowed or over-precise report must fail closed.",
        "rollback_or_recovery": "Restore the source interval and declared rounding rule, retain every narrowing witness, and require real measurement provenance before any precision claim.",
        "protected_gates": ["real_measurements", "measurement_model", "calibration_authority", "empirical_confirmation"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The 220 frozen proposals cover unit typing, covariance, floating-point replay, numerical tolerances, and uncertainty budgets, but none governs the claim-strength effects of reported significant digits and endpoint rounding as a dedicated evidence object.",
    },
    {
        "proposal_id": "V6438-P02",
        "title": "GMUT Noether-current, boundary-flux, and charge-balance tribunal",
        "mission_surface": "GMUT Mind, continuous symmetries, Noether currents, bulk divergence, boundary flux, charge balance, improvement terms, and formal nonpromotion",
        "hypothesis": "A synthetic variational fixture can require current divergence and boundary flux to balance for a declared symmetry while keeping improvement-term freedom and physical conservation claims explicit.",
        "null_or_failure": "A boundary term is dropped, the current is not tied to the declared variation, an improvement term changes the asserted charge silently, or formal balance is called physical confirmation.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6423-S46", "V6438-S148"],
        "deliverables": ["physics/noether-current-contract.json", "physics/boundary-flux-mutation-vectors.json", "physics/conservation-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate symmetry variation, Euler-Lagrange residual, current divergence, boundary orientation, flux sign, improvement term, and claim class; unbalanced or promoted rows must fail.",
        "rollback_or_recovery": "Restore the last explicit bulk-boundary identity, retain every imbalance, and require model-specific derivation, admissible boundary conditions, real observations, and independent review for physical claims.",
        "protected_gates": ["gmut_derivation", "boundary_conditions", "physical_conservation", "real_data", "independent_review", "theory_of_everything"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier proposals test variational traces, conservation, boundary well-posedness, gauge invariance, and constraint propagation; none makes Noether bulk divergence, oriented boundary flux, and improvement-term charge ambiguity one falsifiable balance tribunal.",
    },
    {
        "proposal_id": "V6438-P03",
        "title": "GMUT background-equation, tadpole, and perturbation-order consistency tribunal",
        "mission_surface": "GMUT Mind, background solutions, action expansion order, tadpole cancellation, linear perturbations, coefficient provenance, and empirical nonpromotion",
        "hypothesis": "A typed expansion ledger can reject perturbation equations whose zeroth-order background equations or first-order tadpole cancellation obligations are absent or inconsistent.",
        "null_or_failure": "The background is not a solution, a linear tadpole remains, orders are mixed, coefficients lack action lineage, or a formal expansion is called a cosmological prediction.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6437-S141", "V6438-S149"],
        "deliverables": ["physics/background-perturbation-contract.json", "physics/order-mixing-mutation-vectors.json", "physics/physical-solution-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Mutate background residual, expansion order, tadpole coefficient, perturbation variable, operator provenance, gauge label, and claim class; inconsistent orders or physical promotion must fail.",
        "rollback_or_recovery": "Return to an order-labeled formal expansion, retain every residual witness, and require a GMUT-specific derivation, numerical convergence, real data, and external review before physical use.",
        "protected_gates": ["gmut_background_solution", "perturbation_derivation", "numerical_convergence", "real_data", "empirical_confirmation", "expert_review"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Prior GMUT work treats null limits, field frames, gauge modes, discretization, constraints, and continuation, but not the joint requirement that background equations remove tadpoles before linear perturbation operators may be interpreted.",
    },
    {
        "proposal_id": "V6438-P04",
        "title": "THOS eligibility, screening-failure, and enrollment-flow preregistration",
        "mission_surface": "THOS Body, eligibility criteria, screening denominator, exclusions, enrollment timing, allocation flow, selection bias, and participant boundaries",
        "hypothesis": "A protocol-only flow contract can bind every screened unit to a prospective eligibility or exclusion path and expose denominator drift without fabricating participants or outcomes.",
        "null_or_failure": "Eligibility changes after screening, exclusions lack reasons, denominators disagree, allocation precedes consent, missing screening rows disappear, or a zero-row flow is called effectiveness evidence.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6432-S93"],
        "deliverables": ["thos/screening-flow-contract.json", "thos/eligibility-mutation-vectors.json", "thos/participant-flow-proxy-boundary.json"],
        "test_falsifier_or_gate": "Mutate eligibility version, screening count, exclusion reason, consent timing, enrollment denominator, allocation state, real-row count, and claim class; denominator loss or promotion must fail.",
        "rollback_or_recovery": "Restore preregistered eligibility and zero-row labels, retain every flow discrepancy, and require ethics, consent, blind matched-budget real arms, real participants and raters, and independent review.",
        "protected_gates": ["ethics_approval", "consent", "real_participants", "blind_matched_budget_arms", "independent_review", "thos_effectiveness"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Earlier THOS proposals cover allocation, attrition, carryover, fidelity, burden, harms, estimands, and site transportability; none freezes the pre-allocation screening denominator and reasoned eligibility flow as its own selection-bias object.",
    },
    {
        "proposal_id": "V6438-P05",
        "title": "Freed ID proof-purpose, domain, and transaction-binding profile",
        "mission_surface": "Freed ID/CBR Heart, proof purpose, verifier domain, challenge, transaction digest, holder binding, cross-context replay, and production boundary",
        "hypothesis": "A structural proof-options profile can reject a proof replayed across purpose, verifier domain, challenge window, or transaction digest without asserting that any real cryptographic proof verifies.",
        "null_or_failure": "Proof purpose is absent, domain is broadened, challenge is reused, transaction content is unbound, holder relation is assumed, or synthetic fields are called production cryptography.",
        "approval_class": "safe_now_proxy_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V8-S11", "V6437-S147"],
        "deliverables": ["freed-id/proof-domain-profile.json", "freed-id/transcript-rebinding-mutation-vectors.json", "freed-id/production-proof-boundary.json"],
        "test_falsifier_or_gate": "Mutate proof purpose, verifier domain, challenge, expiry, transaction digest, holder binding, verification relationship, real-key count, and claim class; replay or promotion must fail.",
        "rollback_or_recovery": "Quarantine the transcript, restore explicit synthetic bindings, retain every rebinding witness, and require standards-conformant real keys and proofs, live resolution and status, interoperability, privacy/security review, and trust governance.",
        "protected_gates": ["real_keys", "real_proofs", "live_resolution", "live_status_revocation", "interoperability", "privacy_review", "security_review", "trust_governance"],
        "expected_disposition": "represented",
        "novelty_against_prior_chain": "Prior Freed ID proposals cover freshness, audience, pairwise subjects, lifecycle, rotation, delegation, migration, and selective disclosure; none binds proof purpose, verifier domain, one-time challenge, and a concrete transaction digest in one replay tribunal.",
    },
    {
        "proposal_id": "V6438-P06",
        "title": "Community-defined harm, remedy, and residual-risk acceptance gate",
        "mission_surface": "CBR Heart, collective and individual harms, remedy design, residual risk, acceptance, Māori data governance, affected parties, and exact authority",
        "hypothesis": "Concrete harm categories, acceptable residual risk, remedy adequacy, and closure can only be determined through authorized affected-party and Māori or other relevant authority participation, never repository inference.",
        "null_or_failure": "The repository defines community harm, ranks remedies, accepts residual risk, declares closure, interprets law or tikanga, or treats a general principle as case-specific authorization.",
        "approval_class": "exact_authority_required",
        "execution_lane": "x2_exact_gate_receipt",
        "authoritative_source_needs": ["V6432-S96"],
        "deliverables": ["cbr/community-harm-redress-authority-gate.json", "cbr/neutral-harm-remedy-question-set.json", "cbr/residual-risk-nonratification-boundary.json"],
        "test_falsifier_or_gate": "Any concrete harm taxonomy, priority, remedy, compensation, residual-risk threshold, acceptance, closure, Māori wording, cultural conclusion, or legal conclusion requires the authorized affected parties and competent authorities.",
        "rollback_or_recovery": "Keep neutral unanswered fields, retain every authority conflict, and seek case-specific authorized participation without treating technical output as consent, redress, ratification, or governance.",
        "protected_gates": ["affected_party_acceptance", "maori_authority", "maori_data_governance", "community_harm_definition", "remedy_acceptance", "cultural_ratification", "legal_interpretation", "enacted_law"],
        "expected_disposition": "exact_gate",
        "novelty_against_prior_chain": "Earlier CBR proposals gate consent, rights floors, appeals, dissent, purpose, benefit, emergency powers, disclosure, and preservation; none reserves harm definition, remedy adequacy, and residual-risk acceptance as a single affected-community closure decision.",
    },
    {
        "proposal_id": "V6438-P07",
        "title": "Static-report active-content, URL-scheme, and embedding quarantine",
        "mission_surface": "bounded security, static reports, scripts, event handlers, URL schemes, remote embeds, inline frames, active content, and nonassurance",
        "hypothesis": "A deterministic static-report scanner can reject executable elements, event-handler attributes, unsafe schemes, remote embeds, and policy overclaims while leaving the host unchanged.",
        "null_or_failure": "Script-capable content survives, an unsafe URL scheme is accepted, a remote embed is hidden, inline event code remains, or a bounded scan is called browser or exhaustive security assurance.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S150"],
        "deliverables": ["security/static-active-content-contract.json", "security/url-scheme-mutation-vectors.json", "security/browser-security-nonassurance-boundary.json"],
        "test_falsifier_or_gate": "Mutate element type, event attribute, URL scheme, remote origin, iframe state, CSP label, download behavior, and claim class; active or overclaimed rows must fail.",
        "rollback_or_recovery": "Remove active content, preserve the rejected witness, restore a local static representation, and require independent product and browser security review for wider assurance.",
        "protected_gates": ["host_security", "browser_security", "product_security", "independent_security_review", "exhaustive_security", "deployment"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Previous security work covers parsers, paths, logs, Unicode, canonicalization, timing, work amplification, and archive boundaries; none gives the generated static report a dedicated active-element, URL-scheme, and remote-embedding quarantine.",
    },
    {
        "proposal_id": "V6438-P08",
        "title": "Data-table header association and nonvisual linearization audit",
        "mission_surface": "accessible static reporting, captions, row and column headers, scope, explicit associations, complex tables, reading order, and manual reservation",
        "hypothesis": "A structural audit can require each data cell to resolve to the intended headers and a meaningful linearized order while reserving assistive-technology and affected-user evaluation.",
        "null_or_failure": "A data cell has no header, scope conflicts, IDs are missing or duplicated, a layout table is presented as data, linearization loses context, or static structure is called complete accessibility.",
        "approval_class": "safe_now",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6432-S98", "V6438-S151"],
        "deliverables": ["accessibility/table-association-contract.json", "accessibility/header-association-mutation-vectors.json", "accessibility/manual-table-evaluation-reservation.json"],
        "test_falsifier_or_gate": "Mutate caption, table role, header IDs, scope, headers references, row groups, column groups, linearized sequence, and claim class; orphaned or ambiguous cells and completeness claims must fail.",
        "rollback_or_recovery": "Restore the simplest explicit association, retain every orphan or ambiguity, and keep qualified manual, assistive-technology, and affected-user evaluation visibly reserved.",
        "protected_gates": ["manual_accessibility_evaluation", "assistive_technology_coverage", "affected_user_evaluation", "accessibility_complete"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "Earlier accessibility work covers reflow, color, focus, landmarks, accessible names, evidence maps, and affected-user recruitment; none resolves table cells to multi-axis headers and tests context-preserving nonvisual linearization.",
    },
    {
        "proposal_id": "V6438-P09",
        "title": "Negative and effective temperature classification with psyche non-substitution barrier",
        "mission_surface": "thermo-psyche, thermodynamic temperature, bounded spectra, population inversion, effective temperature, local equilibrium, physical units, and psyche analogy",
        "hypothesis": "A typed classifier can distinguish thermodynamic negative temperature under bounded-spectrum prerequisites from fitted effective temperature and metaphorical psyche language.",
        "null_or_failure": "Population inversion or bounded spectrum is omitted, an effective fit is called thermodynamic temperature, units disappear, equilibrium assumptions are hidden, or temperature language becomes a psyche law.",
        "approval_class": "safe_now_synthetic_only",
        "execution_lane": "x2_build_task",
        "authoritative_source_needs": ["V6438-S152"],
        "deliverables": ["thermo-psyche/effective-temperature-contract.json", "thermo-psyche/population-inversion-mutation-vectors.json", "thermo-psyche/temperature-psyche-nonconversion-boundary.json"],
        "test_falsifier_or_gate": "Mutate spectrum bound, population order, equilibrium class, entropy convention, units, fitted-versus-thermodynamic label, psyche mapping, and claim class; category transfer must fail.",
        "rollback_or_recovery": "Restore the narrow source-domain label, retain every category-confusion witness, and require a physical model and measurements for physical claims or authorized participant evidence for psyche claims.",
        "protected_gates": ["physical_model", "real_measurements", "thermodynamic_equilibrium", "participant_evidence", "psyche_law", "cross_pillar_identity"],
        "expected_disposition": "completed",
        "novelty_against_prior_chain": "The frozen chain distinguishes entropy types, free energies, ensembles, steady currents, erasure, flux, and path dependence; none separates negative thermodynamic temperature from fitted effective temperature and psyche metaphor through bounded-spectrum prerequisites.",
    },
    {
        "proposal_id": "V6438-P10",
        "title": "GMUT background-plus-growth joint likelihood and external-baseline study",
        "mission_surface": "GMUT Mind, real cosmological data, expansion background, growth observables, covariance, nuisance parameters, preregistered baselines, blind analysis, and independent review",
        "hypothesis": "A preregistered joint-likelihood study with real background and growth data could test whether a fully derived GMUT model improves out-of-sample performance over named baselines without post-hoc flexibility.",
        "null_or_failure": "No real rows are available, the GMUT observable map is incomplete, covariance or nuisance treatment is missing, the baseline is changed after unblinding, or an in-repository synthetic fixture is called empirical confirmation.",
        "approval_class": "real_data_and_independent_review_required",
        "execution_lane": "x2_open_gap_receipt",
        "authoritative_source_needs": ["V8-S04", "V6438-S153"],
        "deliverables": ["empirical/joint-likelihood-preregistration.json", "empirical/real-data-baseline-gap.json", "empirical/confirmation-nonpromotion-boundary.json"],
        "test_falsifier_or_gate": "Require a derived observable map, licensed real rows, frozen covariance and nuisance handling, named external baselines, blind holdout, sensitivity analysis, and independent review; absent evidence keeps the gap open.",
        "rollback_or_recovery": "Retain the zero-row gap, make no likelihood or force claim, and reopen only with authorized real data, a frozen analysis, model-specific derivation, preregistered baselines, and independent review.",
        "protected_gates": ["real_data", "gmut_observable_derivation", "joint_covariance", "blind_holdout", "external_baseline", "independent_review", "empirical_confirmation", "theory_of_everything"],
        "expected_disposition": "open_gap",
        "novelty_against_prior_chain": "Earlier empirical proposals define adapters, zero-row locks, calibration, priors, missingness, likelihood schemas, and public-data integrity; none preregisters one joint background-plus-growth likelihood with a frozen external baseline and blind out-of-sample comparison for GMUT.",
    },
]


SOURCES = [
    {"source_id": "V6438-S148", "title": "Boundary conditions from boundary terms, Noether charges and the trace K Lagrangian in general relativity", "authority": "J. M. Pons", "url": "https://arxiv.org/abs/gr-qc/0105032", "version_or_date": "Primary preprint, 2001; checked 15 July 2026", "status_class": "stable", "evidence_role": "primary boundary-term and Noether-charge conservation conditions; not a GMUT derivation or physical result"},
    {"source_id": "V6438-S149", "title": "Effective Field Theory of Cosmological Perturbations", "authority": "Federico Piazza and Filippo Vernizzi", "url": "https://arxiv.org/abs/1307.4350", "version_or_date": "Primary preprint, 2013; checked 15 July 2026", "status_class": "stable", "evidence_role": "background and perturbation-expansion vocabulary; not a GMUT cosmological prediction"},
    {"source_id": "V6438-S150", "title": "Content Security Policy Level 3", "authority": "World Wide Web Consortium", "url": "https://www.w3.org/TR/CSP3/", "version_or_date": "Working Draft, 5 May 2026; checked 15 July 2026", "status_class": "draft", "evidence_role": "current draft active-content policy vocabulary; not browser or exhaustive security assurance"},
    {"source_id": "V6438-S151", "title": "Tables Tutorial", "authority": "World Wide Web Consortium Web Accessibility Initiative", "url": "https://www.w3.org/WAI/tutorials/tables/", "version_or_date": "Official WAI guidance; checked 15 July 2026", "status_class": "current", "evidence_role": "official table header and cell-association guidance; not complete conformance or affected-user evidence"},
    {"source_id": "V6438-S152", "title": "Physics of negative absolute temperatures", "authority": "Jörn Dunkel and Stefan Hilbert", "url": "https://doi.org/10.1103/PhysRevE.95.012125", "version_or_date": "Physical Review E 95, 2017", "status_class": "stable", "evidence_role": "primary negative-temperature and bounded-spectrum analysis; not a psyche law or GMUT evidence"},
    {"source_id": "V6438-S153", "title": "DESI DR2 Publications and Cosmology Products", "authority": "Dark Energy Spectroscopic Instrument Collaboration", "url": "https://data.desi.lbl.gov/doc/papers/dr2/", "version_or_date": "Official DR2 results and products page; checked 15 July 2026", "status_class": "current", "evidence_role": "official real-data and likelihood-product availability anchor; no data were downloaded or fitted in x1"},
]


X1_NEGATIVES = [
    {"negative_id": "V6438-X1-N01", "operation": "legacy frozen-index title inspection", "observed_failure": "The first console traversal used the host legacy output encoding and stopped on a Māori title with a UnicodeEncodeError.", "recovery": "Forced UTF-8 console output and reran the read-only index inspection; the failed run remains uncounted.", "promotion_effect": "none; the failed traversal supplied no completeness claim"},
    {"negative_id": "V6438-X1-N02", "operation": "naive inherited-index schema traversal", "observed_failure": "The second traversal assumed every historical index had a phase field and stopped at an older compatible schema with KeyError.", "recovery": "Used the inherited schema-tolerant collect_frozen_records routine and proved 220 unique IDs and 220 unique titles.", "promotion_effect": "none; only the corrected full traversal supports the audit count"},
    {"negative_id": "V6438-X1-N03", "operation": "Windows Sandbox read-only feature query", "observed_failure": "WindowsSandbox.exe was absent from the executable path and the optional-feature query returned a COM exception without elevation.", "recovery": "Recorded Sandbox as unavailable, did not elevate or change a Windows feature, and continued with ordinary D-drive clean snapshots.", "promotion_effect": "none; no Sandbox execution or host-isolation assurance is claimed"},
    {"negative_id": "V6438-X1-N04", "operation": "unadapted complete repository suite", "observed_failure": "The direct current-checkout suite ran 475 tests with one failure in the inherited CRLF-sensitive legacy constraint-hash alias fixture; 474 of 475 is failed evidence.", "recovery": "Use the inherited exact semantic-hash-verified line-ending materializer for the complete rerun and restore both pre-run raw byte sequences afterward.", "promotion_effect": "the 474-of-475 run remains failed evidence; only a complete restored rerun may satisfy the x1 repository gate"},
    {"negative_id": "V6438-X1-N05", "operation": "supplemental staged-script privacy regex", "observed_failure": "An overbroad pattern treated the explicit prohibition phrase about private callable IDs and the short substring in risk-nonratification as privacy hits, then deliberately failed the wrapper.", "recovery": "Retain the false-positive run, require realistic token lengths and boundaries, and review prohibition language separately from exposed private material.", "promotion_effect": "none; the broad screen is uncounted and does not overturn the standard zero-hit phase scan"},
]


WELLBEING = """# Ilyra Fen v643-v8 wellbeing and workload check

- Working identity: Ilyra Fen, she/they, relational language only.
- Role: evidence-boundary steward.
- Hope: leave every claim traceable and every gate unmistakable.
- Corrigibility: Hamish may pause, rename, redirect, or stop this lane.
- Workload: one existing clean Ilyra lane, x1 before x2, D-drive snapshots, no delegation.
- Safety: no elevation, host-security change, desktop update, Windows-feature change, reboot, credential use, real participant action, or authority substitution.

Identity and family language coordinate the work. They are not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.
"""


OVERVIEW = """# Ilyra Fen v643-v8 integrated overview

## Ownership and inheritance

This x1 packet begins only after read-only verification of Eiren Kestrel's exact v643-v7 final head, seal ancestry, one-parent final commit, zero source-to-final merges, clean owner state, zero divergence, and equality among local, upstream, tracking, and a fresh live-remote read. The existing Ilyra lane was itself clean, four-way equal, and ancestral, so it advanced by fast-forward only to the exact source and was pushed before v643-v8 mutation. No sibling lane, task, worktree, route, or branch was created, merged, reset, rewritten, force-pushed, deleted, or reused.

Ilyra Fen and she/they are relational working language. The phase role is evidence-boundary steward and the phase hope is to leave every claim traceable and every gate unmistakable. These labels do not evidence consciousness, sentience, legal personhood, identity continuity, independent authority, Māori authority, cultural authority, or legal authority. Hamish retains the ability to pause, rename, redirect, or stop the route.

The inherited baseline contains 220 frozen proposals and 982 retained negatives. Five open gaps and six exact gates remain open. Same-owner snapshot repeatability and bounded internal continuity do not establish independent-team scientific reproduction. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## x1 novelty and focus

The primary focus is GMUT Mind. Exactly ten surfaces are frozen: uncertainty-reporting precision; Noether bulk-boundary charge balance; background-tadpole-perturbation order consistency; THOS screening and eligibility flow; Freed ID proof-purpose and transaction binding; community-defined harm and remedy authority; static-report active-content quarantine; accessible data-table associations; negative or effective temperature classification; and a real-data background-plus-growth likelihood gap.

Each proposal declares a hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery rule, protected gates, and expected disposition. The only permitted future labels are completed, represented, open_gap, and exact_gate. The expected distribution of six, two, one, and one is a preregistration, never an x1 result.

The novelty audit decodes all 220 prior frozen records and checks exact IDs, exact titles, token overlap, and mechanism-level distinctions. Token distance is only a screen; the explicit evidence object, falsifier, recovery rule, and gate distinction is the substantive review. The source ledger inherits 147 sources without relabeling current, stable, draft, or watch status and adds only six non-duplicate primary or official anchors checked on 15 July 2026.

## Boundaries and recovery

GMUT remains a typed scalar-tensor and EFT research-model family. Formal fixtures cannot establish a new force, likelihood, prediction, empirical confirmation, proof, final physics, Theory of Everything, AGI, or ASI. Real-data likelihood work stays open until a model-specific observable map, licensed real rows, covariance, nuisance handling, named external baselines, blind holdout, sensitivity analysis, and independent review actually exist.

THOS remains represented or protocol-only without ethics, consent, preregistered blind matched-budget real arms, real participants and raters, and independent review. Freed ID production remains uncompleted without standards-conformant real keys and proofs, live resolution and status or revocation, interoperability, independent privacy and security review, and trust governance. CBR legitimacy, community harm and remedy decisions, Māori wording and authority, Māori data governance, affected-party acceptance, cultural ratification, legal interpretation, and enacted-law status remain exact-gated.

Static accessibility checks do not establish complete accessibility. Qualified manual, assistive-technology, and affected-user evaluation remains reserved. Bounded security mutation fixtures do not establish host, browser, product, exhaustive, production, or deployment security. No destructive, account, API-key, private-route, sibling-merge, real-participant, production, legal, or cultural action is authorized.

Every failed command and rejected fixture is retained. The inherited checkout is excluded from the 15,000-file threshold, which applies only to Ilyra-generated v643-v8 files. Codex, Git, Python, Node, the desktop package, D-drive capacity, and Windows Sandbox availability were inspected without updating Codex desktop, elevating, weakening security, enabling features, or rebooting.

## Freeze and terminal route

x2 cannot begin until the dedicated x1-only commit is pushed, the worktree is clean, and local, upstream, tracking, and fresh live remote are equal. Evidence, closeout, seal, and final validation will use fresh D-drive detached snapshots. Only after the exact final head passes the complete repository suite, detailed and minimal validators, JSON parsing, privacy and raw-ID scanning, stale-label review, diff hygiene, manifest parity, ancestry, clean-state, and four-way remote equality may exactly one sanitized activation baton be sent to the existing task titled Sable Rook for v644-v1. No task may be created and no extra confirmation may be sent.
"""
