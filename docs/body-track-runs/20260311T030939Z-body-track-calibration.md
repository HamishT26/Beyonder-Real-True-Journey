# Body Profile Calibration Report

- generated_utc: `2026-03-11T03:09:39+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `138`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.333 | 0.298 | loosen_duration+tighten_health | noisy |
| standard | 0.333 | 0.298 | loosen_duration+loosen_health | noisy |
| strict | 0.732 | 0.718 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.268116`
- observed_false_regression_rate: `0.253623`
```json
{
  "duration_drift_p90": 1.02139,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.625 | 0.581 | noisy |
| 3 | 1 | 0.176 | 0.162 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.776 | 0.701 | noisy |
| 5 | 1 | 0.433 | 0.403 | noisy |
| 5 | 2 | 0.134 | 0.134 | acceptable |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.818 | 0.712 | noisy |
| 7 | 1 | 0.636 | 0.591 | noisy |
| 7 | 2 | 0.348 | 0.341 | noisy |
| 7 | 3 | 0.106 | 0.106 | acceptable |
| 9 | 0 | 0.846 | 0.708 | noisy |
| 9 | 1 | 0.731 | 0.669 | noisy |
| 9 | 2 | 0.515 | 0.492 | noisy |
| 9 | 3 | 0.300 | 0.300 | noisy |

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
