# Trinity Expansion Result: code_knowledge_graph_cache_board

- generated_utc: `2026-03-31T03:40:59+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| cache_present | PASS | docs/trinity-mcp-cache/code-knowledge-graph-latest.json |
| cache_schema_present | PASS | docs/trinity-mcp-cache-schema-v3.json |
| cache_required_fields | PASS | missing=[] |
| cache_record_count | PASS | records=1 |
| cache_freshness | PASS | age_days=0.0 |
| cache_integration_id | PASS | integration_id=code_knowledge_graph |

## Metrics
```json
{
  "age_days": 0.0,
  "freshness_window_days": 7.0,
  "pack": "code_knowledge_graph",
  "record_count": 1
}
```

## Repo targets touched
- `docs/trinity-code-knowledge-graph-contract-v1.json`
- `docs/trinity-expansion/code-knowledge-graph-sync-bridge-latest.json`
- `docs/trinity-mcp-cache-schema-v3.json`
- `docs/trinity-mcp-cache/code-knowledge-graph-latest.json`
