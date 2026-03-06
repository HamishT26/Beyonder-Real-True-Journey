# Body Profile Calibration Report

- generated_utc: `2026-03-06T02:27:31+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `46`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.217 | 0.077 | loosen_duration+loosen_health | acceptable |
| standard | 0.217 | 0.077 | loosen_duration+loosen_health | acceptable |
| strict | 0.435 | 0.333 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.086957`
- observed_false_regression_rate: `0.043478`
```json
{
  "duration_drift_p90": 0.179,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.227 | 0.091 | acceptable |
| 3 | 1 | 0.045 | 0.000 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.333 | 0.095 | acceptable |
| 5 | 1 | 0.095 | 0.000 | acceptable |
| 5 | 2 | 0.000 | 0.000 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.400 | 0.050 | acceptable |
| 7 | 1 | 0.175 | 0.025 | acceptable |
| 7 | 2 | 0.025 | 0.000 | acceptable |
| 7 | 3 | 0.000 | 0.000 | acceptable |
| 9 | 0 | 0.474 | 0.000 | acceptable |
| 9 | 1 | 0.211 | 0.000 | acceptable |
| 9 | 2 | 0.079 | 0.000 | acceptable |
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
