# Body Profile Calibration Report

- generated_utc: `2026-03-26T02:10:49+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `325`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.634 | 0.626 | loosen_duration+tighten_health | noisy |
| standard | 0.634 | 0.626 | loosen_duration+tighten_health | noisy |
| strict | 0.883 | 0.881 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.326154`
- observed_false_regression_rate: `0.32`
```json
{
  "duration_drift_p90": 1.531964,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.728 | 0.709 | noisy |
| 3 | 1 | 0.235 | 0.229 | noisy |
| 3 | 2 | 0.019 | 0.019 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.872 | 0.841 | noisy |
| 5 | 1 | 0.564 | 0.551 | noisy |
| 5 | 2 | 0.181 | 0.181 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.915 | 0.871 | noisy |
| 7 | 1 | 0.755 | 0.737 | noisy |
| 7 | 2 | 0.458 | 0.455 | noisy |
| 7 | 3 | 0.141 | 0.141 | acceptable |
| 9 | 0 | 0.937 | 0.880 | noisy |
| 9 | 1 | 0.858 | 0.833 | noisy |
| 9 | 2 | 0.644 | 0.634 | noisy |
| 9 | 3 | 0.372 | 0.372 | noisy |

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
