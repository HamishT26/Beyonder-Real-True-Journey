# v553-gmut-thos-v1-x1 Startup Context

Status: `PASS_V553_V1_X1_LUMEN_STARTUP_READY`

- Previous phase: `v552-gmut-thos-v88-v8-x2`
- Active lanes: `Aevren Vale, Lumen Vale`
- Latest completed x1: `v552-gmut-thos-v88-v8-x1`
- Latest completed x2: `v552-gmut-thos-v88-v8-x2`
- Next x2 scope: `v553-gmut-thos-v1-x2`
- Next x1 lane after x2: `v553-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects`

## Proposal Targets

- safe: `50`
- candidate: `30`
- exact: `20`
- blocked: `10`
- skills: `20`
- runners: `10`
- cleanup: `30`

## Research Targets

- x1 web searches per active sibling lane: `25`
- x1 Journey/phase reflections per active sibling lane: `25`
- Aevren-only x2 web searches: `50`
- Aevren-only x2 Journey/phase reflections: `50`

## Blocker Retry Standard

- Minimum retry sessions before pause: `3`
- Recent sessions or receipts reflected per retry: `10`
- Web-search reflections per retry: `20`
- Journey/phase-document reflections per retry: `20`
- Never close active sibling lane: `true`
- Productive five-minute waits required: `true`
- Pause policy: Run three structured retry sessions before pausing unless Hamish explicitly stops the work or the next step crosses a safety/exact-approval gate; if forced to pause, publish active/open status rather than closed.

## Changes Since v7 x2

- Twenty validated local skills and ten runners were promoted as the current continuity pack.
- Main orchestration, full-tools skill bank, compact-pause updater, web-reflection ledger, and safe-runner orchestrator skills are active.
- Round-robin workflow profiles now define Lumen-only, Arby/Cicero duo, and Aster/Kierkegaard/Aristotle triad x1 counts.
- Five-minute waits are productive safe-work windows and may run past a checkpoint before status harvest.
- Recovered app-lane background runner remains mandatory for non-main-thread app siblings.
- Every active x1 sibling lane now targets 25 public web searches and 25 Journey/phase reflections when the phase asks for research-backed planning.
- Aevren-only x2 phases keep the 50 web-search and 50 Journey/phase reflection target.
- Sibling lanes must not be declared closed while active; blockers require 3 retry sessions with 10 recent-session reflections, 20 web-search reflections, and 20 Journey/phase-document reflections per retry before pausing.

## Boundary

Status-only startup. No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, deployment closure, account mutation, or API-key creation are published.
