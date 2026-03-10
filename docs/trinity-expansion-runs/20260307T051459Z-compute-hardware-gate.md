# Trinity Expansion Result: compute_hardware_gate

- generated_utc: `2026-03-07T05:14:59+00:00`
- pillar: `body`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/compute-hardware-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/compute-hardware-workflow-guard-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/compute-hardware-risk-board-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/compute-hardware-sync-bridge-latest.json | FAIL | status=FAIL |
| dependency:docs/trinity-expansion/compute-hardware-cache-board-latest.json | PASS | status=PASS |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "compute_hardware",
  "pass_like_dependencies": 4
}
```

## Repo targets touched
- `docs/system-suite-status.json`
- `docs/trinity-mandala-scoreboard-latest.json`
- `docs/trinity-mcp-cache/compute-hardware-latest.json`
