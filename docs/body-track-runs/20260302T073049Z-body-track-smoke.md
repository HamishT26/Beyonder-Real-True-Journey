# Body Track Smoke Report

- generated_utc: `2026-03-02T07:30:49+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `1.141515`
- body_health_score: `100.0`
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
    "ok": true,
    "actual": 1.0,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": false,
    "actual": 1.141515,
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
| compile_python_modules | PASS | 0 | 0.084 | `/usr/bin/python3 -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.101 | `/usr/bin/python3 trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 0.957 | `/usr/bin/python3 run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.084`

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
Registered DID: did:freed:80231057bdd44e22a65699a1e8df28ea
Task 1 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8079680283231611, 0.19203197167683891], 'counts': {'0': 418, '1': 94}, 'entropy_nats': 0.4891559664051035, 'entropy_bits': 0.7057028869538913, 'mean_phase_rad': 0.3366950369110482, 'coherence': 1.0924128144055898, 'top_outcomes': [{'index': 0, 'count': 418, 'freq': 0.81640625, 'p': 0.8079680283231611}, {'index': 1, 'count': 94, 'freq': 0.18359375, 'p': 0.19203197167683891}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.8079680283231611, 0.19203197167683891], 'counts': {'0': 418, '1': 94}, 'entropy_nats': 0.4891559664051035, 'entropy_bits': 0.7057028869538913, 'mean_phase_rad': 0.3366950369110482, 'coherence': 1.0924128144055898, 'top_outcomes': [{'index': 0, 'count': 418, 'freq': 0.81640625, 'p': 0.8079680283231611}, {'index': 1, 'count': 94, 'freq': 0.18359375, 'p': 0.19203197167683891}]}}, 'waste_energy': 8.630512022906178, 'exotic_energy_generated': 2.4203413486041176, 'total_exotic_energy': 2.4203413486041176}
Task 2 result: {'result': "classical_output(quantum_features:{'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.6766775050989907, 0.3233224949010093], 'counts': {'0': 331, '1': 181}, 'entropy_nats': 0.6293485413919526, 'entropy_bits': 0.9079580196568726, 'mean_phase_rad': 0.9391904791401279, 'coherence': 1.8753875541298344, 'top_outcomes': [{'index': 0, 'count': 331, 'freq': 0.646484375, 'p': 0.6766775050989907}, {'index': 1, 'count': 181, 'freq': 0.353515625, 'p': 0.3233224949010093}]}})", 'quantum_features': {'inputs': {'num_states': 2, 'shots': 512, 'seed': None, 'top_k': 8}, 'outputs': {'probabilities': [0.6766775050989907, 0.3233224949010093], 'counts': {'0': 331, '1': 181}, 'entropy_nats': 0.6293485413919526, 'entropy_bits': 0.9079580196568726, 'mean_phase_rad': 0.9391904791401279, 'coherence': 1.8753875541298344, 'top_outcomes': [{'index': 0, 'count': 331, 'freq': 0.646484375, 'p': 0.6766775050989907}, {'index': 1, 'count': 181, 'freq': 0.353515625, 'p': 0.3233224949010093}]}}, 'waste_energy': 7.953880839588349, 'exotic_energy_generated': 1.9692538930588985, 'total_exotic_energy': 4.389595241663017}
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 2,
  "avg_exotic_energy_generated": 2.194798,
  "final_total_exotic_energy": 4.389595
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `0.957`

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
