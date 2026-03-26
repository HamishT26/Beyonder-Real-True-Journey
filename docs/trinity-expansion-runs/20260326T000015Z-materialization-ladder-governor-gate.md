# Trinity Expansion Result: materialization_ladder_governor_gate

- generated_utc: `2026-03-26T00:00:15+00:00`
- pillar: `trinity`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/materialization-ladder-governor-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/materialization-ladder-governor-sync-bridge-latest.json | FAIL | status=FAIL |
| dependency:docs/trinity-expansion/materialization-ladder-governor-materialization-tracer-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/materialization-ladder-governor-cache-board-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/materialization-ladder-governor-risk-board-latest.json | PASS | status=PASS |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "materialization_ladder_governor",
  "pass_like_dependencies": 4
}
```

## Repo targets touched
- `docs/trinity-materialization-ladder-board-latest.json`
- `docs/trinity-materialization-ladder-v1.json`
- `docs/trinity-mcp-cache/materialization-ladder-governor-latest.json`
