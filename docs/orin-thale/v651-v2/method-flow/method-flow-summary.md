# GHC Family Method Flow State

- Phase: v651-v2
- Owner: Orin Thale
- Methods: 22
- Passing witnesses: 22
- Failed witnesses retained: 23

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
- Witnesses: V6512-M12-WFAIL, V6512-M12-WPASS, V6512-M12-WFAIL2, V6512-M12-WPASS2

### V6512-M13 — Use literal separate probes for quote-bearing Windows searches

- Trigger: A PowerShell search pattern contains alternation, embedded quotes, or shell-significant punctuation.
- Method: Use separate literal Select-String probes for each known phrase instead of passing a quote-heavy alternation through PowerShell.
- Recurrence guard: On Windows, use one literal pattern per probe for quote-bearing code and never interpret partial results from a nonzero search as a complete audit.
- Rollback: Give the nonzero alternation zero complete-search credit, retain its partial matches, and rerun only bounded literal probes.
- Witnesses: V6512-M13-WFAIL, V6512-M13-WPASS

### V6512-M14 — Enumerate exact Windows test paths before discovery

- Trigger: A bounded test selection spans more than one Windows filename.
- Method: Expand the bounded test file list with Get-ChildItem, then search each exact LiteralPath for test methods.
- Recurrence guard: Never pass a Windows wildcard as a literal ripgrep path; enumerate the bounded files first and pass exact paths.
- Rollback: Give the wildcard probe zero discovery credit, retain its error, and do not broaden test selection to compensate.
- Witnesses: V6512-M14-WFAIL, V6512-M14-WPASS

### V6512-M15 — Parse NUL-framed Git porcelain without stripping status columns

- Trigger: Closeout begins with modified and untracked owner-scoped files that must be classified exactly.
- Method: Read NUL-framed porcelain bytes without global stripping, preserve both status columns, and whitelist the exact closeout scaffolding paths.
- Recurrence guard: Parse git status --porcelain=v1 -z as raw records and slice paths only after preserving the fixed three-byte XY-space prefix.
- Rollback: Give the failed closeout build zero artifact credit, retain the parser fault, and write no closeout record until the exact observed set is proven allowed.
- Witnesses: V6512-M15-WFAIL, V6512-M15-WPASS

### V6512-M16 — Separate static measurement from compiler supervision

- Trigger: A combined Windows wrapper mixes a static document check with Python compilation under a short supervision budget.
- Method: Run the overview estimate and Python compilation as separate no-profile probes with attributable outputs and supervision budgets.
- Recurrence guard: Keep static text measurement and compiler checks in separate no-profile invocations; a timed-out aggregate has zero component credit.
- Rollback: Give the combined wrapper zero verification credit, retain the timeout, and do not infer that either component completed.
- Witnesses: V6512-M16-WFAIL, V6512-M16-WPASS

### V6512-M17 — Inspect phase-local CLI contracts before help probes

- Trigger: A phase-local Python entrypoint has not demonstrated an argparse help surface.
- Method: Inspect the bounded review entrypoint before invocation, then stage its required paths and run it with its actual no-argument contract.
- Recurrence guard: Inspect a phase-local entrypoint for an argument parser before using --help; when none exists, read the bounded main contract and invoke only after its preconditions hold.
- Rollback: Give the rejected invocation zero review credit, retain the traceback, and stage nothing outside the exact owner paths.
- Witnesses: V6512-M17-WFAIL, V6512-M17-WPASS

### V6512-M18 — Declare exact regenerable closeout outputs

- Trigger: A bounded owner-local generator may need to refresh its already generated outputs before staging.
- Method: Whitelist the exact declared closeout output paths as regenerable owner-local surfaces while retaining rejection of every undeclared path.
- Recurrence guard: A regenerable builder must declare every exact output path in its preflight contract; never replace the list with a directory-wide wildcard.
- Rollback: Give the rejected regeneration zero artifact credit, retain the exact unexpected-path list, and delete or mutate no prior artifact.
- Witnesses: V6512-M18-WFAIL, V6512-M18-WPASS

### V6512-M19 — Quarantine exact privacy scanner definitions without weakening payload scans

- Trigger: A five-class scanner reports its own compiled patterns or an explicit negative assertion as a candidate.
- Method: Classify only exact scanner-definition lines and explicit sanitizer-negative assertions as definition candidates; keep every other match confirmed and fail closed.
- Recurrence guard: A privacy scanner may classify a candidate only when the exact line is a compiled pattern definition or an explicit rejecting assertion in a named test; never exclude a file or class wholesale.
- Rollback: Give the failed staged review zero credit, retain all five candidates, and write no privacy or manifest receipt until exact classification yields zero unclassified hits.
- Witnesses: V6512-M19-WFAIL, V6512-M19-WPASS

### V6512-M21 — Quarantine exactly two inherited live-lifecycle assertions

- Trigger: Two named inherited assertions have each failed because they inspect successor lifecycle state rather than immutable source-phase state.
- Method: Quarantine exactly the inherited x1 terminal-baton document-cap assertion and the inherited closeout owner/delta live-path assertion, then require all other 22 source tests and all 36 current tests.
- Recurrence guard: Discover source tests exactly, quarantine only named assertions proven lifecycle-bound at the successor head, and require every remaining source and current test without widening to a module exclusion.
- Rollback: Give the targeted manifest test zero successor credit, retain its full failure, keep the route unsent, and stop if any of the remaining 58 tests fail the bounded preflight.
- Witnesses: V6512-M21-WFAIL, V6512-M21-WPASS

### V6512-M22 — Retire falsified candidates through the permitted deprecated state

- Trigger: A candidate workaround is falsified before it has any passing witness.
- Method: Use the schema-permitted candidate-to-deprecated transition with an explicit successor when a candidate workaround is falsified before validation.
- Recurrence guard: Read the state-transition table before retiring a method: candidate methods become deprecated, while validated or preferred methods may become superseded.
- Rollback: Give the rejected transition zero state credit, retain M20 as candidate until the permitted deprecation event is appended, and never fabricate validation.
- Witnesses: V6512-M22-WFAIL, V6512-M22-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
