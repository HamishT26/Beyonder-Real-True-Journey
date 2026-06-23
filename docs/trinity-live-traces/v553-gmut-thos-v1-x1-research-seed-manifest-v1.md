# v553-gmut-thos-v1-x1 Research Seed Manifest

Rows: `25`
Minimum reflections required: `25`

## 1. OpenAI Codex Remote Connections

- Query: OpenAI Codex remote connections
- Pillar: THOS
- Source: https://developers.openai.com/codex/remote-connections
- Phase reflection: Remote/local handoff should stay artifact-backed and reversible.
- Runner implication: Keep handoff receipts small and route remote work through explicit branch/current-state anchors.

## 2. OpenAI Codex Skills

- Query: OpenAI Codex skills
- Pillar: THOS
- Source: https://developers.openai.com/codex/skills
- Phase reflection: Local skills are the right home for startup, compact-pause, and closeout operating rules.
- Runner implication: Validate edited skills before publishing phase truth.

## 3. OpenAI Codex Slash Commands

- Query: OpenAI Codex slash commands
- Pillar: THOS
- Source: https://developers.openai.com/codex/cli/slash-commands
- Phase reflection: Command surfaces should be explicit and recoverable rather than hidden in chat memory.
- Runner implication: Prefer named runner and command entrypoints for repeatable phase work.

## 4. OpenAI Codex Worktrees

- Query: OpenAI Codex worktrees
- Pillar: THOS
- Source: https://developers.openai.com/codex/app/worktrees
- Phase reflection: Worktree isolation supports omega-mini publication and full-tools support separation.
- Runner implication: Keep sanitized publication worktree and richer support lane distinct.

## 5. W3C DID 1.1

- Query: W3C DID Core
- Pillar: Freed ID / CBR
- Source: https://www.w3.org/TR/did-1.1/
- Phase reflection: Identifier control needs verifiable boundaries and controller separation.
- Runner implication: Keep identity work as design/research until exact approval and compliance review.

## 6. W3C VC Data Model 2.0

- Query: W3C Verifiable Credentials 2.0
- Pillar: Freed ID / CBR
- Source: https://www.w3.org/TR/vc-data-model-2.0/
- Phase reflection: Credential claims need issuer, holder, subject, and proof semantics separated.
- Runner implication: Model CBR claims as schema candidates, not as proof closure.

## 7. W3C VC Overview

- Query: W3C Verifiable Credentials overview
- Pillar: Freed ID / CBR
- Source: https://www.w3.org/TR/vc-overview/
- Phase reflection: Reader-facing identity explanations benefit from a plain overview layer.
- Runner implication: Create compact primer artifacts before any implementation-heavy identity lane.

## 8. W3C VC Data Integrity

- Query: W3C Data Integrity
- Pillar: Freed ID / CBR
- Source: https://www.w3.org/TR/vc-data-integrity/
- Phase reflection: Integrity proofs are protocol details that must not be hand-waved.
- Runner implication: Queue cryptographic binding work behind exact approval.

## 9. NIST Digital Identity Guidelines

- Query: NIST SP 800-63-4
- Pillar: Freed ID / CBR
- Source: https://pages.nist.gov/800-63-4/
- Phase reflection: Identity assurance, authentication, and federation should be treated as separate risk lanes.
- Runner implication: Add assurance-level vocabulary to candidate packets.

## 10. OpenID Connect Core 1.0

- Query: OpenID Connect Core
- Pillar: Freed ID / CBR
- Source: https://openid.net/specs/openid-connect-core-1_0.html
- Phase reflection: Authentication claims and tokens need standard protocol mapping.
- Runner implication: Keep any account/auth changes exact-approval only.

## 11. IETF RFC 6749

- Query: OAuth 2.0 RFC 6749
- Pillar: Freed ID / CBR
- Source: https://www.rfc-editor.org/rfc/rfc6749
- Phase reflection: Authorization grants are a different lane from identity proof.
- Runner implication: Separate authz design packets from identity/canon packets.

## 12. IETF RFC 7519

- Query: JWT RFC 7519
- Pillar: Freed ID / CBR
- Source: https://www.rfc-editor.org/rfc/rfc7519
- Phase reflection: Token claims are compact but easy to over-trust.
- Runner implication: Queue token validation and key handling as exact-approval implementation work.

## 13. NIST AI Risk Management Framework

- Query: NIST AI RMF
- Pillar: THOS
- Source: https://www.nist.gov/itl/ai-risk-management-framework
- Phase reflection: AI orchestration should keep govern/map/measure/manage loops visible.
- Runner implication: Add risk-loop labels to approval packets and closeouts.

## 14. Node.js child_process

- Query: Node child_process
- Pillar: THOS
- Source: https://nodejs.org/api/child_process.html
- Phase reflection: Runner orchestration needs explicit child process and stream boundaries.
- Runner implication: Prefer Node entrypoints with summarized stdout/stderr counts.

## 15. Python subprocess

- Query: Python subprocess
- Pillar: THOS
- Source: https://docs.python.org/3/library/subprocess.html
- Phase reflection: Python runners should preserve argument boundaries and avoid shell interpolation.
- Runner implication: Keep Python helpers for validation/gate work where already established.

## 16. Git Worktree Documentation

- Query: Git worktree
- Pillar: THOS
- Source: https://git-scm.com/docs/git-worktree
- Phase reflection: Multiple lanes need clean worktree state rather than stateful directory reuse.
- Runner implication: Check branch/worktree truth before phase publication.

## 17. GitHub Actions Workflow Syntax

- Query: GitHub Actions workflow syntax
- Pillar: THOS
- Source: https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions
- Phase reflection: CI ideas should stay candidate until repo workflow mutation is approved.
- Runner implication: Classify workflow edits as exact-approval unless purely local docs.

## 18. OpenTelemetry Specification

- Query: OpenTelemetry specification
- Pillar: THOS
- Source: https://opentelemetry.io/docs/specs/otel/
- Phase reflection: Long-running orchestration benefits from structured traces, spans, and attributes.
- Runner implication: Propose local status schema improvements before telemetry installation.

## 19. Kubernetes Controller Concepts

- Query: Kubernetes controllers
- Pillar: THOS
- Source: https://kubernetes.io/docs/concepts/architecture/controller/
- Phase reflection: Controller reconciliation is a strong analogy for updater and cadence runners.
- Runner implication: Design runners as reconcile loops with observed, desired, and gap states.

## 20. Playwright Locators

- Query: Playwright locators
- Pillar: THOS
- Source: https://playwright.dev/docs/locators
- Phase reflection: Browser automation must prefer robust locators and auto-waiting.
- Runner implication: If browser handoff resumes, keep it locator-driven and receipt-backed.

## 21. PowerShell Start-Job

- Query: PowerShell jobs
- Pillar: THOS
- Source: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/start-job?view=powershell-7.6
- Phase reflection: Background Windows tasks need explicit lifecycle and harvest semantics.
- Runner implication: Use detached/background runner receipts rather than terminal babysitting.

## 22. Semantic Scholar API

- Query: Semantic Scholar API
- Pillar: GMUT
- Source: https://api.semanticscholar.org/api-docs/
- Phase reflection: Scholar APIs can support bounded literature discovery.
- Runner implication: Queue API harvesters as candidate until rate limits and provenance are validated.

## 23. Crossref REST API

- Query: Crossref REST API
- Pillar: GMUT
- Source: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Phase reflection: DOI metadata can help canonicalize research ledgers.
- Runner implication: Add citation normalization as a safe skill/runner idea.

## 24. OpenAlex API

- Query: OpenAlex API
- Pillar: GMUT
- Source: https://developers.openalex.org/api-reference/introduction
- Phase reflection: Open bibliographic graphs can broaden GMUT literature maps.
- Runner implication: Keep imported metadata compact and source-labelled.

## 25. arXiv API User Manual

- Query: arXiv API manual
- Pillar: GMUT
- Source: https://info.arxiv.org/help/api/user-manual.html
- Phase reflection: Physics paper discovery should be queryable and reproducible.
- Runner implication: Use arXiv manifests for GMUT exploratory queues without claiming closure.

## Boundary

Status-only research seed. No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, deployment closure, account mutation, or API-key creation are published.
