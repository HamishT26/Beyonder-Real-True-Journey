# Body Profile Calibration Report

- generated_utc: `2026-03-18T01:41:52+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `209`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.474 | 0.455 | loosen_duration+tighten_health | noisy |
| standard | 0.474 | 0.455 | loosen_duration+tighten_health | noisy |
| strict | 0.818 | 0.812 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.287081`
- observed_false_regression_rate: `0.277512`
```json
{
  "duration_drift_p90": 1.111342,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.667 | 0.638 | noisy |
| 3 | 1 | 0.188 | 0.179 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.815 | 0.766 | noisy |
| 5 | 1 | 0.483 | 0.463 | noisy |
| 5 | 2 | 0.132 | 0.132 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.872 | 0.803 | noisy |
| 7 | 1 | 0.690 | 0.660 | noisy |
| 7 | 2 | 0.355 | 0.350 | noisy |
| 7 | 3 | 0.099 | 0.099 | acceptable |
| 9 | 0 | 0.900 | 0.811 | noisy |
| 9 | 1 | 0.806 | 0.766 | noisy |
| 9 | 2 | 0.547 | 0.532 | noisy |
| 9 | 3 | 0.284 | 0.284 | noisy |

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
