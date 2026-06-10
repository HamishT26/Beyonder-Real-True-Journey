# v469A GMUT v6 x2 Temporal Card Audit

Classification: `evidence`

This artifact audits the `v6_x1` temporal kinetic formula card after source refresh.

| Row | Requirement | Status | Limit |
|---|---|---|---|
| `partial_0_conversion` | `partial_0 Psi = c^-1 partial_t Psi` under `x0=ct` | `PASS_ROW_READY_FOR_REVIEW_ONLY` | conversion identity only; not an EOM derivation |
| `temporal_contraction` | `g^00 (partial_0 Psi)^2 = g^00 c^-2 (partial_t Psi)^2` | `HOLD_OPEN_GAP` | metric signature and action sign not frozen |
| `spatial_contraction` | spatial-gradient term must cite `h^ij partial_i Psi partial_j Psi` and sign convention | `HOLD_OPEN_GAP` | spatial sign and scalar unit policy not frozen |
| `x0_t_translation_appendix` | `x0=t` rows must be translation-only and record c relocation | `HOLD_OPEN_GAP` | appendix not fully materialized |

Result: only the derivative conversion row is review-ready. The temporal kinetic card remains open because metric signature, action sign, scalar units, and source anchors are not frozen.
