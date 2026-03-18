# Body Profile Calibration Report

- generated_utc: `2026-03-18T00:50:19+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `207`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.469 | 0.450 | loosen_duration+tighten_health | noisy |
| standard | 0.469 | 0.450 | loosen_duration+tighten_health | noisy |
| strict | 0.816 | 0.810 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.285024`
- observed_false_regression_rate: `0.275362`
```json
{
  "duration_drift_p90": 1.112209,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.663 | 0.634 | noisy |
| 3 | 1 | 0.190 | 0.180 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.813 | 0.764 | noisy |
| 5 | 1 | 0.483 | 0.463 | noisy |
| 5 | 2 | 0.133 | 0.133 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.871 | 0.801 | noisy |
| 7 | 1 | 0.687 | 0.657 | noisy |
| 7 | 2 | 0.358 | 0.353 | noisy |
| 7 | 3 | 0.100 | 0.100 | acceptable |
| 9 | 0 | 0.899 | 0.809 | noisy |
| 9 | 1 | 0.804 | 0.764 | noisy |
| 9 | 2 | 0.548 | 0.533 | noisy |
| 9 | 3 | 0.286 | 0.286 | noisy |

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
