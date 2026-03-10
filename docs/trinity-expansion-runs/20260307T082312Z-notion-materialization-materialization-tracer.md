# Trinity Expansion Result: notion_materialization_materialization_tracer

- generated_utc: `2026-03-07T08:23:12+00:00`
- pillar: `heart`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| proof_written | PASS | docs/trinity-live-traces/notion-materialization-proof-v1.json |
| ledger_appended | PASS | docs/trinity-materialization-ledger.jsonl |
| write_scope | PASS | mode=preview_only |
| blockers_recorded | PASS | blockers=2 |

## Metrics
```json
{
  "actual_state": "staged_setup_gate",
  "attempted_write": false,
  "blocker_count": 2,
  "connector_id": "notion",
  "desired_state": "verified_live_write",
  "include_live_writes": false,
  "live_write_enabled": false,
  "mode": "preview_only",
  "pack": "notion_materialization",
  "profile_context": "collab",
  "tracer_result": "SKIP"
}
```

## Repo targets touched
- `docs/trinity-live-traces/notion-materialization-proof-v1.json`
- `docs/trinity-materialization-ledger.jsonl`
- `docs/trinity-mcp-catalog-v2.json`
