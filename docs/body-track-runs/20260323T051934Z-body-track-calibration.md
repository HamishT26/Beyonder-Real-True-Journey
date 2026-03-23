# Body Profile Calibration Report

- generated_utc: `2026-03-23T05:19:34+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `278`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.583 | 0.572 | loosen_duration+tighten_health | noisy |
| standard | 0.583 | 0.572 | loosen_duration+tighten_health | noisy |
| strict | 0.863 | 0.860 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.309353`
- observed_false_regression_rate: `0.302158`
```json
{
  "duration_drift_p90": 1.249853,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.703 | 0.681 | noisy |
| 3 | 1 | 0.217 | 0.210 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.858 | 0.821 | noisy |
| 5 | 1 | 0.529 | 0.515 | noisy |
| 5 | 2 | 0.164 | 0.164 | noisy |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.904 | 0.853 | noisy |
| 7 | 1 | 0.735 | 0.713 | noisy |
| 7 | 2 | 0.423 | 0.419 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.926 | 0.859 | noisy |
| 9 | 1 | 0.844 | 0.815 | noisy |
| 9 | 2 | 0.619 | 0.607 | noisy |
| 9 | 3 | 0.341 | 0.341 | noisy |

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
