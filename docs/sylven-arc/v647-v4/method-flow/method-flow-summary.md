# GHC Family Method Flow State

- Phase: v647-gmut-thos-v4-x1-x2
- Owner: Sylven Arc
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### V6474-M01 — Assign PowerShell loop output before serialization

- Trigger: A read-only PowerShell loop builds structured manifest summaries for later serialization.
- Method: Assign loop output to a variable before piping, or use one bounded structured reader.
- Recurrence guard: Do not pipe directly from a PowerShell foreach statement in compound diagnostics; check each native exit explicitly.
- Rollback: Discard the failed read-only command; it changed no file, ref, index, or worktree.
- Witnesses: V6474-M01-W-F, V6474-M01-W-P

### V6474-M02 — Decompose compound repository inspection probes

- Trigger: A repository inspection combines Git status and filesystem discovery under one short execution envelope.
- Method: Decompose repository status and file discovery into separate bounded commands with explicit timeouts.
- Recurrence guard: Do not combine Git worktree inspection and recursive file discovery in one short-deadline shell invocation.
- Rollback: Terminate the timed-out read-only probe and discard its incomplete output; it changed no file, ref, index, or worktree.
- Witnesses: V6474-M02-W-F, V6474-M02-W-P

### V6474-M03 — Validate structured JSON member shapes after patching

- Trigger: A structured JSON ledger contains multiple arrays whose members share repeated closing-brace context.
- Method: Rebuild the structured state from named records and validate array member shapes as well as JSON syntax.
- Recurrence guard: Never use context-free closing-brace hunks against repeated JSON arrays; target named blocks or rebuild the complete structured document and validate member schemas.
- Rollback: Discard the malformed state assembly, retain its failure witness, and reconstruct the state from the standalone method and witness records.
- Witnesses: V6474-M03-W-F, V6474-M03-W-P

### V6474-M04 — Pin historical lifecycle assertions to immutable commit blobs

- Trigger: A phase reuses x1 tests after x2 has intentionally advanced mutable owner ledgers.
- Method: Pin historical x1 assertions to the immutable x1 commit while testing mutable x2 ledgers separately, and normalize the evidence label to the asserted lowercase form.
- Recurrence guard: Historical lifecycle tests must read immutable commit blobs; current lifecycle tests may read the working tree, and normative labels must be asserted with an explicitly declared case policy.
- Rollback: Keep the frozen x1 commit authoritative, retain the failed 25-test receipt, and modify only lifecycle targeting and label casing before replay.
- Witnesses: V6474-M04-W-F, V6474-M04-W-P

### V6474-M05 — Gate evidence commits on exact staged diff hygiene

- Trigger: An exact owner-scoped evidence candidate has been staged but not committed.
- Method: Remove the single extra EOF blank line, restage the exact file, and rerun Git diff hygiene before any commit.
- Recurrence guard: Run exact staged diff hygiene before manifest generation and commit; do not treat advisory line-ending notices as the same class as a reported whitespace error.
- Rollback: Do not commit the staged candidate; retain the failure and correct only the reported EOF whitespace.
- Witnesses: V6474-M05-W-F, V6474-M05-W-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
