# Body Profile Calibration Report

- generated_utc: `2026-03-14T08:25:21+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `170`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.382 | 0.356 | loosen_duration+tighten_health | noisy |
| standard | 0.382 | 0.356 | loosen_duration+tighten_health | noisy |
| strict | 0.776 | 0.767 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.276471`
- observed_false_regression_rate: `0.264706`
```json
{
  "duration_drift_p90": 1.101679,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.649 | 0.613 | noisy |
| 3 | 1 | 0.179 | 0.167 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.795 | 0.735 | noisy |
| 5 | 1 | 0.452 | 0.428 | noisy |
| 5 | 2 | 0.133 | 0.133 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.848 | 0.762 | noisy |
| 7 | 1 | 0.652 | 0.616 | noisy |
| 7 | 2 | 0.335 | 0.329 | noisy |
| 7 | 3 | 0.098 | 0.098 | acceptable |
| 9 | 0 | 0.877 | 0.765 | noisy |
| 9 | 1 | 0.765 | 0.716 | noisy |
| 9 | 2 | 0.506 | 0.488 | noisy |
| 9 | 3 | 0.278 | 0.278 | noisy |

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
