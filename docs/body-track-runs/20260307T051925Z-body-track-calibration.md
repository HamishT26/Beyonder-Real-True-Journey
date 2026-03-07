# Body Profile Calibration Report

- generated_utc: `2026-03-07T05:19:25+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `84`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.202 | 0.130 | loosen_duration+loosen_health | acceptable |
| standard | 0.202 | 0.130 | loosen_duration+loosen_health | acceptable |
| strict | 0.583 | 0.545 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.178571`
- observed_false_regression_rate: `0.154762`
```json
{
  "duration_drift_p90": 0.318578,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.439 | 0.366 | noisy |
| 3 | 1 | 0.110 | 0.085 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.625 | 0.500 | noisy |
| 5 | 1 | 0.237 | 0.188 | noisy |
| 5 | 2 | 0.075 | 0.075 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.692 | 0.513 | noisy |
| 7 | 1 | 0.410 | 0.333 | noisy |
| 7 | 2 | 0.167 | 0.154 | noisy |
| 7 | 3 | 0.051 | 0.051 | acceptable |
| 9 | 0 | 0.737 | 0.500 | noisy |
| 9 | 1 | 0.539 | 0.434 | noisy |
| 9 | 2 | 0.250 | 0.211 | noisy |
| 9 | 3 | 0.132 | 0.132 | acceptable |

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
