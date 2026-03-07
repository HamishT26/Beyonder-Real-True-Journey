# Body Profile Calibration Report

- generated_utc: `2026-03-07T08:16:47+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `91`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.198 | 0.131 | loosen_duration+loosen_health | acceptable |
| standard | 0.198 | 0.131 | loosen_duration+loosen_health | acceptable |
| strict | 0.615 | 0.583 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.186813`
- observed_false_regression_rate: `0.164835`
```json
{
  "duration_drift_p90": 0.376972,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.472 | 0.404 | noisy |
| 3 | 1 | 0.101 | 0.079 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.655 | 0.540 | noisy |
| 5 | 1 | 0.241 | 0.195 | noisy |
| 5 | 2 | 0.069 | 0.069 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.718 | 0.553 | noisy |
| 7 | 1 | 0.447 | 0.376 | noisy |
| 7 | 2 | 0.153 | 0.141 | acceptable |
| 7 | 3 | 0.047 | 0.047 | acceptable |
| 9 | 0 | 0.759 | 0.542 | noisy |
| 9 | 1 | 0.578 | 0.482 | noisy |
| 9 | 2 | 0.265 | 0.229 | noisy |
| 9 | 3 | 0.120 | 0.120 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 2
  }
}
```
