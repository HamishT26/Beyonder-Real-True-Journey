# v553-gmut-thos-v1-x1 Phase Tool Refresh Standard

Status: `PASS_PHASE_TOOL_REFRESH_STANDARD_RECORDED`
Cadence: `mandatory_every_x1_and_x2_phase`

## Startup Required Actions

- use scripts/ghc_main_startup_builder.mjs as the promoted startup/resume command surface
- inventory active GHC skills and repo runners
- load the main orchestration, full-tools, compact-pause, web-reflection, safe-runner, approval-splitter, x1-to-x2 queue-composer, main-startup, main-closeout, and main-compact-restart rules when relevant
- compare current phase instructions against the skill and runner standards
- publish or update a phase tool refresh receipt

## Closeout Required Actions

- use scripts/ghc_main_closeout_builder.mjs as the promoted closeout command surface
- use scripts/ghc_main_compact_restart_builder.mjs as the promoted compact/restart command surface
- update core orchestration skill/runners when Hamish gives live update authority or when repo-local runner standards need safe publication
- validate changed skills and runners
- record unchanged-but-reviewed tools as reviewed_current
- carry forward the latest tool standard into current-state, latest-updates, and compact-pause handoffs

## Safety Boundary

Do not mutate plugin-cache skills, external accounts, paid resources, deployments, API keys, destructive cleanup, or global hooks without fresh exact approval.
