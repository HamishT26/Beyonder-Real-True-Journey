# Body Profile Calibration Report

- generated_utc: `2026-03-12T12:02:32+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `163`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.368 | 0.340 | loosen_duration+tighten_health | noisy |
| standard | 0.368 | 0.340 | loosen_duration+tighten_health | noisy |
| strict | 0.767 | 0.756 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.269939`
- observed_false_regression_rate: `0.257669`
```json
{
  "duration_drift_p90": 1.004965,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.634 | 0.596 | noisy |
| 3 | 1 | 0.168 | 0.155 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.786 | 0.723 | noisy |
| 5 | 1 | 0.428 | 0.403 | noisy |
| 5 | 2 | 0.119 | 0.119 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.841 | 0.752 | noisy |
| 7 | 1 | 0.637 | 0.599 | noisy |
| 7 | 2 | 0.318 | 0.312 | noisy |
| 7 | 3 | 0.089 | 0.089 | acceptable |
| 9 | 0 | 0.871 | 0.755 | noisy |
| 9 | 1 | 0.755 | 0.703 | noisy |
| 9 | 2 | 0.497 | 0.477 | noisy |
| 9 | 3 | 0.265 | 0.265 | noisy |

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
