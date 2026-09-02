# GHC Family Method Flow State

- Phase: v684-v6-x2
- Owner: Caelen Ash
- Methods: 2
- Passing witnesses: 2
- Failed witnesses retained: 2

## Preferred methods

### CA6846-M013 — Inspect persisted review state after a wrapper-window crossing

- Trigger: A deterministic staged-review wrapper returns without an attributable final projection while its exact child process may still be active.
- Method: Inspect only the exact child process, wait without replay, and then read the persisted review and index scalars.
- Recurrence guard: Retain the failure, inspect the smallest exact persisted surface, and do not replay an already-successful review.
- Rollback: Return to the immutable x1 head and exact staged allowlist without widening scope.
- Witnesses: CA6846-M013-WF01, CA6846-M013-WP01

### CA6846-M014 — Repair one exact staged diff-hygiene dependency

- Trigger: A persisted staged review fails only because an owner-local Python file has a trailing blank line.
- Method: Remove only the trailing blank line, restage that exact file, and rerun the bounded staged review once.
- Recurrence guard: Retain the failure, inspect the smallest exact persisted surface, and do not replay an already-successful review.
- Rollback: Return to the immutable x1 head and exact staged allowlist without widening scope.
- Witnesses: CA6846-M014-WF01, CA6846-M014-WP01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
