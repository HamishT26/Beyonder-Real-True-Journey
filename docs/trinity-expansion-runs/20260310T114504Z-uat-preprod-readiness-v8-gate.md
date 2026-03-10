# Trinity Expansion Result: uat_preprod_readiness_v8_gate

- generated_utc: `2026-03-10T11:45:04+00:00`
- pillar: `body`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/uat-preprod-readiness-v8-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/uat-preprod-readiness-v8-sync-bridge-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/uat-preprod-readiness-v8-materialization-tracer-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/uat-preprod-readiness-v8-cache-board-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/uat-preprod-readiness-v8-risk-board-latest.json | FAIL | status=FAIL |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "uat_preprod_readiness_v8",
  "pass_like_dependencies": 4
}
```

## Repo targets touched
- `docs/trinity-materialization-ladder-v2.json`
- `docs/trinity-mcp-cache/uat-preprod-readiness-v8-latest.json`
- `docs/trinity-uat-preprod-targets-v2.json`
