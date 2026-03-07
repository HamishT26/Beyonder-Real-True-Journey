# Body Profile Calibration Report

- generated_utc: `2026-03-07T05:33:23+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `88`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.205 | 0.136 | loosen_duration+loosen_health | acceptable |
| standard | 0.205 | 0.136 | loosen_duration+loosen_health | acceptable |
| strict | 0.602 | 0.568 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.193182`
- observed_false_regression_rate: `0.170455`
```json
{
  "duration_drift_p90": 0.389827,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.465 | 0.395 | noisy |
| 3 | 1 | 0.105 | 0.081 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.643 | 0.524 | noisy |
| 5 | 1 | 0.238 | 0.190 | noisy |
| 5 | 2 | 0.071 | 0.071 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.707 | 0.537 | noisy |
| 7 | 1 | 0.427 | 0.354 | noisy |
| 7 | 2 | 0.159 | 0.146 | acceptable |
| 7 | 3 | 0.049 | 0.049 | acceptable |
| 9 | 0 | 0.750 | 0.525 | noisy |
| 9 | 1 | 0.562 | 0.463 | noisy |
| 9 | 2 | 0.275 | 0.237 | noisy |
| 9 | 3 | 0.125 | 0.125 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 2
  }
}
```
