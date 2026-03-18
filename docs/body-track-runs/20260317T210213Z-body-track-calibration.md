# Body Profile Calibration Report

- generated_utc: `2026-03-17T21:02:13+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `199`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.457 | 0.438 | loosen_duration+tighten_health | noisy |
| standard | 0.457 | 0.438 | loosen_duration+tighten_health | noisy |
| strict | 0.809 | 0.802 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.286432`
- observed_false_regression_rate: `0.276382`
```json
{
  "duration_drift_p90": 1.111342,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.660 | 0.629 | noisy |
| 3 | 1 | 0.198 | 0.188 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.805 | 0.754 | noisy |
| 5 | 1 | 0.482 | 0.462 | noisy |
| 5 | 2 | 0.138 | 0.138 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.865 | 0.793 | noisy |
| 7 | 1 | 0.679 | 0.648 | noisy |
| 7 | 2 | 0.363 | 0.358 | noisy |
| 7 | 3 | 0.104 | 0.104 | acceptable |
| 9 | 0 | 0.895 | 0.801 | noisy |
| 9 | 1 | 0.796 | 0.754 | noisy |
| 9 | 2 | 0.545 | 0.529 | noisy |
| 9 | 3 | 0.298 | 0.298 | noisy |

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
