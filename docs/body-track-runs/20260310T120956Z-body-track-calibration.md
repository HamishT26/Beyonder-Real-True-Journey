# Body Profile Calibration Report

- generated_utc: `2026-03-10T12:09:56+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `131`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.336 | 0.298 | loosen_duration+loosen_health | noisy |
| standard | 0.336 | 0.298 | loosen_duration+loosen_health | noisy |
| strict | 0.718 | 0.702 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.267176`
- observed_false_regression_rate: `0.251908`
```json
{
  "duration_drift_p90": 1.01053,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.620 | 0.574 | noisy |
| 3 | 1 | 0.171 | 0.155 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.764 | 0.685 | noisy |
| 5 | 1 | 0.425 | 0.394 | noisy |
| 5 | 2 | 0.134 | 0.134 | acceptable |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.808 | 0.696 | noisy |
| 7 | 1 | 0.616 | 0.568 | noisy |
| 7 | 2 | 0.336 | 0.328 | noisy |
| 7 | 3 | 0.112 | 0.112 | acceptable |
| 9 | 0 | 0.837 | 0.691 | noisy |
| 9 | 1 | 0.715 | 0.650 | noisy |
| 9 | 2 | 0.488 | 0.463 | noisy |
| 9 | 3 | 0.301 | 0.301 | noisy |

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
