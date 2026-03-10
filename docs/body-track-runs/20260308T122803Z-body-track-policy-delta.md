# Body Profile Policy Delta Report

- generated_utc: `2026-03-08T12:28:03+00:00`
- overall_status: **PASS**
- apply_mode: `True`
- policy_updated: `False`
- history_samples: `98`

## Benchmark profile deltas
| profile | before_warn | after_warn | before_false_alert | after_false_alert | action |
|---|---:|---:|---:|---:|---|
| quick | 0.133 | 0.133 | 0.066 | 0.066 | keep |
| standard | 0.133 | 0.133 | 0.066 | 0.066 | keep |
| strict | 0.133 | 0.133 | 0.066 | 0.066 | keep |

## Regression window delta
| window_before | window_after | before_alert_rate | after_alert_rate | before_false_alert_rate | after_false_alert_rate | action |
|---|---|---:|---:|---:|---:|---|
| {'window_size': 3, 'max_regressions': 2} | {'window_size': 3, 'max_regressions': 2} | 0.010 | 0.010 | 0.010 | 0.010 | keep |

## Selected updates
```json
{
  "benchmark_profiles": {},
  "regression_window_policy": null
}
```
