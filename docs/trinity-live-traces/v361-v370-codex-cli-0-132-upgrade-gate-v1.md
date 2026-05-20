# v361-v370 Codex CLI 0.132 Upgrade Gate

Generated UTC: `2026-05-20T05:29:00Z`

Status: `codex_cli_0_132_0_verified`

Previous local version: `codex-cli 0.131.0`

Current local version: `codex-cli 0.132.0`

Update command: `codex update`

Doctor status: `13 ok, 1 idle, 2 notes, 0 warn, 0 fail`

Official release source: `https://github.com/openai/codex/releases/tag/0.132.0`

Release features used by this packet:
- Python SDK first-class authentication and account APIs.
- Simpler text-only Python turn APIs and richer `TurnResult` data.
- `codex exec resume --output-schema` for structured resumed automations.
- Faster TUI startup from batched terminal capability probes.
- Remote executor registration through standard Codex authentication.

Truth boundaries:
- The npm update reported a Windows cleanup warning for an old temporary package directory; this is non-blocking because active version and doctor checks are healthy.
- Codex Desktop may still need restart/reopen after CLI update before app-side runtime behavior fully reflects the new install.
- `codex exec resume` must only be used when the target session is proven to belong to the same phase and lane.
- The `v361-v370` runner records future Codex CLI lane sessions for possible resume; raw transport remains unstaged.

Next action: use the updated `v361-v370` prompt and runner from `v363` onward.
