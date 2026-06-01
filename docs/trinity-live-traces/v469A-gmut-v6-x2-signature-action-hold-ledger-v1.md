# v469A GMUT v6 x2 Signature And Action Hold Ledger

Classification: `blocker`

Metric signature and action sign must be frozen before scalar kinetic or `T_Psi` promotion.

## Held Items

`metric_signature`: `HOLD_OPEN_GAP`

- Required before temporal kinetic sign finalization.
- Required before spatial kinetic sign finalization.
- Required before stress-energy template promotion.

`action_sign`: `HOLD_OPEN_GAP`

- Required before scalar EOM attempt.
- Required before `T_Psi` metric variation.
- Required before boundary variation ledger.

`source_anchor`: `HOLD_OPEN_GAP`

- Required before `PASS_ROW_READY` beyond derivative conversion.
- Required before coefficient dictionary closure.
- Required before fixture execution.

Blocked promotions: scalar EOM derived, `T_Psi` derived, temporal kinetic validated, dimensional/SI consistency closed, or fixture passed.
