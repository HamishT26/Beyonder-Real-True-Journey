# Body Profile Calibration Report

- generated_utc: `2026-03-17T07:09:15+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `197`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.452 | 0.432 | loosen_duration+tighten_health | noisy |
| standard | 0.452 | 0.432 | loosen_duration+tighten_health | noisy |
| strict | 0.807 | 0.800 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.284264`
- observed_false_regression_rate: `0.274112`
```json
{
  "duration_drift_p90": 1.104815,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.656 | 0.626 | noisy |
| 3 | 1 | 0.190 | 0.179 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.803 | 0.751 | noisy |
| 5 | 1 | 0.477 | 0.456 | noisy |
| 5 | 2 | 0.140 | 0.140 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.864 | 0.791 | noisy |
| 7 | 1 | 0.675 | 0.644 | noisy |
| 7 | 2 | 0.366 | 0.361 | noisy |
| 7 | 3 | 0.105 | 0.105 | acceptable |
| 9 | 0 | 0.894 | 0.799 | noisy |
| 9 | 1 | 0.794 | 0.751 | noisy |
| 9 | 2 | 0.550 | 0.534 | noisy |
| 9 | 3 | 0.302 | 0.302 | noisy |

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
