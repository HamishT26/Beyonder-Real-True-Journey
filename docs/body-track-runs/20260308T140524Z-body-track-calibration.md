# Body Profile Calibration Report

- generated_utc: `2026-03-08T14:05:24+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `109`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.312 | 0.265 | loosen_duration+loosen_health | noisy |
| standard | 0.312 | 0.265 | loosen_duration+loosen_health | noisy |
| strict | 0.679 | 0.657 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.238532`
- observed_false_regression_rate: `0.220183`
```json
{
  "duration_drift_p90": 0.850019,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.551 | 0.495 | noisy |
| 3 | 1 | 0.168 | 0.150 | acceptable |
| 3 | 2 | 0.009 | 0.009 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.714 | 0.619 | noisy |
| 5 | 1 | 0.343 | 0.305 | noisy |
| 5 | 2 | 0.143 | 0.143 | acceptable |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.767 | 0.631 | noisy |
| 7 | 1 | 0.534 | 0.476 | noisy |
| 7 | 2 | 0.262 | 0.252 | noisy |
| 7 | 3 | 0.117 | 0.117 | acceptable |
| 9 | 0 | 0.802 | 0.624 | noisy |
| 9 | 1 | 0.653 | 0.574 | noisy |
| 9 | 2 | 0.376 | 0.347 | noisy |
| 9 | 3 | 0.238 | 0.238 | noisy |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 3
  }
}
```
