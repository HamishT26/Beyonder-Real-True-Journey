# v553-gmut-thos-v1-x1 Round-Robin Workflow Standard

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
- workflow_standardizer: `scripts/ghc_round_robin_workflow_standardizer.mjs`
- productive_cadence_runner: `scripts/ghc_five_minute_productive_cadence_runner.mjs`
- safe_runner_orchestrator: `scripts/ghc_safe_runner_orchestrator.mjs`
- startup_updater: `scripts/ghc_phase_startup_context_updater.mjs`
- compact_pause_updater: `scripts/ghc_context_compact_pause_updater.mjs`
- app_lane_runner: `ghc_recovered_app_lane_map_runner.mjs in the full-tools support lane`
- strict_cli_runner: `ghc_strict_cli_lane_cycle.mjs in the full-tools support lane`
- web_reflection_ledger: `scripts/ghc_phase_reflection_ledger_builder.mjs`
- main_thread_chatgpt_browser_handoff: `prepared JSON/MD handoff artifact plus in-app Browser send receipt`

## Operating Rules

1. Use first-person sibling wording in lane prompts and summaries.
2. Prefer MD/TXT artifacts for elaborate sibling outputs instead of terminal-heavy dumps.
3. Use x1 for proposal, classification, handoff, and approval-packet formation.
4. For research-backed x1 phases, target at least 25 web searches and 25 Journey/phase record reflections per active sibling lane.
5. Use x2 for building, running, testing, installing, using, validating, and publishing already-authorized safe-now work.
6. Keep five-minute marks as check opportunities, not forced stops.
7. Let productive wait units run beyond a five-minute checkpoint when the current research, coding, eureka, approval, cleanup, or validation unit needs more time.
8. Continue safe-now approval, eureka, cleanup, validation, privacy scan, updater, and orchestration work between cadence marks.
9. Use five-minute productive cadence work to improve Aevren's skill surface, coding reliability, and multi-agent orchestration control.
10. Use the recovered app-lane map runner with explicit boolean values for local app-lane siblings that are not main-thread agents.
11. Use Browser-send receipts for Lumen/main-thread ChatGPT siblings when Hamish explicitly asks for live messaging.
12. Keep held main-thread siblings held unless Hamish explicitly activates them.
13. Do not spawn new agents unless Hamish explicitly asks.
14. Keep exact and blocked gates queued unless Hamish freshly approves the tranche.

## Next Phase Readiness

- Next x1 lane after x2: `v553-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects`
- Lumen-only profile loaded: `true`
- Goal mode status: `not_active_until_hamish_starts_goal_mode`

## Research And Reflection Targets

- x1 web searches per active sibling lane: `25`
- x1 Journey/phase reflections per active sibling lane: `25`
- Aevren-only x2 web searches: `50`
- Aevren-only x2 Journey/phase reflections: `50`

## Five-Minute Productive Cadence

- Runner: `scripts/ghc_five_minute_productive_cadence_runner.mjs`
- Safe unit may run past checkpoint: `true`
- Wait work lanes: `research_and_reflection, safe_eureka_tasks, approval_packet_work, cleanup_and_refinement, skill_and_control_growth, coding_and_multi_agent_orchestration, validation_and_publication_hygiene`
- Harvest rule: finish the current safe unit, then harvest sibling status at the next natural safe pause

## Boundary

Status-only workflow standard. No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, or deployment closure are published.
