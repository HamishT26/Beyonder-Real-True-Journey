# GHC Family Method Flow State

- Phase: v647-gmut-thos-v7-x1-x2
- Owner: Sable Rook
- Methods: 3
- Passing witnesses: 3
- Failed witnesses retained: 3

## Preferred methods

### V6477-M01 — No-profile bounded full skill read after short-wrapper timeout

- Trigger: A required local instruction file remains unread after a bounded short-wrapper timeout.
- Method: Retain the timeout, disable profile startup for the read, extend the wrapper to sixty seconds, and read the unchanged file through EOF.
- Recurrence guard: Do not repeat the same short wrapper; use the observed no-profile startup envelope for required full reads.
- Rollback: Stop the read, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6477-M01-WFAIL, V6477-M01-WPASS

### V6477-M02 — Exact inherited portfolio-title collision quarantine

- Trigger: New owner portfolio labels are compared with inherited phase portfolio ledgers before materialization.
- Method: Stop before packet materialization, preserve the exact collision list, rewrite only the Sable labels while retaining their gates, and rerun the unchanged audit.
- Recurrence guard: Require zero inherited and zero within-current exact title collisions before generating any proposal packet.
- Rollback: Leave the source and generated Method Flow evidence intact; do not materialize the proposal packet until the audit passes.
- Witnesses: V6477-M02-WFAIL, V6477-M02-WPASS

### V6477-M03 — Exact-path ripgrep recovery for Windows wildcard faults

- Trigger: A Windows stale-label or content search spans generated filenames selected by a wildcard.
- Method: Use rg --files to enumerate matching files and pass exact paths to the content search.
- Recurrence guard: Never pass an unexpanded Windows wildcard as an rg path argument; enumerate then search exact paths.
- Rollback: Retain partial read-only output and rerun only the failed search surface; mutate no repository state.
- Witnesses: V6477-M03-WFAIL, V6477-M03-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
