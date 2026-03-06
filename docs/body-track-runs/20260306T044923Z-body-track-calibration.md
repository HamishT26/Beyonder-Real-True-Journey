# Body Profile Calibration Report

- generated_utc: `2026-03-06T04:49:23+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `56`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.214 | 0.102 | loosen_duration+loosen_health | acceptable |
| standard | 0.214 | 0.102 | loosen_duration+loosen_health | acceptable |
| strict | 0.482 | 0.408 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.142857`
- observed_false_regression_rate: `0.107143`
```json
{
  "duration_drift_p90": 0.295463,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.333 | 0.222 | noisy |
| 3 | 1 | 0.093 | 0.056 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.462 | 0.269 | noisy |
| 5 | 1 | 0.192 | 0.115 | acceptable |
| 5 | 2 | 0.058 | 0.058 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.520 | 0.240 | noisy |
| 7 | 1 | 0.300 | 0.180 | noisy |
| 7 | 2 | 0.120 | 0.100 | acceptable |
| 7 | 3 | 0.020 | 0.020 | acceptable |
| 9 | 0 | 0.583 | 0.208 | noisy |
| 9 | 1 | 0.354 | 0.188 | noisy |
| 9 | 2 | 0.188 | 0.125 | acceptable |
| 9 | 3 | 0.062 | 0.062 | acceptable |

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
