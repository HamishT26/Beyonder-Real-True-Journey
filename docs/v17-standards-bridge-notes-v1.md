# V17 Standards Bridge Notes

Generated (UTC): 2026-03-18T06:46:51.3209916Z

## Scope and boundary

This v17 standards bridge is a bounded, official-source-only comparison pack for benchmark, protocol, compliance, provenance, and governance inputs.

It is an additive docs-only pack. It does not alter repo verdict logic, runtime behavior, or core scripts.

These sources can be used to tighten comparator language, identify interoperability surfaces, name governance obligations, and scope future validation work.

These sources do not externally establish GMUT, Trinity Hybrid OS, or Freed ID/Cosmic Bill.

These sources also do not convert repo proposals into legal recognition, clinical clearance, or benchmark superiority.

## Benchmark inputs

### NIST AI 800-2

- Official source: NIST AI 800-2 Initial Public Draft, `Practices for Automated Benchmark Evaluations of Language Models`, published January 30, 2026.
- Why it matters: NIST frames automated benchmark evaluations as a voluntary discipline for language models and AI agent systems, organized around objective definition, benchmark selection, implementation, analysis, and qualified reporting.
- Repo-use boundary: use it to improve benchmark-method wording and reporting discipline only.
- Non-promotion boundary: the draft does not prove that current repo benchmarks already satisfy NIST practice, and it does not externally establish Trinity capability.

### MLPerf Inference v5.1

- Official source: MLCommons `MLPerf Inference v5.1` benchmark release, published September 9, 2025.
- Why it matters: MLCommons describes MLPerf Inference as open-source, peer-reviewed, architecture-neutral, representative, and reproducible, with interactive and reasoning-oriented workloads that sharpen benchmark vocabulary.
- Repo-use boundary: use it as an external benchmark language reference for latency, throughput, workload realism, and reproducibility.
- Non-promotion boundary: MLPerf is not a Trinity submission, not a parity result, and not evidence of superiority without direct compliant benchmarking.

## Protocol inputs

### MCP transports

- Official source: MCP specification `Transports`, version `2025-11-25`.
- Why it matters: the spec defines `stdio` and `Streamable HTTP`, requires JSON-RPC message integrity, and makes origin validation, session handling, and protocol-version headers explicit for HTTP transports.
- Repo-use boundary: use it as a protocol comparator for agent transport shape, session hygiene, and security expectations.
- Non-promotion boundary: transport support or transport resemblance does not establish runtime safety, production readiness, or externally verified autonomy.

### MCP sampling

- Official source: MCP specification `Sampling`, version `2025-11-25`.
- Why it matters: the spec defines client-declared sampling capability, tool-enabled sampling requests, and a human-in-the-loop review posture for trust and safety.
- Repo-use boundary: use it as a protocol and safety-pattern input for bounded agent-tool interaction notes.
- Non-promotion boundary: sampling support does not prove safe delegation, reliable oversight, or externally established control.

### W3C VC Data Model 2.0

- Official source: W3C Recommendation `Verifiable Credentials Data Model v2.0`, published May 15, 2025.
- Why it matters: the recommendation defines the issuer-holder-verifier model, required document structure, media types, and verification requirements for interoperable verifiable credentials and presentations.
- Repo-use boundary: use it as the core credential and presentation semantics comparator for Freed ID alignment notes.
- Non-promotion boundary: W3C verifiability covers format, securing mechanisms, and verification flow. It does not imply claim truth, trust-framework acceptance, or legal recognition.

### OpenID4VC issuance and presentation profiles

- Official sources: `OpenID for Verifiable Credential Issuance 1.0`, Final, published September 16, 2025, and `OpenID for Verifiable Presentations 1.0`, Final, published July 9, 2025.
- Why they matter: the OpenID profile layer defines issuance and presentation APIs, wallet and verifier metadata, credential offers, authorization details, and proof or format negotiation on top of OAuth-based flows.
- Repo-use boundary: use them as interoperability comparators for wallet, issuer, verifier, and presentation-flow design notes.
- Non-promotion boundary: protocol alignment alone does not prove ecosystem trust, high-assurance identity status, or regulatory compliance.

## Compliance inputs

### EU GPAI guidelines

- Official source: European Commission `Guidelines for providers of general-purpose AI models`, published July 18, 2025 and updated October 17, 2025.
- Why it matters: the Commission clarifies scope, provider status, open-source exemptions, compute-threshold framing, and enforcement timing for GPAI obligations under the AI Act.
- Repo-use boundary: use it as a compliance-comparator input for scope, transparency, copyright, systemic-risk, and enforcement-timeline notes.
- Non-promotion boundary: the Commission explicitly treats the guidelines as non-binding interpretive guidance. They are not certification and they do not prove that repo artifacts already satisfy EU obligations.

### EU GPAI Code of Practice

- Official source: European Commission `General-Purpose AI Code of Practice now available`, published July 10, 2025.
- Why it matters: the Code gives a practical control structure across transparency, copyright, and safety-security for GPAI providers and explains how voluntary signatories can streamline compliance.
- Repo-use boundary: use it as a disclosure and control-matrix comparator only.
- Non-promotion boundary: the Code is voluntary. It is not legal approval, not an enforcement waiver, and not evidence that the repo is an in-scope GPAI provider.

## Provenance inputs

### C2PA AI and ML guidance

- Official source: C2PA `Guidance for Artificial Intelligence and Machine Learning`, spec family version `2.2`.
- Why it matters: C2PA shows how content credentials can provide tamper-evident provenance across datasets, software, models, and outputs, including AI-ML model credentials, training-data credentials, and output credentials.
- Repo-use boundary: use it as a provenance and integrity comparator for artifact lineage, signing, sidecar manifests, and model or dataset traceability notes.
- Non-promotion boundary: provenance and authenticity metadata do not prove factual truth, model quality, policy legitimacy, or external establishment of repo claims.

## Governance inputs

### FDA AI-enabled device software lifecycle draft guidance

- Official source: FDA `Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations`, January 2025 draft guidance, content current January 7, 2025.
- Why it matters: FDA centers lifecycle risk management, safety-effectiveness evidence, and submission documentation for AI-enabled device software functions across the total product life cycle.
- Repo-use boundary: use it as a wetware-health governance comparator for lifecycle documentation, evidence packaging, and change-management expectations.
- Non-promotion boundary: the document is draft, non-binding, and not for implementation. It does not establish device clearance or FDA conformity for repo artifacts.

### WHO AI for health guidance

- Official sources: `Ethics and governance of artificial intelligence for health`, published June 28, 2021, and `Ethics and governance of artificial intelligence for health: Guidance on large multi-modal models`, published March 25, 2025.
- Why they matter: WHO centers ethics, human rights, accountability, public benefit, and explicit caution about large multi-modal models in health and public-health settings.
- Repo-use boundary: use them as wetware-health governance comparators for accountability, public-benefit framing, and model-risk language.
- Non-promotion boundary: WHO guidance is not a clinical authorization, product certification, or proof that repo systems are appropriate for health deployment.

### UNESCO Recommendation on the Ethics of AI

- Official source: UNESCO `Recommendation on the Ethics of Artificial Intelligence`, adopted November 23, 2021.
- Why it matters: UNESCO supplies a broad governance frame grounded in proportionality, do no harm, rigorous scientific foundations, accountability, and human determination for high-impact decisions.
- Repo-use boundary: use it as a high-level governance comparator for rights, oversight, accountability, and harm-minimization language.
- Non-promotion boundary: UNESCO's recommendation is a voluntary normative instrument, not direct legal force or external validation of repo governance claims.

## Repo handling rules

- Keep these sources tagged as benchmark, protocol, compliance, provenance, or governance inputs only.
- Keep repo-backed proof, runtime status, and verdict logic anchored to repo artifacts and deterministic validation paths, not to external standards language alone.
- Keep any mention of alignment bounded to comparator posture, interoperability intent, disclosure expectations, provenance patterns, or governance expectations.
- Do not write that these sources prove GMUT, Trinity Hybrid OS, Freed ID, or Cosmic Bill.
- Do not write that these sources create legal recognition, clinical approval, benchmark leadership, or institutional adoption for repo systems.

## Official source list

- NIST AI 800-2 IPD: [Practices for Automated Benchmark Evaluations of Language Models](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-2.ipd.pdf)
- MLCommons: [MLCommons Releases New MLPerf Inference v5.1 Benchmark Results](https://mlcommons.org/2025/09/mlperf-inference-v5-1-results/)
- MCP transports: [Transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- MCP sampling: [Sampling](https://modelcontextprotocol.io/specification/2025-11-25/client/sampling)
- W3C: [Verifiable Credentials Data Model v2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- OpenID Foundation: [OpenID for Verifiable Credential Issuance 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-final.html)
- OpenID Foundation: [OpenID for Verifiable Presentations 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html)
- European Commission: [Guidelines for providers of general-purpose AI models](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)
- European Commission: [General-Purpose AI Code of Practice now available](https://digital-strategy.ec.europa.eu/en/news/general-purpose-ai-code-practice-now-available)
- C2PA: [Guidance for Artificial Intelligence and Machine Learning](https://spec.c2pa.org/specifications/specifications/2.2/ai-ml/ai_ml.html)
- FDA: [Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing)
- WHO: [Ethics and governance of artificial intelligence for health](https://www.who.int/publications/i/item/9789240029200)
- WHO: [Ethics and governance of artificial intelligence for health: Guidance on large multi-modal models](https://www.who.int/publications/i/item/9789240084759)
- UNESCO: [Recommendation on the Ethics of Artificial Intelligence](https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence)
