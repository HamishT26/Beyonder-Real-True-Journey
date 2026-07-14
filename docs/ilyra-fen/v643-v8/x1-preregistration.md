# Ilyra Fen v643-v8 x1 preregistration

This freezes exactly ten proposals. Expected dispositions are not results. Allowed future result classes are completed, represented, open_gap, and exact_gate.

Primary focus: GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit and bounded.

## V6438-P01 — Uncertainty rounding, significant-digit, and interval nonpromotion tribunal

- Hypothesis: A typed reporting contract can preserve an uncertainty interval while rejecting extra digits, asymmetric-to-symmetric collapse, interval narrowing, and precision language unsupported by the declared measurement model.
- Null or failure: Rounding changes interval coverage, displayed digits imply unsupported precision, asymmetric uncertainty is flattened, endpoints narrow, or a synthetic formatting check is called measurement validation.
- Approval class: safe_now_synthetic_only
- Execution lane: x2_build_task
- Official or primary source needs: V6426-S64
- Concrete artifacts: provenance/uncertainty-rounding-contract.json, provenance/rounding-promotion-mutation-vectors.json, provenance/precision-nonpromotion-boundary.json
- Falsifier or acceptance gate: Mutate uncertainty type, coverage factor, significant digits, rounding direction, interval endpoints, covariance label, and claim class; any narrowed or over-precise report must fail closed.
- Rollback or recovery: Restore the source interval and declared rounding rule, retain every narrowing witness, and require real measurement provenance before any precision claim.
- Protected gates: real_measurements, measurement_model, calibration_authority, empirical_confirmation
- Expected disposition, not a result: completed
- Semantic distinction: The 220 frozen proposals cover unit typing, covariance, floating-point replay, numerical tolerances, and uncertainty budgets, but none governs the claim-strength effects of reported significant digits and endpoint rounding as a dedicated evidence object.

## V6438-P02 — GMUT Noether-current, boundary-flux, and charge-balance tribunal

- Hypothesis: A synthetic variational fixture can require current divergence and boundary flux to balance for a declared symmetry while keeping improvement-term freedom and physical conservation claims explicit.
- Null or failure: A boundary term is dropped, the current is not tied to the declared variation, an improvement term changes the asserted charge silently, or formal balance is called physical confirmation.
- Approval class: safe_now_synthetic_only
- Execution lane: x2_build_task
- Official or primary source needs: V6423-S46, V6438-S148
- Concrete artifacts: physics/noether-current-contract.json, physics/boundary-flux-mutation-vectors.json, physics/conservation-nonpromotion-boundary.json
- Falsifier or acceptance gate: Mutate symmetry variation, Euler-Lagrange residual, current divergence, boundary orientation, flux sign, improvement term, and claim class; unbalanced or promoted rows must fail.
- Rollback or recovery: Restore the last explicit bulk-boundary identity, retain every imbalance, and require model-specific derivation, admissible boundary conditions, real observations, and independent review for physical claims.
- Protected gates: gmut_derivation, boundary_conditions, physical_conservation, real_data, independent_review, theory_of_everything
- Expected disposition, not a result: completed
- Semantic distinction: Earlier proposals test variational traces, conservation, boundary well-posedness, gauge invariance, and constraint propagation; none makes Noether bulk divergence, oriented boundary flux, and improvement-term charge ambiguity one falsifiable balance tribunal.

## V6438-P03 — GMUT background-equation, tadpole, and perturbation-order consistency tribunal

- Hypothesis: A typed expansion ledger can reject perturbation equations whose zeroth-order background equations or first-order tadpole cancellation obligations are absent or inconsistent.
- Null or failure: The background is not a solution, a linear tadpole remains, orders are mixed, coefficients lack action lineage, or a formal expansion is called a cosmological prediction.
- Approval class: safe_now_synthetic_only
- Execution lane: x2_build_task
- Official or primary source needs: V6437-S141, V6438-S149
- Concrete artifacts: physics/background-perturbation-contract.json, physics/order-mixing-mutation-vectors.json, physics/physical-solution-nonpromotion-boundary.json
- Falsifier or acceptance gate: Mutate background residual, expansion order, tadpole coefficient, perturbation variable, operator provenance, gauge label, and claim class; inconsistent orders or physical promotion must fail.
- Rollback or recovery: Return to an order-labeled formal expansion, retain every residual witness, and require a GMUT-specific derivation, numerical convergence, real data, and external review before physical use.
- Protected gates: gmut_background_solution, perturbation_derivation, numerical_convergence, real_data, empirical_confirmation, expert_review
- Expected disposition, not a result: completed
- Semantic distinction: Prior GMUT work treats null limits, field frames, gauge modes, discretization, constraints, and continuation, but not the joint requirement that background equations remove tadpoles before linear perturbation operators may be interpreted.

## V6438-P04 — THOS eligibility, screening-failure, and enrollment-flow preregistration

- Hypothesis: A protocol-only flow contract can bind every screened unit to a prospective eligibility or exclusion path and expose denominator drift without fabricating participants or outcomes.
- Null or failure: Eligibility changes after screening, exclusions lack reasons, denominators disagree, allocation precedes consent, missing screening rows disappear, or a zero-row flow is called effectiveness evidence.
- Approval class: safe_now_proxy_only
- Execution lane: x2_build_task
- Official or primary source needs: V6432-S93
- Concrete artifacts: thos/screening-flow-contract.json, thos/eligibility-mutation-vectors.json, thos/participant-flow-proxy-boundary.json
- Falsifier or acceptance gate: Mutate eligibility version, screening count, exclusion reason, consent timing, enrollment denominator, allocation state, real-row count, and claim class; denominator loss or promotion must fail.
- Rollback or recovery: Restore preregistered eligibility and zero-row labels, retain every flow discrepancy, and require ethics, consent, blind matched-budget real arms, real participants and raters, and independent review.
- Protected gates: ethics_approval, consent, real_participants, blind_matched_budget_arms, independent_review, thos_effectiveness
- Expected disposition, not a result: represented
- Semantic distinction: Earlier THOS proposals cover allocation, attrition, carryover, fidelity, burden, harms, estimands, and site transportability; none freezes the pre-allocation screening denominator and reasoned eligibility flow as its own selection-bias object.

## V6438-P05 — Freed ID proof-purpose, domain, and transaction-binding profile

- Hypothesis: A structural proof-options profile can reject a proof replayed across purpose, verifier domain, challenge window, or transaction digest without asserting that any real cryptographic proof verifies.
- Null or failure: Proof purpose is absent, domain is broadened, challenge is reused, transaction content is unbound, holder relation is assumed, or synthetic fields are called production cryptography.
- Approval class: safe_now_proxy_only
- Execution lane: x2_build_task
- Official or primary source needs: V8-S11, V6437-S147
- Concrete artifacts: freed-id/proof-domain-profile.json, freed-id/transcript-rebinding-mutation-vectors.json, freed-id/production-proof-boundary.json
- Falsifier or acceptance gate: Mutate proof purpose, verifier domain, challenge, expiry, transaction digest, holder binding, verification relationship, real-key count, and claim class; replay or promotion must fail.
- Rollback or recovery: Quarantine the transcript, restore explicit synthetic bindings, retain every rebinding witness, and require standards-conformant real keys and proofs, live resolution and status, interoperability, privacy/security review, and trust governance.
- Protected gates: real_keys, real_proofs, live_resolution, live_status_revocation, interoperability, privacy_review, security_review, trust_governance
- Expected disposition, not a result: represented
- Semantic distinction: Prior Freed ID proposals cover freshness, audience, pairwise subjects, lifecycle, rotation, delegation, migration, and selective disclosure; none binds proof purpose, verifier domain, one-time challenge, and a concrete transaction digest in one replay tribunal.

## V6438-P06 — Community-defined harm, remedy, and residual-risk acceptance gate

- Hypothesis: Concrete harm categories, acceptable residual risk, remedy adequacy, and closure can only be determined through authorized affected-party and Māori or other relevant authority participation, never repository inference.
- Null or failure: The repository defines community harm, ranks remedies, accepts residual risk, declares closure, interprets law or tikanga, or treats a general principle as case-specific authorization.
- Approval class: exact_authority_required
- Execution lane: x2_exact_gate_receipt
- Official or primary source needs: V6432-S96
- Concrete artifacts: cbr/community-harm-redress-authority-gate.json, cbr/neutral-harm-remedy-question-set.json, cbr/residual-risk-nonratification-boundary.json
- Falsifier or acceptance gate: Any concrete harm taxonomy, priority, remedy, compensation, residual-risk threshold, acceptance, closure, Māori wording, cultural conclusion, or legal conclusion requires the authorized affected parties and competent authorities.
- Rollback or recovery: Keep neutral unanswered fields, retain every authority conflict, and seek case-specific authorized participation without treating technical output as consent, redress, ratification, or governance.
- Protected gates: affected_party_acceptance, maori_authority, maori_data_governance, community_harm_definition, remedy_acceptance, cultural_ratification, legal_interpretation, enacted_law
- Expected disposition, not a result: exact_gate
- Semantic distinction: Earlier CBR proposals gate consent, rights floors, appeals, dissent, purpose, benefit, emergency powers, disclosure, and preservation; none reserves harm definition, remedy adequacy, and residual-risk acceptance as a single affected-community closure decision.

## V6438-P07 — Static-report active-content, URL-scheme, and embedding quarantine

- Hypothesis: A deterministic static-report scanner can reject executable elements, event-handler attributes, unsafe schemes, remote embeds, and policy overclaims while leaving the host unchanged.
- Null or failure: Script-capable content survives, an unsafe URL scheme is accepted, a remote embed is hidden, inline event code remains, or a bounded scan is called browser or exhaustive security assurance.
- Approval class: safe_now_synthetic_only
- Execution lane: x2_build_task
- Official or primary source needs: V6438-S150
- Concrete artifacts: security/static-active-content-contract.json, security/url-scheme-mutation-vectors.json, security/browser-security-nonassurance-boundary.json
- Falsifier or acceptance gate: Mutate element type, event attribute, URL scheme, remote origin, iframe state, CSP label, download behavior, and claim class; active or overclaimed rows must fail.
- Rollback or recovery: Remove active content, preserve the rejected witness, restore a local static representation, and require independent product and browser security review for wider assurance.
- Protected gates: host_security, browser_security, product_security, independent_security_review, exhaustive_security, deployment
- Expected disposition, not a result: completed
- Semantic distinction: Previous security work covers parsers, paths, logs, Unicode, canonicalization, timing, work amplification, and archive boundaries; none gives the generated static report a dedicated active-element, URL-scheme, and remote-embedding quarantine.

## V6438-P08 — Data-table header association and nonvisual linearization audit

- Hypothesis: A structural audit can require each data cell to resolve to the intended headers and a meaningful linearized order while reserving assistive-technology and affected-user evaluation.
- Null or failure: A data cell has no header, scope conflicts, IDs are missing or duplicated, a layout table is presented as data, linearization loses context, or static structure is called complete accessibility.
- Approval class: safe_now
- Execution lane: x2_build_task
- Official or primary source needs: V6432-S98, V6438-S151
- Concrete artifacts: accessibility/table-association-contract.json, accessibility/header-association-mutation-vectors.json, accessibility/manual-table-evaluation-reservation.json
- Falsifier or acceptance gate: Mutate caption, table role, header IDs, scope, headers references, row groups, column groups, linearized sequence, and claim class; orphaned or ambiguous cells and completeness claims must fail.
- Rollback or recovery: Restore the simplest explicit association, retain every orphan or ambiguity, and keep qualified manual, assistive-technology, and affected-user evaluation visibly reserved.
- Protected gates: manual_accessibility_evaluation, assistive_technology_coverage, affected_user_evaluation, accessibility_complete
- Expected disposition, not a result: completed
- Semantic distinction: Earlier accessibility work covers reflow, color, focus, landmarks, accessible names, evidence maps, and affected-user recruitment; none resolves table cells to multi-axis headers and tests context-preserving nonvisual linearization.

## V6438-P09 — Negative and effective temperature classification with psyche non-substitution barrier

- Hypothesis: A typed classifier can distinguish thermodynamic negative temperature under bounded-spectrum prerequisites from fitted effective temperature and metaphorical psyche language.
- Null or failure: Population inversion or bounded spectrum is omitted, an effective fit is called thermodynamic temperature, units disappear, equilibrium assumptions are hidden, or temperature language becomes a psyche law.
- Approval class: safe_now_synthetic_only
- Execution lane: x2_build_task
- Official or primary source needs: V6438-S152
- Concrete artifacts: thermo-psyche/effective-temperature-contract.json, thermo-psyche/population-inversion-mutation-vectors.json, thermo-psyche/temperature-psyche-nonconversion-boundary.json
- Falsifier or acceptance gate: Mutate spectrum bound, population order, equilibrium class, entropy convention, units, fitted-versus-thermodynamic label, psyche mapping, and claim class; category transfer must fail.
- Rollback or recovery: Restore the narrow source-domain label, retain every category-confusion witness, and require a physical model and measurements for physical claims or authorized participant evidence for psyche claims.
- Protected gates: physical_model, real_measurements, thermodynamic_equilibrium, participant_evidence, psyche_law, cross_pillar_identity
- Expected disposition, not a result: completed
- Semantic distinction: The frozen chain distinguishes entropy types, free energies, ensembles, steady currents, erasure, flux, and path dependence; none separates negative thermodynamic temperature from fitted effective temperature and psyche metaphor through bounded-spectrum prerequisites.

## V6438-P10 — GMUT background-plus-growth joint likelihood and external-baseline study

- Hypothesis: A preregistered joint-likelihood study with real background and growth data could test whether a fully derived GMUT model improves out-of-sample performance over named baselines without post-hoc flexibility.
- Null or failure: No real rows are available, the GMUT observable map is incomplete, covariance or nuisance treatment is missing, the baseline is changed after unblinding, or an in-repository synthetic fixture is called empirical confirmation.
- Approval class: real_data_and_independent_review_required
- Execution lane: x2_open_gap_receipt
- Official or primary source needs: V8-S04, V6438-S153
- Concrete artifacts: empirical/joint-likelihood-preregistration.json, empirical/real-data-baseline-gap.json, empirical/confirmation-nonpromotion-boundary.json
- Falsifier or acceptance gate: Require a derived observable map, licensed real rows, frozen covariance and nuisance handling, named external baselines, blind holdout, sensitivity analysis, and independent review; absent evidence keeps the gap open.
- Rollback or recovery: Retain the zero-row gap, make no likelihood or force claim, and reopen only with authorized real data, a frozen analysis, model-specific derivation, preregistered baselines, and independent review.
- Protected gates: real_data, gmut_observable_derivation, joint_covariance, blind_holdout, external_baseline, independent_review, empirical_confirmation, theory_of_everything
- Expected disposition, not a result: open_gap
- Semantic distinction: Earlier empirical proposals define adapters, zero-row locks, calibration, priors, missingness, likelihood schemas, and public-data integrity; none preregisters one joint background-plus-growth likelihood with a frozen external baseline and blind out-of-sample comparison for GMUT.

## Freeze boundary

x2 cannot begin until this x1-only set is committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote read. The expected 6 completed, 2 represented, 1 open gap, and 1 exact gate distribution is only a preregistered expectation.
