# GHC Family Method Flow State

- Phase: v651-v8-special-cli-prep
- Owner: Ilyra Fen
- Methods: 3
- Passing witnesses: 3
- Failed witnesses retained: 4

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

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
