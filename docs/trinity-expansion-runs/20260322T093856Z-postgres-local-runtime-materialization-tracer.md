# Trinity Expansion Result: postgres_local_runtime_materialization_tracer

- generated_utc: `2026-03-22T09:38:56+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| proof_written | PASS | docs/trinity-live-traces/postgres-local-runtime-proof-v1.json |
| ledger_appended | PASS | docs/trinity-materialization-ledger.jsonl |
| write_scope | PASS | mode=preview_only |
| blockers_recorded | PASS | blockers=0 |

## Metrics
```json
{
  "actual_state": "verified_live_write",
  "attempted_write": false,
  "blocker_count": 0,
  "connector_id": "postgres",
  "desired_state": "verified_live_write",
  "include_live_writes": false,
  "live_write_enabled": true,
  "materialization_level": "l2_persistent_dev",
  "mode": "preview_only",
  "pack": "postgres_local_runtime",
  "profile_context": "standard",
  "tracer_result": "SKIP"
}
```

## Repo targets touched
- `docs/trinity-live-traces/postgres-local-runtime-proof-v1.json`
- `docs/trinity-materialization-ledger.jsonl`
- `docs/trinity-mcp-catalog-v3.json`
