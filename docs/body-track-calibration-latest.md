# Body Profile Calibration Report

- generated_utc: `2026-03-24T06:19:02+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `295`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.603 | 0.594 | loosen_duration+tighten_health | noisy |
| standard | 0.603 | 0.594 | loosen_duration+tighten_health | noisy |
| strict | 0.871 | 0.868 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315254`
- observed_false_regression_rate: `0.308475`
```json
{
  "duration_drift_p90": 1.479867,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.713 | 0.693 | noisy |
| 3 | 1 | 0.225 | 0.218 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.859 | 0.825 | noisy |
| 5 | 1 | 0.543 | 0.529 | noisy |
| 5 | 2 | 0.172 | 0.172 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.907 | 0.858 | noisy |
| 7 | 1 | 0.737 | 0.716 | noisy |
| 7 | 2 | 0.436 | 0.433 | noisy |
| 7 | 3 | 0.135 | 0.135 | acceptable |
| 9 | 0 | 0.930 | 0.868 | noisy |
| 9 | 1 | 0.843 | 0.815 | noisy |
| 9 | 2 | 0.620 | 0.610 | noisy |
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
