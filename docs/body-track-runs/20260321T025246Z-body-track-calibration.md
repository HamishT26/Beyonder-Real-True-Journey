# Body Profile Calibration Report

- generated_utc: `2026-03-21T02:52:46+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `231`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.515 | 0.500 | loosen_duration+tighten_health | noisy |
| standard | 0.515 | 0.500 | loosen_duration+tighten_health | noisy |
| strict | 0.835 | 0.830 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.307359`
- observed_false_regression_rate: `0.298701`
```json
{
  "duration_drift_p90": 1.126855,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.699 | 0.672 | noisy |
| 3 | 1 | 0.218 | 0.210 | noisy |
| 3 | 2 | 0.013 | 0.013 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.833 | 0.789 | noisy |
| 5 | 1 | 0.533 | 0.515 | noisy |
| 5 | 2 | 0.167 | 0.167 | noisy |
| 5 | 3 | 0.022 | 0.022 | acceptable |
| 7 | 0 | 0.884 | 0.822 | noisy |
| 7 | 1 | 0.720 | 0.693 | noisy |
| 7 | 2 | 0.413 | 0.409 | noisy |
| 7 | 3 | 0.138 | 0.138 | acceptable |
| 9 | 0 | 0.910 | 0.830 | noisy |
| 9 | 1 | 0.825 | 0.789 | noisy |
| 9 | 2 | 0.592 | 0.578 | noisy |
| 9 | 3 | 0.336 | 0.336 | noisy |

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
