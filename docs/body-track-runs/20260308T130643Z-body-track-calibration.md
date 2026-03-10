# Body Profile Calibration Report

- generated_utc: `2026-03-08T13:06:43+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `103`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.272 | 0.219 | loosen_duration+loosen_health | noisy |
| standard | 0.272 | 0.219 | loosen_duration+loosen_health | noisy |
| strict | 0.660 | 0.635 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.223301`
- observed_false_regression_rate: `0.203883`
```json
{
  "duration_drift_p90": 0.731583,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.525 | 0.465 | noisy |
| 3 | 1 | 0.149 | 0.129 | acceptable |
| 3 | 2 | 0.010 | 0.010 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.697 | 0.596 | noisy |
| 5 | 1 | 0.303 | 0.263 | noisy |
| 5 | 2 | 0.121 | 0.121 | acceptable |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.753 | 0.608 | noisy |
| 7 | 1 | 0.505 | 0.443 | noisy |
| 7 | 2 | 0.216 | 0.206 | noisy |
| 7 | 3 | 0.103 | 0.103 | acceptable |
| 9 | 0 | 0.789 | 0.600 | noisy |
| 9 | 1 | 0.632 | 0.547 | noisy |
| 9 | 2 | 0.337 | 0.305 | noisy |
| 9 | 3 | 0.189 | 0.189 | noisy |

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
