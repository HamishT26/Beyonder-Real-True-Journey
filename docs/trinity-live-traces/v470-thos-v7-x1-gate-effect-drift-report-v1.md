# v470 THOS v7 x1 Gate-Effect Drift Report

Phase: `v470_THOS_v7_x1`
Created NZ: `2026-06-02T17:48:59+12:00`

## Result

- Validator: `scripts/thos_visualization_binding_check.py`
- Expected status: `FAIL_BLOCKER`
- Actual status: `FAIL_BLOCKER`
- Dominant failure code: `GMUT_GATE_EFFECT_DRIFT`
- Gate-effect drift count: `1`

## Meaning

Any visualization payload that claims a GMUT gate effect outside `none_open_not_tested` is blocker-class in this local checker.

## Boundary

This was a tempdir-only local claim-boundary rehearsal. It does not prove safety or validate GMUT.
