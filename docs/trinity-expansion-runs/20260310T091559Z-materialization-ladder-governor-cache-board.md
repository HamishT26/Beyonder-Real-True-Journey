# Trinity Expansion Result: materialization_ladder_governor_cache_board

- generated_utc: `2026-03-10T09:15:59+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| cache_present | PASS | docs/trinity-mcp-cache/materialization-ladder-governor-latest.json |
| cache_schema_present | PASS | docs/trinity-mcp-cache-schema-v3.json |
| cache_required_fields | PASS | missing=[] |
| cache_record_count | PASS | records=6 |
| cache_freshness | PASS | age_days=0.0 |
| cache_integration_id | PASS | integration_id=materialization_ladder_governor |

## Metrics
```json
{
  "age_days": 0.0,
  "freshness_window_days": 30.0,
  "pack": "materialization_ladder_governor",
  "record_count": 6
}
```

## Repo targets touched
- `docs/trinity-materialization-ladder-board-latest.json`
- `docs/trinity-materialization-ladder-v1.json`
- `docs/trinity-mcp-cache-schema-v3.json`
- `docs/trinity-mcp-cache/materialization-ladder-governor-latest.json`
