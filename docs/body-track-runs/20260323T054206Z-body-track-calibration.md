# Body Profile Calibration Report

- generated_utc: `2026-03-23T05:42:06+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `279`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.584 | 0.574 | loosen_duration+tighten_health | noisy |
| standard | 0.584 | 0.574 | loosen_duration+tighten_health | noisy |
| strict | 0.864 | 0.860 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.308244`
- observed_false_regression_rate: `0.301075`
```json
{
  "duration_drift_p90": 1.243567,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.700 | 0.679 | noisy |
| 3 | 1 | 0.217 | 0.209 | noisy |
| 3 | 2 | 0.014 | 0.014 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.855 | 0.818 | noisy |
| 5 | 1 | 0.527 | 0.513 | noisy |
| 5 | 2 | 0.164 | 0.164 | noisy |
| 5 | 3 | 0.018 | 0.018 | acceptable |
| 7 | 0 | 0.905 | 0.853 | noisy |
| 7 | 1 | 0.733 | 0.711 | noisy |
| 7 | 2 | 0.421 | 0.418 | noisy |
| 7 | 3 | 0.128 | 0.128 | acceptable |
| 9 | 0 | 0.926 | 0.860 | noisy |
| 9 | 1 | 0.841 | 0.812 | noisy |
| 9 | 2 | 0.616 | 0.605 | noisy |
| 9 | 3 | 0.339 | 0.339 | noisy |

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
