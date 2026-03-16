# Body Profile Calibration Report

- generated_utc: `2026-03-16T02:26:16+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `185`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.422 | 0.399 | loosen_duration+tighten_health | noisy |
| standard | 0.422 | 0.399 | loosen_duration+tighten_health | noisy |
| strict | 0.795 | 0.787 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.286486`
- observed_false_regression_rate: `0.275676`
```json
{
  "duration_drift_p90": 1.106906,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.661 | 0.628 | noisy |
| 3 | 1 | 0.191 | 0.180 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.807 | 0.751 | noisy |
| 5 | 1 | 0.481 | 0.459 | noisy |
| 5 | 2 | 0.144 | 0.144 | acceptable |
| 5 | 3 | 0.011 | 0.011 | acceptable |
| 7 | 0 | 0.860 | 0.782 | noisy |
| 7 | 1 | 0.682 | 0.648 | noisy |
| 7 | 2 | 0.374 | 0.369 | noisy |
| 7 | 3 | 0.112 | 0.112 | acceptable |
| 9 | 0 | 0.887 | 0.785 | noisy |
| 9 | 1 | 0.785 | 0.740 | noisy |
| 9 | 2 | 0.548 | 0.531 | noisy |
| 9 | 3 | 0.322 | 0.322 | noisy |

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
