# Body Profile Calibration Report

- generated_utc: `2026-03-31T02:10:14+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `338`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.639 | 0.631 | loosen_duration+tighten_health | noisy |
| standard | 0.639 | 0.631 | loosen_duration+tighten_health | noisy |
| strict | 0.888 | 0.885 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.331361`
- observed_false_regression_rate: `0.325444`
```json
{
  "duration_drift_p90": 1.583835,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.738 | 0.720 | noisy |
| 3 | 1 | 0.241 | 0.235 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.877 | 0.847 | noisy |
| 5 | 1 | 0.578 | 0.566 | noisy |
| 5 | 2 | 0.192 | 0.192 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.919 | 0.877 | noisy |
| 7 | 1 | 0.765 | 0.747 | noisy |
| 7 | 2 | 0.476 | 0.473 | noisy |
| 7 | 3 | 0.151 | 0.151 | noisy |
| 9 | 0 | 0.939 | 0.885 | noisy |
| 9 | 1 | 0.864 | 0.839 | noisy |
| 9 | 2 | 0.658 | 0.648 | noisy |
| 9 | 3 | 0.397 | 0.397 | noisy |

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
