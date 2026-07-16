# GHC Family Method Flow State

- Phase: v646-gmut-thos-v3-x1-x2
- Owner: Sable Rook
- Methods: 4
- Passing witnesses: 4
- Failed witnesses retained: 5

## Preferred methods

### V6463-M01 — Bounded direct-path shell-startup probe

- Trigger: known owner paths are available; a broad D-drive listing would add no evidence; ordinary user privileges only
- Method: Use direct known-path probes with login-profile startup disabled and a measured sixty-second upper bound.
- Recurrence guard: Avoid broad archive-root enumeration; use known paths, disable login startup, and keep the command bound at or below sixty seconds.
- Rollback: Stop the probe without mutation and retain unavailable state if the widened bounded envelope also fails.
- Witnesses: V6463-M01-F1, V6463-M01-F2, V6463-M01-P

### V6463-M02 — Array-before-pipeline PowerShell sequencing

- Trigger: PowerShell foreach output must feed a later pipeline; the operation is read-only
- Method: Materialize foreach output as an array and pipe only the completed array.
- Recurrence guard: Wrap foreach output in an array before formatting or filtering it.
- Rollback: Stop before any command executes and rerun only the read-only query with array materialization.
- Witnesses: V6463-M02-F, V6463-M02-P

### V6463-M03 — Windows ripgrep glob-filter guard

- Trigger: versioned files must be searched on Windows; literal wildcard paths are unsupported
- Method: Pass concrete directories to ripgrep and constrain filenames with -g filters.
- Recurrence guard: Use rg -g for wildcard selection on Windows rather than wildcard path arguments.
- Rollback: Treat the failed search as no result and rerun against real directories with filters.
- Witnesses: V6463-M03-F, V6463-M03-P

### V6463-M04 — Two-layer proposal and support collision quarantine

- Trigger: core and expanded portfolios are both frozen; predecessor artifacts are immutable
- Method: Retain the collision receipt, rewrite only exact title collisions, and rerun the full support-title comparison.
- Recurrence guard: Require both core-proposal and support-portfolio collision counts to be zero before x1 review.
- Rollback: Reject the candidate build, preserve the failed collision list, and edit only Sable-owned definitions.
- Witnesses: V6463-M04-F, V6463-M04-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
