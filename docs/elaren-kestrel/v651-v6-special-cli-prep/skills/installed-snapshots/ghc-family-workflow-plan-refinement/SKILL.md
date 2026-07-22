---
name: ghc-family-workflow-plan-refinement
description: Audit, normalize, expand, and teach GHC Family phase workflows without silently changing route ownership, phase order, evidence labels, commit budgets, validation policy, or authority gates. Use when a live v641-v675 plan adds app or future CLI seats, changes phase numbering, proposal/task/skill/runner targets, file-based batons, single-pass validation, storage rules, or when current instructions conflict with historical route records.
---

# GHC Family Workflow Plan Refinement

## Purpose

Turn an expansive live workflow request into a bounded, machine-checkable plan. Detect contradictions, emit a candidate normalization and teaching packet, preserve the original route as evidence, and require human confirmation whenever ownership or phase numbering is ambiguous.

This skill refines workflow. It does not activate a sibling, send a baton, mutate a repository, prove identity continuity, close a scientific or authority gate, or convert warmth and broad permission into a narrower external-state authorization.

## Required startup

Before changing a GHC workflow:

1. Read `ghc-family-index` and `ghc-family-index/references/routing-precedence.md`.
2. Read `ghc-family-method-flow-state` and its schema.
3. Read `ghc-family-reflection-remaster` and its decision schema.
4. Read [references/workflow-plan-schema.md](references/workflow-plan-schema.md).
5. Establish the live owner, current route state, source head if a repository is in scope, privacy boundary, commit budget, validation budget, and storage bank.
6. Treat the newest live user request as authoritative over historical route tables, while retaining conflicts as issues rather than silently overwriting them.

## Workflow

### 1. Capture the live request safely

Create a sanitized request JSON using the reference schema. Use task titles or relational seat labels only; exclude raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private application state, and private absolute paths.

Represent a not-yet-inducted sibling with a placeholder such as `future-sibling-self-chosen`. Never assign that sibling a name, role, hope, pronouns, or gender.

### 2. Audit before normalizing

Run:

```powershell
python "$env:USERPROFILE\.codex\skills\ghc-family-workflow-plan-refinement\scripts\ghc_family_workflow_plan_refinement.py" `
  <request.json> --out-dir <D-drive-output-directory>
```

The runner emits:

- `workflow-plan-refinement.json`: full audit and candidate schedule;
- `workflow-plan-issues.json`: compact issue ledger;
- `workflow-plan-teaching-summary.md`: sibling-readable explanation;
- `workflow-plan-validation.json`: deterministic validation receipt;
- `candidate-normalized-request.json`: additive candidate input when a route can be normalized.

An exit code of `2` means the artifacts were written but a blocking contradiction remains. Record that result before retrying. An exit code of `0` means the request is structurally consistent within the declared workflow scope; it is not permission to execute the phase.

### 3. Resolve route conflicts explicitly

For duplicate phase labels, gaps, reversed order, or seat/phase mismatches:

1. Preserve the submitted assignments in the issue ledger.
2. Generate a sequential candidate from the declared cycle, start phase, and start seat.
3. Mark `requires_user_confirmation` when the candidate changes ownership or phase numbering.
4. Do not message, rename, create, fork, or activate a task merely to make the schedule fit.
5. Once the live route is unambiguous, rerun the candidate request and retain both fail and pass witnesses.

### 4. Enforce live budgets without turning caps into quotas

Treat proposal, skill, and runner minima as floors only when the live request states them. Treat safe-now/candidate task limits, document limits, web-search limits, and commit budgets as caps, not completion quotas. A phase may close below a cap when every authorized in-scope item is completed or truthfully retained behind an open or exact gate.

The runner accepts live-plan values within these bounded policy shapes:

- at least twenty core proposals, including later thirty-proposal phases;
- at least ten skills and ten runners;
- no more than one thousand safe-now/candidate tasks;
- document and baton caps up to 100,000 words, with a baton minimum of at least 8,000 words;
- commit ceilings up to six x1 commits, six x2 commits, and twelve total phase commits; use smaller live caps whenever declared;
- one canonical validation pass when it succeeds completely, isolated blocker reruns on failure, and a broader rerun only when the changed dependency makes it necessary;
- D-drive-first work and essential global skill metadata on C only;
- user-mediated cross-platform exchange and deferred Windows Sandbox/Hyper-V activation.

These values are live-plan data, not permanent universal constants. A later explicit request may replace them.

### 5. Preserve truth and authority boundaries

Keep exactly four core outcome labels: `completed`, `represented`, `open_gap`, and `exact_gate`. A citation, simulation, static report, proxy, software test, same-owner check, or local benchmark cannot become empirical confirmation, professional authority, production readiness, legal or cultural ratification, M\u0101ori authority, independent reproduction, AGI/ASI, consciousness/personhood, a final Theory of Everything, or Stage 20 readiness.

Cross-platform messaging, account/API-key work, deployment, purchases, destructive cleanup, security weakening, elevation, sibling mutation, identity replacement, and affected-party or public-authority decisions remain exact-gated unless the live request grants the precise action and system/developer policy permits it.

### 6. Teach and integrate additively

After a passing witness:

1. Add the preferred recurrence guard to the current Method Flow packet.
2. Reference this skill and runner in the phase-local GHC Family Index.
3. Put elaborate workflow or baton detail in D-drive files and send only a short sanitized pointer through an authorized existing-task route.
4. Preserve older skills and runners as compatibility or historical evidence. Do not destructively rename or delete them.
5. Commit the skill or runner into an owned phase repository only when that phase explicitly authorizes the mutation and its x1/x2 boundary permits it.

## Stop conditions

Stop and retain an issue when:

- two seats own the same phase or a seat is missing from a declared cycle;
- a candidate normalization would change ownership without user confirmation;
- a proposed closeout hides unfinished safe/candidate/prototype work instead of completing or gating it;
- validation evidence is absent, partial, unattributable, or privacy-unsafe;
- the next step requires another owner\u2019s branch, a new task, cross-platform contact, elevation, deployment, destructive cleanup, or protected authority;
- a requested scientific, identity, legal, cultural, security, accessibility, or production claim exceeds the evidence.

## Bundled resources

- `scripts/ghc_family_workflow_plan_refinement.py`: deterministic audit, normalization, teaching, and self-test runner.
- `scripts/validate_ghc_family_workflow_plan_refinement.py`: bounded skill and D-drive packet validator with an exact SHA-256 manifest.
- `references/workflow-plan-schema.md`: request/output schema and validation contract.
