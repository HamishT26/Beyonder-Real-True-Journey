# Body Profile Calibration Report

- generated_utc: `2026-03-22T12:42:04+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `248`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.544 | 0.531 | loosen_duration+tighten_health | noisy |
| standard | 0.544 | 0.531 | loosen_duration+tighten_health | noisy |
| strict | 0.847 | 0.842 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.310484`
- observed_false_regression_rate: `0.302419`
```json
{
  "duration_drift_p90": 1.249853,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.703 | 0.679 | noisy |
| 3 | 1 | 0.224 | 0.215 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.844 | 0.803 | noisy |
| 5 | 1 | 0.545 | 0.529 | noisy |
| 5 | 2 | 0.164 | 0.164 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.893 | 0.835 | noisy |
| 7 | 1 | 0.736 | 0.711 | noisy |
| 7 | 2 | 0.438 | 0.434 | noisy |
| 7 | 3 | 0.128 | 0.128 | acceptable |
| 9 | 0 | 0.917 | 0.842 | noisy |
| 9 | 1 | 0.838 | 0.804 | noisy |
| 9 | 2 | 0.621 | 0.608 | noisy |
| 9 | 3 | 0.350 | 0.350 | noisy |

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
