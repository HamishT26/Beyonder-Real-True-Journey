# Body Profile Calibration Report

- generated_utc: `2026-04-04T00:54:30+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `428`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.547 | 0.539 | loosen_duration+tighten_health | noisy |
| standard | 0.547 | 0.539 | loosen_duration+tighten_health | noisy |
| strict | 0.900 | 0.898 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.310748`
- observed_false_regression_rate: `0.306075`
```json
{
  "duration_drift_p90": 1.129763,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.702 | 0.688 | noisy |
| 3 | 1 | 0.218 | 0.214 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.844 | 0.821 | noisy |
| 5 | 1 | 0.531 | 0.521 | noisy |
| 5 | 2 | 0.175 | 0.175 | noisy |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.898 | 0.865 | noisy |
| 7 | 1 | 0.713 | 0.699 | noisy |
| 7 | 2 | 0.438 | 0.436 | noisy |
| 7 | 3 | 0.128 | 0.128 | acceptable |
| 9 | 0 | 0.929 | 0.886 | noisy |
| 9 | 1 | 0.819 | 0.800 | noisy |
| 9 | 2 | 0.610 | 0.602 | noisy |
| 9 | 3 | 0.350 | 0.350 | noisy |

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
