# GHC Family Method Flow State

- Phase: v648-gmut-thos-v6-x1-x2
- Owner: Orin Thale
- Methods: 21
- Passing witnesses: 20
- Failed witnesses retained: 21

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

### V6486-X2-M13 — Parse Git divergence into numeric fields

- Trigger: PowerShell consumes tab-separated Git divergence output.
- Method: Parse the two divergence counts and compare them as numeric fields.
- Recurrence guard: Parse native structured fields instead of comparing single-quoted control-character escapes.
- Rollback: Retain the false-negative wrapper result while awarding no failed equality claim.
- Witnesses: V6486-X2-M13-WFAIL, V6486-X2-M13-WPASS

### V6486-X2-M14 — Reconcile aggregates from append-only negative ledgers

- Trigger: An aggregate receipt and its source operational ledger disagree.
- Method: Derive aggregate negative totals from the validated append-only operational ledger and retain any immutable earlier discrepancy explicitly.
- Recurrence guard: Compute aggregate counts from validated source ledgers and require arithmetic parity before seal.
- Rollback: Do not rewrite the immutable evidence commit; quarantine its stale aggregate and withhold final count credit until reconciled.
- Witnesses: V6486-X2-M14-WFAIL, V6486-X2-M14-WPASS

### V6486-X2-M15 — Measure decision-relevant successor batons before seal

- Trigger: A generated activation baton has a declared 4,000-to-6,000-word contract.
- Method: Add decision-relevant successor instructions and measure the generated baton before closeout writes.
- Recurrence guard: Measure baton length before writes and require every added section to carry a decision, gate, or falsifier.
- Rollback: Retain the failed build, leave routing unsent, and do not weaken the declared word contract.
- Witnesses: V6486-X2-M15-WFAIL, V6486-X2-M15-WPASS

### V6486-X2-M16 — Bind historical manifests to immutable Git objects

- Trigger: Later lifecycle work legitimately edits paths that were present in an earlier manifest.
- Method: Resolve manifest entries from their immutable commit object rather than hashing later working-tree files.
- Recurrence guard: Bind every historical manifest assertion to its declared immutable Git commit.
- Rollback: Retain the failed development run and award no manifest credit until commit-local comparison passes.
- Witnesses: V6486-X2-M16-WFAIL, V6486-X2-M16-WPASS

### V6486-X2-M17 — Bind in-process tests to the repository root

- Trigger: A phase-local validator imports repository test modules from a script subdirectory.
- Method: Insert the exact repository root at the front of sys.path before in-process unittest discovery.
- Recurrence guard: Bind in-process discovery to the repository root and reject placeholder suites before execution.
- Rollback: Retain the zero-test failed attempt, leave the successful-pass counter at zero, and do not claim a canonical pass.
- Witnesses: V6486-X2-M17-WFAIL, V6486-X2-M17-WPASS

### V6486-X2-M18 — Bind historical X1 suites to immutable commits

- Trigger: A successor canonical selection includes X1 assertions from an earlier lifecycle boundary.
- Method: Read X1 JSON, blobs, and changed paths from each phase's exact immutable X1 commit.
- Recurrence guard: Declare an exact commit for every historical assertion and resolve its paths and blobs there.
- Rollback: Retain the three failures and do not exclude, rewrite, or award canonical credit to the failed run.
- Witnesses: V6486-X2-M18-WFAIL, V6486-X2-M18-WPASS

### V6486-X2-M19 — Keep inherited immutability checks commit-local

- Trigger: A successor legitimately updates a test file that was itself part of an inherited X1 manifest.
- Method: Verify inherited X1 manifest entries and self-exclusions entirely at the exact historical X1 commit.
- Recurrence guard: Verify historical manifests in their commit domain and review successor edits in the successor manifest.
- Rollback: Retain the 66-of-67 failed run and do not revert the evidence-justified successor compatibility fix.
- Witnesses: V6486-X2-M19-WFAIL, V6486-X2-M19-WPASS

### V6486-X2-M20 — Keep inherited evidence manifests commit-local

- Trigger: A successor edits a file that was included in an inherited evidence manifest.
- Method: Resolve inherited evidence receipts and manifest entries from the exact historical evidence commit.
- Recurrence guard: Resolve every historical evidence receipt and blob at the declared evidence commit.
- Rollback: Retain the 10-of-11 failure and do not revert evidence-justified successor test changes.
- Witnesses: V6486-X2-M20-WFAIL, V6486-X2-M20-WPASS

### V6486-X2-M21 — Quarantine privacy scanner definitions from payload hits

- Trigger: Changed validation scripts contain the privacy patterns they implement.
- Method: Quarantine exact privacy-scanner definition files as candidates while rejecting matches in all payload files.
- Recurrence guard: Separate exact scanner-definition surfaces from payload surfaces and report both counts.
- Rollback: Retain the failed sealer, make no privacy pass claim, and do not rerun tests or the canonical scan.
- Witnesses: V6486-X2-M21-WFAIL, V6486-X2-M21-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
