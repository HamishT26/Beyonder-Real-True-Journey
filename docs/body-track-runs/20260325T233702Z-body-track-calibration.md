# Body Profile Calibration Report

- generated_utc: `2026-03-25T23:37:02+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `319`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.630 | 0.622 | loosen_duration+tighten_health | noisy |
| standard | 0.630 | 0.622 | loosen_duration+tighten_health | noisy |
| strict | 0.881 | 0.878 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.322884`
- observed_false_regression_rate: `0.316614`
```json
{
  "duration_drift_p90": 1.578447,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.722 | 0.703 | noisy |
| 3 | 1 | 0.227 | 0.221 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.870 | 0.838 | noisy |
| 5 | 1 | 0.556 | 0.543 | noisy |
| 5 | 2 | 0.171 | 0.171 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.914 | 0.869 | noisy |
| 7 | 1 | 0.751 | 0.732 | noisy |
| 7 | 2 | 0.450 | 0.447 | noisy |
| 7 | 3 | 0.134 | 0.134 | acceptable |
| 9 | 0 | 0.936 | 0.878 | noisy |
| 9 | 1 | 0.855 | 0.830 | noisy |
| 9 | 2 | 0.637 | 0.627 | noisy |
| 9 | 3 | 0.360 | 0.360 | noisy |

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
