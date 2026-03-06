# Body Profile Calibration Report

- generated_utc: `2026-03-06T04:58:38+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `62`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.194 | 0.091 | loosen_duration+loosen_health | acceptable |
| standard | 0.194 | 0.091 | loosen_duration+loosen_health | acceptable |
| strict | 0.500 | 0.436 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.177419`
- observed_false_regression_rate: `0.145161`
```json
{
  "duration_drift_p90": 0.2907,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.400 | 0.300 | noisy |
| 3 | 1 | 0.133 | 0.100 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.517 | 0.345 | noisy |
| 5 | 1 | 0.276 | 0.207 | noisy |
| 5 | 2 | 0.103 | 0.103 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.571 | 0.321 | noisy |
| 7 | 1 | 0.375 | 0.268 | noisy |
| 7 | 2 | 0.214 | 0.196 | noisy |
| 7 | 3 | 0.071 | 0.071 | acceptable |
| 9 | 0 | 0.630 | 0.296 | noisy |
| 9 | 1 | 0.426 | 0.278 | noisy |
| 9 | 2 | 0.278 | 0.222 | noisy |
| 9 | 3 | 0.167 | 0.167 | noisy |

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
