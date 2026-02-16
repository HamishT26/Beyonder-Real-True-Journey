---
name: trinity-system-integration
description: Integrate Trinity Hybrid OS components in this repo into a coherent execution path (orchestrator, simulation, identity, ethics) with validation checkpoints.
---

# Trinity System Integration

Use when users ask to connect system components into one practical flow.

## Integration sequence
1. Theory anchors: `gmut_lagrangian.md`, `gmut_predictions.md`.
2. Architecture anchor: `trinity_os_architecture.md`.
3. Runtime path: `trinity_orchestrator.py` / `trinity_orchestrator_full.py`.
4. Simulation path: `trinity_simulation_engine.py` + `run_simulation.py`.
5. Governance path: `freed_id_spec.md` + `Cosmic_bill_of_rights.md` + registry code.

## Deliverable
- A concise runbook with:
  - command sequence,
  - expected outputs,
  - governance checks,
  - known constraints.


## Expanded suite command
```bash
python3 scripts/run_all_trinity_systems.py --list-profiles
python3 scripts/run_all_trinity_systems.py --step-timeout-sec 0
python3 scripts/run_all_trinity_systems.py --profile quick --step-timeout-sec 0
python3 scripts/run_all_trinity_systems.py --profile standard --step-timeout-sec 0
```
Deep profile is now the default execution mode. Use this command for full integration by default, `--profile quick` for rapid cycles, and `--profile standard` for reduced base checks. Use `--list-profiles` for a built-in mode catalog. `--quick-mode` is retained as a legacy alias for `--profile quick`.


Use `--status-json docs/system-suite-status.json` to produce a standalone JSON status artifact for CI/automation consumers.

Add `--fail-on-warn` when WARN outcomes should be treated as overall failure. Suite outputs include per-step started/finished timestamps and duration telemetry.

Add `--achievement-target-steps 10` (or higher) when you want the run to finish only after meeting a minimum completed-step threshold.
