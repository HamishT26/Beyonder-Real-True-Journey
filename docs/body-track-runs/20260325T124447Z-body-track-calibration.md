# Body Profile Calibration Report

- generated_utc: `2026-03-25T12:44:47+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `300`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.610 | 0.601 | loosen_duration+tighten_health | noisy |
| standard | 0.610 | 0.601 | loosen_duration+tighten_health | noisy |
| strict | 0.873 | 0.870 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313333`
- observed_false_regression_rate: `0.306667`
```json
{
  "duration_drift_p90": 1.34251,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.711 | 0.691 | noisy |
| 3 | 1 | 0.221 | 0.215 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.861 | 0.828 | noisy |
| 5 | 1 | 0.541 | 0.527 | noisy |
| 5 | 2 | 0.169 | 0.169 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.908 | 0.861 | noisy |
| 7 | 1 | 0.738 | 0.718 | noisy |
| 7 | 2 | 0.435 | 0.432 | noisy |
| 7 | 3 | 0.133 | 0.133 | acceptable |
| 9 | 0 | 0.932 | 0.870 | noisy |
| 9 | 1 | 0.846 | 0.818 | noisy |
| 9 | 2 | 0.623 | 0.613 | noisy |
| 9 | 3 | 0.353 | 0.353 | noisy |

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
