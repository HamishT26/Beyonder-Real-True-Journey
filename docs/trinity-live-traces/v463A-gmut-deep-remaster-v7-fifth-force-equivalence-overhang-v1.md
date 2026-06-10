# v463A GMUT v7 Fifth-Force/Equivalence Overhang

Generated NZ: 2026-05-30T05:08:00+12:00

## Boundary

This artifact records external-constraint risk and parameter-map blockers. It does not claim fifth-force safety, equivalence compatibility, or empirical constraint satisfaction.

## Existing Anchor Overhangs

| Anchor | Working bound | Conservative bound | Overhang | Interpretation |
|---|---:|---:|---:|---|
| MICROSCOPE EP eta | `1.000000e-06` | `1.200000e-14` | `8.333e+07` | requires tighter parameter fit |
| Eot-Wash EP bucket | `1.000000e-06` | `6.000000e-13` | `1.667e+06` | requires tighter parameter fit |
| LLR residual | `1.000000e-06` | `1.200000e-11` | `8.333e+04` | requires tighter parameter fit |

## Required Parameter Map

The missing map must connect candidate coupling channel, `alpha_Psi`, `m_Psi`, any reactivated `lambda_T`, source composition, screening assumptions, and primary-source bounds to observables such as `eta`, anomalous acceleration, range, or relative coupling.

## Coupling Channels

| Channel | Status | Safe note |
|---|---|---|
| direct matter trace coupling | zeroed first pass | reduced current exposure does not clear reactivation risk |
| scalar-mediated force | unmapped | `alpha_Psi` and `m_Psi` need range/strength mapping |
| metric or curvature modification | unmapped | no observable bridge exists |
| hidden or boundary channel | quarantined | `B_Psi` and `alpha_B` inactive and undefined |

## Blocker

- `GMUT-V7-BLK-005 fifth_force_equivalence_parameter_map_overhang`

## Source Context

- `docs/mind-track-gmut-anchor-exclusion-latest.md` lines 13-15.
- `docs/trinity-live-traces/v462A-physics-constraint-suite-v1.json` lines 37-39.
- MICROSCOPE source anchor: https://arxiv.org/abs/2209.15487
- Eot-Wash source anchor: https://www.npl.washington.edu/eotwash/publications

## Safe Summary

External fifth-force/equivalence posture remains a hard blocker: map the parameters to observables, tighten the fit, and only then reassess readiness.
