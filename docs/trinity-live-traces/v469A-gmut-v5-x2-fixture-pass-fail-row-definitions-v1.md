# v469A GMUT v5 x2 Fixture Pass/Fail Row Definitions

Classification: `advisory`

This artifact turns the `v5_x1` fixture ladder into pass/fail row definitions without executing fixtures.

## Row Semantics

`PASS_ROW_READY`: all inputs, expected outputs, comparison rule, tolerance, and source anchor are defined. The row is ready to execute later.

`HOLD_OPEN_GAP`: at least one prerequisite is missing. The row must not be counted as a pass.

`FAIL_ROW_INVALID`: a contradiction, mixed convention, forbidden claim, or missing switch invalidates the row.

## Fixture Rows

| ID | Name | Current Status | Missing |
|---|---|---|---|
| F0 | scalar disabled flat reference | `HOLD_OPEN_GAP` | full scalar disablement switch, comparison tolerance, source-bound expected output |
| F1 | constant scalar symbolic potential probe | `HOLD_OPEN_GAP` | `V(Psi0)` interpretation rule, potential hold rule, comparison rule |
| F2 | homogeneous temporal mode | `HOLD_OPEN_GAP` | temporal kinetic formula card, scalar unit policy, c-factor derivative audit |
| F3 | static spatial profile | `HOLD_OPEN_GAP` | spatial-gradient sign card, stress-template import boundary, momentum-density expectation |
| F4 | shift transport translation | `HOLD_OPEN_GAP` | `x0=t` translation card, shift unit policy, transport-equivalence comparison |
| F5 | boundary policy probe | `HOLD_OPEN_GAP` | boundary class selection, `B_Psi` definition or quarantine confirmation, finite-box rule |

Execution status: `not_run`.
