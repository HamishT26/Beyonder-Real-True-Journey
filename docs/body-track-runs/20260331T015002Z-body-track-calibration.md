# Body Profile Calibration Report

- generated_utc: `2026-03-31T01:50:02+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `337`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.638 | 0.630 | loosen_duration+tighten_health | noisy |
| standard | 0.638 | 0.630 | loosen_duration+tighten_health | noisy |
| strict | 0.887 | 0.885 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.332344`
- observed_false_regression_rate: `0.326409`
```json
{
  "duration_drift_p90": 1.589223,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.737 | 0.719 | noisy |
| 3 | 1 | 0.239 | 0.233 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.877 | 0.847 | noisy |
| 5 | 1 | 0.577 | 0.565 | noisy |
| 5 | 2 | 0.192 | 0.192 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.918 | 0.876 | noisy |
| 7 | 1 | 0.764 | 0.746 | noisy |
| 7 | 2 | 0.474 | 0.471 | noisy |
| 7 | 3 | 0.151 | 0.151 | noisy |
| 9 | 0 | 0.939 | 0.884 | noisy |
| 9 | 1 | 0.863 | 0.839 | noisy |
| 9 | 2 | 0.657 | 0.647 | noisy |
| 9 | 3 | 0.395 | 0.395 | noisy |

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
