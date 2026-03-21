# Trinity Expansion Result: code_knowledge_graph_sync_bridge

- generated_utc: `2026-03-21T04:37:47+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| repo_file_inventory | PASS | files=8449 |
| symbol_inventory | PASS | symbols=857 |
| dependency_inventory | PASS | dependencies=717 |
| postgres_ready | PASS | bounded fallback from cached summary and prior Postgres proof |
| knowledge_graph_write_mode | PASS | read_only_cached_summary |

## Metrics
```json
{
  "connector_state_count": 10,
  "continuity_anchor_count": 13,
  "dependency_count": 717,
  "file_count": 8449,
  "generated_utc": "2026-03-21T04:37:47+00:00",
  "manifest_entry_count": 656,
  "postgres_ready": true,
  "postgres_runtime_detail": "bounded fallback from cached summary and prior Postgres proof",
  "profile_context": "materialize",
  "sql_summary": {
    "rows_written": {},
    "schema_loaded": false
  },
  "symbol_count": 857,
  "write_mode": false
}
```

## Repo targets touched
- `docs/trinity-code-knowledge-graph-contract-v1.json`
- `docs/trinity-code-knowledge-graph-summary-v1.json`
- `docs/trinity-live-traces/code-knowledge-graph-proof-v1.json`
