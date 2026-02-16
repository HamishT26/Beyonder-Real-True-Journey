# Body Track Smoke Report

- generated_utc: `2026-02-16T06:21:28+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.136266`
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
    "actual": 0.136266,
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
| run_full_orchestrator_demo | PASS | 0 | 0.035 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.072 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.035`

### stdout (trimmed)
```
Registered DID: did:freed:66dd6e1d4298486ebb1b23dab8b56f4c
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6755866539100049, 'entropy_bits': 0.9091163945882129, 'top_states': [{'state': 1, 'probability': 0.6755866539100049}, {'state': 0, 'probability': 0.32441334608999506}], 'empirical_top_states': [{'state': 1, 'count': 346, 'frequency': 0.67578125}, {'state': 0, 'count': 166, 'frequency': 0.32421875}], 'expected_state_index': 0.6755866539100049, 'measurement_histogram': [166, 346]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6755866539100049, 'entropy_bits': 0.9091163945882129, 'top_states': [{'state': 1, 'probability': 0.6755866539100049}, {'state': 0, 'probability': 0.32441334608999506}], 'empirical_top_states': [{'state': 1, 'count': 346, 'frequency': 0.67578125}, {'state': 0, 'count': 166, 'frequency': 0.32421875}], 'expected_state_index': 0.6755866539100049, 'measurement_histogram': [166, 346]}, 'waste_energy': 7.973704904449647, 'exotic_energy_generated': 1.9824699362997646, 'total_exotic_energy': 1.9824699362997646}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5199154013448186, 'entropy_bits': 0.9988552845289573, 'top_states': [{'state': 1, 'probability': 0.5199154013448186}, {'state': 0, 'probability': 0.4800845986551814}], 'empirical_top_states': [{'state': 1, 'count': 266, 'frequency': 0.51953125}, {'state': 0, 'count': 246, 'frequency': 0.48046875}], 'expected_state_index': 0.5199154013448186, 'measurement_histogram': [246, 266]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5199154013448186, 'entropy_bits': 0.9988552845289573, 'top_states': [{'state': 1, 'probability': 0.5199154013448186}, {'state': 0, 'probability': 0.4800845986551814}], 'empirical_top_states': [{'state': 1, 'count': 266, 'frequency': 0.51953125}, {'state': 0, 'count': 246, 'frequency': 0.48046875}], 'expected_state_index': 0.5199154013448186, 'measurement_histogram': [246, 266]}, 'waste_energy': 6.760739038618359, 'exotic_energy_generated': 1.1738260257455724, 'total_exotic_energy': 3.156295962045337}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.578148,
  "final_total_exotic_energy": 3.156296
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.072`

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
