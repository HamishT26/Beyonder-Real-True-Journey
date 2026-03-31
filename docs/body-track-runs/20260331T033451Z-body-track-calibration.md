# Body Profile Calibration Report

- generated_utc: `2026-03-31T03:34:51+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `344`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.640 | 0.632 | loosen_duration+tighten_health | noisy |
| standard | 0.640 | 0.632 | loosen_duration+tighten_health | noisy |
| strict | 0.890 | 0.887 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.334302`
- observed_false_regression_rate: `0.328488`
```json
{
  "duration_drift_p90": 1.54207,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.743 | 0.725 | noisy |
| 3 | 1 | 0.240 | 0.234 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.879 | 0.850 | noisy |
| 5 | 1 | 0.582 | 0.571 | noisy |
| 5 | 2 | 0.194 | 0.194 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.920 | 0.879 | noisy |
| 7 | 1 | 0.769 | 0.751 | noisy |
| 7 | 2 | 0.485 | 0.482 | noisy |
| 7 | 3 | 0.148 | 0.148 | acceptable |
| 9 | 0 | 0.940 | 0.887 | noisy |
| 9 | 1 | 0.866 | 0.842 | noisy |
| 9 | 2 | 0.664 | 0.655 | noisy |
| 9 | 3 | 0.402 | 0.402 | noisy |

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
