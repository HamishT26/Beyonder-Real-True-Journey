# Trinity Expansion Result: uat_preprod_fabric_gate

- generated_utc: `2026-03-19T07:45:24+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/uat-preprod-fabric-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/uat-preprod-fabric-sync-bridge-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/uat-preprod-fabric-materialization-tracer-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/uat-preprod-fabric-cache-board-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/uat-preprod-fabric-risk-board-latest.json | PASS | status=PASS |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "uat_preprod_fabric",
  "pass_like_dependencies": 5
}
```

## Repo targets touched
- `docs/trinity-materialization-ladder-v1.json`
- `docs/trinity-mcp-cache/uat-preprod-fabric-latest.json`
- `docs/trinity-uat-preprod-targets-v1.json`
