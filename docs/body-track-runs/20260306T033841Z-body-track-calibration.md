# Body Profile Calibration Report

- generated_utc: `2026-03-06T03:38:41+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `55`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.218 | 0.104 | loosen_duration+loosen_health | acceptable |
| standard | 0.218 | 0.104 | loosen_duration+loosen_health | acceptable |
| strict | 0.491 | 0.417 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.145455`
- observed_false_regression_rate: `0.109091`
```json
{
  "duration_drift_p90": 0.302984,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.321 | 0.208 | noisy |
| 3 | 1 | 0.094 | 0.057 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.451 | 0.255 | noisy |
| 5 | 1 | 0.176 | 0.098 | acceptable |
| 5 | 2 | 0.059 | 0.059 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.510 | 0.224 | noisy |
| 7 | 1 | 0.286 | 0.163 | noisy |
| 7 | 2 | 0.102 | 0.082 | acceptable |
| 7 | 3 | 0.020 | 0.020 | acceptable |
| 9 | 0 | 0.574 | 0.191 | noisy |
| 9 | 1 | 0.340 | 0.170 | noisy |
| 9 | 2 | 0.170 | 0.106 | acceptable |
| 9 | 3 | 0.043 | 0.043 | acceptable |

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
