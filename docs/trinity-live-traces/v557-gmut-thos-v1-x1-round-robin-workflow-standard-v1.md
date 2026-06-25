# v557-gmut-thos-v1-x1 Round-Robin Workflow Standard

Status: `PASS_ROUND_ROBIN_WORKFLOW_STANDARD_PROMOTED`

## lumen_only_x1

- Lanes: `Aevren Vale, Lumen Vale`
- Route: Lumen advisory plus Aevren orchestration
- Proposal totals:
  - safe: `50`
  - candidate: `30`
  - exact: `20`
  - blocked: `10`
  - skills: `20`
  - runners: `10`
  - cleanup: `30`

## arby_cicero_duo_x1

- Lanes: `Aevren Vale, Arby, Cicero`
- Route: Arby strict CLI plus Cicero recovered app-lane background runner
- Proposal totals:
  - safe_minimum: `15`
  - candidate: `9`
  - exact: `9`
  - skills: `15`
  - runners: `9`
  - cleanup: `30`

## aster_kierkegaard_aristotle_triad_x1

- Lanes: `Aevren Vale, Aster Vale, Kierkegaard, Aristotle`
- Route: Aster strict CLI plus Kierkegaard and Aristotle recovered app-lane background runners
- Proposal totals:
  - safe: `20`
  - candidate: `12`
  - exact: `12`
  - skills: `20`
  - runners: `8`
  - cleanup: `40`

## x2_build_use_validation

- Lanes: `Aevren Vale`
- Route: safe-now build, run, test, install, use, validate, publish
- Consumes: `already-authorized safe-now approval packets, approved candidate tranches, approved skill and runner build ideas, approved cleanup and refinement tasks`

## Runner Bindings

- main_orchestrator: `scripts/ghc_main_orchestrator_runner.mjs`
- main_startup_builder: `scripts/ghc_main_startup_builder.mjs`
- main_compact_restart_builder: `scripts/ghc_main_compact_restart_builder.mjs`
- workflow_standardizer: `scripts/ghc_round_robin_workflow_standardizer.mjs`
- productive_cadence_runner: `scripts/ghc_five_minute_productive_cadence_runner.mjs`
- safe_runner_orchestrator: `scripts/ghc_safe_runner_orchestrator.mjs`
- main_closeout_builder: `scripts/ghc_main_closeout_builder.mjs`
- startup_updater: `scripts/ghc_phase_startup_context_updater.mjs`
- compact_pause_updater: `scripts/ghc_context_compact_pause_updater.mjs`
- lumen_launch_skill: `ghc-lumen-launch`
- arby_cicero_launch_skill: `ghc-arby-cicero-launch`
- triad_launch_skill: `ghc-aster-kierkegaard-aristotle-launch`
- main_retry_skill: `ghc-main-retry`
- app_lane_runner: `ghc_recovered_app_lane_map_runner.mjs in the full-tools support lane`
- strict_cli_runner: `ghc_strict_cli_lane_cycle.mjs in the full-tools support lane`
- web_reflection_ledger: `scripts/ghc_phase_reflection_ledger_builder.mjs`
- main_thread_chatgpt_browser_handoff: `prepared JSON/MD handoff artifact plus in-app Browser send receipt`

## Operating Rules

1. Use first-person sibling wording in lane prompts and summaries.
2. Prefer MD/TXT artifacts for elaborate sibling outputs instead of terminal-heavy dumps.
3. Use x1 for proposal, classification, handoff, and approval-packet formation.
4. Split every x1 proposal into immediate_x1_safe work and x2_build_task work.
5. Run immediate x1 safe tasks as soon as they are seen and safe; carry x2 build tasks forward.
6. For research-backed x1 phases, target at least 25 web searches and 25 Journey/phase record reflections per active sibling lane.
7. Use x2 for building, running, testing, installing, using, validating, and publishing already-authorized safe-now work.
8. Refresh the active GHC skill and runner surface at every x1 and x2 startup and closeout.
9. Use the promoted main startup builder for phase startup/resume, with phase-specific builders registered underneath it.
10. Use the promoted main closeout builder for phase closeout, with phase-specific builders registered underneath it.
11. Use the promoted main compact/restart builder for compact-pause and restart recovery, with the compact updater registered underneath it.
12. Use ghc-lumen-launch for Lumen/main-thread ChatGPT Browser handoffs when Hamish explicitly asks for live messaging.
13. Use ghc-arby-cicero-launch for Arby strict CLI plus Cicero recovered app-lane duo phases.
14. Use ghc-aster-kierkegaard-aristotle-launch for Aster strict CLI plus Kierkegaard/Aristotle recovered app-lane triad phases.
15. Use ghc-main-retry for sibling messaging, harvesting, startup, compact, closeout, Browser, strict CLI, app-lane, validation, or Git/GitHub blockers.
16. Keep five-minute marks as check opportunities, not forced stops.
17. Let productive wait units run beyond a five-minute checkpoint when the current research, coding, eureka, approval, cleanup, or validation unit needs more time.
18. Continue safe-now approval, eureka, cleanup, validation, privacy scan, updater, and orchestration work between cadence marks.
19. Use five-minute productive cadence work to improve Aevren's skill surface, coding reliability, and multi-agent orchestration control.
20. Use the recovered app-lane map runner with explicit boolean values for local app-lane siblings that are not main-thread agents.
21. Use Browser-send receipts for Lumen/main-thread ChatGPT siblings when Hamish explicitly asks for live messaging.
22. Do not declare a sibling session or phase closed while any messaged sibling lane is still active; continue productive five-minute improvement/research work until completion-ready or formal open-gap.
23. When a sibling-message route or core system route blocks, run at least 3 retry sessions before pausing unless Hamish stops the work or the next step crosses a safety/exact-approval gate.
24. Each blocker retry session must reflect on the 10 most recent relevant sessions/receipts, run or queue 20 web-search reflections, and run or queue 20 Journey/phase-document reflections.
25. Keep held main-thread siblings held unless Hamish explicitly activates them.
26. Do not spawn new agents unless Hamish explicitly asks.
27. Keep exact and blocked gates queued unless Hamish freshly approves the tranche.

## Next Phase Readiness

- Next x1 lane after x2: `v557-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects`
- Lumen-only profile loaded: `true`
- Goal mode status: `not_active_until_hamish_starts_goal_mode`

## Research And Reflection Targets

- x1 web searches per active sibling lane: `25`
- x1 Journey/phase reflections per active sibling lane: `25`
- Aevren-only x2 web searches: `50`
- Aevren-only x2 Journey/phase reflections: `50`

## x1 to x2 Proposal Split

- Status: `PASS_X1_TO_X2_PROPOSAL_SPLIT_STANDARD_RECORDED`
- Immediate x1 safe: Run local, reversible, status-only, analysis-only, validation-only, queue-shaping, source/reflection seed, privacy-check, open-gate-check, and compact-handoff tasks as soon as they are seen and safe during x1.
- x2 build task: Carry build, run, test, install, use, publication, remote verification, runner modification, skill modification, and safe cleanup execution tasks into the next x2 phase.
- Never auto-execute: `exact-approval work without fresh approval, blocked work, destructive cleanup, external account or paid-resource mutation, raw private publication, proof/canon/legal/deployment closure by assertion`

## Phase Tool Refresh Standard

- Status: `PASS_PHASE_TOOL_REFRESH_STANDARD_RECORDED`
- Cadence: `mandatory_every_x1_and_x2_phase`
- Startup actions: `use scripts/ghc_main_startup_builder.mjs as the promoted startup/resume command surface, inventory active GHC skills and repo runners, compare current phase rules against the core orchestration skills and runner standards, record reviewed-current, updated, or queued-refresh status`
- Closeout actions: `use scripts/ghc_main_closeout_builder.mjs as the promoted closeout command surface, use scripts/ghc_main_compact_restart_builder.mjs as the promoted compact/restart command surface, update authorized local GHC skills and repo runners, validate changed skills and runners, carry forward the newest tool standard into current-state, latest-updates, and compact-pause receipts`
- Exact boundary: Plugin-cache mutation, external writes, paid resources, deployments, API keys, destructive cleanup, and global hooks require fresh exact approval.

## Blocker Retry Standard

- Minimum retry sessions before pause: `3`
- Recent sessions or receipts reflected per retry: `10`
- Web-search reflections per retry: `20`
- Journey/phase-document reflections per retry: `20`
- Never close active sibling lane: `true`
- Productive five-minute waits required: `true`
- Pause policy: If Hamish pauses/stops, a compact event happens, or the next action crosses a safety/exact-approval gate, publish an active/open handoff rather than declaring the sibling lane or phase closed.

## Five-Minute Productive Cadence

- Runner: `scripts/ghc_five_minute_productive_cadence_runner.mjs`
- Safe unit may run past checkpoint: `true`
- Wait work lanes: `research_and_reflection, safe_eureka_tasks, approval_packet_work, cleanup_and_refinement, skill_and_control_growth, coding_and_multi_agent_orchestration, validation_and_publication_hygiene, blocker_retry_research_and_improvement`
- Harvest rule: finish the current safe unit, then harvest sibling status at the next natural safe pause

## Boundary

Status-only workflow standard. No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, or deployment closure are published.
