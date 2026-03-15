# Body Profile Calibration Report

- generated_utc: `2026-03-14T07:54:53+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `169`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.379 | 0.352 | loosen_duration+tighten_health | noisy |
| standard | 0.379 | 0.352 | loosen_duration+tighten_health | noisy |
| strict | 0.775 | 0.765 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.278107`
- observed_false_regression_rate: `0.266272`
```json
{
  "duration_drift_p90": 1.102724,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.647 | 0.611 | noisy |
| 3 | 1 | 0.180 | 0.168 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.794 | 0.733 | noisy |
| 5 | 1 | 0.448 | 0.424 | noisy |
| 5 | 2 | 0.127 | 0.127 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.847 | 0.761 | noisy |
| 7 | 1 | 0.650 | 0.613 | noisy |
| 7 | 2 | 0.331 | 0.325 | noisy |
| 7 | 3 | 0.098 | 0.098 | acceptable |
| 9 | 0 | 0.876 | 0.764 | noisy |
| 9 | 1 | 0.764 | 0.714 | noisy |
| 9 | 2 | 0.503 | 0.484 | noisy |
| 9 | 3 | 0.273 | 0.273 | noisy |

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
