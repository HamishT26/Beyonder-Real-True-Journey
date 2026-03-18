# Trinity Expansion Result: ha_failover_drill_v9_gate

- generated_utc: `2026-03-18T02:56:25+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/ha-failover-drill-v9-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/ha-failover-drill-v9-sync-bridge-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/ha-failover-drill-v9-materialization-tracer-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/ha-failover-drill-v9-cache-board-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/ha-failover-drill-v9-risk-board-latest.json | PASS | status=PASS |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "ha_failover_drill_v9",
  "pass_like_dependencies": 5
}
```

## Repo targets touched
- `docs/trinity-ha-failover-drill-v1.json`
- `docs/trinity-materialization-ladder-v3.json`
- `docs/trinity-mcp-cache/ha-failover-drill-v9-latest.json`
- `docs/trinity-synthetic-mesh-schema-contract-v1.json`
