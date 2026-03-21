# Body Profile Calibration Report

- generated_utc: `2026-03-20T23:45:16+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `226`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.504 | 0.489 | loosen_duration+tighten_health | noisy |
| standard | 0.504 | 0.489 | loosen_duration+tighten_health | noisy |
| strict | 0.832 | 0.826 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.30531`
- observed_false_regression_rate: `0.29646`
```json
{
  "duration_drift_p90": 1.115875,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.692 | 0.665 | noisy |
| 3 | 1 | 0.210 | 0.201 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.829 | 0.784 | noisy |
| 5 | 1 | 0.523 | 0.505 | noisy |
| 5 | 2 | 0.153 | 0.153 | noisy |
| 5 | 3 | 0.023 | 0.023 | acceptable |
| 7 | 0 | 0.882 | 0.818 | noisy |
| 7 | 1 | 0.714 | 0.686 | noisy |
| 7 | 2 | 0.400 | 0.395 | noisy |
| 7 | 3 | 0.127 | 0.127 | acceptable |
| 9 | 0 | 0.908 | 0.826 | noisy |
| 9 | 1 | 0.821 | 0.784 | noisy |
| 9 | 2 | 0.583 | 0.569 | noisy |
| 9 | 3 | 0.321 | 0.321 | noisy |

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
