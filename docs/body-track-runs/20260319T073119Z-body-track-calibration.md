# Body Profile Calibration Report

- generated_utc: `2026-03-19T07:31:19+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `220`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.491 | 0.474 | loosen_duration+tighten_health | noisy |
| standard | 0.491 | 0.474 | loosen_duration+tighten_health | noisy |
| strict | 0.827 | 0.822 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.3`
- observed_false_regression_rate: `0.290909`
```json
{
  "duration_drift_p90": 1.114876,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.683 | 0.656 | noisy |
| 3 | 1 | 0.202 | 0.193 | noisy |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.824 | 0.778 | noisy |
| 5 | 1 | 0.509 | 0.491 | noisy |
| 5 | 2 | 0.139 | 0.139 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.879 | 0.813 | noisy |
| 7 | 1 | 0.706 | 0.678 | noisy |
| 7 | 2 | 0.383 | 0.379 | noisy |
| 7 | 3 | 0.103 | 0.103 | acceptable |
| 9 | 0 | 0.906 | 0.821 | noisy |
| 9 | 1 | 0.816 | 0.778 | noisy |
| 9 | 2 | 0.571 | 0.557 | noisy |
| 9 | 3 | 0.302 | 0.302 | noisy |

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
