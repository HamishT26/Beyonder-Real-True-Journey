# Body Profile Calibration Report

- generated_utc: `2026-03-25T22:37:02+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `316`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.630 | 0.621 | loosen_duration+tighten_health | noisy |
| standard | 0.630 | 0.621 | loosen_duration+tighten_health | noisy |
| strict | 0.880 | 0.877 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.31962`
- observed_false_regression_rate: `0.313291`
```json
{
  "duration_drift_p90": 1.391759,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.723 | 0.704 | noisy |
| 3 | 1 | 0.226 | 0.220 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.869 | 0.837 | noisy |
| 5 | 1 | 0.551 | 0.538 | noisy |
| 5 | 2 | 0.173 | 0.173 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.913 | 0.868 | noisy |
| 7 | 1 | 0.748 | 0.729 | noisy |
| 7 | 2 | 0.445 | 0.442 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.935 | 0.877 | noisy |
| 9 | 1 | 0.854 | 0.828 | noisy |
| 9 | 2 | 0.633 | 0.623 | noisy |
| 9 | 3 | 0.357 | 0.357 | noisy |

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
