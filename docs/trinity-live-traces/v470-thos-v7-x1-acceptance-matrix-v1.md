# v470 THOS v7 x1 Acceptance Matrix

Phase: `v470_THOS_v7_x1`
Created NZ: `2026-06-02T17:48:59+12:00`

## Cases

- Clean pass shape: `PASS_SHAPE_ONLY`, digest references present.
- Missing digest references: `OPEN_GAP`, dominant finding `MISSING_DIGEST_REF_OPEN_GAP`.
- Orphan plus missing digest references: `FAIL_BLOCKER`, dominant failure `ORPHAN_VISUALIZATION_ROW`, secondary digest gap retained.
- Gate-effect drift: `FAIL_BLOCKER`, dominant failure `GMUT_GATE_EFFECT_DRIFT`.

## Boundary

The matrix records local checker behavior only. It does not certify safety, publication, connector action, GMUT validity, or gate closure.
