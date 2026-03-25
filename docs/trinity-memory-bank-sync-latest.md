# Trinity Memory Bank Sync

- generated_utc: `2026-03-25T12:07:52+00:00`
- overall_status: `PASS`
- archive: `docs/memory-archives/20260325T120735Z-v11-memory-bank.zip`
- archive_mb: `0.15`
- free_gib: `6.55`

## Surfaces
- `repo`: status=`authoritative`, reachable=`True`, proof_state=`repo_first_authority`, blockers=`none`
- `github`: status=`live_mirror`, reachable=`True`, proof_state=`remote_reachable`, blockers=`none`
- `postgres`: status=`live_query_store`, reachable=`True`, proof_state=`postgres_ready`, blockers=`none`
- `docker`: status=`live_runtime_storage`, reachable=`True`, proof_state=`docker_ready`, blockers=`none`
- `notion`: status=`bounded_mirror`, reachable=`True`, proof_state=`bounded_mirror_only`, blockers=`none`
- `linear`: status=`bounded_action_mirror`, reachable=`True`, proof_state=`bounded_action_only`, blockers=`none`
- `new_project_workbench`: status=`local_read_surface`, reachable=`True`, proof_state=`workbench_read_only`, blockers=`none`
- `google_drive`: status=`staged_with_blockers`, reachable=`False`, proof_state=`operator_hold`, blockers=`google drive activation deferred by operator`

## Notes
- Repo remains the authority source.
- GitHub is the current off-device path that is verifiably reachable today.
- Google Drive stays archive-only and never overrides repo authority.
- Docker/Postgres remain bounded runtime mirrors, not remote archive truth.
