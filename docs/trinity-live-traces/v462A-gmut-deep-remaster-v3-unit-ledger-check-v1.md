# v462A_GMUT_v3 Unit-Ledger Check v1

Generated UTC: 2026-05-29T08:50:45Z
Generated NZ: 2026-05-29T20:50:45+12:00

## Scope

This is a structural unit-class check against the v2 unit-ledger seed. It is not physics validation and does not close dimensional consistency.

## Result

- evidence: Four baseline rows were checked as baseline unit classes: `G_mu_nu`, `Lambda_g_mu_nu`, `kappa_T_SM_mu_nu`, and `kappa_T_DM_mu_nu`.
- blocker: Five candidate rows remain blocked or excluded: `alpha_Psi_T_Psi_mu_nu`, `alpha_B_B_Psi_mu_nu`, `Psi`, `V_Psi`, and `lambda_T`.
- context: `beta_I`, `gamma_C`, `delta_S`, and `epsilon_H` remain meta-layer or meaning-layer terms and are excluded from physical unit promotion.
- blocker: Dimensional consistency is not passed.

## Candidate Blockers

- blocker: `alpha_Psi_T_Psi_mu_nu` needs coupling units, source units, bounds, observables, null behavior, and conservation/exchange behavior.
- blocker: `alpha_B_B_Psi_mu_nu` needs tensor or effective-term definition, units, and divergence behavior.
- blocker: `Psi` and `V(Psi)` need action, Lagrangian, or convention before units are stable.
- blocker: `lambda_T` needs an explicitly defined source trace before use.

## Handoff

v462A_GMUT_v4 should define the blocked candidate objects before attempting dimensional gate closure.
