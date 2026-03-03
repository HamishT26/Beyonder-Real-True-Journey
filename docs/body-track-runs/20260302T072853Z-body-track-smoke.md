# Body Track Smoke Report

- generated_utc: `2026-03-02T07:28:53+00:00`
- overall_status: **FAIL**

## Summary metrics
- pass_rate: `0.666667`
- total_duration_seconds: `1.24138`
- body_health_score: `66.67`
- speed_band: `steady`

## Benchmark guardrail
- status: **WARN**
- profile: `standard`
- trend: `stable`
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
    "actual": 1.24138,
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
| compile_python_modules | FAIL | 1 | 0.070 | `/usr/bin/python3 -m py_compile Freed_id_registry.py freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.147 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 1.025 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `1`
- duration_seconds: `0.070`

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
- duration_seconds: `0.147`

### stdout (trimmed)
```
Registered DID: did:freed:dc6476b34a194ce0936073d12af196c4
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8020646129567752, 0.19793538704322483], 'counts': {'0': 404, '1': 108}, 'entropy_nats': 0.4975269069589612, 'entropy_bits': 0.717779601378518, 'mean_phase_rad': 1.0235027871145186, 'coherence': 1.7881403397954976, 'top_outcomes': [{'index': 0, 'count': 404, 'freq': 0.7890625, 'p': 0.8020646129567752}, {'index': 1, 'count': 108, 'freq': 0.2109375, 'p': 0.19793538704322483}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8020646129567752, 0.19793538704322483], 'counts': {'0': 404, '1': 108}, 'entropy_nats': 0.4975269069589612, 'entropy_bits': 0.717779601378518, 'mean_phase_rad': 1.0235027871145186, 'coherence': 1.7881403397954976, 'top_outcomes': [{'index': 0, 'count': 404, 'freq': 0.7890625, 'p': 0.8020646129567752}, {'index': 1, 'count': 108, 'freq': 0.2109375, 'p': 0.19793538704322483}]}}, 'waste_energy': 7.633671038359415, 'exotic_energy_generated': 1.7557806922396095, 'total_exotic_energy': 1.7557806922396095}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.28254498899243813, 0.7174550110075619], 'counts': {'0': 154, '1': 358}, 'entropy_nats': 0.5953409275093815, 'entropy_bits': 0.8588954037560206, 'mean_phase_rad': 0.8939836771377931, 'coherence': 1.870822757649726, 'top_outcomes': [{'index': 1, 'count': 358, 'freq': 0.69921875, 'p': 0.7174550110075619}, {'index': 0, 'count': 154, 'freq': 0.30078125, 'p': 0.28254498899243813}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.28254498899243813, 0.7174550110075619], 'counts': {'0': 154, '1': 358}, 'entropy_nats': 0.5953409275093815, 'entropy_bits': 0.8588954037560206, 'mean_phase_rad': 0.8939836771377931, 'coherence': 1.870822757649726, 'top_outcomes': [{'index': 1, 'count': 358, 'freq': 0.69921875, 'p': 0.7174550110075619}, {'index': 0, 'count': 154, 'freq': 0.30078125, 'p': 0.28254498899243813}]}}, 'waste_energy': 6.570615758418057, 'exotic_energy_generated': 1.047077172278705, 'total_exotic_energy': 2.802857864518314}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.401429,
  "final_total_exotic_energy": 2.802858
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `1.025`

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
