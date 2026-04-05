# Body Benchmark Trend Guard Report

- generated_utc: `2026-04-05T15:06:19+00:00`
- overall_status: **PASS**
- trend_profile: `standard`
- trend_classification: `stable_or_improving`
- window_size_used: `3`

## Thresholds
```json
{
  "window_size": 3.0,
  "max_regressions": 3.0,
  "max_duration_drift": 6.0,
  "max_health_drop": 2.0
}
```

## Checks
| check | status | detail |
|---|---|---|
| latest_benchmark_status | PASS | status=PASS |
| history_window_available | PASS | window_len=3 |
| regression_count_window | PASS | regressions=1, max=3 |
| duration_drift_window | PASS | drift=-0.240456, max=6.0, effective_max=6.02 |
| health_drop_window | PASS | drop=0.000000, max=2.0 |
