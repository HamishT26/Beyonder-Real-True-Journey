# Body Profile Calibration Report

- generated_utc: `2026-03-22T20:54:08+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `261`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.567 | 0.555 | loosen_duration+tighten_health | noisy |
| standard | 0.567 | 0.555 | loosen_duration+tighten_health | noisy |
| strict | 0.854 | 0.850 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.314176`
- observed_false_regression_rate: `0.306513`
```json
{
  "duration_drift_p90": 1.315038,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.710 | 0.687 | noisy |
| 3 | 1 | 0.224 | 0.216 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.852 | 0.813 | noisy |
| 5 | 1 | 0.549 | 0.533 | noisy |
| 5 | 2 | 0.175 | 0.175 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.898 | 0.843 | noisy |
| 7 | 1 | 0.745 | 0.722 | noisy |
| 7 | 2 | 0.443 | 0.439 | noisy |
| 7 | 3 | 0.137 | 0.137 | acceptable |
| 9 | 0 | 0.921 | 0.850 | noisy |
| 9 | 1 | 0.846 | 0.814 | noisy |
| 9 | 2 | 0.632 | 0.621 | noisy |
| 9 | 3 | 0.364 | 0.364 | noisy |

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
