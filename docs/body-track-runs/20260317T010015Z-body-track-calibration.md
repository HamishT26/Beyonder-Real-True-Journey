# Body Profile Calibration Report

- generated_utc: `2026-03-17T01:00:15+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `190`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.432 | 0.410 | loosen_duration+tighten_health | noisy |
| standard | 0.432 | 0.410 | loosen_duration+tighten_health | noisy |
| strict | 0.800 | 0.792 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.289474`
- observed_false_regression_rate: `0.278947`
```json
{
  "duration_drift_p90": 1.110909,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.670 | 0.638 | noisy |
| 3 | 1 | 0.197 | 0.186 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.812 | 0.758 | noisy |
| 5 | 1 | 0.489 | 0.468 | noisy |
| 5 | 2 | 0.145 | 0.145 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.864 | 0.788 | noisy |
| 7 | 1 | 0.685 | 0.652 | noisy |
| 7 | 2 | 0.375 | 0.370 | noisy |
| 7 | 3 | 0.109 | 0.109 | acceptable |
| 9 | 0 | 0.890 | 0.791 | noisy |
| 9 | 1 | 0.791 | 0.747 | noisy |
| 9 | 2 | 0.555 | 0.538 | noisy |
| 9 | 3 | 0.313 | 0.313 | noisy |

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
