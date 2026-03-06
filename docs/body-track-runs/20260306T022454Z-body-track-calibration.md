# Body Profile Calibration Report

- generated_utc: `2026-03-06T02:24:54+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `45`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.222 | 0.079 | loosen_duration+loosen_health | acceptable |
| standard | 0.222 | 0.079 | loosen_duration+loosen_health | acceptable |
| strict | 0.422 | 0.316 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.088889`
- observed_false_regression_rate: `0.044444`
```json
{
  "duration_drift_p90": 0.182464,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.209 | 0.070 | acceptable |
| 3 | 1 | 0.047 | 0.000 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.317 | 0.073 | acceptable |
| 5 | 1 | 0.098 | 0.000 | acceptable |
| 5 | 2 | 0.000 | 0.000 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.385 | 0.026 | acceptable |
| 7 | 1 | 0.179 | 0.026 | acceptable |
| 7 | 2 | 0.026 | 0.000 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.459 | 0.000 | acceptable |
| 9 | 1 | 0.189 | 0.000 | acceptable |
| 9 | 2 | 0.054 | 0.000 | acceptable |
| 9 | 3 | 0.000 | 0.000 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 9,
    "max_regressions": 1
  }
}
```
