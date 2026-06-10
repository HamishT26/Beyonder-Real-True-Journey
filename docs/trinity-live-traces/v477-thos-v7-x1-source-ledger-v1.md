# v477 THOS v7 x1 Source Ledger

- search_count: `32`
- claim ceiling: THOS architecture and governance context only.

## Sources
- OpenAI Codex app-server source: https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md (official_source_repo) - App-lane transport assumptions.
- OpenAI Codex releases: https://github.com/openai/codex/releases (official_source_repo) - CLI version and feature drift context.
- OpenAI Windows sandbox: https://openai.com/index/building-codex-windows-sandbox/ (official) - Windows sandbox architecture context.
- MCP tools spec: https://modelcontextprotocol.io/specification/2025-06-18/server/tools (official) - Tool output and resource-link semantics.
- MCP authorization spec: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization (official) - Connector authorization boundary context.
- MCP SDK docs: https://modelcontextprotocol.io/docs/sdk (official) - SDK routing for future MCP probes.
- GitHub push protection: https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection (official) - Publication guard context.
- GitHub Actions security: https://docs.github.com/en/actions/how-tos/security-for-github-actions (official) - Workflow hardening context.
- GitHub MCP Server in IDE: https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/use-the-github-mcp-server (official) - MCP connector usage context.
- Windows Sandbox configuration: https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file (official) - Sandbox config vocabulary.
- Windows integrity control: https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control (official) - Integrity-level vocabulary.
- PowerShell execution policies: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6 (official) - PowerShell safety caveat.
- Python subprocess: https://docs.python.org/3.12/library/subprocess.html (official) - Safe process invocation context.
- Python tempfile: https://docs.python.org/3.12/library/tempfile.html (official) - Temporary output lifecycle context.
- OpenTelemetry signals: https://opentelemetry.io/docs/concepts/signals/ (official) - Trace, metric, log, and event vocabulary.
- Docker Compose Watch: https://docs.docker.com/compose/how-tos/file-watch/ (official) - Watcher analogy.
- Kubernetes Jobs: https://kubernetes.io/docs/concepts/workloads/controllers/job/ (official) - Completion and retry vocabulary.
- Vertex AI Agent Engine: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview (official) - Agent runtime architecture context.
- Gemini API File Search: https://ai.google.dev/gemini-api/docs/file-search (official) - RAG citation and retrieval context.
- Google File Search update: https://blog.google/innovation-and-ai/technology/developers-tools/expanded-gemini-api-file-search-multimodal-rag/ (official_blog) - Current retrieval context.
- NVIDIA NIM: https://docs.nvidia.com/nim/ (official) - Inference microservice architecture context.
- NVIDIA DGX Spark: https://docs.nvidia.com/dgx/dgx-spark/index.html (official) - Local AI capacity planning context.
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework (official) - Risk taxonomy context.
- UNESCO AI ethics: https://www.unesco.org/en/artificial-intelligence/recommendation-ethics (official) - Human-centered AI ethics context.
- OECD AI Principles: https://www.oecd.org/en/topics/ai-principles.html (official) - Trustworthy AI policy context.
- EU AI Act timeline: https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline (official) - Regulatory-timeline context.
- OpenAI Agents SDK: https://platform.openai.com/docs/guides/agents-sdk/ (official) - Agent orchestration and tracing context.
- OpenAI Agents SDK tracing: https://openai.github.io/openai-agents-python/tracing/ (official_source_docs) - Trace and handoff design context.
- OpenAI Apps SDK help: https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk (official) - App and MCP connector design context.
- OpenAI structured outputs: https://platform.openai.com/docs/guides/structured-outputs (official) - Schema-bound output context.
