# Body Profile Calibration Report

- generated_utc: `2026-03-25T20:00:07+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `309`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.621 | 0.613 | loosen_duration+tighten_health | noisy |
| standard | 0.621 | 0.613 | loosen_duration+tighten_health | noisy |
| strict | 0.877 | 0.874 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.317152`
- observed_false_regression_rate: `0.31068`
```json
{
  "duration_drift_p90": 1.369982,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.720 | 0.700 | noisy |
| 3 | 1 | 0.221 | 0.215 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.866 | 0.833 | noisy |
| 5 | 1 | 0.544 | 0.531 | noisy |
| 5 | 2 | 0.167 | 0.167 | noisy |
| 5 | 3 | 0.016 | 0.016 | acceptable |
| 7 | 0 | 0.911 | 0.865 | noisy |
| 7 | 1 | 0.743 | 0.723 | noisy |
| 7 | 2 | 0.436 | 0.432 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.934 | 0.874 | noisy |
| 9 | 1 | 0.850 | 0.824 | noisy |
| 9 | 2 | 0.625 | 0.615 | noisy |
| 9 | 3 | 0.349 | 0.349 | noisy |

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
