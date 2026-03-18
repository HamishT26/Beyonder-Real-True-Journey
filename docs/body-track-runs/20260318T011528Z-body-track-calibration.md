# Body Profile Calibration Report

- generated_utc: `2026-03-18T01:15:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `208`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.471 | 0.453 | loosen_duration+tighten_health | noisy |
| standard | 0.471 | 0.453 | loosen_duration+tighten_health | noisy |
| strict | 0.817 | 0.811 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.283654`
- observed_false_regression_rate: `0.274038`
```json
{
  "duration_drift_p90": 1.111776,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.665 | 0.636 | noisy |
| 3 | 1 | 0.189 | 0.180 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.814 | 0.765 | noisy |
| 5 | 1 | 0.480 | 0.461 | noisy |
| 5 | 2 | 0.132 | 0.132 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.871 | 0.802 | noisy |
| 7 | 1 | 0.688 | 0.658 | noisy |
| 7 | 2 | 0.356 | 0.351 | noisy |
| 7 | 3 | 0.099 | 0.099 | acceptable |
| 9 | 0 | 0.900 | 0.810 | noisy |
| 9 | 1 | 0.805 | 0.765 | noisy |
| 9 | 2 | 0.545 | 0.530 | noisy |
| 9 | 3 | 0.285 | 0.285 | noisy |

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
