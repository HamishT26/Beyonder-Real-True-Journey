# Body Benchmark Trend Guard Report

- generated_utc: `2026-03-06T04:58:22+00:00`
- overall_status: **PASS**
- trend_profile: `standard`
- trend_classification: `stable_or_improving`
- window_size_used: `5`

## Thresholds
```json
{
  "window_size": 5.0,
  "max_regressions": 2.0,
  "max_duration_drift": 0.2,
  "max_health_drop": 2.0
}
```

## Checks
| check | status | detail |
|---|---|---|
| latest_benchmark_status | PASS | status=PASS |
| history_window_available | PASS | window_len=5 |
| regression_count_window | PASS | regressions=3, max=2; latest duration/health remain within tolerance |
| duration_drift_window | PASS | drift=0.045985, max=0.2 |
| health_drop_window | PASS | drop=0.000000, max=2.0 |
