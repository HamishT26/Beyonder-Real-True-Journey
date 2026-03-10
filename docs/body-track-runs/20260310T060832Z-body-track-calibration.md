# Body Profile Calibration Report

- generated_utc: `2026-03-10T06:08:32+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `119`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.353 | 0.312 | loosen_duration+loosen_health | noisy |
| standard | 0.353 | 0.312 | loosen_duration+loosen_health | noisy |
| strict | 0.706 | 0.688 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.260504`
- observed_false_regression_rate: `0.243697`
```json
{
  "duration_drift_p90": 1.01777,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.590 | 0.538 | noisy |
| 3 | 1 | 0.179 | 0.162 | noisy |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.739 | 0.652 | noisy |
| 5 | 1 | 0.391 | 0.357 | noisy |
| 5 | 2 | 0.148 | 0.148 | acceptable |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.788 | 0.664 | noisy |
| 7 | 1 | 0.575 | 0.522 | noisy |
| 7 | 2 | 0.319 | 0.310 | noisy |
| 7 | 3 | 0.124 | 0.124 | acceptable |
| 9 | 0 | 0.820 | 0.658 | noisy |
| 9 | 1 | 0.685 | 0.613 | noisy |
| 9 | 2 | 0.432 | 0.405 | noisy |
| 9 | 3 | 0.297 | 0.297 | noisy |

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
