# Body Profile Calibration Report

- generated_utc: `2026-03-12T06:42:37+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `152`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.388 | 0.359 | loosen_duration+tighten_health | noisy |
| standard | 0.388 | 0.359 | loosen_duration+tighten_health | noisy |
| strict | 0.757 | 0.745 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.269737`
- observed_false_regression_rate: `0.256579`
```json
{
  "duration_drift_p90": 1.00691,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.640 | 0.600 | noisy |
| 3 | 1 | 0.173 | 0.160 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.791 | 0.723 | noisy |
| 5 | 1 | 0.439 | 0.412 | noisy |
| 5 | 2 | 0.128 | 0.128 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.836 | 0.740 | noisy |
| 7 | 1 | 0.651 | 0.610 | noisy |
| 7 | 2 | 0.336 | 0.329 | noisy |
| 7 | 3 | 0.096 | 0.096 | acceptable |
| 9 | 0 | 0.861 | 0.736 | noisy |
| 9 | 1 | 0.757 | 0.701 | noisy |
| 9 | 2 | 0.514 | 0.493 | noisy |
| 9 | 3 | 0.271 | 0.271 | noisy |

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
