# Body Profile Calibration Report

- generated_utc: `2026-03-06T13:04:19+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `74`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.216 | 0.134 | loosen_duration+loosen_health | acceptable |
| standard | 0.216 | 0.134 | loosen_duration+loosen_health | acceptable |
| strict | 0.541 | 0.493 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.175676`
- observed_false_regression_rate: `0.148649`
```json
{
  "duration_drift_p90": 0.318578,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.431 | 0.347 | noisy |
| 3 | 1 | 0.111 | 0.083 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.600 | 0.457 | noisy |
| 5 | 1 | 0.229 | 0.171 | noisy |
| 5 | 2 | 0.086 | 0.086 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.647 | 0.441 | noisy |
| 7 | 1 | 0.397 | 0.309 | noisy |
| 7 | 2 | 0.191 | 0.176 | noisy |
| 7 | 3 | 0.059 | 0.059 | acceptable |
| 9 | 0 | 0.697 | 0.424 | noisy |
| 9 | 1 | 0.515 | 0.394 | noisy |
| 9 | 2 | 0.288 | 0.242 | noisy |
| 9 | 3 | 0.152 | 0.152 | noisy |

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
