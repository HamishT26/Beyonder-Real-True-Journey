# v463A GMUT v2 Unit Dimension Ledger

Generated UTC: 2026-05-29T12:48:47Z
Generated NZ: 2026-05-30T00:48:47+12:00

## Status

`v463A_GMUT_v2` creates a unit and dimension blocker ledger. It does not close the dimensional consistency gate.

## Source Boundary

- Evidence: NIST SI material supports explicit quantity, unit, base-unit, derived-unit, and defining-constant discipline.
- Evidence: NIST SP 330 supports keeping `c` and `h` explicit in SI bridge work.
- Evidence: NIST SP 811 Chapter 5 supports identifying the natural-unit system when it is used.
- Context: Solas v45 supports projection-gate discipline as `journey_context_not_canon`.

## Ledger Defaults

- Unit system: `natural_units_c_hbar_1_for_fixture_only_with_SI_bridge_required`
- Metric signature: not finalized; v7 `-+++` remains a dry-run default only.
- Coordinate convention: not finalized.
- Action normalization: not finalized.
- Dimensional gate completed: `false`

## Rows

- `Psi`: blocked. Field dimension depends on action normalization, coordinate convention, spacetime dimension, and source route.
- `partial_mu_Psi_or_nabla_mu_Psi`: blocked. Operator and coordinate dimensions remain unselected.
- `V(Psi)`: blocked. Potential functional form, normalization, and field dimension are not fixed.
- `T_Psi_mu_nu`: blocked. Expected stress/energy-density target only; no metric-variation derivation exists.
- `alpha_Psi`: blocked. Coupling dimension depends on target term and observable normalization.
- `alpha_B`: blocked. Bridge-term dimensions depend on missing `B_Psi_mu_nu` definition.
- `natural_units_c_hbar_1`: context only. Natural units simplify notation but do not remove unit-row duties.

## Boundary

Allowed v2 labels are ledger-hygiene labels only: `pass_unit_row_well_formed_for_review`, `pass_symbolic_only_classified`, and `pass_blocker_explicit`.

Forbidden v2 labels include dimensional gate pass, stress-energy derivation pass, conservation pass, fifth-force clearance, and consciousness bridge pass.
