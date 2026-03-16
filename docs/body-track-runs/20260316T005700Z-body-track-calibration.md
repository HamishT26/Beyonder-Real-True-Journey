# Body Profile Calibration Report

- generated_utc: `2026-03-16T00:57:00+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `181`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.420 | 0.397 | loosen_duration+tighten_health | noisy |
| standard | 0.420 | 0.397 | loosen_duration+tighten_health | noisy |
| strict | 0.790 | 0.782 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.287293`
- observed_false_regression_rate: `0.276243`
```json
{
  "duration_drift_p90": 1.110475,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.670 | 0.637 | noisy |
| 3 | 1 | 0.196 | 0.184 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.808 | 0.751 | noisy |
| 5 | 1 | 0.486 | 0.463 | noisy |
| 5 | 2 | 0.147 | 0.147 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.857 | 0.777 | noisy |
| 7 | 1 | 0.674 | 0.640 | noisy |
| 7 | 2 | 0.377 | 0.371 | noisy |
| 7 | 3 | 0.114 | 0.114 | acceptable |
| 9 | 0 | 0.884 | 0.780 | noisy |
| 9 | 1 | 0.780 | 0.734 | noisy |
| 9 | 2 | 0.538 | 0.520 | noisy |
| 9 | 3 | 0.324 | 0.324 | noisy |

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
