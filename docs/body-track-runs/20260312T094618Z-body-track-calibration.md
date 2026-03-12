# Body Profile Calibration Report

- generated_utc: `2026-03-12T09:46:18+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `153`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.392 | 0.363 | loosen_duration+tighten_health | noisy |
| standard | 0.392 | 0.363 | loosen_duration+tighten_health | noisy |
| strict | 0.758 | 0.747 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.27451`
- observed_false_regression_rate: `0.261438`
```json
{
  "duration_drift_p90": 1.039491,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.642 | 0.603 | noisy |
| 3 | 1 | 0.172 | 0.159 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.792 | 0.725 | noisy |
| 5 | 1 | 0.443 | 0.416 | noisy |
| 5 | 2 | 0.128 | 0.128 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.837 | 0.741 | noisy |
| 7 | 1 | 0.653 | 0.612 | noisy |
| 7 | 2 | 0.340 | 0.333 | noisy |
| 7 | 3 | 0.095 | 0.095 | acceptable |
| 9 | 0 | 0.862 | 0.738 | noisy |
| 9 | 1 | 0.759 | 0.703 | noisy |
| 9 | 2 | 0.517 | 0.497 | noisy |
| 9 | 3 | 0.276 | 0.276 | noisy |

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
