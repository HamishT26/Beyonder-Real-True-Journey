# UAT Pre-Prod Fabric Workflow

- pack: `uat_preprod_fabric`
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
- uat mirror
- latency budget
- full-shape test data
- rollback proof
