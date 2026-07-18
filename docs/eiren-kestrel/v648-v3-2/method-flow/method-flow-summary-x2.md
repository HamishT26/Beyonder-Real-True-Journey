# GHC Family Method Flow State

- Phase: v648-gmut-thos-v3-x1-x2-r2
- Owner: Eiren Kestrel
- Methods: 12
- Passing witnesses: 13
- Failed witnesses retained: 13

## Preferred methods

### V6483R2-M01 — Independent receipts for expected no-match probes

- Trigger: A preflight combines instruction discovery with unrelated drive or Git probes.
- Method: Run each probe independently and normalize only the documented expected no-match exit.
- Recurrence guard: Do not aggregate unrelated read-only probes under fail-fast Promise.all when one command uses exit 1 for no matches.
- Rollback: Give the aggregate wrapper zero evidence credit and rerun only the required probes independently.
- Witnesses: V6483R2-M01-WFAIL, V6483R2-M01-WPASS

### V6483R2-M02 — Materialize PowerShell foreach output before pipelines

- Trigger: A PowerShell command needs to serialize objects produced by foreach.
- Method: Assign foreach output to an array, then pipe the array to the consumer.
- Recurrence guard: Use $rows=@(foreach(...){...}); $rows | ConvertTo-Json and never direct foreach-to-pipeline composition.
- Rollback: Retain the parser failure and replace only the orchestration form, not the underlying inspection.
- Witnesses: V6483R2-M02-WFAIL, V6483R2-M02-WPASS, V6483R2-M02-WFAIL-X2-01, V6483R2-M02-WPASS-X2-01

### V6483R2-M03 — Conservative proposal-title collision replacement

- Trigger: A new core proposal is compared with the complete inherited frozen-title corpus.
- Method: Replace the proposal with a substantively different surface and rerun the unchanged threshold.
- Recurrence guard: Never lower the novelty threshold to admit a collision; change the research surface instead.
- Rollback: Retain the rejected proposal and restore the last collision-free x1 candidate.
- Witnesses: V6483R2-M03-WFAIL, V6483R2-M03-WPASS

### V6483R2-M04 — Explicit numeric-key selection for tied diagnostics

- Trigger: A diagnostic ranks tuples containing a score and a structured payload.
- Method: Select the maximum with an explicit numeric-score key and report the payload separately.
- Recurrence guard: Never rely on tuple fallback ordering when later tuple fields are mappings or heterogeneous objects.
- Rollback: Give the failed diagnostic zero evidence credit and rerun the same data with numeric-key ordering.
- Witnesses: V6483R2-M04-WFAIL, V6483R2-M04-WPASS

### V6483R2-M05 — Pre-launch UTF-8 for Unicode diagnostics

- Trigger: A Windows child process may print te reo Maori or other non-ASCII source text.
- Method: Set PYTHONUTF8=1 before process launch and rerun unchanged content.
- Recurrence guard: Pin UTF-8 before launching Unicode-emitting diagnostics; never transliterate valid source text to satisfy a console locale.
- Rollback: Retain the encoding failure and rerun the unchanged diagnostic only under explicit UTF-8.
- Witnesses: V6483R2-M05-WFAIL, V6483R2-M05-WPASS

### V6483R2-M06 — Windows-local New Zealand timestamp fallback

- Trigger: A phase timestamp needs New Zealand local time on a host already configured to that timezone.
- Method: Use datetime.astimezone with the configured Windows timezone and verify its UTC offset is plus twelve or plus thirteen hours.
- Recurrence guard: Do not install tzdata merely for a phase timestamp; fail closed if the configured local offset is not a valid New Zealand offset.
- Rollback: Retain the missing-zone failure and omit local-time credit if the configured offset check fails.
- Witnesses: V6483R2-M06-WFAIL, V6483R2-M06-WPASS

### V6483R2-M07 — Exact frozen route-enum validation

- Trigger: A phase contract serializes a route or lifecycle enum that later validators must inspect.
- Method: Read and validate the exact frozen enum rather than substituting a reviewer-local synonym.
- Recurrence guard: Treat serialized lifecycle enums as contracts and centralize or import them when practical.
- Rollback: Retain the failed review and keep the freeze blocked until validator and frozen contract agree exactly.
- Witnesses: V6483R2-M07-WFAIL, V6483R2-M07-WPASS

### V6483R2-M08 — Dynamic retained-negative arithmetic

- Trigger: A phase derives an effective total from inherited, operational, and synthetic negative counts.
- Method: Compute the total from its authoritative component counts and validate the same equation.
- Recurrence guard: Never hand-update a derived negative total; retain components and calculate the projection at generation time.
- Rollback: Retain the stale receipt and block the freeze until the recomputed total and component counts agree.
- Witnesses: V6483R2-M08-WFAIL, V6483R2-M08-WPASS

### V6483R2-M09 — Exact scanner-definition privacy disposition

- Trigger: A staged source file contains the exact privacy regular expressions it executes.
- Method: Classify only exact reviewed scanner-definition paths separately while retaining payload-hit treatment everywhere else.
- Recurrence guard: Keep a narrow exact scanner-definition set; never exempt a directory, wildcard, generated artifact, or unrelated script.
- Rollback: Retain the failed scan and keep the commit blocked if any candidate occurs outside an exact scanner-definition path.
- Witnesses: V6483R2-M09-WFAIL, V6483R2-M09-WPASS

### V6483R2-M10 — Declared-symbol introspection before portfolio access

- Trigger: A phase helper consumes a definitions module derived from but not identical to an older phase schema.
- Method: Inspect the module's declared uppercase symbols before constructing a portfolio introspection query.
- Recurrence guard: Discover or import the declared API before reuse; do not infer constant names from an earlier phase template.
- Rollback: Retain the AttributeError and give the failed query zero evidence credit.
- Witnesses: V6483R2-M10-WFAIL, V6483R2-M10-WPASS

### V6483R2-M11 — Independent receipts for slow Git worktree probes

- Trigger: A large Windows worktree requires status and untracked-file inventory before staging.
- Method: Run Git status and untracked-file discovery as independent processes with separate timeouts and receipts.
- Recurrence guard: Do not combine potentially slow Git worktree scans under one short process budget.
- Rollback: Give the timed wrapper zero evidence credit and rerun only the required probes independently.
- Witnesses: V6483R2-M11-WFAIL, V6483R2-M11-WPASS

### V6483R2-M12 — Single-newline source-file termination

- Trigger: git diff --cached --check reports a blank line at end of a newly added source file.
- Method: Remove only the extra terminal blank line and preserve one terminating newline.
- Recurrence guard: Require exactly one terminating newline and no terminal blank line in new source files.
- Rollback: Retain the hygiene failure and block the evidence commit until the exact staged check passes.
- Witnesses: V6483R2-M12-WFAIL, V6483R2-M12-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
