# Body Profile Calibration Report

- generated_utc: `2026-03-21T02:05:16+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `230`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.513 | 0.498 | loosen_duration+tighten_health | noisy |
| standard | 0.513 | 0.498 | loosen_duration+tighten_health | noisy |
| strict | 0.835 | 0.830 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.308696`
- observed_false_regression_rate: `0.3`
```json
{
  "duration_drift_p90": 1.136835,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.697 | 0.671 | noisy |
| 3 | 1 | 0.219 | 0.211 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.832 | 0.788 | noisy |
| 5 | 1 | 0.531 | 0.513 | noisy |
| 5 | 2 | 0.168 | 0.168 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.884 | 0.821 | noisy |
| 7 | 1 | 0.719 | 0.692 | noisy |
| 7 | 2 | 0.411 | 0.406 | noisy |
| 7 | 3 | 0.138 | 0.138 | acceptable |
| 9 | 0 | 0.910 | 0.829 | noisy |
| 9 | 1 | 0.824 | 0.788 | noisy |
| 9 | 2 | 0.590 | 0.577 | noisy |
| 9 | 3 | 0.333 | 0.333 | noisy |

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
