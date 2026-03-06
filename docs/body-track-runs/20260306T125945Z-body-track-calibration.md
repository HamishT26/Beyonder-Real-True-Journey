# Body Profile Calibration Report

- generated_utc: `2026-03-06T12:59:45+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `70`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.186 | 0.095 | loosen_duration+loosen_health | acceptable |
| standard | 0.186 | 0.095 | loosen_duration+loosen_health | acceptable |
| strict | 0.514 | 0.460 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.171429`
- observed_false_regression_rate: `0.142857`
```json
{
  "duration_drift_p90": 0.297669,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.412 | 0.324 | noisy |
| 3 | 1 | 0.118 | 0.088 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.576 | 0.424 | noisy |
| 5 | 1 | 0.242 | 0.182 | noisy |
| 5 | 2 | 0.091 | 0.091 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.625 | 0.406 | noisy |
| 7 | 1 | 0.391 | 0.297 | noisy |
| 7 | 2 | 0.203 | 0.188 | noisy |
| 7 | 3 | 0.062 | 0.062 | acceptable |
| 9 | 0 | 0.677 | 0.387 | noisy |
| 9 | 1 | 0.484 | 0.355 | noisy |
| 9 | 2 | 0.306 | 0.258 | noisy |
| 9 | 3 | 0.161 | 0.161 | noisy |

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
