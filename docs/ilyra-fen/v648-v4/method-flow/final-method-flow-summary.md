# GHC Family Method Flow State

- Phase: v648-gmut-thos-v4-x1-x2
- Owner: Ilyra Fen
- Methods: 13
- Passing witnesses: 13
- Failed witnesses retained: 13

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

### V6484-M06 — Split large-file inspection into bounded metadata and syntax probes

- Trigger: New or generated implementation files must be inspected on a latency-variable Windows worktree.
- Method: Probe file existence and byte length first, then run syntax and status checks independently.
- Recurrence guard: Do not place content-wide line counting, status, and syntax checks in one short wrapper.
- Rollback: Give the timed-out wrapper zero credit and retain the unmodified worktree.
- Witnesses: V6484-M06-WFAIL, V6484-M06-WPASS

### V6484-M07 — Assign PowerShell foreach output before piping

- Trigger: A Windows PowerShell 5.1 probe must format or filter rows produced by foreach.
- Method: Assign the foreach result to an array and pipe that array in a separate statement.
- Recurrence guard: Never pipe directly from a PowerShell 5.1 foreach statement.
- Rollback: Retain the parser failure with zero credit; no repository state requires rollback.
- Witnesses: V6484-M07-WFAIL, V6484-M07-WPASS

### V6484-M08 — Escalate a timed exact-file search to a bounded native probe

- Trigger: A known exact file and exact pattern set must be inspected after a short search timeout.
- Method: Use a longer bounded native exact-pattern search on only the known file.
- Recurrence guard: Treat measured Windows worktree latency, not apparent file size, as the timeout input.
- Rollback: Give the timed-out search zero credit and retain the unchanged worktree.
- Witnesses: V6484-M08-WFAIL, V6484-M08-WPASS

### V6484-M09 — Derive staged runner scope from the frozen runner-name ledger

- Trigger: A phase generates runner files from an X1-frozen runner-name ledger.
- Method: Load the exact frozen runner names and union them with the fixed builder, runtime, test, and owner-packet paths.
- Recurrence guard: Never substitute a guessed naming prefix for an available frozen filename ledger.
- Rollback: Give the rejected preflight zero evidence credit and stage nothing until the exact-name check passes.
- Witnesses: V6484-M09-WFAIL, V6484-M09-WPASS

### V6484-M10 — Split privacy-negative test literals from scanner-shaped payload spelling

- Trigger: A public unit test must assert that a durable baton omits prohibited privacy patterns.
- Method: Construct the negative expectation from nonmatching string fragments while preserving the exact runtime assertion.
- Recurrence guard: Do not publish scanner-shaped negative examples in public tests or fixtures.
- Rollback: Give the failed preflight zero credit, send nothing, and keep the canonical pass unspent.
- Witnesses: V6484-M10-WFAIL, V6484-M10-WPASS

### V6484-M11 — Reject unittest loader placeholders and require an empty loader-error list

- Trigger: A canonical selection is loaded without execution from a script whose import root differs from the repository root.
- Method: Insert the exact repository root, use a fresh TestLoader, and require loader.errors to be empty before accepting countTestCases.
- Recurrence guard: Never accept a test-count preflight without inspecting the loader error collection.
- Rollback: Give the false count zero credit and do not run the canonical aggregate.
- Witnesses: V6484-M11-WFAIL, V6484-M11-WPASS

### V6484-M12 — Regenerate final manifest entries from measured Git blobs

- Trigger: A post-pass result receipt must be added and the generated final manifest requires an exact refresh.
- Method: Read or regenerate the exact manifest structure from measured current Git-blob hashes rather than guessed context.
- Recurrence guard: Never patch generated manifest entries against inferred bytes or hash context.
- Rollback: Retain the rejected patch with zero credit; it changed no file and requires no content rollback.
- Witnesses: V6484-M12-WFAIL, V6484-M12-WPASS

### V6484-M13 — Split post-pass receipt patches by exact current context

- Trigger: Several self-excluded lifecycle receipts require additive post-pass count reconciliation.
- Method: Apply one exact-context receipt update per patch and refresh the measured manifest only after all patches succeed.
- Recurrence guard: Never join unrelated receipt edits through a hunk without exact current context.
- Rollback: Retain the rejected patch with zero credit; no file changed and no content rollback is required.
- Witnesses: V6484-M13-WFAIL, V6484-M13-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
