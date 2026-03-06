# Body Benchmark Trend Guard Report

- generated_utc: `2026-03-06T04:54:40+00:00`
- overall_status: **WARN**
- trend_profile: `standard`
- trend_classification: `watch`
- window_size_used: `3`

## Thresholds
```json
{
  "window_size": 3.0,
  "max_regressions": 2.0,
  "max_duration_drift": 0.2,
  "max_health_drop": 2.0
}
```

## Checks
| check | status | detail |
|---|---|---|
| latest_benchmark_status | PASS | status=PASS |
| history_window_available | PASS | window_len=3 |
| regression_count_window | PASS | regressions=1, max=2 |
| duration_drift_window | WARN | drift=0.238186, max=0.2 |
| health_drop_window | PASS | drop=0.000000, max=2.0 |
