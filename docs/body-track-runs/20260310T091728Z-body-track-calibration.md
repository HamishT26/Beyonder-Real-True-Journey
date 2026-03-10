# Body Profile Calibration Report

- generated_utc: `2026-03-10T09:17:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `125`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.344 | 0.305 | loosen_duration+loosen_health | noisy |
| standard | 0.344 | 0.305 | loosen_duration+loosen_health | noisy |
| strict | 0.712 | 0.695 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.264`
- observed_false_regression_rate: `0.248`
```json
{
  "duration_drift_p90": 1.001076,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.602 | 0.553 | noisy |
| 3 | 1 | 0.179 | 0.163 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.752 | 0.669 | noisy |
| 5 | 1 | 0.405 | 0.372 | noisy |
| 5 | 2 | 0.140 | 0.140 | acceptable |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.798 | 0.681 | noisy |
| 7 | 1 | 0.597 | 0.546 | noisy |
| 7 | 2 | 0.328 | 0.319 | noisy |
| 7 | 3 | 0.118 | 0.118 | acceptable |
| 9 | 0 | 0.829 | 0.675 | noisy |
| 9 | 1 | 0.701 | 0.632 | noisy |
| 9 | 2 | 0.462 | 0.436 | noisy |
| 9 | 3 | 0.308 | 0.308 | noisy |

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
