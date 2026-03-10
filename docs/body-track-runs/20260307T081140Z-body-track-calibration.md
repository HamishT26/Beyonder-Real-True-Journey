# Body Profile Calibration Report

- generated_utc: `2026-03-07T08:11:40+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `90`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.200 | 0.133 | loosen_duration+loosen_health | acceptable |
| standard | 0.200 | 0.133 | loosen_duration+loosen_health | acceptable |
| strict | 0.611 | 0.578 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.188889`
- observed_false_regression_rate: `0.166667`
```json
{
  "duration_drift_p90": 0.381257,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.477 | 0.409 | noisy |
| 3 | 1 | 0.102 | 0.080 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.651 | 0.535 | noisy |
| 5 | 1 | 0.244 | 0.198 | noisy |
| 5 | 2 | 0.070 | 0.070 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.714 | 0.548 | noisy |
| 7 | 1 | 0.440 | 0.369 | noisy |
| 7 | 2 | 0.155 | 0.143 | acceptable |
| 7 | 3 | 0.048 | 0.048 | acceptable |
| 9 | 0 | 0.756 | 0.537 | noisy |
| 9 | 1 | 0.573 | 0.476 | noisy |
| 9 | 2 | 0.268 | 0.232 | noisy |
| 9 | 3 | 0.122 | 0.122 | acceptable |

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
