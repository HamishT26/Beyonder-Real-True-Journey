# Body Profile Calibration Report

- generated_utc: `2026-03-23T02:38:01+00:00`
- profile_context: `standard`
- overall_status: **WARN**
- history_samples: `268`

## Benchmark profile analysis
| profile | warn_rate | false_alert_rate | recommendation_action | quality |
|---|---:|---:|---|---|
| quick | 0.578 | 0.567 | loosen_duration+tighten_health | noisy |
| standard | 0.578 | 0.567 | loosen_duration+tighten_health | noisy |
| strict | 0.858 | 0.854 | loosen_duration+tighten_health | noisy |

## Trend alert analysis
- observed_regression_rate: `0.317164`
- observed_false_regression_rate: `0.309701`
```json
{
  "duration_drift_p90": 1.397453,
  "health_drop_p90": 0.0
}
```

## Regression window diagnostics
| window_size | max_regressions | alert_rate | false_alert_rate | quality |
|---:|---:|---:|---:|---|
| 3 | 0 | 0.711 | 0.688 | noisy |
| 3 | 1 | 0.222 | 0.214 | noisy |
| 3 | 2 | 0.015 | 0.015 | acceptable |
| 3 | 3 | 0.000 | 0.000 | acceptable |
| 5 | 0 | 0.856 | 0.818 | noisy |
| 5 | 1 | 0.538 | 0.523 | noisy |
| 5 | 2 | 0.170 | 0.170 | noisy |
| 5 | 3 | 0.019 | 0.019 | acceptable |
| 7 | 0 | 0.901 | 0.847 | noisy |
| 7 | 1 | 0.740 | 0.718 | noisy |
| 7 | 2 | 0.435 | 0.431 | noisy |
| 7 | 3 | 0.134 | 0.134 | acceptable |
| 9 | 0 | 0.923 | 0.854 | noisy |
| 9 | 1 | 0.846 | 0.815 | noisy |
| 9 | 2 | 0.623 | 0.612 | noisy |
| 9 | 3 | 0.354 | 0.354 | noisy |

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
