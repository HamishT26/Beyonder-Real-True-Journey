# Trinity Expansion Result: multi_instance_runtime_v14_gate

- generated_utc: `2026-03-17T00:16:52+00:00`
- pillar: `body`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/multi-instance-runtime-v14-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/multi-instance-runtime-v14-sync-bridge-latest.json | FAIL | missing artifact: docs/trinity-expansion/multi-instance-runtime-v14-sync-bridge-latest.json |
| dependency:docs/trinity-expansion/multi-instance-runtime-v14-materialization-tracer-latest.json | FAIL | missing artifact: docs/trinity-expansion/multi-instance-runtime-v14-materialization-tracer-latest.json |
| dependency:docs/trinity-expansion/multi-instance-runtime-v14-cache-board-latest.json | FAIL | missing artifact: docs/trinity-expansion/multi-instance-runtime-v14-cache-board-latest.json |
| dependency:docs/trinity-expansion/multi-instance-runtime-v14-risk-board-latest.json | FAIL | missing artifact: docs/trinity-expansion/multi-instance-runtime-v14-risk-board-latest.json |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "multi_instance_runtime_v14",
  "pass_like_dependencies": 1
}
```

## Repo targets touched
- `docs/trinity-control-tower-latest.json`
- `docs/trinity-instance-handoff-contract-v1.json`
- `docs/trinity-instance-registry-v1.json`
- `docs/trinity-mcp-cache/multi-instance-runtime-v14-latest.json`
