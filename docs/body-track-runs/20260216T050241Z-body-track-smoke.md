# Body Track Smoke Report

- generated_utc: `2026-02-16T05:02:41+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.135108`
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
    "actual": 0.135108,
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
| run_full_orchestrator_demo | PASS | 0 | 0.036 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.069 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.036`

### stdout (trimmed)
```
Registered DID: did:freed:15f9ecc18db349018af22d93e928296b
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5975821856133623, 'entropy_bits': 0.9723473666204029, 'top_states': [{'state': 1, 'probability': 0.5975821856133623}, {'state': 0, 'probability': 0.4024178143866377}], 'empirical_top_states': [{'state': 1, 'count': 306, 'frequency': 0.59765625}, {'state': 0, 'count': 206, 'frequency': 0.40234375}], 'expected_state_index': 0.5975821856133623, 'measurement_histogram': [206, 306]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5975821856133623, 'entropy_bits': 0.9723473666204029, 'top_states': [{'state': 1, 'probability': 0.5975821856133623}, {'state': 0, 'probability': 0.4024178143866377}], 'empirical_top_states': [{'state': 1, 'count': 306, 'frequency': 0.59765625}, {'state': 0, 'count': 206, 'frequency': 0.40234375}], 'expected_state_index': 0.5975821856133623, 'measurement_histogram': [206, 306]}, 'waste_energy': 7.771244428294436, 'exotic_energy_generated': 1.847496285529624, 'total_exotic_energy': 1.847496285529624}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7468105172841983, 'entropy_bits': 0.8162943084351677, 'top_states': [{'state': 0, 'probability': 0.7468105172841983}, {'state': 1, 'probability': 0.2531894827158016}], 'empirical_top_states': [{'state': 0, 'count': 382, 'frequency': 0.74609375}, {'state': 1, 'count': 130, 'frequency': 0.25390625}], 'expected_state_index': 0.2531894827158016, 'measurement_histogram': [382, 130]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7468105172841983, 'entropy_bits': 0.8162943084351677, 'top_states': [{'state': 0, 'probability': 0.7468105172841983}, {'state': 1, 'probability': 0.2531894827158016}], 'empirical_top_states': [{'state': 0, 'count': 382, 'frequency': 0.74609375}, {'state': 1, 'count': 130, 'frequency': 0.25390625}], 'expected_state_index': 0.2531894827158016, 'measurement_histogram': [382, 130]}, 'waste_energy': 6.480890430662553, 'exotic_energy_generated': 0.9872602871083684, 'total_exotic_energy': 2.8347565726379926}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.417378,
  "final_total_exotic_energy": 2.834757
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.069`

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
