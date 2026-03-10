# Body Profile Calibration Report

- generated_utc: `2026-03-10T12:25:23+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `133`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.338 | 0.302 | loosen_duration+loosen_health | noisy |
| standard | 0.338 | 0.302 | loosen_duration+loosen_health | noisy |
| strict | 0.722 | 0.706 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.270677`
- observed_false_regression_rate: `0.255639`
```json
{
  "duration_drift_p90": 1.004965,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.626 | 0.580 | noisy |
| 3 | 1 | 0.183 | 0.168 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.767 | 0.690 | noisy |
| 5 | 1 | 0.434 | 0.403 | noisy |
| 5 | 2 | 0.140 | 0.140 | acceptable |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.811 | 0.701 | noisy |
| 7 | 1 | 0.622 | 0.575 | noisy |
| 7 | 2 | 0.346 | 0.339 | noisy |
| 7 | 3 | 0.110 | 0.110 | acceptable |
| 9 | 0 | 0.840 | 0.696 | noisy |
| 9 | 1 | 0.720 | 0.656 | noisy |
| 9 | 2 | 0.496 | 0.472 | noisy |
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
