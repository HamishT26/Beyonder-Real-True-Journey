# GHC Family Method Flow State

- Phase: v648-gmut-thos-v2-x1-x2
- Owner: Sylven Arc
- Methods: 20
- Passing witnesses: 20
- Failed witnesses retained: 20

## Preferred methods

### V6482-M01 — Decompose exact skill reads after a content-free aggregate timeout

- Trigger: Multiple required instruction files are exact and known but an aggregate read expires.
- Method: Read each exact required file sequentially with a longer bounded envelope and stop only after complete content is returned.
- Recurrence guard: Do not infer absence or partial compliance from an aggregate read timeout.
- Rollback: Discard the timeout result; it changed no repository or external state.
- Witnesses: V6482-M01-WFAIL, V6482-M01-WPASS

### V6482-M02 — Treat registry search exit one as a no-match state rather than a failed exact note read

- Trigger: A targeted newest memory note is readable and a supplemental rg lookup may legitimately find no match.
- Method: Preserve the successful targeted read, classify rg exit one as no match, and let the live verified baton outrank older memory.
- Recurrence guard: Capture exact-read and optional-search outcomes separately when no match is allowed.
- Rollback: Discard only the overstrict combined status; no file or ref changed.
- Witnesses: V6482-M02-WFAIL, V6482-M02-WPASS

### V6482-M03 — Decompose slow Git and proposal discovery into bounded witnesses

- Trigger: A large Windows worktree makes status and broad proposal scans slower than a shared aggregate timeout.
- Method: Run clean-state, ancestry, equality, schema, and concept searches as separate bounded commands and retain each completed witness.
- Recurrence guard: Avoid broad worktree enumeration inside a short shared timeout; bound each required witness independently.
- Rollback: Discard the timed-out aggregate; it issued read-only commands and made no mutation.
- Witnesses: V6482-M03-WFAIL, V6482-M03-WPASS

### V6482-M04 — Pin inherited read paths after owner-phase template substitution

- Trigger: A successor adapts a prior builder whose owner and phase strings occur in both output paths and inherited-source paths.
- Method: Apply owner and phase substitutions, then explicitly restore the exact inherited source directory and proposal-ledger path as the final transformation step.
- Recurrence guard: Keep inherited read roots and current owner write roots in distinct explicit domains after every template transformation.
- Rollback: No rollback was required because the failure preceded every packet write and changed no ref.
- Witnesses: V6482-M04-WFAIL, V6482-M04-WPASS

### V6482-M05 — Review every hardcoded lifecycle and narrative literal after family-template adaptation

- Trigger: A versioned builder contains arithmetic and narrative literals that are not derived from imported definitions.
- Method: Reject the generated packet before staging, add exact substitutions for the lifecycle count, core surfaces, practice vocabulary, and successor route, then regenerate deterministically.
- Recurrence guard: Run stale-topic, count, owner, source, and route scans before any x1 staged review or commit.
- Rollback: Overwrite only the uncommitted owner-generated packet from frozen definitions; retain this failed generation as an operational negative.
- Witnesses: V6482-M05-WFAIL, V6482-M05-WPASS

### V6482-M06 — Resolve staged-review output paths before repository-relative classification

- Trigger: The staged reviewer is invoked from the repository root with relative review, manifest, and privacy output arguments.
- Method: Resolve each output path to an absolute path before deriving its repository-relative self-exclusion.
- Recurrence guard: Make the reviewer normalize paths internally and stop chained lifecycle commands on the first failed review.
- Rollback: No review outputs or commit existed; retain the staged owner files and rerun only after regenerating the expanded negative ledger.
- Witnesses: V6482-M06-WFAIL, V6482-M06-WPASS

### V6482-M07 — Materialize prepared Method Flow records with the family runner before reading derived receipts

- Trigger: The preregistration builder has prepared records and witnesses but has not invoked init, record, witness, set-state, validate, and summarize.
- Method: Enumerate the bounded Method Flow directory, run the required family runner sequence for every prepared record and witness, then read the explicitly named validation receipt.
- Recurrence guard: Treat generated record files as runner input, not as a validated ledger; require the runner receipt before x1 freeze.
- Rollback: Discard the null summary field; it changed no repository data beyond the already staged owner packet.
- Witnesses: V6482-M07-WFAIL, V6482-M07-WPASS

### V6482-M08 — Verify and invoke the actual family-template entry point

- Trigger: A successor adapter compiles a versioned family builder whose terminal guard calls build directly rather than exposing main.
- Method: Invoke the family-current template's build entry point directly, preserve the exact x1 head gate, and grant no partial x2 credit to the failed adapter call.
- Recurrence guard: Inspect a family template's exported entry point before wrapping it and call only the verified build function under the exact x1 head guard.
- Rollback: No runner or evidence write began, so discard the failed invocation and retain only its sanitized witness.
- Witnesses: V6482-M08-WFAIL, V6482-M08-WPASS

### V6482-M09 — Require enclosing success and exact register-schema use for partial-output evidence

- Trigger: A builder produces bounded artifacts before a post-processing step reads a derived register.
- Method: Read the exact retained-negative register schema, use effective_total, rerun the deterministic owner-scoped builder, and withhold evidence completion credit until the enclosing command exits zero.
- Recurrence guard: Inspect generated register keys before post-processing and require the enclosing lifecycle command to exit zero before granting evidence credit.
- Rollback: Retain candidate files as uncommitted partial output, overwrite only deterministic owner outputs on recovery, and grant no evidence lifecycle credit to the failed invocation.
- Witnesses: V6482-M09-WFAIL, V6482-M09-WPASS

### V6482-M10 — Route owner-growth queries to the exact lifecycle rotation receipt

- Trigger: Both x1 rotation-guard and x2 rotation-receipt documents exist with distinct schemas.
- Method: Read x2-rotation-receipt.json and its owner_generated_count field, retain the x1 rotation guard separately, and require the enclosing evidence command to exit zero.
- Recurrence guard: Route each lifecycle query to its explicitly named receipt and inspect exact schema keys before deriving overview counts.
- Rollback: Retain candidate outputs uncommitted, overwrite only deterministic owner reports after schema correction, and grant no lifecycle credit to the failed enclosure.
- Witnesses: V6482-M10-WFAIL, V6482-M10-WPASS

### V6482-M11 — Declare UTF-8 for Unicode-bearing evidence inspection

- Trigger: A read-only child process may print repository text outside the active Windows code page.
- Method: Set the child process output encoding to UTF-8 before printing JSON that may contain macrons or other non-CP1252 characters.
- Recurrence guard: Declare UTF-8 child output for repository JSON inspection and require a zero exit before using printed results.
- Rollback: Keep repository files unchanged, discard partial console output, and rerun the same read-only query with explicit UTF-8 output.
- Witnesses: V6482-M11-WFAIL, V6482-M11-WPASS

### V6482-M12 — Route Method Flow operations to the skill-owned runner

- Trigger: The Method Flow skill is required and no repository-local runner has been verified.
- Method: Invoke the Method Flow runner from the fully read ghc-family-method-flow-state skill package rather than guessing a repository-local copy.
- Recurrence guard: Resolve the runner from the required skill instructions and verify its help surface before recording state.
- Rollback: Make no ledger mutation through an unresolved path; retain the failed lookup and use the verified skill-owned runner.
- Witnesses: V6482-M12-WFAIL, V6482-M12-WPASS

### V6482-M13 — Bound runner discovery and require a complete zero-exit witness

- Trigger: A known skill directory contains the required runner and broad repository enumeration is unnecessary.
- Method: Use an exact bounded skill-directory query and treat discovery completeness separately from partial pipeline output.
- Recurrence guard: Query the known skill directory directly and require a zero exit before treating runner discovery as complete.
- Rollback: Discard completeness credit from partial pipeline output, retain the failure, and rerun an exact bounded query.
- Witnesses: V6482-M13-WFAIL, V6482-M13-WPASS

### V6482-M14 — Review generated path labels as part of lifecycle adaptation

- Trigger: A family-template adapter transforms phase content while generated path literals may use a different spelling.
- Method: Transform candidate-witness path literals as well as content literals, regenerate the owner packet, and reject any staged path carrying an inherited phase label.
- Recurrence guard: Scan staged pathnames as well as file contents for inherited phase labels before lifecycle commit.
- Rollback: Withhold the evidence commit, replace only uncommitted owner-generated stale candidate files, regenerate deterministically, and rerun exact staged review.
- Witnesses: V6482-M14-WFAIL, V6482-M14-WPASS

### V6482-M15 — Bind negative-count tests to the exact operational register

- Trigger: Operational failures may be added before the evidence commit and the register is the authoritative evidence surface.
- Method: Compare retained-negative arithmetic to the exact operational-negative register and use a minimum only for the known evidence floor.
- Recurrence guard: Derive lifecycle-negative parity from the exact register rather than copying a mutable count into test code.
- Rollback: Withhold validation credit, retain the failed assertion, update only the uncommitted owner test, rebuild the register, and rerun the same suite.
- Witnesses: V6482-M15-WFAIL, V6482-M15-WPASS

### V6482-M16 — Parse remote-divergence fields instead of formatted text

- Trigger: Git reports left-right counts as whitespace-separated fields under PowerShell.
- Method: Parse Git divergence as two integer fields rather than comparing tab-formatted console text to an escape literal.
- Recurrence guard: Split rev-list left-right counts on whitespace, cast both to integers, and compare hashes independently.
- Rollback: Grant no equality-wrapper credit, retain the successful push as Git state only, and replay the same read-only equality observations with parsed fields.
- Witnesses: V6482-M16-WFAIL, V6482-M16-WPASS

### V6482-M17 — Use tool-native globs for Windows source searches

- Trigger: A bounded source search needs a filename filter under Windows.
- Method: Pass Windows tree roots as literal paths and express filename selection with ripgrep's -g filter.
- Recurrence guard: Use literal search roots plus -g for globs; require zero exit and exact matches before relying on discovery.
- Rollback: Discard the rejected invocation, preserve repository state, and rerun the exact pattern against literal roots with a tool-native glob.
- Witnesses: V6482-M17-WFAIL, V6482-M17-WPASS

### V6482-M18 — Inspect rendered boundaries for split inherited practice literals

- Trigger: A family template contains practice wording split across adjacent string literals.
- Method: Review the assembled boundary after transformation and replace split inherited practice literals before staging.
- Recurrence guard: Inspect rendered boundary values, not only source replacement tables, before closeout staging.
- Rollback: Withhold closeout staging, retain the adaptation miss, update only the uncommitted adapter, and regenerate deterministic owner outputs.
- Witnesses: V6482-M18-WFAIL, V6482-M18-WPASS

### V6482-M19 — Decompose a timed-out closeout stale-topic scan

- Trigger: The closeout review surface is a known bounded file list and a combined search exceeds its deadline.
- Method: Use exact per-file PowerShell matching over the known closeout surface when the combined ripgrep wrapper exceeds its bound.
- Recurrence guard: Keep the target file list exact and record the complete per-file match count under a bounded envelope.
- Rollback: Grant no scan credit to the timeout, retain it, and replay only read-only exact target matching.
- Witnesses: V6482-M19-WFAIL, V6482-M19-WPASS

### V6482-M20 — Distinguish retained historical failures from current truth labels

- Trigger: A retained-negative register necessarily contains the stale wording that a prior guard detected.
- Method: Separate current-truth label scans from retained-negative historical witness text and explicitly adjudicate the latter by field context.
- Recurrence guard: Scan current truth surfaces for zero hits and validate retained-negative text as historical witness data rather than current claims.
- Rollback: Grant no stale-label credit to the overbroad gate, retain its result, keep the negative witness unchanged, and replay context-aware checks.
- Witnesses: V6482-M20-WFAIL, V6482-M20-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
