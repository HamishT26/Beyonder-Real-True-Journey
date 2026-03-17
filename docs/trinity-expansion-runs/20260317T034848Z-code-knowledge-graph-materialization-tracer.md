# Trinity Expansion Result: code_knowledge_graph_materialization_tracer

- generated_utc: `2026-03-17T03:48:48+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| proof_written | PASS | docs/trinity-live-traces/code-knowledge-graph-proof-v1.json |
| ledger_appended | PASS | docs/trinity-materialization-ledger.jsonl |
| write_scope | PASS | mode=l5_ha_prod |
| blockers_recorded | PASS | blockers=0 |

## Metrics
```json
{
  "actual_state": "verified_live_write",
  "attempted_write": true,
  "blocker_count": 0,
  "connector_id": "postgres",
  "desired_state": "verified_live_write",
  "include_live_writes": true,
  "live_write_enabled": true,
  "materialization_level": "l5_ha_prod",
  "mode": "l5_ha_prod",
  "pack": "code_knowledge_graph",
  "profile_context": "materialize",
  "tracer_result": "PASS"
}
```

## Repo targets touched
- `docs/trinity-code-knowledge-graph-contract-v1.json`
- `docs/trinity-expansion/code-knowledge-graph-sync-bridge-latest.json`
- `docs/trinity-live-traces/code-knowledge-graph-proof-v1.json`
- `docs/trinity-materialization-ledger.jsonl`
