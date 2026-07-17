# GHC Family Method Flow State

- Phase: v648-gmut-thos-v1-x1-x2
- Owner: Tamar Vey
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### V6481-M01 — Increase only the bound on an exact read after a content-free timeout

- Trigger: A required read-only memory or instruction file is exact and known but the initial bound expires.
- Method: Retry the same exact read once with a longer bounded timeout and no broader scan.
- Recurrence guard: Keep memory discovery narrow and do not convert a timeout into absence.
- Rollback: Discard the timeout result; it changed no repository or external state.
- Witnesses: V6481-M01-WFAIL, V6481-M01-WPASS

### V6481-M02 — Materialize PowerShell loop results before piping them

- Trigger: A PowerShell wrapper aggregates multiple manifest checks into JSON.
- Method: Assign loop results to an explicit array and pipe the completed array to ConvertTo-Json.
- Recurrence guard: Do not attach a native or cmdlet pipeline directly to a statement block without grouping or assignment.
- Rollback: Discard the pre-execution parser failure; no child command or mutation ran.
- Witnesses: V6481-M02-WFAIL, V6481-M02-WPASS

### V6481-M03 — Force UTF-8 for Unicode-bearing Python audit output

- Trigger: A read-only audit prints proposal titles or authority terms containing non-ASCII characters.
- Method: Set Python output encoding to UTF-8 or emit ASCII-safe structured counts while preserving source text.
- Recurrence guard: Use explicit UTF-8 for every phase script and console witness that may carry Māori text.
- Rollback: Discard the failed display; it made no file or ref change.
- Witnesses: V6481-M03-WFAIL, V6481-M03-WPASS

### V6481-M04 — Enumerate exact source-phase receipt paths before reading optional evidence

- Trigger: A successor wants an optional source-phase environment receipt whose filename may vary.
- Method: Enumerate the bounded source-phase environment directory, select the actual public receipt, then verify current local state independently.
- Recurrence guard: Do not infer optional receipt names from an older phase pattern.
- Rollback: Discard the failed read-only path request; it changed no file or ref.
- Witnesses: V6481-M04-WFAIL, V6481-M04-WPASS

### V6481-M05 — Set UTF-8 on Method Flow summary command output

- Trigger: A Method Flow ledger contains Māori text and the runner prints its JSON payload to a Windows console.
- Method: Set PYTHONIOENCODING to UTF-8 for the same summarize command, retain the failed attempt, and credit only the successful replay.
- Recurrence guard: Apply explicit UTF-8 to every family runner that may print Unicode-bearing phase evidence.
- Rollback: Do not credit the partial invocation; overwrite only the same owner-scoped derived summary outputs on successful replay.
- Witnesses: V6481-M05-WFAIL, V6481-M05-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
