# Council Sync Governor V10 Workflow

- pack: `council_sync_governor_v10`
- track: `connector_ops`
- council_scope: `council_shared`
- authority_scope: `live_sync_scope`
- mirror_target: `repo_then_live_mirrors`

- repo-first authority
- proof before promotion
- no direct writes to main
- New project workbench may read and trigger, but not bypass authority
