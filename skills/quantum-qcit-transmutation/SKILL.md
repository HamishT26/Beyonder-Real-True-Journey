---
name: quantum-qcit-transmutation
description: Run QCIT coordination and quantum energy transmutation engines, then verify generated reports for integration into Trinity suite workflows.
---

# Quantum QCIT Transmutation

Use when users request QCIT/quantum transmutation execution, validation, or integration into orchestration flows.

## Workflow
1. Run QCIT coordination engine:
   - `python3 scripts/qcit_coordination_engine.py --out docs/qcit-coordination-report.json`
2. Run quantum energy transmutation engine:
   - `python3 scripts/quantum_energy_transmutation_engine.py --out docs/quantum-energy-transmutation-report.json`
3. Validate report structure and numeric guardrails:
   - `python3 scripts/validate_transmutation_reports.py --qcit docs/qcit-coordination-report.json --quantum docs/quantum-energy-transmutation-report.json`
4. If running integrated suite, use:
   - `python3 scripts/run_all_trinity_systems.py --profile deep --step-timeout-sec 0`

## Expected outputs
- `docs/qcit-coordination-report.json`
- `docs/quantum-energy-transmutation-report.json`
