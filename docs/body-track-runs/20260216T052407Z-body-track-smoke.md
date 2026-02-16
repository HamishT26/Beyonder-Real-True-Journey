# Body Track Smoke Report

- generated_utc: `2026-02-16T05:24:07+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.131269`
- body_health_score: `100.0`
- speed_band: `fast`

## Benchmark guardrail
- status: **PASS**
- profile: `quick`
- trend: `stable`
```json
{
  "min_pass_rate": 1.0,
  "max_duration_sec": 1.5,
  "min_health_score": 94.0
}
```

### check_results
```json
{
  "pass_rate": {
    "ok": true,
    "actual": 1.0,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": true,
    "actual": 0.131269,
    "threshold": 1.5
  },
  "body_health_score": {
    "ok": true,
    "actual": 100.0,
    "threshold": 94.0
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.030 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.034 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.067 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.030`

### stdout (trimmed)
```
(empty)
```

### stderr (trimmed)
```
(empty)
```

## run_full_orchestrator_demo

- returncode: `0`
- duration_seconds: `0.034`

### stdout (trimmed)
```
Registered DID: did:freed:4754cf4ad33b447381918b043631e964
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.5201558305145433, 'entropy_bits': 0.9988274709417642, 'top_states': [{'state': 0, 'probability': 0.5201558305145433}, {'state': 1, 'probability': 0.4798441694854566}], 'empirical_top_states': [{'state': 0, 'count': 266, 'frequency': 0.51953125}, {'state': 1, 'count': 246, 'frequency': 0.48046875}], 'expected_state_index': 0.4798441694854566, 'measurement_histogram': [266, 246]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.5201558305145433, 'entropy_bits': 0.9988274709417642, 'top_states': [{'state': 0, 'probability': 0.5201558305145433}, {'state': 1, 'probability': 0.4798441694854566}], 'empirical_top_states': [{'state': 0, 'count': 266, 'frequency': 0.51953125}, {'state': 1, 'count': 246, 'frequency': 0.48046875}], 'expected_state_index': 0.4798441694854566, 'measurement_histogram': [266, 246]}, 'waste_energy': 7.48910743787849, 'exotic_energy_generated': 1.6594049585856594, 'total_exotic_energy': 1.6594049585856594}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8970599005463713, 'entropy_bits': 0.47824680016222093, 'top_states': [{'state': 0, 'probability': 0.8970599005463713}, {'state': 1, 'probability': 0.10294009945362875}], 'empirical_top_states': [{'state': 0, 'count': 459, 'frequency': 0.896484375}, {'state': 1, 'count': 53, 'frequency': 0.103515625}], 'expected_state_index': 0.10294009945362875, 'measurement_histogram': [459, 53]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8970599005463713, 'entropy_bits': 0.47824680016222093, 'top_states': [{'state': 0, 'probability': 0.8970599005463713}, {'state': 1, 'probability': 0.10294009945362875}], 'empirical_top_states': [{'state': 0, 'count': 459, 'frequency': 0.896484375}, {'state': 1, 'count': 53, 'frequency': 0.103515625}], 'expected_state_index': 0.10294009945362875, 'measurement_histogram': [459, 53]}, 'waste_energy': 7.032091965526156, 'exotic_energy_generated': 1.3547279770174376, 'total_exotic_energy': 3.0141329356030973}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.507066,
  "final_total_exotic_energy": 3.014133
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.067`

### stdout (trimmed)
```
Gamma=0.0000: energy density ratio = 1.00000
Gamma=0.0100: energy density ratio = 1.00993
Gamma=0.0500: energy density ratio = 1.04964
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "gamma_count": 3,
  "gamma_ratios": {
    "0.0000": 1.0,
    "0.0100": 1.00993,
    "0.0500": 1.04964
  },
  "ratio_min": 1.0,
  "ratio_max": 1.04964,
  "ratio_span": 0.04964
}
```
