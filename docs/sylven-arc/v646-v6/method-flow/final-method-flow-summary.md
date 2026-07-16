# GHC Family Method Flow State

- Phase: v646-gmut-thos-v6-x1-x2-final
- Owner: Sylven Arc
- Methods: 4
- Passing witnesses: 4
- Failed witnesses retained: 4

## Preferred methods

### V6466-FINAL-M01 — Bind x1 content seals to exact Git-blob bytes

- Trigger: clean named Windows worktree; x1 content seal; line-ending conversion; exact historical revision
- Method: Verify the x1 seal against bytes read from the exact x1 Git blobs rather than checkout-dependent working-tree bytes.
- Recurrence guard: Content seals declare and test one Git-object hash domain; working-tree byte hashes are not used for cross-worktree replay on platforms with line-ending conversion.
- Rollback: Retain the 23-of-24 named replay and award no replay credit until the exact final commit passes on the same local-only named lane.
- Witnesses: V6466-FINAL-M01-W-F, V6466-FINAL-M01-W-P

### V6466-FINAL-M02 — Resolve diagnostic artifact paths from their consumer

- Trigger: terminal replay diagnosis; repository-relative artifact; multiple evidence directories; read-only lookup
- Method: Read the test's declared seal path before inspection and use the repository-relative reproduction location exactly.
- Recurrence guard: Diagnostic artifact lookups are derived from the consuming test or manifest before invocation; guessed directory placement is not treated as evidence.
- Rollback: Retain the failed lookup and exclude it from evidence; use only the successful exact-path audit.
- Witnesses: V6466-FINAL-M02-W-F, V6466-FINAL-M02-W-P

### V6466-FINAL-M03 — Keep mixed-quote diagnostics structured and fail-visible

- Trigger: PowerShell shell; mixed quote search pattern; multiple diagnostic commands; native exit code
- Method: Use PowerShell Select-String with an explicit pattern array for mixed quote and space searches, and evaluate each diagnostic command independently.
- Recurrence guard: Mixed-quote diagnostics use structured pattern arrays; multi-command diagnostics check every native exit code so later success cannot mask an earlier failure.
- Rollback: Retain the failed search and exclude it from inspection evidence; rely only on the explicit successful inspection.
- Witnesses: V6466-FINAL-M03-W-F, V6466-FINAL-M03-W-P

### V6466-FINAL-M04 — Patch repeated builder keys with schema-local context

- Trigger: generated JSON builder; repeated key name; historical stage count; terminal correction
- Method: Patch repeated JSON-builder keys only with schema-local context, then inspect each affected block before regeneration.
- Recurrence guard: Repeated builder keys require a nearby schema identifier or receipt filename in patch context, followed by independent block-level verification before execution.
- Rollback: Do not execute the builder from the mispatched state; restore phase truth and apply the historical count only inside the closeout receipt block.
- Witnesses: V6466-FINAL-M04-W-F, V6466-FINAL-M04-W-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
