# v469A GMUT v6 x1 Scalar Unit Policy Hold Ledger

Classification: `open_gap`

This ledger records scalar field unit-policy alternatives without silently importing natural units or source assumptions.

| Policy | Meaning | Status | Blocked Until |
|---|---|---|---|
| `dimensionless_scalar_with_coefficients` | `Psi` is dimensionless and coefficients carry the SI load | `hypothesis` | coefficient dictionary exists |
| `action_inferred_scalar_dimension` | `Psi` dimension is derived from the action-unit target | `open_gap` | kinetic normalization and prefactor are fixed |
| `natural_unit_scalar_dimension` | natural-unit dimension is declared and later bridged to SI | `open_gap` | SI bridge exists |
| `source_defined_scalar_unit` | `Psi` unit is defined by an external source coupling | `blocker` | source authority is exact |

Parent decision: `UNIT_POLICY` remains `HOLD` for `v6_x1`.

Downstream effect:

- No dimensional inference from `V(Psi)`.
- No dimensional inference from `T_Psi`.
- No fifth-force parameter inference.
- No fixture pass or recovery claim.
