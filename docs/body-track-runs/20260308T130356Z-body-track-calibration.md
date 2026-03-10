# Body Profile Calibration Report

- generated_utc: `2026-03-08T13:03:56+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `101`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.257 | 0.202 | loosen_duration+loosen_health | noisy |
| standard | 0.257 | 0.202 | loosen_duration+loosen_health | noisy |
| strict | 0.653 | 0.628 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.227723`
- observed_false_regression_rate: `0.207921`
```json
{
  "duration_drift_p90": 0.74468,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.515 | 0.455 | noisy |
| 3 | 1 | 0.152 | 0.131 | acceptable |
| 3 | 2 | 0.010 | 0.010 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.691 | 0.588 | noisy |
| 5 | 1 | 0.289 | 0.247 | noisy |
| 5 | 2 | 0.124 | 0.124 | acceptable |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.747 | 0.600 | noisy |
| 7 | 1 | 0.495 | 0.432 | noisy |
| 7 | 2 | 0.200 | 0.189 | noisy |
| 7 | 3 | 0.095 | 0.095 | acceptable |
| 9 | 0 | 0.785 | 0.591 | noisy |
| 9 | 1 | 0.624 | 0.538 | noisy |
| 9 | 2 | 0.323 | 0.290 | noisy |
| 9 | 3 | 0.172 | 0.172 | noisy |

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
