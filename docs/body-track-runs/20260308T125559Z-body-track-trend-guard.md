# Body Benchmark Trend Guard Report

- generated_utc: `2026-03-08T12:55:59+00:00`
- overall_status: **WARN**
- trend_profile: `standard`
- trend_classification: `regression_pressure`
- window_size_used: `5`

## Thresholds
```json
{
  "window_size": 5.0,
  "max_regressions": 2.0,
  "max_duration_drift": 1.0,
  "max_health_drop": 2.0
}
```

## Checks
| check | status | detail |
|---|---|---|
| latest_benchmark_status | WARN | status=WARN |
| history_window_available | PASS | window_len=5 |
| regression_count_window | WARN | regressions=4, max=2 |
| duration_drift_window | WARN | drift=2.103996, max=1.0, effective_max=1.02 |
| health_drop_window | PASS | drop=0.000000, max=2.0 |
