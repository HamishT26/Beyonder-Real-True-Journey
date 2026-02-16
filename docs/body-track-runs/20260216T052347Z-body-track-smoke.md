# Body Track Smoke Report

- generated_utc: `2026-02-16T05:23:47+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.189436`
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
    "actual": 0.189436,
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
| run_gmut_simulation | PASS | 0 | 0.123 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.01 0.05` |

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
Registered DID: did:freed:d6411b9cb86748b9b0f2ffb21da298fe
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5455643807990523, 'entropy_bits': 0.9940012859030526, 'top_states': [{'state': 1, 'probability': 0.5455643807990523}, {'state': 0, 'probability': 0.45443561920094766}], 'empirical_top_states': [{'state': 1, 'count': 279, 'frequency': 0.544921875}, {'state': 0, 'count': 233, 'frequency': 0.455078125}], 'expected_state_index': 0.5455643807990523, 'measurement_histogram': [233, 279]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5455643807990523, 'entropy_bits': 0.9940012859030526, 'top_states': [{'state': 1, 'probability': 0.5455643807990523}, {'state': 0, 'probability': 0.45443561920094766}], 'empirical_top_states': [{'state': 1, 'count': 279, 'frequency': 0.544921875}, {'state': 0, 'count': 233, 'frequency': 0.455078125}], 'expected_state_index': 0.5455643807990523, 'measurement_histogram': [233, 279]}, 'waste_energy': 8.103905280084085, 'exotic_energy_generated': 2.0692701867227226, 'total_exotic_energy': 2.0692701867227226}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6618487194443866, 'entropy_bits': 0.923038611206773, 'top_states': [{'state': 1, 'probability': 0.6618487194443866}, {'state': 0, 'probability': 0.3381512805556134}], 'empirical_top_states': [{'state': 1, 'count': 339, 'frequency': 0.662109375}, {'state': 0, 'count': 173, 'frequency': 0.337890625}], 'expected_state_index': 0.6618487194443866, 'measurement_histogram': [173, 339]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.6618487194443866, 'entropy_bits': 0.923038611206773, 'top_states': [{'state': 1, 'probability': 0.6618487194443866}, {'state': 0, 'probability': 0.3381512805556134}], 'empirical_top_states': [{'state': 1, 'count': 339, 'frequency': 0.662109375}, {'state': 0, 'count': 173, 'frequency': 0.337890625}], 'expected_state_index': 0.6618487194443866, 'measurement_histogram': [173, 339]}, 'waste_energy': 7.60206527471542, 'exotic_energy_generated': 1.7347101831436134, 'total_exotic_energy': 3.803980369866336}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.90199,
  "final_total_exotic_energy": 3.80398
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.123`

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
