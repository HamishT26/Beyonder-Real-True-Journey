# Body Profile Calibration Report

- generated_utc: `2026-03-06T02:28:33+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `47`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.213 | 0.075 | loosen_duration+loosen_health | acceptable |
| standard | 0.213 | 0.075 | loosen_duration+loosen_health | acceptable |
| strict | 0.426 | 0.325 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.085106`
- observed_false_regression_rate: `0.042553`
```json
{
  "duration_drift_p90": 0.175536,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.222 | 0.089 | acceptable |
| 3 | 1 | 0.044 | 0.000 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.349 | 0.116 | acceptable |
| 5 | 1 | 0.093 | 0.000 | acceptable |
| 5 | 2 | 0.000 | 0.000 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.415 | 0.073 | acceptable |
| 7 | 1 | 0.171 | 0.024 | acceptable |
| 7 | 2 | 0.024 | 0.000 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.487 | 0.026 | acceptable |
| 9 | 1 | 0.231 | 0.026 | acceptable |
| 9 | 2 | 0.077 | 0.000 | acceptable |
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
