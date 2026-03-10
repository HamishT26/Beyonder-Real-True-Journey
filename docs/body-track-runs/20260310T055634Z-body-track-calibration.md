# Body Profile Calibration Report

- generated_utc: `2026-03-10T05:56:34+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `117`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.350 | 0.309 | loosen_duration+loosen_health | noisy |
| standard | 0.350 | 0.309 | loosen_duration+loosen_health | noisy |
| strict | 0.701 | 0.682 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.25641`
- observed_false_regression_rate: `0.239316`
```json
{
  "duration_drift_p90": 1.025011,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.583 | 0.530 | noisy |
| 3 | 1 | 0.174 | 0.157 | noisy |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.735 | 0.646 | noisy |
| 5 | 1 | 0.381 | 0.345 | noisy |
| 5 | 2 | 0.150 | 0.150 | noisy |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.784 | 0.658 | noisy |
| 7 | 1 | 0.568 | 0.514 | noisy |
| 7 | 2 | 0.306 | 0.297 | noisy |
| 7 | 3 | 0.117 | 0.117 | acceptable |
| 9 | 0 | 0.817 | 0.651 | noisy |
| 9 | 1 | 0.679 | 0.606 | noisy |
| 9 | 2 | 0.422 | 0.394 | noisy |
| 9 | 3 | 0.284 | 0.284 | noisy |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 3
  }
}
```
