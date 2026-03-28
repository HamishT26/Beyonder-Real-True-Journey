# Trinity Memory Bank Sync

- generated_utc: `2026-03-28T15:45:59+00:00`
- overall_status: `PASS`
- archive: `docs/memory-archives/20260328T154544Z-v27-omega-memory-bank.zip`
- archive_mb: `0.13`
- free_gib: `7.64`

## Surfaces
- `repo`: status=`authoritative`, reachable=`True`, proof_state=`repo_first_authority`, blockers=`none`
- `github`: status=`live_mirror`, reachable=`True`, proof_state=`remote_reachable`, blockers=`none`
- `postgres`: status=`blocked`, reachable=`False`, proof_state=`postgres_blocked`, blockers=`postgres container not ready`
- `docker`: status=`blocked`, reachable=`False`, proof_state=`docker_unavailable`, blockers=`docker CLI unavailable`
- `notion`: status=`bounded_mirror`, reachable=`True`, proof_state=`bounded_mirror_only`, blockers=`none`
- `linear`: status=`bounded_action_mirror`, reachable=`True`, proof_state=`bounded_action_only`, blockers=`none`
- `new_project_workbench`: status=`local_read_surface`, reachable=`True`, proof_state=`workbench_read_only`, blockers=`none`
- `google_drive`: status=`bounded_working_mirror`, reachable=`True`, proof_state=`working_mirror_verified`, blockers=`none`

## Notes
- Repo remains the authority source.
- GitHub is the current off-device path that is verifiably reachable today.
- Google Drive may act as a bounded working mirror for non-authoritative artifacts, but it never overrides repo authority.
- Docker/Postgres remain bounded runtime mirrors, not remote archive truth.
