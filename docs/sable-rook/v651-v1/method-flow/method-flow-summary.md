# GHC Family Method Flow State

- Phase: v651-v1
- Owner: Sable Rook
- Methods: 12
- Passing witnesses: 12
- Failed witnesses retained: 13

## Preferred methods

### V6511-M01 — Pin UTF-8 before frozen-title diagnostics

- Trigger: A Python diagnostic may emit non-ASCII frozen titles under Windows PowerShell.
- Method: Set the Python standard-stream encoding to UTF-8 before emitting frozen titles that may contain Māori text.
- Recurrence guard: Pin UTF-8 before every Unicode-emitting Python diagnostic and give partial output zero completeness credit.
- Rollback: Retain the partial probe with zero novelty credit and change no proposal until a complete UTF-8 witness passes.
- Witnesses: V6511-M01-WFAIL, V6511-M01-WPASS

### V6511-M03 — Validate Method Flow records before dependent witnesses

- Trigger: A new method and one or more dependent witnesses must be appended to the family Method Flow ledger.
- Method: Validate every Method Flow input against the required record fields before invoking record, then attach witnesses only after the method exists.
- Recurrence guard: Read the exact Method Flow schema, include all required record fields, and ingest a method before any dependent witness.
- Rollback: Keep the rejected input and unattached witness with zero append credit; do not hand-edit the canonical ledger.
- Witnesses: V6511-M03-WFAIL, V6511-M03-WPASS, V6511-M03-WFAIL, V6511-M03-WPASS

### V6511-M02 — Separate live routing restrictions from frozen workflow vocabulary

- Trigger: A live instruction is stricter than an enumerated base label accepted by a frozen family workflow runner.
- Method: Use the workflow runner's frozen user-mediated file-relay vocabulary and preserve the stricter live no-cross-platform-send rule as an explicit phase boundary.
- Recurrence guard: Keep live additive restrictions separate from a frozen runner's enumerated base vocabulary unless that runner is explicitly remastered and validated.
- Rollback: Retain the invalid request and its 19-of-20 receipt with zero workflow-validity credit; contact no task.
- Witnesses: V6511-M02-WFAIL, V6511-M02-WPASS, V6511-M02-WFAIL, V6511-M02-WPASS

### V6511-M04 — Require one terminal newline before manifest sealing

- Trigger: A staged source or generated file is about to enter an immutable lifecycle commit.
- Method: Review the exact staged diff, require one terminal newline, regenerate every affected manifest hash, and rerun diff hygiene.
- Recurrence guard: Review exact end-of-file bytes before staging generated or patched source, then rebuild dependent hashes after any byte correction.
- Rollback: Retain the failed staged check, commit nothing, and change only the exact terminal blank line plus dependent receipts.
- Witnesses: V6511-M04-WFAIL, V6511-M04-WPASS, V6511-M04-WFAIL, V6511-M04-WPASS

### V6511-M05 — Seal manifests in the normalized Git-blob byte domain

- Trigger: Generated text may use platform newline bytes before Git clean filtering.
- Method: Hash prospective normalized Git-blob bytes rather than platform checkout bytes, then replay every manifest entry from the index.
- Recurrence guard: Declare the manifest hash domain and normalize text exactly as Git does before sealing; verify again from index blobs.
- Rollback: Retain the failed parity receipt, commit nothing, and regenerate only the manifest and dependent receipts.
- Witnesses: V6511-M05-WFAIL, V6511-M05-WPASS, V6511-M05-WFAIL, V6511-M05-WPASS

### V6511-M06 — Use directory-scoped ripgrep on Windows

- Trigger: A recursive text search is needed across files on Windows PowerShell.
- Method: Search the directory root and let ripgrep recurse instead of passing Windows wildcard path arguments.
- Recurrence guard: On Windows, pass a real directory to ripgrep and filter results by pattern; do not assume shell wildcard expansion in path arguments.
- Rollback: Keep the failed wildcard probe with zero search credit and change no repository state until a directory-scoped query passes.
- Witnesses: V6511-M06-WFAIL, V6511-M06-WPASS, V6511-M06-WFAIL, V6511-M06-WPASS, V6511-M06-WFAIL-02

### V6511-M07 — Resolve skill references from exact links

- Trigger: A selected skill names a required local reference that must be read before action.
- Method: Follow the skill's exact required-reference link and read references/schema.md instead of guessing a filename.
- Recurrence guard: Resolve required references from the exact link in SKILL.md; never derive or guess a schema filename from the skill title.
- Rollback: Retain the failed guessed-path read with zero schema credit and make no ledger change until the exact linked schema is read.
- Witnesses: V6511-M07-WFAIL, V6511-M07-WPASS, V6511-M07-WFAIL, V6511-M07-WPASS

### V6511-M08 — Judge unittest by native exit code under PowerShell 5.1

- Trigger: A native test runner writes normal progress to stderr while PowerShell terminating error handling is active.
- Method: Use non-terminating PowerShell handling around native unittest output, capture the complete stream, and decide success only from the explicit native exit code.
- Recurrence guard: For native tools that legitimately write progress to stderr under Windows PowerShell 5.1, capture output with non-terminating handling and gate solely on LASTEXITCODE plus parsed totals.
- Rollback: Retain the interrupted wrapper with zero aggregate credit and change no repository evidence until one complete exit-code-governed selection passes.
- Witnesses: V6511-M08-WFAIL, V6511-M08-WPASS, V6511-M08-WFAIL, V6511-M08-WPASS

### V6511-M09 — Use exact successor module allowlists

- Trigger: A successor phase must reuse inherited x1/x2 tests while predecessor closeout tests bind themselves to an older exact HEAD.
- Method: Use an exact module allowlist: inherited v650-v7 and v650-v8 x1/x2 modules plus all v651-v1 modules, leaving predecessor closeout self-state tests outside successor credit.
- Recurrence guard: Bind successor test credit to an explicit module allowlist and never broaden inherited phase-local closeout assertions merely to increase cardinality.
- Rollback: Retain the 20-test two-failure aggregate with zero selection credit and change no immutable predecessor test; run only the frozen eligible module set.
- Witnesses: V6511-M09-WFAIL, V6511-M09-WPASS, V6511-M09-WFAIL, V6511-M09-WPASS

### V6511-M10 — Reserve the frozen terminal-baton document exception

- Trigger: A frozen x1 document-cap test predates a preregistered terminal baton whose range is an explicit exception.
- Method: Exclude only the immutable x1 all-Markdown document-cap assertion after terminal-baton materialization, and require the closeout test to enforce the 6,000-word ordinary cap plus the frozen 8,000-to-20,000-word baton exception.
- Recurrence guard: At terminal selection, quarantine only the named immutable x1 assertion that predates baton materialization and require a closeout assertion for both ordinary and baton ranges.
- Rollback: Retain the seven-test one-failure x1 run with zero selection credit, leave the frozen x1 test unchanged, and do not credit a terminal selection until the exact replacement contract passes.
- Witnesses: V6511-M10-WFAIL, V6511-M10-WPASS, V6511-M10-WFAIL, V6511-M10-WPASS

### V6511-M11 — Budget final Git-blob manifest rebuilds to the measured envelope

- Trigger: A source-to-final manifest rebuild hashes hundreds of Git-filtered blobs in the Windows owner lane.
- Method: Allow 120 seconds for the owner and delta Git-blob manifest rebuild, then verify coverage and hashes from the emitted receipts.
- Recurrence guard: Use the measured manifest-rebuild envelope rather than the generic short wrapper, and grant credit only after exact coverage and hash parity pass.
- Rollback: Retain the timed-out attempt with zero manifest credit, inspect partial outputs, and overwrite only generated manifest receipts during one bounded recovery.
- Witnesses: V6511-M11-WFAIL, V6511-M11-WPASS, V6511-M11-WFAIL, V6511-M11-WPASS

### V6511-M12 — Require explicit execution for inline audit probes

- Trigger: A PowerShell here-string contains inline code intended for another interpreter.
- Method: Pipe the complete PowerShell here-string explicitly to Python, keep the recovery probe minimal, and require a structured success value before granting review credit.
- Recurrence guard: Require an explicit pipeline or script invocation for every inline-language probe and accept only a structured result emitted by the invoked interpreter.
- Rollback: Retain the printed-but-unexecuted probe with zero review credit and change no evidence claim until a minimal explicit invocation passes.
- Witnesses: V6511-M12-WFAIL, V6511-M12-WPASS, V6511-M12-WFAIL, V6511-M12-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
