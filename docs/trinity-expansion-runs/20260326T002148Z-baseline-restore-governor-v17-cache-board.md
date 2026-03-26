# Trinity Expansion Result: baseline_restore_governor_v17_cache_board

- generated_utc: `2026-03-26T00:21:48+00:00`
- pillar: `trinity`
- overall_status: **PASS**
- effective_success: `True`

## Checks
| name | status | detail |
|---|---|---|
| cache_present | PASS | docs/trinity-mcp-cache/baseline-restore-governor-v17-latest.json |
| cache_schema_present | PASS | docs/trinity-mcp-cache-schema-v3.json |
| cache_required_fields | PASS | missing=[] |
| cache_record_count | PASS | records=2 |
| cache_freshness | PASS | age_days=0.0 |
| cache_integration_id | PASS | integration_id=baseline_restore_governor_v17 |

## Metrics
```json
{
  "age_days": 0.0,
  "freshness_window_days": 30.0,
  "pack": "baseline_restore_governor_v17",
  "record_count": 2
}
```

## Repo targets touched
- `docs/system-suite-status.json`
- `docs/trinity-mcp-cache-schema-v3.json`
- `docs/trinity-mcp-cache/baseline-restore-governor-v17-latest.json`
- `docs/v17-baseline-state-v1.json`
- `docs/v17-system-suite-status-latest.json`
