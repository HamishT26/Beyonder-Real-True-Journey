# Body Profile Calibration Report

- generated_utc: `2026-03-07T08:24:26+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `93`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.204 | 0.140 | loosen_duration+loosen_health | acceptable |
| standard | 0.204 | 0.140 | loosen_duration+loosen_health | acceptable |
| strict | 0.624 | 0.593 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.193548`
- observed_false_regression_rate: `0.172043`
```json
{
  "duration_drift_p90": 0.367973,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.473 | 0.407 | noisy |
| 3 | 1 | 0.099 | 0.077 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.663 | 0.551 | noisy |
| 5 | 1 | 0.236 | 0.191 | noisy |
| 5 | 2 | 0.067 | 0.067 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.724 | 0.563 | noisy |
| 7 | 1 | 0.448 | 0.379 | noisy |
| 7 | 2 | 0.149 | 0.138 | acceptable |
| 7 | 3 | 0.046 | 0.046 | acceptable |
| 9 | 0 | 0.765 | 0.553 | noisy |
| 9 | 1 | 0.588 | 0.494 | noisy |
| 9 | 2 | 0.271 | 0.235 | noisy |
| 9 | 3 | 0.118 | 0.118 | acceptable |

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
