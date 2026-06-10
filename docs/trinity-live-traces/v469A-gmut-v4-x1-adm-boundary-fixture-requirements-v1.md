# v469A GMUT v4 x1 ADM, Boundary, and Fixture Requirements

Classification: `open_gap`

## Measure Requirement

The safe requirement is:

`sqrt(-g) d4x = N sqrt(h) dt d3x`

A bare `dt d3x` shortcut is not acceptable unless lapse `N`, induced spatial determinant `h`, signature, and coordinate convention are declared.

## Boundary Requirements

- State fixed data on initial and final time slices.
- State fixed data on the spatial boundary.
- State falloff requirements for metric perturbations, `Psi` minus background, and first derivatives.
- Acknowledge corner terms where relevant.
- Track generalized boundary completion for `F(Psi)R` or broader nonminimal structures.
- Keep `B_Psi` separate from observable mapping or weak-field reduction until boundary equivalence is shown.

## Fixture Inventory

- `fixture_action_4d_master`
- `fixture_measure_identity`
- `fixture_adm_bulk_boundary_split`
- `fixture_nonminimal_boundary_case`
- `fixture_minimal_control_case`
- `fixture_weak_field_symbolic`
- `fixture_eotvos_placeholder`
- `fixture_inverse_square_placeholder`
- `fixture_gate_language`

## Weak-Field and Observable Placeholders

Do not overload scalar `Psi` with a metric potential. Use distinct metric variables such as `Phi_g` and `Psi_g` if needed. Keep `V(Psi)` symbolic. Eotvos and inverse-square rows remain placeholders only and must not imply sign, size, exclusion strength, or safety.

All six gates remain open.
