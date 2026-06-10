# v464A GMUT v7 Divergence Target Hold Matrix

Status: `divergence_targets_named_not_evaluated`

This matrix names possible divergence and exchange targets only. It does not evaluate any divergence or assert conservation.

## Held Targets

- `nabla_mu T_total^mu_nu`: future total conservation target only.
- `nabla_mu T_Psi^mu_nu`: future scalar-sector check only.
- `exchange_current_placeholder`: reserved, not defined.
- `boundary_flux_terms`: reserved, not evaluated.

Do not promote any target to a conservation or exchange result until the required inputs exist and a separate derivation artifact evaluates the target.
