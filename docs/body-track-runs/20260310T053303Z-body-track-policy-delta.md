# Body Profile Policy Delta Report

- generated_utc: `2026-03-10T05:33:03+00:00`
- overall_status: **PASS**
- apply_mode: `True`
- policy_updated: `True`
- history_samples: `115`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.348 | 0.104 | 0.306 | 0.046 | apply_recommended_thresholds |
| standard | 0.348 | 0.104 | 0.306 | 0.046 | apply_recommended_thresholds |
| strict | 0.696 | 0.104 | 0.676 | 0.046 | apply_recommended_thresholds |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 5, 'max_regressions': 2} | {'window_size': 3, 'max_regressions': 3} | 0.144 | 0.000 | 0.144 | 0.000 | apply_recommended_window |

## Selected updates
```json
{
  "benchmark_profiles": {
    "quick": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 5.88,
      "min_health_score": 66.17
    },
    "standard": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 5.88,
      "min_health_score": 66.17
    },
    "strict": {
      "min_pass_rate": 1.0,
      "max_duration_sec": 5.88,
      "min_health_score": 66.17
    }
  },
  "regression_window_policy": {
    "window_size": 3,
    "max_regressions": 3
  }
}
```
