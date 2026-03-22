# Body Profile Calibration Report

- generated_utc: `2026-03-22T07:44:37+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `239`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.527 | 0.513 | loosen_duration+tighten_health | noisy |
| standard | 0.527 | 0.513 | loosen_duration+tighten_health | noisy |
| strict | 0.841 | 0.836 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.309623`
- observed_false_regression_rate: `0.301255`
```json
{
  "duration_drift_p90": 1.146815,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.700 | 0.675 | noisy |
| 3 | 1 | 0.224 | 0.215 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.838 | 0.796 | noisy |
| 5 | 1 | 0.540 | 0.523 | noisy |
| 5 | 2 | 0.170 | 0.170 | noisy |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.888 | 0.828 | noisy |
| 7 | 1 | 0.730 | 0.704 | noisy |
| 7 | 2 | 0.433 | 0.429 | noisy |
| 7 | 3 | 0.133 | 0.133 | acceptable |
| 9 | 0 | 0.913 | 0.835 | noisy |
| 9 | 1 | 0.831 | 0.797 | noisy |
| 9 | 2 | 0.606 | 0.593 | noisy |
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
