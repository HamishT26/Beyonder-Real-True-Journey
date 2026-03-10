# Body Profile Calibration Report

- generated_utc: `2026-03-07T05:28:29+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `86`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.198 | 0.127 | loosen_duration+loosen_health | acceptable |
| standard | 0.198 | 0.127 | loosen_duration+loosen_health | acceptable |
| strict | 0.593 | 0.557 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.186047`
- observed_false_regression_rate: `0.162791`
```json
{
  "duration_drift_p90": 0.353831,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.452 | 0.381 | noisy |
| 3 | 1 | 0.107 | 0.083 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.634 | 0.512 | noisy |
| 5 | 1 | 0.232 | 0.183 | noisy |
| 5 | 2 | 0.073 | 0.073 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.700 | 0.525 | noisy |
| 7 | 1 | 0.425 | 0.350 | noisy |
| 7 | 2 | 0.163 | 0.150 | acceptable |
| 7 | 3 | 0.050 | 0.050 | acceptable |
| 9 | 0 | 0.744 | 0.513 | noisy |
| 9 | 1 | 0.551 | 0.449 | noisy |
| 9 | 2 | 0.269 | 0.231 | noisy |
| 9 | 3 | 0.128 | 0.128 | acceptable |

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
