# v465A GMUT v4 x2 Run Status

Status: `ready_for_validation`.

Start NZ: `2026-06-01T01:01:20+12:00`.

Prepared NZ: `2026-06-01T01:05:18+12:00`.

Live git start:

- Branch: `codex/GHC-Family/v58-omega-exec`
- Local HEAD: `615161e2118fc606fae8ee97a8190dc4566f06ad`
- Upstream HEAD: `615161e2118fc606fae8ee97a8190dc4566f06ad`
- Shared remote HEAD: `615161e2118fc606fae8ee97a8190dc4566f06ad`
- Drift: `0 0`

## Result

`v465A_GMUT_v4_x2` completed the 20-search refresh and synthesized `v4 x1` into a narrow `v5 x1` route: fill non-closing scaffold cards only, keep `full_scalar_disablement` blocked for closure, and keep all six gates open.

## Decisions

- `v5 x1` should attempt scaffold-card materialization only.
- Fixture execution remains forbidden.
- `PASS_HYGIENE_ONLY` remains premature.
- Source authority is sufficient for routing but insufficient for closure.

Next expected phase: `v465A_GMUT_v5_x1`.

All six GMUT gates remain open.
