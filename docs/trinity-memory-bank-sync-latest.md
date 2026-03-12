# Trinity Memory Bank Sync

- generated_utc: `2026-03-12T12:42:19+00:00`
- overall_status: `PASS`
- archive: `docs/memory-archives/20260312T124125Z-v11-memory-bank.zip`
- archive_mb: `0.1`
- free_gib: `0.38`

## Surfaces
- `repo`: status=`authoritative`, reachable=`True`, proof_state=`repo_first_authority`, blockers=`none`
- `github`: status=`live_mirror`, reachable=`True`, proof_state=`remote_reachable`, blockers=`none`
- `postgres`: status=`blocked`, reachable=`False`, proof_state=`postgres_blocked`, blockers=`postgres container not ready`
- `docker`: status=`blocked`, reachable=`False`, proof_state=`docker_unavailable`, blockers=`docker CLI unavailable`
- `notion`: status=`bounded_mirror`, reachable=`True`, proof_state=`bounded_mirror_only`, blockers=`none`
- `linear`: status=`bounded_action_mirror`, reachable=`True`, proof_state=`bounded_action_only`, blockers=`none`
- `new_project_workbench`: status=`local_read_surface`, reachable=`True`, proof_state=`workbench_read_only`, blockers=`none`
- `google_drive`: status=`staged_with_blockers`, reachable=`False`, proof_state=`drive_not_connected`, blockers=`google drive auth not configured`

## Notes
- Repo remains the authority source.
- GitHub is the current off-device path that is verifiably reachable today.
- Google Drive stays archive-only and never overrides repo authority.
- Docker/Postgres remain bounded runtime mirrors, not remote archive truth.
