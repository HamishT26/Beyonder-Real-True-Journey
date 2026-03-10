# Body Profile Calibration Report

- generated_utc: `2026-03-07T08:04:31+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `89`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.202 | 0.134 | loosen_duration+loosen_health | acceptable |
| standard | 0.202 | 0.134 | loosen_duration+loosen_health | acceptable |
| strict | 0.607 | 0.573 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.191011`
- observed_false_regression_rate: `0.168539`
```json
{
  "duration_drift_p90": 0.385542,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.471 | 0.402 | noisy |
| 3 | 1 | 0.103 | 0.080 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.647 | 0.529 | noisy |
| 5 | 1 | 0.247 | 0.200 | noisy |
| 5 | 2 | 0.071 | 0.071 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.711 | 0.542 | noisy |
| 7 | 1 | 0.434 | 0.361 | noisy |
| 7 | 2 | 0.157 | 0.145 | acceptable |
| 7 | 3 | 0.048 | 0.048 | acceptable |
| 9 | 0 | 0.753 | 0.531 | noisy |
| 9 | 1 | 0.568 | 0.469 | noisy |
| 9 | 2 | 0.272 | 0.235 | noisy |
| 9 | 3 | 0.123 | 0.123 | acceptable |

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
