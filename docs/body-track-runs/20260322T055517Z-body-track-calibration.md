# Body Profile Calibration Report

- generated_utc: `2026-03-22T05:55:17+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `236`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.525 | 0.511 | loosen_duration+tighten_health | noisy |
| standard | 0.525 | 0.511 | loosen_duration+tighten_health | noisy |
| strict | 0.839 | 0.834 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.313559`
- observed_false_regression_rate: `0.305085`
```json
{
  "duration_drift_p90": 1.176755,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.701 | 0.675 | noisy |
| 3 | 1 | 0.226 | 0.218 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.836 | 0.793 | noisy |
| 5 | 1 | 0.539 | 0.522 | noisy |
| 5 | 2 | 0.168 | 0.168 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.887 | 0.826 | noisy |
| 7 | 1 | 0.726 | 0.700 | noisy |
| 7 | 2 | 0.426 | 0.422 | noisy |
| 7 | 3 | 0.135 | 0.135 | acceptable |
| 9 | 0 | 0.912 | 0.833 | noisy |
| 9 | 1 | 0.829 | 0.794 | noisy |
| 9 | 2 | 0.601 | 0.588 | noisy |
| 9 | 3 | 0.351 | 0.351 | noisy |

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
