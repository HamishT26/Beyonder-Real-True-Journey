# v470 THOS v7 x1 Enhanced Precedence Report

Phase: `v470_THOS_v7_x1`
Created NZ: `2026-06-02T17:48:59+12:00`

## Result

- Validator: `scripts/thos_visualization_binding_check.py`
- Expected status: `FAIL_BLOCKER`
- Actual status: `FAIL_BLOCKER`
- Dominant failure code: `ORPHAN_VISUALIZATION_ROW`
- Secondary findings: `MISSING_DIGEST_REF_OPEN_GAP`
- Weaker findings suppressed: `false`

## Meaning

The checker preserves the weaker digest-reference gap while correctly letting the orphan visualization row dominate the aggregate status.

## Boundary

This was a tempdir-only local precedence rehearsal with temp paths redacted. It does not prove safety or validate GMUT.
