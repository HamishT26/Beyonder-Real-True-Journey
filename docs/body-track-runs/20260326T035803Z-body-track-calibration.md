# Body Profile Calibration Report

- generated_utc: `2026-03-26T03:58:03+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `330`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.639 | 0.632 | loosen_duration+tighten_health | noisy |
| standard | 0.639 | 0.632 | loosen_duration+tighten_health | noisy |
| strict | 0.885 | 0.882 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.330303`
- observed_false_regression_rate: `0.324242`
```json
{
  "duration_drift_p90": 1.618674,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.732 | 0.713 | noisy |
| 3 | 1 | 0.241 | 0.235 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.874 | 0.844 | noisy |
| 5 | 1 | 0.571 | 0.558 | noisy |
| 5 | 2 | 0.190 | 0.190 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.917 | 0.873 | noisy |
| 7 | 1 | 0.759 | 0.741 | noisy |
| 7 | 2 | 0.466 | 0.463 | noisy |
| 7 | 3 | 0.151 | 0.151 | noisy |
| 9 | 0 | 0.938 | 0.882 | noisy |
| 9 | 1 | 0.860 | 0.835 | noisy |
| 9 | 2 | 0.649 | 0.640 | noisy |
| 9 | 3 | 0.382 | 0.382 | noisy |

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
