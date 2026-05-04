# v110 Provider PATH and MCP Live-Write Receipt

## Summary

v110 finished as a guarded local/cloud live-write phase with the provider layer materially improved, but not falsely marked complete. PATH is now healthy for the major local CLIs: `codex`, `kimi`, `gh`, `oci`, `wrangler`, `circleci`, `node`, `npm`, `npx`, `e2b`, `vercel`, `neonctl`, `neon`, and `render`.

No provider create, deploy, delete, DNS, billing, or spend action was executed. The pass only installed local CLIs, verified checksums where needed, tested read/status surfaces, and opened a visible auth-repair lane for the providers that still need operator/browser completion.

## PATH Results

The following blocked CLIs were repaired:

- `e2b` now resolves on PATH at version `2.10.1`.
- `vercel` now resolves on PATH at version `53.1.0`.
- `neonctl` and `neon` now resolve on PATH at version `2.22.0`.
- `render` now resolves on PATH at version `2.16.0`.

Install sources used:

- E2B: official `npm install -g @e2b/cli@latest`.
- Vercel: official `vercel@latest` global npm CLI.
- Neon: official `neonctl@latest` global npm CLI.
- Render: official `render-oss/cli` Windows AMD64 release `v2.16.0`, checksum verified, copied to `C:/Users/hamis/bin/render.exe`.

## MCP And Plugin Truth

- GitHub app connector is callable and returned the installed account.
- Google Drive app connector is callable; shared-drive listing returned empty, so `google_drive_state=operator_hold` remains the honest state.
- Linear app connector is callable and returned the `Beyonder-Real-True Journey` project.
- Cloudflare Wrangler CLI is authenticated and usable for read/status checks.
- Cloudflare MCP is still blocked from Codex with `Auth required` after multiple OAuth retries, so Wrangler auth and Codex MCP auth must be treated as separate surfaces.

## Auth Truth

- GitHub CLI auth was repaired; `gh auth status` now reports logged in.
- CircleCI CLI has local config and token according to `circleci diagnostic`.
- Wrangler reports Cloudflare OAuth login.
- E2B CLI is now authenticated after retry.
- Vercel CLI is now authenticated after retry.
- Neon CLI is now authenticated after focused retry; scripted project probes should pass `--org-id` to avoid the interactive organization picker.
- Render CLI is now authenticated after retry.
- OCI CLI now returns region metadata from a bounded read-only probe.

## Auth Lane

A visible PowerShell auth lane was launched with this serial sequence:

- `gh auth login -h github.com -w`
- `e2b auth login`
- `vercel login`
- `neonctl auth`
- `render login`

The lane is intentionally serial so it does not spray multiple browser prompts at once. After the retry window, GitHub CLI, E2B CLI, Vercel CLI, Neon CLI, and Render CLI were confirmed repaired. Neon needs org-scoped commands for automation, because an unscoped project list opens an interactive organization picker.

## Cloudflare MCP Final Retry

Cloudflare MCP was retried three ways:

- `codex mcp login cloudflare-api`
- `codex mcp logout cloudflare-api` followed by `codex mcp login cloudflare-api`
- A final hold-open `codex mcp logout/login` retry with a 10 minute terminal hold

The live MCP probe still returned `Auth required`. The honest interpretation is that this is no longer just a rushed browser approval window. Wrangler CLI auth works, but this Codex session's Cloudflare MCP tool has not received or reloaded the OAuth grant. The next repair path is a Codex app MCP reconnect/session refresh, or a static bearer-token MCP configuration if we choose that route later with a narrow secret-handling plan.

## CLI Agent Boundary

Codex CLI and Kimi CLI are both callable. Codex exposes non-interactive `exec` lanes with read-only ephemeral sandboxing, and Kimi exposes agent, MCP, print, and session lanes.

That proves CLI capability, not durable identity persistence. New Codex/Kimi lanes should be treated as receipt-backed task lanes until a native close/reopen continuity proof demonstrates persistent memory and identity on the underlying platform.

## Next Gate

Before v111 provider live-write actions, rerun the bounded provider probe after Cloudflare MCP auth changes or a Codex app refresh. Any provider mutation must remain an exact action pack with provider, resource, command, cost ceiling, rollback, and expected artifact.
