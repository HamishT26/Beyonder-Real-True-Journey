# Trinity Expansion Result: public_web_weaver_cache_board

- generated_utc: `2026-03-31T00:44:31+00:00`
- pillar: `mind`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| cache_present | PASS | docs/trinity-mcp-cache/public-web-weaver-latest.json |
| cache_schema_present | PASS | docs/trinity-mcp-cache-schema-v3.json |
| cache_required_fields | PASS | missing=[] |
| cache_record_count | PASS | records=5 |
| cache_freshness | PASS | age_days=0.0 |
| cache_integration_id | PASS | integration_id=public_web_weaver |

## Metrics
```json
{
  "age_days": 0.0,
  "freshness_window_days": 30.0,
  "pack": "public_web_weaver",
  "record_count": 5
}
```

## Repo targets touched
- `docs/trinity-benchmark-registry-v1.json`
- `docs/trinity-mcp-cache-schema-v3.json`
- `docs/trinity-mcp-cache/public-web-weaver-latest.json`
- `docs/trinity-public-source-registry-v1.json`
