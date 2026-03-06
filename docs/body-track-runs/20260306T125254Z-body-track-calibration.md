# Body Profile Calibration Report

- generated_utc: `2026-03-06T12:52:54+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `67`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.194 | 0.100 | loosen_duration+loosen_health | acceptable |
| standard | 0.194 | 0.100 | loosen_duration+loosen_health | acceptable |
| strict | 0.507 | 0.450 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.179104`
- observed_false_regression_rate: `0.149254`
```json
{
  "duration_drift_p90": 0.308123,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.415 | 0.323 | noisy |
| 3 | 1 | 0.123 | 0.092 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.556 | 0.397 | noisy |
| 5 | 1 | 0.254 | 0.190 | noisy |
| 5 | 2 | 0.095 | 0.095 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.607 | 0.377 | noisy |
| 7 | 1 | 0.410 | 0.311 | noisy |
| 7 | 2 | 0.213 | 0.197 | noisy |
| 7 | 3 | 0.066 | 0.066 | acceptable |
| 9 | 0 | 0.661 | 0.356 | noisy |
| 9 | 1 | 0.475 | 0.339 | noisy |
| 9 | 2 | 0.322 | 0.271 | noisy |
| 9 | 3 | 0.169 | 0.169 | noisy |

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
