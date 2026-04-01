# Trinity Expansion Result: docker_pilot_gate

- generated_utc: `2026-04-01T02:27:28+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/docker-pilot-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/docker-pilot-sync-bridge-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/docker-pilot-materialization-tracer-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/docker-pilot-cache-board-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/docker-pilot-risk-board-latest.json | PASS | status=PASS |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "docker_pilot",
  "pass_like_dependencies": 5
}
```

## Repo targets touched
- `docs/trinity-docker-pilot-report-v1.json`
- `docs/trinity-materialization-ledger.jsonl`
- `docs/trinity-mcp-cache/docker-pilot-latest.json`
