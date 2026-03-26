# Body Profile Calibration Report

- generated_utc: `2026-03-25T23:10:05+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `318`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.629 | 0.621 | loosen_duration+tighten_health | noisy |
| standard | 0.629 | 0.621 | loosen_duration+tighten_health | noisy |
| strict | 0.881 | 0.878 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.320755`
- observed_false_regression_rate: `0.314465`
```json
{
  "duration_drift_p90": 1.501645,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.722 | 0.703 | noisy |
| 3 | 1 | 0.225 | 0.218 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.869 | 0.838 | noisy |
| 5 | 1 | 0.554 | 0.541 | noisy |
| 5 | 2 | 0.172 | 0.172 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.913 | 0.869 | noisy |
| 7 | 1 | 0.750 | 0.731 | noisy |
| 7 | 2 | 0.449 | 0.446 | noisy |
| 7 | 3 | 0.131 | 0.131 | acceptable |
| 9 | 0 | 0.935 | 0.877 | noisy |
| 9 | 1 | 0.855 | 0.829 | noisy |
| 9 | 2 | 0.635 | 0.626 | noisy |
| 9 | 3 | 0.358 | 0.358 | noisy |

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
