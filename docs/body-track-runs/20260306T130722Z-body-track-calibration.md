# Body Profile Calibration Report

- generated_utc: `2026-03-06T13:07:22+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `75`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.213 | 0.132 | loosen_duration+loosen_health | acceptable |
| standard | 0.213 | 0.132 | loosen_duration+loosen_health | acceptable |
| strict | 0.547 | 0.500 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.173333`
- observed_false_regression_rate: `0.146667`
```json
{
  "duration_drift_p90": 0.315093,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.425 | 0.342 | noisy |
| 3 | 1 | 0.110 | 0.082 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.606 | 0.465 | noisy |
| 5 | 1 | 0.225 | 0.169 | noisy |
| 5 | 2 | 0.085 | 0.085 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.652 | 0.449 | noisy |
| 7 | 1 | 0.391 | 0.304 | noisy |
| 7 | 2 | 0.188 | 0.174 | noisy |
| 7 | 3 | 0.058 | 0.058 | acceptable |
| 9 | 0 | 0.701 | 0.433 | noisy |
| 9 | 1 | 0.507 | 0.388 | noisy |
| 9 | 2 | 0.284 | 0.239 | noisy |
| 9 | 3 | 0.149 | 0.149 | acceptable |

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
