# Trinity Expansion Result: uat_preprod_fabric_cache_board

- generated_utc: `2026-03-16T00:21:36+00:00`
- pillar: `body`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| cache_present | PASS | docs/trinity-mcp-cache/uat-preprod-fabric-latest.json |
| cache_schema_present | PASS | docs/trinity-mcp-cache-schema-v3.json |
| cache_required_fields | PASS | missing=[] |
| cache_record_count | PASS | records=2 |
| cache_freshness | PASS | age_days=0.0 |
| cache_integration_id | PASS | integration_id=uat_preprod_fabric |

## Metrics
```json
{
  "age_days": 0.0,
  "freshness_window_days": 30.0,
  "pack": "uat_preprod_fabric",
  "record_count": 2
}
```

## Repo targets touched
- `docs/trinity-materialization-ladder-v1.json`
- `docs/trinity-mcp-cache-schema-v3.json`
- `docs/trinity-mcp-cache/uat-preprod-fabric-latest.json`
- `docs/trinity-uat-preprod-targets-v1.json`
