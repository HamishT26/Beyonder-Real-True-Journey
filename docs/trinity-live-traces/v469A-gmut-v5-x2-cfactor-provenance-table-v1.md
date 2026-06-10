# v469A GMUT v5 x2 C-Factor Provenance Table

Classification: `evidence`

This table stress-tests c-factor placement for the selected `x0=ct` rehearsal branch and the held `x0=t` translation branch.

| Surface | `x0=ct` rehearsal branch | `x0=t` translation branch | Status |
|---|---|---|---|
| covariant measure | `d4x = dx0 d3x = c dt d3x` | `d4x = dt d3x`, but determinant or line-element convention must carry c placement | `ct_rehearsal_preferred` |
| prefactor | `c^3/G` on `dx0 d3x` becomes `c^4/G` after `dx0=c dt` | `c^4/G` can appear directly when `t` is used and the line element carries `c dt` | `compatible_if_not_mixed` |
| derivative | `partial_0 = (1/c) partial_t` | `partial_0 = partial_t` if `x0=t`, with c factors carried elsewhere | `must_not_cross_import` |
| lapse/shift | `N` and `h` dimensionless; dimensionless `beta^i` preferred | `N` can remain dimensionless if `c` is explicit; shift may be velocity-like or rescaled | `translation_hold` |
| curvature bundle | `R` and ADM curvature terms carry `m^-2` after derivative conversion | same physical dimension only if metric and derivative c factors are consistently allocated | `open_gap_until_bundle_frozen` |
| scalar temporal kinetic | temporal scalar terms inherit `1/c` through each conversion | time derivative is direct but metric inverse and lapse factors carry c allocation | `open_gap_until_formula_card` |

Result: the `x0=ct` branch survives `v5_x2` as the safer rehearsal branch. `x0=t` remains usable only as a held translation branch.

Gate effect: dimensional/SI consistency remains open because the curvature bundle, scalar dimensions, and source authority are not fully frozen.
