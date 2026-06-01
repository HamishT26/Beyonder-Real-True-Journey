# v467A GMUT v7 x1 Lint Readiness Packet

Prepared: 2026-06-01T22:11:46+12:00

This packet defines lint readiness only. No lint rule was executed as a physics fixture.

## Derived Lint Report

Each derived report includes report ID, input row ID, lint status, failure codes, blocked claims, missing fields, forbidden fields detected, and unchanged-open gate carry.

Valid lint statuses are `SCHEMA_ACCEPTED_NO_CLAIM`, `HOLD_OPEN_GAP`, and `FAIL_FATAL`.

## Fatal Rules

Fatal rules block missing source anchors, empty affected-expression refs, forbidden result fields, non-open gate verdicts, `B_Psi` promotion, specified `V(Psi)` without rules, and Journey/Solas overpromotion.

## Hold-Open Gaps

Hold-open gaps include missing exact baseline artifact, missing reference-state boundary conditions, expected output not shape-only, residual tolerance without units/threshold/mode, incomplete switch-leakage policy, missing fifth-force parameter map, and missing consciousness proxy protocol.

Schema accept is not a result. All six GMUT gates remain `OPEN_NOT_TESTED`.
