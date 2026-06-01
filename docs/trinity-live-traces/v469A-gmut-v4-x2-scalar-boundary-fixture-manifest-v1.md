# v469A GMUT v4 x2 Scalar, Boundary, and Fixture Manifest

Classification: `open_gap`

This is a prerequisite manifest only. No fixture is executed.

## Boundary Policy Requirements

- Declare fixed metric data on initial and final hypersurfaces.
- Declare fixed scalar data or scalar variation class.
- Declare spatial boundary and falloff class.
- Declare compact support, Dirichlet, Neumann, mixed, or asymptotic conditions.
- Declare generalized boundary completion for `F(Psi)R`-like terms before any nonminimal route advances.
- Keep `B_Psi` as a quarantine bucket until separately defined.

## Fixture Manifest

- `fixture_action_4d_master`
- `fixture_measure_identity`
- `fixture_adm_bulk_boundary_split`
- `fixture_minimal_scalar_control`
- `fixture_nonminimal_boundary_case`
- `fixture_scalar_disablement_manifest`
- `fixture_weak_field_symbolic`
- `fixture_gate_language`

All fixtures are `not_executed`.
