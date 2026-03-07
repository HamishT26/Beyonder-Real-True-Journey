# Body Profile Calibration Report

- generated_utc: `2026-03-07T02:12:01+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `78`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.218 | 0.141 | loosen_duration+loosen_health | acceptable |
| standard | 0.218 | 0.141 | loosen_duration+loosen_health | acceptable |
| strict | 0.564 | 0.521 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.179487`
- observed_false_regression_rate: `0.153846`
```json
{
  "duration_drift_p90": 0.4789,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.421 | 0.342 | noisy |
| 3 | 1 | 0.105 | 0.079 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.595 | 0.459 | noisy |
| 5 | 1 | 0.216 | 0.162 | noisy |
| 5 | 2 | 0.081 | 0.081 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.667 | 0.472 | noisy |
| 7 | 1 | 0.375 | 0.292 | noisy |
| 7 | 2 | 0.181 | 0.167 | noisy |
| 7 | 3 | 0.056 | 0.056 | acceptable |
| 9 | 0 | 0.714 | 0.457 | noisy |
| 9 | 1 | 0.500 | 0.386 | noisy |
| 9 | 2 | 0.271 | 0.229 | noisy |
| 9 | 3 | 0.143 | 0.143 | acceptable |

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
