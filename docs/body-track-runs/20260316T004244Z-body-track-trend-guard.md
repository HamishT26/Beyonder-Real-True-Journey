# Body Benchmark Trend Guard Report

- generated_utc: `2026-03-16T00:42:44+00:00`
- overall_status: **WARN**
- trend_profile: `standard`
- trend_classification: `watch`
- window_size_used: `5`

## Thresholds
```json
{
  "window_size": 5.0,
  "max_regressions": 3.0,
  "max_duration_drift": 6.0,
  "max_health_drop": 2.0
}
```

## Checks
| check | status | detail |
|---|---|---|
| latest_benchmark_status | WARN | status=WARN |
| history_window_available | PASS | window_len=5 |
| regression_count_window | PASS | regressions=3, max=3 |
| duration_drift_window | WARN | drift=9.469427, max=6.0, effective_max=6.02 |
| health_drop_window | PASS | drop=0.000000, max=2.0 |
