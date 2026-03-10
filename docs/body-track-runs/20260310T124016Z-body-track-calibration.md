# Body Profile Calibration Report

- generated_utc: `2026-03-10T12:40:16+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `135`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.333 | 0.297 | loosen_duration+loosen_health | noisy |
| standard | 0.333 | 0.297 | loosen_duration+loosen_health | noisy |
| strict | 0.726 | 0.711 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.266667`
- observed_false_regression_rate: `0.251852`
```json
{
  "duration_drift_p90": 1.001076,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.624 | 0.579 | noisy |
| 3 | 1 | 0.180 | 0.165 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.771 | 0.695 | noisy |
| 5 | 1 | 0.443 | 0.412 | noisy |
| 5 | 2 | 0.137 | 0.137 | acceptable |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.814 | 0.705 | noisy |
| 7 | 1 | 0.628 | 0.581 | noisy |
| 7 | 2 | 0.349 | 0.341 | noisy |
| 7 | 3 | 0.109 | 0.109 | acceptable |
| 9 | 0 | 0.843 | 0.701 | noisy |
| 9 | 1 | 0.724 | 0.661 | noisy |
| 9 | 2 | 0.504 | 0.480 | noisy |
| 9 | 3 | 0.307 | 0.307 | noisy |

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
