# V13 Validation Matrix Summary

- generated_utc: `2026-03-16T02:44:00+00:00`
- branch: `codex/Aletheon/v13-canonical-trinity-lab`

## Repair notes
- `body_latency_budget_guard` now reads the Body benchmark policy instead of a stale hardcoded latency ceiling.
- `cache_waste_regenerator` now skips unreadable tracked paths rather than failing the entire suite on one corrupted filesystem entry.
- The comparative validation grid was restored to the standards-aligned shape expected by the Heart/public refresh guards.

## Matrix
| run | status | pass | warn | fail | timeout | actual posture |
|---|---|---:|---:|---:|---:|---|
| `standard` | `PASS` | 833 | 0 | 0 | 0 | `n/a` |
| `deep` | `PASS` | 838 | 0 | 0 | 0 | `n/a` |
| `collab --include-mcp-refresh` | `PASS` | 753 | 0 | 0 | 0 | `verified_live` refresh path |
| `standard --offline-only` | `PASS` | 833 | 0 | 0 | 0 | `offline_safe` |
| `materialize --materialization-level l2_persistent_dev` | `PASS` | 833 | 0 | 0 | 0 | `readiness_only` |
| `materialize --materialization-level l3_uat_preprod` | `PASS` | 833 | 0 | 0 | 0 | `readiness_only` |
| `materialize --materialization-level l4_standard_prod` | `PASS` | 833 | 0 | 0 | 0 | `readiness_only` |
| `materialize --materialization-level l5_ha_prod` | `PASS` | 833 | 0 | 0 | 0 | `readiness_only` |

## Close-out
- Final matrix close-out run: `materialize --materialization-level l5_ha_prod`
- Final suite state: `833 PASS / 0 WARN / 0 FAIL`
- Final expansion state: `776/776`
- Mandala scoreboard: `PASS`
