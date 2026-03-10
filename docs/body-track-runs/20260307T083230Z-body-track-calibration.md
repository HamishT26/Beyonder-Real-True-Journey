# Body Profile Calibration Report

- generated_utc: `2026-03-07T08:32:30+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `95`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.211 | 0.148 | loosen_duration+loosen_health | acceptable |
| standard | 0.211 | 0.148 | loosen_duration+loosen_health | acceptable |
| strict | 0.632 | 0.602 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.2`
- observed_false_regression_rate: `0.178947`
```json
{
  "duration_drift_p90": 0.402682,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.484 | 0.419 | noisy |
| 3 | 1 | 0.108 | 0.086 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.670 | 0.560 | noisy |
| 5 | 1 | 0.242 | 0.198 | noisy |
| 5 | 2 | 0.066 | 0.066 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.730 | 0.573 | noisy |
| 7 | 1 | 0.461 | 0.393 | noisy |
| 7 | 2 | 0.146 | 0.135 | acceptable |
| 7 | 3 | 0.045 | 0.045 | acceptable |
| 9 | 0 | 0.770 | 0.563 | noisy |
| 9 | 1 | 0.598 | 0.506 | noisy |
| 9 | 2 | 0.276 | 0.241 | noisy |
| 9 | 3 | 0.115 | 0.115 | acceptable |

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
