# Body Profile Calibration Report

- generated_utc: `2026-03-16T03:10:47+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `187`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.428 | 0.406 | loosen_duration+tighten_health | noisy |
| standard | 0.428 | 0.406 | loosen_duration+tighten_health | noisy |
| strict | 0.797 | 0.789 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.28877`
- observed_false_regression_rate: `0.278075`
```json
{
  "duration_drift_p90": 1.104815,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.665 | 0.632 | noisy |
| 3 | 1 | 0.195 | 0.184 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.809 | 0.754 | noisy |
| 5 | 1 | 0.481 | 0.459 | noisy |
| 5 | 2 | 0.142 | 0.142 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.862 | 0.785 | noisy |
| 7 | 1 | 0.680 | 0.646 | noisy |
| 7 | 2 | 0.370 | 0.365 | noisy |
| 7 | 3 | 0.110 | 0.110 | acceptable |
| 9 | 0 | 0.888 | 0.788 | noisy |
| 9 | 1 | 0.788 | 0.743 | noisy |
| 9 | 2 | 0.553 | 0.536 | noisy |
| 9 | 3 | 0.318 | 0.318 | noisy |

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
