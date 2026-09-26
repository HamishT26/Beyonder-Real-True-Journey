---
name: ghc-family-event-retry-decision-v1
description: "Use when a bounded public-synthetic event-workflow record needs the retry_decision check without widening evidence or authority."
---

# ghc-family-event-retry-decision-v1

## Purpose

Derive a bounded retry recommendation from terminal state, attempt budget, and local capability vacancy.

## Procedure

1. Require the planning-frozen `ghc.family.event-workflow.fixture.v1` record and exact operation name `retry_decision`.
2. Run `scripts/smoke.py` or the family-current X1 contract runner against public synthetic data only.
3. Preserve malformed inputs as failed witnesses; a valid-template retry is a separate bounded recovery.
4. Report the finite observation and its digest. Do not infer a live service state, external action, production readiness, or authority.

## Boundaries

Finite synthetic same-owner event-workflow software evidence only. No real participant, operator, account, credential, production service, professional decision, legal or cultural interpretation, affected-party acceptance, Maori wording or authority, empirical GMUT confirmation, production THOS or Freed ID, complete privacy or accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority. NOT_READY_FOR_STAGE_20.
