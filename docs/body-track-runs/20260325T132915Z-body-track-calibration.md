# Body Profile Calibration Report

- generated_utc: `2026-03-25T13:29:15+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `303`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.614 | 0.605 | loosen_duration+tighten_health | noisy |
| standard | 0.614 | 0.605 | loosen_duration+tighten_health | noisy |
| strict | 0.875 | 0.872 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313531`
- observed_false_regression_rate: `0.306931`
```json
{
  "duration_drift_p90": 1.286207,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.714 | 0.694 | noisy |
| 3 | 1 | 0.219 | 0.213 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.863 | 0.829 | noisy |
| 5 | 1 | 0.535 | 0.522 | noisy |
| 5 | 2 | 0.167 | 0.167 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.909 | 0.862 | noisy |
| 7 | 1 | 0.737 | 0.717 | noisy |
| 7 | 2 | 0.431 | 0.428 | noisy |
| 7 | 3 | 0.131 | 0.131 | acceptable |
| 9 | 0 | 0.932 | 0.871 | noisy |
| 9 | 1 | 0.847 | 0.820 | noisy |
| 9 | 2 | 0.620 | 0.610 | noisy |
| 9 | 3 | 0.349 | 0.349 | noisy |

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
