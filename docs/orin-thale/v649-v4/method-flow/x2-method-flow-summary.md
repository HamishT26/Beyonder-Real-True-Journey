# GHC Family Method Flow State

- Phase: v649-gmut-thos-v4-x2
- Owner: Orin Thale
- Methods: 3
- Passing witnesses: 3
- Failed witnesses retained: 3

## Preferred methods

### V6494-X2-M01 — Windows ripgrep explicit-root x2 inventory

- Trigger: Windows filesystem; multiple phase Python files; stale-token inventory
- Method: Use explicit roots and ripgrep -g filename filters instead of literal wildcard path arguments.
- Recurrence guard: Never pass shell-style wildcard path arguments to ripgrep on Windows; use explicit roots and -g includes.
- Rollback: Discard the incomplete inventory and leave repository content unchanged.
- Witnesses: V6494-X2-M01-WFAIL, V6494-X2-M01-WPASS

### V6494-X2-M02 — Precommit successor-baton completeness preflight

- Trigger: sanitized successor pointer; declared word floor; terminal route held
- Method: Expand the pointer with substantive verified truth and protected-gate instructions, then remeasure before evidence commit.
- Recurrence guard: Measure generated baton text before evidence commit and require its declared lower and upper bounds without padding it with claims.
- Rollback: Write no baton artifact and leave the route PREPARED_NOT_SENT.
- Witnesses: V6494-X2-M02-WFAIL, V6494-X2-M02-WPASS

### V6494-X2-M03 — Isolated evidence postflight after review completion

- Trigger: passed staged review; large checkout; nested status summary timeout
- Method: Separate staged-review credit from status postflights and compare precomputed manifest and x1 path sets.
- Recurrence guard: Do not group a successful staged review with nested large-checkout Git summaries; isolate each postflight and compare precomputed path sets.
- Rollback: Retain the successful staged-review receipt, discard the incomplete summary, and leave the index unchanged until isolated probes finish.
- Witnesses: V6494-X2-M03-WFAIL, V6494-X2-M03-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
