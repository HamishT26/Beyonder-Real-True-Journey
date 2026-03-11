# Body Profile Calibration Report

- generated_utc: `2026-03-11T02:36:36+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `137`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.336 | 0.300 | loosen_duration+loosen_health | noisy |
| standard | 0.336 | 0.300 | loosen_duration+loosen_health | noisy |
| strict | 0.730 | 0.715 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.270073`
- observed_false_regression_rate: `0.255474`
```json
{
  "duration_drift_p90": 1.025011,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.622 | 0.578 | noisy |
| 3 | 1 | 0.178 | 0.163 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.774 | 0.699 | noisy |
| 5 | 1 | 0.436 | 0.406 | noisy |
| 5 | 2 | 0.135 | 0.135 | acceptable |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.817 | 0.710 | noisy |
| 7 | 1 | 0.634 | 0.588 | noisy |
| 7 | 2 | 0.351 | 0.344 | noisy |
| 7 | 3 | 0.107 | 0.107 | acceptable |
| 9 | 0 | 0.845 | 0.705 | noisy |
| 9 | 1 | 0.729 | 0.667 | noisy |
| 9 | 2 | 0.512 | 0.488 | noisy |
| 9 | 3 | 0.302 | 0.302 | noisy |

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
