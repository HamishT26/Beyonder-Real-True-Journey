# v505-v515 Drive Cleanup, Codex Update, and Live Adapter Preflight v1

Generated: 2026-06-11 NZ evening

Status: PREPARED_FOR_APPROVAL

## Purpose

This preflight records the safe facts gathered before resuming the v505-v515 GMUT/THOS phase run. It is intentionally status-only. It does not delete, move, rename, archive, publish raw session material, mutate plugin cache, mutate user skills, or touch external accounts.

## Current Local State

- C drive: 108.91 GB used, 8.06 GB free, 116.97 GB total after the Codex CLI update.
- D drive: 275.01 GB used, 656.47 GB free, 931.48 GB total.
- Current shell working folder: C workspace label, user OneDrive project folder. Exact local path is intentionally not published.
- Canonical active repo inspected: D omega workspace label, v58 omega worktree. Exact local path is intentionally not published.
- Active repo branch: `codex/GHC-Family/v58-omega-exec`.
- Latest verified local omega commit before this preflight: `8ea93dd6cecb72c3c4f783d14e3e83a19c99e411`.
- Codex CLI before update: `codex-cli 0.138.0`.
- Codex CLI after update: `codex-cli 0.139.0`.
- npm stale temp folder matching the approved `.codex-*` pattern under the user npm `@openai` global package directory was present before the update and was no longer present after `npm install -g @openai/codex@0.139.0`.
- Active npm Codex package after update: about 278.93 MB.

## C Drive Pressure Findings

- User Codex home: about 5.846 GB.
- Codex session store: about 4.132 GB.
- Codex temporary staging folder: about 0.595 GB.
- Codex plugin cache: about 0.471 GB.
- User local temp folder: about 1.134 GB.
- User videos folder: about 3.001 GB.
- User downloads folder: about 0.300 GB.
- User npm roaming folder: about 0.981 GB before update, with active Codex package and stale temp package identified.
- Current C workspace folder: effectively 0 GB by recursive file scan, so the current C workspace folder itself is not the main pressure source.

## Source Refresh

- Official Codex app changelog: [OpenAI Developers Codex changelog](https://developers.openai.com/codex/changelog/)
- Official Codex CLI releases: [openai/codex releases](https://github.com/openai/codex/releases)

Observed official release themes relevant to this run:

- Codex CLI 0.139.0 adds direct standalone web search from code mode, including nested JavaScript tool calls.
- Codex CLI 0.139.0 improves preservation of `oneOf` and `allOf` in richer tool and connector schemas.
- Codex CLI 0.139.0 expands `codex doctor` with local editor and pager environment details while redacting raw values in JSON output.
- Codex CLI 0.139.0 improves plugin marketplace JSON source reporting and cached catalog behavior.
- Codex CLI 0.139.0 fixes session resume/fork prompt parsing, thread reset configuration reload behavior, MCP startup warning routing, image edit path handling, TUI spinner behavior, and related stability issues.
- Codex app 26.608 adds Migrate to Codex flows, improves plugin marketplace/category UX, expands settings search, and includes bug fixes for active-goal UI and rendering behavior.

## Safety Boundary

The highest-yield cleanup area is `.codex\sessions`, but it is also the highest-risk area because it contains continuity-bearing session history. The safe path is:

1. Create a D-drive mirror or compressed cold archive first.
2. Verify hashes and counts.
3. Keep current live session material in place.
4. Only then consider scoped deletion or junction/symlink routing under a separately approved exact packet.

The second safest cleanup area is `.codex\.tmp`, but it contains plugin backups and current marketplace/plugin sync material. The safe path is:

1. Identify stale folders by age and active-lock state.
2. Back up candidate folders to D.
3. Delete only exact stale folders that are not active locks, current plugin sync folders, plugin cache, user skills, sessions, secrets, logs, or active app state.

## Recommended Next Step

Use the companion approval packet tapestry:

- `v505-v515-round-robin-live-adapter-20-approval-packets-v1.md`

Then run cleanup and transfer work in this order:

1. Read-only inventory.
2. Backup/mirror to D.
3. Hash verification.
4. Exact stale cleanup.
5. Codex readiness recheck.
6. Resume v505 v6 x2.
7. Prepare v506-v507.
8. Begin v508 live-adapter round robin only after UI/control packets are approved.
