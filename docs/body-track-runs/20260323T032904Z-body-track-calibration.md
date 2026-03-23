# Body Profile Calibration Report

- generated_utc: `2026-03-23T03:29:04+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `270`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.581 | 0.570 | loosen_duration+tighten_health | noisy |
| standard | 0.581 | 0.570 | loosen_duration+tighten_health | noisy |
| strict | 0.859 | 0.856 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.314815`
- observed_false_regression_rate: `0.307407`
```json
{
  "duration_drift_p90": 1.34251,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.713 | 0.690 | noisy |
| 3 | 1 | 0.224 | 0.216 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.857 | 0.820 | noisy |
| 5 | 1 | 0.541 | 0.526 | noisy |
| 5 | 2 | 0.169 | 0.169 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.902 | 0.848 | noisy |
| 7 | 1 | 0.742 | 0.720 | noisy |
| 7 | 2 | 0.432 | 0.428 | noisy |
| 7 | 3 | 0.133 | 0.133 | acceptable |
| 9 | 0 | 0.924 | 0.855 | noisy |
| 9 | 1 | 0.847 | 0.817 | noisy |
| 9 | 2 | 0.626 | 0.615 | noisy |
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
