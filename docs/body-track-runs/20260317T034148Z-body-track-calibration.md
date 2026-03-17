# Body Profile Calibration Report

- generated_utc: `2026-03-17T03:41:48+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `196`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.449 | 0.429 | loosen_duration+tighten_health | noisy |
| standard | 0.449 | 0.429 | loosen_duration+tighten_health | noisy |
| strict | 0.806 | 0.799 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.280612`
- observed_false_regression_rate: `0.270408`
```json
{
  "duration_drift_p90": 1.10586,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.655 | 0.624 | noisy |
| 3 | 1 | 0.191 | 0.180 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.802 | 0.750 | noisy |
| 5 | 1 | 0.479 | 0.458 | noisy |
| 5 | 2 | 0.141 | 0.141 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.863 | 0.789 | noisy |
| 7 | 1 | 0.679 | 0.647 | noisy |
| 7 | 2 | 0.368 | 0.363 | noisy |
| 7 | 3 | 0.105 | 0.105 | acceptable |
| 9 | 0 | 0.894 | 0.798 | noisy |
| 9 | 1 | 0.793 | 0.750 | noisy |
| 9 | 2 | 0.553 | 0.537 | noisy |
| 9 | 3 | 0.303 | 0.303 | noisy |

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
