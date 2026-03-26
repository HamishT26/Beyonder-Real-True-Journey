# Body Profile Calibration Report

- generated_utc: `2026-03-25T20:27:19+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `314`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.627 | 0.619 | loosen_duration+tighten_health | noisy |
| standard | 0.627 | 0.619 | loosen_duration+tighten_health | noisy |
| strict | 0.879 | 0.876 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.321656`
- observed_false_regression_rate: `0.315287`
```json
{
  "duration_drift_p90": 1.42649,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.721 | 0.702 | noisy |
| 3 | 1 | 0.224 | 0.218 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.868 | 0.835 | noisy |
| 5 | 1 | 0.548 | 0.535 | noisy |
| 5 | 2 | 0.168 | 0.168 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.912 | 0.867 | noisy |
| 7 | 1 | 0.747 | 0.727 | noisy |
| 7 | 2 | 0.442 | 0.438 | noisy |
| 7 | 3 | 0.130 | 0.130 | acceptable |
| 9 | 0 | 0.935 | 0.876 | noisy |
| 9 | 1 | 0.853 | 0.827 | noisy |
| 9 | 2 | 0.631 | 0.621 | noisy |
| 9 | 3 | 0.353 | 0.353 | noisy |

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
