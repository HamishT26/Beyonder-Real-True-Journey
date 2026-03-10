# Docker Pilot Workflow

- pack: `docker_pilot`
- pillar: `body`
- gating_class: `active`
- sync_strategy: `local_probe`
- activation_group: `runtime_orchestration`
- continuity_band: `v6`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `bounded_write`

## Workflow Tokens
- docker probe
- disposable runtime
- cleanup required
- audit log
