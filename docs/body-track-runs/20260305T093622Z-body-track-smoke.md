# Body Track Smoke Report

- generated_utc: `2026-03-05T09:36:22+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `0.376627`
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
    "actual": 0.376627,
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
| compile_python_modules | PASS | 0 | 0.081 | `/usr/bin/python3 -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.101 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.195 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.081`

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
- duration_seconds: `0.101`

### stdout (trimmed)
```
Registered DID: did:freed:8a27361ed3b5474aa9528dd4e49789f3
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.6587182627581782, 0.34128173724182165], 'counts': {'0': 332, '1': 180}, 'entropy_nats': 0.6418819884656233, 'entropy_bits': 0.9260399615953016, 'mean_phase_rad': 0.5477832093666504, 'coherence': 1.795996161700323, 'top_outcomes': [{'index': 0, 'count': 332, 'freq': 0.6484375, 'p': 0.6587182627581782}, {'index': 1, 'count': 180, 'freq': 0.3515625, 'p': 0.34128173724182165}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.6587182627581782, 0.34128173724182165], 'counts': {'0': 332, '1': 180}, 'entropy_nats': 0.6418819884656233, 'entropy_bits': 0.9260399615953016, 'mean_phase_rad': 0.5477832093666504, 'coherence': 1.795996161700323, 'top_outcomes': [{'index': 0, 'count': 332, 'freq': 0.6484375, 'p': 0.6587182627581782}, {'index': 1, 'count': 180, 'freq': 0.3515625, 'p': 0.34128173724182165}]}}, 'waste_energy': 8.030888785421418, 'exotic_energy_generated': 2.0205925236142788, 'total_exotic_energy': 2.0205925236142788}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.5321685991447995, 0.4678314008552005], 'counts': {'0': 279, '1': 233}, 'entropy_nats': 0.6910761128489379, 'entropy_bits': 0.9970120808839844, 'mean_phase_rad': 1.0807817862577256, 'coherence': 1.7100421205742653, 'top_outcomes': [{'index': 0, 'count': 279, 'freq': 0.544921875, 'p': 0.5321685991447995}, {'index': 1, 'count': 233, 'freq': 0.455078125, 'p': 0.4678314008552005}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.5321685991447995, 0.4678314008552005], 'counts': {'0': 279, '1': 233}, 'entropy_nats': 0.6910761128489379, 'entropy_bits': 0.9970120808839844, 'mean_phase_rad': 1.0807817862577256, 'coherence': 1.7100421205742653, 'top_outcomes': [{'index': 0, 'count': 279, 'freq': 0.544921875, 'p': 0.5321685991447995}, {'index': 1, 'count': 233, 'freq': 0.455078125, 'p': 0.4678314008552005}]}}, 'waste_energy': 6.403108688168205, 'exotic_energy_generated': 0.9354057921121366, 'total_exotic_energy': 2.9559983157264154}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 1.477999,
  "final_total_exotic_energy": 2.955998
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.195`

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
