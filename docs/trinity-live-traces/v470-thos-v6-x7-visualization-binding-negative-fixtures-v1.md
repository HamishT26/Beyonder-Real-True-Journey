# v470 THOS v6 x7 Visualization Binding Negative Fixtures

Phase: `v470_THOS_v6_x7`
Created NZ: `2026-06-02T17:28:28+12:00`

## Result

- Validator: `scripts/thos_visualization_binding_check.py`
- Expected status: `FAIL_BLOCKER`
- Actual status: `FAIL_BLOCKER`
- Expected exit code: `1`
- Actual exit code: `1`
- Structural binding status: `FAIL_BLOCKER`
- Digest evidence status: `FAIL_BLOCKER`

## Failure Codes Exercised

- `MALFORMED_VISUALIZATION_ROW`
- `DUPLICATE_VISUALIZATION_BINDING`
- `ORPHAN_VISUALIZATION_ROW`
- `MISSING_CANONICAL_VISUALIZATION_ROW`
- `TUPLE_MISMATCH`
- `DIGEST_MISMATCH`

## Boundary

This was a tempdir-only local rehearsal with temp paths redacted. It tests local projection failure routing only; it does not prove safety or validate GMUT.
