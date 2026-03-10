# Body Profile Calibration Report

- generated_utc: `2026-03-10T12:48:13+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `136`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.331 | 0.295 | loosen_duration+loosen_health | noisy |
| standard | 0.331 | 0.295 | loosen_duration+loosen_health | noisy |
| strict | 0.728 | 0.713 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.264706`
- observed_false_regression_rate: `0.25`
```json
{
  "duration_drift_p90": 0.999131,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.619 | 0.575 | noisy |
| 3 | 1 | 0.179 | 0.164 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.773 | 0.697 | noisy |
| 5 | 1 | 0.439 | 0.409 | noisy |
| 5 | 2 | 0.136 | 0.136 | acceptable |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.815 | 0.708 | noisy |
| 7 | 1 | 0.631 | 0.585 | noisy |
| 7 | 2 | 0.346 | 0.338 | noisy |
| 7 | 3 | 0.108 | 0.108 | acceptable |
| 9 | 0 | 0.844 | 0.703 | noisy |
| 9 | 1 | 0.727 | 0.664 | noisy |
| 9 | 2 | 0.508 | 0.484 | noisy |
| 9 | 3 | 0.305 | 0.305 | noisy |

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
