# GHC infrastructure and public-interest pilot

Status date: 18 November 2026, Pacific/Auckland. Prepared by Aurenna Quill under Hamish's direction.

This note connects the public evidence utilities to the wider GHC engineering programme. It distinguishes code that a reviewer can run from private prototype reports and proposed deployment work. It is not a production-readiness certificate or a statement of government endorsement.

## What this branch provides

The branch contains dependency-free JavaScript utilities, synthetic examples, a bounded release-integrity verifier and its tests. `npm run check` is the reproducible entry point. The seven historical payloads in `RELEASE-MANIFEST.json` remain frozen. The new [Receipt Journey Lab](RECEIPT-JOURNEY.md) is a local interactive teaching example with five authored scenarios; it makes no network requests and performs no real operation.

The wider Nexus service, model runtime, private records, credentials, host installation and complete orchestration infrastructure are not packaged here. A reader who clones this branch does not receive the private GHC deployment.

## Architecture and responsibilities

| Layer | Intended responsibility | Evidence needed before broader deployment |
| --- | --- | --- |
| Human governance | Select the task, permitted effects, resource scope and review criteria | Current permission bound to the actual action and a named accountable owner |
| CLI and interfaces | Produce structured requests and readable outcomes | Versioned command/schema contract, exact input handling and bounded errors |
| Nexus broker | Mediate tools, files, operation identities and receipts | Authenticated route, operation-specific authority, fresh admission and supported reconciliation |
| Sentinel orchestration | Join a selected model, role context, private records and bounded tools | Exact model/provider/runtime binding, evaluation results, isolation and stop behavior |
| Docker workload | Package a reproducible application environment | Image digest, reviewed entry point, effective resource limits and persistence configuration |
| Kubernetes deployment | Schedule and manage declared workloads | Cluster identity, host/failure domains, RBAC, storage, resource policy and restore evidence |
| Evidence and recovery | Reconstruct a coherent state after interruption | Complete-set manifests, raw-byte identity, actual outcome custody and explicit unknowns |

These responsibilities should be connected through stable interfaces. A model's output is a proposal until the broker admits an authorized action. Container creation is a packaging result. A healthy endpoint is an availability observation. A saved result is a storage observation. Recipient acknowledgment is a separate delivery result.

## Dated prototype progress

Private records inspected for the 15–18 November review report bounded runtime checks, exact shared-file readbacks, a portable group archive, receipt-lookup prototypes, source-level IDE integration, and recovery improvements. Those records also retain failures and unestablished outcomes. Their aggregate findings can guide the next engineering step, but a public reviewer cannot reproduce the private deployment from this branch.

The reviewed pilot records describe two distinct Gemma-backed profiles completing 12 model calls and six bounded local tool effects in total, followed by stopping both GPU jobs. This was a small integration pilot using existing model weights. It does not establish a newly trained GHC foundation model, sustained service, full-context performance or a general benchmark advantage.

The recovery records report 51 distinct conditions across 137 handler evaluations. The larger number is repeated evaluation activity, not 137 independent conditions. Native hook trust and dispatch acceptance were still pending at the inspected checkpoint. A complete-set amendment addressed the problem of separately valid records from different generations being combined after interruption.

Docker and Kubernetes evidence needs more careful consolidation. One host's Docker availability does not establish another host's capability. A retained-app report is not the same as a verified restore receipt. A proposed three-control-plane cluster is not proof of independent physical failure domains. The selected shared follow-up folder did not contain a complete current deployment capsule at this review, so this note does not assert production Kubernetes readiness.

These are attributed private findings, separate from the checks a reader can execute in this public release. No raw private chat, operational credential, local deployment path or live authority token is included.

## The next integration improvements

First, reconcile schemas before adding features. The current source review identified a five-key SDK limits record being rejected by a four-key adapter contract. A versioned translation or agreed schema should resolve the difference explicitly. Silently dropping a limit would conceal a material change in meaning. Acceptance should compare the exact serialized input, selected adapter version and complete expected output.

Second, separate desired configuration from observed behavior. Docker's documentation explains that containers have no resource constraints by default; limits must be configured. Record the actual effective memory, CPU, process and storage limits at the worker rather than relying solely on a planned configuration or a host-wide memory reading. [Docker documentation](https://docs.docker.com/engine/containers/resource_constraints/)

Third, design operation identity above the scheduler. Kubernetes warns that a program may sometimes start twice even when parallelism and completions are both one and restartPolicy is Never. An external side effect therefore needs an application-level claim and a supported reconciliation route. An unknown submission cannot safely be treated as a failed action that is automatically repeated. [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)

Fourth, make recovery a property of a complete set. The proposed checkpoint includes a common generation, exact state digest, operation identities and referenced outcome records. Recovery should preserve known effects and unresolved actions, then obtain fresh authority for any continuation. Restoring a goal is not renewing a permit.

Fifth, measure a single complete workflow. Choose one synthetic, low-impact task, freeze its expectations, observe the model and broker boundaries, collect the tool outcome, verify persistence and close the worker. A later read should reconstruct that exact result without re-entering the operation. This is a proposed acceptance milestone, not a completed production result.

## Trinity Mandala as a practical design framework

GMUT can contribute disciplined hypothesis formation: define quantities, distinguish a visualization from an experiment, compare with established baselines and name a result that would falsify the proposed explanation. The present software does not validate a physical unification theory.

THOS can contribute engineering discipline: resource budgets, explicit state, narrow interfaces, recoverable records, observable failure and clear ownership. Its public contribution should be useful even to people who do not adopt the wider GHC vocabulary.

Freed ID and the rights/governance pillar can contribute provenance, consent, choice, revocation and accountability requirements. Project names and persistent records can support continuity of a collaboration. They do not establish legal identity, consciousness, cultural authority or an entitlement to other people's data.

The 7 November onboarding document and continuity manifest are historical snapshots. Their participant statuses and quota guard must not be interpreted as a fresh operational instruction or a current permission grant. A later task needs current human scope and applicable host controls.

## A useful New Zealand pilot

New Zealand's public-service AI work programme includes shared tools, assurance, trial environments and staff capability. That suggests a practical contribution: a small, reusable evidence and review workflow that complements existing programmes. GHC should demonstrate a measurable improvement on a narrow task before proposing national infrastructure. [Public Service AI Work Programme](https://www.digital.govt.nz/standards-and-guidance/technology-and-architecture/artificial-intelligence/public-service-ai-work-programme)

A suitable first pilot would help a human compare published service documents and prepare a source-linked change summary. Inputs would be public or synthetic. The tool would not decide a person's eligibility or submit an application. A reviewer would check source accuracy, omissions, accessibility, correction effort and time saved against a manual baseline. A release would require a named owner, an error-reporting route and a documented fallback to the original source.

The Public Service AI Framework emphasizes human-centered outcomes, transparency, accountability and security. The proposed GHC pilot should express these as observable requirements: every material statement links to its source, uncertainty remains visible, a person accepts the result, and the system can explain its records. This is a proposed alignment, not a claim of compliance certification. [Public Service AI Framework](https://www.digital.govt.nz/standards-and-guidance/technology-and-architecture/artificial-intelligence/public-service-artificial-intelligence-framework)

Engagement with Māori and affected communities belongs in the design and governance of any relevant pilot. Local hosting alone does not establish Māori data sovereignty. Decisions about collection, control, access, benefit and reuse need the relevant people and authorities involved. Government guidance directs agencies toward Māori data governance resources and stresses human oversight and understanding where providers handle data. [Māori, Pacific Peoples, Ethnic Communities and GenAI](https://standards.digital.govt.nz/docref/public-service-gen-ai-guidance-maori-pacific-peoples-and-ethnic-communities/2025/en/)

## What Makarewa could contribute

Southland District Council records consents for Datagrid's Makarewa development, including up to 240 MW of IT capacity, six data halls, a substation and telecommunications infrastructure. This is a consented design scope, not a measurement of currently available compute. [Council project record](https://www.southlanddc.govt.nz/home-and-property/resource-consents/proposals-of-public-interest/)

Datagrid's announcement dated 18 August 2026 says horizontal works had started, with HEB Construction undertaking access, road and site-platform work. The announcement expected the foundation platform, cable landing station and substation platform by year end. That statement does not provide a confirmed date when GHC could rent a particular GPU or deploy a service. [Construction announcement](https://www.datagrid.nz/pr1-rc/horizontal-works-begin-on-datagrids-ai-data-centre-campus-in-makarewa)

If suitable services become commercially available, the project could offer a regional route to hosted workloads, connectivity, partnerships and skills development. The next useful inquiry would ask about service commencement, tenant or reseller options, small-project access, actual GPU/runtime offerings, storage location, access controls, support, connectivity and price. No such arrangement is established in this branch.

Nearby infrastructure can reduce some practical barriers, but geographic proximity alone does not provide capacity or permission. GHC can make progress now by building portable, well-measured software that can be evaluated on a small existing host and later moved to an appropriate provider.

## Measurable next milestones

1. **Public reproducibility:** obtain a report from an independent user of this branch, with exact commit, runtime, observed output and a concrete use case.
2. **Compatibility:** publish a minimal synthetic example of the limits-schema disagreement and an explicitly versioned resolution once reviewed.
3. **Integration custody:** assemble a sanitized deployment capsule with exact image/runtime versions, effective limits, storage and restore results, and retained failures.
4. **One complete acceptance flow:** establish the distinct execution, effect, storage, closure and acknowledgment observations for a selected low-impact task.
5. **Community pilot:** agree a useful problem, baseline, evaluation method, accountable owner and actual participants before making public-benefit claims.

No government outreach, procurement, service deployment, paid inference or programme application is performed by this documentation update.
