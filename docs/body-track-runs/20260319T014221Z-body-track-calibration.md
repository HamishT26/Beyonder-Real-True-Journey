# Body Profile Calibration Report

- generated_utc: `2026-03-19T01:42:21+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `219`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.489 | 0.472 | loosen_duration+tighten_health | noisy |
| standard | 0.489 | 0.472 | loosen_duration+tighten_health | noisy |
| strict | 0.826 | 0.821 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.296804`
- observed_false_regression_rate: `0.287671`
```json
{
  "duration_drift_p90": 1.115126,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.682 | 0.654 | noisy |
| 3 | 1 | 0.198 | 0.189 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.823 | 0.777 | noisy |
| 5 | 1 | 0.507 | 0.488 | noisy |
| 5 | 2 | 0.135 | 0.135 | acceptable |
| 5 | 3 | 0.009 | 0.009 | acceptable |
| 7 | 0 | 0.878 | 0.812 | noisy |
| 7 | 1 | 0.704 | 0.676 | noisy |
| 7 | 2 | 0.380 | 0.376 | noisy |
| 7 | 3 | 0.099 | 0.099 | acceptable |
| 9 | 0 | 0.905 | 0.820 | noisy |
| 9 | 1 | 0.815 | 0.777 | noisy |
| 9 | 2 | 0.569 | 0.555 | noisy |
| 9 | 3 | 0.299 | 0.299 | noisy |

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
