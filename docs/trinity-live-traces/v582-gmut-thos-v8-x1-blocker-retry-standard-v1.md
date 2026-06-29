# v582-gmut-thos-v8-x1 Blocker Retry Standard

Status: `PASS_BLOCKER_RETRY_STANDARD_RECORDED`

## Mandatory Sibling Completion

- Never close while sibling active: `true`
- Completion states: `completed_ready_for_harvest, completion_gate_passed`
- Noncompletion states: `active_fresh, active_stale, retrying, formal_open_gap`
- Pause policy: If Hamish explicitly pauses/stops, a compact event happens, or an exact/safety gate blocks continuation, publish an active/open handoff rather than a closed session.

## Blocker Retry Protocol

- Minimum retry sessions before pause: `3`
- Recent sessions or receipts reflected per retry: `10`
- Web-search reflections per retry: `20`
- Journey/phase-document reflections per retry: `20`
- Productive cadence minutes: `10`
- Productive cadence runner: `scripts/ghc_family_productive_cadence_runner.mjs`
- Productive five-minute waits required: `false`
- Retry receipt required: `true`

## Productive Wait Standard

- Ten-minute marks are checkpoints, not hard stops: `true`
- Older five-minute marks are historical fallback only: `true`
- Safe units may run past checkpoint: `true`
- Improvement lanes: `research_and_reflection, safe_eureka_tasks, approval_packet_work, cleanup_and_refinement, skill_and_control_growth, coding_and_multi_agent_orchestration, browser_handoff_harvest, blocker_retry_research_and_improvement, validation_and_publication_hygiene`

## Boundary

Status-only standard. No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, deployment closure, account mutation, or API-key creation are published.
