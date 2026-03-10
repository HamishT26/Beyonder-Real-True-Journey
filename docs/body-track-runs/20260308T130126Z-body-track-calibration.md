# Body Profile Calibration Report

- generated_utc: `2026-03-08T13:01:26+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `100`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.250 | 0.194 | loosen_duration+loosen_health | noisy |
| standard | 0.250 | 0.194 | loosen_duration+loosen_health | noisy |
| strict | 0.650 | 0.624 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.22`
- observed_false_regression_rate: `0.2`
```json
{
  "duration_drift_p90": 0.75526,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.510 | 0.449 | noisy |
| 3 | 1 | 0.143 | 0.122 | acceptable |
| 3 | 2 | 0.010 | 0.010 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.688 | 0.583 | noisy |
| 5 | 1 | 0.281 | 0.240 | noisy |
| 5 | 2 | 0.115 | 0.115 | acceptable |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.745 | 0.596 | noisy |
| 7 | 1 | 0.489 | 0.426 | noisy |
| 7 | 2 | 0.191 | 0.181 | noisy |
| 7 | 3 | 0.085 | 0.085 | acceptable |
| 9 | 0 | 0.783 | 0.587 | noisy |
| 9 | 1 | 0.620 | 0.533 | noisy |
| 9 | 2 | 0.315 | 0.283 | noisy |
| 9 | 3 | 0.163 | 0.163 | noisy |

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
