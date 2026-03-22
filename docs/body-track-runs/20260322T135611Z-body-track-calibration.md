# Body Profile Calibration Report

- generated_utc: `2026-03-22T13:56:11+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `253`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.553 | 0.541 | loosen_duration+tighten_health | noisy |
| standard | 0.553 | 0.541 | loosen_duration+tighten_health | noisy |
| strict | 0.850 | 0.846 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.316206`
- observed_false_regression_rate: `0.3083`
```json
{
  "duration_drift_p90": 1.281281,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.709 | 0.685 | noisy |
| 3 | 1 | 0.223 | 0.215 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.847 | 0.807 | noisy |
| 5 | 1 | 0.546 | 0.530 | noisy |
| 5 | 2 | 0.165 | 0.165 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.895 | 0.838 | noisy |
| 7 | 1 | 0.741 | 0.717 | noisy |
| 7 | 2 | 0.433 | 0.429 | noisy |
| 7 | 3 | 0.126 | 0.126 | acceptable |
| 9 | 0 | 0.918 | 0.845 | noisy |
| 9 | 1 | 0.841 | 0.808 | noisy |
| 9 | 2 | 0.620 | 0.608 | noisy |
| 9 | 3 | 0.347 | 0.347 | noisy |

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
