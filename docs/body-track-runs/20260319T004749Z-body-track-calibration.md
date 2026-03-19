# Body Profile Calibration Report

- generated_utc: `2026-03-19T00:47:49+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `218`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.486 | 0.469 | loosen_duration+tighten_health | noisy |
| standard | 0.486 | 0.469 | loosen_duration+tighten_health | noisy |
| strict | 0.826 | 0.820 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.293578`
- observed_false_regression_rate: `0.284404`
```json
{
  "duration_drift_p90": 1.115376,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.681 | 0.653 | noisy |
| 3 | 1 | 0.194 | 0.185 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.822 | 0.776 | noisy |
| 5 | 1 | 0.505 | 0.486 | noisy |
| 5 | 2 | 0.131 | 0.131 | acceptable |
| 5 | 3 | 0.009 | 0.009 | acceptable |
| 7 | 0 | 0.877 | 0.811 | noisy |
| 7 | 1 | 0.703 | 0.675 | noisy |
| 7 | 2 | 0.377 | 0.373 | noisy |
| 7 | 3 | 0.094 | 0.094 | acceptable |
| 9 | 0 | 0.905 | 0.819 | noisy |
| 9 | 1 | 0.814 | 0.776 | noisy |
| 9 | 2 | 0.567 | 0.552 | noisy |
| 9 | 3 | 0.295 | 0.295 | noisy |

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
