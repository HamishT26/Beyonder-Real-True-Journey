# v470 THOS v6 x8 Precedence Fixture Report

Phase: `v470_THOS_v6_x8`
Created NZ: `2026-06-02T17:32:47+12:00`

## Result

- Validator: `scripts/thos_visualization_binding_check.py`
- Expected status: `FAIL_BLOCKER`
- Actual status: `FAIL_BLOCKER`
- Expected exit code: `1`
- Actual exit code: `1`
- Precedence rule: `FAIL_BLOCKER` overrides `OPEN_GAP`

## Meaning

When a structural blocker appears alongside missing digest references, blocker status dominates. The weaker open-gap finding does not soften the blocker.

## Boundary

This is a tempdir-only local precedence rehearsal with temp paths redacted. It does not prove safety or validate GMUT.
