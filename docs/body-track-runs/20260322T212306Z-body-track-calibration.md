# Body Profile Calibration Report

- generated_utc: `2026-03-22T21:23:06+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `263`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.570 | 0.559 | loosen_duration+tighten_health | noisy |
| standard | 0.570 | 0.559 | loosen_duration+tighten_health | noisy |
| strict | 0.856 | 0.852 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.315589`
- observed_false_regression_rate: `0.307985`
```json
{
  "duration_drift_p90": 1.281281,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.713 | 0.690 | noisy |
| 3 | 1 | 0.222 | 0.215 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.853 | 0.815 | noisy |
| 5 | 1 | 0.544 | 0.529 | noisy |
| 5 | 2 | 0.174 | 0.174 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.899 | 0.844 | noisy |
| 7 | 1 | 0.747 | 0.724 | noisy |
| 7 | 2 | 0.440 | 0.436 | noisy |
| 7 | 3 | 0.136 | 0.136 | acceptable |
| 9 | 0 | 0.922 | 0.851 | noisy |
| 9 | 1 | 0.847 | 0.816 | noisy |
| 9 | 2 | 0.631 | 0.620 | noisy |
| 9 | 3 | 0.361 | 0.361 | noisy |

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
