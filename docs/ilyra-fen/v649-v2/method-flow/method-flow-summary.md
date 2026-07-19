# GHC Family Method Flow State

- Phase: v649-gmut-thos-v2-x1-x2
- Owner: Ilyra Fen
- Methods: 4
- Passing witnesses: 4
- Failed witnesses retained: 4

## Preferred methods

### v6492-m01 — Split required skill reads by file

- Trigger: multiple required instruction files; bounded tool output
- Method: Read each required file separately with raw content through EOF, then proceed only after every output completes.
- Recurrence guard: Never combine required full-file reads when the aggregate may exceed the model output boundary.
- Rollback: Stop after any truncated output; make no repository change and restart only the unproved read as a separate bounded probe.
- Witnesses: v6492-m01-wfail, v6492-m01-wpass

### v6492-m02 — Probe named worktrees instead of enumerating the shared bank

- Trigger: large inherited worktree bank; only two named lanes are in scope
- Method: Probe path existence, Git metadata, exact refs, and clean state only for the named source and owned lane.
- Recurrence guard: Do not run broad shared-bank enumeration when exact named paths and refs are already authorized.
- Rollback: Stop the broad probe; preserve the timeout and leave all worktrees untouched.
- Witnesses: v6492-m02-wfail, v6492-m02-wpass

### v6492-m03 — Normalize expected-empty ripgrep exit state

- Trigger: read-only search; zero matches is an expected valid result
- Method: Capture output and accept exit codes 0 or 1; reject only codes greater than 1, then assert the explicit match count.
- Recurrence guard: Every expected-empty rg probe must distinguish no-match from execution failure.
- Rollback: Stop after an ambiguous wrapper result; do not infer absence until an explicit zero-line witness passes.
- Witnesses: v6492-m03-wfail, v6492-m03-wpass

### v6492-m04 — Bind witness helper result explicitly

- Trigger: generated Method Flow witness fixtures; positional helper parameters
- Method: Pass the result value explicitly for every failed and passing witness, regenerate the deterministic x1 tree, and validate the ledger with the family runner.
- Recurrence guard: Before running a lifecycle builder, compile it and inspect every helper call against the declared signature; prefer explicit result values.
- Rollback: Stop the builder, retain partial uncommitted output, make no outcome claim, and rebuild the complete x1 tree after the bounded code fix.
- Witnesses: v6492-m04-wfail, v6492-m04-wpass

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
