# Orin Thale v644-v8 x1 preregistration

This is an x1-only freeze. Expected dispositions are not outcomes.

- Exact source: 10beac16b96510b0475d27950d0da3826d79dfe4
- Prior frozen proposals audited: 300
- New proposals: 10
- Effective frozen chain after commit: 310
- Expected distribution: {'completed': 6, 'open_gap': 1, 'represented': 2, 'exact_gate': 1}
- Primary pillar: THOS Body
- Applied practice study: clinical-trial monitoring and statistical practice
- Terminal verdict: NOT_READY_FOR_STAGE_20

## Frozen proposals

### V6448-P01 — Method Flow witness invalidation, environment-drift, and recommendation-demotion ledger

- Expected disposition: completed
- Approval class: safe_now_structural_only
- Hypothesis: A typed Method Flow extension can detect when a previously passing witness no longer matches its declared environment or preconditions and can demote the associated recommendation without deleting either the successful historical witness or the triggering negative.
- Null/failure: A recommendation stays preferred after its witness context changes, demotion overwrites history, drift has no typed reason, a workaround is treated as universal, or a same-owner witness is promoted to independent reproduction.
- Falsifier/gate: Mutate environment fingerprints, trigger preconditions, witness result, retained-negative linkage, and recommendation state; stale witnesses must invalidate or demote without erasing append-only history.
- Recovery: Return the recommendation to candidate, preserve every state event and witness, record the drift reason, and require a new bounded witness before any later promotion.

### V6448-P02 — GMUT decoupling-limit, screening-radius, and regime-overlap obligation tribunal

- Expected disposition: completed
- Approval class: safe_now_research_scaffold
- Hypothesis: A typed synthetic scaffold can reject a claimed screened solution unless inner, transition, and outer regimes declare compatible scales, possess a nonempty overlap domain, and bound their matching residual without treating the scaffold as an observed new force.
- Null/failure: The screening scale is dimensionally inconsistent, the overlap interval is empty, branches are matched outside their assumptions, residuals exceed the frozen tolerance, or synthetic consistency is called empirical confirmation or a unique prediction.
- Falsifier/gate: Mutate scale dimensions, ordering, branch labels, overlap endpoints, residual tolerance, coupling assumptions, and promotion labels; inconsistent or unsupported screening claims must fail closed.
- Recovery: Restore the last typed regime map, retain every rejected vector, mark the screening obligation unresolved, and require model-specific analysis before any stronger statement.

### V6448-P03 — GMUT redshift-space-distortion multipole and Alcock-Paczynski blind public-data study

- Expected disposition: open_gap
- Approval class: safe_now_protocol_only_real_data_required
- Hypothesis: A preregistered blind adapter could test a frozen GMUT growth-and-geometry model against official clustering multipoles only if exact released rows, covariance, window functions, nuisance priors, baseline, and analysis lock are obtained and reviewed before unblinding.
- Null/failure: No real rows are ingested, covariance or window operators are absent, nuisance choices are post-hoc, the baseline is missing, released products cannot support the declared estimand, or synthetic fixtures are reported as a likelihood result.
- Falsifier/gate: Require nonzero official rows, exact covariance and window provenance, a frozen baseline, nuisance lock, withheld outcome labels, and independent review; any missing element keeps the study open.
- Recovery: Retain the zero-row and missing-input receipts, perform no fit, publish no likelihood or constraint, and reopen only under a separately reviewed real-data protocol.

### V6448-P04 — THOS blinded sample-size re-estimation and nuisance-variance firewall

- Expected disposition: represented
- Approval class: safe_now_proxy_only
- Hypothesis: A synthetic protocol can distinguish a blinded nuisance-variance update from an outcome-informed adaptation by sealing treatment labels, prespecifying the information target, and rejecting any path that exposes arm-specific effects or silently changes the matched budget.
- Null/failure: Arm labels or comparative effects enter the update, the variance rule is selected after outcomes, the information target moves, budget parity is lost, participant harms are ignored, or proxy fixtures are called a real-arm superiority result.
- Falsifier/gate: Mutate treatment-label visibility, variance source, timing, information target, sample-size cap, budget parity, adverse-event reservation, and result language; any unblinding or post-hoc change must fail.
- Recovery: Restore the frozen synthetic protocol, retain contaminated vectors, label the work proxy, and require preregistered blind matched-budget real arms, participants, raters where applicable, and independent review.

### V6448-P05 — Freed ID OpenID4VCI credential-offer, nonce, and proof-of-possession binding profile

- Expected disposition: represented
- Approval class: safe_now_synthetic_identity_profile
- Hypothesis: A synthetic structural profile can reject issuance transcripts that cross-bind credential offers, issuer metadata, nonces, proof audiences, or holder keys, while reserving real cryptographic and interoperability assurance.
- Null/failure: An offer resolves to the wrong issuer, configuration identifiers drift, nonce freshness is absent, proof audience or key binding is mismatched, replay is accepted, or synthetic keys are described as production identity evidence.
- Falsifier/gate: Mutate issuer identity, offer transport, configuration identifier, nonce freshness, proof audience, holder key, credential response, and replay state; mismatches must reject deterministically.
- Recovery: Return to the last valid synthetic state, retain every rejected transcript, expose no real key material, and require real standards-conformant keys, live issuance, resolution, status, revocation, interoperability, privacy and security review, and trust governance for production.

### V6448-P06 — CBR remedy-fund insolvency, creditor-priority, and ring-fencing authority gate

- Expected disposition: exact_gate
- Approval class: exact_authority_gate
- Hypothesis: A refusal-first authority matrix can show that software evidence cannot determine whether remedy assets are ring-fenced, trust property, preferential, recoverable, or distributable during insolvency without competent legal authority, affected-party participation, and Maori authority where relevant.
- Null/failure: The phase assigns legal priority, assumes a trust, selects beneficiaries, discloses claimant data, substitutes consultation for authority, treats Maori concepts as software-owned, or reports an unenacted remedy structure as law.
- Falsifier/gate: Every scenario involving asset character, creditor rank, trust status, transfer, disclosure, beneficiary selection, Maori wording, or remedy authority must remain refused unless the exact competent authorities and affected parties provide evidence for that decision.
- Recovery: Revert to unknown and exact-gated, preserve the refusal case, expose no beneficiary data, and route the issue to competent legal authorities, affected parties, and Maori authorities without drafting their conclusion.

### V6448-P07 — Git submodule gitlink, nested-repository, and checkout-visibility tribunal

- Expected disposition: completed
- Approval class: safe_now_read_only_tooling
- Hypothesis: A read-only family-compatible classifier can distinguish ordinary directories, declared gitlinks, deinitialized submodules, and undeclared nested repositories so that manifest and privacy claims cannot silently skip an opaque repository boundary.
- Null/failure: A gitlink is hashed as an ordinary directory, an undeclared nested repository is ignored, deinitialized content is assumed present, a remote is fetched, or a path outside the allowed root is traversed.
- Falsifier/gate: Exercise ordinary trees, mode-160000 entries, declared and undeclared nested repositories, missing worktrees, malicious paths, and network-required states; ambiguous or out-of-root cases must fail closed without fetching.
- Recovery: Stop traversal, retain the opaque-boundary witness, make no network or repository mutation, and require explicit owner review before including or excluding the nested object.

### V6448-P08 — CSS generated-content, icon-only state, and print-suppression accessibility audit

- Expected disposition: completed
- Approval class: safe_now_structural_accessibility
- Hypothesis: A bounded structural audit can reject a static report when essential status or gate meaning exists only in CSS pseudo-elements, symbolic icons, background images, or screen-only content omitted from print.
- Null/failure: A status loses meaning when styles are disabled, an icon has no visible and programmatic text, print suppresses essential evidence, automated checks are called complete accessibility, or affected-user evaluation is treated as optional evidence already supplied.
- Falsifier/gate: Strip CSS, inspect pseudo-elements, icon-only nodes, background images, hidden print rules, accessible names, headings, landmarks, tables, and links; essential semantics must remain textual and printable.
- Recovery: Restore explicit visible text, remove meaning-bearing decoration, retain each structural failure, and reserve manual keyboard, zoom, reflow, screen-reader, print, and affected-user evaluation.

### V6448-P09 — Zeroth-law transitivity, intensive-variable equilibration, and psyche-harmony nonconversion classifier

- Expected disposition: completed
- Approval class: safe_now_classification_only
- Hypothesis: A typed classifier can preserve thermal-equilibrium transitivity and temperature-measurement conditions while rejecting any inference that interpersonal agreement, emotional harmony, or psychological similarity is a thermodynamic equilibrium relation.
- Null/failure: A psyche label is assigned temperature units, social agreement is made transitive by analogy, equilibrium is inferred without thermal contact conditions, participant evidence is invented, or a metaphor is promoted to a scientific law.
- Falsifier/gate: Mutate units, relation domains, contact conditions, transitivity premises, measurement objects, participant labels, and conclusion strength; cross-domain conversion must reject.
- Recovery: Return the statement to metaphor or unknown, retain the rejected mapping, and require domain-valid thermodynamic measurements or separately authorized participant research for any empirical claim.

### V6448-P10 — Stage 20 randomized evidence-challenge, audit-yield, and tamper-detection board

- Expected disposition: completed
- Approval class: safe_now_decision_rehearsal
- Hypothesis: A synthetic board can show whether a precommitted random challenge sample would expose missing or altered evidence more reliably than convenience review while refusing to convert a clean sample into readiness or exhaustive-security assurance.
- Null/failure: The sample is chosen after inspection, randomness provenance is absent, withheld items are silently excluded, a clean sample closes exact gates, or same-owner audit yield is called independent review.
- Falsifier/gate: Mutate seed provenance, sample frame, selection timing, missing-item treatment, tamper flags, clean-sample interpretation, exact gates, and reviewer independence; biased or overpromoted boards must fail.
- Recovery: Reopen the board, retain the failed sampling receipt, restore every open and exact gate, and require competent external decision makers and independent evidence before Stage 20.

## Boundary

No x2 implementation or result exists in this freeze. No empirical, participant, production, legal, cultural, Māori-authority, AGI/ASI, consciousness/personhood, proof/canon, Theory-of-Everything, deployment, exhaustive-security, complete-accessibility, independent-reproduction, or Stage 20 claim is made.
