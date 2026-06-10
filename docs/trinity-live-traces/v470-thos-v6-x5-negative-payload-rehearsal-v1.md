# v470 THOS v6 x5 Negative Payload Rehearsal

This artifact records three tempdir-only row-universe negative payload rehearsals. No curated file was corrupted or overwritten.

## Cases

- Duplicate row ID: expected `FAIL_BLOCKER`, actual exit `1`.
- Unknown status enum: expected `FAIL_BLOCKER`, actual exit `1`.
- Missing family field: expected `FAIL_BLOCKER`, actual exit `1`.

## Boundary

The temp paths are intentionally not preserved in curated artifacts. These rehearsals show local refusal routing only; they do not prove safety or validate GMUT.
