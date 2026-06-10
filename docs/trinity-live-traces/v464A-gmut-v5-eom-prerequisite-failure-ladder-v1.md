# v464A GMUT v5 EOM Prerequisite Failure Ladder

Status: `prerequisites_ranked_for_future_derivation`

This ladder ranks blockers for a future scalar EOM derivation. It is not a derivation and does not validate the scalar sector.

## Hard Prerequisites

- `V(Psi)` remains symbolic, so `dV_dPsi` is formal only.
- `Z_Psi` remains symbolic or unknown, so kinetic normalization and field dimensions are unresolved.
- Boundary policy is undefined, so integration by parts cannot support a result.
- Integration by parts is planned but not executed.
- Field dimensions and SI bridge remain open.
- Metric variation policy remains held, so `T_Psi_mu_nu` and divergence checks remain unavailable.

## Allowed Placeholders

- `dV_dPsi`: symbolic derivative only.
- `Z_Psi`: held normalization placeholder only.
- `delta S_Psi / delta Psi`: route label only.

Dimensional/SI and conservation/exchange gates remain open.
