# v333-v360 Toolchain Upgrade Readiness

Generated NZT: `2026-05-19T16:27:49+12:00`
Status: `ready_for_operator_unpause`
Branch head at start of upgrade pass: `5299d082aded170fd9b9228cf75e9539a0ec9d2d`

## Boundary

This was a local toolchain and readiness pass only.

- v333 was not completed.
- v334 was not opened.
- No paid provider spend was triggered.
- No cloud resources were created, deleted, deployed, or mutated.
- No personal-account settings were changed.
- No raw lane replies, stdout/stderr logs, live logs, pycache files, or scratch probes were staged.

## Durable Phase State

- v281-v300: complete, `600/600`, global v2 complete.
- v301-v320: complete through v320.
- v321-v340: paused at `v333 phase_started`, with v332 complete.
- Run-status authority: `docs/trinity-live-traces/v321-v340-sibling-run-status-v1.json`.
- Health check status after upgrade pass: `v321_v340_paused`.

## Toolchain Updates Completed

| Surface | Before | After | Method |
| --- | --- | --- | --- |
| Codex CLI | `0.130.0` | `0.131.0` | `npm install -g @openai/codex@0.131.0` |
| npm | `11.12.0` | `11.14.1` | `npm install -g npm@11.14.1` |
| Kimi CLI | `1.38.0` | `1.44.0` | `uv tool upgrade kimi-cli --no-cache` |
| GitHub CLI | `2.91.0` | `2.92.0` | `winget upgrade --id GitHub.cli` |
| CircleCI CLI | `0.1.35213` | `0.1.36202` | `winget upgrade --id CircleCI.CLI` |
| Vercel CLI | `53.1.0` | `54.1.0` | `npm install -g vercel@54.1.0` |
| Wrangler CLI | `4.86.0` | `4.92.0` | `npm install -g wrangler@4.92.0` |
| EAS CLI | `18.8.1` | `18.13.1` | `npm install -g eas-cli@18.13.1` |
| E2B SDK package | `2.19.2` | `2.21.0` | `npm install -g e2b@2.21.0` |

Already current:

- `@e2b/cli`: `2.10.1`.
- `neonctl`: `2.22.0`.
- `kimi-code-mcp`: npm latest `1.0.0`.

## Verification

- `codex --version`: `codex-cli 0.131.0`.
- `kimi --version`: `kimi, version 1.44.0`.
- `kimi info`: wire protocol `1.10`, Python `3.13.13`.
- `npm outdated -g --depth=0 --json`: `{}` after updates.
- `gh --version`: `2.92.0`.
- `circleci version`: `0.1.36202+50a6f56`.
- `vercel --version`: `54.1.0`.
- `wrangler --version`: `4.92.0`.
- `eas --version`: `18.13.1`.
- `e2b --version`: `2.10.1`.
- `neon --version`: `2.22.0`.

## Codex Doctor Result

`codex doctor --json` completed with overall status `warning`, not failure.

Important findings:

- Runtime version: `0.131.0`.
- Auth: configured through ChatGPT tokens.
- Config: loaded successfully.
- MCP config: locally consistent.
- Configured MCP servers: `11` in doctor output, `12` visible in `codex mcp list` including `xcodebuildmcp`.
- Network provider reachability: OK.
- WebSocket handshake: OK.
- State DB integrity: OK.
- Search provider: `rg.exe` OK.

Warnings:

- The persistent daemon-style app-server was not running; Codex was operating in ephemeral app-server mode.
- Doctor could not inspect npm global root even though `npm` itself was callable and the active `codex` command verified as `0.131.0`.

Operational interpretation:

- The warnings do not block the v333 automation resume.
- If later remote-control work needs a durable daemon, start and verify that daemon intentionally instead of treating the warning as a repo failure.

## MCP and Plugin Posture

Codex MCP list:

- `circleci`
- `docker`
- `e2b`
- `expo`
- `github`
- `kimicode`
- `neon`
- `notion`
- `oci`
- `openai`
- `render`
- `xcodebuildmcp`

Kimi:

- `kimi mcp list`: no Kimi-side MCP servers configured.
- `kimi plugin list`: no Kimi-side plugins installed.

Interpretation:

- Codex remains the MCP-heavy coordinator.
- Kimi is clean and ready as a CLI lane.
- Do not add new OAuth/API-key MCP connections during unattended automation; use explicit scope approval first.

## Source Anchors Used

- OpenAI Codex CLI help: https://help.openai.com/en/articles/11096431
- OpenAI Codex releases: https://github.com/openai/codex/releases
- OpenAI Codex automations: https://openai.com/academy/codex-automations
- OpenAI Codex use cases: https://developers.openai.com/codex/use-cases/
- OpenAI GPT-5.2-Codex model page: https://developers.openai.com/api/docs/models/gpt-5.2-codex
- Kimi CLI getting started and upgrade: https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html
- Kimi CLI sessions: https://moonshotai.github.io/kimi-cli/en/guides/sessions.html
- Kimi CLI MCP: https://moonshotai.github.io/kimi-cli/en/customization/mcp.html
- Kimi CLI agents: https://moonshotai.github.io/kimi-cli/en/customization/agents.html
- Kimi CLI changelog: https://moonshotai.github.io/kimi-cli/en/release-notes/changelog.html
- Vercel CLI docs: https://vercel.com/docs/cli
- Cloudflare Wrangler install/update: https://developers.cloudflare.com/workers/wrangler/install-and-update/
- Expo EAS CLI docs: https://docs.expo.dev/eas/cli/
- Neon MCP overview: https://neon.com/docs/ai/neon-mcp-server
- E2B CLI docs: https://e2b.dev/docs/cli
- CircleCI CLI docs: https://circleci.com/docs/guides/toolkit/local-cli/
- GitHub CLI releases: https://github.com/cli/cli/releases
- MCP security best practices: https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices
- MCP authorization: https://modelcontextprotocol.io/docs/tutorials/security/authorization

## Operator Unpause Recommendation

You can unpause the `Aletheon` thread automation at 30 minutes using the v333-v360 resume bridge prompt.

Recommended first wake expectation:

- It should read the run-status JSON.
- It should see paused `v333`.
- It should complete exactly v333 and open v334 if no duplicate active child exists.
- It should stage only curated phase artifacts and preserve all raw/log/pycache exclusions.
