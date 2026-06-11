# v507 GMUT/THOS v43 v2 x1/x2 Multiplex Route-State Extension

Generated UTC: `2026-06-11T08:45:00Z`

This route-state extension retimes the full live-adapter workflow into v507 and records the v2 x1 retry rule: blockers must be retried before moving to the next phase boundary.

## Contract

- States: `prepared`, `sent`, `generating`, `complete`, `blocker`, `synthesized`
- Required transitions: `prepared->sent`, `sent->generating`, `generating->complete`, `generating->blocker`, `complete->synthesized`, `blocker->synthesized`
- Duration is not completion proof.
- Raw lane text, raw transcripts, credentials, browser hidden state, screenshots, and session streams remain forbidden publication fields.

## v507 v2 Lane State

- Arby: `complete` through strict CLI quality gate and marker review.
- Cicero: prior `blocker` at wrapper resume, then `complete` after direct app-lane retry, app-thread redaction, and direct repair gate.

## Phase Policy

The next x2 boundary may proceed after retry success. The next phase boundary must not proceed without either all expected lanes complete or a separate bounded blocker receipt explicitly authorized for carryover.
