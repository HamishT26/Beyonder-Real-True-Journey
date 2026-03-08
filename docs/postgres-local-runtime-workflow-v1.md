# Postgres Local Runtime Workflow

- pack: `postgres_local_runtime`
- pillar: `body`
- gating_class: `verified_live_write`
- sync_strategy: `local_probe`

## Guardrails
- offline-safe by default
- proof before promotion
- cache-backed continuity
- no secrets in repo
