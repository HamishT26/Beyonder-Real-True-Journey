# Body Profile Calibration Report

- generated_utc: `2026-03-20T23:16:57+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `223`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.498 | 0.481 | loosen_duration+tighten_health | noisy |
| standard | 0.498 | 0.481 | loosen_duration+tighten_health | noisy |
| strict | 0.830 | 0.824 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.300448`
- observed_false_regression_rate: `0.29148`
```json
{
  "duration_drift_p90": 1.116625,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.688 | 0.661 | noisy |
| 3 | 1 | 0.208 | 0.199 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.826 | 0.781 | noisy |
| 5 | 1 | 0.516 | 0.498 | noisy |
| 5 | 2 | 0.151 | 0.151 | noisy |
| 5 | 3 | 0.023 | 0.023 | acceptable |
| 7 | 0 | 0.880 | 0.816 | noisy |
| 7 | 1 | 0.710 | 0.682 | noisy |
| 7 | 2 | 0.392 | 0.387 | noisy |
| 7 | 3 | 0.115 | 0.115 | acceptable |
| 9 | 0 | 0.907 | 0.823 | noisy |
| 9 | 1 | 0.819 | 0.781 | noisy |
| 9 | 2 | 0.577 | 0.563 | noisy |
| 9 | 3 | 0.312 | 0.312 | noisy |

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
