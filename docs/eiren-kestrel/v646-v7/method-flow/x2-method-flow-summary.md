# GHC Family Method Flow State

- Phase: v646-gmut-thos-v7-x1-x2
- Owner: Eiren Kestrel
- Methods: 8
- Passing witnesses: 9
- Failed witnesses retained: 9

## Preferred methods

### V6467-M01 — Resolve frozen proposal collection from declared schema keys

- Trigger: inherited JSON index; unknown proposal collection field; PowerShell ConvertFrom-Json; partial output after runtime error
- Method: Inspect and record the frozen-index top-level keys first, then select the declared proposal collection by exact schema field and fail explicitly if it is absent.
- Recurrence guard: Never let a later successful PowerShell expression mask an earlier schema-access error; inspect declared keys and check every native or runtime failure before credit.
- Rollback: Give the partial probe zero novelty-audit credit, retain the null-array error, and rerun only the smallest key-first read-only query.
- Witnesses: V6467-M01-W-F, V6467-M01-W-P

### V6467-M02 — Serialize PowerShell loop results after explicit accumulation

- Trigger: PowerShell foreach loop; structured result objects; JSON serialization; read-only novelty audit
- Method: Accumulate PowerShell loop results in an explicit array and pipe that completed array to ConvertTo-Json after the loop.
- Recurrence guard: PowerShell loops that feed serialization must assign to an explicit results array; parser failures receive no downstream evidence credit.
- Rollback: Retain the parser failure, award zero novelty-search credit, and rerun only the corrected read-only loop.
- Witnesses: V6467-M02-W-F, V6467-M02-W-P

### V6467-M03 — Split login-shell startup from bounded filesystem and compiler probes

- Trigger: Windows PowerShell login shell; large Git worktree; short wrapper deadline; filesystem or compiler inspection
- Method: Disable login-shell initialization for bounded probes, use an already responsive neutral working directory, address the target by absolute path, and separate existence, content, and compilation checks.
- Recurrence guard: Do not retry an identical timed-out login-shell inspection; change one causal dimension, split the probe, and preserve the original timeout as a failed witness.
- Rollback: Award no inspection or compilation credit to either timeout and retain both wrapper expirations before using the bounded recovery.
- Witnesses: V6467-M03-W-F, V6467-M03-W-P

### V6467-M04 — Interrogate Method Flow subcommand help before receipt emission

- Trigger: Method Flow CLI; receipt refresh; locally guessed option name; partially completed command sequence
- Method: Read the exact validate and summarize subcommand help, use validate --receipt and summarize --json-output plus --markdown-output, and avoid replaying already successful append-only mutations.
- Recurrence guard: Treat each Method Flow subcommand as a separate contract; check help before first use and resume only from the first failed step.
- Rollback: Retain the parser failure, award no validation-receipt credit to it, and do not duplicate the preceding successful ledger events.
- Witnesses: V6467-M04-W-F, V6467-M04-W-P

### V6467-M05 — Fail closed and rename exact inherited portfolio collisions

- Trigger: expanded x1 portfolio; inherited portfolio corpus; exact normalized title collision; pre-materialization novelty gate
- Method: Emit each exact collision and source, rename the new designs around their phase-specific acceptance semantics, and rerun the unchanged counted audit before materialization.
- Recurrence guard: No quota, prefix, or nearby purpose earns novelty credit when a normalized portfolio title collides exactly with inherited work.
- Rollback: Write no x1 portfolio, retain the collision evidence, and change only the colliding declarations before rerunning the same audit.
- Witnesses: V6467-M05-W-F, V6467-M05-W-P

### V6467-M06 — Discover prior artifact names before reading a presumed ledger

- Trigger: inherited phase packet; unknown artifact filename; compound shell inspection; later successful output after an earlier path error
- Method: Enumerate bounded prior-phase filenames first, select the actual skill-build-use and runner-build-use receipts, and treat an earlier missing-path error as failure even when later commands succeed.
- Recurrence guard: Never infer an artifact filename from a conceptual label; discover the bounded file surface and stop compound-command success from masking an earlier error.
- Rollback: Give the presumed-path read zero reuse credit, retain the missing-path witness, and use only the discovered exact filenames.
- Witnesses: V6467-M06-W-F, V6467-M06-W-P

### V6467-M07 — Pin UTF-8 for console diagnostics containing Māori text

- Trigger: Windows console; Python stdout; Unicode source text; legacy code page
- Method: Set PYTHONIOENCODING=utf-8 for the bounded diagnostic, preserve UTF-8 source and artifacts, and rerun only the incomplete display.
- Recurrence guard: Any diagnostic expected to emit te reo Māori or other non-ASCII text must pin UTF-8 before Python starts; partial output earns no complete-review credit.
- Rollback: Retain the encoding exception, award no complete-list credit, and do not transliterate or remove the source text.
- Witnesses: V6467-M07-W-F, V6467-M07-W-P, V6467-M07-W-F2, V6467-M07-W-P2

### V6467-M08 — Bind x1 lifecycle assertions to the immutable x1 Git object

- Trigger: strict x1-before-x2 lifecycle; x1 tests rerun during x2; append-only Method Flow growth; live working-tree assertions
- Method: Check x2 absence against the exact x1 Git object and check x1 Method Flow records as a preserved identified subset while allowing later append-only methods and witnesses.
- Recurrence guard: Lifecycle tests must state whether their domain is an immutable commit or the current head; never infer historical contamination from legitimate additive later-phase files.
- Rollback: Retain the two-test failure, award no current-suite credit, and change only the time-domain assertions before rerunning the same 26 tests.
- Witnesses: V6467-M08-W-F, V6467-M08-W-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
