# GHC Family Method Flow State

- Phase: v651-v8-special-cli-prep
- Owner: Ilyra Fen
- Methods: 8
- Passing witnesses: 8
- Failed witnesses retained: 10

## Preferred methods

### V6518-SPECIAL-M01 — Preassign PowerShell statement-loop output before piping

- Trigger: Windows PowerShell 5.1; statement-level foreach output must feed another pipeline
- Method: Assign the foreach output to an array variable, then pipe the variable.
- Recurrence guard: Reject wrappers containing a closing foreach block immediately followed by a pipeline token.
- Rollback: Return to separate scalar probes if the assigned-array form changes output semantics.
- Witnesses: V6518-SPECIAL-W01F2, V6518-SPECIAL-W01F, V6518-SPECIAL-W01P

### V6518-SPECIAL-M02 — Separate live-remote equality from local source verification

- Trigger: large Windows Git worktree; live-remote lookup and local checks combined
- Method: Run bounded local revision probes first and one separate live ls-remote probe second.
- Recurrence guard: Do not place ls-remote and broad worktree status in the same timed wrapper.
- Rollback: Retain the previous verified receipt and stop without mutation if either bounded probe fails.
- Witnesses: V6518-SPECIAL-W02F, V6518-SPECIAL-W02P

### V6518-SPECIAL-M03 — Separate broad worktree cleanliness from ancestry arithmetic

- Trigger: large sparse-capable repository; status and ancestry combined
- Method: Check HEAD, branch, upstream, and ancestry separately; then run one dedicated status command.
- Recurrence guard: Keep broad status as its own command with a dedicated timeout budget.
- Rollback: Use diff, cached-diff, and bounded untracked probes only as partial evidence until full status completes.
- Witnesses: V6518-SPECIAL-W03F, V6518-SPECIAL-W03P

### V6518-SPECIAL-M04 — Capture native exit codes before PowerShell object construction

- Trigger: Windows PowerShell 5.1; native command success must be included in a structured receipt
- Method: Run the native ancestry command first, capture its exit code in a scalar, then construct the PowerShell object.
- Recurrence guard: Do not embed native commands with statement separators inside hash-literal value expressions.
- Rollback: Use one scalar probe per command and stop without mutation if any exit code is nonzero.
- Witnesses: V6518-SPECIAL-W04F, V6518-SPECIAL-W04P

### V6518-SPECIAL-M05 — Use exact Method Flow subcommands and inspect auto-transition state

- Trigger: Method Flow ledger append or promotion; runner interface or current method state is not already materialized in context
- Method: Read each subcommand help, use record and witness with their exact file options, then inspect current state before requesting a transition.
- Recurrence guard: Interrogate exact help and current ledger state before every Method Flow mutation.
- Rollback: Stop after a failed transition, inspect the ledger, and apply only the missing state change.
- Witnesses: V6518-SPECIAL-W05F1, V6518-SPECIAL-W05F2, V6518-SPECIAL-W05P

### V6518-SPECIAL-M06 — Bind Meta Tool Box phase roots to the repository

- Trigger: Meta Tool Box build invocation; caller shell working directory differs from repository root
- Method: Resolve the phase root against the repository before invoking the Meta Tool Box build command.
- Recurrence guard: Pass an absolute repository-bound phase root and require the expected nonzero card count before credit.
- Rollback: Retain the zero-card refusal, change only the path binding, and rerun the bounded catalogue step.
- Witnesses: V6518-SPECIAL-W06F, V6518-SPECIAL-W06P

### V6518-SPECIAL-M07 — Bind aggregate assertions to their frozen authoritative artifact

- Trigger: a validator combines row-level and aggregate proposal evidence; the fields live in separate immutable artifacts
- Method: Read aggregate chain counts from the frozen provenance index and proposal rows from the proposal ledger.
- Recurrence guard: Resolve each count from its declared frozen authoritative artifact before writing a validator assertion.
- Rollback: Leave the frozen x1 files unchanged and correct only the validator lookup.
- Witnesses: V6518-SPECIAL-W07F, V6518-SPECIAL-W07P

### V6518-SPECIAL-M08 — Separate scanner definitions from confirmed staged payload hits

- Trigger: a staged validator contains the literal patterns it applies; privacy disposition must distinguish definitions from payload
- Method: Classify exact scanner implementation files as definition surfaces while continuing to scan every public payload file.
- Recurrence guard: Keep a minimal exact scanner-definition allowlist and report it separately from confirmed payload hits.
- Rollback: Remove the definition exception if the file begins carrying public payload rather than scanner code.
- Witnesses: V6518-SPECIAL-W08F, V6518-SPECIAL-W08P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
