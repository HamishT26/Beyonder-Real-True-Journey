# Body Profile Calibration Report

- generated_utc: `2026-03-25T22:39:00+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `317`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.628 | 0.619 | loosen_duration+tighten_health | noisy |
| standard | 0.628 | 0.619 | loosen_duration+tighten_health | noisy |
| strict | 0.880 | 0.877 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.318612`
- observed_false_regression_rate: `0.312303`
```json
{
  "duration_drift_p90": 1.374394,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.721 | 0.702 | noisy |
| 3 | 1 | 0.225 | 0.219 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.869 | 0.837 | noisy |
| 5 | 1 | 0.553 | 0.540 | noisy |
| 5 | 2 | 0.173 | 0.173 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.913 | 0.868 | noisy |
| 7 | 1 | 0.749 | 0.730 | noisy |
| 7 | 2 | 0.447 | 0.444 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.935 | 0.877 | noisy |
| 9 | 1 | 0.854 | 0.828 | noisy |
| 9 | 2 | 0.634 | 0.625 | noisy |
| 9 | 3 | 0.356 | 0.356 | noisy |

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
