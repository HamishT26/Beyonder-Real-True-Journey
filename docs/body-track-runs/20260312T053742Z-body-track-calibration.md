# Body Profile Calibration Report

- generated_utc: `2026-03-12T05:37:42+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `150`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.380 | 0.350 | loosen_duration+tighten_health | noisy |
| standard | 0.380 | 0.350 | loosen_duration+tighten_health | noisy |
| strict | 0.753 | 0.741 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.273333`
- observed_false_regression_rate: `0.26`
```json
{
  "duration_drift_p90": 1.01415,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.635 | 0.595 | noisy |
| 3 | 1 | 0.176 | 0.162 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.788 | 0.719 | noisy |
| 5 | 1 | 0.438 | 0.411 | noisy |
| 5 | 2 | 0.130 | 0.130 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.833 | 0.736 | noisy |
| 7 | 1 | 0.646 | 0.604 | noisy |
| 7 | 2 | 0.326 | 0.319 | noisy |
| 7 | 3 | 0.097 | 0.097 | acceptable |
| 9 | 0 | 0.859 | 0.732 | noisy |
| 9 | 1 | 0.754 | 0.697 | noisy |
| 9 | 2 | 0.507 | 0.486 | noisy |
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
