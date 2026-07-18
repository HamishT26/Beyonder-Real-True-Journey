# GHC Family Method Flow State

- Phase: v648-gmut-thos-v6-x1-x2
- Owner: Orin Thale
- Methods: 12
- Passing witnesses: 11
- Failed witnesses retained: 12

## Preferred methods

### V6486-X2-M01 — Bind assertions to the artifact schema that declares the field

- Trigger: A proposal emits separate contract and mutation evidence artifacts.
- Method: Load cbr/live-performance-remedy-matrix.json for contract-level authority reservations and keep the mutation receipt for mutation counts only.
- Recurrence guard: Bind each test assertion to the artifact schema that declares the asserted field.
- Rollback: Retain the failed module run, award it no aggregate credit, and leave the correct CBR artifacts unchanged.
- Witnesses: V6486-X2-M01-WFAIL, V6486-X2-M01-WPASS

### V6486-X2-M02 — Scope stale-label review around historical evidence

- Trigger: A successor packet embeds frozen proposal history and retained failed witnesses.
- Method: Exclude frozen-chain proposal history and retained failed-witness domains, then scan active v648-v6 schemas, paths, and current origin fields for predecessor drift.
- Recurrence guard: Classify historical and failure-evidence domains before interpreting predecessor tokens as stale.
- Rollback: Retain the false-positive result, award no hygiene credit, and leave inherited history unchanged.
- Witnesses: V6486-X2-M02-WFAIL, V6486-X2-M02-WPASS

### V6486-X2-M03 — Avoid raw multiline code inside orchestration strings

- Trigger: A read-only recovery check requires multiline embedded source.
- Method: Use native PowerShell file selection with explicit historical-domain exclusions and exact Select-String patterns.
- Recurrence guard: Do not place raw multiline source inside a quoted orchestration string; use a checked script or native pipeline.
- Rollback: Retain the orchestration failure, award no scan credit, and rerun only with a parse-safe method.
- Witnesses: V6486-X2-M03-WFAIL, V6486-X2-M03-WPASS

### V6486-X2-M07 — Validate Method Flow records before dependent witnesses

- Trigger: A new record and witness are about to be appended.
- Method: Add validation_witness_ids, record each method successfully, then append its witness.
- Recurrence guard: Validate required Method Flow fields and gate witness calls on record success.
- Rollback: Retain all rejected calls and retry only with schema-complete records.
- Witnesses: V6486-X2-M07-WFAIL, V6486-X2-M07-WPASS

### V6486-X2-M04 — Separate patch syntax from JSON content

- Trigger: A generated patch adds JSON objects.
- Method: Remove only literal patch-marker characters, preserve every negative object, and parse the exact file.
- Recurrence guard: Inspect generated patch prefixes separately from intended JSON content.
- Rollback: Retain the invalid parse, award no JSON credit, and remove only the literal markers.
- Witnesses: V6486-X2-M04-WFAIL, V6486-X2-M04-WPASS

### V6486-X2-M05 — Propagate every native validation exit immediately

- Trigger: Multiple native validation commands share one PowerShell wrapper.
- Method: Check LASTEXITCODE immediately after every native parser or validator.
- Recurrence guard: Never rely on the last command's exit code for a multi-command native validation wrapper.
- Rollback: Retain the misleading wrapper result and rerun with immediate exit propagation.
- Witnesses: V6486-X2-M05-WFAIL, V6486-X2-M05-WPASS

### V6486-X2-M06 — Use literal patches for recovery

- Trigger: A recovery patch itself requires complex code generation.
- Method: Split the repair into small literal apply_patch calls.
- Recurrence guard: Prefer small literal patches over nested generated-code construction during recovery.
- Rollback: Retain the pre-execution fault and apply no repository credit to it.
- Witnesses: V6486-X2-M06-WFAIL, V6486-X2-M06-WPASS

### V6486-X2-M09 — Use a checked script for JSON sweeps

- Trigger: Nontrivial Python must run under Windows PowerShell native argument binding.
- Method: Move the JSON sweep into a checked phase-local Python runner and invoke it by filename.
- Recurrence guard: Use a script file for nontrivial Python under Windows PowerShell.
- Rollback: Retain the native-binding failure and avoid further inline retries.
- Witnesses: V6486-X2-M09-WFAIL, V6486-X2-M09-WPASS

### V6486-X2-M10 — Preserve unpromoted failed methods

- Trigger: A failed workaround has no passing witness but a different method recovers the task.
- Method: Leave the failed method candidate and use the passing replacement as preferred.
- Recurrence guard: Consult the transition graph and never force lifecycle state for parity.
- Rollback: Retain the rejected transition and leave the original method candidate.
- Witnesses: V6486-X2-M10-WFAIL, V6486-X2-M10-WPASS

### V6486-X2-M11 — Validate append-only ledgers by internal parity

- Trigger: A ledger may gain retained entries during the phase.
- Method: Assert internal count and list parity instead of a fixed operational total.
- Recurrence guard: Use invariant parity checks for append-only ledgers.
- Rollback: Retain the failed runner invocation and do not lower the negative count.
- Witnesses: V6486-X2-M11-WFAIL, V6486-X2-M11-WPASS

### V6486-X2-M12 — Separate Windows search roots from glob filters

- Trigger: A native search requires wildcard filename selection on Windows.
- Method: Pass a literal directory root to ripgrep and put wildcard matching in a -g filter.
- Recurrence guard: Use literal search roots and -g filename filters for all Windows ripgrep calls.
- Rollback: Retain both failed invocations and discard their partial output as a passing witness.
- Witnesses: V6486-X2-M12-WFAIL, V6486-X2-M12-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
