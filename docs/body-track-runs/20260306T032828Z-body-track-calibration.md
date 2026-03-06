# Body Profile Calibration Report

- generated_utc: `2026-03-06T03:28:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `51`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.216 | 0.091 | loosen_duration+loosen_health | acceptable |
| standard | 0.216 | 0.091 | loosen_duration+loosen_health | acceptable |
| strict | 0.451 | 0.364 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.117647`
- observed_false_regression_rate: `0.078431`
```json
{
  "duration_drift_p90": 0.232714,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.265 | 0.143 | acceptable |
| 3 | 1 | 0.061 | 0.020 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.404 | 0.191 | noisy |
| 5 | 1 | 0.106 | 0.021 | acceptable |
| 5 | 2 | 0.000 | 0.000 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.467 | 0.156 | noisy |
| 7 | 1 | 0.222 | 0.089 | acceptable |
| 7 | 2 | 0.022 | 0.000 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.535 | 0.116 | acceptable |
| 9 | 1 | 0.279 | 0.093 | acceptable |
| 9 | 2 | 0.093 | 0.023 | acceptable |
| 9 | 3 | 0.000 | 0.000 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 7,
    "max_regressions": 2
  }
}
```
