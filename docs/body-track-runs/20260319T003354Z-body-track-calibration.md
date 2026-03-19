# Body Profile Calibration Report

- generated_utc: `2026-03-19T00:33:54+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `217`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.484 | 0.467 | loosen_duration+tighten_health | noisy |
| standard | 0.484 | 0.467 | loosen_duration+tighten_health | noisy |
| strict | 0.825 | 0.819 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.290323`
- observed_false_regression_rate: `0.281106`
```json
{
  "duration_drift_p90": 1.115625,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.679 | 0.651 | noisy |
| 3 | 1 | 0.191 | 0.181 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.822 | 0.775 | noisy |
| 5 | 1 | 0.502 | 0.484 | noisy |
| 5 | 2 | 0.131 | 0.131 | acceptable |
| 5 | 3 | 0.009 | 0.009 | acceptable |
| 7 | 0 | 0.877 | 0.810 | noisy |
| 7 | 1 | 0.701 | 0.673 | noisy |
| 7 | 2 | 0.374 | 0.370 | noisy |
| 7 | 3 | 0.095 | 0.095 | acceptable |
| 9 | 0 | 0.904 | 0.818 | noisy |
| 9 | 1 | 0.813 | 0.775 | noisy |
| 9 | 2 | 0.565 | 0.550 | noisy |
| 9 | 3 | 0.292 | 0.292 | noisy |

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
