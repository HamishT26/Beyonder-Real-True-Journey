# Trinity Expansion Result: code_knowledge_graph_sync_bridge

- generated_utc: `2026-03-11T04:04:40+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| repo_file_inventory | PASS | files=7951 |
| symbol_inventory | PASS | symbols=821 |
| dependency_inventory | PASS | dependencies=705 |
| postgres_ready | PASS | /var/run/postgresql:5432 - accepting connections |
| postgres_handshake | PASS | trinity_v5 |
| knowledge_graph_write_mode | PASS | read_only_preview |

## Metrics
```json
{
  "connector_state_count": 9,
  "continuity_anchor_count": 13,
  "dependency_count": 705,
  "file_count": 7951,
  "generated_utc": "2026-03-11T04:04:40+00:00",
  "manifest_entry_count": 314,
  "profile_context": "deep",
  "sql_summary": {
    "rows_written": {},
    "schema_loaded": false
  },
  "symbol_count": 821,
  "write_mode": false
}
```

## Repo targets touched
- `docs/trinity-code-knowledge-graph-contract-v1.json`
- `docs/trinity-code-knowledge-graph-summary-v1.json`
- `docs/trinity-live-traces/code-knowledge-graph-proof-v1.json`
