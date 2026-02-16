# Body Track Smoke Report

- generated_utc: `2026-02-16T03:50:33+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.12993`
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
    "actual": 0.12993,
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
| run_full_orchestrator_demo | PASS | 0 | 0.033 | `/usr/bin/python3 trinity_orchestrator_full.py` |
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
- duration_seconds: `0.033`

### stdout (trimmed)
```
Registered DID: did:freed:65591afa2a4e4ea0979bcfc472192f1a
Task 1 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5496982341303931, 'entropy_bits': 0.9928615518093813, 'top_states': [{'state': 1, 'probability': 0.5496982341303931}, {'state': 0, 'probability': 0.45030176586960685}], 'empirical_top_states': [{'state': 1, 'count': 281, 'frequency': 0.548828125}, {'state': 0, 'count': 231, 'frequency': 0.451171875}], 'expected_state_index': 0.5496982341303931, 'measurement_histogram': [231, 281]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 1, 'dominant_probability': 0.5496982341303931, 'entropy_bits': 0.9928615518093813, 'top_states': [{'state': 1, 'probability': 0.5496982341303931}, {'state': 0, 'probability': 0.45030176586960685}], 'empirical_top_states': [{'state': 1, 'count': 281, 'frequency': 0.548828125}, {'state': 0, 'count': 231, 'frequency': 0.451171875}], 'expected_state_index': 0.5496982341303931, 'measurement_histogram': [231, 281]}, 'waste_energy': 7.637185950411522, 'exotic_energy_generated': 1.7581239669410145, 'total_exotic_energy': 1.7581239669410145}
Task 2 result: {'result': "classical_output(quantum_features:{'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8096685131281882, 'entropy_bits': 0.7021643899178551, 'top_states': [{'state': 0, 'probability': 0.8096685131281882}, {'state': 1, 'probability': 0.1903314868718118}], 'empirical_top_states': [{'state': 0, 'count': 415, 'frequency': 0.810546875}, {'state': 1, 'count': 97, 'frequency': 0.189453125}], 'expected_state_index': 0.1903314868718118, 'measurement_histogram': [415, 97]})", 'quantum_features': {'num_states': 2, 'shots': 512, 'dominant_state': 0, 'dominant_probability': 0.8096685131281882, 'entropy_bits': 0.7021643899178551, 'top_states': [{'state': 0, 'probability': 0.8096685131281882}, {'state': 1, 'probability': 0.1903314868718118}], 'empirical_top_states': [{'state': 0, 'count': 415, 'frequency': 0.810546875}, {'state': 1, 'count': 97, 'frequency': 0.189453125}], 'expected_state_index': 0.1903314868718118, 'measurement_histogram': [415, 97]}, 'waste_energy': 7.037587422233197, 'exotic_energy_generated': 1.358391614822131, 'total_exotic_energy': 3.116515581763146}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.558258,
  "final_total_exotic_energy": 3.116516
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
