# Body Profile Calibration Report

- generated_utc: `2026-03-17T00:28:59+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `189`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.429 | 0.407 | loosen_duration+tighten_health | noisy |
| standard | 0.429 | 0.407 | loosen_duration+tighten_health | noisy |
| strict | 0.799 | 0.791 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.291005`
- observed_false_regression_rate: `0.280423`
```json
{
  "duration_drift_p90": 1.111342,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.668 | 0.636 | noisy |
| 3 | 1 | 0.198 | 0.187 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.811 | 0.757 | noisy |
| 5 | 1 | 0.486 | 0.465 | noisy |
| 5 | 2 | 0.146 | 0.146 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.863 | 0.787 | noisy |
| 7 | 1 | 0.683 | 0.650 | noisy |
| 7 | 2 | 0.372 | 0.366 | noisy |
| 7 | 3 | 0.109 | 0.109 | acceptable |
| 9 | 0 | 0.890 | 0.790 | noisy |
| 9 | 1 | 0.790 | 0.746 | noisy |
| 9 | 2 | 0.552 | 0.536 | noisy |
| 9 | 3 | 0.315 | 0.315 | noisy |

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
