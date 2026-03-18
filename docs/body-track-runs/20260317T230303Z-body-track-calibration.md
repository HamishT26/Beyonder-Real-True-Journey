# Body Profile Calibration Report

- generated_utc: `2026-03-17T23:03:03+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `204`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.466 | 0.447 | loosen_duration+tighten_health | noisy |
| standard | 0.466 | 0.447 | loosen_duration+tighten_health | noisy |
| strict | 0.814 | 0.807 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.284314`
- observed_false_regression_rate: `0.27451`
```json
{
  "duration_drift_p90": 1.107951,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.663 | 0.634 | noisy |
| 3 | 1 | 0.193 | 0.183 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.810 | 0.760 | noisy |
| 5 | 1 | 0.485 | 0.465 | noisy |
| 5 | 2 | 0.135 | 0.135 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.869 | 0.798 | noisy |
| 7 | 1 | 0.687 | 0.657 | noisy |
| 7 | 2 | 0.364 | 0.359 | noisy |
| 7 | 3 | 0.101 | 0.101 | acceptable |
| 9 | 0 | 0.898 | 0.806 | noisy |
| 9 | 1 | 0.801 | 0.760 | noisy |
| 9 | 2 | 0.546 | 0.531 | noisy |
| 9 | 3 | 0.291 | 0.291 | noisy |

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
