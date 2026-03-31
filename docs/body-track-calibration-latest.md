# Body Profile Calibration Report

- generated_utc: `2026-03-31T14:26:34+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `359`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.618 | 0.611 | loosen_duration+tighten_health | noisy |
| standard | 0.618 | 0.611 | loosen_duration+tighten_health | noisy |
| strict | 0.894 | 0.892 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.325905`
- observed_false_regression_rate: `0.320334`
```json
{
  "duration_drift_p90": 1.339663,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.728 | 0.711 | noisy |
| 3 | 1 | 0.232 | 0.227 | noisy |
| 3 | 2 | 0.017 | 0.017 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.865 | 0.837 | noisy |
| 5 | 1 | 0.569 | 0.558 | noisy |
| 5 | 2 | 0.189 | 0.189 | noisy |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.909 | 0.870 | noisy |
| 7 | 1 | 0.754 | 0.737 | noisy |
| 7 | 2 | 0.479 | 0.476 | noisy |
| 7 | 3 | 0.142 | 0.142 | acceptable |
| 9 | 0 | 0.934 | 0.883 | noisy |
| 9 | 1 | 0.852 | 0.829 | noisy |
| 9 | 2 | 0.655 | 0.647 | noisy |
| 9 | 3 | 0.393 | 0.393 | noisy |

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
