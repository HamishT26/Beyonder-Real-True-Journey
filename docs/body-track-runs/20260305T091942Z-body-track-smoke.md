# Body Track Smoke Report

- generated_utc: `2026-03-05T09:19:42+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.345559`
- body_health_score: `100.0`
- speed_band: `fast`

## Benchmark guardrail
- status: **PASS**
- profile: `standard`
- trend: `stable`
```json
{
  "min_pass_rate": 1.0,
  "max_duration_sec": 1.274,
  "min_health_score": 32.83
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
    "actual": 0.345559,
    "threshold": 1.274
  },
  "body_health_score": {
    "ok": true,
    "actual": 100.0,
    "threshold": 32.83
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.074 | `/usr/bin/python3 -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.089 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.182 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.074`

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
- duration_seconds: `0.089`

### stdout (trimmed)
```
Registered DID: did:freed:8ac5889c958640e495aa12c3e246b5cb
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.9815363052728159, 0.01846369472718418], 'counts': {'0': 508, '1': 4}, 'entropy_nats': 0.09199830811793516, 'entropy_bits': 0.13272550289191992, 'mean_phase_rad': 0.49548602509394496, 'coherence': 1.26718970549816, 'top_outcomes': [{'index': 0, 'count': 508, 'freq': 0.9921875, 'p': 0.9815363052728159}, {'index': 1, 'count': 4, 'freq': 0.0078125, 'p': 0.01846369472718418}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.9815363052728159, 0.01846369472718418], 'counts': {'0': 508, '1': 4}, 'entropy_nats': 0.09199830811793516, 'entropy_bits': 0.13272550289191992, 'mean_phase_rad': 0.49548602509394496, 'coherence': 1.26718970549816, 'top_outcomes': [{'index': 0, 'count': 508, 'freq': 0.9921875, 'p': 0.9815363052728159}, {'index': 1, 'count': 4, 'freq': 0.0078125, 'p': 0.01846369472718418}]}}, 'waste_energy': 8.94714518938123, 'exotic_energy_generated': 2.6314301262541533, 'total_exotic_energy': 2.6314301262541533}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.15999895729118127, 0.8400010427088188], 'counts': {'0': 101, '1': 411}, 'entropy_nats': 0.4396681503482592, 'entropy_bits': 0.6343070601442568, 'mean_phase_rad': 0.7648519405570008, 'coherence': 1.6710085378185064, 'top_outcomes': [{'index': 1, 'count': 411, 'freq': 0.802734375, 'p': 0.8400010427088188}, {'index': 0, 'count': 101, 'freq': 0.197265625, 'p': 0.15999895729118127}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.15999895729118127, 0.8400010427088188], 'counts': {'0': 101, '1': 411}, 'entropy_nats': 0.4396681503482592, 'entropy_bits': 0.6343070601442568, 'mean_phase_rad': 0.7648519405570008, 'coherence': 1.6710085378185064, 'top_outcomes': [{'index': 1, 'count': 411, 'freq': 0.802734375, 'p': 0.8400010427088188}, {'index': 0, 'count': 101, 'freq': 0.197265625, 'p': 0.15999895729118127}]}}, 'waste_energy': 7.269140177520018, 'exotic_energy_generated': 1.5127601183466786, 'total_exotic_energy': 4.144190244600832}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.072095,
  "final_total_exotic_energy": 4.14419
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.182`

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
