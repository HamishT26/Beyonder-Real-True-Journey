# Body Profile Calibration Report

- generated_utc: `2026-03-16T03:32:41+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `188`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.426 | 0.403 | loosen_duration+tighten_health | noisy |
| standard | 0.426 | 0.403 | loosen_duration+tighten_health | noisy |
| strict | 0.798 | 0.790 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.287234`
- observed_false_regression_rate: `0.276596`
```json
{
  "duration_drift_p90": 1.10377,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.667 | 0.634 | noisy |
| 3 | 1 | 0.194 | 0.183 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.810 | 0.755 | noisy |
| 5 | 1 | 0.484 | 0.462 | noisy |
| 5 | 2 | 0.141 | 0.141 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.863 | 0.786 | noisy |
| 7 | 1 | 0.681 | 0.648 | noisy |
| 7 | 2 | 0.368 | 0.363 | noisy |
| 7 | 3 | 0.110 | 0.110 | acceptable |
| 9 | 0 | 0.889 | 0.789 | noisy |
| 9 | 1 | 0.789 | 0.744 | noisy |
| 9 | 2 | 0.550 | 0.533 | noisy |
| 9 | 3 | 0.317 | 0.317 | noisy |

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
