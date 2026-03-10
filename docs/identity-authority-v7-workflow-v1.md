# Identity Authority V7 Workflow

- pack: `identity_authority_v7`
- pillar: `heart`
- gating_class: `active`
- sync_strategy: `identity_registry`
- activation_group: `authority_memory`
- continuity_band: `v6-v7`

## Guardrails
- offline-safe by default
- proof before promotion
- no secrets in repo
- autonomy_class: `manual`

## Workflow Tokens
- repo authority
- mirror scope
- connector scope
- human override explicit
