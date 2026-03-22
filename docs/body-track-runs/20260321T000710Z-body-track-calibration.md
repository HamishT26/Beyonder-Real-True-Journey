# Body Profile Calibration Report

- generated_utc: `2026-03-21T00:07:10+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `227`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.507 | 0.491 | loosen_duration+tighten_health | noisy |
| standard | 0.507 | 0.491 | loosen_duration+tighten_health | noisy |
| strict | 0.833 | 0.827 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.30837`
- observed_false_regression_rate: `0.299559`
```json
{
  "duration_drift_p90": 1.166775,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.693 | 0.667 | noisy |
| 3 | 1 | 0.213 | 0.204 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.830 | 0.785 | noisy |
| 5 | 1 | 0.525 | 0.507 | noisy |
| 5 | 2 | 0.157 | 0.157 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.882 | 0.819 | noisy |
| 7 | 1 | 0.715 | 0.688 | noisy |
| 7 | 2 | 0.403 | 0.398 | noisy |
| 7 | 3 | 0.131 | 0.131 | acceptable |
| 9 | 0 | 0.909 | 0.826 | noisy |
| 9 | 1 | 0.822 | 0.785 | noisy |
| 9 | 2 | 0.584 | 0.571 | noisy |
| 9 | 3 | 0.324 | 0.324 | noisy |

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
