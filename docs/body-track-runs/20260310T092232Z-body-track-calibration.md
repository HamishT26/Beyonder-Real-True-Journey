# Body Profile Calibration Report

- generated_utc: `2026-03-10T09:22:32+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `126`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.341 | 0.303 | loosen_duration+loosen_health | noisy |
| standard | 0.341 | 0.303 | loosen_duration+loosen_health | noisy |
| strict | 0.714 | 0.697 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.261905`
- observed_false_regression_rate: `0.246032`
```json
{
  "duration_drift_p90": 0.999131,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.605 | 0.556 | noisy |
| 3 | 1 | 0.177 | 0.161 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.754 | 0.672 | noisy |
| 5 | 1 | 0.410 | 0.377 | noisy |
| 5 | 2 | 0.139 | 0.139 | acceptable |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.800 | 0.683 | noisy |
| 7 | 1 | 0.600 | 0.550 | noisy |
| 7 | 2 | 0.325 | 0.317 | noisy |
| 7 | 3 | 0.117 | 0.117 | acceptable |
| 9 | 0 | 0.831 | 0.678 | noisy |
| 9 | 1 | 0.703 | 0.636 | noisy |
| 9 | 2 | 0.466 | 0.441 | noisy |
| 9 | 3 | 0.305 | 0.305 | noisy |

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
