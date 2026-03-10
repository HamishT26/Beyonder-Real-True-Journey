# Body Profile Calibration Report

- generated_utc: `2026-03-10T11:52:45+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `129`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.341 | 0.303 | loosen_duration+loosen_health | noisy |
| standard | 0.341 | 0.303 | loosen_duration+loosen_health | noisy |
| strict | 0.721 | 0.705 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.263566`
- observed_false_regression_rate: `0.248062`
```json
{
  "duration_drift_p90": 1.01777,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.614 | 0.567 | noisy |
| 3 | 1 | 0.173 | 0.157 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.760 | 0.680 | noisy |
| 5 | 1 | 0.424 | 0.392 | noisy |
| 5 | 2 | 0.136 | 0.136 | acceptable |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.805 | 0.691 | noisy |
| 7 | 1 | 0.610 | 0.561 | noisy |
| 7 | 2 | 0.333 | 0.325 | noisy |
| 7 | 3 | 0.114 | 0.114 | acceptable |
| 9 | 0 | 0.835 | 0.686 | noisy |
| 9 | 1 | 0.711 | 0.645 | noisy |
| 9 | 2 | 0.479 | 0.455 | noisy |
| 9 | 3 | 0.298 | 0.298 | noisy |

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
