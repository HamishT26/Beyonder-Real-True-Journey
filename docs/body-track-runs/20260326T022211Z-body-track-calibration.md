# Body Profile Calibration Report

- generated_utc: `2026-03-26T02:22:11+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `326`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.635 | 0.627 | loosen_duration+tighten_health | noisy |
| standard | 0.635 | 0.627 | loosen_duration+tighten_health | noisy |
| strict | 0.883 | 0.881 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.325153`
- observed_false_regression_rate: `0.319018`
```json
{
  "duration_drift_p90": 1.521858,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.728 | 0.710 | noisy |
| 3 | 1 | 0.235 | 0.228 | noisy |
| 3 | 2 | 0.019 | 0.019 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.873 | 0.842 | noisy |
| 5 | 1 | 0.565 | 0.553 | noisy |
| 5 | 2 | 0.183 | 0.183 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.916 | 0.872 | noisy |
| 7 | 1 | 0.756 | 0.738 | noisy |
| 7 | 2 | 0.459 | 0.456 | noisy |
| 7 | 3 | 0.141 | 0.141 | acceptable |
| 9 | 0 | 0.937 | 0.881 | noisy |
| 9 | 1 | 0.858 | 0.833 | noisy |
| 9 | 2 | 0.645 | 0.635 | noisy |
| 9 | 3 | 0.374 | 0.374 | noisy |

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
