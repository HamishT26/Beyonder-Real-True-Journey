# GHC Family Method Flow State

- Phase: v647-gmut-thos-v8-x1-x2
- Owner: Orin Thale
- Methods: 8
- Passing witnesses: 8
- Failed witnesses retained: 8

## Preferred methods

### V6478-M01 — Retained x1 failure recovery V6478-X1-N01

- Trigger: The declared bounded owner-local x1 workflow failure has occurred and remains retained.
- Method: Use rg globs or exact paths and rerun the read-only search.
- Recurrence guard: Use rg globs or exact paths and rerun the read-only search.
- Rollback: Stop, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6478-M01-WFAIL, V6478-M01-WPASS

### V6478-M02 — Retained x1 failure recovery V6478-X1-N02

- Trigger: The declared bounded owner-local x1 workflow failure has occurred and remains retained.
- Method: Classify lifecycle paths as repository-relative and final-owner paths as owner-relative, then replay.
- Recurrence guard: Classify lifecycle paths as repository-relative and final-owner paths as owner-relative, then replay.
- Rollback: Stop, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6478-M02-WFAIL, V6478-M02-WPASS

### V6478-M03 — Retained x1 failure recovery V6478-X1-N03

- Trigger: The declared bounded owner-local x1 workflow failure has occurred and remains retained.
- Method: Split status, exact selection, and inventory into no-profile bounded probes.
- Recurrence guard: Split status, exact selection, and inventory into no-profile bounded probes.
- Rollback: Stop, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6478-M03-WFAIL, V6478-M03-WPASS

### V6478-M04 — Retained x1 failure recovery V6478-X1-N04

- Trigger: The declared bounded owner-local x1 workflow failure has occurred and remains retained.
- Method: Initialize with apply_patch and materialize explicit structured definitions without separator inference.
- Recurrence guard: Initialize with apply_patch and materialize explicit structured definitions without separator inference.
- Rollback: Stop, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6478-M04-WFAIL, V6478-M04-WPASS

### V6478-M05 — Retained x1 failure recovery V6478-X1-N05

- Trigger: The declared bounded owner-local x1 workflow failure has occurred and remains retained.
- Method: Rename the parameter to a nonreserved short identifier and rerun the same owner-scoped apply_patch materialization.
- Recurrence guard: Rename the parameter to a nonreserved short identifier and rerun the same owner-scoped apply_patch materialization.
- Rollback: Stop, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6478-M05-WFAIL, V6478-M05-WPASS

### V6478-M06 — Retained x1 failure recovery V6478-X1-N06

- Trigger: The declared bounded owner-local x1 workflow failure has occurred and remains retained.
- Method: Retain the contradictory failure, change only the comparison to 530, let Method Flow ingest the new witness pair, and rerun the unchanged x1 build.
- Recurrence guard: Retain the contradictory failure, change only the comparison to 530, let Method Flow ingest the new witness pair, and rerun the unchanged x1 build.
- Rollback: Stop, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6478-M06-WFAIL, V6478-M06-WPASS

### V6478-M07 — Retained x1 failure recovery V6478-X1-N07

- Trigger: The declared bounded owner-local x1 workflow failure has occurred and remains retained.
- Method: Retain the false replacement assumption, patch only the three exact assertions, and inspect their rendered lines before running validation.
- Recurrence guard: Retain the false replacement assumption, patch only the three exact assertions, and inspect their rendered lines before running validation.
- Rollback: Stop, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6478-M07-WFAIL, V6478-M07-WPASS

### V6478-M08 — Retained x1 failure recovery V6478-X1-N08

- Trigger: The declared bounded owner-local x1 workflow failure has occurred and remains retained.
- Method: Retain every invalid receipt, remove only the two extra EOF blank lines, restage the exact files, and repeat until the two self-exclusions and diff hygiene are stable and valid.
- Recurrence guard: Retain every invalid receipt, remove only the two extra EOF blank lines, restage the exact files, and repeat until the two self-exclusions and diff hygiene are stable and valid.
- Rollback: Stop, retain the failure, and leave repository and external state unchanged.
- Witnesses: V6478-M08-WFAIL, V6478-M08-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
