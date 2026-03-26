# Body Profile Calibration Report

- generated_utc: `2026-03-26T03:45:32+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `329`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.638 | 0.630 | loosen_duration+tighten_health | noisy |
| standard | 0.638 | 0.630 | loosen_duration+tighten_health | noisy |
| strict | 0.884 | 0.882 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.328267`
- observed_false_regression_rate: `0.322188`
```json
{
  "duration_drift_p90": 1.578447,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.731 | 0.713 | noisy |
| 3 | 1 | 0.239 | 0.232 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.874 | 0.843 | noisy |
| 5 | 1 | 0.569 | 0.557 | noisy |
| 5 | 2 | 0.188 | 0.188 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.916 | 0.873 | noisy |
| 7 | 1 | 0.759 | 0.740 | noisy |
| 7 | 2 | 0.464 | 0.461 | noisy |
| 7 | 3 | 0.149 | 0.149 | acceptable |
| 9 | 0 | 0.938 | 0.882 | noisy |
| 9 | 1 | 0.860 | 0.835 | noisy |
| 9 | 2 | 0.648 | 0.639 | noisy |
| 9 | 3 | 0.380 | 0.380 | noisy |

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
