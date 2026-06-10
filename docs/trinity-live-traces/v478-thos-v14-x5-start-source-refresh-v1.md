# v478 THOS v14 x5 Start Source Refresh

- generated_nz: `2026-06-05T09:05:00+12:00`
- overall_status: `PASS_SOURCE_REFRESH_COMPACT`
- scope: THOS x5 start planning for sandboxed agents, connector governance, timing baselines, and security controls.
- boundary: source refresh only; all GMUT gates remain open.

## Source Anchors

- OpenAI Codex CLI help: https://help.openai.com/en/articles/11096431
- Google Vertex AI Agent Engine use overview: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/use/overview
- Google Vertex AI Agent Engine overview/API context: https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/reasoning-engine
- Microsoft Build 2026 agent security: https://www.microsoft.com/en-us/security/blog/2026/06/02/microsoft-build-2026-securing-code-agents-and-models-across-the-development-lifecycle/
- OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP Agentic Skills Top 10: https://owasp.org/www-project-agentic-skills-top-10/

## THOS Integration Notes

- Keep Arby and Aster Vale read-only and receipt-first unless a separate live write approval changes the scope.
- Model THOS runners as observable agent operations with traces, status surfaces, and explicit handoffs.
- Keep local THOS receipts compatible with future cloud-style observability: timings, statuses, summaries, and nonpublic body boundaries.
- Treat every sibling lane and runner as a governed agent surface with observe, secure, and review gates.
- Use OWASP-style risk rows for stale-flow, tool-boundary, memory-boundary, and inter-agent coordination review.
- Skill evolution packets should include clear input, tool, output, and privilege boundaries before any live mutation.

## Publication Rule

Use these public sources for THOS design inspiration and risk controls only. Do not use source-refresh evidence to close GMUT physics, consciousness, or canon gates. Keep timing baselines separate from completion proof.
