---
name: ghc-family-event-rollback-reachability-v1
description: "Use when a bounded public-synthetic workflow record needs the rollback_reachability check while gaps and protected authority stay explicit."
---

# ghc-family-event-rollback-reachability-v1

## Purpose

Compute rollback reachability in the declared finite transition graph without authorizing a live rollback.

## Procedure

1. Require the planning-frozen public-synthetic fixture and exact `rollback_reachability` operation.
2. Run `scripts/smoke.py` or the family-current X2 contract runner.
3. Retain malformed subjects as zero-credit failures and keep `open_gap` or `exact_gate` dispositions unchanged.
4. Report only the finite observation and digest; infer no live service, external action, real-world outcome, or authority.

## Boundaries

Finite synthetic same-owner event-workflow and 3D graph-model evidence only. No live service, real participant, external action, empirical GMUT confirmation, production THOS or Freed ID, complete privacy or accessibility, exhaustive security, professional, legal, cultural, affected-party or Maori authority, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.
