# v477 THOS v8 x1 Source Ledger

- generated_nz: `2026-06-04T08:08:24+12:00`
- source_count: `32`
- policy: official or primary sources preferred; no queued search is claimed as completed unless represented in this ledger.

## Sources
- S01: [OpenAI Codex app-server README](https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md) — Local app-lane notifier routing and sanitized thread read/resume/start evidence.
- S02: [OpenAI Codex releases](https://github.com/openai/codex/releases) — CLI readiness context and version-drift checks.
- S03: [OpenAI Windows sandbox writeup](https://openai.com/index/building-codex-windows-sandbox/) — Sandbox constraint routing for Arby/Aster and app-lane read-only requests.
- S04: [MCP tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) — Tool metadata and command-index surface contracts.
- S05: [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) — Connector access boundary checks for read/use surfaces.
- S06: [MCP security best practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) — Tool-poisoning and cross-tool trust boundaries.
- S07: [MCP SDK documentation](https://modelcontextprotocol.io/docs/sdk) — Future local connector runner design.
- S08: [GitHub Actions security hardening](https://docs.github.com/en/actions/how-tos/security-for-github-actions) — Commit/push and automation guard requirements.
- S09: [GitHub push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection) — Publication guard checks before exact staging.
- S10: [GitHub SARIF support](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning) — Structured issue-report shape for later THOS validators.
- S11: [GitHub Copilot coding agent MCP docs](https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-coding-agent-with-mcp) — MCP handoff and agent tool exposure context.
- S12: [Microsoft Windows Sandbox configuration](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file) — Sandbox setup blocker taxonomy.
- S13: [Microsoft Mandatory Integrity Control](https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control) — Windows trust-boundary reasoning for low-write probes.
- S14: [Python subprocess documentation](https://docs.python.org/3.12/library/subprocess.html) — Bounded launcher and notifier process handling.
- S15: [Python tempfile documentation](https://docs.python.org/3.12/library/tempfile.html) — Temp-only lane output handling.
- S16: [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/) — Watcher event taxonomy without publishing event payloads.
- S17: [Docker Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/) — Future local service watcher design.
- S18: [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) — Retry budget and blocker-dominance conventions.
- S19: [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/) — Portable naming scheme for THOS receipt events.
- S20: [Vertex AI Agent Engine overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview) — External agent-engine comparison context only.
- S21: [Gemini API File Search](https://ai.google.dev/gemini-api/docs/file-search) — Future RAG handoff framing.
- S22: [NVIDIA NIM documentation](https://docs.nvidia.com/nim/) — Compute expansion context, not executed in this phase.
- S23: [NVIDIA DGX Spark documentation](https://docs.nvidia.com/dgx/dgx-spark/index.html) — Hardware-roadmap context, not a local capability claim.
- S24: [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — Risk register and safety-governance language.
- S25: [UNESCO AI ethics recommendation](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics) — High-level governance context only.
- S26: [OECD AI principles](https://www.oecd.org/en/topics/ai-principles.html) — High-level governance context only.
- S27: [EU AI Act implementation timeline](https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline) — Regulatory-timeline context for future THOS compliance notes.
- S28: [OpenAI Agents SDK guide](https://platform.openai.com/docs/guides/agents-sdk/) — Agent handoff and trace framing.
- S29: [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/) — Trace shape inspiration for local notifier receipts.
- S30: [OpenAI Agents SDK handoffs](https://openai.github.io/openai-agents-js/guides/handoffs/) — Handoff-board framing for v8 x2.
- S31: [OpenAI Apps SDK help](https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk) — App connector/tool-surface context.
- S32: [OpenAI structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — Schema-bound receipt quality checks.
