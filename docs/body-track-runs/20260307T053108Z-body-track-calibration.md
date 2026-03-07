# Body Profile Calibration Report

- generated_utc: `2026-03-07T05:31:08+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `87`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.195 | 0.125 | loosen_duration+loosen_health | acceptable |
| standard | 0.195 | 0.125 | loosen_duration+loosen_health | acceptable |
| strict | 0.598 | 0.562 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.183908`
- observed_false_regression_rate: `0.16092`
```json
{
  "duration_drift_p90": 0.349117,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.459 | 0.388 | noisy |
| 3 | 1 | 0.106 | 0.082 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.639 | 0.518 | noisy |
| 5 | 1 | 0.229 | 0.181 | noisy |
| 5 | 2 | 0.072 | 0.072 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.704 | 0.531 | noisy |
| 7 | 1 | 0.420 | 0.346 | noisy |
| 7 | 2 | 0.160 | 0.148 | acceptable |
| 7 | 3 | 0.049 | 0.049 | acceptable |
| 9 | 0 | 0.747 | 0.519 | noisy |
| 9 | 1 | 0.557 | 0.456 | noisy |
| 9 | 2 | 0.266 | 0.228 | noisy |
| 9 | 3 | 0.127 | 0.127 | acceptable |

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
