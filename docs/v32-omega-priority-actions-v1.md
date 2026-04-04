# V32 Omega Priority Actions

Status: advisory, non-authoritative follow-through from the published V31 state.

## Priority Order

1. Repair or formally retire the degraded OneDrive repo copy.
   Rationale: V31 proved the stable local clone is healthy, but the OneDrive-hosted repo still fails as a real worktree. V32 should either rehydrate it into a readable git worktree or explicitly demote it to mirror-only status.
   Touch next: `scripts/trinity_v31_onedrive_hydration_probe.py`, `docs/trinity-live-traces/v31-onedrive-repo-hydration-proof-v1.json`, `docs/trinity-live-traces/v31-onedrive-mirror-sync-proof-v1.json`.

2. Unblock Gmail materialization with a scope-first auth repair.
   Rationale: the blocker is no longer abstract. The current refresh token is missing usable Gmail scope, so the next useful step is auth repair, not more probing.
   Touch next: `scripts/trinity_v31_gmail_api_probe.py`, `docs/trinity-live-traces/v31-gmail-materialization-proof-v1.json`.

3. Convert the Hugging Face execution proof into a reusable guarded lane.
   Rationale: V31 moved Hugging Face from blocked to `live_execution_proven`. V32 should preserve that gain with a reusable low-cost probe and a simple spend guard so execution stays honest and repeatable.
   Touch next: `docs/trinity-live-traces/v31-huggingface-execution-proof-v1.json`, `docs/trinity-mcp-cache/connector-materialization-latest.json`.

4. Promote the session-end archive and prune flow into a repeatable closeout routine.
   Rationale: the archive plus retention pass reclaimed space and cleared the memory-bank watch-band issue. That should become the standard end-of-session path rather than a manual recovery step.
   Touch next: `scripts/trinity_zip_memory_converter.py`, `scripts/trinity_storage_retention.py`, `docs/trinity-storage-prune-latest.json`.

5. Add verification to the OneDrive non-authoritative mirror lane.
   Rationale: the mirror sync now works, but V32 should add stronger verification around counts, hashes, and allowed families before any broader migration.
   Touch next: `scripts/trinity_google_drive_working_mirror_probe.py`, `docs/trinity-live-traces/v31-onedrive-mirror-sync-proof-v1.json`.

6. Investigate the WSL git timeout separately from repo truth.
   Rationale: V31 recovered suite health with the Windows-git bridge, but the WSL timeout is still technical debt. It should be fixed as an environment issue, not folded into repo authority claims.
   Touch next: `docs/trinity-live-traces/v31-onedrive-repo-hydration-proof-v1.json`, `docs/trinity-runtime-model-resolution-v1.json`.

7. Keep V32 expansions curated and directly tied to operator quality.
   Rationale: the highest-value additions now are not bulk installs. They are small deterministic helpers for storage hygiene, auth health, mirror verification, and execution cost control.
   Touch next: `docs/v32-beta-continuity-pack-v1.md`, `docs/auto-generated/v31-ghc-contributions-digest.md`.
