# Body Profile Calibration Report

- generated_utc: `2026-03-06T05:02:33+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `65`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.185 | 0.086 | loosen_duration+loosen_health | acceptable |
| standard | 0.185 | 0.086 | loosen_duration+loosen_health | acceptable |
| strict | 0.492 | 0.431 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.169231`
- observed_false_regression_rate: `0.138462`
```json
{
  "duration_drift_p90": 0.285721,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.397 | 0.302 | noisy |
| 3 | 1 | 0.127 | 0.095 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.541 | 0.377 | noisy |
| 5 | 1 | 0.262 | 0.197 | noisy |
| 5 | 2 | 0.098 | 0.098 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.593 | 0.356 | noisy |
| 7 | 1 | 0.390 | 0.288 | noisy |
| 7 | 2 | 0.220 | 0.203 | noisy |
| 7 | 3 | 0.068 | 0.068 | acceptable |
| 9 | 0 | 0.649 | 0.333 | noisy |
| 9 | 1 | 0.456 | 0.316 | noisy |
| 9 | 2 | 0.316 | 0.263 | noisy |
| 9 | 3 | 0.175 | 0.175 | noisy |

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
