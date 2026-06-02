# v470 THOS v7 x1 Report Schema Contract

Phase: `v470_THOS_v7_x1`
Created NZ: `2026-06-02T17:48:59+12:00`

## Contract

v7 x1 hardens the visualization binding report shape. Reports now expose local mode, precedence order, dominant failure or finding code, secondary findings, a precedence reason, unsuppressed weaker findings, digest-reference presence status, count reconciliation status, and explicit orphan/duplicate/tuple/gate-effect counts.

## Status Rule

`FAIL_BLOCKER` overrides `OPEN_GAP`; `OPEN_GAP` overrides `PASS_SHAPE_ONLY`. Weaker findings remain visible and are not treated as resolved.

## Boundary

This is local THOS report-schema hardening. It does not certify safety, publish governance findings, authorize connector writes, validate GMUT, or move any GMUT gate.
