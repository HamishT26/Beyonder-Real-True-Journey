# Body Profile Calibration Report

- generated_utc: `2026-03-14T11:21:48+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `177`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.407 | 0.382 | loosen_duration+tighten_health | noisy |
| standard | 0.407 | 0.382 | loosen_duration+tighten_health | noisy |
| strict | 0.785 | 0.776 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.282486`
- observed_false_regression_rate: `0.271186`
```json
{
  "duration_drift_p90": 1.078844,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.663 | 0.629 | noisy |
| 3 | 1 | 0.183 | 0.171 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.803 | 0.746 | noisy |
| 5 | 1 | 0.474 | 0.451 | noisy |
| 5 | 2 | 0.133 | 0.133 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.854 | 0.772 | noisy |
| 7 | 1 | 0.667 | 0.632 | noisy |
| 7 | 2 | 0.363 | 0.357 | noisy |
| 7 | 3 | 0.105 | 0.105 | acceptable |
| 9 | 0 | 0.882 | 0.775 | noisy |
| 9 | 1 | 0.775 | 0.728 | noisy |
| 9 | 2 | 0.527 | 0.509 | noisy |
| 9 | 3 | 0.308 | 0.308 | noisy |

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
