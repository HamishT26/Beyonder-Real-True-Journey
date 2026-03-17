# Body Profile Calibration Report

- generated_utc: `2026-03-17T01:26:27+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `191`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.435 | 0.413 | loosen_duration+tighten_health | noisy |
| standard | 0.435 | 0.413 | loosen_duration+tighten_health | noisy |
| strict | 0.801 | 0.793 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.287958`
- observed_false_regression_rate: `0.277487`
```json
{
  "duration_drift_p90": 1.110475,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.672 | 0.640 | noisy |
| 3 | 1 | 0.196 | 0.185 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.813 | 0.759 | noisy |
| 5 | 1 | 0.492 | 0.471 | noisy |
| 5 | 2 | 0.144 | 0.144 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.865 | 0.789 | noisy |
| 7 | 1 | 0.686 | 0.654 | noisy |
| 7 | 2 | 0.378 | 0.373 | noisy |
| 7 | 3 | 0.108 | 0.108 | acceptable |
| 9 | 0 | 0.891 | 0.792 | noisy |
| 9 | 1 | 0.792 | 0.749 | noisy |
| 9 | 2 | 0.557 | 0.541 | noisy |
| 9 | 3 | 0.311 | 0.311 | noisy |

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
