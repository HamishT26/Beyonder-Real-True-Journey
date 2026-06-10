# v470 THOS v7 x2 Evidence Matrix

## Must Pass

- Regenerated pass report assertion: `PASS_SHAPE_ONLY`.
- Regenerated open-gap report assertion: `PASS_SHAPE_ONLY`.
- Regenerated gate-drift blocker assertion after the binding-checker fix: `PASS_SHAPE_ONLY`.

## Must Fail

- Pre-fix gate-drift count-status gap: `count:detail_reconciliation`.
- Negative count mismatch: `count:detail_reconciliation`.
- Negative secondary suppression: `secondary:retention`.
- Negative digest status: `digest:presence_reconciliation`.
- Negative boundary mutation/Gate effect claim: `boundary:local_non_mutating`.

## Boundary

All evidence is local, deterministic, and non-mutating. It does not authorize connector writes or move any GMUT gate.
