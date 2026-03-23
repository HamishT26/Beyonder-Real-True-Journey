# Body Profile Calibration Report

- generated_utc: `2026-03-23T04:53:31+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `276`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.580 | 0.569 | loosen_duration+tighten_health | noisy |
| standard | 0.580 | 0.569 | loosen_duration+tighten_health | noisy |
| strict | 0.862 | 0.859 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.311594`
- observed_false_regression_rate: `0.304348`
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
| 3 | 1 | 0.219 | 0.212 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.860 | 0.824 | noisy |
| 5 | 1 | 0.533 | 0.518 | noisy |
| 5 | 2 | 0.165 | 0.165 | noisy |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.904 | 0.852 | noisy |
| 7 | 1 | 0.741 | 0.719 | noisy |
| 7 | 2 | 0.426 | 0.422 | noisy |
| 7 | 3 | 0.130 | 0.130 | acceptable |
| 9 | 0 | 0.925 | 0.858 | noisy |
| 9 | 1 | 0.851 | 0.821 | noisy |
| 9 | 2 | 0.623 | 0.612 | noisy |
| 9 | 3 | 0.343 | 0.343 | noisy |

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
