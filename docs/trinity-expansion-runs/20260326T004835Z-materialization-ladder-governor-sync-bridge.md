# Trinity Expansion Result: materialization_ladder_governor_sync_bridge

- generated_utc: `2026-03-26T00:48:35+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| tool:docker | PASS | Docker version 29.2.1, build a5c7197 |
| tool:git | PASS | git version 2.53.0.windows.1 |
| tool:materialized | PASS | missing (optional probe) |
| tool:mz | PASS | missing (optional probe) |
| tool:dbt | PASS | missing (optional probe) |
| required_probe_tools_available | PASS | missing=[] |
| cache_written | PASS | docs/trinity-mcp-cache/materialization-ladder-governor-latest.json |

## Metrics
```json
{
  "actual_state": "active",
  "auth_state": "local_repo",
  "blocker_count": 0,
  "cache_status": "active",
  "desired_state": "active",
  "live_read_enabled": false,
  "live_write_enabled": false,
  "pack": "materialization_ladder_governor",
  "record_count": 6,
  "strategy": "local_probe"
}
```

## Repo targets touched
- `docs/trinity-materialization-ladder-board-latest.json`
- `docs/trinity-materialization-ladder-v1.json`
- `docs/trinity-mcp-cache/materialization-ladder-governor-latest.json`
