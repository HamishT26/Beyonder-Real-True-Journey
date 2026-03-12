# Body Profile Calibration Report

- generated_utc: `2026-03-12T11:18:58+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `159`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.377 | 0.349 | loosen_duration+tighten_health | noisy |
| standard | 0.377 | 0.349 | loosen_duration+tighten_health | noisy |
| strict | 0.767 | 0.757 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.264151`
- observed_false_regression_rate: `0.251572`
```json
{
  "duration_drift_p90": 1.01777,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.631 | 0.592 | noisy |
| 3 | 1 | 0.166 | 0.153 | noisy |
| 3 | 2 | 0.006 | 0.006 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.787 | 0.723 | noisy |
| 5 | 1 | 0.432 | 0.406 | noisy |
| 5 | 2 | 0.123 | 0.123 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.843 | 0.752 | noisy |
| 7 | 1 | 0.647 | 0.608 | noisy |
| 7 | 2 | 0.327 | 0.320 | noisy |
| 7 | 3 | 0.092 | 0.092 | acceptable |
| 9 | 0 | 0.868 | 0.748 | noisy |
| 9 | 1 | 0.762 | 0.709 | noisy |
| 9 | 2 | 0.510 | 0.490 | noisy |
| 9 | 3 | 0.272 | 0.272 | noisy |

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
