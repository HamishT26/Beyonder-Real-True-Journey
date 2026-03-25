# Body Profile Calibration Report

- generated_utc: `2026-03-25T14:04:29+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `305`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.616 | 0.607 | loosen_duration+tighten_health | noisy |
| standard | 0.616 | 0.607 | loosen_duration+tighten_health | noisy |
| strict | 0.875 | 0.872 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.314754`
- observed_false_regression_rate: `0.308197`
```json
{
  "duration_drift_p90": 1.283488,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.716 | 0.696 | noisy |
| 3 | 1 | 0.218 | 0.211 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.864 | 0.831 | noisy |
| 5 | 1 | 0.538 | 0.525 | noisy |
| 5 | 2 | 0.166 | 0.166 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.910 | 0.863 | noisy |
| 7 | 1 | 0.739 | 0.719 | noisy |
| 7 | 2 | 0.428 | 0.425 | noisy |
| 7 | 3 | 0.130 | 0.130 | acceptable |
| 9 | 0 | 0.933 | 0.872 | noisy |
| 9 | 1 | 0.848 | 0.822 | noisy |
| 9 | 2 | 0.620 | 0.609 | noisy |
| 9 | 3 | 0.347 | 0.347 | noisy |

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
