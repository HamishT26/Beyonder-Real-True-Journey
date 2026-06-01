# v469A GMUT v2 x2 SI Pass/Fail Ledger

Classification: `open_gap`

## Rows

| Symbol | Status | Reason |
|---|---|---|
| `c` | pass as known symbol | SI route exists; placement still open |
| `G` | pass as known symbol | SI route exists; coefficient placement still open |
| `R` | conditional | coordinate convention needed |
| `Lambda` | conditional | baseline role and coordinates needed |
| `Psi` | fail open | field dimension not derived |
| `nabla_mu Psi` | fail open | depends on `Psi` and coordinates |
| `V(Psi)` | fail symbolic | no potential rule |
| `dV/dPsi` | fail blocked | no derivative rule |
| `T_Psi_mu_nu` | fail open | needs metric variation and unit check |
| `Q^nu` | not applicable yet | no coupling declared |
| `B_Psi` | quarantined | separate definition artifact required |

## Result

The dimensional/SI gate remains open. v3 x1 should focus on turning the failed rows into either declared assumptions or explicit blockers.
