# Body Profile Calibration Report

- generated_utc: `2026-03-12T05:11:47+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `147`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.367 | 0.336 | loosen_duration+tighten_health | noisy |
| standard | 0.367 | 0.336 | loosen_duration+tighten_health | noisy |
| strict | 0.748 | 0.736 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.272109`
- observed_false_regression_rate: `0.258503`
```json
{
  "duration_drift_p90": 1.025011,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.628 | 0.586 | noisy |
| 3 | 1 | 0.172 | 0.159 | noisy |
| 3 | 2 | 0.007 | 0.007 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.783 | 0.713 | noisy |
| 5 | 1 | 0.427 | 0.399 | noisy |
| 5 | 2 | 0.126 | 0.126 | acceptable |
| 5 | 3 | 0.014 | 0.014 | acceptable |
| 7 | 0 | 0.830 | 0.730 | noisy |
| 7 | 1 | 0.638 | 0.596 | noisy |
| 7 | 2 | 0.326 | 0.319 | noisy |
| 7 | 3 | 0.099 | 0.099 | acceptable |
| 9 | 0 | 0.856 | 0.727 | noisy |
| 9 | 1 | 0.748 | 0.691 | noisy |
| 9 | 2 | 0.504 | 0.482 | noisy |
| 9 | 3 | 0.281 | 0.281 | noisy |

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
