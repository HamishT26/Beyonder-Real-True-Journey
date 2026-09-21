---
name: ghc-family-finite-evidence-frame-v1
description: Validate bounded finite evidence frames, focal masks, and exact rational mass records without promoting them into human belief, observation, identity, or authority claims.
---

# Finite Evidence Frame v1

Use this guide when a task needs a small, declared finite frame and exact mass assignments over its subset masks.

## Required input

- A non-empty `frame` array of unique labels.
- A `mass` array whose rows contain an integer subset `mask` and an exact rational `value`.
- A declared synthetic purpose and a refusal boundary.

## Method

1. Reject duplicate or empty frame labels.
2. Reject masks outside `0..(2^frame.length)-1`.
3. Parse each rational exactly; never silently coerce a decimal approximation.
4. Require non-negative masses and an exact total of one.
5. Preserve the empty-subset row if present instead of hiding conflict or malformed input.
6. Record the finite frame and source status beside every derived result.

## Boundaries

This validates a finite software record only. A field named belief, plausibility, evidence, or mass is mathematical vocabulary, not a measurement of a person's beliefs, a physical datum, an identity fact, or an authority decision. Do not infer empirical confirmation, participant evidence, professional competence, legal effect, cultural legitimacy, Maori authority, production readiness, consciousness, personhood, or Stage 20 status.

## Output

Return a normalized finite-frame record, exact acceptance or rejection reasons, and a reversible provenance reference. Retain invalid subjects at zero completion credit.
