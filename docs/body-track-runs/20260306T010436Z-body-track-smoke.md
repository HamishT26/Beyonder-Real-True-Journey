# Body Track Smoke Report

- generated_utc: `2026-03-06T01:04:36+00:00`
- overall_status: **FAIL**

## Summary metrics
- pass_rate: `0.666667`
- total_duration_seconds: `3.518666`
- body_health_score: `66.67`
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
    "ok": false,
    "actual": 0.666667,
    "threshold": 1.0
  },
  "total_duration_seconds": {
    "ok": false,
    "actual": 3.518666,
    "threshold": 1.274
  },
  "body_health_score": {
    "ok": true,
    "actual": 66.67,
    "threshold": 32.83
  }
}
```

## Step summary
| step | status | returncode | duration_seconds | command |
|---|---|---:|---:|---|
| compile_python_modules | PASS | 0 | 0.385 | `C:\Users\hamis\AppData\Local\Programs\Python\Python312\python3.exe -m py_compile freed_id_registry.py qc_transmuter.py trinity_orchestrator.py trinity_orchestrator_full.py trinity_simulation_engine.py run_simulation.py body_track_runner.py` |
| run_full_orchestrator_demo | PASS | 0 | 0.549 | `C:\Users\hamis\AppData\Local\Programs\Python\Python312\python3.exe trinity_orchestrator_full.py` |
| run_gmut_simulation | FAIL | 1 | 2.584 | `C:\Users\hamis\AppData\Local\Programs\Python\Python312\python3.exe run_simulation.py --gammas 0.0 0.02 0.05` |

## compile_python_modules

- returncode: `0`
- duration_seconds: `0.385`

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
- duration_seconds: `0.549`

### stdout (trimmed)
```
Registered DID: did:freed:35c8d53bba604f8980cdaa9a9a4b08ba

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

- returncode: `1`
- duration_seconds: `2.584`

### stdout (trimmed)
```
(empty)
```

### stderr (trimmed)
```
Traceback (most recent call last):
  File "C:\Users\hamis\OneDrive\Documents\GitHub\Beyonder-Real-True-Journey\run_simulation.py", line 43, in <module>
    main()
  File "C:\Users\hamis\OneDrive\Documents\GitHub\Beyonder-Real-True-Journey\run_simulation.py", line 35, in main
    ratio = result.energy_density_ratio()
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\hamis\OneDrive\Documents\GitHub\Beyonder-Real-True-Journey\trinity_simulation_engine.py", line 64, in energy_density_ratio
    baseline_int = np.trapz(self.baseline_spectrum, self.frequencies)
                   ^^^^^^^^
  File "C:\Users\hamis\AppData\Local\Programs\Python\Python312\Lib\site-packages\numpy\__init__.py", line 805, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'trapz'. Did you mean: 'trace'?
```

### extracted_metrics
```json
{
  "gamma_count": 0,
  "analysis_status": "skipped_due_to_failure"
}
```
