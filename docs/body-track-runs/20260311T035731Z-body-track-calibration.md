# Body Profile Calibration Report

- generated_utc: `2026-03-11T03:57:31+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `141`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.340 | 0.306 | loosen_duration+tighten_health | noisy |
| standard | 0.340 | 0.306 | loosen_duration+tighten_health | noisy |
| strict | 0.738 | 0.724 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.269504`
- observed_false_regression_rate: `0.255319`
```json
{
  "duration_drift_p90": 1.01053,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.633 | 0.590 | noisy |
| 3 | 1 | 0.173 | 0.158 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.781 | 0.708 | noisy |
| 5 | 1 | 0.438 | 0.409 | noisy |
| 5 | 2 | 0.131 | 0.131 | acceptable |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.822 | 0.719 | noisy |
| 7 | 1 | 0.637 | 0.593 | noisy |
| 7 | 2 | 0.341 | 0.333 | noisy |
| 7 | 3 | 0.104 | 0.104 | acceptable |
| 9 | 0 | 0.850 | 0.714 | noisy |
| 9 | 1 | 0.737 | 0.677 | noisy |
| 9 | 2 | 0.519 | 0.496 | noisy |
| 9 | 3 | 0.293 | 0.293 | noisy |

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
