# Body Profile Calibration Report

- generated_utc: `2026-03-26T02:53:50+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `327`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.636 | 0.628 | loosen_duration+tighten_health | noisy |
| standard | 0.636 | 0.628 | loosen_duration+tighten_health | noisy |
| strict | 0.884 | 0.881 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.327217`
- observed_false_regression_rate: `0.321101`
```json
{
  "duration_drift_p90": 1.589223,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.729 | 0.711 | noisy |
| 3 | 1 | 0.234 | 0.228 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.873 | 0.842 | noisy |
| 5 | 1 | 0.567 | 0.554 | noisy |
| 5 | 2 | 0.186 | 0.186 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.916 | 0.872 | noisy |
| 7 | 1 | 0.757 | 0.738 | noisy |
| 7 | 2 | 0.461 | 0.458 | noisy |
| 7 | 3 | 0.143 | 0.143 | acceptable |
| 9 | 0 | 0.937 | 0.881 | noisy |
| 9 | 1 | 0.859 | 0.834 | noisy |
| 9 | 2 | 0.646 | 0.636 | noisy |
| 9 | 3 | 0.376 | 0.376 | noisy |

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
