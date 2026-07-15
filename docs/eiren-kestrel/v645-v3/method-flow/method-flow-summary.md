# GHC Family Method Flow State

- Phase: v645-gmut-thos-v3-x1-x2
- Owner: Eiren Kestrel
- Methods: 17
- Passing witnesses: 17
- Failed witnesses retained: 17

## Preferred methods

### V6453-M01 — Explicit scripts-path import bootstrap

- Trigger: Python helper invoked outside the scripts directory; family module import required
- Method: Insert the repository scripts directory at the front of the process-local import path before importing the collector.
- Recurrence guard: Resolve the script directory explicitly before importing phase-local modules.
- Rollback: Remove the process-local path insertion and use a package entry point if module layout changes.
- Witnesses: V6453-W01-F, V6453-W01-P

### V6453-M02 — Metadata-first bounded long read

- Trigger: Small local instruction file; initial full read timed out; file remains readable
- Method: Read file metadata first, then repeat the complete UTF-8 read with a bounded sixty-second command window.
- Recurrence guard: Use a sixty-second bound for slow local skill reads after checking size and type; never loop unbounded.
- Rollback: Stop after the bounded retry and retain an open tooling gap if the complete read still fails.
- Witnesses: V6453-W02-F, V6453-W02-P

### V6453-M03 — Absolute current-phase exclusion in recursive proposal scans

- Trigger: Recursive absolute filesystem scan; current phase path stored as repository-relative path
- Method: Resolve the current phase directory against the repository root and exclude that absolute parent before collecting prior proposals.
- Recurrence guard: Compare like-for-like absolute Path objects when excluding the active phase from recursive scans.
- Rollback: Stop the novelty audit if the prior count differs from the frozen predecessor count.
- Witnesses: V6453-W03-F, V6453-W03-P

### V6453-M04 — Normalized authoritative-source classifier

- Trigger: Human-readable authority labels; case-sensitive test expression
- Method: Normalize the authority label to lowercase and accept official, primary, or final specification classifications.
- Recurrence guard: Normalize descriptive classifications before matching and keep accepted classes explicit.
- Rollback: Fail the source ledger if an authority class remains unrecognized after normalization.
- Witnesses: V6453-W04-F, V6453-W04-P

### V6453-M05 — Literal line-bounded PowerShell diagnostic read

- Trigger: Complex mixed quote pattern; only bounded source context is needed
- Method: Read the file literally and select explicit line ranges instead of interpolating a complex search pattern.
- Recurrence guard: Prefer literal paths and bounded line slices for diagnostics when a regex would require nested shell quoting.
- Rollback: Stop rather than retrying a malformed quoted command; use a simpler read-only procedure.
- Witnesses: V6453-W05-F, V6453-W05-P

### V6453-M06 — Self-excluding privacy-pattern construction

- Trigger: Scanner source is part of its own public scan scope; forbidden literal appears verbatim in pattern source
- Method: Construct sensitive path tokens from benign fragments so the scanner source does not contain the forbidden literal it detects.
- Recurrence guard: Self-scan every public scanner and fragment forbidden literals without weakening the compiled expression.
- Rollback: Treat any self-hit as invalid, retain the hit, and do not issue a zero-hit receipt.
- Witnesses: V6453-W06-F, V6453-W06-P

### V6453-M07 — Blueprint-only sandbox fallback when runtime is unavailable

- Trigger: sandbox runtime unavailable; active route must not be interrupted; templates can still be linted
- Method: Compose and lint six fail-closed owner profiles, preserve runtime and installation as open, and defer feature changes, elevation, and reboot.
- Recurrence guard: Probe runtime availability before launch or installation claims; never infer success from a valid template.
- Rollback: Retain the templates as inactive blueprints and make no host change.
- Witnesses: V6453-W07-F, V6453-W07-P

### V6453-M08 — Runner-derived Method Flow count refresh

- Trigger: ledger methods or witnesses changed; derived counts were edited manually
- Method: Regenerate counts using the runner schema: methods, witnesses, state_events, recommendations, state histogram, and witness-result histogram.
- Recurrence guard: After every ledger mutation, invoke the family runner or reproduce its exact refresh_counts schema before validation.
- Rollback: Treat the ledger as invalid and retain the failed receipt until runner validation passes.
- Witnesses: V6453-W08-F, V6453-W08-P

### V6453-M09 — Inspect phase-local schemas before adapting inherited validators

- Trigger: a validator is adapted from an earlier phase; the current builder uses a phase-local schema; final receipts depend on exact field names
- Method: Inspect representative current artifacts, bind checks to their exact keys, and rerun the bounded validator without deleting the failed witness.
- Recurrence guard: Before first execution, compare every inherited validator lookup with one current phase artifact and retain mismatches as operational negatives.
- Rollback: Keep the validator invalid and preserve the exception until the schema alignment is reviewed.
- Witnesses: V6453-W09-F, V6453-W09-P

### V6453-M10 — Separate shell yield cadence from process lifetime

- Trigger: a repository suite can exceed the commentary cadence; the shell tool supports asynchronous output yielding; the process itself must remain bounded but alive
- Method: Give the test process a realistic bounded lifetime, let the orchestration layer yield after ten seconds, and poll the live cell while sending concise progress updates.
- Recurrence guard: Use tool yielding for responsiveness and reserve process timeouts for genuine upper bounds; never substitute one for the other.
- Rollback: Terminate the live cell if it exceeds the declared upper bound, preserve the incomplete log, and do not call it a test result.
- Witnesses: V6453-W10-F, V6453-W10-P

### V6453-M11 — Normalize generated JSON before exact staged review

- Trigger: JSON was generated by mixed Windows tooling; the exact staged reviewer decodes strict UTF-8; the content is otherwise valid JSON
- Method: Rewrite the bounded receipt through reviewed UTF-8-without-BOM text, retain all rows, then rerun strict staged parsing.
- Recurrence guard: Generate repository JSON with the family write_json helper or explicitly verify the first bytes before staging.
- Rollback: Keep the staged review invalid and retain the original parsing failure if normalization changes semantics.
- Witnesses: V6453-W11-F, V6453-W11-P

### V6453-M12 — Split large-index staging checks into witnessed bounded steps

- Trigger: the inherited index is large; multiple Git scans are composed in one wrapper; a failed early receipt requires repair
- Method: Run normalization, staging, manifest, exact review, and status summaries as separate bounded commands so each has a truthful exit status and retry boundary.
- Recurrence guard: Do not combine repeated large-index scans after a known invalid receipt; bound and witness each lifecycle step separately.
- Rollback: Leave the index staged but uncommitted, inspect the last valid receipt, and do not claim completion.
- Witnesses: V6453-W12-F, V6453-W12-P

### V6453-M13 — Bind lifecycle manifests to their declared immutable target

- Trigger: an evidence manifest was frozen before lifecycle receipts; the final worktree legitimately adds or updates closeout metadata; the evidence commit remains ancestral and immutable
- Method: Read the manifest's declared evidence target, hash those committed blobs with logical newline normalization, and validate later lifecycle files through the separate final staged manifest.
- Recurrence guard: Every manifest validator must select its hash domain and immutable target from the manifest lifecycle rather than silently defaulting to the mutable worktree.
- Rollback: Keep parity invalid if the target is absent, nonancestral, or mismatched; never refresh evidence hashes merely to hide lifecycle drift.
- Witnesses: V6453-W13-F, V6453-W13-P

### V6453-M15 — Resolve the current phase ledger before Method Flow mutation

- Trigger: the phase contains a Method Flow ledger; the caller relies on a remembered filename instead of current phase evidence; the runner performs a mutating subcommand
- Method: Enumerate the phase-scoped Method Flow artifacts read-only, select the existing state ledger, and verify its schema, phase, and owner before invoking a mutating runner command.
- Recurrence guard: Every Method Flow mutation must resolve the ledger from the current phase artifact set rather than a remembered or generic filename.
- Rollback: If no single matching ledger exists, preserve the failure and stop without initializing or overwriting a replacement.
- Witnesses: V6453-W15-F, V6453-W15-P

### V6453-M14 — Separate combined metadata reads under large-index latency

- Trigger: the repository carries a large inherited index; multiple lifecycle artifacts are read in one diagnostic wrapper; the wrapper has a short fixed timeout
- Method: Read one literal lifecycle artifact per command, or raise the bounded read timeout only after confirming the target path and metadata size; do not over-combine diagnostics.
- Recurrence guard: Lifecycle diagnostics must prefer one-file literal reads and reserve combined wrappers for operations already measured within their timeout budget.
- Rollback: If a decomposed read still fails, preserve the failure and stop before interpreting or rewriting the artifact.
- Witnesses: V6453-W14-F, V6453-W14-P

### V6453-M16 — Synchronize structural assertions after Method Flow growth

- Trigger: a new Method Flow method and witnesses were appended; phase validators and tests contain exact structural counts; only a subset of those assertions was updated
- Method: After appending a Method Flow incident, audit every phase-local validator, test, receipt, and index assertion for the former method, witness, state, and negative counts before rerunning.
- Recurrence guard: Use one bounded search for the prior exact counts across the phase-local test, validator, receipts, and index surfaces after every ledger growth event.
- Rollback: If any count cannot be reconciled arithmetically with the append-only ledger, keep validation failed and do not edit evidence to fit the assertion.
- Witnesses: V6453-W16-F, V6453-W16-P

### V6453-M17 — Derive mutable lifecycle component invariants from append-only rows

- Trigger: append-only negative and Method Flow rows can grow during validation; the validator carries fixed historical component counts; the total receipt has already been updated
- Method: Keep the frozen inherited, x1, and synthetic baselines explicit, but derive the growing x2 row count and Method Flow state histogram from the append-only collections themselves.
- Recurrence guard: Use fixed counts only for frozen inputs; for lifecycle-grown collections validate row-count equality, balanced witnesses, unique identifiers, and all-preferred state dynamically.
- Rollback: If a derived invariant disagrees with the underlying rows, preserve the validator failure and do not coerce either side.
- Witnesses: V6453-W17-F, V6453-W17-P

## Retained boundary

Software and synthetic fixtures can establish only bounded structural behavior. They do not establish empirical GMUT confirmation, THOS effectiveness, production identity assurance, legal or cultural authority, independent reproduction, AGI/ASI, complete accessibility, exhaustive security, or Stage 20 readiness.
