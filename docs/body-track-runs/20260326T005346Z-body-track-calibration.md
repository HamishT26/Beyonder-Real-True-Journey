# Body Profile Calibration Report

- generated_utc: `2026-03-26T00:53:46+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `321`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.629 | 0.621 | loosen_duration+tighten_health | noisy |
| standard | 0.629 | 0.621 | loosen_duration+tighten_health | noisy |
| strict | 0.882 | 0.879 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.320872`
- observed_false_regression_rate: `0.314642`
```json
{
  "duration_drift_p90": 1.56767,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.724 | 0.705 | noisy |
| 3 | 1 | 0.229 | 0.223 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.871 | 0.839 | noisy |
| 5 | 1 | 0.558 | 0.546 | noisy |
| 5 | 2 | 0.170 | 0.170 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.914 | 0.870 | noisy |
| 7 | 1 | 0.752 | 0.733 | noisy |
| 7 | 2 | 0.451 | 0.448 | noisy |
| 7 | 3 | 0.133 | 0.133 | acceptable |
| 9 | 0 | 0.936 | 0.879 | noisy |
| 9 | 1 | 0.856 | 0.831 | noisy |
| 9 | 2 | 0.639 | 0.629 | noisy |
| 9 | 3 | 0.364 | 0.364 | noisy |

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
