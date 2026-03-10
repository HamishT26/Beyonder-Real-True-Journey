# Body Profile Calibration Report

- generated_utc: `2026-03-10T06:03:03+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `118`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.347 | 0.306 | loosen_duration+loosen_health | noisy |
| standard | 0.347 | 0.306 | loosen_duration+loosen_health | noisy |
| strict | 0.703 | 0.685 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.254237`
- observed_false_regression_rate: `0.237288`
```json
{
  "duration_drift_p90": 1.02139,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.586 | 0.534 | noisy |
| 3 | 1 | 0.172 | 0.155 | noisy |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.737 | 0.649 | noisy |
| 5 | 1 | 0.386 | 0.351 | noisy |
| 5 | 2 | 0.149 | 0.149 | acceptable |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.786 | 0.661 | noisy |
| 7 | 1 | 0.571 | 0.518 | noisy |
| 7 | 2 | 0.312 | 0.304 | noisy |
| 7 | 3 | 0.116 | 0.116 | acceptable |
| 9 | 0 | 0.818 | 0.655 | noisy |
| 9 | 1 | 0.682 | 0.609 | noisy |
| 9 | 2 | 0.427 | 0.400 | noisy |
| 9 | 3 | 0.291 | 0.291 | noisy |

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
