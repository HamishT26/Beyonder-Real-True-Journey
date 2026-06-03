# V477 THOS V3 X1 Roadmap

- generated_nz: `2026-06-04T04:25:51+12:00`
- overall_status: `READY_FOR_V477_THOS_V3_X1`
- task_count: `60`

## Tasks

- v477-v3-task-01 [app_lane_notifier]: Run one probe-only pass before each new advisory turn.
- v477-v3-task-02 [app_lane_notifier]: Use targeted retries rather than duplicate all-lane starts after a timeout.
- v477-v3-task-03 [app_lane_notifier]: Record completion by lane, operation, attempt count, and bounded wait window.
- v477-v3-task-04 [app_lane_notifier]: Keep unfiltered app-server events out of curated artifacts.
- v477-v3-task-05 [app_lane_notifier]: Add stale-active-turn wording to every app-lane handoff.
- v477-v3-task-06 [app_lane_notifier]: Prefer existing callable lanes and record blocker if only spawn tools are exposed.
- v477-v3-task-07 [cli_lane_watchers]: Refresh Arby and Aster read-only launcher health before heavy THOS delegation.
- v477-v3-task-08 [cli_lane_watchers]: Keep CLI lanes non-ephemeral and advisory-only.
- v477-v3-task-09 [cli_lane_watchers]: Record runtime duration, exit state, and sanitized blocker class.
- v477-v3-task-10 [cli_lane_watchers]: Separate CLI sandbox readiness from app-lane notifier readiness.
- v477-v3-task-11 [cli_lane_watchers]: Use watcher receipts so completed CLI reports do not require manual supervision.
- v477-v3-task-12 [cli_lane_watchers]: Avoid mutating advisory worktrees unless a separate exact approval exists.
- v477-v3-task-13 [command_index_surface]: Locate the current command book surface and its latest validation artifact.
- v477-v3-task-14 [command_index_surface]: Create a compact command-index manifest for workbench discovery.
- v477-v3-task-15 [command_index_surface]: Mark missing command surfaces as open gaps, not failures.
- v477-v3-task-16 [command_index_surface]: Link each command to source, owner, safety level, and validation status.
- v477-v3-task-17 [command_index_surface]: Keep executable examples bounded and non-destructive.
- v477-v3-task-18 [command_index_surface]: Add a drift receipt when command metadata points to stale files.
- v477-v3-task-19 [v54_v55_handoff]: Locate v54 and v55 handoff packs without broad importing old archives.
- v477-v3-task-20 [v54_v55_handoff]: Create surfaced handoff receipts with title, status, and next receiver.
- v477-v3-task-21 [v54_v55_handoff]: Mark unavailable handoffs as source gaps with search paths omitted from publication.
- v477-v3-task-22 [v54_v55_handoff]: Cross-reference Orun continuity only as routing context.
- v477-v3-task-23 [v54_v55_handoff]: Do not promote handoff material into canon by assertion.
- v477-v3-task-24 [v54_v55_handoff]: Add handoff acceptance criteria for v478 continuation.
- v477-v3-task-25 [skill_and_system_readiness]: Scan skill frontmatter health only through approved non-mutating checks.
- v477-v3-task-26 [skill_and_system_readiness]: Separate skill-loader repairs from THOS design artifacts.
- v477-v3-task-27 [skill_and_system_readiness]: Build a skill capability index from metadata, not full skill body dumps.
- v477-v3-task-28 [skill_and_system_readiness]: Flag duplicate or ambiguous skill names for later exact-path review.
- v477-v3-task-29 [skill_and_system_readiness]: Add a no-plugin-cache-mutation marker to ordinary THOS phases.
- v477-v3-task-30 [skill_and_system_readiness]: Create a skills-to-phase routing map for v478 and v479.
- v477-v3-task-31 [source_refresh_and_research]: Use official sources first for Codex, MCP, OpenAI Agents, NVIDIA, and cloud systems.
- v477-v3-task-32 [source_refresh_and_research]: Record source refresh as completed only after live page review.
- v477-v3-task-33 [source_refresh_and_research]: Separate journey_context_not_canon from evidence and implementation sources.
- v477-v3-task-34 [source_refresh_and_research]: Prefer source ledgers over large copied notes.
- v477-v3-task-35 [source_refresh_and_research]: Add citation-required flags to claims that depend on current product behavior.
- v477-v3-task-36 [source_refresh_and_research]: Keep search counts as process metadata rather than truth claims.
- v477-v3-task-37 [drive_github_continuity]: Use Google Drive v49 as journey context only, not physics validation.
- v477-v3-task-38 [drive_github_continuity]: Keep GitHub remote verification authoritative for repo state.
- v477-v3-task-39 [drive_github_continuity]: Avoid publishing restricted connector payloads into repo artifacts.
- v477-v3-task-40 [drive_github_continuity]: Record Drive/GitHub source titles without large copied passages.
- v477-v3-task-41 [drive_github_continuity]: Add continuity pointers for v49 to v477 without claiming full import.
- v477-v3-task-42 [drive_github_continuity]: Keep absolute local paths out of public-facing summaries where possible.
- v477-v3-task-43 [thos_safety_and_validation]: Validate every JSON artifact before staging.
- v477-v3-task-44 [thos_safety_and_validation]: Compile every new helper script before staging.
- v477-v3-task-45 [thos_safety_and_validation]: Run secret, session, screen-capture, and restricted-material guards on staged files.
- v477-v3-task-46 [thos_safety_and_validation]: Use exact staging only, never broad staging.
- v477-v3-task-47 [thos_safety_and_validation]: Fetch and drift-check before every push.
- v477-v3-task-48 [thos_safety_and_validation]: Verify remote equals local after publication.
- v477-v3-task-49 [gmut_boundary]: Keep all six GMUT gates open unless exact closure artifacts exist.
- v477-v3-task-50 [gmut_boundary]: Classify GMUT-adjacent THOS work as support infrastructure, not validation.
- v477-v3-task-51 [gmut_boundary]: Label Journey and Solas material as journey_context_not_canon.
- v477-v3-task-52 [gmut_boundary]: Avoid fifth-force safety, consciousness proof, or final physics claims.
- v477-v3-task-53 [gmut_boundary]: Preserve null, SI, conservation, baseline, equivalence, and bridge ledgers as open.
- v477-v3-task-54 [gmut_boundary]: Use simulation labels for any toy or fixture outputs.
- v477-v3-task-55 [phase_management]: Timestamp every x-session start and closeout in NZ time.
- v477-v3-task-56 [phase_management]: Allow x3 or x4 overlays only for concrete blockers or hardening work.
- v477-v3-task-57 [phase_management]: Commit every second phase where feasible and safe.
- v477-v3-task-58 [phase_management]: Publish blocker receipts instead of forcing closure.
- v477-v3-task-59 [phase_management]: Hand off a 60-task roadmap after each x2 or overlay closeout.
- v477-v3-task-60 [phase_management]: Keep v477 moving toward v478 only after five-lane readiness is confirmed.

## Acceptance Criteria

- Every new or updated JSON artifact parses.
- Every new helper script compiles.
- Staged files pass secret, session, screen-capture, restricted-material, and path-safety guards.
- No unfiltered app-lane, CLI-lane, or connector payloads are published.
- No new old-style subagents are spawned.
- Remote verification equals local after each publication.
