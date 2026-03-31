# Body Profile Calibration Report

- generated_utc: `2026-03-31T00:59:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `334`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.641 | 0.633 | loosen_duration+tighten_health | noisy |
| standard | 0.641 | 0.633 | loosen_duration+tighten_health | noisy |
| strict | 0.886 | 0.884 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.329341`
- observed_false_regression_rate: `0.323353`
```json
{
  "duration_drift_p90": 1.605388,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.735 | 0.717 | noisy |
| 3 | 1 | 0.238 | 0.232 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.876 | 0.845 | noisy |
| 5 | 1 | 0.576 | 0.564 | noisy |
| 5 | 2 | 0.191 | 0.191 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.918 | 0.875 | noisy |
| 7 | 1 | 0.762 | 0.744 | noisy |
| 7 | 2 | 0.473 | 0.470 | noisy |
| 7 | 3 | 0.152 | 0.152 | noisy |
| 9 | 0 | 0.939 | 0.883 | noisy |
| 9 | 1 | 0.862 | 0.837 | noisy |
| 9 | 2 | 0.653 | 0.644 | noisy |
| 9 | 3 | 0.390 | 0.390 | noisy |

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
