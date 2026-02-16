# Body Track Smoke Report

- generated_utc: `2026-02-16T02:40:43+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.189112`
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
    "actual": 0.189112,
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
| compile_python_modules | PASS | 0 | 0.039 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.035 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.115 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.039`

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
Registered DID: did:freed:85f1b34130ec4d9fb0e1e3dde844645d
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.5528855026657565, 'entropy_bits': 0.991914805511622, 'top_states': [{'state': 0, 'probability': 0.5528855026657565}, {'state': 1, 'probability': 0.4471144973342435}], 'empirical_top_states': [{'state': 0, 'count': 283, 'frequency': 0.552734375}, {'state': 1, 'count': 229, 'frequency': 0.447265625}], 'expected_state_index': 0.4471144973342435, 'measurement_histogram': [283, 229]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.5528855026657565, 'entropy_bits': 0.991914805511622, 'top_states': [{'state': 0, 'probability': 0.5528855026657565}, {'state': 1, 'probability': 0.4471144973342435}], 'empirical_top_states': [{'state': 0, 'count': 283, 'frequency': 0.552734375}, {'state': 1, 'count': 229, 'frequency': 0.447265625}], 'expected_state_index': 0.4471144973342435, 'measurement_histogram': [283, 229]}, 'waste_energy': 8.440133154196523, 'exotic_energy_generated': 2.2934221027976815, 'total_exotic_energy': 2.2934221027976815}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6222687125226655, 'entropy_bits': 0.9564239301673754, 'top_states': [{'state': 1, 'probability': 0.6222687125226655}, {'state': 0, 'probability': 0.37773128747733453}], 'empirical_top_states': [{'state': 1, 'count': 319, 'frequency': 0.623046875}, {'state': 0, 'count': 193, 'frequency': 0.376953125}], 'expected_state_index': 0.6222687125226655, 'measurement_histogram': [193, 319]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6222687125226655, 'entropy_bits': 0.9564239301673754, 'top_states': [{'state': 1, 'probability': 0.6222687125226655}, {'state': 0, 'probability': 0.37773128747733453}], 'empirical_top_states': [{'state': 1, 'count': 319, 'frequency': 0.623046875}, {'state': 0, 'count': 193, 'frequency': 0.376953125}], 'expected_state_index': 0.6222687125226655, 'measurement_histogram': [193, 319]}, 'waste_energy': 6.862073566499474, 'exotic_energy_generated': 1.2413823776663158, 'total_exotic_energy': 3.5348044804639973}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.767402,
  "final_total_exotic_energy": 3.534804
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.115`

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
