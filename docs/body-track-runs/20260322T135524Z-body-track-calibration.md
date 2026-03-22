# Body Profile Calibration Report

- generated_utc: `2026-03-22T13:55:24+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `252`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.552 | 0.539 | loosen_duration+tighten_health | noisy |
| standard | 0.552 | 0.539 | loosen_duration+tighten_health | noisy |
| strict | 0.849 | 0.845 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313492`
- observed_false_regression_rate: `0.305556`
```json
{
  "duration_drift_p90": 1.287567,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.708 | 0.684 | noisy |
| 3 | 1 | 0.220 | 0.212 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.847 | 0.806 | noisy |
| 5 | 1 | 0.544 | 0.528 | noisy |
| 5 | 2 | 0.161 | 0.161 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.894 | 0.837 | noisy |
| 7 | 1 | 0.740 | 0.715 | noisy |
| 7 | 2 | 0.431 | 0.427 | noisy |
| 7 | 3 | 0.126 | 0.126 | acceptable |
| 9 | 0 | 0.918 | 0.844 | noisy |
| 9 | 1 | 0.840 | 0.807 | noisy |
| 9 | 2 | 0.619 | 0.607 | noisy |
| 9 | 3 | 0.344 | 0.344 | noisy |

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
