# Body Profile Calibration Report

- generated_utc: `2026-03-22T13:19:03+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `251`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.550 | 0.537 | loosen_duration+tighten_health | noisy |
| standard | 0.550 | 0.537 | loosen_duration+tighten_health | noisy |
| strict | 0.849 | 0.844 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.310757`
- observed_false_regression_rate: `0.302789`
```json
{
  "duration_drift_p90": 1.315038,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.707 | 0.683 | noisy |
| 3 | 1 | 0.221 | 0.213 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.846 | 0.806 | noisy |
| 5 | 1 | 0.543 | 0.526 | noisy |
| 5 | 2 | 0.162 | 0.162 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.894 | 0.837 | noisy |
| 7 | 1 | 0.739 | 0.714 | noisy |
| 7 | 2 | 0.433 | 0.429 | noisy |
| 7 | 3 | 0.127 | 0.127 | acceptable |
| 9 | 0 | 0.918 | 0.844 | noisy |
| 9 | 1 | 0.840 | 0.807 | noisy |
| 9 | 2 | 0.617 | 0.605 | noisy |
| 9 | 3 | 0.346 | 0.346 | noisy |

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
