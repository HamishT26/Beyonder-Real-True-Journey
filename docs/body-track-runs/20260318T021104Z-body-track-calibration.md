# Body Profile Calibration Report

- generated_utc: `2026-03-18T02:11:04+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `210`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.476 | 0.458 | loosen_duration+tighten_health | noisy |
| standard | 0.476 | 0.458 | loosen_duration+tighten_health | noisy |
| strict | 0.819 | 0.813 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.285714`
- observed_false_regression_rate: `0.27619`
```json
{
  "duration_drift_p90": 1.110909,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.668 | 0.639 | noisy |
| 3 | 1 | 0.188 | 0.178 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.816 | 0.767 | noisy |
| 5 | 1 | 0.485 | 0.466 | noisy |
| 5 | 2 | 0.131 | 0.131 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.873 | 0.804 | noisy |
| 7 | 1 | 0.691 | 0.662 | noisy |
| 7 | 2 | 0.353 | 0.348 | noisy |
| 7 | 3 | 0.098 | 0.098 | acceptable |
| 9 | 0 | 0.901 | 0.812 | noisy |
| 9 | 1 | 0.807 | 0.767 | noisy |
| 9 | 2 | 0.550 | 0.535 | noisy |
| 9 | 3 | 0.282 | 0.282 | noisy |

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
