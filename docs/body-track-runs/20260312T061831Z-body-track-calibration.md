# Body Profile Calibration Report

- generated_utc: `2026-03-12T06:18:31+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `151`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.384 | 0.354 | loosen_duration+tighten_health | noisy |
| standard | 0.384 | 0.354 | loosen_duration+tighten_health | noisy |
| strict | 0.755 | 0.743 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.271523`
- observed_false_regression_rate: `0.258278`
```json
{
  "duration_drift_p90": 1.01053,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.638 | 0.597 | noisy |
| 3 | 1 | 0.174 | 0.161 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.789 | 0.721 | noisy |
| 5 | 1 | 0.442 | 0.415 | noisy |
| 5 | 2 | 0.129 | 0.129 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.834 | 0.738 | noisy |
| 7 | 1 | 0.648 | 0.607 | noisy |
| 7 | 2 | 0.331 | 0.324 | noisy |
| 7 | 3 | 0.097 | 0.097 | acceptable |
| 9 | 0 | 0.860 | 0.734 | noisy |
| 9 | 1 | 0.755 | 0.699 | noisy |
| 9 | 2 | 0.510 | 0.490 | noisy |
| 9 | 3 | 0.273 | 0.273 | noisy |

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
