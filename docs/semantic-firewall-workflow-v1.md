# Semantic Firewall Workflow

- pack: `semantic_firewall`
- pillar: `heart`
- gating_class: `active`
- sync_strategy: `local_repo`
- activation_group: `safety`
- continuity_band: `v6`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `guarded`

## Workflow Tokens
- risk score
- dangerous command classification
- dry run first
- ask before high risk
