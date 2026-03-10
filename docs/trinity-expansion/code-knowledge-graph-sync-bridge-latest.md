# Trinity Expansion Result: code_knowledge_graph_sync_bridge

- generated_utc: `2026-03-10T09:31:49+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| repo_file_inventory | PASS | files=6452 |
| symbol_inventory | PASS | symbols=744 |
| dependency_inventory | PASS | dependencies=680 |
| postgres_ready | PASS | /var/run/postgresql:5432 - accepting connections |
| postgres_handshake | PASS | trinity_v5 |
| knowledge_graph_write_mode | PASS | read_only_preview |

## Metrics
```json
{
  "connector_state_count": 9,
  "continuity_anchor_count": 13,
  "dependency_count": 680,
  "file_count": 6452,
  "generated_utc": "2026-03-10T09:31:49+00:00",
  "manifest_entry_count": 314,
  "profile_context": "materialize",
  "sql_summary": {
    "rows_written": {},
    "schema_loaded": false
  },
  "symbol_count": 744,
  "write_mode": false
}
```

## Repo targets touched
- `docs/trinity-code-knowledge-graph-contract-v1.json`
- `docs/trinity-code-knowledge-graph-summary-v1.json`
- `docs/trinity-live-traces/code-knowledge-graph-proof-v1.json`
