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
- Cloudflare MCP is still blocked from Codex with `Auth required`, so Wrangler auth and Codex MCP auth must be treated as separate surfaces.

## Auth Truth

- GitHub CLI auth was repaired; `gh auth status` now reports logged in.
- CircleCI CLI has local config and token according to `circleci diagnostic`.
- Wrangler reports Cloudflare OAuth login.
- E2B CLI still reports `Not logged in`.
- Vercel CLI remained interactive or timed out under bounded `whoami`.
- Neon CLI reached the browser/OAuth path but returned an OAuth `server_error`.
- Render CLI reports `render login` is required.
- OCI CLI is installed on PATH, but the bounded live auth probe timed out and was left unmutated.

## Auth Lane

A visible PowerShell auth lane was launched with this serial sequence:

- `gh auth login -h github.com -w`
- `e2b auth login`
- `vercel login`
- `neonctl auth`
- `render login`

The lane is intentionally serial so it does not spray multiple browser prompts at once. After the wait window, GitHub CLI was confirmed repaired; E2B, Vercel, Neon, and Render still need operator/browser completion or provider-side reconnect.

## CLI Agent Boundary

Codex CLI and Kimi CLI are both callable. Codex exposes non-interactive `exec` lanes with read-only ephemeral sandboxing, and Kimi exposes agent, MCP, print, and session lanes.

That proves CLI capability, not durable identity persistence. New Codex/Kimi lanes should be treated as receipt-backed task lanes until a native close/reopen continuity proof demonstrates persistent memory and identity on the underlying platform.

## Next Gate

Before v111 provider live-write actions, rerun the bounded provider probe after the auth lane is completed. Any provider mutation must remain an exact action pack with provider, resource, command, cost ceiling, rollback, and expected artifact.
