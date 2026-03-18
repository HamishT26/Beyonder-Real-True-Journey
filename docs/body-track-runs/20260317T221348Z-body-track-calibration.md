# Body Profile Calibration Report

- generated_utc: `2026-03-17T22:13:48+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `202`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.460 | 0.441 | loosen_duration+tighten_health | noisy |
| standard | 0.460 | 0.441 | loosen_duration+tighten_health | noisy |
| strict | 0.812 | 0.805 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.287129`
- observed_false_regression_rate: `0.277228`
```json
{
  "duration_drift_p90": 1.110042,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.660 | 0.630 | noisy |
| 3 | 1 | 0.195 | 0.185 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.808 | 0.758 | noisy |
| 5 | 1 | 0.490 | 0.470 | noisy |
| 5 | 2 | 0.136 | 0.136 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.867 | 0.796 | noisy |
| 7 | 1 | 0.684 | 0.653 | noisy |
| 7 | 2 | 0.362 | 0.357 | noisy |
| 7 | 3 | 0.102 | 0.102 | acceptable |
| 9 | 0 | 0.897 | 0.804 | noisy |
| 9 | 1 | 0.799 | 0.758 | noisy |
| 9 | 2 | 0.541 | 0.526 | noisy |
| 9 | 3 | 0.294 | 0.294 | noisy |

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
