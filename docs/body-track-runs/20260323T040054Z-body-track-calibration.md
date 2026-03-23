# Body Profile Calibration Report

- generated_utc: `2026-03-23T04:00:54+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `272`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.581 | 0.570 | loosen_duration+tighten_health | noisy |
| standard | 0.581 | 0.570 | loosen_duration+tighten_health | noisy |
| strict | 0.860 | 0.857 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.3125`
- observed_false_regression_rate: `0.305147`
```json
{
  "duration_drift_p90": 1.287567,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.707 | 0.685 | noisy |
| 3 | 1 | 0.222 | 0.215 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.858 | 0.821 | noisy |
| 5 | 1 | 0.541 | 0.526 | noisy |
| 5 | 2 | 0.168 | 0.168 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.902 | 0.850 | noisy |
| 7 | 1 | 0.744 | 0.722 | noisy |
| 7 | 2 | 0.429 | 0.425 | noisy |
| 7 | 3 | 0.132 | 0.132 | acceptable |
| 9 | 0 | 0.924 | 0.856 | noisy |
| 9 | 1 | 0.848 | 0.818 | noisy |
| 9 | 2 | 0.621 | 0.610 | noisy |
| 9 | 3 | 0.348 | 0.348 | noisy |

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
