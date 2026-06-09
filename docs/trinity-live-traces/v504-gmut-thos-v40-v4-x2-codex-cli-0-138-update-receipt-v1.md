# v504 GMUT/THOS v40 v4 x2 Codex CLI 0.138.0 Update Receipt

Generated UTC: `2026-06-09T06:08:00Z`

Status: `PASS_CODEX_CLI_0_138_0_UPDATED`

## Result

- Before update: `codex-cli 0.137.0`.
- Published npm latest: `0.138.0`.
- Update command: `codex update`.
- Update result: success.
- After update: `codex-cli 0.138.0`.
- Post-update doctor version: `0.138.0`.
- Post-update doctor failures: `0`.
- Doctor status: `warning`, due to thread inventory parity and ephemeral app-server state.

## Watch Items

- The updater reported a stale npm temp cleanup warning. No cleanup was performed in this receipt.
- Doctor reports rollout files and state DB thread inventory differ. No raw session state was edited.
- Doctor reports app-server is not running in persistent daemon mode. This remains compatible with the existing ephemeral/local app-server lane workflow.

## Source Checks

- OpenAI Codex GitHub releases showed `0.138.0` as latest on June 8, 2026.
- npm reported `@openai/codex` latest as `0.138.0`.

## Boundary

This receipt is status-only. It publishes no raw logs, credentials, screenshots, session streams, private dumps, local install paths, or raw lane text. GMUT, canon, consciousness, and final-physics gates remain open.
