# Body Profile Calibration Report

- generated_utc: `2026-03-06T04:51:18+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `58`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.207 | 0.098 | loosen_duration+loosen_health | acceptable |
| standard | 0.207 | 0.098 | loosen_duration+loosen_health | acceptable |
| strict | 0.500 | 0.431 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.172414`
- observed_false_regression_rate: `0.137931`
```json
{
  "duration_drift_p90": 0.294681,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.357 | 0.250 | noisy |
| 3 | 1 | 0.125 | 0.089 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.481 | 0.296 | noisy |
| 5 | 1 | 0.222 | 0.148 | acceptable |
| 5 | 2 | 0.074 | 0.074 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.538 | 0.269 | noisy |
| 7 | 1 | 0.327 | 0.212 | noisy |
| 7 | 2 | 0.154 | 0.135 | acceptable |
| 7 | 3 | 0.058 | 0.058 | acceptable |
| 9 | 0 | 0.600 | 0.240 | noisy |
| 9 | 1 | 0.380 | 0.220 | noisy |
| 9 | 2 | 0.220 | 0.160 | noisy |
| 9 | 3 | 0.100 | 0.100 | acceptable |

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
