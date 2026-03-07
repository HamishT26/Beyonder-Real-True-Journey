# Body Profile Calibration Report

- generated_utc: `2026-03-07T02:29:00+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `80`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.212 | 0.137 | loosen_duration+loosen_health | acceptable |
| standard | 0.212 | 0.137 | loosen_duration+loosen_health | acceptable |
| strict | 0.575 | 0.534 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.1875`
- observed_false_regression_rate: `0.1625`
```json
{
  "duration_drift_p90": 0.402223,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.436 | 0.359 | noisy |
| 3 | 1 | 0.115 | 0.090 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.605 | 0.474 | noisy |
| 5 | 1 | 0.224 | 0.171 | noisy |
| 5 | 2 | 0.079 | 0.079 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.676 | 0.486 | noisy |
| 7 | 1 | 0.378 | 0.297 | noisy |
| 7 | 2 | 0.176 | 0.162 | noisy |
| 7 | 3 | 0.054 | 0.054 | acceptable |
| 9 | 0 | 0.722 | 0.472 | noisy |
| 9 | 1 | 0.514 | 0.403 | noisy |
| 9 | 2 | 0.264 | 0.222 | noisy |
| 9 | 3 | 0.139 | 0.139 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 2
  }
}
```
