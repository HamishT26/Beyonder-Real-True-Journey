# Body Profile Calibration Report

- generated_utc: `2026-03-23T04:27:40+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `274`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.584 | 0.573 | loosen_duration+tighten_health | noisy |
| standard | 0.584 | 0.573 | loosen_duration+tighten_health | noisy |
| strict | 0.861 | 0.858 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313869`
- observed_false_regression_rate: `0.306569`
```json
{
  "duration_drift_p90": 1.274996,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.710 | 0.688 | noisy |
| 3 | 1 | 0.221 | 0.213 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.859 | 0.822 | noisy |
| 5 | 1 | 0.537 | 0.522 | noisy |
| 5 | 2 | 0.167 | 0.167 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.903 | 0.851 | noisy |
| 7 | 1 | 0.746 | 0.724 | noisy |
| 7 | 2 | 0.429 | 0.425 | noisy |
| 7 | 3 | 0.131 | 0.131 | acceptable |
| 9 | 0 | 0.925 | 0.857 | noisy |
| 9 | 1 | 0.850 | 0.820 | noisy |
| 9 | 2 | 0.624 | 0.613 | noisy |
| 9 | 3 | 0.346 | 0.346 | noisy |

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
