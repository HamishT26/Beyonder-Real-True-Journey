# Persistent Dev Fabric Workflow

- pack: `persistent_dev_fabric`
- pillar: `body`
- gating_class: `active`
- sync_strategy: `local_repo`
- activation_group: `materialization_ladder`
- continuity_band: `v7`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `bounded_write`

## Workflow Tokens
- persistent dev only
- no main writes
- dedicated scopes
- rollback ready
