# Body Profile Calibration Report

- generated_utc: `2026-03-06T13:02:01+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `73`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.219 | 0.136 | loosen_duration+loosen_health | acceptable |
| standard | 0.219 | 0.136 | loosen_duration+loosen_health | acceptable |
| strict | 0.534 | 0.485 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.178082`
- observed_false_regression_rate: `0.150685`
```json
{
  "duration_drift_p90": 0.322062,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.437 | 0.352 | noisy |
| 3 | 1 | 0.113 | 0.085 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.594 | 0.449 | noisy |
| 5 | 1 | 0.232 | 0.174 | noisy |
| 5 | 2 | 0.087 | 0.087 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.642 | 0.433 | noisy |
| 7 | 1 | 0.403 | 0.313 | noisy |
| 7 | 2 | 0.194 | 0.179 | noisy |
| 7 | 3 | 0.060 | 0.060 | acceptable |
| 9 | 0 | 0.692 | 0.415 | noisy |
| 9 | 1 | 0.508 | 0.385 | noisy |
| 9 | 2 | 0.292 | 0.246 | noisy |
| 9 | 3 | 0.154 | 0.154 | noisy |

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
