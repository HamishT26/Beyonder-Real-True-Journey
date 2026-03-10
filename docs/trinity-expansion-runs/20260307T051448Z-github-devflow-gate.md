# Trinity Expansion Result: github_devflow_gate

- generated_utc: `2026-03-07T05:14:48+00:00`
- pillar: `trinity`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/github-devflow-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/github-devflow-workflow-guard-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/github-devflow-risk-board-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/github-devflow-sync-bridge-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/github-devflow-cache-board-latest.json | FAIL | status=FAIL |
| connector_catalog_status | PASS | staged_setup_gate |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "staged_setup_gate",
  "pack": "github_devflow",
  "pass_like_dependencies": 4
}
```

## Repo targets touched
- `docs/trinity-mandala-scoreboard-latest.json`
- `docs/trinity-mcp-cache/github-devflow-latest.json`
- `docs/trinity-mcp-catalog-v1.json`
