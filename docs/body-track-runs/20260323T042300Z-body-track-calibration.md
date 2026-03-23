# Body Profile Calibration Report

- generated_utc: `2026-03-23T04:23:00+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `273`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.582 | 0.571 | loosen_duration+tighten_health | noisy |
| standard | 0.582 | 0.571 | loosen_duration+tighten_health | noisy |
| strict | 0.861 | 0.857 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315018`
- observed_false_regression_rate: `0.307692`
```json
{
  "duration_drift_p90": 1.281281,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.708 | 0.686 | noisy |
| 3 | 1 | 0.221 | 0.214 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.859 | 0.822 | noisy |
| 5 | 1 | 0.539 | 0.524 | noisy |
| 5 | 2 | 0.167 | 0.167 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.903 | 0.850 | noisy |
| 7 | 1 | 0.745 | 0.723 | noisy |
| 7 | 2 | 0.431 | 0.427 | noisy |
| 7 | 3 | 0.131 | 0.131 | acceptable |
| 9 | 0 | 0.925 | 0.857 | noisy |
| 9 | 1 | 0.849 | 0.819 | noisy |
| 9 | 2 | 0.623 | 0.611 | noisy |
| 9 | 3 | 0.347 | 0.347 | noisy |

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
