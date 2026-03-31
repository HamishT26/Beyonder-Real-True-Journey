# Body Profile Calibration Report

- generated_utc: `2026-03-31T02:32:32+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `339`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.637 | 0.630 | loosen_duration+tighten_health | noisy |
| standard | 0.637 | 0.630 | loosen_duration+tighten_health | noisy |
| strict | 0.888 | 0.886 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.330383`
- observed_false_regression_rate: `0.324484`
```json
{
  "duration_drift_p90": 1.578447,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.739 | 0.721 | noisy |
| 3 | 1 | 0.240 | 0.234 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.878 | 0.848 | noisy |
| 5 | 1 | 0.579 | 0.567 | noisy |
| 5 | 2 | 0.191 | 0.191 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.919 | 0.877 | noisy |
| 7 | 1 | 0.766 | 0.748 | noisy |
| 7 | 2 | 0.477 | 0.474 | noisy |
| 7 | 3 | 0.150 | 0.150 | noisy |
| 9 | 0 | 0.940 | 0.885 | noisy |
| 9 | 1 | 0.864 | 0.840 | noisy |
| 9 | 2 | 0.659 | 0.650 | noisy |
| 9 | 3 | 0.396 | 0.396 | noisy |

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
