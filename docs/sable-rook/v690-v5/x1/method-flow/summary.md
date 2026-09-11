# GHC Family Method Flow State

- Phase: v690-v5-x1
- Owner: Sable Rook
- Methods: 3
- Passing witnesses: 7
- Failed witnesses retained: 7

## Preferred methods

### SR6905-X1-M001 — Structural runner-envelope comparison

- Trigger: runner emits parsed JSON value; frozen expected envelope may use another key insertion order
- Method: Compare the parsed runner envelope and frozen expected envelope structurally rather than comparing insertion-order JSON strings.
- Recurrence guard: Use structural deep equality for JSON values and reserve byte equality for explicitly named canonical byte domains.
- Rollback: Retain all five failed runner outputs and stop x1 completion until each exact runner smoke passes structurally.
- Witnesses: SR6905-X1-W001-A-F, SR6905-X1-W001-B-F, SR6905-X1-W001-C-F, SR6905-X1-W001-D-F, SR6905-X1-W001-E-F, SR6905-X1-W001-A-P, SR6905-X1-W001-B-P, SR6905-X1-W001-C-P, SR6905-X1-W001-D-P, SR6905-X1-W001-E-P

### SR6905-X1-M002 — Attributable scalar staged validation

- Trigger: exact x1 staged index; combined validation wrapper lacks a terminal summary
- Method: Run manifest replay, syntax, JSON, privacy, diff, and lifecycle checks as separate attributable scalar probes.
- Recurrence guard: Split staged validation into bounded probes whenever one wrapper combines filesystem enumeration, compilers, Git blobs, and privacy scanning.
- Rollback: Audit persisted index and process state before rerunning only checks without attributable output.
- Witnesses: SR6905-X1-W002-F, SR6905-X1-W002-P

### SR6905-X1-M003 — Text-entrypoint syntax compiler

- Trigger: Node JavaScript stored in .txt under v5 policy; syntax-only validation required
- Method: Compile authorized JavaScript-in-text entrypoints with Node vm.Script instead of node --check, which rejects the .txt extension.
- Recurrence guard: Use the text-source syntax runner for .txt JavaScript and reserve node --check for recognized JavaScript extensions.
- Rollback: Retain the rejected check-mode invocation and do not rename or duplicate source files merely to satisfy the checker.
- Witnesses: SR6905-X1-W003-F, SR6905-X1-W003-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
