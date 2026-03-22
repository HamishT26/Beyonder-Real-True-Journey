# Body Profile Calibration Report

- generated_utc: `2026-03-22T12:36:53+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `247`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.543 | 0.529 | loosen_duration+tighten_health | noisy |
| standard | 0.543 | 0.529 | loosen_duration+tighten_health | noisy |
| strict | 0.846 | 0.842 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.311741`
- observed_false_regression_rate: `0.303644`
```json
{
  "duration_drift_p90": 1.256138,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.706 | 0.682 | noisy |
| 3 | 1 | 0.224 | 0.216 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.844 | 0.802 | noisy |
| 5 | 1 | 0.547 | 0.531 | noisy |
| 5 | 2 | 0.165 | 0.165 | noisy |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.892 | 0.834 | noisy |
| 7 | 1 | 0.739 | 0.714 | noisy |
| 7 | 2 | 0.440 | 0.436 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.916 | 0.841 | noisy |
| 9 | 1 | 0.837 | 0.803 | noisy |
| 9 | 2 | 0.619 | 0.607 | noisy |
| 9 | 3 | 0.351 | 0.351 | noisy |

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
