# Body Profile Calibration Report

- generated_utc: `2026-03-18T07:49:10+00:00`
- profile_context: `quick`
- overall_status: **WARN**
- history_samples: `213`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.479 | 0.461 | loosen_duration+tighten_health | noisy |
| standard | 0.479 | 0.461 | loosen_duration+tighten_health | noisy |
| strict | 0.822 | 0.816 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.29108`
- observed_false_regression_rate: `0.28169`
```json
{
  "duration_drift_p90": 1.113943,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.673 | 0.645 | noisy |
| 3 | 1 | 0.194 | 0.185 | noisy |
| 3 | 2 | 0.005 | 0.005 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.818 | 0.770 | noisy |
| 5 | 1 | 0.493 | 0.474 | noisy |
| 5 | 2 | 0.134 | 0.134 | acceptable |
| 5 | 3 | 0.010 | 0.010 | acceptable |
| 7 | 0 | 0.874 | 0.807 | noisy |
| 7 | 1 | 0.696 | 0.667 | noisy |
| 7 | 2 | 0.362 | 0.357 | noisy |
| 7 | 3 | 0.097 | 0.097 | acceptable |
| 9 | 0 | 0.902 | 0.815 | noisy |
| 9 | 1 | 0.810 | 0.771 | noisy |
| 9 | 2 | 0.556 | 0.541 | noisy |
| 9 | 3 | 0.283 | 0.283 | noisy |

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
