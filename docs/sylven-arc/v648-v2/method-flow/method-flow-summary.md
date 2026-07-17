# GHC Family Method Flow State

- Phase: v648-gmut-thos-v2-x1-x2
- Owner: Sylven Arc
- Methods: 7
- Passing witnesses: 7
- Failed witnesses retained: 7

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

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
