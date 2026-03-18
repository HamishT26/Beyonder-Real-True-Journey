# Body Profile Calibration Report

- generated_utc: `2026-03-17T22:38:46+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `203`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.463 | 0.444 | loosen_duration+tighten_health | noisy |
| standard | 0.463 | 0.444 | loosen_duration+tighten_health | noisy |
| strict | 0.813 | 0.806 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.285714`
- observed_false_regression_rate: `0.275862`
```json
{
  "duration_drift_p90": 1.108997,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.662 | 0.632 | noisy |
| 3 | 1 | 0.194 | 0.184 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.809 | 0.759 | noisy |
| 5 | 1 | 0.487 | 0.467 | noisy |
| 5 | 2 | 0.136 | 0.136 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.868 | 0.797 | noisy |
| 7 | 1 | 0.685 | 0.655 | noisy |
| 7 | 2 | 0.365 | 0.360 | noisy |
| 7 | 3 | 0.102 | 0.102 | acceptable |
| 9 | 0 | 0.897 | 0.805 | noisy |
| 9 | 1 | 0.800 | 0.759 | noisy |
| 9 | 2 | 0.544 | 0.528 | noisy |
| 9 | 3 | 0.292 | 0.292 | noisy |

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
