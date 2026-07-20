# GHC Family Method Flow State

- Phase: v651-v2
- Owner: Orin Thale
- Methods: 13
- Passing witnesses: 13
- Failed witnesses retained: 13

## Preferred methods

### V6512-M01 — Resolve stale memory rollout pointers with one bounded suffix search

- Trigger: A current memory registry entry names a rollout summary that is absent at that exact path.
- Method: Treat the memory registry filename as a lead, then resolve one bounded suffix match before reading the rollout summary.
- Recurrence guard: Use an exact filename first, then at most one suffix-scoped rg --files recovery; never broad-scan private rollout content.
- Rollback: Give the stale pointer zero read credit, retain the miss, and stop if the bounded suffix search is not unique.
- Witnesses: V6512-M01-WFAIL, V6512-M01-WPASS

### V6512-M02 — Isolate local, ancestry, live-remote, and owned-lane Git probes

- Trigger: A grouped Windows Git audit approaches or exceeds its supervision budget.
- Method: Split local Git facts, ancestry, live remote, and owned-lane probes into small no-profile invocations.
- Recurrence guard: Keep network and local Git probes separate and disable the login profile for bounded verification commands.
- Rollback: Give the grouped audit zero verification credit and make no branch change until every isolated probe passes.
- Witnesses: V6512-M02-WFAIL, V6512-M02-WPASS

### V6512-M03 — Verify manifests with tree maps and one-request blob framing

- Trigger: Hundreds of immutable Git blobs require exact byte, digest, blob-ID, and path-set comparison.
- Method: Resolve commit trees once and read each unique blob with one flushed request followed by its complete response.
- Recurrence guard: Build one ls-tree map per commit and use strict request-flush-read framing; never write all batch requests before reading.
- Rollback: Retain the timed wrapper with zero aggregate pass credit and do not reuse a blocking batch transport.
- Witnesses: V6512-M03-WFAIL, V6512-M03-WPASS

### V6512-M04 — Bind x1 assertions to frozen schemas and semantic prose

- Trigger: A test fails because its asserted key or prose casing differs from the committed current schema or equivalent boundary text.
- Method: Bind assertions to the committed workflow and reflection schemas and compare semantic boundary phrases case-insensitively.
- Recurrence guard: Inspect frozen JSON keys before assertions and reserve exact string checks for normative machine labels, not prose capitalization.
- Rollback: Retain the first suite with zero aggregate pass credit and change no phase data or implementation to satisfy a stale test assumption.
- Witnesses: V6512-M04-WFAIL, V6512-M04-WPASS

### V6512-M05 — Bind resumed repository work to the explicit owned worktree

- Trigger: A resumed shell or compacted turn may have lost its prior repository working directory.
- Method: Resolve the owned worktree from the bounded worktree bank and pass its absolute path as the working directory for every repository command.
- Recurrence guard: Before any staged review or mutation after a resumed turn, prove the explicit owned worktree path, branch, and head; never infer repository context from the process default directory.
- Rollback: Give the mismatched-directory probe zero repository credit, retain the miss, and perform no staging until the owned lane is explicitly resolved.
- Witnesses: V6512-M05-WFAIL, V6512-M05-WPASS

### V6512-M06 — Bind Method Flow validation to its documented receipt option

- Trigger: A Method Flow subcommand output contract has not been independently verified.
- Method: Read the subcommand help and pass the documented --receipt path rather than assuming the summarizer and validator share an output option.
- Recurrence guard: Interrogate each runner subcommand independently; do not infer option parity between summarize and validate.
- Rollback: Give the rejected validation invocation zero validation credit, preserve the already successful append-only operations, and retry only the validator with its documented receipt option.
- Witnesses: V6512-M06-WFAIL, V6512-M06-WPASS

### V6512-M07 — Keep live Method Flow assertions lifecycle-safe

- Trigger: An append-only Method Flow ledger may acquire later bounded recovery evidence while the same phase test remains in successor selections.
- Method: Assert the frozen minimum Method Flow evidence and the invariant that every recorded method is preferred, rather than binding a successor-capable test to a transient exact count.
- Recurrence guard: Use exact counts only for immutable commit-blob receipts; use declared minimums and semantic invariants for live lifecycle ledgers.
- Rollback: Give the failed rebuilt suite zero aggregate credit, retain the obsolete assertion, and change no proposal or outcome data.
- Witnesses: V6512-M07-WFAIL, V6512-M07-WPASS

### V6512-M08 — Make recovery acceptance independent of its own future witness

- Trigger: A recovery method's proposed acceptance assertion counts append-only witnesses or states that the recovery itself will create.
- Method: Anchor live-ledger assertions to evidence that already existed before the recovering method began; never require a method's own future passing witness as a precondition for running its acceptance check.
- Recurrence guard: Set recovery acceptance minima from immutable pre-recovery evidence and test active lifecycle states separately from later promotion.
- Rollback: Give the circular targeted assertion zero credit, retain M07 as candidate, and append no passing witness until a noncircular bounded check succeeds.
- Witnesses: V6512-M08-WFAIL, V6512-M08-WPASS

### V6512-M09 — Pin UTF-8 for official phase-skill validation

- Trigger: An official Python skill tool reads UTF-8 package text on Windows.
- Method: Pin PYTHONUTF8=1 for the official skill validator and keep every skill file encoded as UTF-8.
- Recurrence guard: Set PYTHONUTF8=1 before every Windows invocation of the skill-creator validators or generators that read non-ASCII text.
- Rollback: Give the CP1252 attempt zero skill-validation credit, retain the traceback classification, and change no skill semantics merely to fit a legacy code page.
- Witnesses: V6512-M09-WFAIL, V6512-M09-WPASS

### V6512-M10 — Run v651-v2 proposal groups before aggregate bounded validation

- Trigger: The dedicated x1 freeze is pushed and four-way remote-equal, and x2 execution is authorized.
- Method: Execute each frozen proposal group through its family-current runner, then run portfolios and aggregate current-phase validation only after every group witness passes.
- Recurrence guard: Keep group runners small, emit one attributable witness per runner, and run the aggregate validator only after all prerequisite receipts exist.
- Rollback: Stop at the first failing group or invalid Method Flow promotion, retain its output with zero aggregate credit, change no external state, and repair only the bounded workflow record.
- Witnesses: V6512-M10-WPASS, V6512-M10-WFAIL

### V6512-M11 — Bind historical x1 assertions to the immutable x1 commit

- Trigger: A current or successor suite reuses tests that assert an earlier lifecycle state.
- Method: Bind x1 absence assertions to the immutable x1 commit tree with read-only Git object checks instead of inspecting the live x2 worktree.
- Recurrence guard: Every historical phase-state assertion must name and inspect its immutable commit or manifest; never infer prior state from a later live tree.
- Rollback: Give the first 25-of-26 aggregate zero credit, retain the live-tree assumption, and change no x1 commit or x2 surface.
- Witnesses: V6512-M11-WFAIL, V6512-M11-WPASS

### V6512-M12 — Inspect exact file context before lifecycle repair patches

- Trigger: A file may have been regenerated or its import and assertion context is not proven current.
- Method: Read the exact bounded file context before applying a narrow patch and change only the verified import and assertion lines.
- Recurrence guard: Inspect the exact local context after compaction or regeneration before constructing multi-file patches.
- Rollback: Retain the rejected patch with zero edit credit, inspect the exact context read-only, and apply only the corrected bounded patch.
- Witnesses: V6512-M12-WFAIL, V6512-M12-WPASS

### V6512-M13 — Use literal separate probes for quote-bearing Windows searches

- Trigger: A PowerShell search pattern contains alternation, embedded quotes, or shell-significant punctuation.
- Method: Use separate literal Select-String probes for each known phrase instead of passing a quote-heavy alternation through PowerShell.
- Recurrence guard: On Windows, use one literal pattern per probe for quote-bearing code and never interpret partial results from a nonzero search as a complete audit.
- Rollback: Give the nonzero alternation zero complete-search credit, retain its partial matches, and rerun only bounded literal probes.
- Witnesses: V6512-M13-WFAIL, V6512-M13-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
