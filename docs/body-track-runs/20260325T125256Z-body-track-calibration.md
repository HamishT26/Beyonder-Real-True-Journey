# Body Profile Calibration Report

- generated_utc: `2026-03-25T12:52:56+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `301`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.611 | 0.602 | loosen_duration+tighten_health | noisy |
| standard | 0.611 | 0.602 | loosen_duration+tighten_health | noisy |
| strict | 0.874 | 0.871 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315615`
- observed_false_regression_rate: `0.30897`
```json
{
  "duration_drift_p90": 1.315039,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.712 | 0.692 | noisy |
| 3 | 1 | 0.221 | 0.214 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.862 | 0.828 | noisy |
| 5 | 1 | 0.539 | 0.525 | noisy |
| 5 | 2 | 0.168 | 0.168 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.908 | 0.861 | noisy |
| 7 | 1 | 0.739 | 0.719 | noisy |
| 7 | 2 | 0.434 | 0.431 | noisy |
| 7 | 3 | 0.132 | 0.132 | acceptable |
| 9 | 0 | 0.932 | 0.870 | noisy |
| 9 | 1 | 0.846 | 0.819 | noisy |
| 9 | 2 | 0.625 | 0.614 | noisy |
| 9 | 3 | 0.352 | 0.352 | noisy |

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
