# Body Profile Calibration Report

- generated_utc: `2026-03-31T01:24:21+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `335`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.639 | 0.631 | loosen_duration+tighten_health | noisy |
| standard | 0.639 | 0.631 | loosen_duration+tighten_health | noisy |
| strict | 0.887 | 0.884 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.328358`
- observed_false_regression_rate: `0.322388`
```json
{
  "duration_drift_p90": 1.6,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.736 | 0.718 | noisy |
| 3 | 1 | 0.237 | 0.231 | noisy |
| 3 | 2 | 0.018 | 0.018 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.876 | 0.846 | noisy |
| 5 | 1 | 0.574 | 0.562 | noisy |
| 5 | 2 | 0.190 | 0.190 | noisy |
| 5 | 3 | 0.015 | 0.015 | acceptable |
| 7 | 0 | 0.918 | 0.875 | noisy |
| 7 | 1 | 0.763 | 0.745 | noisy |
| 7 | 2 | 0.471 | 0.468 | noisy |
| 7 | 3 | 0.152 | 0.152 | noisy |
| 9 | 0 | 0.939 | 0.884 | noisy |
| 9 | 1 | 0.862 | 0.838 | noisy |
| 9 | 2 | 0.654 | 0.645 | noisy |
| 9 | 3 | 0.391 | 0.391 | noisy |

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
