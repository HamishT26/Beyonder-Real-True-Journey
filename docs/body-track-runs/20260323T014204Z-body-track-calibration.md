# Body Profile Calibration Report

- generated_utc: `2026-03-23T01:42:04+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `266`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.575 | 0.564 | loosen_duration+tighten_health | noisy |
| standard | 0.575 | 0.564 | loosen_duration+tighten_health | noisy |
| strict | 0.857 | 0.853 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.31203`
- observed_false_regression_rate: `0.304511`
```json
{
  "duration_drift_p90": 1.262424,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.708 | 0.686 | noisy |
| 3 | 1 | 0.220 | 0.212 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.855 | 0.817 | noisy |
| 5 | 1 | 0.538 | 0.523 | noisy |
| 5 | 2 | 0.172 | 0.172 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.900 | 0.846 | noisy |
| 7 | 1 | 0.738 | 0.715 | noisy |
| 7 | 2 | 0.435 | 0.431 | noisy |
| 7 | 3 | 0.135 | 0.135 | acceptable |
| 9 | 0 | 0.922 | 0.853 | noisy |
| 9 | 1 | 0.845 | 0.814 | noisy |
| 9 | 2 | 0.624 | 0.612 | noisy |
| 9 | 3 | 0.357 | 0.357 | noisy |

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
