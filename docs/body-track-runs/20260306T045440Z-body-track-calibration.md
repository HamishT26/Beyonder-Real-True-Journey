# Body Profile Calibration Report

- generated_utc: `2026-03-06T04:54:40+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `61`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.197 | 0.093 | loosen_duration+loosen_health | acceptable |
| standard | 0.197 | 0.093 | loosen_duration+loosen_health | acceptable |
| strict | 0.492 | 0.426 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.180328`
- observed_false_regression_rate: `0.147541`
```json
{
  "duration_drift_p90": 0.294185,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.390 | 0.288 | noisy |
| 3 | 1 | 0.136 | 0.102 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.509 | 0.333 | noisy |
| 5 | 1 | 0.263 | 0.193 | noisy |
| 5 | 2 | 0.105 | 0.105 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.564 | 0.309 | noisy |
| 7 | 1 | 0.364 | 0.255 | noisy |
| 7 | 2 | 0.200 | 0.182 | noisy |
| 7 | 3 | 0.073 | 0.073 | acceptable |
| 9 | 0 | 0.623 | 0.283 | noisy |
| 9 | 1 | 0.415 | 0.264 | noisy |
| 9 | 2 | 0.264 | 0.208 | noisy |
| 9 | 3 | 0.151 | 0.151 | noisy |

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
