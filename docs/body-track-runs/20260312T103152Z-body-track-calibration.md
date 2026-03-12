# Body Profile Calibration Report

- generated_utc: `2026-03-12T10:31:52+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `155`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.387 | 0.358 | loosen_duration+tighten_health | noisy |
| standard | 0.387 | 0.358 | loosen_duration+tighten_health | noisy |
| strict | 0.761 | 0.750 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.270968`
- observed_false_regression_rate: `0.258065`
```json
{
  "duration_drift_p90": 1.032251,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.647 | 0.608 | noisy |
| 3 | 1 | 0.170 | 0.157 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.795 | 0.728 | noisy |
| 5 | 1 | 0.444 | 0.417 | noisy |
| 5 | 2 | 0.126 | 0.126 | acceptable |
| 5 | 3 | 0.013 | 0.013 | acceptable |
| 7 | 0 | 0.839 | 0.745 | noisy |
| 7 | 1 | 0.658 | 0.617 | noisy |
| 7 | 2 | 0.336 | 0.329 | noisy |
| 7 | 3 | 0.094 | 0.094 | acceptable |
| 9 | 0 | 0.864 | 0.741 | noisy |
| 9 | 1 | 0.762 | 0.707 | noisy |
| 9 | 2 | 0.524 | 0.503 | noisy |
| 9 | 3 | 0.279 | 0.279 | noisy |

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
