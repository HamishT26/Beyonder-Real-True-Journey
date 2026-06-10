# v469A GMUT v5 x1 Fixture Prerequisite Ladder

Classification: `blocker`

This ladder defines what must exist before null recovery or baseline recovery can be claimed. No fixture is executed in this phase.

## Null Fixture Ladder

`F0 scalar_disabled_flat_reference`

- `N=1`
- `beta^i=0`
- `h_ij=delta_ij`
- `R_ADM=0`
- `Psi` disabled by explicit switch
- `V(Psi)` unsampled
- Status: `not_run`

`F1 constant_scalar_symbolic_potential_probe`

- `Psi=Psi0` constant
- all derivatives zero
- `V(Psi0)` recorded but not interpreted
- comparison rule declared
- Status: `not_run`

`F2 homogeneous_temporal_mode`

- `partial_i Psi=0`
- `partial_0=(1/c)partial_t` applied
- temporal kinetic c-factor row checked
- Status: `not_run`

`F3 static_spatial_profile`

- `partial_t Psi=0`
- spatial gradient sign checked
- no spurious momentum density with zero shift
- Status: `not_run`

`F4 shift_transport_translation`

- nonzero shift
- `x0=ct` expression compared with `x0=t` translation
- transport combination verified
- Status: `not_run`

`F5 boundary_policy_probe`

- finite box
- periodic and Dirichlet variants
- `B_Psi` remains explicit unless conditions make it vanish
- Status: `not_run`

## Baseline Prerequisites

Before any recovery claim:

- exact baseline equation card
- selected ADM/SI branch
- full scalar disablement manifest
- disabled and held term list
- expected output shape
- comparison rule
- residual tolerance
- source-authority binding

Gate status: `null_recovery` and `baseline_recovery` remain open.
