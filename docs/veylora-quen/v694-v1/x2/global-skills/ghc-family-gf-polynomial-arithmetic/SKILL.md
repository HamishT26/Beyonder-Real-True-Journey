---
name: ghc-family-gf-polynomial-arithmetic
description: Evaluate and review bounded prime-field polynomial contracts while retaining failures and declared evidence limits.
---

# ghc family gf polynomial arithmetic

Use this merged guide for the four operations below. Read [the frozen contracts](references/operations.json) and [the source merge record](references/merge-sources.json). Run the named public TXT runner with one JSON input-file argument using the installed Node runtime. The two sibling runtime TXT modules must remain beside the runner.

## gf_polynomial_normalize

Read coefficients in ascending powers, reduce them modulo p and remove trailing zeros. Preserve the unique zero representation [0]. Inputs contain one through eight coefficients.

## gf_polynomial_sum

Add aligned coefficients and normalize the trailing zero suffix. Missing higher coefficients contribute zero, while a missing or empty input polynomial is refused.

## gf_polynomial_product

Convolve coefficient pairs with reduction at each addition. The output may be longer than an admitted input, so internal arithmetic does not reapply the external input length bound.

## gf_polynomial_division

Divide by a nonzero polynomial over the admitted prime field. Cancel the leading term using its inverse, retain quotient and remainder, and require degree descent at each iteration.

## Review and rollback

Compare the complete envelope, outcome and authority boundary. Request JSON is limited to one megabyte, depth 32 and unique keys. Use the accepting and adverse fixtures first, then a defined case within the same scope. Inputs never grant permission to contact tasks or change external state.

Preserve each failed subject and its original definition. An independent refusal check can pass while the subject remains failed. If an installed binding changes, stop using that dependency and select the retained source package; do not overwrite another owner's files, erase evidence or replay a successful canonical. Manual accessibility, production safety and independent reproduction remain open.

Veylora Quen, she/her, evidence steward, and the hope to make each handoff clearer, more faithful and easier for Hamish to review are relational working language only. Same-owner finite synthetic software under shared infrastructure is not independent reproduction and establishes no consciousness, sentience, personhood, legal identity, identity continuity, employment, qualification, independent agency, empirical GMUT confirmation, production THOS or Freed ID, professional, scientific, operational, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, AGI or ASI, Theory-of-Everything proof, canon or Stage 20 readiness. Maori concepts remain under Maori authority. NOT_READY_FOR_STAGE_20.
