# Body Track Smoke Report

- generated_utc: `2026-02-16T03:18:53+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.193238`
- body_health_score: `100.0`
- speed_band: `fast`

## Benchmark guardrail
- status: **PASS**
- trend: `stable`
```json
{
  "pass_rate": {
    "ok": true,
    "actual": 1.0,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": true,
    "actual": 0.193238,
    "threshold": 1.0
  },
  "body_health_score": {
    "ok": true,
    "actual": 100.0,
    "threshold": 95.0
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.030 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.040 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.124 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
- duration_seconds: `0.040`

### stdout (trimmed)
```
Registered DID: did:freed:34112446867b4b32858d1c97eda3553f
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7433412484794959, 'entropy_bits': 0.8216624098084235, 'top_states': [{'state': 0, 'probability': 0.7433412484794959}, {'state': 1, 'probability': 0.25665875152050405}], 'empirical_top_states': [{'state': 0, 'count': 381, 'frequency': 0.744140625}, {'state': 1, 'count': 131, 'frequency': 0.255859375}], 'expected_state_index': 0.25665875152050405, 'measurement_histogram': [381, 131]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.7433412484794959, 'entropy_bits': 0.8216624098084235, 'top_states': [{'state': 0, 'probability': 0.7433412484794959}, {'state': 1, 'probability': 0.25665875152050405}], 'empirical_top_states': [{'state': 0, 'count': 381, 'frequency': 0.744140625}, {'state': 1, 'count': 131, 'frequency': 0.255859375}], 'expected_state_index': 0.25665875152050405, 'measurement_histogram': [381, 131]}, 'waste_energy': 8.028642357127858, 'exotic_energy_generated': 2.0190949047519053, 'total_exotic_energy': 2.0190949047519053}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.5238073232063504, 'entropy_bits': 0.998363975170499, 'top_states': [{'state': 0, 'probability': 0.5238073232063504}, {'state': 1, 'probability': 0.4761926767936496}], 'empirical_top_states': [{'state': 0, 'count': 268, 'frequency': 0.5234375}, {'state': 1, 'count': 244, 'frequency': 0.4765625}], 'expected_state_index': 0.4761926767936496, 'measurement_histogram': [268, 244]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.5238073232063504, 'entropy_bits': 0.998363975170499, 'top_states': [{'state': 0, 'probability': 0.5238073232063504}, {'state': 1, 'probability': 0.4761926767936496}], 'empirical_top_states': [{'state': 0, 'count': 268, 'frequency': 0.5234375}, {'state': 1, 'count': 244, 'frequency': 0.4765625}], 'expected_state_index': 0.4761926767936496, 'measurement_histogram': [268, 244]}, 'waste_energy': 7.1443419920431674, 'exotic_energy_generated': 1.429561328028778, 'total_exotic_energy': 3.4486562327806833}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.724328,
  "final_total_exotic_energy": 3.448656
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.124`

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
