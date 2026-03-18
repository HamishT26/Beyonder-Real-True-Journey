# Body Profile Calibration Report

- generated_utc: `2026-03-18T07:53:29+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `214`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.481 | 0.464 | loosen_duration+tighten_health | noisy |
| standard | 0.481 | 0.464 | loosen_duration+tighten_health | noisy |
| strict | 0.822 | 0.816 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.28972`
- observed_false_regression_rate: `0.280374`
```json
{
  "duration_drift_p90": 1.113509,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.675 | 0.646 | noisy |
| 3 | 1 | 0.193 | 0.184 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.819 | 0.771 | noisy |
| 5 | 1 | 0.495 | 0.476 | noisy |
| 5 | 2 | 0.133 | 0.133 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.875 | 0.808 | noisy |
| 7 | 1 | 0.697 | 0.668 | noisy |
| 7 | 2 | 0.365 | 0.361 | noisy |
| 7 | 3 | 0.096 | 0.096 | acceptable |
| 9 | 0 | 0.903 | 0.816 | noisy |
| 9 | 1 | 0.811 | 0.772 | noisy |
| 9 | 2 | 0.558 | 0.544 | noisy |
| 9 | 3 | 0.286 | 0.286 | noisy |

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
