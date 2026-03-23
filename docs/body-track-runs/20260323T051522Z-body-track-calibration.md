# Body Profile Calibration Report

- generated_utc: `2026-03-23T05:15:22+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `277`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.581 | 0.570 | loosen_duration+tighten_health | noisy |
| standard | 0.581 | 0.570 | loosen_duration+tighten_health | noisy |
| strict | 0.863 | 0.859 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.310469`
- observed_false_regression_rate: `0.303249`
```json
{
  "duration_drift_p90": 1.256138,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.705 | 0.684 | noisy |
| 3 | 1 | 0.218 | 0.211 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.861 | 0.824 | noisy |
| 5 | 1 | 0.531 | 0.516 | noisy |
| 5 | 2 | 0.165 | 0.165 | noisy |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.904 | 0.852 | noisy |
| 7 | 1 | 0.738 | 0.716 | noisy |
| 7 | 2 | 0.424 | 0.421 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.926 | 0.859 | noisy |
| 9 | 1 | 0.848 | 0.818 | noisy |
| 9 | 2 | 0.621 | 0.610 | noisy |
| 9 | 3 | 0.342 | 0.342 | noisy |

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
