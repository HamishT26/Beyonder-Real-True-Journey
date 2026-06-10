# v502-gmut-thos-v38-v7-x1 Productive Wait Research Ledger

- generated_utc: `2026-06-08T11:52:18Z`
- overall_status: `PASS_PRODUCTIVE_WAIT_RESEARCH_RECORDED`
- watcher_supervision: `true`
- manual_babysitting_before_gate: `false`
- phase_advance_requires_all_five_responses: `true`

## Source Findings

- OpenAI Codex CLI Help Center: Codex CLI is a terminal-based coding agent. Application: keep Arby/Aster bridge launches scriptable and resumable with temp-only raw output.
- OpenAI Codex CLI sign-in guidance: CLI auth and generated secrets are separate from ChatGPT session state. Application: keep secrets, session material, and raw logs out of phase artifacts.
- OpenAI Codex GitHub releases: current Codex surfaces benefit from machine-readable receipts. Application: keep launch, gate, quality, marker, exposure, classifier, and phase-advance receipts separated.
- MCP security best practices: scope minimization matters for local tool surfaces. Application: keep connector and tool use read-scoped unless exact mutation approval exists.
- OWASP Secrets Management Cheat Sheet: prevent repository exposure of secrets. Application: continue staged-name guards, exposure guards, redaction guards, and temp-only raw output.

## x2 Build Implications

- Make direct CLI bridge and app-server watcher evidence reusable across v7-v8.
- Treat marker-review warnings as a required safety gate.
- Split source-ledger evidence from raw sibling outputs.
- Use status-only build queues for x2 implementation work.

Boundary: status only; no raw lane text, raw logs, prompts, screenshots, session streams, credentials, or local absolute paths.
