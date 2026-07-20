# GHC Family Method Flow State

- Phase: v650-gmut-thos-v1-x1-x2
- Owner: Vesper Arlen
- Methods: 22
- Passing witnesses: 22
- Failed witnesses retained: 22

## Preferred methods

### V6501-M01 — Retain and recover startup failure N01

- Trigger: Startup exposes N01.
- Method: Re-read the baton in bounded line ranges and verify complete coverage before granting read credit.
- Recurrence guard: Re-read the baton in bounded line ranges and verify complete coverage before granting read credit.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M01-WFAIL, V6501-M01-WPASS

### V6501-M02 — Retain and recover startup failure N02

- Trigger: Startup exposes N02.
- Method: Normalize expected no-match exits inside the smallest attributable command.
- Recurrence guard: Normalize expected no-match exits inside the smallest attributable command.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M02-WFAIL, V6501-M02-WPASS

### V6501-M03 — Retain and recover startup failure N03

- Trigger: Startup exposes N03.
- Method: Use exact indexed branch, worktree, skill, memory, and current-family-index surfaces.
- Recurrence guard: Use exact indexed branch, worktree, skill, memory, and current-family-index surfaces.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M03-WFAIL, V6501-M03-WPASS

### V6501-M04 — Retain and recover startup failure N04

- Trigger: Startup exposes N04.
- Method: Split collision probes by registry and retain each result independently.
- Recurrence guard: Split collision probes by registry and retain each result independently.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M04-WFAIL, V6501-M04-WPASS

### V6501-M05 — Retain and recover startup failure N05

- Trigger: Startup exposes N05.
- Method: Limit the claim to the live family index and exact registries; do not claim exhaustive historical byte search.
- Recurrence guard: Limit the claim to the live family index and exact registries; do not claim exhaustive historical byte search.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M05-WFAIL, V6501-M05-WPASS

### V6501-M06 — Retain and recover startup failure N06

- Trigger: Startup exposes N06.
- Method: Use enumeration only for path discovery and run exact checks on current committed identity surfaces.
- Recurrence guard: Use enumeration only for path discovery and run exact checks on current committed identity surfaces.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M06-WFAIL, V6501-M06-WPASS

### V6501-M07 — Retain and recover startup failure N07

- Trigger: Startup exposes N07.
- Method: Run current-index and memory-registry checks separately with expected no-match handling.
- Recurrence guard: Run current-index and memory-registry checks separately with expected no-match handling.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M07-WFAIL, V6501-M07-WPASS

### V6501-M08 — Retain and recover startup failure N08

- Trigger: Startup exposes N08.
- Method: Invoke the exact runner path and obtain a bounded help receipt directly.
- Recurrence guard: Invoke the exact runner path and obtain a bounded help receipt directly.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M08-WFAIL, V6501-M08-WPASS

### V6501-M09 — Retain and recover startup failure N09

- Trigger: Startup exposes N09.
- Method: Use the already-read schema plus exact runner help and deterministic request validation.
- Recurrence guard: Use the already-read schema plus exact runner help and deterministic request validation.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M09-WFAIL, V6501-M09-WPASS

### V6501-M10 — Retain and recover startup failure N10

- Trigger: Startup exposes N10.
- Method: Retain the failed audit and rerun the generated eighty-eight-entry candidate in a separate output directory.
- Recurrence guard: Retain the failed audit and rerun the generated eighty-eight-entry candidate in a separate output directory.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M10-WFAIL, V6501-M10-WPASS

### V6501-M11 — Retain and recover startup failure N11

- Trigger: Startup exposes N11.
- Method: Inspect the exact path, branch, head, and upstream before resuming only the missing push step.
- Recurrence guard: Inspect the exact path, branch, head, and upstream before resuming only the missing push step.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M11-WFAIL, V6501-M11-WPASS

### V6501-M12 — Retain and recover startup failure N12

- Trigger: Startup exposes N12.
- Method: Split filesystem, head, status, upstream, tracking, and live-remote probes into attributable checks.
- Recurrence guard: Split filesystem, head, status, upstream, tracking, and live-remote probes into attributable checks.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M12-WFAIL, V6501-M12-WPASS

### V6501-M13 — Retain and recover startup failure N13

- Trigger: Startup exposes N13.
- Method: Separate ASCII-safe hunks and inspect Unicode through UTF-8-aware tooling.
- Recurrence guard: Separate ASCII-safe hunks and inspect Unicode through UTF-8-aware tooling.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M13-WFAIL, V6501-M13-WPASS

### V6501-M14 — Retain and recover startup failure N14

- Trigger: Startup exposes N14.
- Method: Treat the encoding error as retained and inspect or write Unicode through UTF-8 files rather than the console.
- Recurrence guard: Treat the encoding error as retained and inspect or write Unicode through UTF-8 files rather than the console.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M14-WFAIL, V6501-M14-WPASS

### V6501-M15 — Retain and recover startup failure N15

- Trigger: Startup exposes N15.
- Method: Replace the uniquely marked block through a UTF-8 marker-based mechanical remaster.
- Recurrence guard: Replace the uniquely marked block through a UTF-8 marker-based mechanical remaster.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M15-WFAIL, V6501-M15-WPASS

### V6501-M16 — Retain and recover startup failure N16

- Trigger: Startup exposes N16.
- Method: Inspect the file state, retain the ambiguous wrapper failure, and apply one deterministic marker-based correction.
- Recurrence guard: Inspect the file state, retain the ambiguous wrapper failure, and apply one deterministic marker-based correction.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M16-WFAIL, V6501-M16-WPASS

### V6501-M17 — Retain and recover startup failure N17

- Trigger: Startup exposes N17.
- Method: Inspect bounded partial output, grant no aggregate pass credit, then rerun the deterministic builder with a wider wrapper while preserving the timeout.
- Recurrence guard: Inspect bounded partial output, grant no aggregate pass credit, then rerun the deterministic builder with a wider wrapper while preserving the timeout.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M17-WFAIL, V6501-M17-WPASS

### V6501-M18 — Retain and recover startup failure N18

- Trigger: Startup exposes N18.
- Method: Install nothing unrelated; retain the failed invocation and run the same committed suite through the standard-library unittest runner.
- Recurrence guard: Install nothing unrelated; retain the failed invocation and run the same committed suite through the standard-library unittest runner.
- Rollback: Give the failed attempt zero credit and return to the last attributable bounded state.
- Witnesses: V6501-M18-WFAIL, V6501-M18-WPASS

### V6501-M19 — Retain and recover NEG-V6501-X2-001

- Trigger: The v650-v1 x2 workflow exposes this exact bounded failure signature.
- Method: Split ancestry into an attributable command, preserve the parse failure with zero equality credit, and rerun the read-only proof.
- Recurrence guard: Split ancestry into an attributable command, preserve the parse failure with zero equality credit, and rerun the read-only proof.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6501-M19-WFAIL, V6501-M19-WPASS

### V6501-M20 — Retain and recover NEG-V6501-X2-002

- Trigger: The v650-v1 x2 workflow exposes this exact bounded failure signature.
- Method: Retain the syntax failure, change only the transformer's outer delimiters, rerun syntax checks, and grant no artifact credit to the failed remaster.
- Recurrence guard: Retain the syntax failure, change only the transformer's outer delimiters, rerun syntax checks, and grant no artifact credit to the failed remaster.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6501-M20-WFAIL, V6501-M20-WPASS

### V6501-M21 — Retain and recover NEG-V6501-X2-003

- Trigger: The v650-v1 x2 workflow exposes this exact bounded failure signature.
- Method: Retain the failed skill validations, use ASCII Maori wording only inside validator-facing skill packages, preserve macron spelling in UTF-8 phase records, and rerun without global installation.
- Recurrence guard: Retain the failed skill validations, use ASCII Maori wording only inside validator-facing skill packages, preserve macron spelling in UTF-8 phase records, and rerun without global installation.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6501-M21-WFAIL, V6501-M21-WPASS

### V6501-M22 — Retain and recover NEG-V6501-X2-004

- Trigger: The v650-v1 x2 workflow exposes this exact bounded failure signature.
- Method: Retain the undersized document with zero three-page credit, correct only dynamic f-string braces, and regenerate before scoped tests or evidence commit.
- Recurrence guard: Retain the undersized document with zero three-page credit, correct only dynamic f-string braces, and regenerate before scoped tests or evidence commit.
- Rollback: Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.
- Witnesses: V6501-M22-WFAIL, V6501-M22-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
