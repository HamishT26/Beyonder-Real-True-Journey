# Body Profile Calibration Report

- generated_utc: `2026-03-23T03:08:40+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `269`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.580 | 0.569 | loosen_duration+tighten_health | noisy |
| standard | 0.580 | 0.569 | loosen_duration+tighten_health | noisy |
| strict | 0.859 | 0.855 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315985`
- observed_false_regression_rate: `0.30855`
```json
{
  "duration_drift_p90": 1.369982,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.712 | 0.689 | noisy |
| 3 | 1 | 0.225 | 0.217 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.857 | 0.819 | noisy |
| 5 | 1 | 0.540 | 0.525 | noisy |
| 5 | 2 | 0.170 | 0.170 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.901 | 0.848 | noisy |
| 7 | 1 | 0.741 | 0.719 | noisy |
| 7 | 2 | 0.433 | 0.430 | noisy |
| 7 | 3 | 0.133 | 0.133 | acceptable |
| 9 | 0 | 0.923 | 0.854 | noisy |
| 9 | 1 | 0.847 | 0.816 | noisy |
| 9 | 2 | 0.625 | 0.613 | noisy |
| 9 | 3 | 0.352 | 0.352 | noisy |

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
