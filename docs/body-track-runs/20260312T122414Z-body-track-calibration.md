# Body Profile Calibration Report

- generated_utc: `2026-03-12T12:24:14+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `165`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.364 | 0.335 | loosen_duration+tighten_health | noisy |
| standard | 0.364 | 0.335 | loosen_duration+tighten_health | noisy |
| strict | 0.770 | 0.759 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.266667`
- observed_false_regression_rate: `0.254545`
```json
{
  "duration_drift_p90": 1.001076,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.638 | 0.601 | noisy |
| 3 | 1 | 0.166 | 0.153 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.789 | 0.727 | noisy |
| 5 | 1 | 0.435 | 0.410 | noisy |
| 5 | 2 | 0.118 | 0.118 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.843 | 0.755 | noisy |
| 7 | 1 | 0.642 | 0.604 | noisy |
| 7 | 2 | 0.314 | 0.308 | noisy |
| 7 | 3 | 0.088 | 0.088 | acceptable |
| 9 | 0 | 0.873 | 0.758 | noisy |
| 9 | 1 | 0.758 | 0.707 | noisy |
| 9 | 2 | 0.490 | 0.471 | noisy |
| 9 | 3 | 0.261 | 0.261 | noisy |

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
