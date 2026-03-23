# Body Profile Calibration Report

- generated_utc: `2026-03-23T01:33:33+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `264`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.572 | 0.560 | loosen_duration+tighten_health | noisy |
| standard | 0.572 | 0.560 | loosen_duration+tighten_health | noisy |
| strict | 0.856 | 0.852 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.314394`
- observed_false_regression_rate: `0.306818`
```json
{
  "duration_drift_p90": 1.274996,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.714 | 0.691 | noisy |
| 3 | 1 | 0.221 | 0.214 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.854 | 0.815 | noisy |
| 5 | 1 | 0.542 | 0.527 | noisy |
| 5 | 2 | 0.173 | 0.173 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.899 | 0.845 | noisy |
| 7 | 1 | 0.744 | 0.721 | noisy |
| 7 | 2 | 0.438 | 0.434 | noisy |
| 7 | 3 | 0.136 | 0.136 | acceptable |
| 9 | 0 | 0.922 | 0.852 | noisy |
| 9 | 1 | 0.848 | 0.816 | noisy |
| 9 | 2 | 0.629 | 0.617 | noisy |
| 9 | 3 | 0.359 | 0.359 | noisy |

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
