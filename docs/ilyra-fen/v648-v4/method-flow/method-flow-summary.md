# GHC Family Method Flow State

- Phase: v648-gmut-thos-v4-x1-x2
- Owner: Ilyra Fen
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### V6484-M01 — Split PowerShell Git proof from exit-code assembly

- Trigger: Several Git ancestry probes must be combined into one sanitized receipt on Windows PowerShell.
- Method: Run each Git command as a separate statement, capture LASTEXITCODE, and assemble the receipt only after every probe returns.
- Recurrence guard: Do not place command invocation and LASTEXITCODE capture inside the same parenthesized assignment.
- Rollback: Give the failed wrapper zero credit and rerun only the read-only probes as independent statements.
- Witnesses: V6484-M01-WFAIL, V6484-M01-WPASS

### V6484-M02 — Inspect serialized receipt schema before property binding

- Trigger: A current phase reads a structured receipt produced by an earlier phase or builder.
- Method: Inspect the exact serialized keys, bind the declared field, and preserve the source receipt unchanged.
- Recurrence guard: Never infer receipt property names from prose when the committed schema is available.
- Rollback: Retain the null result and give it no version evidence credit.
- Witnesses: V6484-M02-WFAIL, V6484-M02-WPASS

### V6484-M03 — Respect Method Flow automatic witness promotion

- Trigger: A method is recorded as candidate and the family runner ingests a bounded passing witness.
- Method: Read the runner-produced state after witness ingestion and request only the remaining validated-to-preferred transition.
- Recurrence guard: Treat runner state transitions as authoritative; never replay an already-applied transition.
- Rollback: Retain the failed builder run, delete no witness, and rebuild the uncommitted ledger from its declared inputs.
- Witnesses: V6484-M03-WFAIL, V6484-M03-WPASS

### V6484-M04 — Union cached unstaged and untracked paths for staged coverage

- Trigger: An exact staged manifest is validated after git add while the worktree itself has no remaining unstaged paths.
- Method: Build the current intended surface from cached, unstaged, and untracked path sets before comparing coverage.
- Recurrence guard: Never infer the staged surface from git diff without --cached after index mutation.
- Rollback: Retain the failed suite, leave staged blobs unchanged, and rerun only after the coverage-domain fix is staged.
- Witnesses: V6484-M04-WFAIL, V6484-M04-WPASS

### V6484-M05 — Exact self-referential privacy receipt disposition

- Trigger: A privacy receipt is a declared self-exclusion and already exists from a prior uncommitted builder run.
- Method: Classify only the exact scanner implementation and exact privacy receipt as scanner-definition surfaces.
- Recurrence guard: Never exempt a directory, wildcard, unrelated receipt, or arbitrary generated output from privacy adjudication.
- Rollback: Retain the failed scan and keep the x1 commit blocked until zero non-definition candidates remain.
- Witnesses: V6484-M05-WFAIL, V6484-M05-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
