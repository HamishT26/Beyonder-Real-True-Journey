# Trinity Expansion Result: os_runtime_benchmark_gate

- generated_utc: `2026-03-08T12:08:21+00:00`
- pillar: `body`
- overall_status: **FAIL**
- effective_success: `False`

## Checks
| name | status | detail |
|---|---|---|
| dependency:docs/trinity-expansion/os-runtime-benchmark-surface-audit-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/os-runtime-benchmark-sync-bridge-latest.json | FAIL | status=FAIL |
| dependency:docs/trinity-expansion/os-runtime-benchmark-materialization-tracer-latest.json | PASS | status=PASS |
| dependency:docs/trinity-expansion/os-runtime-benchmark-cache-board-latest.json | FAIL | status=FAIL |
| dependency:docs/trinity-expansion/os-runtime-benchmark-risk-board-latest.json | PASS | status=PASS |

## Metrics
```json
{
  "dependencies_checked": 5,
  "gating_class": "active",
  "pack": "os_runtime_benchmark",
  "pass_like_dependencies": 3
}
```

## Repo targets touched
- `docs/trinity-materialization-ledger.jsonl`
- `docs/trinity-mcp-cache/os-runtime-benchmark-latest.json`
- `docs/trinity-mcp-catalog-v3.json`
