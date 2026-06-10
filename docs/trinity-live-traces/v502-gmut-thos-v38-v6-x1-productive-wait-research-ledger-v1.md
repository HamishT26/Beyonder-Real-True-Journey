# v502-gmut-thos-v38-v6-x1 Productive Wait Research Ledger

- generated_utc: `2026-06-08T10:53:16Z`
- generated_nz: `2026-06-08T22:53:16+12:00`
- overall_status: `PASS_PRODUCTIVE_WAIT_RESEARCH_RECORDED`
- watcher_supervision: `true`
- manual_babysitting_before_gate: `false`
- phase_advance_requires_all_five_responses: `true`
- duration_is_completion_proof: `false`

## Source Findings

- OpenAI Codex releases: Codex `0.137.0` is marked latest and includes TUI control improvements, app-server v2 remote-control RPCs, plugin JSON output, cached remote catalog suggestions, and hosted web/image/search support in more code-mode flows. Application: keep v502 v6 aligned to direct CLI bridge, app-server callable lanes, and machine-readable status receipts.
- OpenAI Windows sandbox article: Windows sandboxing should be treated as a scoped runtime boundary. Application: keep Arby and Aster Vale output temp-only with hashes, byte counts, quality gates, and marker-review receipts.
- MCP security best practices: confused deputy, local server compromise, and scope minimization remain central risks. Application: keep connector use read-scoped unless exact approval exists.
- OWASP Logging Cheat Sheet: logging should sanitize untrusted event data and avoid sensitive leakage. Application: continue status-only receipts and redaction guards for watcher, notifier, and completion artifacts.

## x2 Build Implications

- Promote the direct Node Codex bridge as the default CLI lane path for Arby and Aster Vale.
- Preserve launch-once, defer-checks-until-gate behavior so Aletheon can research and prepare instead of manually watching.
- Treat app-server and remote-control health as status metadata only; do not publish thread IDs or raw app messages.
- Keep plugin, MCP, and connector evidence scoped to source ledgers unless exact mutation approval exists.

Boundary: status only; no raw lane text, raw logs, prompts, screenshots, session streams, credentials, or local absolute paths are published here.

Claim boundary: GMUT, canon, consciousness, and final-physics gates remain open.
