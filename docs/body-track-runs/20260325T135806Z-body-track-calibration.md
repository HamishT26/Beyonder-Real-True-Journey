# Body Profile Calibration Report

- generated_utc: `2026-03-25T13:58:06+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `304`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.615 | 0.606 | loosen_duration+tighten_health | noisy |
| standard | 0.615 | 0.606 | loosen_duration+tighten_health | noisy |
| strict | 0.875 | 0.872 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315789`
- observed_false_regression_rate: `0.309211`
```json
{
  "duration_drift_p90": 1.284848,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.715 | 0.695 | noisy |
| 3 | 1 | 0.219 | 0.212 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.863 | 0.830 | noisy |
| 5 | 1 | 0.537 | 0.523 | noisy |
| 5 | 2 | 0.167 | 0.167 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.909 | 0.862 | noisy |
| 7 | 1 | 0.738 | 0.718 | noisy |
| 7 | 2 | 0.430 | 0.426 | noisy |
| 7 | 3 | 0.131 | 0.131 | acceptable |
| 9 | 0 | 0.932 | 0.872 | noisy |
| 9 | 1 | 0.848 | 0.821 | noisy |
| 9 | 2 | 0.622 | 0.611 | noisy |
| 9 | 3 | 0.348 | 0.348 | noisy |

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
