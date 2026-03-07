# Body Profile Calibration Report

- generated_utc: `2026-03-07T05:11:32+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `83`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.205 | 0.132 | loosen_duration+loosen_health | acceptable |
| standard | 0.205 | 0.132 | loosen_duration+loosen_health | acceptable |
| strict | 0.578 | 0.539 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.180723`
- observed_false_regression_rate: `0.156627`
```json
{
  "duration_drift_p90": 0.322062,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.444 | 0.370 | noisy |
| 3 | 1 | 0.111 | 0.086 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.620 | 0.494 | noisy |
| 5 | 1 | 0.241 | 0.190 | noisy |
| 5 | 2 | 0.076 | 0.076 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.688 | 0.506 | noisy |
| 7 | 1 | 0.403 | 0.325 | noisy |
| 7 | 2 | 0.169 | 0.156 | noisy |
| 7 | 3 | 0.052 | 0.052 | acceptable |
| 9 | 0 | 0.733 | 0.493 | noisy |
| 9 | 1 | 0.533 | 0.427 | noisy |
| 9 | 2 | 0.253 | 0.213 | noisy |
| 9 | 3 | 0.133 | 0.133 | acceptable |

## Recommendations
```json
{
  "recommended_benchmark_profile": "quick",
  "recommended_trend_profile": "quick",
  "recommended_regression_window": {
    "window_size": 3,
    "max_regressions": 2
  }
}
```
