# Body Profile Calibration Report

- generated_utc: `2026-03-26T04:34:24+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `331`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.640 | 0.633 | loosen_duration+tighten_health | noisy |
| standard | 0.640 | 0.633 | loosen_duration+tighten_health | noisy |
| strict | 0.885 | 0.883 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.329305`
- observed_false_regression_rate: `0.323263`
```json
{
  "duration_drift_p90": 1.61742,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.733 | 0.714 | noisy |
| 3 | 1 | 0.240 | 0.234 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.875 | 0.844 | noisy |
| 5 | 1 | 0.572 | 0.560 | noisy |
| 5 | 2 | 0.193 | 0.193 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.917 | 0.874 | noisy |
| 7 | 1 | 0.760 | 0.742 | noisy |
| 7 | 2 | 0.468 | 0.465 | noisy |
| 7 | 3 | 0.151 | 0.151 | noisy |
| 9 | 0 | 0.938 | 0.882 | noisy |
| 9 | 1 | 0.861 | 0.836 | noisy |
| 9 | 2 | 0.650 | 0.641 | noisy |
| 9 | 3 | 0.384 | 0.384 | noisy |

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
