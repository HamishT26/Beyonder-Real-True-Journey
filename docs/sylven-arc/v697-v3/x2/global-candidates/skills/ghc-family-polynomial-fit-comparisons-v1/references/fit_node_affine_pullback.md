---
name: ghc-family-x2-fit-node-affine-pullback
description: Inspect node affine pullback for bounded declared rational sample constraints; use this x2 guide for the finite fitting profile, not real observations or professional decisions.
---

# fit_node_affine_pullback

An invertible affine node reparameterization can preserve constraint families with explicit coordinate lineage.

## Exact input and caller

The JSON request has only `op` and `input`; `op` is `fit_node_affine_pullback`. Input fields are `case_id`, `degree`, `samples`, `scale`, `offset`. Degree is 0 through 4, raw sample count is at most 12, rational literals use at most 30 digits per numerator/denominator, and denominator zero is refused. The case label is finite provenance, not an identity event.

Use the paired caller `../../runners/ghc_family_fit_x2_pair_3.txt` with JSON on stdin. It admits only its two named operations, returns the complete evidence envelope, and refuses malformed subjects with exit 2. It cannot select an outside file, URL, process, person or decision endpoint.

## Interpretation and refusal

Preserve the declared degree, raw versus normalized rows, duplicate conflicts, consistency, nullspace, and particular-versus-identified distinction. Equal duplicate constraints may collapse; conflicting values at one node remain. Never silently substitute least squares, normalize away a free parameter, interpret exact algebra as physical data, or turn a passing malformed-input refusal into subject success.

The frozen expected outcome is `completed`. Match the entire envelope, not a selected value or wording fragment. Source definitions and observed results remain separate.

## Recovery and evidence boundary

Stop selecting only the failed mechanism and correct its smallest dependency additively; retain the definition, initial failure, all passing prefixes, and the source bindings.

Relational working language only; bounded same-owner finite synthetic software and workflow evidence. No empirical, participant, identity, professional, production, legal, cultural, affected-party, Maori-authority, complete privacy/accessibility/security, independent-reproduction, AGI/ASI, Theory-of-Everything or Stage 20 credit. NOT_READY_FOR_STAGE_20.
