# Body Profile Calibration Report

- generated_utc: `2026-03-22T20:26:31+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `259`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.564 | 0.552 | loosen_duration+tighten_health | noisy |
| standard | 0.564 | 0.552 | loosen_duration+tighten_health | noisy |
| strict | 0.853 | 0.849 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.316602`
- observed_false_regression_rate: `0.30888`
```json
{
  "duration_drift_p90": 1.369982,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.716 | 0.693 | noisy |
| 3 | 1 | 0.226 | 0.218 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.851 | 0.812 | noisy |
| 5 | 1 | 0.553 | 0.537 | noisy |
| 5 | 2 | 0.176 | 0.176 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.897 | 0.842 | noisy |
| 7 | 1 | 0.747 | 0.723 | noisy |
| 7 | 2 | 0.447 | 0.443 | noisy |
| 7 | 3 | 0.138 | 0.138 | acceptable |
| 9 | 0 | 0.920 | 0.849 | noisy |
| 9 | 1 | 0.845 | 0.813 | noisy |
| 9 | 2 | 0.629 | 0.618 | noisy |
| 9 | 3 | 0.363 | 0.363 | noisy |

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
