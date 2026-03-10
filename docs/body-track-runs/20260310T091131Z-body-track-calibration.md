# Body Profile Calibration Report

- generated_utc: `2026-03-10T09:11:31+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `124`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.347 | 0.308 | loosen_duration+loosen_health | noisy |
| standard | 0.347 | 0.308 | loosen_duration+loosen_health | noisy |
| strict | 0.710 | 0.692 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.258065`
- observed_false_regression_rate: `0.241935`
```json
{
  "duration_drift_p90": 1.003021,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.598 | 0.549 | noisy |
| 3 | 1 | 0.172 | 0.156 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.750 | 0.667 | noisy |
| 5 | 1 | 0.400 | 0.367 | noisy |
| 5 | 2 | 0.142 | 0.142 | acceptable |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.797 | 0.678 | noisy |
| 7 | 1 | 0.593 | 0.542 | noisy |
| 7 | 2 | 0.322 | 0.314 | noisy |
| 7 | 3 | 0.119 | 0.119 | acceptable |
| 9 | 0 | 0.828 | 0.672 | noisy |
| 9 | 1 | 0.698 | 0.629 | noisy |
| 9 | 2 | 0.457 | 0.431 | noisy |
| 9 | 3 | 0.302 | 0.302 | noisy |

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
