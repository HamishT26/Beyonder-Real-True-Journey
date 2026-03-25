# Body Profile Calibration Report

- generated_utc: `2026-03-25T11:22:36+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `296`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.605 | 0.595 | loosen_duration+tighten_health | noisy |
| standard | 0.605 | 0.595 | loosen_duration+tighten_health | noisy |
| strict | 0.872 | 0.869 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.317568`
- observed_false_regression_rate: `0.310811`
```json
{
  "duration_drift_p90": 1.452396,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.714 | 0.694 | noisy |
| 3 | 1 | 0.224 | 0.218 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.860 | 0.825 | noisy |
| 5 | 1 | 0.545 | 0.531 | noisy |
| 5 | 2 | 0.171 | 0.171 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.907 | 0.859 | noisy |
| 7 | 1 | 0.738 | 0.717 | noisy |
| 7 | 2 | 0.438 | 0.434 | noisy |
| 7 | 3 | 0.134 | 0.134 | acceptable |
| 9 | 0 | 0.931 | 0.868 | noisy |
| 9 | 1 | 0.844 | 0.816 | noisy |
| 9 | 2 | 0.622 | 0.611 | noisy |
| 9 | 3 | 0.354 | 0.354 | noisy |

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
