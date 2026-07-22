# GHC Family Method Flow State

- Phase: v651-v8
- Owner: Ilyra Fen
- Methods: 23
- Passing witnesses: 24
- Failed witnesses retained: 24

## Preferred methods

### V6518-M01 — Bind memory searches to the declared memory registry

- Trigger: A phase needs prior GHC continuity and the memory root is declared separately from task metadata.
- Method: Search the exact declared memory registry path before opening any referenced rollout record.
- Recurrence guard: Never infer the memory registry from the current task directory.
- Rollback: Retain the failed read-only search and make no repository or memory mutation.
- Witnesses: V6518-M01-WFAIL, V6518-M01-WPASS

### V6518-M02 — Use ordinary non-force push after a verified fast-forward

- Trigger: The owned branch is clean, its old head is ancestral to the verified source, and an explicit refspec is available.
- Method: Verify the intended head and divergence, then use an ordinary explicit-refspec push without force.
- Recurrence guard: Apply ff-only to merge or pull, not push; ordinary push already rejects non-fast-forward updates by default.
- Rollback: If the explicit push fails, retain local history and stop without force or reset.
- Witnesses: V6518-M02-WFAIL, V6518-M02-WPASS

### V6518-M03 — Pin UTF-8 before emitting inherited Unicode proposal titles

- Trigger: A Windows Python process may emit Māori or other non-ASCII repository text.
- Method: Set PYTHONUTF8 and PYTHONIOENCODING before process start and preserve source text unchanged.
- Recurrence guard: Pin UTF-8 for every Unicode-emitting diagnostic; never transliterate source text to satisfy a console.
- Rollback: Retain the failed read-only probe and change no culturally authoritative wording.
- Witnesses: V6518-M03-WFAIL, V6518-M03-WPASS

### V6518-M04 — Materialize foreach output before piping in Windows PowerShell 5.1

- Trigger: A Windows PowerShell 5.1 wrapper needs to serialize rows produced by a statement-level foreach loop.
- Method: Assign the foreach results to an array and pipe only that array.
- Recurrence guard: Never append a pipeline directly to statement-level foreach in Windows PowerShell 5.1.
- Rollback: Retain the parser failure; it changed no files, branches, or external state.
- Witnesses: V6518-M04-WFAIL, V6518-M04-WPASS

### V6518-M05 — Use score-only keys for lexical-neighbour selection

- Trigger: A collection of scored records may contain equal numeric scores and non-orderable payload objects.
- Method: Select the maximum candidate with an explicit key over the numeric similarity field.
- Recurrence guard: Every max or sort over scored records must declare a numeric key and never depend on payload comparability.
- Rollback: Retain the failed read-only probe with zero novelty credit and change no inherited proposal record.
- Witnesses: V6518-M05-WFAIL, V6518-M05-WPASS

### V6518-M06 — Avoid escaped nested expressions in diagnostic f-strings

- Trigger: A generated Python diagnostic needs to render multiple dictionary fields inside a joined line.
- Method: Assemble identifier-and-title diagnostic fragments outside nested f-string expressions.
- Recurrence guard: Keep nested diagnostic formatting shallow and bind dictionary fields to plain local fragments before joining.
- Rollback: Retain the parser failure with zero search credit and change no proposal record.
- Witnesses: V6518-M06-WFAIL, V6518-M06-WPASS

### V6518-M07 — Use verified Windows local time when optional IANA tzdata is absent

- Trigger: A Windows Python runtime lacks the optional IANA timezone database and the host timezone has been verified.
- Method: Use the verified Windows system-local New Zealand offset alongside UTC and record the Windows timezone name separately.
- Recurrence guard: Do not assume Windows Python ships an IANA zone database; use a verified system-local offset or an already approved runtime.
- Rollback: Retain the failed pre-generation builder invocation and install no package or runtime.
- Witnesses: V6518-M07-WFAIL, V6518-M07-WPASS

### V6518-M08 — Discover non-package tests by exact filename

- Trigger: The repository tests directory is not an importable Python package.
- Method: Use unittest discovery with the exact tests directory and filename.
- Recurrence guard: Use exact discovery when the tests directory has no package initializer.
- Rollback: Give the import failure zero test credit and change no test file to disguise the invocation error.
- Witnesses: V6518-M08-WFAIL, V6518-M08-WPASS

### V6518-M09 — Propagate authoritative child failures before later checks

- Trigger: A PowerShell wrapper runs more than one authoritative validation child.
- Method: Run the authoritative child separately and propagate its exit status before subsequent commands.
- Recurrence guard: Check every authoritative child exit status immediately or use separate fail-fast invocations.
- Rollback: Retain the misleading aggregate exit as a failure and grant no pass credit to the wrapper.
- Witnesses: V6518-M09-WFAIL, V6518-M09-WPASS

### V6518-M10 — Gate every commit on exact staged diff hygiene

- Trigger: An additive owner-local staged file fails Git diff hygiene.
- Method: Remove only the reported owner-local whitespace defect, restage, and rerun the unchanged diff check.
- Recurrence guard: Run staged diff hygiene before every commit and correct only attributable owner-local defects.
- Rollback: Retain the failed staged check, avoid committing, and leave all sibling and inherited paths unchanged.
- Witnesses: V6518-M10-WFAIL, V6518-M10-WPASS

### V6518-M11 — Self-exclude mutable count-bearing validation receipts

- Trigger: A receipt is written after it reports counts over the surface covered by its enclosing manifest.
- Method: Declare the count-bearing validation receipt as a manifest self-exclusion while preserving owner-path coverage.
- Recurrence guard: Exclude count-bearing receipts from their enclosing manifest or make their bytes stable before sealing.
- Rollback: Retain the stale-entry failure, do not commit, and preserve all other manifest rows unchanged.
- Witnesses: V6518-M11-WFAIL, V6518-M11-WPASS

### V6518-M13 — Use exact Method Flow subcommand argument contracts

- Trigger: A Method Flow runner subcommand has a command-specific file option.
- Method: Use the exact option declared by each Method Flow subcommand: record for methods and witness-file for witnesses.
- Recurrence guard: Check the exact subcommand argument contract before every Method Flow runner invocation.
- Rollback: Retain the refused invocation, grant it zero witness credit, and leave the ledger otherwise unchanged.
- Witnesses: V6518-M13-WFAIL, V6518-M13-WPASS

### V6518-M12 — Replay privacy patterns with an identical definition quarantine

- Trigger: A privacy receipt or scanner source contains its own pattern-class vocabulary.
- Method: Use the exact scanner-definition quarantine set recorded by the preregistered scanner.
- Recurrence guard: Bind privacy replays to both the exact patterns and the exact definition-quarantine paths.
- Rollback: Retain the false-positive replay, grant no zero-hit credit, and leave scanner definitions visible.
- Witnesses: V6518-M12-WFAIL, V6518-M12-WPASS

### V6518-M14 — Correct generated count mirrors at their source

- Trigger: A regenerated test or receipt restores a count that conflicts with the authoritative append-only ledger.
- Method: Update generator-owned assertions at the generator and every authoritative count mirror before regeneration.
- Recurrence guard: Trace every generated failure to its generator source and refresh all count-dependent mirrors together.
- Rollback: Retain the failed validator run, grant it zero pass credit, and do not commit the stale generated assertion.
- Witnesses: V6518-M14-WFAIL, V6518-M14-WPASS

### V6518-M15 — Bind Method Flow summary output to the exact CLI contract

- Trigger: A lifecycle builder needs to refresh Method Flow summaries through the family runner.
- Method: Read the exact summarize subcommand help and bind the evidence builder to its documented output arguments.
- Recurrence guard: Read exact subcommand help before composing lifecycle-runner output flags and preserve stderr on failure.
- Rollback: Retain the failed evidence build with zero pass credit, do not commit, and leave all external and sibling state unchanged.
- Witnesses: V6518-M15-WFAIL, V6518-M15-WPASS

### V6518-M16 — Parse exact NUL-delimited status and declared runner paths

- Trigger: A lifecycle builder validates an uncommitted Windows worktree with modified and generated paths.
- Method: Parse NUL-delimited porcelain without trimming and bind the preflight to the exact declared runner path set.
- Recurrence guard: Never strip porcelain output before parsing status columns; use NUL records and exact generated-path allowlists.
- Rollback: Retain the refused preflight, grant zero build credit, and leave all uncommitted owner-local surfaces available for inspection.
- Witnesses: V6518-M16-WFAIL, V6518-M16-WPASS

### V6518-M17 — Split large-worktree closeout startup probes

- Trigger: A Windows worktree closeout preflight needs exact Git and declared-path state.
- Method: Split Git and filesystem state inspection into independently bounded exact-purpose probes.
- Recurrence guard: Never combine exact-head, tracked-delta, and untracked-surface inspection in one short Windows wrapper on a large worktree.
- Rollback: Retain the timeout with zero credit and make no repository mutation before bounded probes succeed.
- Witnesses: V6518-M17-WFAIL, V6518-M17-WPASS

### V6518-M18 — Constrain closeout discovery to exact paths

- Trigger: An inherited repository makes recursive discovery exceed its bounded window.
- Method: Resolve declared files directly and scope any listing to the current phase root.
- Recurrence guard: Prefer exact known paths and phase-root-scoped inventories over recursive repository discovery during lifecycle work.
- Rollback: Retain the timeout and avoid widening the search or mutating any path.
- Witnesses: V6518-M18-WFAIL, V6518-M18-WPASS

### V6518-M19 — Materialize foreach output before piping

- Trigger: A Windows PowerShell 5.1 probe needs to serialize rows produced by statement-level foreach.
- Method: Materialize statement-level foreach output before piping or serialization in Windows PowerShell 5.1.
- Recurrence guard: Assign statement-level foreach output to a variable before passing it into a pipeline.
- Rollback: Retain the parser failure with zero credit and rerun only the corrected read-only probe.
- Witnesses: V6518-M19-WFAIL, V6518-M19-WPASS

### V6518-M20 — Expose exact child diagnostics before recovery

- Trigger: A scoped validation wrapper stops on a captured child failure without printing the child result.
- Method: Expose the exact failed child selection output before changing any test or validator.
- Recurrence guard: Lifecycle validators must surface captured child diagnostics or direct operators to one exact isolated selection before recovery.
- Rollback: Retain the aggregate failure with zero pass credit and change no test until its exact output is visible.
- Witnesses: V6518-M20-WFAIL, V6518-M20-WPASS, V6518-M20-WFAIL2, V6518-M20-WPASS2

### V6518-M21 — Bind x1-only assertions to the immutable x1 tree

- Trigger: A final descendant needs to preserve prior x1 validation without applying x1-only absence assertions to x2 content.
- Method: Verify historical x1-only test credit from the immutable x1 commit receipt and run descendant-compatible selections at final.
- Recurrence guard: Bind historical absence assertions to their immutable commit and never relabel them as current descendant tests.
- Rollback: Retain the descendant-context failure and do not weaken or rewrite the historical x1 test.
- Witnesses: V6518-M21-WFAIL, V6518-M21-WPASS

### V6518-M22 — Preserve semantic payloads across manifest self-exclusion

- Trigger: A semantic lifecycle receipt is deliberately excluded from its enclosing self-referential manifest.
- Method: Exclude a semantic receipt from self-referential manifest hashing without replacing its already-written payload.
- Recurrence guard: A manifest self-exclusion controls hash coverage only; it must never erase or replace the semantic artifact it excludes.
- Rollback: Retain the failed six-test selection, do not commit, and regenerate the closeout from the immutable evidence parent.
- Witnesses: V6518-M22-WFAIL, V6518-M22-WPASS

### V6518-M23 — Use in-tool self-tests for nested diagnostic witnesses

- Trigger: A validator helper needs a synthetic nonzero child to prove error-output propagation.
- Method: Move nested executable witness logic into a declared validator self-test option.
- Recurrence guard: Do not nest multi-layer executable Python source inside a PowerShell command when a bounded in-tool self-test can express the witness.
- Rollback: Retain the parser and shell errors with zero witness credit and make no lifecycle claim.
- Witnesses: V6518-M23-WFAIL, V6518-M23-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
