# Body Profile Calibration Report

- generated_utc: `2026-03-22T10:47:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `244`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.537 | 0.523 | loosen_duration+tighten_health | noisy |
| standard | 0.537 | 0.523 | loosen_duration+tighten_health | noisy |
| strict | 0.844 | 0.840 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.311475`
- observed_false_regression_rate: `0.303279`
```json
{
  "duration_drift_p90": 1.223103,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.702 | 0.678 | noisy |
| 3 | 1 | 0.227 | 0.219 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.842 | 0.800 | noisy |
| 5 | 1 | 0.550 | 0.533 | noisy |
| 5 | 2 | 0.167 | 0.167 | noisy |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.891 | 0.832 | noisy |
| 7 | 1 | 0.735 | 0.710 | noisy |
| 7 | 2 | 0.437 | 0.433 | noisy |
| 7 | 3 | 0.130 | 0.130 | acceptable |
| 9 | 0 | 0.915 | 0.839 | noisy |
| 9 | 1 | 0.835 | 0.801 | noisy |
| 9 | 2 | 0.614 | 0.602 | noisy |
| 9 | 3 | 0.356 | 0.356 | noisy |

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
