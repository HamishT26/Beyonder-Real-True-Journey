# Body Profile Calibration Report

- generated_utc: `2026-03-14T08:49:57+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `171`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.386 | 0.360 | loosen_duration+tighten_health | noisy |
| standard | 0.386 | 0.360 | loosen_duration+tighten_health | noisy |
| strict | 0.778 | 0.768 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.280702`
- observed_false_regression_rate: `0.269006`
```json
{
  "duration_drift_p90": 1.100633,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.651 | 0.615 | noisy |
| 3 | 1 | 0.183 | 0.172 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.796 | 0.737 | noisy |
| 5 | 1 | 0.455 | 0.431 | noisy |
| 5 | 2 | 0.138 | 0.138 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.848 | 0.764 | noisy |
| 7 | 1 | 0.655 | 0.618 | noisy |
| 7 | 2 | 0.339 | 0.333 | noisy |
| 7 | 3 | 0.103 | 0.103 | acceptable |
| 9 | 0 | 0.877 | 0.767 | noisy |
| 9 | 1 | 0.767 | 0.718 | noisy |
| 9 | 2 | 0.509 | 0.491 | noisy |
| 9 | 3 | 0.282 | 0.282 | noisy |

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
