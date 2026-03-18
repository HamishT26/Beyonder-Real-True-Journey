# Body Profile Calibration Report

- generated_utc: `2026-03-18T00:22:50+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `206`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.466 | 0.447 | loosen_duration+tighten_health | noisy |
| standard | 0.466 | 0.447 | loosen_duration+tighten_health | noisy |
| strict | 0.816 | 0.809 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.286408`
- observed_false_regression_rate: `0.276699`
```json
{
  "duration_drift_p90": 1.112642,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.662 | 0.632 | noisy |
| 3 | 1 | 0.191 | 0.181 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.812 | 0.762 | noisy |
| 5 | 1 | 0.485 | 0.465 | noisy |
| 5 | 2 | 0.134 | 0.134 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.870 | 0.800 | noisy |
| 7 | 1 | 0.685 | 0.655 | noisy |
| 7 | 2 | 0.360 | 0.355 | noisy |
| 7 | 3 | 0.100 | 0.100 | acceptable |
| 9 | 0 | 0.899 | 0.808 | noisy |
| 9 | 1 | 0.803 | 0.763 | noisy |
| 9 | 2 | 0.551 | 0.535 | noisy |
| 9 | 3 | 0.288 | 0.288 | noisy |

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
