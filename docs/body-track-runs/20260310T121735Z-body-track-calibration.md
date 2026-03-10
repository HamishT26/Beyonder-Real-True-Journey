# Body Profile Calibration Report

- generated_utc: `2026-03-10T12:17:35+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `132`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.341 | 0.304 | loosen_duration+loosen_health | noisy |
| standard | 0.341 | 0.304 | loosen_duration+loosen_health | noisy |
| strict | 0.720 | 0.704 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.272727`
- observed_false_regression_rate: `0.257576`
```json
{
  "duration_drift_p90": 1.00691,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.623 | 0.577 | noisy |
| 3 | 1 | 0.177 | 0.162 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.766 | 0.688 | noisy |
| 5 | 1 | 0.430 | 0.398 | noisy |
| 5 | 2 | 0.141 | 0.141 | acceptable |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.810 | 0.698 | noisy |
| 7 | 1 | 0.619 | 0.571 | noisy |
| 7 | 2 | 0.341 | 0.333 | noisy |
| 7 | 3 | 0.111 | 0.111 | acceptable |
| 9 | 0 | 0.839 | 0.694 | noisy |
| 9 | 1 | 0.718 | 0.653 | noisy |
| 9 | 2 | 0.492 | 0.468 | noisy |
| 9 | 3 | 0.306 | 0.306 | noisy |

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
