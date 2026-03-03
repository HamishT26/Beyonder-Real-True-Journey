# Body Track Smoke Report

- generated_utc: `2026-03-02T07:02:10+00:00`
- overall_status: **FAIL**

## Summary metrics
- pass_rate: `0.666667`
- total_duration_seconds: `1.157871`
- body_health_score: `66.67`
- speed_band: `steady`

## Benchmark guardrail
- status: **WARN**
- profile: `standard`
- trend: `improvement`
```json
{
  "min_pass_rate": 1.0,
  "max_duration_sec": 1.0,
  "min_health_score": 95.0
}
```

### check_results
```json
{
  "pass_rate": {
    "ok": false,
    "actual": 0.666667,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": false,
    "actual": 1.157871,
    "threshold": 1.0
  },
  "body_health_score": {
    "ok": false,
    "actual": 66.67,
    "threshold": 95.0
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | FAIL | 1 | 0.064 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.115 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.979 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `1`
- duration_seconds: `0.064`

### stdout (trimmed)
```
(empty)
```

### stderr (trimmed)
```
[Errno 2] No such file or directory: 'Freed_id_registry.py'
```

## run_full_orchestrator_demo

- returncode: `0`
- duration_seconds: `0.115`

### stdout (trimmed)
```
Registered DID: did:freed:7f88820849bb49b39ba2f1be79a9d23b
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.2381652584538429, 0.761834741546157], 'counts': {'0': 116, '1': 396}, 'entropy_nats': 0.548955815209237, 'entropy_bits': 0.7919758322695244, 'mean_phase_rad': 0.8515812234560187, 'coherence': 1.6760464296590547, 'top_outcomes': [{'index': 1, 'count': 396, 'freq': 0.7734375, 'p': 0.761834741546157}, {'index': 0, 'count': 116, 'freq': 0.2265625, 'p': 0.2381652584538429}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.2381652584538429, 0.761834741546157], 'counts': {'0': 116, '1': 396}, 'entropy_nats': 0.548955815209237, 'entropy_bits': 0.7919758322695244, 'mean_phase_rad': 0.8515812234560187, 'coherence': 1.6760464296590547, 'top_outcomes': [{'index': 1, 'count': 396, 'freq': 0.7734375, 'p': 0.761834741546157}, {'index': 0, 'count': 116, 'freq': 0.2265625, 'p': 0.2381652584538429}]}}, 'waste_energy': 8.842018532680246, 'exotic_energy_generated': 2.5613456884534975, 'total_exotic_energy': 2.5613456884534975}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.49847641237672347, 0.5015235876232766], 'counts': {'0': 253, '1': 259}, 'entropy_nats': 0.6931425379142689, 'entropy_bits': 0.9999933020781061, 'mean_phase_rad': 0.6663908120085978, 'coherence': 1.2711515304787309, 'top_outcomes': [{'index': 1, 'count': 259, 'freq': 0.505859375, 'p': 0.5015235876232766}, {'index': 0, 'count': 253, 'freq': 0.494140625, 'p': 0.49847641237672347}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.49847641237672347, 0.5015235876232766], 'counts': {'0': 253, '1': 259}, 'entropy_nats': 0.6931425379142689, 'entropy_bits': 0.9999933020781061, 'mean_phase_rad': 0.6663908120085978, 'coherence': 1.2711515304787309, 'top_outcomes': [{'index': 1, 'count': 259, 'freq': 0.505859375, 'p': 0.5015235876232766}, {'index': 0, 'count': 253, 'freq': 0.494140625, 'p': 0.49847641237672347}]}}, 'waste_energy': 7.586616983287371, 'exotic_energy_generated': 1.7244113221915802, 'total_exotic_energy': 4.285757010645078}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.142879,
  "final_total_exotic_energy": 4.285757
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.979`

### stdout (trimmed)
```
Gamma=0.0000: energy density ratio = 1.00000
Gamma=0.0200: energy density ratio = 1.01986
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
    "0.0200": 1.01986,
    "0.0500": 1.04964
  },
  "ratio_min": 1.0,
  "ratio_max": 1.04964,
  "ratio_span": 0.04964
}
```
