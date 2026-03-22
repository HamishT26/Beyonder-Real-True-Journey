# Body Profile Calibration Report

- generated_utc: `2026-03-22T07:09:52+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `238`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.529 | 0.515 | loosen_duration+tighten_health | noisy |
| standard | 0.529 | 0.515 | loosen_duration+tighten_health | noisy |
| strict | 0.840 | 0.835 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.310924`
- observed_false_regression_rate: `0.302521`
```json
{
  "duration_drift_p90": 1.156795,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.703 | 0.678 | noisy |
| 3 | 1 | 0.225 | 0.216 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.838 | 0.795 | noisy |
| 5 | 1 | 0.543 | 0.526 | noisy |
| 5 | 2 | 0.171 | 0.171 | noisy |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.888 | 0.828 | noisy |
| 7 | 1 | 0.728 | 0.703 | noisy |
| 7 | 2 | 0.431 | 0.427 | noisy |
| 7 | 3 | 0.134 | 0.134 | acceptable |
| 9 | 0 | 0.913 | 0.835 | noisy |
| 9 | 1 | 0.830 | 0.796 | noisy |
| 9 | 2 | 0.604 | 0.591 | noisy |
| 9 | 3 | 0.352 | 0.352 | noisy |

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
