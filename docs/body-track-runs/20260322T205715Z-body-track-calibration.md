# Body Profile Calibration Report

- generated_utc: `2026-03-22T20:57:15+00:00`
- profile_context: `deep`
- overall_status: **WARN**
- history_samples: `262`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.569 | 0.557 | loosen_duration+tighten_health | noisy |
| standard | 0.569 | 0.557 | loosen_duration+tighten_health | noisy |
| strict | 0.855 | 0.851 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.316794`
- observed_false_regression_rate: `0.30916`
```json
{
  "duration_drift_p90": 1.287567,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.712 | 0.688 | noisy |
| 3 | 1 | 0.223 | 0.215 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.853 | 0.814 | noisy |
| 5 | 1 | 0.547 | 0.531 | noisy |
| 5 | 2 | 0.174 | 0.174 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.898 | 0.844 | noisy |
| 7 | 1 | 0.746 | 0.723 | noisy |
| 7 | 2 | 0.441 | 0.438 | noisy |
| 7 | 3 | 0.137 | 0.137 | acceptable |
| 9 | 0 | 0.921 | 0.850 | noisy |
| 9 | 1 | 0.846 | 0.815 | noisy |
| 9 | 2 | 0.634 | 0.622 | noisy |
| 9 | 3 | 0.362 | 0.362 | noisy |

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
