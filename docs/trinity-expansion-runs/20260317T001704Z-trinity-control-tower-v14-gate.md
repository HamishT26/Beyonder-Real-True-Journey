# Trinity Expansion Result: trinity_control_tower_v14_gate

- generated_utc: `2026-03-17T00:17:04+00:00`
- pillar: `trinity`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/trinity-control-tower-v14-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/trinity-control-tower-v14-sync-bridge-latest.json | FAIL | missing artifact: docs/trinity-expansion/trinity-control-tower-v14-sync-bridge-latest.json |
| dependency:docs/trinity-expansion/trinity-control-tower-v14-materialization-tracer-latest.json | FAIL | missing artifact: docs/trinity-expansion/trinity-control-tower-v14-materialization-tracer-latest.json |
| dependency:docs/trinity-expansion/trinity-control-tower-v14-cache-board-latest.json | FAIL | missing artifact: docs/trinity-expansion/trinity-control-tower-v14-cache-board-latest.json |
| dependency:docs/trinity-expansion/trinity-control-tower-v14-risk-board-latest.json | FAIL | missing artifact: docs/trinity-expansion/trinity-control-tower-v14-risk-board-latest.json |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "trinity_control_tower_v14",
  "pass_like_dependencies": 1
}
```

## Repo targets touched
- `docs/trinity-control-tower-latest.json`
- `docs/trinity-control-tower-latest.md`
- `docs/trinity-mcp-cache/trinity-control-tower-v14-latest.json`
- `docs/v14-trinity-verdict-v1.json`
