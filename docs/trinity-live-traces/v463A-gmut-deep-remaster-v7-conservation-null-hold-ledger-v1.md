# v463A GMUT v7 Conservation/Null Hold Ledger

Generated NZ: 2026-05-30T05:08:00+12:00

## Boundary

This artifact records readiness and holds. It does not claim conservation, exchange closure, null recovery, or baseline recovery.

## Conservation Route

The current safe target is a minimal decoupled scalar conservation route, not an exchange-law closure. This depends on `lambda_T = 0`, `B_Psi` staying quarantined, `V(Psi)` remaining symbolic, and `T_Psi_mu_nu` staying on metric-variation hold.

Unsafe phrases remain blocked: “conservation verified,” “divergence vanishes,” “exchange resolved,” “baseline recovered,” and “null recovery passed.”

## Hold Rows

| Row | Status | Required artifact |
|---|---|---|
| scalar EOM | prepared, not derived | explicit derivation under selected signature, action sign, and potential convention |
| `T_Psi_mu_nu` | metric-variation hold | metric variation derivation and sign review |
| divergence behavior | not executed | explicit divergence calculation or exchange-law ledger |
| boundary conditions | not declared | boundary condition and source/sink declaration |
| null switch | design only | dry-run or formal fixture for inert limits |
| baseline comparator | not executed | comparison against GR/LambdaCDM/SM or preserved baseline surface |
| fixture result | absent | closure fixture with inputs, expected baseline, observed result, and verdict |

## Blockers

- `GMUT-V7-BLK-003 conservation_divergence_readiness_hold`
- `GMUT-V7-BLK-004 null_baseline_execution_hold`

## Source Context

- `docs/trinity-live-traces/v463A-gmut-deep-remaster-v6-v7-handoff-v1.json`.
- `docs/trinity-live-traces/v462A-physics-constraint-suite-v1.json` lines 7-8 and 12-13.

## Safe Summary

v7 preserves the minimal scalar conservation route as a target, while keeping EOM, stress-energy, divergence, null execution, and baseline recovery explicitly open.
