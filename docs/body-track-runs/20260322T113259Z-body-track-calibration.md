# Body Profile Calibration Report

- generated_utc: `2026-03-22T11:32:59+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `245`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.539 | 0.525 | loosen_duration+tighten_health | noisy |
| standard | 0.539 | 0.525 | loosen_duration+tighten_health | noisy |
| strict | 0.845 | 0.840 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.314286`
- observed_false_regression_rate: `0.306122`
```json
{
  "duration_drift_p90": 1.26871,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.704 | 0.679 | noisy |
| 3 | 1 | 0.226 | 0.218 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.842 | 0.801 | noisy |
| 5 | 1 | 0.552 | 0.535 | noisy |
| 5 | 2 | 0.166 | 0.166 | noisy |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.891 | 0.833 | noisy |
| 7 | 1 | 0.736 | 0.711 | noisy |
| 7 | 2 | 0.439 | 0.435 | noisy |
| 7 | 3 | 0.130 | 0.130 | acceptable |
| 9 | 0 | 0.916 | 0.840 | noisy |
| 9 | 1 | 0.835 | 0.802 | noisy |
| 9 | 2 | 0.616 | 0.603 | noisy |
| 9 | 3 | 0.354 | 0.354 | noisy |

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
