# GHC Family Method Flow State

- Phase: v651-v7-special-cli-prep
- Owner: Vesper Arlen
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### V6517-SPECIAL-M01 — Classify zero-output native commands by exit code

- Trigger: A successful native Git probe emits no stdout and is cast to false by PowerShell boolean evaluation.
- Method: Run the native command, capture LASTEXITCODE immediately, and classify success from zero.
- Recurrence guard: Never use stdout truthiness for merge-base or cat-file existence checks.
- Rollback: Retain the failed read-only attempt at zero credit; no Git history or sibling state requires rollback.
- Witnesses: V6517-SPECIAL-M01-WFAIL, V6517-SPECIAL-M01-WPASS

### V6517-SPECIAL-M02 — Use sparse-checkout add syntax supported by the active Git version

- Trigger: git sparse-checkout add rejects the initialization-only --no-cone option.
- Method: Keep non-cone mode from initialization and pass new patterns through add --stdin.
- Recurrence guard: Inspect subcommand help before carrying mode-selection flags across sparse-checkout verbs.
- Rollback: Retain the failed read-only attempt at zero credit; no Git history or sibling state requires rollback.
- Witnesses: V6517-SPECIAL-M02-WFAIL, V6517-SPECIAL-M02-WPASS

### V6517-SPECIAL-M03 — Bind repository paths inside every PowerShell wrapper

- Trigger: A verification wrapper references an unset local PowerShell repository variable.
- Method: Assign the literal owner-worktree path at the start of the wrapper before any Git or file probe.
- Recurrence guard: Require every standalone wrapper to declare its own repository binding rather than relying on caller state.
- Rollback: Retain the failed read-only attempt at zero credit; no Git history or sibling state requires rollback.
- Witnesses: V6517-SPECIAL-M03-WFAIL, V6517-SPECIAL-M03-WPASS

### V6517-SPECIAL-M04 — Read Method Flow state before requesting a transition

- Trigger: A passing witness auto-promotes a candidate method to validated and a wrapper requests validated again.
- Method: Inspect the authoritative method state after every witness and request only the next legal transition.
- Recurrence guard: Never assume a witness command leaves the method in its previous state.
- Rollback: Retain the failed read-only attempt at zero credit; no Git history or sibling state requires rollback.
- Witnesses: V6517-SPECIAL-M04-WFAIL, V6517-SPECIAL-M04-WPASS

### V6517-SPECIAL-M05 — Preserve contradictory routes before advisory normalization

- Trigger: The submitted expanded route is non-sequential and its normalized schedule changes future ownership.
- Method: Retain the raw failing audit, then validate the generated sequential candidate only as advisory teaching material.
- Recurrence guard: Never use a structurally valid normalization as launch or ownership authority.
- Rollback: Retain the failed read-only attempt at zero credit; no Git history or sibling state requires rollback.
- Witnesses: V6517-SPECIAL-M05-WFAIL, V6517-SPECIAL-M05-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
