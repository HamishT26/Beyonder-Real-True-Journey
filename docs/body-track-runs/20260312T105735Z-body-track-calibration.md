# Body Profile Calibration Report

- generated_utc: `2026-03-12T10:57:35+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `157`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.382 | 0.353 | loosen_duration+tighten_health | noisy |
| standard | 0.382 | 0.353 | loosen_duration+tighten_health | noisy |
| strict | 0.764 | 0.753 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.267516`
- observed_false_regression_rate: `0.254777`
```json
{
  "duration_drift_p90": 1.025011,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.639 | 0.600 | noisy |
| 3 | 1 | 0.168 | 0.155 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.797 | 0.732 | noisy |
| 5 | 1 | 0.438 | 0.412 | noisy |
| 5 | 2 | 0.124 | 0.124 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.841 | 0.748 | noisy |
| 7 | 1 | 0.656 | 0.616 | noisy |
| 7 | 2 | 0.331 | 0.325 | noisy |
| 7 | 3 | 0.093 | 0.093 | acceptable |
| 9 | 0 | 0.866 | 0.745 | noisy |
| 9 | 1 | 0.765 | 0.711 | noisy |
| 9 | 2 | 0.517 | 0.497 | noisy |
| 9 | 3 | 0.275 | 0.275 | noisy |

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
