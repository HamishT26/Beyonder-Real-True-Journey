# v504-gmut-thos-v40-v1-x1 Productive Wait Research Ledger

Generated UTC: `2026-06-08T22:01:08Z`

Status: `PASS_PRODUCTIVE_WAIT_RESEARCH_RECORDED`

Manual sibling polling before gate: `false`

Next manual status check not before: `2026-06-08T22:08:24Z`

## Sources

- OpenAI Codex app introduction: skills and reusable workflows are first-class Codex app surfaces; THOS helper governance should keep skills explicit, scoped, and repeatable. Source: <https://openai.com/index/introducing-the-codex-app/>
- OpenAI Codex product page: Codex is positioned for multi-agent workflows with worktrees and parallel agents, matching watcher-first lane orchestration. Source: <https://openai.com/codex/>
- OpenAI Codex GitHub releases: official release surface shows `0.137.0` as latest stable while `0.138.0-alpha` prereleases are visible; production runners should distinguish stable from prerelease signals. Source: <https://github.com/openai/codex/releases>
- Model Context Protocol security best practices: connector and tool boundaries should minimize scope and treat authorization, proxy behavior, and local server compromise as explicit risks. Source: <https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices>
- OWASP Logging Cheat Sheet: status receipts should be useful for operations while avoiding sensitive raw runtime output and testing logging failure modes. Source: <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>

## Design Implications

- Keep watcher/notifier helpers as explicit reusable workflow surfaces rather than ad hoc manual polling.
- Separate stable Codex CLI readiness from prerelease awareness before changing runner assumptions.
- Treat app wrapper stale receipts as operational log-quality gaps, not proof that sibling work failed.
- Use MCP and OWASP guidance to keep connector and receipt publication boundaries tight.
- Prepare x2 build work around helper acceptance tests, command-surface compatibility, and source-backed safety gates.
