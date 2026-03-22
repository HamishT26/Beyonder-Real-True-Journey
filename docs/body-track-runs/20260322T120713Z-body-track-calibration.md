# Body Profile Calibration Report

- generated_utc: `2026-03-22T12:07:13+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `246`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.541 | 0.527 | loosen_duration+tighten_health | noisy |
| standard | 0.541 | 0.527 | loosen_duration+tighten_health | noisy |
| strict | 0.846 | 0.841 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313008`
- observed_false_regression_rate: `0.304878`
```json
{
  "duration_drift_p90": 1.262424,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.705 | 0.680 | noisy |
| 3 | 1 | 0.225 | 0.217 | noisy |
| 3 | 2 | 0.012 | 0.012 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.843 | 0.802 | noisy |
| 5 | 1 | 0.550 | 0.533 | noisy |
| 5 | 2 | 0.165 | 0.165 | noisy |
| 5 | 3 | 0.021 | 0.021 | acceptable |
| 7 | 0 | 0.892 | 0.833 | noisy |
| 7 | 1 | 0.738 | 0.713 | noisy |
| 7 | 2 | 0.442 | 0.438 | noisy |
| 7 | 3 | 0.129 | 0.129 | acceptable |
| 9 | 0 | 0.916 | 0.840 | noisy |
| 9 | 1 | 0.836 | 0.803 | noisy |
| 9 | 2 | 0.618 | 0.605 | noisy |
| 9 | 3 | 0.353 | 0.353 | noisy |

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
