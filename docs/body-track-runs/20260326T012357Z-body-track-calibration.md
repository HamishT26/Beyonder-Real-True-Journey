# Body Profile Calibration Report

- generated_utc: `2026-03-26T01:23:57+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `323`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.632 | 0.623 | loosen_duration+tighten_health | noisy |
| standard | 0.632 | 0.623 | loosen_duration+tighten_health | noisy |
| strict | 0.882 | 0.880 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.325077`
- observed_false_regression_rate: `0.318885`
```json
{
  "duration_drift_p90": 1.552176,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.726 | 0.707 | noisy |
| 3 | 1 | 0.231 | 0.224 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.871 | 0.840 | noisy |
| 5 | 1 | 0.561 | 0.549 | noisy |
| 5 | 2 | 0.176 | 0.176 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.915 | 0.871 | noisy |
| 7 | 1 | 0.754 | 0.735 | noisy |
| 7 | 2 | 0.454 | 0.451 | noisy |
| 7 | 3 | 0.136 | 0.136 | acceptable |
| 9 | 0 | 0.937 | 0.879 | noisy |
| 9 | 1 | 0.857 | 0.832 | noisy |
| 9 | 2 | 0.641 | 0.632 | noisy |
| 9 | 3 | 0.368 | 0.368 | noisy |

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
