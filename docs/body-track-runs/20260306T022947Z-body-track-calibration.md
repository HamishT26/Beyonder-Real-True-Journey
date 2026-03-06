# Body Profile Calibration Report

- generated_utc: `2026-03-06T02:29:47+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `49`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.224 | 0.095 | loosen_duration+loosen_health | acceptable |
| standard | 0.224 | 0.095 | loosen_duration+loosen_health | acceptable |
| strict | 0.449 | 0.357 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.102041`
- observed_false_regression_rate: `0.061224`
```json
{
  "duration_drift_p90": 0.232664,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.234 | 0.106 | acceptable |
| 3 | 1 | 0.043 | 0.000 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.378 | 0.156 | noisy |
| 5 | 1 | 0.089 | 0.000 | acceptable |
| 5 | 2 | 0.000 | 0.000 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.442 | 0.116 | acceptable |
| 7 | 1 | 0.186 | 0.047 | acceptable |
| 7 | 2 | 0.023 | 0.000 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.512 | 0.073 | acceptable |
| 9 | 1 | 0.244 | 0.049 | acceptable |
| 9 | 2 | 0.073 | 0.000 | acceptable |
| 9 | 3 | 0.000 | 0.000 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 5,
    "max_regressions": 1
  }
}
```
