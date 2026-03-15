# Body Profile Calibration Report

- generated_utc: `2026-03-14T10:01:08+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `174`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.397 | 0.371 | loosen_duration+tighten_health | noisy |
| standard | 0.397 | 0.371 | loosen_duration+tighten_health | noisy |
| strict | 0.782 | 0.772 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.281609`
- observed_false_regression_rate: `0.270115`
```json
{
  "duration_drift_p90": 1.09129,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.657 | 0.622 | noisy |
| 3 | 1 | 0.180 | 0.169 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.800 | 0.741 | noisy |
| 5 | 1 | 0.465 | 0.441 | noisy |
| 5 | 2 | 0.135 | 0.135 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.851 | 0.768 | noisy |
| 7 | 1 | 0.661 | 0.625 | noisy |
| 7 | 2 | 0.351 | 0.345 | noisy |
| 7 | 3 | 0.107 | 0.107 | acceptable |
| 9 | 0 | 0.880 | 0.771 | noisy |
| 9 | 1 | 0.771 | 0.723 | noisy |
| 9 | 2 | 0.518 | 0.500 | noisy |
| 9 | 3 | 0.295 | 0.295 | noisy |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 3
  }
}
```
