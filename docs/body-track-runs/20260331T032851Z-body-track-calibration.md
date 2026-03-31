# Body Profile Calibration Report

- generated_utc: `2026-03-31T03:28:51+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `343`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.638 | 0.631 | loosen_duration+tighten_health | noisy |
| standard | 0.638 | 0.631 | loosen_duration+tighten_health | noisy |
| strict | 0.889 | 0.887 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.332362`
- observed_false_regression_rate: `0.326531`
```json
{
  "duration_drift_p90": 1.552176,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.742 | 0.724 | noisy |
| 3 | 1 | 0.238 | 0.232 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.879 | 0.850 | noisy |
| 5 | 1 | 0.581 | 0.569 | noisy |
| 5 | 2 | 0.192 | 0.192 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.920 | 0.878 | noisy |
| 7 | 1 | 0.769 | 0.751 | noisy |
| 7 | 2 | 0.484 | 0.481 | noisy |
| 7 | 3 | 0.148 | 0.148 | acceptable |
| 9 | 0 | 0.940 | 0.887 | noisy |
| 9 | 1 | 0.866 | 0.842 | noisy |
| 9 | 2 | 0.663 | 0.654 | noisy |
| 9 | 3 | 0.400 | 0.400 | noisy |

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
