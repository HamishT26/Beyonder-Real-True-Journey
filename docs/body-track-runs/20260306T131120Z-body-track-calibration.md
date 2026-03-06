# Body Profile Calibration Report

- generated_utc: `2026-03-06T13:11:20+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `77`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.208 | 0.129 | loosen_duration+loosen_health | acceptable |
| standard | 0.208 | 0.129 | loosen_duration+loosen_health | acceptable |
| strict | 0.558 | 0.514 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.168831`
- observed_false_regression_rate: `0.142857`
```json
{
  "duration_drift_p90": 0.308123,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.413 | 0.333 | noisy |
| 3 | 1 | 0.107 | 0.080 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.589 | 0.452 | noisy |
| 5 | 1 | 0.219 | 0.164 | noisy |
| 5 | 2 | 0.082 | 0.082 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.662 | 0.465 | noisy |
| 7 | 1 | 0.380 | 0.296 | noisy |
| 7 | 2 | 0.183 | 0.169 | noisy |
| 7 | 3 | 0.056 | 0.056 | acceptable |
| 9 | 0 | 0.710 | 0.449 | noisy |
| 9 | 1 | 0.493 | 0.377 | noisy |
| 9 | 2 | 0.275 | 0.232 | noisy |
| 9 | 3 | 0.145 | 0.145 | acceptable |

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
