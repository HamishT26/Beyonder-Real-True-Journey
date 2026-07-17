# GHC Family Method Flow State

- Phase: v647-gmut-thos-v7-x1-x2
- Owner: Sable Rook
- Methods: 9
- Passing witnesses: 10
- Failed witnesses retained: 10

## Preferred methods

### V6477-M01 — No-profile bounded full skill read after short-wrapper timeout

- Trigger: A required local instruction file remains unread after a bounded short-wrapper timeout.
- Method: Retain the timeout, disable profile startup for the read, extend the wrapper to sixty seconds, and read the unchanged file through EOF.
- Recurrence guard: Do not repeat the same short wrapper; use the observed no-profile startup envelope for required full reads.
- Rollback: Stop the read, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6477-M01-WFAIL, V6477-M01-WPASS

### V6477-M02 — Exact inherited portfolio-title collision quarantine

- Trigger: New owner portfolio labels are compared with inherited phase portfolio ledgers before materialization.
- Method: Stop before packet materialization, preserve the exact collision list, rewrite only the Sable labels while retaining their gates, and rerun the unchanged audit.
- Recurrence guard: Require zero inherited and zero within-current exact title collisions before generating any proposal packet.
- Rollback: Leave the source and generated Method Flow evidence intact; do not materialize the proposal packet until the audit passes.
- Witnesses: V6477-M02-WFAIL, V6477-M02-WPASS

### V6477-M03 — Exact-path ripgrep recovery for Windows wildcard faults

- Trigger: A Windows stale-label or content search spans generated filenames selected by a wildcard.
- Method: Use rg --files to enumerate matching files and pass exact paths to the content search.
- Recurrence guard: Never pass an unexpanded Windows wildcard as an rg path argument; enumerate then search exact paths.
- Rollback: Retain partial read-only output and rerun only the failed search surface; mutate no repository state.
- Witnesses: V6477-M03-WFAIL, V6477-M03-WPASS

### V6477-M05 — Atomic patch context recovery with smaller verified edits

- Trigger: A multi-file patch includes long generated prose or several unrelated context anchors.
- Method: Inspect exact current context, split the failed multi-file patch into smaller patches, and apply each only against verified lines.
- Recurrence guard: Read exact context immediately before a multi-file patch and split unrelated edits when any long prose anchor is involved.
- Rollback: Rely on apply_patch atomic rejection, verify no partial diff, and leave the last clean logical state unchanged.
- Witnesses: V6477-M05-WFAIL, V6477-M05-WPASS

### V6477-M04 — Exact inherited phase-local commit-cap test quarantine

- Trigger: A successor phase validates inherited closeout behavior at a head beyond the inherited phase's own commit cap.
- Method: Exclude only the exact inherited test method whose commit-cap assertion is scoped to its original phase, while running every other inherited closeout test.
- Recurrence guard: List every inherited exclusion by fully qualified test identifier and preserve all other inherited assertions.
- Rollback: Restore the broad failed selection receipt if the exact filtered selection does not pass; do not weaken current-phase tests.
- Witnesses: V6477-M04-WFAIL, V6477-M04-WPASS

### V6477-M06 — Immutable x1 assertion and derived-ledger refresh sequencing

- Trigger: A successor x2 phase appends Method Flow evidence after an x1-only historical assertion was frozen.
- Method: Bind x1 historical assertions to the immutable x1 Git blob and regenerate authoritative x2 negative mirrors before rerunning the aggregate selection.
- Recurrence guard: Read historical counts from exact Git blobs and refresh authoritative and derived mirrors before any aggregate rerun.
- Rollback: Retain the failed selection receipt, restore no history, and rerun only after current ledgers and historical assertions agree in their declared domains.
- Witnesses: V6477-M06-WFAIL, V6477-M06-WPASS

### V6477-M07 — Isolated no-profile closeout probes after parallel-wrapper timeout

- Trigger: A bounded Windows closeout preflight combines startup-sensitive read-only probes under a ten-second member timeout.
- Method: Retain the timeout, isolate each probe, disable login-profile semantics, and give the observed Windows startup envelope a bounded sixty-second limit.
- Recurrence guard: Do not group startup-sensitive Windows probes behind the shortest member timeout; isolate them and preserve each exit code.
- Rollback: Stop after the timeout, retain the failed wrapper receipt, and verify repository state before any retry.
- Witnesses: V6477-M07-WFAIL, V6477-M07-WPASS

### V6477-M08 — Literal ASCII inspection wrapper after Unicode quote-parser fault

- Trigger: A read-only PowerShell search wrapper mixes quoted regex alternation with Unicode display text.
- Method: Retain the parser fault and split the inspection into literal single-quoted ASCII search patterns and separate exact-path reads.
- Recurrence guard: Keep PowerShell search wrappers ASCII and single-quoted when Unicode byte integrity is being checked separately.
- Rollback: Retain the pre-execution parser error and make no repository change before the corrected read-only probe.
- Witnesses: V6477-M08-WFAIL, V6477-M08-WPASS, V6477-M08-WFAIL2, V6477-M08-WPASS2

### V6477-M09 — Lifecycle-scoped Method Flow parity and negative-total validation

- Trigger: A closeout validator reuses evidence-boundary assertions after append-only lifecycle failures are retained.
- Method: Retain the failed 67-test closeout receipt, bind Method Flow parity and negative totals to the declared evidence or closeout lifecycle boundary, regenerate the final mirrors, and rerun the unchanged closeout selection.
- Recurrence guard: Declare evidence-boundary and closeout-boundary counts separately and select the exact domain from the validator lifecycle flag.
- Rollback: Preserve the failed closeout validation receipt, do not weaken the test selection, and retry only after count domains and ledgers agree.
- Witnesses: V6477-M09-WFAIL, V6477-M09-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
