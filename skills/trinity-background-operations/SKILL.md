---
name: trinity-background-operations
description: Run bounded Trinity Hybrid OS maintenance cycles with lock safety, cache/energy guardrails, and quick recovery checks. Use when you need autonomous or AFK cycle execution and validation.
---

# Trinity Background Operations

Use this skill when operating the background maintenance loop safely.

## Quick run
```bash
python3 scripts/trinity_background_os.py --profile quick --cycles 1 --status docs/trinity-background-os-status.json
```

## Safer bounded run (recommended)
```bash
python3 scripts/trinity_background_os.py \
  --profile quick \
  --cycles 5 \
  --interval-sec 30 \
  --max-runtime-sec 600 \
  --cache-purge \
  --fail-fast \
  --lockfile docs/.trinity-background-os.lock
```

## Lock recovery
If a stale lock is present:
```bash
python3 scripts/trinity_background_os.py --profile quick --cycles 1 --force-lock
```

## Validation checkpoints
After a run, verify critical outputs:
```bash
python3 scripts/validate_cache_waste_report.py --cache docs/cache-waste-regenerator-report.json
python3 scripts/validate_token_energy_reports.py --token docs/token-credit-bank-report.json --energy docs/energy-bank-report.json
```
This validator includes strict projection integrity checks (exact horizon length, coverage reconciliation, non-increasing reserve surplus, and projection-summary aggregate reconciliation plus non-negativity/coverage-bounds checks).

## Projection horizon tuning
When forecasting reserve usage directly, tune projection depth:
```bash
python3 scripts/trinity_energy_bank_system.py --token-report docs/token-credit-bank-report.json --cache-report docs/cache-waste-regenerator-report.json --auto-max-cap --cap-ceiling 100 --projection-sessions 20
```
This report now includes covered/uncovered per-session token/credit fields for shortfall planning.

## Local skill installation
```bash
python3 scripts/trinity_skill_installer_system.py --force --verify
```
Use this to install/refresh repo-local skills into Codex skill storage with a verification report.
