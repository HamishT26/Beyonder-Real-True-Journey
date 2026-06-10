# v469A GMUT v3 x2 Time-Derivative C-Factor Ledger

Classification: `open_gap`

Route A depends on one narrow bookkeeping idea: a length-normalized four-volume using `x0 = ct` can be rewritten as `dx0 d3x = c dt d3x`. Under that interpretation, a prefactor with `c3/G` in the length-volume route can become `c4/G` in a `dt d3x` route.

That observation is not enough for scalar dynamics.

## Required Rows

- `coordinate_choice`: unresolved until `x0 = ct` versus `x0 = t` is written explicitly.
- `measure_conversion`: ready as bookkeeping only.
- `prefactor_conversion`: ready only if tied to the measure conversion.
- `partial_operator`: unresolved until `partial_0 = (1/c) partial_t` or another rule is declared.
- `metric_components`: unresolved until `g00`, `g^00`, line-element convention, and inverse-metric units are fixed.
- `scalar_kinetic_density`: unresolved until `Psi`, `partial_mu Psi`, and `V(Psi)` units are declared.
- `stress_energy_units`: unresolved until the matter/scalar variation convention exists.

## v4 x1 Required Output

The next phase should produce coordinate, measure, derivative, metric-component, scalar-kinetic, and stress-energy cards. No gate closes from this ledger.
