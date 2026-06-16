# v544 GMUT/THOS v80 v7 x2 Rows 304-305 Reconciliation

Status: `PASS_ROWS_304_305_RECONCILED`

## Complete Rows

- `304`: Current-state beacon refresh.
- `305`: Omega-mini first lookup rule.

## Held Row

- `306`: Runner freshness classifier remains `held_blocked` and is not complete.

## Next Slice

The next authorized non-contiguous slice is `307-318`. Any receipt that executes this slice must explicitly preserve row `306` as held.
