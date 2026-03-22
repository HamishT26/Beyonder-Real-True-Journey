# Body Profile Calibration Report

- generated_utc: `2026-03-22T20:30:18+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `260`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.565 | 0.553 | loosen_duration+tighten_health | noisy |
| standard | 0.565 | 0.553 | loosen_duration+tighten_health | noisy |
| strict | 0.854 | 0.850 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315385`
- observed_false_regression_rate: `0.307692`
```json
{
  "duration_drift_p90": 1.34251,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.713 | 0.690 | noisy |
| 3 | 1 | 0.225 | 0.217 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.852 | 0.812 | noisy |
| 5 | 1 | 0.551 | 0.535 | noisy |
| 5 | 2 | 0.176 | 0.176 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.898 | 0.843 | noisy |
| 7 | 1 | 0.748 | 0.724 | noisy |
| 7 | 2 | 0.445 | 0.441 | noisy |
| 7 | 3 | 0.138 | 0.138 | acceptable |
| 9 | 0 | 0.921 | 0.849 | noisy |
| 9 | 1 | 0.845 | 0.813 | noisy |
| 9 | 2 | 0.631 | 0.619 | noisy |
| 9 | 3 | 0.365 | 0.365 | noisy |

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
