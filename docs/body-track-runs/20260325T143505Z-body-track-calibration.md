# Body Profile Calibration Report

- generated_utc: `2026-03-25T14:35:05+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `306`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.618 | 0.609 | loosen_duration+tighten_health | noisy |
| standard | 0.618 | 0.609 | loosen_duration+tighten_health | noisy |
| strict | 0.876 | 0.873 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.316993`
- observed_false_regression_rate: `0.310458`
```json
{
  "duration_drift_p90": 1.452396,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.717 | 0.697 | noisy |
| 3 | 1 | 0.220 | 0.214 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.864 | 0.831 | noisy |
| 5 | 1 | 0.540 | 0.526 | noisy |
| 5 | 2 | 0.166 | 0.166 | noisy |
| 5 | 3 | 0.017 | 0.017 | acceptable |
| 7 | 0 | 0.910 | 0.863 | noisy |
| 7 | 1 | 0.740 | 0.720 | noisy |
| 7 | 2 | 0.430 | 0.427 | noisy |
| 7 | 3 | 0.130 | 0.130 | acceptable |
| 9 | 0 | 0.933 | 0.872 | noisy |
| 9 | 1 | 0.849 | 0.822 | noisy |
| 9 | 2 | 0.621 | 0.611 | noisy |
| 9 | 3 | 0.346 | 0.346 | noisy |

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
