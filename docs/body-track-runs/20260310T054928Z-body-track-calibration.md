# Body Profile Calibration Report

- generated_utc: `2026-03-10T05:49:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `116`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.345 | 0.303 | loosen_duration+loosen_health | noisy |
| standard | 0.345 | 0.303 | loosen_duration+loosen_health | noisy |
| strict | 0.698 | 0.679 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.25`
- observed_false_regression_rate: `0.232759`
```json
{
  "duration_drift_p90": 1.028631,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.579 | 0.526 | noisy |
| 3 | 1 | 0.175 | 0.158 | noisy |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.732 | 0.643 | noisy |
| 5 | 1 | 0.375 | 0.339 | noisy |
| 5 | 2 | 0.143 | 0.143 | acceptable |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.782 | 0.655 | noisy |
| 7 | 1 | 0.564 | 0.509 | noisy |
| 7 | 2 | 0.300 | 0.291 | noisy |
| 7 | 3 | 0.118 | 0.118 | acceptable |
| 9 | 0 | 0.815 | 0.648 | noisy |
| 9 | 1 | 0.676 | 0.602 | noisy |
| 9 | 2 | 0.417 | 0.389 | noisy |
| 9 | 3 | 0.278 | 0.278 | noisy |

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
