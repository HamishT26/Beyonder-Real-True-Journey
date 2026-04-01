# Body Profile Policy Delta Report

- generated_utc: `2026-04-01T02:43:08+00:00`
- overall_status: **PASS**
- apply_mode: `False`
- policy_updated: `False`
- history_samples: `373`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.054 | 0.070 | 0.036 | 0.052 | keep |
| standard | 0.021 | 0.070 | 0.003 | 0.052 | keep |
| strict | 0.054 | 0.070 | 0.036 | 0.052 | keep |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 3, 'max_regressions': 3} | {'window_size': 3, 'max_regressions': 3} | 0.000 | 0.000 | 0.000 | 0.000 | keep |

## Selected updates
```json
{
  "benchmark_profiles": {},
  "regression_window_policy": null
}
```
