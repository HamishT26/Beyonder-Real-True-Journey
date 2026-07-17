# GHC Family Method Flow State

- Phase: v648-gmut-thos-v1-x1-x2
- Owner: Tamar Vey
- Methods: 11
- Passing witnesses: 15
- Failed witnesses retained: 15

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
- Witnesses: V6481-M02-WFAIL, V6481-M02-WPASS, V6481-M02-WFAIL-LC10, V6481-M02-WPASS-LC10

### V6481-M03 — Force UTF-8 for Unicode-bearing Python audit output

- Trigger: A read-only audit prints proposal titles or authority terms containing non-ASCII characters.
- Method: Set Python output encoding to UTF-8 or emit ASCII-safe structured counts while preserving source text.
- Recurrence guard: Use explicit UTF-8 for every phase script and console witness that may carry Māori text.
- Rollback: Discard the failed display; it made no file or ref change.
- Witnesses: V6481-M03-WFAIL, V6481-M03-WPASS, V6481-M03-WFAIL-LC05, V6481-M03-WPASS-LC05

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

### V6481-M06 — Expose the exact repository root before dotted unittest loading

- Trigger: A validator is executed from the scripts directory and loads repository tests by dotted module name.
- Method: Insert the exact repository root into sys.path before loading the frozen unittest names, without changing the selection or exclusions.
- Recurrence guard: When a validator loads dotted unittest names while invoked from scripts, expose only the exact repository root before constructing the suite.
- Rollback: Retain the failed receipt, award zero substantive-test credit, and make no change to the frozen test selection or exclusion set.
- Witnesses: V6481-M06-WFAIL, V6481-M06-WPASS

### V6481-M07 — Use literal prefix checks for Git porcelain status codes

- Trigger: A PowerShell diagnostic classifies Git porcelain lines by their two-character status prefix.
- Method: Use the string StartsWith method for the literal two-character untracked prefix in Git porcelain output.
- Recurrence guard: Use StartsWith for literal Git porcelain prefixes; do not use wildcard operators for punctuation-bearing status codes.
- Rollback: Discard the false read-only count and leave the staged surface unchanged.
- Witnesses: V6481-M07-WFAIL, V6481-M07-WPASS

### V6481-M08 — Recover bounded repository reads by changing invocation mode and probe granularity

- Trigger: A required read-only repository or process probe times out before returning usable evidence.
- Method: Use a non-login shell and split repository probes into exact bounded Git primitives before retrying ordinary status.
- Recurrence guard: Treat a timeout as missing evidence, retain each failed witness, and change only invocation mode or probe granularity before retry.
- Rollback: Discard every timed-out result; none supplies clean-state, exact-head, or process-state credit and none changed repository or external state.
- Witnesses: V6481-M08-WFAIL, V6481-M08-WPASS, V6481-M08-WFAIL-LC06, V6481-M08-WPASS-LC06

### V6481-M09 — Validate Method Flow parity without erasing recurrence witnesses

- Trigger: A Method Flow ledger has balanced recurrence witnesses and a test assumes exactly one fail/pass pair per method.
- Method: Require failed and passing witness parity while allowing multiple retained recurrence pairs per method.
- Recurrence guard: Test fail/pass parity and at least one failed witness per method; do not assume exactly one pair when recurrences are retained.
- Rollback: Retain the failed 75-test receipt and change only the invalid witness-cardinality assertion.
- Witnesses: V6481-M09-WFAIL, V6481-M09-WPASS

### V6481-M10 — Batch exact staged Git-blob reads without changing the hash domain

- Trigger: An exact staged reviewer hashes many stage-zero paths and per-path Git process startup exceeds the bounded runtime.
- Method: Read the stage-zero index once and use one communicate-based cat-file batch for all unique blobs.
- Recurrence guard: Batch immutable blob reads through communicate; never use a write-all-then-read pipe wrapper and never substitute working-tree bytes.
- Rollback: Discard the timed-out run and any incomplete outputs; leave the staged index unchanged.
- Witnesses: V6481-M10-WFAIL, V6481-M10-WPASS, V6481-M10-WFAIL-LC11, V6481-M10-WPASS-LC11

### V6481-M11 — Retain failed validator evidence without publishing private traceback paths

- Trigger: A repository-bound failed validation receipt contains an otherwise useful traceback with a private absolute local path.
- Method: Preserve the failed test and assertion while replacing only the private absolute traceback prefix with a repository-neutral owner-worktree marker.
- Recurrence guard: Sanitize traceback location prefixes before repository retention without deleting the test name, assertion, counts, or failure state.
- Rollback: Keep the staged review invalid until the same exact privacy scan passes; do not delete the failed receipt.
- Witnesses: V6481-M11-WFAIL, V6481-M11-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
