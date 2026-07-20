# GHC Family Method Flow State

- Phase: v650-v8
- Owner: Ilyra Fen
- Methods: 9
- Passing witnesses: 9
- Failed witnesses retained: 9

## Preferred methods

### V6508-M01 — Recover from combined broad Git preflight timeout without erasing the failed witness

- Trigger: combined broad Git preflight timeout
- Method: Split branch, live-ref, worktree, ancestry, and status checks into independently bounded probes.
- Recurrence guard: Never combine broad branch, ref, worktree, and status discovery under one short wrapper.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M01-WFAIL, V6508-M01-WPASS

### V6508-M02 — Recover from native output early-close failure without erasing the failed witness

- Trigger: native output early-close failure
- Method: Consume the complete immutable blob first and then slice the in-memory text for inspection.
- Recurrence guard: Do not pipe native Git blob output to an early-closing consumer when complete-read evidence is required.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M02-WFAIL, V6508-M02-WPASS

### V6508-M03 — Recover from short-bound Git diff timeout without erasing the failed witness

- Trigger: short-bound Git diff timeout
- Method: Use explicit tracked-status and untracked-count probes with a wider bounded wrapper.
- Recurrence guard: Use attributable status probes instead of a short silent diff wrapper on a large Windows worktree.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M03-WFAIL, V6508-M03-WPASS

### V6508-M04 — Recover from PowerShell foreach pipeline parse without erasing the failed witness

- Trigger: PowerShell foreach pipeline parse
- Method: Materialize foreach output in an explicit array before piping or serializing it.
- Recurrence guard: Never pipe directly from a statement-level foreach block in Windows PowerShell 5.1.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M04-WFAIL, V6508-M04-WPASS

### V6508-M05 — Recover from bounded search early-close failure without erasing the failed witness

- Trigger: bounded search early-close failure
- Method: Read exact files and bounded result sets without prematurely closing the producer.
- Recurrence guard: Do not grant search credit when an early consumer termination makes producer completion ambiguous.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M05-WFAIL, V6508-M05-WPASS

### V6508-M06 — Recover from owner-manifest coverage scope error without erasing the failed witness

- Trigger: owner-manifest coverage scope error
- Method: Compare the immutable source-to-final path set across documentation, scripts, and tests against the declared owner manifest and exclusions.
- Recurrence guard: Define owner coverage from the exact Git change set, never from one assumed subtree.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M06-WFAIL, V6508-M06-WPASS

### V6508-M07 — Recover from stale Method Flow subcommand names without erasing the failed witness

- Trigger: stale Method Flow subcommand names
- Method: Inspect the installed record, witness, and set-state help and use only those exact subcommands.
- Recurrence guard: Treat remembered local-runner subcommands as unverified until current --help confirms them.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M07-WFAIL, V6508-M07-WPASS

### V6508-M08 — Split broad builder patches at exact current function boundaries

- Trigger: A long patch spans multiple generated-style regions and one remembered context line is stale.
- Method: Read the exact current function boundaries and split the update into small uniquely anchored patches.
- Recurrence guard: Do not combine unrelated builder changes behind one long remembered context block.
- Rollback: Treat the rejected patch as zero change and preserve the pre-patch file unchanged.
- Witnesses: V6508-M08-WFAIL, V6508-M08-WPASS

### V6508-M09 — Inspect exact UTF-8 source bytes before patching rendered separators

- Trigger: Console rendering differs from the UTF-8 code points stored in a source literal.
- Method: Patch non-Unicode fields independently, then inspect exact source bytes before replacing the two rendered separator literals.
- Recurrence guard: Do not use console-rendered mojibake as patch context for UTF-8 source.
- Rollback: Treat the rejected patch as zero change and preserve the UTF-8 source unchanged.
- Witnesses: V6508-M09-WFAIL, V6508-M09-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
