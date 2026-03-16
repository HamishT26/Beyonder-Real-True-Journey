# Trinity Expansion Result: filesystem_scope_governor_cache_board

- generated_utc: `2026-03-16T01:01:15+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| cache_present | PASS | docs/trinity-mcp-cache/filesystem-scope-governor-latest.json |
| cache_schema_present | PASS | docs/trinity-mcp-cache-schema-v3.json |
| cache_required_fields | PASS | missing=[] |
| cache_record_count | PASS | records=2 |
| cache_freshness | PASS | age_days=0.0 |
| cache_integration_id | PASS | integration_id=filesystem_scope_governor |

## Metrics
```json
{
  "age_days": 0.0,
  "freshness_window_days": 30.0,
  "pack": "filesystem_scope_governor",
  "record_count": 2
}
```

## Repo targets touched
- `docs/trinity-materialization-ledger.jsonl`
- `docs/trinity-mcp-cache-schema-v3.json`
- `docs/trinity-mcp-cache/filesystem-scope-governor-latest.json`
- `docs/trinity-mcp-catalog-v3.json`
