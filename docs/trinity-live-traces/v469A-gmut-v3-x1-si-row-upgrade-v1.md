# v469A GMUT v3 x1 SI Row Upgrade

Classification: `open_gap`

## Upgraded Rows

| Row | Expression | Status | Condition |
|---|---|---|---|
| gravitational prefactor Route A | `c^4/G` | pass conditional | measure is `dt d3x` and `R` is `m^-2` |
| gravitational prefactor Route B | `c^3/G` | pass conditional alternative | measure is length-normalized `d4x` |
| prior compact expression | `d4x c^4 R/G` | fail ambiguous | only works if `d4x` means `dt d3x` |
| scalar kinetic density | `1/2 g^{mu nu} nabla_mu Psi nabla_nu Psi` | fail open | `Psi` and metric dimensions undeclared |
| potential density | `V(Psi)` | fail symbolic | potential rule absent |
| stress-energy | `T_Psi_mu_nu` | fail open | metric variation and energy-density check incomplete |

## Result

The gravitational prefactor ambiguity is narrowed, but the scalar-sector unit gate remains open.
