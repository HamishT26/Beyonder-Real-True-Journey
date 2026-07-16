# GHC Family Method Flow State

- Phase: v645-gmut-thos-v8-x1-x2
- Owner: Sylven Arc
- Methods: 8
- Passing witnesses: 8
- Failed witnesses retained: 8

## Preferred methods

### V6458-M01 — Query explicit upstream refs after shorthand transformation

- Trigger: read-only Git startup probe; revision shorthand was transformed before native parsing
- Method: Replace transformed revision shorthand with an explicit branch-ref lookup and retain the original parser failure.
- Recurrence guard: In wrappers that may transform metasyntax, never assume Git revision shorthand reaches the native command unchanged.
- Rollback: Give the failed wrapper zero startup credit and make no branch change until the explicit query passes.
- Witnesses: V6458-W01-F, V6458-W01-P

### V6458-M02 — Decompose a timed-out parallel startup probe into evidenced child commands

- Trigger: multiple evidence-producing startup children; parallel wrapper returned no reliable child result set
- Method: Decompose composite startup probes so each child has an independent deadline, result, and evidence-credit decision.
- Recurrence guard: Parallelize evidence-producing probes only when the orchestrator returns every child result even if one times out.
- Rollback: Make no branch change until all required split probes pass.
- Witnesses: V6458-W02-F, V6458-W02-P

### V6458-M03 — Decompose a timed-out multi-file text probe into bounded per-file reads

- Trigger: explicitly named x1 working files; combined read-only scan returned no usable output before its deadline
- Method: Split multi-file working-tree probes by file when shared-drive latency consumes the original envelope, retaining the timed-out command as a negative.
- Recurrence guard: Treat timeout-without-output as no evidence; never infer either matches or cleanliness from it.
- Rollback: Give the combined scan zero review credit and make no x1 claim until the per-file reads complete.
- Witnesses: V6458-W03-F, V6458-W03-P

### V6458-M04 — Normalize generated family-index line endings before x1 sealing

- Trigger: family-index generator emitted CRLF text; x1 structural review rejected both generated artifacts
- Method: Apply a narrowly scoped LF normalization step to the two family-index generator outputs before staging and sealing.
- Recurrence guard: Require the structural reviewer to reject every owner artifact containing CRLF rather than relying on Git checkout normalization.
- Rollback: Retain the failed review, remove all x1 validation credit from it, and do not stage receipts until the unchanged reviewer passes.
- Witnesses: V6458-W04-F, V6458-W04-P

### V6458-M05 — Split an overbroad substantive patch after context verification failure

- Trigger: v645-v8 x2 evidence validation; same-owner local tooling
- Method: Retain the rejected patch, verify that no file changed, and apply the core-runner replacement alone before reviewing runtime separately.
- Recurrence guard: Do not combine independent context-sensitive edits unless every expected hunk was re-read from the current file.
- Rollback: Give the rejected patch zero implementation credit and preserve the source tree until the bounded replacement succeeds.
- Witnesses: V6458-W05-F, V6458-W05-P, V6458-W05-F, V6458-W05-P

### V6458-M06 — Pass multi-alternative stale-term search patterns as quoted data

- Trigger: v645-v8 x2 evidence validation; same-owner local tooling
- Method: Retain the parser failure, pass the unchanged alternation as a double-quoted data argument, and split the explicitly named files into bounded groups.
- Recurrence guard: Keep shell metacharacters and apostrophes inside a verified quoted data argument; a parser error receives zero scan credit.
- Rollback: Treat the failed scan as no evidence and make no stale-label claim until the quoted grouped searches finish.
- Witnesses: V6458-W06-F, V6458-W06-P, V6458-W06-F, V6458-W06-P

### V6458-M07 — Separate verification commands after inline summary quoting failure

- Trigger: v645-v8 x2 evidence validation; same-owner local tooling
- Method: Retain the syntax error, give every unavailable child result zero credit, and rerun tests, validators, Git checks, and JSON or privacy summaries as separately bounded commands.
- Recurrence guard: Do not place nested quoted JSON indexing inside a shell-embedded f-string; result aggregation must not hide independently required evidence.
- Rollback: Discard the wrapper result set and do not advance the evidence commit until every separated command passes.
- Witnesses: V6458-W07-F, V6458-W07-P, V6458-W07-F, V6458-W07-P

### V6458-M08 — Reject ancestry summaries built from a mistyped source revision

- Trigger: v645-v8 x2 evidence validation; same-owner local tooling
- Method: Retain the fatal error, withdraw the merge-count value, and rerun the merge count alone with the exact verified source revision and explicit exit-status check.
- Recurrence guard: A summary is invalid if any child writes a Git fatal error; never coerce absent numeric output into evidence.
- Rollback: Give the failed summary no merge-count credit and do not commit evidence until the isolated ancestry command passes.
- Witnesses: V6458-W08-F, V6458-W08-P, V6458-W08-F, V6458-W08-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
