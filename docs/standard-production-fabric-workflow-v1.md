# Standard Production Fabric Workflow

- pack: `standard_production_fabric`
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
- prod contracts
- protected target
- change window
- rollback mandatory
