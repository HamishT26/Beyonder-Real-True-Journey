# Body Benchmark Trend Guard Report

- generated_utc: `2026-03-20T23:01:07+00:00`
- overall_status: **PASS**
- trend_profile: `quick`
- trend_classification: `stable_or_improving`
- window_size_used: `3`

## Thresholds
```json
{
  "window_size": 3.0,
  "max_regressions": 1.0,
  "max_duration_drift": 0.25,
  "max_health_drop": 2.5
}
```

## Checks
| check | status | detail |
|---|---|---|
| latest_benchmark_status | PASS | status=PASS |
| history_window_available | PASS | window_len=3 |
| regression_count_window | PASS | regressions=2, max=1; latest duration/health remain within tolerance |
| duration_drift_window | PASS | drift=-0.955438, max=0.25, effective_max=0.27 |
| health_drop_window | PASS | drop=0.000000, max=2.5 |
