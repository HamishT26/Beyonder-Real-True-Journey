# Body Profile Calibration Report

- generated_utc: `2026-03-10T05:33:01+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `115`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.348 | 0.306 | loosen_duration+loosen_health | noisy |
| standard | 0.348 | 0.306 | loosen_duration+loosen_health | noisy |
| strict | 0.696 | 0.676 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.252174`
- observed_false_regression_rate: `0.234783`
```json
{
  "duration_drift_p90": 1.032251,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.575 | 0.522 | noisy |
| 3 | 1 | 0.177 | 0.159 | noisy |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.730 | 0.640 | noisy |
| 5 | 1 | 0.369 | 0.333 | noisy |
| 5 | 2 | 0.144 | 0.144 | acceptable |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.780 | 0.651 | noisy |
| 7 | 1 | 0.560 | 0.505 | noisy |
| 7 | 2 | 0.294 | 0.284 | noisy |
| 7 | 3 | 0.119 | 0.119 | acceptable |
| 9 | 0 | 0.813 | 0.645 | noisy |
| 9 | 1 | 0.673 | 0.598 | noisy |
| 9 | 2 | 0.411 | 0.383 | noisy |
| 9 | 3 | 0.280 | 0.280 | noisy |

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
