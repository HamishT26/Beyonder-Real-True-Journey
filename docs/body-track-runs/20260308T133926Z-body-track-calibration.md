# Body Profile Calibration Report

- generated_utc: `2026-03-08T13:39:26+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `107`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.299 | 0.250 | loosen_duration+loosen_health | noisy |
| standard | 0.299 | 0.250 | loosen_duration+loosen_health | noisy |
| strict | 0.673 | 0.650 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.242991`
- observed_false_regression_rate: `0.224299`
```json
{
  "duration_drift_p90": 0.856765,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.543 | 0.486 | noisy |
| 3 | 1 | 0.171 | 0.152 | noisy |
| 3 | 2 | 0.010 | 0.010 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.709 | 0.612 | noisy |
| 5 | 1 | 0.330 | 0.291 | noisy |
| 5 | 2 | 0.136 | 0.136 | acceptable |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.762 | 0.624 | noisy |
| 7 | 1 | 0.525 | 0.465 | noisy |
| 7 | 2 | 0.248 | 0.238 | noisy |
| 7 | 3 | 0.119 | 0.119 | acceptable |
| 9 | 0 | 0.798 | 0.616 | noisy |
| 9 | 1 | 0.646 | 0.566 | noisy |
| 9 | 2 | 0.364 | 0.333 | noisy |
| 9 | 3 | 0.222 | 0.222 | noisy |

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
