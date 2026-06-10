# v469A GMUT v2 x1 Coefficient/SI Dictionary

Classification: `open_gap`

## Basis

This dictionary is routed through BIPM SI and NIST SP 811 references carried in v1 x2. It is a scaffold, not dimensional closure.

## Rows

| Symbol | Role | Current SI status | Closure need |
|---|---|---|---|
| `c` | speed of light | known, `m s^-1` | check placement in action and temporal derivatives |
| `G` | Newtonian gravitational constant | known, `m^3 kg^-1 s^-2` | match Einstein equation convention |
| `R` | Ricci scalar | conditional | declare coordinate convention |
| `Lambda` | cosmological constant | conditional | declare baseline role |
| `Psi` | scalar field | open | derive from action density |
| `nabla_mu Psi` | scalar gradient | open | declare `x0` convention |
| kinetic density | scalar kinetic term | open | derive field units and normalization |
| `V(Psi)` | potential density | symbolic hold | provide potential rule |
| `dV/dPsi` | scalar EOM term | blocked | define `V(Psi)` and `Psi` units |
| `T_Psi_mu_nu` | scalar stress-energy | open | derive by metric variation |
| `Q^nu` | exchange current | not declared | define only if coupling exists |
| `B_Psi` | previous coupling-like symbol | quarantined | separate definition artifact required |

## Result

The dimensional/SI gate remains open. The dictionary is now precise enough to guide v2 x2, but it does not close units.
