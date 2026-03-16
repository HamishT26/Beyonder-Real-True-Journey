# Body Profile Calibration Report

- generated_utc: `2026-03-16T00:11:15+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `178`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.410 | 0.386 | loosen_duration+tighten_health | noisy |
| standard | 0.410 | 0.386 | loosen_duration+tighten_health | noisy |
| strict | 0.787 | 0.778 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.286517`
- observed_false_regression_rate: `0.275281`
```json
{
  "duration_drift_p90": 1.10377,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.665 | 0.631 | noisy |
| 3 | 1 | 0.188 | 0.176 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.805 | 0.747 | noisy |
| 5 | 1 | 0.477 | 0.454 | noisy |
| 5 | 2 | 0.138 | 0.138 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.855 | 0.773 | noisy |
| 7 | 1 | 0.669 | 0.634 | noisy |
| 7 | 2 | 0.366 | 0.360 | noisy |
| 7 | 3 | 0.105 | 0.105 | acceptable |
| 9 | 0 | 0.882 | 0.776 | noisy |
| 9 | 1 | 0.776 | 0.729 | noisy |
| 9 | 2 | 0.529 | 0.512 | noisy |
| 9 | 3 | 0.312 | 0.312 | noisy |

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
