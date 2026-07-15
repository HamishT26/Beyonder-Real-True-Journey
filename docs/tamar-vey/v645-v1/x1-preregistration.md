# Tamar Vey v645-v1 x1 preregistration

This is an x1-only freeze. Expected dispositions are not outcomes.

- Exact source: a6c869a44eb7d3fe32ba80bc64964aa7903531c2
- Prior frozen proposals audited: 310
- New proposals: 10
- Effective frozen chain after commit: 320
- Expected distribution: {'completed': 6, 'open_gap': 1, 'represented': 2, 'exact_gate': 1}
- Primary pillar: Freed ID/CBR Heart
- Applied practice study: public-interest fund administration and fiduciary governance
- Terminal verdict: NOT_READY_FOR_STAGE_20

## Frozen proposals

### V6451-P01 — Method Flow child-process start attestation, evidence-credit, and preflight-failure ledger

- Expected disposition: completed
- Approval class: safe_now_structural_only
- Hypothesis: A typed Method Flow extension can distinguish a parser or launcher failure that executes no evidence-producing child command from a started child process and can withhold replay credit unless a bounded start and completion receipt exist, while retaining every failed attempt.
- Null/failure: A parser-failed wrapper receives replay credit, a missing start marker is inferred from intent, a timed-out child is called complete, a retry erases the original negative, or a same-owner start receipt is promoted to independent reproduction.
- Falsifier/gate: Mutate parser outcome, launcher outcome, child start token, command fingerprint, completion receipt, timeout state, retained-negative link, and replay count; only one actually started and successfully completed bounded child may receive replay credit.
- Recovery: Return the attempt to zero-credit observed failure, retain its negative, repair only the wrapper or launcher, and require a new bounded child-start and completion witness before promotion.

### V6451-P02 — GMUT adiabatic-mode, soft-limit, and gauge-artifact obligation tribunal

- Expected disposition: completed
- Approval class: safe_now_research_scaffold
- Hypothesis: A typed synthetic tribunal can reject a claimed cosmological soft-limit relation unless the long-wavelength mode, residual gauge transformation, regularity assumptions, constraint equations, and conserved quantity are stated consistently without treating the relation as an observed GMUT prediction.
- Null/failure: A gauge artifact is counted as a physical mode, the long-wavelength limit is taken outside declared regularity assumptions, entropy or anisotropic-stress terms are silently omitted, dimensions or perturbative orders conflict, or synthetic consistency is called empirical confirmation.
- Falsifier/gate: Mutate wave-number scaling, gauge generator, regularity, constraint satisfaction, entropy source, anisotropic stress, conserved-variable definition, perturbative order, and promotion language; inconsistent or unsupported relations must fail closed.
- Recovery: Restore the last typed assumption set, retain every rejected vector, mark the soft-limit obligation unresolved, and require model-specific analysis and real observations before any stronger statement.

### V6451-P03 — GMUT late-time integrated Sachs-Wolfe galaxy-cross-correlation blind public-data study

- Expected disposition: open_gap
- Approval class: safe_now_protocol_only_real_data_required
- Hypothesis: A preregistered blind adapter could compare a frozen GMUT late-time potential-evolution model with an official CMB-galaxy cross-correlation only if exact maps or released spectra, masks, tracer kernels, covariance, nuisance assumptions, a baseline, and an independent review lock are present before unblinding.
- Null/failure: No real rows or maps are ingested, mask or tracer-window provenance is absent, cross-covariance is improvised, foreground or look-elsewhere choices are post-hoc, the baseline is missing, or synthetic fixtures are reported as a likelihood or constraint.
- Falsifier/gate: Require nonzero official inputs, exact map and mask lineage, tracer selection kernels, covariance, frozen nuisance treatment, a declared baseline, withheld decision labels, and independent review; any missing element keeps the study open.
- Recovery: Retain the zero-row and missing-input receipts, run no fit, publish no likelihood or parameter constraint, and reopen only under a separately reviewed real-data protocol.

### V6451-P04 — THOS independent data-monitoring firewall, operational-bias, and recommendation-minimization protocol

- Expected disposition: represented
- Approval class: safe_now_proxy_only
- Hypothesis: A synthetic protocol can distinguish a bounded monitoring recommendation from leakage of comparative interim data by sealing role permissions, separating open and closed materials, minimizing recommendation content, and rejecting operational changes that reveal arm-specific trends or break matched-budget parity.
- Null/failure: Unblinded tables reach operational staff, recommendation wording reveals comparative effects, sponsor queries reconstruct interim outcomes, role conflicts are ignored, budget parity changes, participant safeguards are omitted, or proxy messages are called a real-arm superiority result.
- Falsifier/gate: Mutate role membership, session visibility, report granularity, recommendation text, sponsor query paths, operational response, adverse-event reservation, matched budget, and result language; any reconstructable comparative signal or unauthorized adaptation must fail.
- Recovery: Restore the frozen synthetic role matrix, retain contaminated messages, label the work proxy, and require preregistered blind matched-budget real arms, participant safeguards, competent monitoring authority, and independent review.

### V6451-P05 — Freed ID OpenID Federation trust-chain, entity-statement expiry, and policy-operator profile

- Expected disposition: represented
- Approval class: safe_now_synthetic_identity_profile
- Hypothesis: A synthetic structural profile can reject federation chains whose issuer-subject linkage, signature-key reference, expiry ordering, authority-hint path, trust anchor, or metadata-policy operator application is inconsistent while reserving real cryptographic and interoperability assurance.
- Null/failure: A chain skips an authority edge, trusts an expired statement, applies an unsupported policy operator, accepts a key rollover without linkage, chooses an undeclared trust anchor, or describes synthetic signatures as production identity assurance.
- Falsifier/gate: Mutate issuer, subject, authority hints, trust anchor, statement expiry, signing key, key rollover, chain ordering, policy operator, metadata result, and replay state; malformed or unsupported chains must reject deterministically.
- Recovery: Return to the last valid synthetic chain, retain every rejected transcript, expose no real key material, and require standards-conformant real keys and proofs, live federation resolution, interoperability, privacy and security review, and trust governance for production.

### V6451-P06 — CBR remedy-fund investment mandate, inflation-risk, and loss-allocation authority gate

- Expected disposition: exact_gate
- Approval class: exact_authority_gate
- Hypothesis: A refusal-first authority matrix can show that software evidence cannot select a remedy-fund investment mandate, risk tolerance, inflation objective, liquidity reserve, service provider, or loss-allocation rule without competent fiduciary and legal authority, affected-party participation, and Maori authority where relevant.
- Null/failure: The phase recommends an asset allocation, sets a return target, assigns losses, chooses custodians or advisers, reveals beneficiary data, substitutes consultation for authority, treats Maori concepts as software-owned, or reports a proposed mandate as enacted law.
- Falsifier/gate: Every scenario involving investment objective, risk, liquidity, inflation, delegation, fees, conflicts, loss allocation, disclosure, beneficiary selection, Maori wording, or remedy authority must remain refused unless exact competent authorities and affected parties provide evidence for that decision.
- Recovery: Revert to unknown and exact-gated, preserve the refusal case, expose no beneficiary data, and route the issue to competent fiduciary and legal authorities, affected parties, and Maori authorities without drafting their conclusion.

### V6451-P07 — Git LFS pointer, materialized-object, and missing-content boundary tribunal

- Expected disposition: completed
- Approval class: safe_now_read_only_tooling
- Hypothesis: A read-only family-compatible classifier can distinguish ordinary Git blobs, valid and malformed LFS pointers, materialized LFS content, and pointer-only missing-content states so a manifest or privacy claim cannot silently treat a small pointer as the referenced large object.
- Null/failure: A pointer is hashed as if it were materialized content, malformed keys or sizes are accepted, missing objects are called complete, the classifier fetches from a network, or an out-of-root object path is traversed.
- Falsifier/gate: Exercise ordinary blobs, canonical pointers, wrong versions, non-SHA-256 identifiers, size mismatches, extension lines, oversized pointers, missing objects, materialized content, malicious paths, and network-required states; ambiguity must fail closed without fetching.
- Recovery: Stop classification, retain the opaque-content witness, make no network or repository mutation, and require explicit owner review before including or excluding the referenced object from a manifest or privacy claim.

### V6451-P08 — Color-only status, contrast-token, and monochrome-redundancy accessibility audit

- Expected disposition: completed
- Approval class: safe_now_structural_accessibility
- Hypothesis: A bounded structural audit can reject a static report when completion, warning, gap, or gate meaning is conveyed only by hue or when declared foreground-background tokens fail frozen contrast calculations, while preserving visible textual status and a monochrome cue.
- Null/failure: A red or green state has no text label, adjacent graphical states rely only on hue, a contrast token is missing or below the frozen ratio, automated calculations are called complete accessibility, or manual and affected-user evaluation are treated as already supplied.
- Falsifier/gate: Remove color, convert the report to a monochrome state map, inspect visible status text and redundant marks, calculate frozen token contrasts, and inspect headings, landmarks, tables, and links; color-dependent or under-contrast fixtures must fail.
- Recovery: Restore explicit visible text and redundant shapes or borders, replace failing color tokens, retain each structural failure, and reserve manual keyboard, zoom, reflow, screen-reader, print, color-perception, and affected-user evaluation.

### V6451-P09 — Heat-capacity response, convexity stability, and psyche-resilience nonconversion classifier

- Expected disposition: completed
- Approval class: safe_now_classification_only
- Hypothesis: A typed classifier can preserve heat-capacity definitions, constraint conditions, units, and stability caveats while rejecting any inference that emotional resilience, social adaptability, or psychological coping is a heat capacity or thermodynamic convexity relation.
- Null/failure: A psyche label receives joules per kelvin, constant-pressure and constant-volume quantities are interchanged, a negative response is interpreted without domain conditions, participant evidence is invented, or an analogy is promoted to a fundamental law.
- Falsifier/gate: Mutate units, derivative variables, pressure or volume constraints, sign, stability premises, phase domain, psyche labels, participant fields, and conclusion strength; cross-domain conversion must reject.
- Recovery: Return the statement to metaphor or unknown, retain the rejected mapping, and require domain-valid thermodynamic measurements or separately authorized participant research for any empirical claim.

### V6451-P10 — Stage 20 circular-support, self-citation, and bootstrap-evidence rejection board

- Expected disposition: completed
- Approval class: safe_now_decision_rehearsal
- Hypothesis: A synthetic decision board can reject a readiness argument whose apparent support is generated only by a cycle of mutually citing receipts, while preserving legitimate acyclic derivations and refusing to let repeated internal references substitute for an external evidence root.
- Null/failure: A strongly connected support component is counted as multiple independent roots, a receipt cites its own derived output, duplicate internal references increase assurance, exact gates are closed by graph density, or same-owner structure is called independent review.
- Falsifier/gate: Mutate support edges, self-loops, derived-artifact roots, duplicated citations, strongly connected components, withdrawn sources, exact gates, and reviewer labels; rootless cycles or overpromoted boards must fail.
- Recovery: Reopen the board, retain the failed support graph, collapse circular components to zero independent-root credit, restore every open and exact gate, and require competent external decision makers and independent evidence before Stage 20.

## Boundary

No x2 implementation or result exists in this freeze. No empirical, participant, production, legal, cultural, Māori-authority, AGI/ASI, consciousness/personhood, proof/canon, Theory-of-Everything, deployment, exhaustive-security, complete-accessibility, independent-reproduction, or Stage 20 claim is made.
