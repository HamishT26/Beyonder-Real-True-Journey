# Body Profile Calibration Report

- generated_utc: `2026-03-26T00:56:40+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `322`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.630 | 0.622 | loosen_duration+tighten_health | noisy |
| standard | 0.630 | 0.622 | loosen_duration+tighten_health | noisy |
| strict | 0.882 | 0.879 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.322981`
- observed_false_regression_rate: `0.31677`
```json
{
  "duration_drift_p90": 1.562282,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.725 | 0.706 | noisy |
| 3 | 1 | 0.228 | 0.222 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.871 | 0.840 | noisy |
| 5 | 1 | 0.560 | 0.547 | noisy |
| 5 | 2 | 0.173 | 0.173 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.915 | 0.870 | noisy |
| 7 | 1 | 0.753 | 0.734 | noisy |
| 7 | 2 | 0.453 | 0.449 | noisy |
| 7 | 3 | 0.133 | 0.133 | acceptable |
| 9 | 0 | 0.936 | 0.879 | noisy |
| 9 | 1 | 0.857 | 0.831 | noisy |
| 9 | 2 | 0.640 | 0.631 | noisy |
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
