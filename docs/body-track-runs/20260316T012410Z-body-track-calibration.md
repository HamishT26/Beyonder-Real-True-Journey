# Body Profile Calibration Report

- generated_utc: `2026-03-16T01:24:10+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `182`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.423 | 0.400 | loosen_duration+tighten_health | noisy |
| standard | 0.423 | 0.400 | loosen_duration+tighten_health | noisy |
| strict | 0.791 | 0.783 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.285714`
- observed_false_regression_rate: `0.274725`
```json
{
  "duration_drift_p90": 1.110042,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.667 | 0.633 | noisy |
| 3 | 1 | 0.194 | 0.183 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.809 | 0.753 | noisy |
| 5 | 1 | 0.489 | 0.466 | noisy |
| 5 | 2 | 0.146 | 0.146 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.858 | 0.778 | noisy |
| 7 | 1 | 0.676 | 0.642 | noisy |
| 7 | 2 | 0.381 | 0.375 | noisy |
| 7 | 3 | 0.114 | 0.114 | acceptable |
| 9 | 0 | 0.885 | 0.782 | noisy |
| 9 | 1 | 0.782 | 0.736 | noisy |
| 9 | 2 | 0.540 | 0.523 | noisy |
| 9 | 3 | 0.328 | 0.328 | noisy |

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
