# Body Profile Calibration Report

- generated_utc: `2026-03-17T20:31:53+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `198`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.455 | 0.435 | loosen_duration+tighten_health | noisy |
| standard | 0.455 | 0.435 | loosen_duration+tighten_health | noisy |
| strict | 0.808 | 0.801 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.287879`
- observed_false_regression_rate: `0.277778`
```json
{
  "duration_drift_p90": 1.111776,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.658 | 0.628 | noisy |
| 3 | 1 | 0.194 | 0.184 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.804 | 0.753 | noisy |
| 5 | 1 | 0.479 | 0.459 | noisy |
| 5 | 2 | 0.139 | 0.139 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.865 | 0.792 | noisy |
| 7 | 1 | 0.677 | 0.646 | noisy |
| 7 | 2 | 0.365 | 0.359 | noisy |
| 7 | 3 | 0.104 | 0.104 | acceptable |
| 9 | 0 | 0.895 | 0.800 | noisy |
| 9 | 1 | 0.795 | 0.753 | noisy |
| 9 | 2 | 0.547 | 0.532 | noisy |
| 9 | 3 | 0.300 | 0.300 | noisy |

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
