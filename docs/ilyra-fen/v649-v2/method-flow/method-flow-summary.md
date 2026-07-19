# GHC Family Method Flow State

- Phase: v649-gmut-thos-v2-x1-x2
- Owner: Ilyra Fen
- Methods: 11
- Passing witnesses: 14
- Failed witnesses retained: 15

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
- Witnesses: v6492-m03-wfail, v6492-m03-wpass, v6492-m03-wfail-recurrence, v6492-m03-wpass-index

### v6492-m04 — Bind witness helper result explicitly

- Trigger: generated Method Flow witness fixtures; positional helper parameters
- Method: Pass the result value explicitly for every failed and passing witness, regenerate the deterministic x1 tree, and validate the ledger with the family runner.
- Recurrence guard: Before running a lifecycle builder, compile it and inspect every helper call against the declared signature; prefer explicit result values.
- Rollback: Stop the builder, retain partial uncommitted output, make no outcome claim, and rebuild the complete x1 tree after the bounded code fix.
- Witnesses: v6492-m04-wfail, v6492-m04-wpass

### v6492-m05 — Pin UTF-8 for Unicode-emitting skill initialization

- Trigger: phase-local skill metadata includes non-ASCII wording; Windows default codec is not UTF-8
- Method: Set PYTHONUTF8=1 before running the unchanged official skill initializer or metadata generator, preserving the correct Unicode wording.
- Recurrence guard: Pin UTF-8 before every Unicode-emitting phase-local skill initialization or validation process; never delete, transliterate, or downgrade culturally correct wording to satisfy a locale decoder.
- Rollback: Stop at the partially initialized owner-local package, grant no validation or use credit, leave global skill state untouched, and regenerate only the missing metadata after the bounded environment fix.
- Witnesses: v6492-m05-wfail, v6492-m05-wpass, v6492-m05-wfail-recurrence, v6492-m05-wpass-projection

### v6492-m06 — Inventory lifecycle filenames before bounded field projection

- Trigger: generated lifecycle filenames may differ across phases; complete ledger serialization may exceed the output boundary
- Method: Inventory the exact Method Flow directory first, then read only the named ledger and project small fields rather than serializing the complete ledger through one bounded output channel.
- Recurrence guard: Before reading generated lifecycle state, inventory exact filenames and cap output to the required fields; never infer command failure or success from truncated presentation alone.
- Rollback: Stop the inspection, make no repository inference from incomplete output, and use an exact read-only inventory followed by bounded field projection.
- Witnesses: v6492-m06-wfail, v6492-m06-wpass, v6492-m06-wfail-recurrence, v6492-m06-wpass-projection

### v6492-m07 — Bind frozen x1 assertions to the immutable x1 Git tree

- Trigger: x2 legitimately appends lifecycle evidence; x1 test asserts mutable worktree cardinality
- Method: Validate frozen x1 state from the immutable x1 Git tree and manifest, while evaluating current x2 lifecycle state only with current-phase tests.
- Recurrence guard: Never apply frozen x1 worktree-state assertions to a legitimate x2 descendant; resolve x1 content and lifecycle counts from the exact x1 commit tree.
- Rollback: Stop the mixed-lifecycle test selection, retain the failure with no pass credit, leave x1 files and history untouched, and use the immutable x1 blob contract plus current-phase tests.
- Witnesses: v6492-m07-wfail, v6492-m07-wpass

### v6492-m08 — Capture ripgrep output before projecting bounded rows

- Trigger: producer exit code is evidence; only a short projection should be displayed
- Method: Capture each bounded rg command to an array, inspect its producer exit code, and only then project a count or first rows from the completed array.
- Recurrence guard: Do not truncate a live rg producer with Select-Object when its exit code is evidence; capture bounded output first and attribute failures only after separate exit-code witnesses.
- Rollback: Withdraw the unsupported diagnosis, retain it as a false-assumption negative, make no repository claim, and rerun only bounded separate read-only probes.
- Witnesses: v6492-m08-wfail, v6492-m08-wfail-empty-contract, v6492-m08-wpass

### v6492-m09 — Separate multi-file Apply Patch sections

- Trigger: one patch updates and adds multiple files; patch verification must remain atomic
- Method: Use complete independent Apply Patch sections for each updated or added file and close each hunk before starting another file section.
- Recurrence guard: Before submitting a multi-file patch, verify that every context hunk is complete and every new file starts in its own top-level patch section.
- Rollback: Treat verification failure as no mutation, retain the malformed patch fault, inspect the intended hunks, and resubmit only well-formed independent sections.
- Witnesses: v6492-m09-wfail, v6492-m09-wpass

### v6492-m10 — Type-guard heterogeneous JSON index projection

- Trigger: index contains mappings, lists, and scalar metadata; frozen x1 index must remain unchanged
- Method: Guard every projected JSON value by its actual type and create an additive x2 index supplement instead of rewriting the frozen x1 inventory.
- Recurrence guard: Before projecting heterogeneous JSON, branch explicitly for mapping, list, scalar, and null values; never mutate a frozen index to recover an inspection fault.
- Rollback: Stop the projection, retain the type-assumption fault, leave the x1 index unchanged, and use a type-guarded read plus additive x2 supplement.
- Witnesses: v6492-m10-wfail, v6492-m10-wpass

### v6492-m11 — Capture Git staging diagnostics before compact projection

- Trigger: large owner-local Windows staging set; line-ending advisories may exceed display limits
- Method: Capture Git add diagnostics and exit code before projecting only warning count, then read staged-review receipt fields rather than streaming every advisory.
- Recurrence guard: For large Windows staging sets, capture Git diagnostics and exit status before displaying only counts; never infer staged-review success from truncated console presentation.
- Rollback: Hold the commit, retain the truncated presentation, inspect the exact review receipts read-only, and restage only after bounded diagnostic capture.
- Witnesses: v6492-m11-wfail, v6492-m11-wpass

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
