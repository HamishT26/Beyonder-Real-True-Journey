# Body Profile Calibration Report

- generated_utc: `2026-03-16T02:48:53+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `186`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.425 | 0.402 | loosen_duration+tighten_health | noisy |
| standard | 0.425 | 0.402 | loosen_duration+tighten_health | noisy |
| strict | 0.796 | 0.788 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.284946`
- observed_false_regression_rate: `0.274194`
```json
{
  "duration_drift_p90": 1.10586,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.663 | 0.630 | noisy |
| 3 | 1 | 0.190 | 0.179 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.808 | 0.753 | noisy |
| 5 | 1 | 0.478 | 0.456 | noisy |
| 5 | 2 | 0.143 | 0.143 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.861 | 0.783 | noisy |
| 7 | 1 | 0.678 | 0.644 | noisy |
| 7 | 2 | 0.372 | 0.367 | noisy |
| 7 | 3 | 0.111 | 0.111 | acceptable |
| 9 | 0 | 0.888 | 0.787 | noisy |
| 9 | 1 | 0.787 | 0.742 | noisy |
| 9 | 2 | 0.551 | 0.534 | noisy |
| 9 | 3 | 0.320 | 0.320 | noisy |

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
