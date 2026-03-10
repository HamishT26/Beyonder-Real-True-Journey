# HA Production Fabric Workflow

- pack: `ha_production_fabric`
- pillar: `body`
- gating_class: `active`
- sync_strategy: `local_repo`
- activation_group: `materialization_ladder`
- continuity_band: `v7`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `read_only`

## Workflow Tokens
- ha readiness
- replica requirements
- failover proof
- zero downtime conditions
