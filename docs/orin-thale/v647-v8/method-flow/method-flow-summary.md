# GHC Family Method Flow State

- Phase: v647-gmut-thos-v8-x1-x2
- Owner: Orin Thale
- Methods: 12
- Passing witnesses: 12
- Failed witnesses retained: 12

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

### V6478-M09 — Inspect generated list boundary before validator execution

- Trigger: A generated validator fails compilation at a list-to-branch boundary.
- Method: Insert one exact newline at the list boundary, recompile, and then run the unchanged bounded selection.
- Recurrence guard: Compile generated Python before execution and inspect list-to-control-flow boundaries after slice replacement.
- Rollback: Stop before execution, retain the syntax failure, and leave external and sibling state unchanged.
- Witnesses: V6478-M09-WFAIL, V6478-M09-WPASS

### V6478-M10 — Bind historical x1 assertions to immutable Git blobs

- Trigger: The x1 commit is known and ancestral.; The asserted x1 artifact is immutable in that commit.; The live artifact is intentionally append-only.
- Method: Read only the historical assertion target from the exact x1 Git blob while keeping current lifecycle assertions live.
- Recurrence guard: Declare whether each lifecycle assertion is historical or live before selecting its data source.
- Rollback: Restore the live read, retain the failing selection, and stop if the x1 commit or blob path is not exact.
- Witnesses: V6478-M10-WFAIL, V6478-M10-WPASS

### V6478-M11 — Normalize generated Python EOF before staged review

- Trigger: Only additive owner-generated Python files are named by the exact diff-hygiene output.
- Method: Remove only the reported extra EOF blank lines, restage the same paths, and rerun the unchanged exact review.
- Recurrence guard: Generate exactly one terminal newline and run diff hygiene before the first staged-manifest pass.
- Rollback: Restore the owner-generated files from the staged index and retain the failed gate if any non-EOF content changes.
- Witnesses: V6478-M11-WFAIL, V6478-M11-WPASS

### V6478-M12 — Normalize closeout Python EOF before seal review

- Trigger: Only additive owner-generated closeout Python files are named by the exact diff output.
- Method: Remove only the reported EOF blank lines, restage the same paths, and rerun the unchanged closeout gate.
- Recurrence guard: Generate exactly one terminal newline and run diff hygiene before closeout-manifest materialization.
- Rollback: Restore the files from the staged index and retain the failure if any non-EOF content changes.
- Witnesses: V6478-M12-WFAIL, V6478-M12-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
