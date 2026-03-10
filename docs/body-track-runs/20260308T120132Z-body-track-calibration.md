# Body Profile Calibration Report

- generated_utc: `2026-03-08T12:01:32+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `96`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.219 | 0.157 | loosen_duration+loosen_health | noisy |
| standard | 0.219 | 0.157 | loosen_duration+loosen_health | noisy |
| strict | 0.635 | 0.607 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.208333`
- observed_false_regression_rate: `0.1875`
```json
{
  "duration_drift_p90": 0.591572,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.489 | 0.426 | noisy |
| 3 | 1 | 0.117 | 0.096 | acceptable |
| 3 | 2 | 0.000 | 0.000 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.674 | 0.565 | noisy |
| 5 | 1 | 0.250 | 0.207 | noisy |
| 5 | 2 | 0.076 | 0.076 | acceptable |
| 5 | 3 | 0.000 | 0.000 | acceptable |
| 7 | 0 | 0.733 | 0.578 | noisy |
| 7 | 1 | 0.467 | 0.400 | noisy |
| 7 | 2 | 0.156 | 0.144 | acceptable |
| 7 | 3 | 0.044 | 0.044 | acceptable |
| 9 | 0 | 0.773 | 0.568 | noisy |
| 9 | 1 | 0.602 | 0.511 | noisy |
| 9 | 2 | 0.284 | 0.250 | noisy |
| 9 | 3 | 0.125 | 0.125 | acceptable |

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
