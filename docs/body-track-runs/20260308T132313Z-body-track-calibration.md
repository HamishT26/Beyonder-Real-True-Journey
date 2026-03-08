# Body Profile Calibration Report

- generated_utc: `2026-03-08T13:23:13+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `105`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.286 | 0.235 | loosen_duration+loosen_health | noisy |
| standard | 0.286 | 0.235 | loosen_duration+loosen_health | noisy |
| strict | 0.667 | 0.643 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.238095`
- observed_false_regression_rate: `0.219048`
```json
{
  "duration_drift_p90": 0.808161,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.534 | 0.476 | noisy |
| 3 | 1 | 0.155 | 0.136 | acceptable |
| 3 | 2 | 0.010 | 0.010 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.703 | 0.604 | noisy |
| 5 | 1 | 0.317 | 0.277 | noisy |
| 5 | 2 | 0.129 | 0.129 | acceptable |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.758 | 0.616 | noisy |
| 7 | 1 | 0.515 | 0.455 | noisy |
| 7 | 2 | 0.232 | 0.222 | noisy |
| 7 | 3 | 0.111 | 0.111 | acceptable |
| 9 | 0 | 0.794 | 0.608 | noisy |
| 9 | 1 | 0.639 | 0.557 | noisy |
| 9 | 2 | 0.351 | 0.320 | noisy |
| 9 | 3 | 0.206 | 0.206 | noisy |

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
