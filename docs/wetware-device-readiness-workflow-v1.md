# Wetware Device Readiness Workflow

- pack: `wetware_device_readiness`
- pillar: `heart`
- gating_class: `active`
- sync_strategy: `local_repo`

## Guardrails
- device-ready only
- no live biometric ingestion
- explicit consent boundary
- non-clinical advisory only

## Operating notes
- offline-safe by default
- cache-backed artifacts remain the source of suite continuity
- promotion requires proof artifacts, not narrative intent
- disposable staging targets only for any live write path
