# Body Profile Calibration Report

- generated_utc: `2026-03-12T11:28:22+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `160`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.375 | 0.346 | loosen_duration+tighten_health | noisy |
| standard | 0.375 | 0.346 | loosen_duration+tighten_health | noisy |
| strict | 0.762 | 0.752 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.2625`
- observed_false_regression_rate: `0.25`
```json
{
  "duration_drift_p90": 1.01415,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.627 | 0.589 | noisy |
| 3 | 1 | 0.165 | 0.152 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.782 | 0.718 | noisy |
| 5 | 1 | 0.429 | 0.404 | noisy |
| 5 | 2 | 0.122 | 0.122 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.838 | 0.747 | noisy |
| 7 | 1 | 0.643 | 0.604 | noisy |
| 7 | 2 | 0.325 | 0.318 | noisy |
| 7 | 3 | 0.091 | 0.091 | acceptable |
| 9 | 0 | 0.868 | 0.750 | noisy |
| 9 | 1 | 0.757 | 0.704 | noisy |
| 9 | 2 | 0.507 | 0.487 | noisy |
| 9 | 3 | 0.270 | 0.270 | noisy |

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
