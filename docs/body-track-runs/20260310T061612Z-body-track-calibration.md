# Body Profile Calibration Report

- generated_utc: `2026-03-10T06:16:12+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `120`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.358 | 0.319 | loosen_duration+loosen_health | noisy |
| standard | 0.358 | 0.319 | loosen_duration+loosen_health | noisy |
| strict | 0.708 | 0.690 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.258333`
- observed_false_regression_rate: `0.241667`
```json
{
  "duration_drift_p90": 1.01415,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.593 | 0.542 | noisy |
| 3 | 1 | 0.178 | 0.161 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.741 | 0.655 | noisy |
| 5 | 1 | 0.397 | 0.362 | noisy |
| 5 | 2 | 0.147 | 0.147 | acceptable |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.789 | 0.667 | noisy |
| 7 | 1 | 0.579 | 0.526 | noisy |
| 7 | 2 | 0.325 | 0.316 | noisy |
| 7 | 3 | 0.123 | 0.123 | acceptable |
| 9 | 0 | 0.821 | 0.661 | noisy |
| 9 | 1 | 0.688 | 0.616 | noisy |
| 9 | 2 | 0.438 | 0.411 | noisy |
| 9 | 3 | 0.304 | 0.304 | noisy |

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
