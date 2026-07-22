# GHC Family Method Flow State

- Phase: v651-v7-special-cli-prep
- Owner: Vesper Arlen
- Methods: 10
- Passing witnesses: 11
- Failed witnesses retained: 12

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

### V6517-SPECIAL-M06 — Gate persistent baton length before evidence publication

- Trigger: A generated file-backed baton is below its authorized minimum word count.
- Method: Measure the file-backed baton before publication, preserve the undersized build as zero-credit evidence, add substantive successor guidance, and rerun only the evidence builder.
- Recurrence guard: Generate and count the persistent baton before the evidence commit; never treat an undersized draft as handoff-ready.
- Rollback: Keep the partial owner-local artifacts uncommitted, correct the deterministic builder, and regenerate them in place without repeating passed CLI preflights.
- Witnesses: V6517-SPECIAL-M06-WFAIL, V6517-SPECIAL-M06-WFAIL-2, V6517-SPECIAL-M06-WPASS

### V6517-SPECIAL-M07 — Bind x1 contamination tests to the immutable x1 Git tree

- Trigger: A plan-only x1 test runs after valid x2 artifacts exist in the current working tree.
- Method: Validate x1 contamination against the immutable x1 Git tree instead of the later x2 working tree.
- Recurrence guard: Lifecycle-specific tests must bind their file-domain assertions to the lifecycle commit they claim to validate.
- Rollback: Keep the failed combined test at zero credit, patch only the stale test domain, and rerun the isolated x1 module before the broader evidence suite.
- Witnesses: V6517-SPECIAL-M07-WFAIL, V6517-SPECIAL-M07-WPASS

### V6517-SPECIAL-M08 — Extend sparse checkout for exact new tool paths before staging

- Trigger: Git reports that intended owner-scoped files are outside the sparse-checkout definition.
- Method: Add only the exact new family-current script paths to the existing non-cone sparse-checkout definition, then stage the same reviewed path set.
- Recurrence guard: Before staging a new repository-local tool in a sparse lane, add its exact path to the sparse definition and remeasure the materialized surface.
- Rollback: Retain the failed staging attempt, leave the index content inspectable, and add only the missing paths without disabling sparse checkout.
- Witnesses: V6517-SPECIAL-M08-WFAIL, V6517-SPECIAL-M08-WPASS

### V6517-SPECIAL-M09 — Separate validator import roots and scanner definitions from evidence data

- Trigger: A validator passes direct tests but its script-mode loader cannot import named test modules, or scanner definitions match their own literals.
- Method: Bind the repository root into the validator's script-mode import path, split scanner self-test literals so they are not misclassified as data hits, preserve the failed receipt, and write the corrected pass separately.
- Recurrence guard: Validators invoked by file path must add the repository root before named test imports, and self-scanner fixtures must be classified or constructed without becoming data candidates.
- Rollback: Leave the failed receipt immutable, patch only import and scanner-definition domains, regenerate the index manifest with both receipt exclusions, and rerun the authoritative evidence validator once.
- Witnesses: V6517-SPECIAL-M09-WFAIL, V6517-SPECIAL-M09-WPASS, V6517-SPECIAL-M09-WFAIL-2, V6517-SPECIAL-M09-WPASS-2

### V6517-SPECIAL-M10 — Anchor lifecycle path guards to phase-root directories

- Trigger: A forbidden-lifecycle regex matches legitimate nested tooling directories whose names contain final.
- Method: Anchor forbidden lifecycle checks to the phase-root closeout, seal, and final directories rather than matching every nested path segment containing the word final.
- Recurrence guard: Lifecycle path guards must use a phase-root anchored directory expression and report the matched paths before stopping.
- Rollback: Retain the failed wrapper at zero credit, change no staged content, and rerun only the anchored path classifier.
- Witnesses: V6517-SPECIAL-M10-WFAIL, V6517-SPECIAL-M10-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
