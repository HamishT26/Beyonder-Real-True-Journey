# Body Profile Calibration Report

- generated_utc: `2026-03-14T10:52:29+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `176`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.403 | 0.379 | loosen_duration+tighten_health | noisy |
| standard | 0.403 | 0.379 | loosen_duration+tighten_health | noisy |
| strict | 0.784 | 0.775 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.284091`
- observed_false_regression_rate: `0.272727`
```json
{
  "duration_drift_p90": 1.082993,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.661 | 0.626 | noisy |
| 3 | 1 | 0.184 | 0.172 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.802 | 0.744 | noisy |
| 5 | 1 | 0.471 | 0.448 | noisy |
| 5 | 2 | 0.134 | 0.134 | acceptable |
| 5 | 3 | 0.012 | 0.012 | acceptable |
| 7 | 0 | 0.853 | 0.771 | noisy |
| 7 | 1 | 0.665 | 0.629 | noisy |
| 7 | 2 | 0.359 | 0.353 | noisy |
| 7 | 3 | 0.106 | 0.106 | acceptable |
| 9 | 0 | 0.881 | 0.774 | noisy |
| 9 | 1 | 0.774 | 0.726 | noisy |
| 9 | 2 | 0.524 | 0.506 | noisy |
| 9 | 3 | 0.304 | 0.304 | noisy |

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
