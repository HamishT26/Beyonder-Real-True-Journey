# Body Profile Calibration Report

- generated_utc: `2026-03-26T00:23:37+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `320`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.631 | 0.623 | loosen_duration+tighten_health | noisy |
| standard | 0.631 | 0.623 | loosen_duration+tighten_health | noisy |
| strict | 0.881 | 0.879 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.321875`
- observed_false_regression_rate: `0.315625`
```json
{
  "duration_drift_p90": 1.573059,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.723 | 0.704 | noisy |
| 3 | 1 | 0.230 | 0.223 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.870 | 0.839 | noisy |
| 5 | 1 | 0.557 | 0.544 | noisy |
| 5 | 2 | 0.171 | 0.171 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.914 | 0.869 | noisy |
| 7 | 1 | 0.752 | 0.732 | noisy |
| 7 | 2 | 0.452 | 0.449 | noisy |
| 7 | 3 | 0.134 | 0.134 | acceptable |
| 9 | 0 | 0.936 | 0.878 | noisy |
| 9 | 1 | 0.856 | 0.830 | noisy |
| 9 | 2 | 0.638 | 0.628 | noisy |
| 9 | 3 | 0.362 | 0.362 | noisy |

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
