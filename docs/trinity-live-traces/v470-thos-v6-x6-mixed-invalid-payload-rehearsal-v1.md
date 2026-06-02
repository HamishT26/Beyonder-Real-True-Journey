# v470 THOS v6 x6 Mixed-Invalid Payload Rehearsal

Phase: `v470_THOS_v6_x6`
Created NZ: `2026-06-02T17:13:52+12:00`

## Result

- Validator: `scripts/thos_row_universe_check.py`
- Expected status: `FAIL_BLOCKER`
- Actual status: `FAIL_BLOCKER`
- Expected exit code: `1`
- Actual exit code: `1`
- Source rows: `16`
- Canonical rows: `12`
- Rejected rows: `4`
- Accepted plus rejected equals source: `true`

## Rejection Buckets

- `duplicate_row_id`: `2`
- `missing_required:surface`: `1`
- `unknown_status`: `1`
- `non_object_row`: `1`

One rejected row can carry more than one reason, so reason-bucket counts may exceed rejected-row count.

## Boundary

This was a tempdir-only local rehearsal with temp paths redacted. It tests rejection routing only; it does not prove whole-system safety or validate GMUT.
