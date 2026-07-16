# GHC Family Method Flow State

- Phase: v646-gmut-thos-v8-x1-x2
- Owner: Ilyra Fen
- Methods: 6
- Passing witnesses: 5
- Failed witnesses retained: 6

## Preferred methods

### V6468-M01 — Follow the exact reference path declared by the selected skill

- Trigger: a selected skill names a required reference; a similarly named path is tempting
- Method: Read the selected SKILL.md completely and resolve its literal relative reference before opening the schema.
- Recurrence guard: Never infer a reference filename when SKILL.md declares one.
- Rollback: Give the failed read zero instruction credit and make no task mutation.
- Witnesses: V6468-M01-F, V6468-M01-P

### V6468-M02 — Collect PowerShell loop output before formatting or piping

- Trigger: a loop emits objects; the result will be formatted or piped
- Method: Assign the loop output to a variable, then pipe that variable.
- Recurrence guard: Evaluate compound PowerShell producers before formatting consumers.
- Rollback: Give the parser-failed wrapper zero diagnostic credit.
- Witnesses: V6468-M02-F, V6468-M02-P

### V6468-M04 — Use Git-index path evidence for exact skill-name collision preflight

- Trigger: candidate names map to package paths; the worktree content surface is large
- Method: Enumerate tracked Git paths once and compare candidate names against the returned path set.
- Recurrence guard: Use path evidence for package-name collisions; reserve content search for a bounded explicit file set.
- Rollback: Give the timed-out content scan zero absence credit and leave the candidate list unfrozen until the path witness passes.
- Witnesses: V6468-M04-F, V6468-M04-P

### V6468-M05 — Invoke PowerShell command shims through PowerShell

- Trigger: a command resolves to a PowerShell script shim; a Python subprocess probe needs only version text
- Method: Invoke the shim through a no-profile PowerShell command and capture only its sanitized version line.
- Recurrence guard: Resolve the command type before selecting a subprocess invocation method.
- Rollback: Give the failed builder zero packet credit and make no permission or installation change.
- Witnesses: V6468-M05-F, V6468-M05-P

### V6468-M06 — Require diff-hygiene success after staged-review fixed point

- Trigger: staged review and manifest are byte-stable; diff hygiene has not yet passed
- Method: Retain the failed staged state, normalize only the reported EOF, restage, and rerun the unchanged staged and diff gates.
- Recurrence guard: A stable manifest is necessary but never substitutes for diff hygiene.
- Rollback: Do not commit the stable but hygiene-invalid staged tree.
- Witnesses: V6468-M06-F, V6468-M06-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
