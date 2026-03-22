# Body Profile Calibration Report

- generated_utc: `2026-03-22T18:54:42+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `254`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.555 | 0.543 | loosen_duration+tighten_health | noisy |
| standard | 0.555 | 0.543 | loosen_duration+tighten_health | noisy |
| strict | 0.850 | 0.846 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.318898`
- observed_false_regression_rate: `0.311024`
```json
{
  "duration_drift_p90": 1.507339,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.710 | 0.687 | noisy |
| 3 | 1 | 0.226 | 0.218 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.848 | 0.808 | noisy |
| 5 | 1 | 0.548 | 0.532 | noisy |
| 5 | 2 | 0.168 | 0.168 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.895 | 0.839 | noisy |
| 7 | 1 | 0.742 | 0.718 | noisy |
| 7 | 2 | 0.435 | 0.431 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.919 | 0.846 | noisy |
| 9 | 1 | 0.841 | 0.809 | noisy |
| 9 | 2 | 0.622 | 0.610 | noisy |
| 9 | 3 | 0.350 | 0.350 | noisy |

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
