# Body Profile Calibration Report

- generated_utc: `2026-03-11T05:06:11+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `145`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.359 | 0.326 | loosen_duration+tighten_health | noisy |
| standard | 0.359 | 0.326 | loosen_duration+tighten_health | noisy |
| strict | 0.745 | 0.732 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.262069`
- observed_false_regression_rate: `0.248276`
```json
{
  "duration_drift_p90": 1.001076,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.622 | 0.580 | noisy |
| 3 | 1 | 0.168 | 0.154 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.780 | 0.709 | noisy |
| 5 | 1 | 0.426 | 0.397 | noisy |
| 5 | 2 | 0.128 | 0.128 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.827 | 0.727 | noisy |
| 7 | 1 | 0.633 | 0.590 | noisy |
| 7 | 2 | 0.331 | 0.324 | noisy |
| 7 | 3 | 0.101 | 0.101 | acceptable |
| 9 | 0 | 0.854 | 0.723 | noisy |
| 9 | 1 | 0.745 | 0.686 | noisy |
| 9 | 2 | 0.504 | 0.482 | noisy |
| 9 | 3 | 0.285 | 0.285 | noisy |

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
