# Trinity Expansion Result: baseline_restore_governor_v17_gate

- generated_utc: `2026-03-22T19:56:46+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/baseline-restore-governor-v17-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/baseline-restore-governor-v17-sync-bridge-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/baseline-restore-governor-v17-materialization-tracer-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/baseline-restore-governor-v17-cache-board-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/baseline-restore-governor-v17-risk-board-latest.json | PASS | status=PASS |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "baseline_restore_governor_v17",
  "pass_like_dependencies": 5
}
```

## Repo targets touched
- `docs/system-suite-status.json`
- `docs/trinity-mcp-cache/baseline-restore-governor-v17-latest.json`
- `docs/v17-baseline-state-v1.json`
- `docs/v17-system-suite-status-latest.json`
