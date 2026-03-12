# Body Profile Calibration Report

- generated_utc: `2026-03-12T12:13:50+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `164`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.366 | 0.338 | loosen_duration+tighten_health | noisy |
| standard | 0.366 | 0.338 | loosen_duration+tighten_health | noisy |
| strict | 0.768 | 0.758 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.268293`
- observed_false_regression_rate: `0.256098`
```json
{
  "duration_drift_p90": 1.003021,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.636 | 0.599 | noisy |
| 3 | 1 | 0.167 | 0.154 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.787 | 0.725 | noisy |
| 5 | 1 | 0.431 | 0.406 | noisy |
| 5 | 2 | 0.119 | 0.119 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.842 | 0.753 | noisy |
| 7 | 1 | 0.639 | 0.601 | noisy |
| 7 | 2 | 0.316 | 0.310 | noisy |
| 7 | 3 | 0.089 | 0.089 | acceptable |
| 9 | 0 | 0.872 | 0.756 | noisy |
| 9 | 1 | 0.756 | 0.705 | noisy |
| 9 | 2 | 0.494 | 0.474 | noisy |
| 9 | 3 | 0.263 | 0.263 | noisy |

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
