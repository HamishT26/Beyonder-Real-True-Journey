# Body Profile Calibration Report

- generated_utc: `2026-03-17T21:25:03+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `200`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.460 | 0.440 | loosen_duration+tighten_health | noisy |
| standard | 0.460 | 0.440 | loosen_duration+tighten_health | noisy |
| strict | 0.810 | 0.803 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.285`
- observed_false_regression_rate: `0.275`
```json
{
  "duration_drift_p90": 1.110909,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.662 | 0.631 | noisy |
| 3 | 1 | 0.197 | 0.187 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.806 | 0.755 | noisy |
| 5 | 1 | 0.485 | 0.464 | noisy |
| 5 | 2 | 0.138 | 0.138 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.866 | 0.794 | noisy |
| 7 | 1 | 0.680 | 0.649 | noisy |
| 7 | 2 | 0.361 | 0.356 | noisy |
| 7 | 3 | 0.103 | 0.103 | acceptable |
| 9 | 0 | 0.896 | 0.802 | noisy |
| 9 | 1 | 0.797 | 0.755 | noisy |
| 9 | 2 | 0.542 | 0.526 | noisy |
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
