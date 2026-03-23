# Body Profile Calibration Report

- generated_utc: `2026-03-23T04:49:19+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `275`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.582 | 0.571 | loosen_duration+tighten_health | noisy |
| standard | 0.582 | 0.571 | loosen_duration+tighten_health | noisy |
| strict | 0.862 | 0.858 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.312727`
- observed_false_regression_rate: `0.305455`
```json
{
  "duration_drift_p90": 1.26871,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.711 | 0.689 | noisy |
| 3 | 1 | 0.220 | 0.212 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.860 | 0.823 | noisy |
| 5 | 1 | 0.535 | 0.520 | noisy |
| 5 | 2 | 0.166 | 0.166 | noisy |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.903 | 0.851 | noisy |
| 7 | 1 | 0.743 | 0.721 | noisy |
| 7 | 2 | 0.428 | 0.424 | noisy |
| 7 | 3 | 0.130 | 0.130 | acceptable |
| 9 | 0 | 0.925 | 0.858 | noisy |
| 9 | 1 | 0.850 | 0.820 | noisy |
| 9 | 2 | 0.625 | 0.614 | noisy |
| 9 | 3 | 0.345 | 0.345 | noisy |

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
