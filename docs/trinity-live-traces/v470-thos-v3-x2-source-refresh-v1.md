# v470 THOS v3 x2 Source Refresh

Phase: `v470_THOS_v3_x2`

Created NZ: `2026-06-02T14:28:24+12:00`

This artifact records the official-source refresh used for the x2 synthesis. The refresh met the x2 floor with 24 web searches against a requested minimum of 20.

## Claim Ceiling

- The sources are context and comparator evidence for THOS planning.
- They do not validate GMUT physics.
- They do not close any GMUT gate.
- They do not authorize cleanup, connector writes, deployment, paid cloud resource creation, or Drive/GitHub mutation.

## Source Set

- NVIDIA DGX Spark User Guide: https://docs.nvidia.com/dgx/dgx-spark/index.html
- NVIDIA RTX PRO 6000 Blackwell Series: https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000-family/
- NVIDIA NVLink and NVLink Switch: https://www.nvidia.com/en-us/data-center/nvlink/
- NVIDIA Nemotron: https://www.nvidia.com/en-us/ai-data-science/foundation-models/llama-nemotron/
- Google Cloud Vertex AI Agent Engine overview: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview
- Google Cloud Gemini CLI: https://cloud.google.com/gemini/docs/codeassist/gemini-cli
- Google Kubernetes Engine AI/ML workloads: https://docs.cloud.google.com/kubernetes-engine/docs/concepts/machine-learning
- OpenAI Running Codex safely: https://openai.com/index/running-codex-safely/
- OpenAI Agents guide: https://platform.openai.com/docs/guides/agents
- OpenAI Agent evals: https://platform.openai.com/docs/guides/agent-evals
- Model Context Protocol authorization specification: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
- GitHub artifact attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- PowerShell execution policies: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies
- NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final
- CISA Secure by Design: https://www.cisa.gov/resources-tools/resources/secure-by-design
- W3C DID Core: https://www.w3.org/TR/did-core/
- W3C Verifiable Credentials Data Model v2.0: https://www.w3.org/TR/vc-data-model/
- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications
- OpenTelemetry semantic conventions: https://opentelemetry.io/docs/concepts/semantic-conventions/
- Git add documentation: https://git-scm.com/docs/git-add
- Git diff documentation: https://git-scm.com/docs/git-diff
- Google Drive read-only v49 Journey presence check: https://docs.google.com/document/d/1eoISeXj_78XFnZmQ1pE3u4B1p4BRbw_1fa2Xp5eYQ2Q

## THOS Routing

The source refresh routes into four THOS lanes:

- Runtime fabric: NVIDIA, Google Cloud, OpenAI Agents, GKE, OpenTelemetry.
- Command and connector surface: MCP authorization, PowerShell, Git, GitHub attestations.
- Governance and identity comparator: W3C DID, W3C Verifiable Credentials, CISA, NIST.
- AI-agent risk model: OpenAI Codex safety, OWASP LLM Top 10, Agent evals.

## Open Gaps

- The NVIDIA connector tool was not exposed as a callable tool in the current context, though local NVIDIA skill bundles were discovered for future THOS routing.
- Google Drive was not mutated in this phase.
- No cloud deployment, connector write, or paid resource creation was performed.
- Source refresh is not a substitute for local artifact validation.
