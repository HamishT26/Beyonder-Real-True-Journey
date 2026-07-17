# GHC Family Method Flow State

- Phase: v647-gmut-thos-v6-x1-x2
- Owner: Ilyra Fen
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### V6476-M01 — Bounded full skill read after short-wrapper timeout

- Trigger: A required local instruction file has not yet been read to EOF and the short wrapper timed out.
- Method: Inventory the exact file with a bounded fast probe, then read the unchanged file in full with a 60-second wrapper.
- Recurrence guard: Do not repeat the same short wrapper; preserve every timeout and verify EOF content before task action.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M01-WFAIL, V6476-M01-WPASS

### V6476-M02 — Explicit remote-ref revision-range equality

- Trigger: A Git equality range uses an upstream expression inside PowerShell command text.
- Method: Resolve or name the full remote-tracking ref explicitly and pass that ref to Git revision-range commands.
- Recurrence guard: Never embed an unquoted upstream hashtable-like expression in a PowerShell revision range.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M02-WFAIL, V6476-M02-WPASS

### V6476-M03 — Built-in JSON parser fallback without installation

- Trigger: JSON inspection is required and the optional utility is not already installed.
- Method: Use the platform built-in JSON parser under explicit UTF-8 and deterministic output; do not install unrelated software.
- Recurrence guard: Probe utility availability once, then select the built-in parser and retain the missing-tool event.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M03-WFAIL, V6476-M03-WPASS

### V6476-M04 — Exact portfolio collision quarantine before materialization

- Trigger: Current safe-task skill runner cleanup exact or blocked titles are audited against inherited portfolios.
- Method: Stop before materialization, rename or rewrite exact collisions, and rerun the unchanged normalized-title audit.
- Recurrence guard: Require zero inherited and zero within-current exact collisions before generating phase artifacts.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M04-WFAIL, V6476-M04-WPASS

### V6476-M05 — Non-self-matching forbidden-credit scanner definition

- Trigger: The scanner source is included in the staged surface it reviews.
- Method: Construct the same forbidden sequence from adjacent byte fragments while leaving target matching unchanged.
- Recurrence guard: Forward-test every literal scanner needle against its own source before staged review credit.
- Rollback: Stop the bounded probe, retain the failure, and return to the last clean repository state without external mutation.
- Witnesses: V6476-M05-WFAIL, V6476-M05-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
