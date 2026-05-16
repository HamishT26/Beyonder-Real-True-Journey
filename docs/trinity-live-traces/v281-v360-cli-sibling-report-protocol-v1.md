# v281-v360 CLI Sibling Report Protocol

Generated UTC: `2026-05-16T08:06:56.071547+00:00`
Status: `active_protocol`

Give Arby, Kimi, and Aster Vale a higher-quality read-only lane contract with skills awareness, safe tool boundaries, and report-backed outputs.

Capability contract:
- Use local skills visible to the current CLI session when they are relevant and load cleanly.
- Name any skill, web source, or plugin-like surface used in the response.
- Use safe read-only web/search or simple document/plugin surfaces only when exposed without extra authentication.
- Do not mutate files, repos, external services, accounts, or plugin state from lane sessions.
- Do not expose secrets, tokens, cookies, private keys, or authentication material in reports.
- If a requested tool is unavailable, state the blocker and continue from local prompt context.

Report contract:
- The lane runner persists the final response file as the durable report artifact.
- Keep terminal-visible responses structured and concise enough to avoid terminal overload.
- For long work, write a report capsule in Omega and put the recommended report title/path in Next-phase handoff.
- Treat the lane response file as the first safe worktree-backed report; promote only curated summaries later.
- Use the six required labels exactly: Receipt, Beta, Alpha, Omega, Blocker, Next-phase handoff.
- Every label must contain a concrete non-empty sentence.

Timing contract:
- Do not optimize for speed over validity.
- A message may take minutes or hours if the lane is doing substantive work.
- Long waits are acceptable when status files and process health show progress.

Publication contract:
- Stage only curated summaries, protocols, gates, scripts, and complete non-raw reports.
- Never stage raw transport logs, stdout/stderr logs, partial live lane files, or marker-only invalid outputs.
- Keep Supervisor and v2 watcher as infrastructure candidates until persistence proof is reviewed.

Safe plugin boundary:
- `codex_app_documents`: Safe for curated document drafting when exposed in the app, but not assumed available inside CLI lane sessions.
- `web`: Allowed for read-only research when exposed and sourceable; use official or primary sources for product guidance.
- `mcp`: Deferred unless a lane-specific need is approved and startup health is verified.
- `external_auth`: Not allowed inside unattended lane sessions.

Recommended report paths:
- `docs/trinity-live-traces/v281-v300-double-trinity-lane-logs/<lane>-phase-v<phase>-response-<turn>.txt`
- `docs/trinity-live-traces/v301-v320-aletheon-phase-reports/`
- `docs/trinity-live-traces/v321-v340-cli-sibling-handoff/`
