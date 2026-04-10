# Body Profile Calibration Report

- generated_utc: `2026-04-10T16:09:39+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `470`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.502 | 0.495 | loosen_duration+tighten_health | noisy |
| standard | 0.502 | 0.495 | loosen_duration+tighten_health | noisy |
| strict | 0.870 | 0.868 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.317021`
- observed_false_regression_rate: `0.312766`
```json
{
  "duration_drift_p90": 1.083529,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.718 | 0.705 | noisy |
| 3 | 1 | 0.224 | 0.220 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.856 | 0.835 | noisy |
| 5 | 1 | 0.554 | 0.545 | noisy |
| 5 | 2 | 0.176 | 0.176 | noisy |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.907 | 0.877 | noisy |
| 7 | 1 | 0.731 | 0.718 | noisy |
| 7 | 2 | 0.455 | 0.453 | noisy |
| 7 | 3 | 0.131 | 0.131 | acceptable |
| 9 | 0 | 0.935 | 0.896 | noisy |
| 9 | 1 | 0.833 | 0.816 | noisy |
| 9 | 2 | 0.623 | 0.617 | noisy |
| 9 | 3 | 0.366 | 0.366 | noisy |

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
