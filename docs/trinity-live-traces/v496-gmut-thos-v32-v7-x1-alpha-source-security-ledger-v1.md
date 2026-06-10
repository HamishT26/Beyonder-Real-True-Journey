# v496 GMUT/THOS v32 v7 x1 Alpha Source Security Ledger

- Phase: `v496-gmut-thos-v32-v7-x1`
- Status: `PASS_ALPHA_SOURCE_SECURITY_LEDGER_RECORDED`
- Wait started: `2026-06-06T09:37:36Z`
- Scheduled harvest after: `2026-06-06T09:52:36Z`
- Sibling status checked here: false
- Artifact upload checked here: false

## Sources

- [OpenAI Codex CLI Getting Started](https://help.openai.com/en/articles/11096431): sandbox, approval, and local-workflow boundaries for CLI lanes and x2 build sessions.
- [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/): low-risk autonomous work with explicit authorization boundaries.
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization): connector and app-server token/audience boundaries.
- [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/): skills, command runners, and helper workflows as execution-layer security surfaces.
- [OWASP Agentic Skills Checklist](https://owasp.org/www-project-agentic-skills-top-10/checklist.html): scoped credential, provenance, review, and least-privilege checks.
- [Google Cloud GKE Agent Sandbox](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/agent-sandbox): isolation and runtime-observability principles for local watcher and sandbox readiness.

## x2 Security Tasks

1. Add no-overclaim validation for GMUT/canon closure language.
2. Add a scoped skill-inventory receipt helper before any skill cleanup packet.
3. Add an MCP connector-boundary receipt for app-server and connector use.
4. Add a watcher/no-poll proof receipt for scheduled waiting windows.
5. Add a command-risk summary receipt that flags critical and high-risk command counts before x2 builds.

Claim boundary: no raw lane text, raw transport, credentials, local absolute paths, GMUT validation, or canon promotion is claimed.
