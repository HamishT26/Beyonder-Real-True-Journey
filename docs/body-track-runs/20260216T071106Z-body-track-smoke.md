# Body Track Smoke Report

- generated_utc: `2026-02-16T07:11:06+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.131915`
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
    "actual": 0.131915,
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
| compile_python_modules | PASS | 0 | 0.031 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.034 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.068 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.031`

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
Registered DID: did:freed:fa572fb500e84a12aad8d3d81bdb17ce
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6538772349269016, 'entropy_bits': 0.9305576079853864, 'top_states': [{'state': 1, 'probability': 0.6538772349269016}, {'state': 0, 'probability': 0.3461227650730983}], 'empirical_top_states': [{'state': 1, 'count': 335, 'frequency': 0.654296875}, {'state': 0, 'count': 177, 'frequency': 0.345703125}], 'expected_state_index': 0.6538772349269016, 'measurement_histogram': [177, 335]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6538772349269016, 'entropy_bits': 0.9305576079853864, 'top_states': [{'state': 1, 'probability': 0.6538772349269016}, {'state': 0, 'probability': 0.3461227650730983}], 'empirical_top_states': [{'state': 1, 'count': 335, 'frequency': 0.654296875}, {'state': 0, 'count': 177, 'frequency': 0.345703125}], 'expected_state_index': 0.6538772349269016, 'measurement_histogram': [177, 335]}, 'waste_energy': 8.464969657273445, 'exotic_energy_generated': 2.30997977151563, 'total_exotic_energy': 2.30997977151563}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.9328531323594262, 'entropy_bits': 0.3551849632176137, 'top_states': [{'state': 1, 'probability': 0.9328531323594262}, {'state': 0, 'probability': 0.06714686764057383}], 'empirical_top_states': [{'state': 1, 'count': 478, 'frequency': 0.93359375}, {'state': 0, 'count': 34, 'frequency': 0.06640625}], 'expected_state_index': 0.9328531323594262, 'measurement_histogram': [34, 478]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.9328531323594262, 'entropy_bits': 0.3551849632176137, 'top_states': [{'state': 1, 'probability': 0.9328531323594262}, {'state': 0, 'probability': 0.06714686764057383}], 'empirical_top_states': [{'state': 1, 'count': 478, 'frequency': 0.93359375}, {'state': 0, 'count': 34, 'frequency': 0.06640625}], 'expected_state_index': 0.9328531323594262, 'measurement_histogram': [34, 478]}, 'waste_energy': 7.829571584654849, 'exotic_energy_generated': 1.8863810564365655, 'total_exotic_energy': 4.196360827952195}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.09818,
  "final_total_exotic_energy": 4.196361
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.068`

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
