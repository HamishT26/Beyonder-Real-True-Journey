# GHC Family Method Flow State

- Phase: v646-gmut-thos-v4-x1-x2
- Owner: Orin Thale
- Methods: 22
- Passing witnesses: 22
- Failed witnesses retained: 22

## Preferred methods

### V6464-M01 — Split no-login startup audit

- Trigger: known owner and source paths; multiple read-only evidence classes; ordinary user privileges
- Method: Use the emitted receipt without repeating the broad probe and split later checks into bounded no-login commands.
- Recurrence guard: Do not combine recursive file counts, live remote queries, ancestry, and state summaries in one repeated probe.
- Rollback: Stop without mutation and retain unavailable state if any bounded component fails.
- Witnesses: V6464-M01-F, V6464-M01-P

### V6464-M02 — Schema-first frozen-index selection

- Trigger: JSON schema may have evolved; PowerShell object access is used; read-only corpus audit
- Method: Inspect top-level keys, select prior_proposals explicitly, and null-check the first object before indexing.
- Recurrence guard: Never treat @($null).Count as proof that a source collection exists.
- Rollback: Treat the failed probe as zero evidence and rerun only the schema-first read.
- Witnesses: V6464-M02-F, V6464-M02-P

### V6464-M03 — Broad-first then exact-pin adapter transformation

- Trigger: a compatibility source adapter is used; owner and phase strings overlap source paths; pre-run review is available
- Method: Apply broad owner and phase substitutions first, then pin inherited Sable paths and Tamar routing targets exactly.
- Recurrence guard: Inspect transformed source paths and targets before executing any compatibility adapter.
- Rollback: Do not execute the adapter; restore the last reviewed replacement order.
- Witnesses: V6464-M03-F, V6464-M03-P

### V6464-M04 — Enumerate before witness-template selection

- Trigger: historical filenames vary by phase; a bounded source directory exists; only a template is needed
- Method: Enumerate the directory first and select an existing method-based witness filename.
- Recurrence guard: Do not synthesize historical witness filenames from memory.
- Rollback: Treat missing-file output as no evidence and leave source files untouched.
- Witnesses: V6464-M04-F, V6464-M04-P

### V6464-M05 — Underscore-form module import substitution

- Trigger: Python source is adapted across phases; module names encode the phase; the source corpus count changed
- Method: Replace ghc_family_v646_v3 with ghc_family_v646_v4 before executing the adapted builder.
- Recurrence guard: Preflight both hyphenated artifact identifiers and underscore-form Python imports.
- Rollback: Stop before artifact generation, retain the failed build, and rerun only after import identity is verified.
- Witnesses: V6464-M05-F, V6464-M05-P

### V6464-M06 — Parent-creating phase JSON writer

- Trigger: a builder introduces a new nested phase directory; the write helper receives a relative path; deterministic regeneration is safe
- Method: Create target.parent before every phase JSON write and regenerate the deterministic x1 packet.
- Recurrence guard: All phase writers must create parents immediately before writing a new relative path.
- Rollback: Assign no credit to the partial build and overwrite only owner-scoped generated x1 artifacts from frozen definitions.
- Witnesses: V6464-M06-F, V6464-M06-P

### V6464-M07 — Schema-first Method Flow summary projection

- Trigger: a derived summary is read; field names may differ from validation receipts; the authoritative ledger remains intact
- Method: Inspect top-level and count keys first, then select authoritative fields without rerunning existing methods.
- Recurrence guard: Never infer Method Flow summary field names from a prior phase or wrapper.
- Rollback: Discard only the null convenience projection and preserve the valid runner receipt and ledger.
- Witnesses: V6464-M07-F, V6464-M07-P

### V6464-M08 — Package-metadata desktop version fallback

- Trigger: desktop version verification is required; running-process version fields are empty; updates are prohibited
- Method: Read bounded installed-package metadata and record the version with verify-only status.
- Recurrence guard: Treat executable and package metadata as alternative read-only surfaces; never infer an update from an empty process field.
- Rollback: Record the desktop version as unavailable if both read-only surfaces fail; do not install or update.
- Witnesses: V6464-M08-F, V6464-M08-P

### V6464-M09 — Direct-shell Codex CLI version fallback

- Trigger: Codex CLI verification is required; Python subprocess command resolution fails; updates are prohibited
- Method: Use a bounded no-login shell version query and carry only the observed version and verify-only action into the receipt.
- Recurrence guard: On Windows, verify the command surface independently before treating Python subprocess absence as CLI absence.
- Rollback: Record unavailable if the direct shell also fails; never install or update.
- Witnesses: V6464-M09-F, V6464-M09-P

### V6464-M10 — Verified-context apply_patch recovery

- Trigger: apply_patch rejected an owner-scoped edit; no file changed; the target source is bounded
- Method: Read numbered source anchors and apply the correction against exact verified context.
- Recurrence guard: Never infer patch context from generated output shape; inspect the source lines first.
- Rollback: Retain the rejected patch as zero-change evidence and do not use a bulk rewrite fallback.
- Witnesses: V6464-M10-F, V6464-M10-P

### V6464-M11 — Numbered direct-read source context lookup

- Trigger: exact patch context is required; the source file is known; regex matching adds no evidence
- Method: Read bounded numbered line ranges directly instead of composing a regex and path.
- Recurrence guard: Use literal paths separately from search expressions and prefer direct line ranges for patch anchors.
- Rollback: Treat the regex failure as no lookup evidence and leave the file unchanged.
- Witnesses: V6464-M11-F, V6464-M11-P

### V6464-M12 — Underscore-aware x1 staged allowlist adapter

- Trigger: a predecessor staged reviewer is adapted; allowed filenames encode the phase with underscores; the path set must remain exact
- Method: Substitute underscore-form phase identifiers and rerun without broadening the explicit allowlist.
- Recurrence guard: Preflight both artifact identifiers and Python filenames in every compatibility reviewer.
- Rollback: Keep the failed staged receipt as zero credit and do not add wildcard allowances.
- Witnesses: V6464-M12-F, V6464-M12-P

### V6464-M13 — Builder-owned final footprint receipt

- Trigger: deterministic regeneration resets generated receipts; the final owner file set is known; the builder remains owner-scoped
- Method: Set the measured final footprint in the builder postprocessor and regenerate once, rather than patching an outdated generated value.
- Recurrence guard: Finalize generated receipt values in the builder source before the last regeneration.
- Rollback: Keep the rejected patch as zero change and leave rotation gated if the exact footprint cannot be measured.
- Witnesses: V6464-M13-F, V6464-M13-P

### V6464-M14 — Unittest exit-code separation from stderr

- Trigger: Python unittest writes progress to stderr; PowerShell captures native output; the process exit code is authoritative
- Method: Run unittest without ErrorActionPreference Stop and inspect LASTEXITCODE only after the process ends.
- Recurrence guard: Do not classify native stderr as failure when the tool's contract uses stderr for normal progress.
- Rollback: Give the interrupted wrapper no validation credit and rerun only the test process.
- Witnesses: V6464-M14-F, V6464-M14-P

### V6464-M15 — Single-iteration staged fixed-point witness

- Trigger: staged review rewrites self-excluding receipts; Python startup is nontrivial; blob-pair convergence is required
- Method: Run one review per invocation, stage both receipts, and compare staged blob IDs with the prior invocation.
- Recurrence guard: Do not place repeated interpreter startups inside one closeout timeout envelope.
- Rollback: Retain the interrupted aggregate as zero credit and keep the latest staged pair pending verification.
- Witnesses: V6464-M15-F, V6464-M15-P

### V6464-M16 — Sixty-second single staged-review envelope

- Trigger: the staged set is large; one reviewer invocation is required; aggregate loops remain prohibited
- Method: Give one reviewer invocation sixty seconds, then inspect staged blob IDs in a separate bounded command.
- Recurrence guard: Keep review execution and pair reporting in separate invocations and never widen an aggregate loop.
- Rollback: Treat written-but-unreported receipts as pending and award no fixed-point credit until re-read.
- Witnesses: V6464-M16-F, V6464-M16-P

### V6464-M17 — Frozen route-invariant vocabulary check

- Trigger: a phase-local route skill is smoke-tested; the frozen route plan is authoritative; no route action is authorized yet
- Method: Inspect the frozen route preconditions and require the invariant tokens exactly one and named-lane replay rather than an unregistered local-only phrase.
- Recurrence guard: Bind smoke checks to frozen invariant tokens and inspect the source plan before adding narrower vocabulary.
- Rollback: Keep the skill portfolio invalid and send no route message if the corrected invariant check fails.
- Witnesses: V6464-M17-F, V6464-M17-P

### V6464-M18 — Frozen-x1-aware compatibility normalization

- Trigger: a successor reuses a prior phase serialization scaffold; the exact x1 commit is known; the evidence candidate is not committed
- Method: Restore the accidental tracked x1 byte changes from the exact x1 commit, then restrict compatibility normalization to new x2 artifacts and exact schema or proposal identifiers.
- Recurrence guard: Before normalizing a generated tree, query exact x1 object membership and skip every path present at the frozen x1 revision; transform only exact schema and proposal-ID tokens.
- Rollback: Keep the evidence candidate uncommitted and route unsent if any undeclared x1 path remains byte-different from the frozen commit.
- Witnesses: V6464-M18-F, V6464-M18-P

### V6464-M19 — Explicit UTF-8 phase text probe

- Trigger: repository text may contain non-ASCII Unicode; a Python validation or count probe reads phase files
- Method: Pass encoding='utf-8' to every Python text read used for phase counts or validation and keep the failed locale-default probe as a negative witness.
- Recurrence guard: Use explicit UTF-8 for every repository text read and set PYTHONUTF8 for bounded validation subprocesses.
- Rollback: Do not report file, JSON, or word counts from a probe that fails decoding.
- Witnesses: V6464-M19-F, V6464-M19-P

### V6464-M20 — Shape-aware aggregate runner witness projection

- Trigger: a runner witness may be a single result or a named result map; each mapped result declares a passed boolean
- Method: Classify a runner witness as passing when it either has a top-level passed or valid boolean, or is a nonempty mapping whose every result object has passed true.
- Recurrence guard: Inspect witness shape before projecting pass state and require every child result to pass for mapped all-runner witnesses.
- Rollback: Keep the aggregate runner receipt invalid and assign zero aggregate credit if any child result is missing or fails.
- Witnesses: V6464-M20-F, V6464-M20-P

### V6464-M21 — File-based nonpackage test selection

- Trigger: the repository tests directory has no package initializer; the exact current files and two inherited exclusions are known
- Method: Load the two current test files with file-based discovery instead of package-qualified names, then run the scoped selector separately to expose and correct its one exact error without broadening exclusions.
- Recurrence guard: Inspect whether the test directory is packaged before selecting import names, use exact file patterns when it is not, and never hide a scoped error by expanding the exclusion set.
- Rollback: Keep the validation runner invalid and award zero current or scoped pass credit until every eligible test runs without failures or errors.
- Witnesses: V6464-M21-F, V6464-M21-P

### V6464-M22 — Explicit PowerShell path-array stale-label scan

- Trigger: multiple known repository paths require one bounded search; PowerShell is the active shell
- Method: Pass an explicit PowerShell path array to ripgrep and keep the pattern as a separate literal argument; do not use Bash brace expansion in a PowerShell command.
- Recurrence guard: Use explicit PowerShell arrays for multiple literal paths and never copy shell brace-list syntax into PowerShell wrappers.
- Rollback: Assign zero stale-label credit to the parser-failed wrapper and leave the staged candidate unchanged.
- Witnesses: V6464-M22-F, V6464-M22-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
