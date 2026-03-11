# Body Profile Calibration Report

- generated_utc: `2026-03-11T03:42:51+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `140`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.336 | 0.301 | loosen_duration+tighten_health | noisy |
| standard | 0.336 | 0.301 | loosen_duration+tighten_health | noisy |
| strict | 0.736 | 0.722 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.271429`
- observed_false_regression_rate: `0.257143`
```json
{
  "duration_drift_p90": 1.01415,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.630 | 0.587 | noisy |
| 3 | 1 | 0.174 | 0.159 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.779 | 0.706 | noisy |
| 5 | 1 | 0.434 | 0.404 | noisy |
| 5 | 2 | 0.132 | 0.132 | acceptable |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.821 | 0.716 | noisy |
| 7 | 1 | 0.634 | 0.590 | noisy |
| 7 | 2 | 0.343 | 0.336 | noisy |
| 7 | 3 | 0.104 | 0.104 | acceptable |
| 9 | 0 | 0.848 | 0.712 | noisy |
| 9 | 1 | 0.735 | 0.674 | noisy |
| 9 | 2 | 0.523 | 0.500 | noisy |
| 9 | 3 | 0.295 | 0.295 | noisy |

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
