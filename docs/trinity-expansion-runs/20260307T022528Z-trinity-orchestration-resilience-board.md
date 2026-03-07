# Trinity Expansion Result: trinity_orchestration_resilience_board

- generated_utc: `2026-03-07T02:25:28+00:00`
- pillar: `trinity`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/trinity-operation-mode-guard-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/trinity-system-dependency-graph-latest.json | PASS | status=PASS |
| dependency:docs/system-suite-status.json | FAIL | status=FAIL |
| suite_status_effective | FAIL | effective_success=False |

## Metrics
```json
{
  "dependencies_checked": 3,
  "pass_like_dependencies": 2
}
```

## Repo targets touched
- `docs/system-suite-status.json`
- `scripts/run_all_trinity_systems.py`
