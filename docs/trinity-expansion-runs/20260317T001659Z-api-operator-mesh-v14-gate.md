# Trinity Expansion Result: api_operator_mesh_v14_gate

- generated_utc: `2026-03-17T00:16:59+00:00`
- pillar: `trinity`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/api-operator-mesh-v14-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/api-operator-mesh-v14-sync-bridge-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/api-operator-mesh-v14-materialization-tracer-latest.json | FAIL | missing artifact: docs/trinity-expansion/api-operator-mesh-v14-materialization-tracer-latest.json |
| dependency:docs/trinity-expansion/api-operator-mesh-v14-cache-board-latest.json | FAIL | missing artifact: docs/trinity-expansion/api-operator-mesh-v14-cache-board-latest.json |
| dependency:docs/trinity-expansion/api-operator-mesh-v14-risk-board-latest.json | FAIL | missing artifact: docs/trinity-expansion/api-operator-mesh-v14-risk-board-latest.json |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "api_operator_mesh_v14",
  "pass_like_dependencies": 2
}
```

## Repo targets touched
- `docs/trinity-api-book-latest.md`
- `docs/trinity-api-book-v3.json`
- `docs/trinity-api-usage-ledger.jsonl`
- `docs/trinity-mcp-cache/api-operator-mesh-v14-latest.json`
