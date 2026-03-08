# Body Profile Policy Delta Report

- generated_utc: `2026-03-08T12:58:13+00:00`
- overall_status: **PASS**
- apply_mode: `True`
- policy_updated: `True`
- history_samples: `99`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.141 | 0.121 | 0.076 | 0.054 | apply_recommended_thresholds |
| standard | 0.141 | 0.121 | 0.076 | 0.054 | apply_recommended_thresholds |
| strict | 0.141 | 0.121 | 0.076 | 0.054 | apply_recommended_thresholds |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 3, 'max_regressions': 2} | {'window_size': 3, 'max_regressions': 3} | 0.010 | 0.000 | 0.010 | 0.000 | apply_recommended_window |

## Selected updates
```json
{
  "benchmark_profiles": {
    "quick": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 3.364,
      "min_health_score": 66.17
    },
    "standard": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 3.364,
      "min_health_score": 66.17
    },
    "strict": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 3.364,
      "min_health_score": 66.17
    }
  },
  "regression_window_policy": {
    "window_size": 3,
    "max_regressions": 3
  }
}
```
