# Body Track Smoke Report

- generated_utc: `2026-03-06T01:12:25+00:00`
- overall_status: **PASS**

## Summary metrics
- pass_rate: `1.0`
- total_duration_seconds: `7.41675`
- body_health_score: `100.0`
- speed_band: `heavy`

## Benchmark guardrail
- status: **WARN**
- profile: `standard`
- trend: `regression`
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
    "ok": false,
    "actual": 7.41675,
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
| compile_python_modules | PASS | 0 | 0.600 | `C:\Users\hamis\AppData\Local\Programs\Python\Python312\python.exe -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 1.309 | `C:\Users\hamis\AppData\Local\Programs\Python\Python312\python.exe trinity_orchestrator_full.py` |
| run_gmut_simulation | PASS | 0 | 5.508 | `C:\Users\hamis\AppData\Local\Programs\Python\Python312\python.exe run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.600`

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
- duration_seconds: `1.309`

### stdout (trimmed)
```
Registered DID: did:freed:907a4f8b357a453ab0f1a3b31693f108

Task 'Harmonize energy flows' ARC Score: 0.9090
Task 'Harmonize energy flows' completed.

Task 'Corrupt data logs' ARC Score: 0.8609
Task 'Corrupt data logs' completed.

Task 'Simulate consciousness expansion' ARC Score: 0.8730
Task 'Simulate consciousness expansion' completed.

Task 'Generate chaotic noise' ARC Score: 0.8797
Task 'Generate chaotic noise' completed.

--- Top 3 Memories from Psi-Index Core ---
Memory Core is empty.
```

### stderr (trimmed)
```
(empty)
```

### extracted_metrics
```json
{
  "task_count": 0
}
```

## run_gmut_simulation

- returncode: `0`
- duration_seconds: `5.508`

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
