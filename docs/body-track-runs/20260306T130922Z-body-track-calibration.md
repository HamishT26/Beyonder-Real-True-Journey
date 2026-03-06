# Body Profile Calibration Report

- generated_utc: `2026-03-06T13:09:22+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `76`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.211 | 0.130 | loosen_duration+loosen_health | acceptable |
| standard | 0.211 | 0.130 | loosen_duration+loosen_health | acceptable |
| strict | 0.553 | 0.507 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.171053`
- observed_false_regression_rate: `0.144737`
```json
{
  "duration_drift_p90": 0.311608,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.419 | 0.338 | noisy |
| 3 | 1 | 0.108 | 0.081 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.597 | 0.458 | noisy |
| 5 | 1 | 0.222 | 0.167 | noisy |
| 5 | 2 | 0.083 | 0.083 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.657 | 0.457 | noisy |
| 7 | 1 | 0.386 | 0.300 | noisy |
| 7 | 2 | 0.186 | 0.171 | noisy |
| 7 | 3 | 0.057 | 0.057 | acceptable |
| 9 | 0 | 0.706 | 0.441 | noisy |
| 9 | 1 | 0.500 | 0.382 | noisy |
| 9 | 2 | 0.279 | 0.235 | noisy |
| 9 | 3 | 0.147 | 0.147 | acceptable |

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
