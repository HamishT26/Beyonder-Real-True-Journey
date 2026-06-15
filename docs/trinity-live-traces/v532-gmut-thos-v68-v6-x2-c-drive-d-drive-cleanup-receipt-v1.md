# v532 GMUT/THOS v68 v6 x2 C/D Cleanup Receipt v1

Generated local: 2026-06-15T17:32:19.2905661+12:00

## Result

- C free before: 12.634 GB.
- C free after: 21.539 GB.
- C reclaimed: 8.905 GB.
- D free after: 614.396 GB.
- Goal status: PASS, the 8 GB target was exceeded.

## Completed Actions

- Created D-side cleanup, archive, workspace, and tool-cache structure.
- Moved npm cache routing from C to D and verified the new D cache.
- Removed the old C npm cache after confirming it was no longer active.
- Backed up and removed exact stale Codex .tmp backup/staging candidates.
- Backed up and removed exact user temp diagnostics, installer, and old GHC scratch candidates where verification passed.
- Backed up the old C workspace to D and retired all unlocked archived source material.
- Changed Codex force-push default to false.
- Hardened PowerShell Codex Desktop routing toward the D v58 omega worktree.

## Preserved By Design

- Codex sessions and continuity stores.
- Codex plugin cache, user skills, credentials, auth files, and active app state.
- Active npm global packages and command shims.
- Active Codex temp PATH helper.
- Raw session, lane, screenshot, credential, and private log content.

## Open Residue / Blockers

- Old C workspace has a tiny active .local-runtime residue left because one log file was in use; remaining size is 0.607 MB.
- Several zero-byte protected temp folders were skipped because Windows denied access or they were in use.
- codex doctor was not used as a final gate because it timed out during planning; command health checks passed through direct version/cache probes.

## Health Checks

- Codex CLI: codex-cli 0.139.0
- npm: 11.15.0
- node: v24.15.0
- npm cache: D-drive cache path verified.
- PowerShell profile parse: PASS.
- Codex config TOML parse: PASS.

All cleanup was bounded to the approved packets. No broad staging, reset, rebase, force-push, plugin-cache mutation, user-skill mutation, account mutation, or raw material publication was performed.
