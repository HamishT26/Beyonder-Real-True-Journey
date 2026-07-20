# GHC Family Method Flow State

- Phase: v649-gmut-thos-v8-x1-x2
- Owner: Elaren Kestrel
- Methods: 9
- Passing witnesses: 9
- Failed witnesses retained: 9

## Preferred methods

### V6498-M01 — Retain and recover startup failure N01

- Trigger: Startup exposes N01.
- Method: Normalize each no-match exit locally and emit independent root receipts before aggregation.
- Recurrence guard: Normalize each no-match exit locally and emit independent root receipts before aggregation.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M01-WFAIL, V6498-M01-WPASS

### V6498-M02 — Retain and recover startup failure N02

- Trigger: Startup exposes N02.
- Method: Inspect top-level keys first, then concatenate only the declared proposal arrays.
- Recurrence guard: Inspect top-level keys first, then concatenate only the declared proposal arrays.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M02-WFAIL, V6498-M02-WPASS

### V6498-M03 — Retain and recover startup failure N03

- Trigger: Startup exposes N03.
- Method: Materialize foreach output in an array before piping the array to JSON serialization.
- Recurrence guard: Materialize foreach output in an array before piping the array to JSON serialization.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M03-WFAIL, V6498-M03-WPASS

### V6498-M04 — Retain and recover startup failure N04

- Trigger: Startup exposes N04.
- Method: Bind the wrapper to the runner's exact workflow-plan-validation contract before granting workflow credit.
- Recurrence guard: Bind the wrapper to the runner's exact workflow-plan-validation contract before granting workflow credit.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M04-WFAIL, V6498-M04-WPASS

### V6498-M05 — Retain and recover startup failure N05

- Trigger: Startup exposes N05.
- Method: Use an exact discovered LiteralPath for each required workflow receipt.
- Recurrence guard: Use an exact discovered LiteralPath for each required workflow receipt.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M05-WFAIL, V6498-M05-WPASS

### V6498-M06 — Retain and recover startup failure N06

- Trigger: Startup exposes N06.
- Method: Quarantine the scanner implementation and its definition receipt while continuing to scan every other staged text blob.
- Recurrence guard: Quarantine the scanner implementation and its definition receipt while continuing to scan every other staged text blob.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M06-WFAIL, V6498-M06-WPASS

### V6498-M07 — Retain and recover startup failure N07

- Trigger: Startup exposes N07.
- Method: Bind every shell interpolation value explicitly before constructing the commit and equality command.
- Recurrence guard: Bind every shell interpolation value explicitly before constructing the commit and equality command.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M07-WFAIL, V6498-M07-WPASS

### V6498-M08 — Retain and recover startup failure N08

- Trigger: Startup exposes N08.
- Method: Run each exact file and Git-state probe in its own bounded process with an independently attributable receipt.
- Recurrence guard: Run each exact file and Git-state probe in its own bounded process with an independently attributable receipt.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M08-WFAIL, V6498-M08-WPASS

### V6498-M09 — Retain and recover startup failure N09

- Trigger: Startup exposes N09.
- Method: Inspect the exact target lines before composing each patch hunk and preserve atomic rejection as zero mutation.
- Recurrence guard: Inspect the exact target lines before composing each patch hunk and preserve atomic rejection as zero mutation.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6498-M09-WFAIL, V6498-M09-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
