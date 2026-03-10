# Trinity Dashboard Workflow

- pack: `trinity_dashboard`
- pillar: `body`
- gating_class: `active`
- sync_strategy: `local_repo`
- activation_group: `visibility`
- continuity_band: `v6`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `manual`

## Workflow Tokens
- local dashboard
- cached status
- postgres summary
- no live dependency
