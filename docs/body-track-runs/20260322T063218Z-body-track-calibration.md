# Body Profile Calibration Report

- generated_utc: `2026-03-22T06:32:18+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `237`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.527 | 0.513 | loosen_duration+tighten_health | noisy |
| standard | 0.527 | 0.513 | loosen_duration+tighten_health | noisy |
| strict | 0.840 | 0.835 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.312236`
- observed_false_regression_rate: `0.303797`
```json
{
  "duration_drift_p90": 1.166775,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.702 | 0.677 | noisy |
| 3 | 1 | 0.226 | 0.217 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.837 | 0.794 | noisy |
| 5 | 1 | 0.541 | 0.524 | noisy |
| 5 | 2 | 0.172 | 0.172 | noisy |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.887 | 0.827 | noisy |
| 7 | 1 | 0.727 | 0.701 | noisy |
| 7 | 2 | 0.429 | 0.424 | noisy |
| 7 | 3 | 0.134 | 0.134 | acceptable |
| 9 | 0 | 0.913 | 0.834 | noisy |
| 9 | 1 | 0.830 | 0.795 | noisy |
| 9 | 2 | 0.603 | 0.590 | noisy |
| 9 | 3 | 0.354 | 0.354 | noisy |

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
