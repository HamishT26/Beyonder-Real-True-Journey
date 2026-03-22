# Body Profile Calibration Report

- generated_utc: `2026-03-22T20:01:55+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `258`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.562 | 0.550 | loosen_duration+tighten_health | noisy |
| standard | 0.562 | 0.550 | loosen_duration+tighten_health | noisy |
| strict | 0.853 | 0.849 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.317829`
- observed_false_regression_rate: `0.310078`
```json
{
  "duration_drift_p90": 1.397453,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.715 | 0.691 | noisy |
| 3 | 1 | 0.227 | 0.219 | noisy |
| 3 | 2 | 0.016 | 0.016 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.850 | 0.811 | noisy |
| 5 | 1 | 0.555 | 0.539 | noisy |
| 5 | 2 | 0.177 | 0.177 | noisy |
| 5 | 3 | 0.020 | 0.020 | acceptable |
| 7 | 0 | 0.897 | 0.841 | noisy |
| 7 | 1 | 0.746 | 0.722 | noisy |
| 7 | 2 | 0.444 | 0.440 | noisy |
| 7 | 3 | 0.139 | 0.139 | acceptable |
| 9 | 0 | 0.920 | 0.848 | noisy |
| 9 | 1 | 0.844 | 0.812 | noisy |
| 9 | 2 | 0.628 | 0.616 | noisy |
| 9 | 3 | 0.360 | 0.360 | noisy |

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
