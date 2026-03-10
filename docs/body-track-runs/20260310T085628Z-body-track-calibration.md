# Body Profile Calibration Report

- generated_utc: `2026-03-10T08:56:28+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `122`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.352 | 0.313 | loosen_duration+loosen_health | noisy |
| standard | 0.352 | 0.313 | loosen_duration+loosen_health | noisy |
| strict | 0.713 | 0.696 | loosen_duration+loosen_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.254098`
- observed_false_regression_rate: `0.237705`
```json
{
  "duration_drift_p90": 1.00691,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.592 | 0.542 | noisy |
| 3 | 1 | 0.175 | 0.158 | noisy |
| 3 | 2 | 0.008 | 0.008 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.746 | 0.661 | noisy |
| 5 | 1 | 0.398 | 0.364 | noisy |
| 5 | 2 | 0.144 | 0.144 | acceptable |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.793 | 0.672 | noisy |
| 7 | 1 | 0.586 | 0.534 | noisy |
| 7 | 2 | 0.319 | 0.310 | noisy |
| 7 | 3 | 0.121 | 0.121 | acceptable |
| 9 | 0 | 0.825 | 0.667 | noisy |
| 9 | 1 | 0.693 | 0.623 | noisy |
| 9 | 2 | 0.447 | 0.421 | noisy |
| 9 | 3 | 0.307 | 0.307 | noisy |

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
