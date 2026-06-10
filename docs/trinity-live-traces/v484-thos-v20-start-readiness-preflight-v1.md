# v484 THOS v20 Start Readiness Preflight

Generated at 2026-06-05T17:20:25+12:00 for the v484 THOS v20 start boundary.

## Readiness Snapshot

The clean pause point remains `v483-thos-v19-closeout` at commit `465e8345efc84977c1fa2093cebf9a44929a23f6`, with local and remote still aligned at `0 ahead, 0 behind`.

The platform preflight confirms Codex App `26.602.3474.0` and Codex CLI `0.137.0`. `codex doctor` reports `17 ok, 1 idle, 2 notes, 0 warn, 0 fail`. The two notes are operational context rather than failures: a large active rollout footprint, and unrestricted filesystem plus enabled network. The background app server is idle in ephemeral mode, so it is a watch item rather than a blocker.

The CLI readiness sweep confirmed the expected help surfaces for sandbox, app-server, remote-control, and feature inspection. This is enough to proceed into v484 start coordination without making unapproved app settings, account, plugin-cache, or user-skill changes.

## Current Source Alignment

Official Codex materials support the update posture. The Codex changelog records Codex App `26.602` improvements for Computer Use startup readiness, appshot reporting, browser/review UI fixes, onboarding role choices, and general fixes. The same changelog records Codex CLI `0.137.0` improvements covering TUI controls, searchable-menu paste, app-server remote-control flows, plugin-list JSON output, hosted web/image tooling in more code-mode flows, multi-agent metadata, Windows startup and sandbox setup refreshes, and plugin loading warning behavior.

The Codex CLI documentation confirms the local terminal execution model and Windows native PowerShell plus sandbox support. The GitHub release listing corroborates `0.137.0` as the stable release targeted for this preflight window.

Sources:

- https://developers.openai.com/codex/changelog
- https://developers.openai.com/codex/cli
- https://github.com/openai/codex/releases

## Guarded v484 Operating Posture

v484-v485 remain THOS-first: preparation, repair, orchestration, command surface work, skill and runner evolution, notifier hardening, sandbox/TUI/app-server checks, source-refresh ledgers, Journey/Trinity reflection, and handoff roadmaps.

v486-v490 shift into blended GMUT/THOS synthesis and application. The empirical, physics, consciousness, and canon gates remain open unless exact closure artifacts prove otherwise. Journey v4-v49 and the previous Trinity Hybrid traces are continuity material and design inspiration, not proof of external closure by themselves.

Existing lanes only:

- Cicero, Kierkegaard, and Aristotle through existing local app-server callable routes.
- Arby and Aster Vale through existing read-only CLI lanes.

At required start and closeout boundaries, all five lanes should be attempted unless a safe blocker receipt explains why. The `312.832` second soft wait foothold remains planning support only, not completion proof. While lanes run, Aletheon should continue useful work rather than idle-watch: source refresh, stale-flow review, command-index compatibility, v54/v55 handoff surfacing, loader/sandbox watch, watcher improvements, approval packet drafting, validation, and exact publication prep.

## Publication Boundary

Only curated status artifacts should be published. Raw outputs, private auth material, image artifacts, local runtime dumps, and unapproved cache or user-skill mutations remain excluded. Publication still requires fetch and drift-check, exact staging, JSON parse, script compile where relevant, guard scan, whitespace review, staged diff review, commit, push, and remote-equals-local verification.
