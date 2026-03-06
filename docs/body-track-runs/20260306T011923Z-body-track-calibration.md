# Body Profile Calibration Report

- generated_utc: `2026-03-06T01:19:23+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `44`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.227 | 0.081 | loosen_duration+loosen_health | acceptable |
| standard | 0.227 | 0.081 | loosen_duration+loosen_health | acceptable |
| strict | 0.409 | 0.297 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.090909`
- observed_false_regression_rate: `0.045455`
```json
{
  "duration_drift_p90": 0.185928,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.190 | 0.048 | acceptable |
| 3 | 1 | 0.048 | 0.000 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.300 | 0.050 | acceptable |
| 5 | 1 | 0.100 | 0.000 | acceptable |
| 5 | 2 | 0.000 | 0.000 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.368 | 0.000 | acceptable |
| 7 | 1 | 0.158 | 0.000 | acceptable |
| 7 | 2 | 0.026 | 0.000 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.444 | 0.000 | acceptable |
| 9 | 1 | 0.167 | 0.000 | acceptable |
| 9 | 2 | 0.028 | 0.000 | acceptable |
| 9 | 3 | 0.000 | 0.000 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 9,
    "max_regressions": 1
  }
}
```
