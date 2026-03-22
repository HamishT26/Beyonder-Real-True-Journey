# Body Profile Calibration Report

- generated_utc: `2026-03-22T05:14:40+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `235`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.523 | 0.509 | loosen_duration+tighten_health | noisy |
| standard | 0.523 | 0.509 | loosen_duration+tighten_health | noisy |
| strict | 0.838 | 0.833 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.310638`
- observed_false_regression_rate: `0.302128`
```json
{
  "duration_drift_p90": 1.116125,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.700 | 0.674 | noisy |
| 3 | 1 | 0.223 | 0.215 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.835 | 0.792 | noisy |
| 5 | 1 | 0.537 | 0.519 | noisy |
| 5 | 2 | 0.165 | 0.165 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.886 | 0.825 | noisy |
| 7 | 1 | 0.725 | 0.699 | noisy |
| 7 | 2 | 0.424 | 0.419 | noisy |
| 7 | 3 | 0.135 | 0.135 | acceptable |
| 9 | 0 | 0.912 | 0.833 | noisy |
| 9 | 1 | 0.828 | 0.793 | noisy |
| 9 | 2 | 0.599 | 0.586 | noisy |
| 9 | 3 | 0.348 | 0.348 | noisy |

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
