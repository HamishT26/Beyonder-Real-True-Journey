# Body Profile Calibration Report

- generated_utc: `2026-03-21T04:26:21+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `233`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.519 | 0.504 | loosen_duration+tighten_health | noisy |
| standard | 0.519 | 0.504 | loosen_duration+tighten_health | noisy |
| strict | 0.837 | 0.832 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.309013`
- observed_false_regression_rate: `0.300429`
```json
{
  "duration_drift_p90": 1.116625,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.697 | 0.671 | noisy |
| 3 | 1 | 0.216 | 0.208 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.834 | 0.790 | noisy |
| 5 | 1 | 0.533 | 0.515 | noisy |
| 5 | 2 | 0.166 | 0.166 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.885 | 0.824 | noisy |
| 7 | 1 | 0.722 | 0.696 | noisy |
| 7 | 2 | 0.419 | 0.414 | noisy |
| 7 | 3 | 0.137 | 0.137 | acceptable |
| 9 | 0 | 0.911 | 0.831 | noisy |
| 9 | 1 | 0.827 | 0.791 | noisy |
| 9 | 2 | 0.596 | 0.582 | noisy |
| 9 | 3 | 0.342 | 0.342 | noisy |

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
