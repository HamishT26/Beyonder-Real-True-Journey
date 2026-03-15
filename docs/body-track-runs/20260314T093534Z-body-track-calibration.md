# Body Profile Calibration Report

- generated_utc: `2026-03-14T09:35:34+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `173`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.393 | 0.367 | loosen_duration+tighten_health | noisy |
| standard | 0.393 | 0.367 | loosen_duration+tighten_health | noisy |
| strict | 0.780 | 0.771 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.277457`
- observed_false_regression_rate: `0.265896`
```json
{
  "duration_drift_p90": 1.095439,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.655 | 0.620 | noisy |
| 3 | 1 | 0.181 | 0.170 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.799 | 0.740 | noisy |
| 5 | 1 | 0.462 | 0.438 | noisy |
| 5 | 2 | 0.136 | 0.136 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.850 | 0.766 | noisy |
| 7 | 1 | 0.659 | 0.623 | noisy |
| 7 | 2 | 0.347 | 0.341 | noisy |
| 7 | 3 | 0.108 | 0.108 | acceptable |
| 9 | 0 | 0.879 | 0.770 | noisy |
| 9 | 1 | 0.770 | 0.721 | noisy |
| 9 | 2 | 0.515 | 0.497 | noisy |
| 9 | 3 | 0.291 | 0.291 | noisy |

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
