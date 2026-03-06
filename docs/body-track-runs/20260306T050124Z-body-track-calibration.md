# Body Profile Calibration Report

- generated_utc: `2026-03-06T05:01:24+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `64`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.188 | 0.088 | loosen_duration+loosen_health | acceptable |
| standard | 0.188 | 0.088 | loosen_duration+loosen_health | acceptable |
| strict | 0.500 | 0.439 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.171875`
- observed_false_regression_rate: `0.140625`
```json
{
  "duration_drift_p90": 0.287381,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.403 | 0.306 | noisy |
| 3 | 1 | 0.129 | 0.097 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.533 | 0.367 | noisy |
| 5 | 1 | 0.267 | 0.200 | noisy |
| 5 | 2 | 0.100 | 0.100 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.586 | 0.345 | noisy |
| 7 | 1 | 0.397 | 0.293 | noisy |
| 7 | 2 | 0.224 | 0.207 | noisy |
| 7 | 3 | 0.069 | 0.069 | acceptable |
| 9 | 0 | 0.643 | 0.321 | noisy |
| 9 | 1 | 0.446 | 0.304 | noisy |
| 9 | 2 | 0.304 | 0.250 | noisy |
| 9 | 3 | 0.179 | 0.179 | noisy |

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
