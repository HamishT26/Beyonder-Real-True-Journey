# Body Profile Calibration Report

- generated_utc: `2026-03-06T12:55:52+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `68`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.191 | 0.098 | loosen_duration+loosen_health | acceptable |
| standard | 0.191 | 0.098 | loosen_duration+loosen_health | acceptable |
| strict | 0.515 | 0.459 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.176471`
- observed_false_regression_rate: `0.147059`
```json
{
  "duration_drift_p90": 0.304639,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.424 | 0.333 | noisy |
| 3 | 1 | 0.121 | 0.091 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.562 | 0.406 | noisy |
| 5 | 1 | 0.250 | 0.188 | noisy |
| 5 | 2 | 0.094 | 0.094 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.613 | 0.387 | noisy |
| 7 | 1 | 0.403 | 0.306 | noisy |
| 7 | 2 | 0.210 | 0.194 | noisy |
| 7 | 3 | 0.065 | 0.065 | acceptable |
| 9 | 0 | 0.667 | 0.367 | noisy |
| 9 | 1 | 0.483 | 0.350 | noisy |
| 9 | 2 | 0.317 | 0.267 | noisy |
| 9 | 3 | 0.167 | 0.167 | noisy |

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
