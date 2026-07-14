# Orin Thale v643-v4 x1 preregistration

This is the frozen x1 plan for exactly ten proposals. No outcome below is a result. The only allowed future result classes are `completed`, `represented`, `open_gap`, and `exact_gate`.

Primary focus: **GMUT Mind**. THOS Body and Freed ID/CBR Heart remain explicitly addressed and bounded.

## V6434-P01 — Retraction, correction, and supersession propagation with stale-citation quarantine

- Hypothesis: A typed update graph can propagate retraction, correction, expression-of-concern, and supersession states into dependent claims while quarantining stale citations until their evidential effect is reviewed.
- Null/failure: A changed source status leaves a dependent claim promotable, a correction is treated as equivalent to a retraction, supersession is silently ignored, or quarantine can be cleared without a recorded review.
- Approval class: `safe_now`
- Execution lane: `x2_build_task`
- Official/primary source needs: V6434-S111
- Concrete artifacts: `provenance/correction-propagation-contract.json`, `provenance/stale-citation-mutation-vectors.json`, `provenance/post-publication-status-boundary.json`
- Falsifier/acceptance gate: Mutate update type, source identity, dependency direction, review state, and quarantine clearance; any stale promotion or status flattening must fail closed.
- Rollback/recovery: Restore the last reviewed dependency graph, retain the update event and stale citation as negatives, and require source-level reassessment before promotion.
- Protected gates: `source_currency`, `scientific_review`, `empirical_confirmation`, `proof_or_canon`
- Expected disposition, not a result: `completed`
- Semantic distinction: Earlier work handled source freshness and private-source taint, but did not encode post-publication retraction, correction, concern, and supersession propagation with status-specific quarantine semantics.

## V6434-P02 — Boundary-condition well-posedness and characteristic initial-data obligation for GMUT

- Hypothesis: A typed obligation ledger can distinguish a written field equation from a well-posed initial-boundary value problem by requiring characteristic, compatibility, existence, uniqueness, and continuous-dependence evidence before causal promotion.
- Null/failure: An equation is promoted as predictive without admissible data surfaces, incompatible boundary data pass, characteristic degeneracy is ignored, or a typed obligation is described as a GMUT theorem or observation.
- Approval class: `safe_now`
- Execution lane: `x2_build_task`
- Official/primary source needs: V6434-S112
- Concrete artifacts: `physics/initial-boundary-obligation.json`, `physics/well-posedness-mutation-vectors.json`, `physics/characteristic-data-boundary.json`
- Falsifier/acceptance gate: Mutate characteristic status, initial data, boundary compatibility, uniqueness, continuous dependence, and claim class; unsupported predictive or causal promotion must fail.
- Rollback/recovery: Return the item to typed scaffold status, preserve the missing mathematical obligation, and require an expert derivation and independent review for promotion.
- Protected gates: `gmut_derivation`, `mathematical_proof`, `expert_review`, `empirical_confirmation`, `theory_of_everything`
- Expected disposition, not a result: `completed`
- Semantic distinction: Prior GMUT proposals addressed rank, hyperbolicity, cones, and degeneracy; none made compatible initial-boundary data and continuous dependence a separate promotion obligation.

## V6434-P03 — Selection-model and missing-not-at-random sensitivity envelope with zero-row promotion lock

- Hypothesis: A synthetic selection-model envelope can expose how missing-not-at-random assumptions alter a claimed estimate while a zero-row lock prevents the envelope from being mistaken for empirical evidence.
- Null/failure: A missingness parameter is untracked, a synthetic row is described as observed data, sensitivity results are promoted as a likelihood result, or zero real rows do not block empirical language.
- Approval class: `safe_now_proxy_only`
- Execution lane: `x2_build_task`
- Official/primary source needs: V6434-S113
- Concrete artifacts: `empirical/mnar-sensitivity-envelope.json`, `empirical/selection-model-mutation-vectors.json`, `empirical/zero-row-selection-lock.json`
- Falsifier/acceptance gate: Vary selection parameters, missingness class, observed-row count, provenance, and claim label; zero-row or unidentified configurations must not promote.
- Rollback/recovery: Restore the last fully typed synthetic envelope, retain failed parameterizations, and require real preregistered data and statistical review for empirical claims.
- Protected gates: `real_data`, `likelihood_result`, `empirical_confirmation`, `independent_statistical_review`
- Expected disposition, not a result: `represented`
- Semantic distinction: Earlier zero-row and calibration work did not model a missing-not-at-random selection parameter or bind its sensitivity surface to an explicit zero-row promotion lock.

## V6434-P04 — Mediation identification and post-treatment-confounding non-promotion protocol for THOS

- Hypothesis: A typed mediation protocol can separate total, direct, and indirect estimands from their identification assumptions and refuse promotion when post-treatment mediator-outcome confounding is uncontrolled.
- Null/failure: A mediator is treated as randomized, post-treatment confounding is ignored, a synthetic decomposition is reported as a real THOS mechanism, or sensitivity assumptions are omitted.
- Approval class: `safe_now_proxy_only`
- Execution lane: `x2_build_task`
- Official/primary source needs: V6434-S114
- Concrete artifacts: `thos/mediation-identification-protocol.json`, `thos/post-treatment-confounding-vectors.json`, `thos/mediation-nonpromotion-boundary.json`
- Falsifier/acceptance gate: Mutate treatment timing, mediator timing, confounder timing, identification assumptions, real-row count, and claim class; any unsupported causal mechanism claim must fail.
- Rollback/recovery: Revert to association-only proxy language, preserve the failed identification row, and require preregistered real arms plus independent causal review.
- Protected gates: `real_participants`, `causal_identification`, `thos_superiority`, `independent_review`, `empirical_confirmation`
- Expected disposition, not a result: `represented`
- Semantic distinction: Prior THOS estimand and protocol-deviation work did not isolate mediator identification or post-treatment mediator-outcome confounding as a distinct non-promotion condition.

## V6434-P05 — Real-arm facilitator learning-curve and temporal-drift parity gate for THOS

- Hypothesis: A preregistered real-arm design could estimate facilitator learning curves and temporal drift without confounding treatment, facilitator, cohort, budget, or rater effects.
- Null/failure: Facilitator and treatment are aliased, calendar time is omitted, budgets differ, ratings are unblinded, real participants are absent, or facilitator drift is generalized beyond the observed design.
- Approval class: `external_evidence_required`
- Execution lane: `x2_open_gap_receipt`
- Official/primary source needs: V6434-S115
- Concrete artifacts: `thos/facilitator-drift-preregistration.json`, `thos/real-arm-temporal-parity-gap.json`, `thos/facilitator-learning-curve-boundary.json`
- Falsifier/acceptance gate: Require preregistered blind matched-budget real arms, repeated facilitator observations, calendar-time modeling, participant and rater evidence, and independent review; any missing element keeps the gap open.
- Rollback/recovery: Retain the proposed design and every failed recruitment or measurement attempt, make no participant claim, and resume only with ethics, consent, governance, and independent-review authority.
- Protected gates: `ethics_approval`, `real_participants`, `blind_matched_budget_arms`, `independent_review`, `thos_superiority`
- Expected disposition, not a result: `open_gap`
- Semantic distinction: Prior THOS work gated burden, fidelity, rater drift, and protocol deviation; none preregistered facilitator learning curves jointly with calendar-time drift and matched-budget real-arm parity.

## V6434-P06 — Controller-delegation attenuation and cyclic-authority refusal graph for Freed ID

- Hypothesis: A static authority graph can require delegated capabilities to attenuate, detect controller cycles, and refuse ambiguous or self-amplifying authority without claiming production interoperability.
- Null/failure: A delegate gains undeclared authority, a controller cycle passes, purpose scope expands, a verification method is treated as governance authority, or fixtures are described as real credentials.
- Approval class: `safe_now_synthetic_only`
- Execution lane: `x2_build_task`
- Official/primary source needs: V6434-S116
- Concrete artifacts: `freed-id/controller-delegation-contract.json`, `freed-id/cyclic-authority-mutation-vectors.json`, `freed-id/production-delegation-boundary.json`
- Falsifier/acceptance gate: Mutate controller edges, delegation depth, purpose, capability set, cycle shape, key material, and claim class; expansion, ambiguity, or cyclic control must fail closed.
- Rollback/recovery: Restore the last acyclic attenuating graph, retain rejected edges, and require standards-conformant real keys, resolution, status, revocation, interoperability, review, and governance for production use.
- Protected gates: `real_keys`, `live_resolution`, `revocation`, `interoperability`, `security_review`, `trust_governance`
- Expected disposition, not a result: `completed`
- Semantic distinction: Earlier Freed ID work covered purpose-bound verification, confused deputies, status, and rotation; none modeled controller cycles and monotonic delegation attenuation together.

## V6434-P07 — Settlement-confidentiality, compelled-disclosure, and public-interest authority gate for CBR

- Hypothesis: Only authorized affected parties and competent authorities can determine whether confidentiality, compelled disclosure, and public-interest obligations are legitimate in a concrete CBR setting.
- Null/failure: A synthetic policy resolves a real conflict of law, confidentiality suppresses protected disclosure by default, Māori wording or authority is inferred, or a legal/cultural conclusion is made without competent authority.
- Approval class: `exact_authority_required`
- Execution lane: `x2_exact_gate_receipt`
- Official/primary source needs: V6434-S117
- Concrete artifacts: `cbr/confidentiality-disclosure-authority-gate.json`, `cbr/public-interest-nonwaiver-vectors.json`, `cbr/affected-party-authority-boundary.json`
- Falsifier/acceptance gate: Any concrete ruling requires authorized affected parties, Māori authorities where Māori concepts or data are involved, competent legal authority, jurisdiction-specific facts, and recorded ratification; absence preserves exact_gate.
- Rollback/recovery: Keep only neutral issue-spotting fields, retain every unresolved authority conflict, and seek authorized cultural and legal review without substituting repository output for authority.
- Protected gates: `affected_party_acceptance`, `maori_authority`, `maori_data_governance`, `legal_interpretation`, `cultural_ratification`, `enacted_law`
- Expected disposition, not a result: `exact_gate`
- Semantic distinction: Prior CBR work addressed jurisdiction, remedy, anti-retaliation, emergencies, and wording authority; none separated settlement confidentiality from compelled disclosure and public-interest authority.

## V6434-P08 — Signed-payload canonicalization and serialization ambiguity tribunal

- Hypothesis: A deterministic static tribunal can distinguish canonicalizable payloads from ambiguous serializations and reject signature assertions when parsers, numbers, duplicate names, or Unicode handling do not preserve the signed meaning.
- Null/failure: Duplicate names pass, numeric representation changes meaning, Unicode is silently normalized, non-finite values pass, or static fixture agreement is called live cryptographic interoperability.
- Approval class: `safe_now_synthetic_only`
- Execution lane: `x2_build_task`
- Official/primary source needs: V6434-S118
- Concrete artifacts: `security/signed-payload-canonicalization-contract.json`, `security/serialization-ambiguity-vectors.json`, `security/cryptographic-interoperability-boundary.json`
- Falsifier/acceptance gate: Mutate member order, duplicate names, negative zero, non-finite numbers, Unicode sequences, whitespace, and signature claims; ambiguity or unsupported interoperability must fail.
- Rollback/recovery: Return to the last byte-explicit fixture, preserve parser disagreement, and require real standards-conformant implementations, keys, and independent security review for interoperability claims.
- Protected gates: `real_keys`, `live_signatures`, `interoperability`, `independent_security_review`, `production_readiness`
- Expected disposition, not a result: `completed`
- Semantic distinction: The nearest earlier tribunal compared multiple parser meanings; this proposal focuses on the exact byte-to-sign contract and canonical-number, Unicode, and duplicate-name failure modes before signature verification.

## V6434-P09 — Floating-point environment, rounding-mode, and cross-architecture parity envelope

- Hypothesis: An environment-explicit envelope can expose rounding-mode and representation dependencies and refuse cross-architecture parity claims unless independently replayed on genuinely different architectures.
- Null/failure: Rounding mode is omitted, signed zero or exceptional values are flattened, decimal/binary conversion is untracked, or same-host replay is called cross-architecture evidence.
- Approval class: `safe_now_synthetic_only`
- Execution lane: `x2_build_task`
- Official/primary source needs: V6434-S119
- Concrete artifacts: `reproduction/floating-environment-contract.json`, `reproduction/rounding-mode-mutation-vectors.json`, `reproduction/cross-architecture-parity-boundary.json`
- Falsifier/acceptance gate: Mutate rounding metadata, precision, signed zero, overflow, underflow, NaN policy, architecture identity, and evidence-owner identity; unsupported parity must fail.
- Rollback/recovery: Restore the last environment-explicit result, retain numeric disagreements, and require independent different-architecture replay before portability promotion.
- Protected gates: `cross_architecture_parity`, `independent_reproduction`, `numeric_proof`, `deployment_readiness`
- Expected disposition, not a result: `completed`
- Semantic distinction: Earlier floating-point work tested edge cases and comparison policy; it did not require rounding-environment metadata or separate same-host repeatability from different-architecture parity.

## V6434-P10 — Time-scale separation and coarse-graining non-substitution evidence board

- Hypothesis: A typed evidence board can show when coarse graining introduces memory or unresolved time scales and prevent an effective description in one pillar from substituting for evidence in another.
- Null/failure: A Markov approximation is assumed without a scale argument, discarded variables vanish from provenance, an effective model becomes a microscopic proof, or a physics proxy is treated as psychological, identity, legal, or cultural evidence.
- Approval class: `safe_now_synthetic_only`
- Execution lane: `x2_build_task`
- Official/primary source needs: V6434-S120
- Concrete artifacts: `thermo-psyche/time-scale-separation-board.json`, `thermo-psyche/coarse-graining-mutation-vectors.json`, `thermo-psyche/non-substitution-boundary.json`
- Falsifier/acceptance gate: Mutate resolved variables, memory kernel, scale ratio, approximation label, pillar, and claim class; silent loss of memory or cross-pillar evidence conversion must fail.
- Rollback/recovery: Restore the last explicit resolved/unresolved split, retain failed approximations, and require domain-specific data, authority, and review for every promoted pillar claim.
- Protected gates: `gmut_derivation`, `thos_real_arms`, `freed_id_production`, `legal_cultural_authority`, `proof_or_canon`
- Expected disposition, not a result: `completed`
- Semantic distinction: Prior non-substitution work protected evidence classes; this proposal adds explicit time-scale separation, projection memory, and resolved-variable provenance as the mechanism preventing conversion.

## Freeze boundary

x2 cannot begin until this x1-only file set is committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote read. Expected counts of 6 completed, 2 represented, 1 open gap, and 1 exact gate are hypotheses about artifact-level execution only; evidence may force a more conservative allowed disposition.
