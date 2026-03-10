# Body Profile Calibration Report

- generated_utc: `2026-03-10T11:38:29+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `128`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.344 | 0.306 | loosen_duration+loosen_health | noisy |
| standard | 0.344 | 0.306 | loosen_duration+loosen_health | noisy |
| strict | 0.719 | 0.702 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.265625`
- observed_false_regression_rate: `0.25`
```json
{
  "duration_drift_p90": 1.02139,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.611 | 0.563 | noisy |
| 3 | 1 | 0.175 | 0.159 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.758 | 0.677 | noisy |
| 5 | 1 | 0.419 | 0.387 | noisy |
| 5 | 2 | 0.137 | 0.137 | acceptable |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.803 | 0.689 | noisy |
| 7 | 1 | 0.607 | 0.557 | noisy |
| 7 | 2 | 0.328 | 0.320 | noisy |
| 7 | 3 | 0.115 | 0.115 | acceptable |
| 9 | 0 | 0.833 | 0.683 | noisy |
| 9 | 1 | 0.708 | 0.642 | noisy |
| 9 | 2 | 0.475 | 0.450 | noisy |
| 9 | 3 | 0.300 | 0.300 | noisy |

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
