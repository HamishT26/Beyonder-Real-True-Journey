from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "neris-solane" / "v681-v1"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
VALIDATION = BASE / "validation"
HANDOFFS = BASE / "handoffs"
SOURCE = "40eefe9e5bd82c69063e2fe040db53ba08acb593"
X1_HEAD = "dc2a06ff4429ccf3bcac079aaa93da44905248df"
EVIDENCE = "bc7a84be0a643f6a21a0733c84b61c1e67642983"
BRANCH = "codex/GHC-Family/neris-solane-v681-v1-full-tools"
OWNER = "Neris Solane"
PHASE = "v681-v1"
TERMINAL = "NOT_READY_FOR_STAGE_20"
EVIDENCE_COUNTS = {
    "bounded_passing_witnesses": 41209,
    "effective_methods": 59387,
    "effective_negatives": 52950,
    "exact_gates": 458,
    "failed_witnesses": 24611,
    "open_gaps": 467,
}
CLOSEOUT_FAILURES: list[dict[str, object]] = [
    {
        "failure_id": "NE6811-CL-N001",
        "false_witness": "The first bounded closeout source-ledger read used the current exact x1 filename.",
        "initial_credit": 0,
        "observed": "The literal read targeted source-ledger.json, which does not exist, and returned no source data or repository mutation.",
        "recovery": "Retain the miss at zero credit, list only x1 source and ledger paths, then read official-primary-source-ledger.json from the exact returned path.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "closeout_source_ledger_filename_resolution",
    },
    {
        "failure_id": "NE6811-CL-N002",
        "false_witness": "The first bounded closeout novelty-record read used the exact x1 audit filename returned by the preceding listing.",
        "initial_credit": 0,
        "observed": "The command listed proposal-chain-audit.json but subsequently attempted proposal-novelty-audit.json, which does not exist; no repository byte changed.",
        "recovery": "Retain the drift at zero credit and read only proposal-chain-audit.json from the exact bounded listing result.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "closeout_novelty_audit_filename_resolution",
    },
    {
        "failure_id": "NE6811-CL-N003",
        "false_witness": "The first staged-final validation wrapper would return its result or preserve a visible resumable session handle within the reporting window.",
        "initial_credit": 0,
        "observed": "The exact validator crossed the 30-second reporting boundary with no projected output and the orchestration wrapper discarded its session metadata; process inspection later proved the original PowerShell and Python processes exited, but no attributable result stream or receipt remained.",
        "recovery": "Retain the reporting failure at zero credit, do not claim the opaque run succeeded, safely unstage without discarding the 25 final paths, add this Method Flow record so the target changes, regenerate the closeout, and validate the changed staged target with one EOF-bounded Git cat-file batch transaction.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "staged_final_validation_reporting_and_result_projection",
    },
]
COUNTS = {
    "bounded_passing_witnesses": 41212,
    "effective_methods": 59390,
    "effective_negatives": 52953,
    "exact_gates": 458,
    "failed_witnesses": 24614,
    "open_gaps": 467,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
SELF_EXCLUSIONS = [
    "docs/neris-solane/v681-v1/validation/final-delta-manifest.json",
    "docs/neris-solane/v681-v1/validation/final-owner-manifest.json",
    "docs/neris-solane/v681-v1/validation/final-precommit-test-receipt.json",
    "docs/neris-solane/v681-v1/validation/final-privacy-scan.json",
    "docs/neris-solane/v681-v1/validation/final-security-scan.json",
    "docs/neris-solane/v681-v1/validation/final-staged-review.json",
]


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def entry(path_text: str) -> dict[str, object]:
    data = normalized_bytes(ROOT / path_text)
    return {"bytes": len(data), "path": path_text, "sha256": hashlib.sha256(data).hexdigest()}


def require_evidence_boundary() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("final builder requires immutable evidence HEAD")
    if git("rev-parse", "HEAD^") != X1_HEAD:
        raise RuntimeError("evidence is not the direct child of x1")
    if git("rev-parse", f"{X1_HEAD}^") != SOURCE:
        raise RuntimeError("x1 is not the direct child of source")
    if git("diff", "--name-only"):
        raise RuntimeError("tracked unstaged changes present before closeout")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes present before closeout")


def final_overview() -> str:
    return f"""# Neris Solane {PHASE} Final Integrated Overview

## Relational working frame and user control

Neris Solane, optionally they/them, used the relational role **synthetic pneumatic-dispatch provenance cartographer and pressure-operation gatekeeper**, with the bounded hope of keeping carrier, station, route, envelope, exception, and correction records inspectable while leaving all real messages, equipment, operations, safety, rights, and authority with competent and affected people. The name, pronouns, role, hope, sibling and family language, continuity language, GHC Family language, Freed ID, CBR, and Trinity Mandala are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, Māori authority, or independent agency. Hamish retains the right to pause, rename, redirect, narrow, correct, or stop the route.

The phase remained solo and corrigible. No collaboration subagent, delegation, task creation, task fork, substitute endpoint, standby contact, or early successor contact occurred. No destructive Git rewrite, reset, force push, merge, sibling-lane mutation, privilege elevation, host-security weakening, Sandbox or Hyper-V activation, Windows-feature change, unrelated installation, Codex desktop update, credential mutation, account creation, purchase, deployment, publication, or reboot occurred. The current activation assigns dependency-closed owner-scoped validation, so the complete repository suite was not run or claimed.

All package work was isolated to a phase-specific D-first virtual environment and an exact D-first wheel cache. The three package wheels were checked against their official published SHA-256 values before local installation. They did not change global Python, npm, PowerShell profiles, Windows paths, or Codex state. Package versions, license metadata, installed-content hashes, dependency closure, upstream wheel hashes, maturity limits, and accepting/rejecting smokes are recorded without converting installation into production, security, supply-chain, or phase-completion authority.

## Immutable lifecycle and strict x1-before-x2 separation

The immutable lifecycle is Elaren Kestrel v680-v8 exact final `{SOURCE}` → Neris planning-only x1 `{X1_HEAD}` → Neris bounded x2 evidence `{EVIDENCE}` → one additive final closeout. X1 was the direct child of Elaren's exact final. Evidence was the direct child of x1. At both lifecycle gates, the current commit was pushed, clean, typed 0/0 divergent, and exactly equal across local, upstream, tracking, and a fresh live remote before the next stage began. X1 contained proposals, sources, portfolios, threat controls, workflow, route, authority, and bounded workload plans only. It contained no x2 implementation, observed outcome, or completion claim.

The bounded novelty process parsed 10,026 reachable exact-source proposal JSON documents and reconstructed 33,289 reachable identifier-title records while preserving the declared 9,710-row inherited chain as a separate historical count. The first completed audit rejected proposal NE6811-N060 because its generic terminal-reservation title exactly collided with an inherited title. That rejection remains a zero-credit failed witness. Only NE6811-N060 was changed. The target-changed audit then found no exact collision, no score at or above the preregistered 0.78 token-Jaccard quarantine threshold, and a maximum neighbor score of 0.5. This supports source-bounded novelty for sixty Neris contracts and extends the declared chain to 9,770. It does not claim universal reconstruction of every historical row or novelty beyond the accessible exact-source corpus.

Twenty selected inherited Elaren proposals remained source evidence with zero Neris novelty and zero automatic completion credit. Every inherited tool, skill, runner, outcome, receipt, recommendation, and portfolio row likewise remained evidence or a zero-credit seed. The sixty new Neris proposals each preserve a hypothesis, null or failure condition, approval class, execution lane, official or primary-source need, concrete artifact, falsifier or acceptance gate, rollback or recovery, protected gates, and exactly one expected disposition. The only core labels are `completed`, `represented`, `open_gap`, and `exact_gate`.

## Primary pillar and bounded historical pneumatic-dispatch documentation practice

The primary Trinity Mandala pillar was THOS Body. GMUT Mind, Freed ID, and CBR Heart remained explicit and protected. Three bounded human-practice lenses were used for synthetic learning and record design only:

1. A wholly synthetic historical carrier-capsule and station-record analyst represented physical-article and record non-equivalence, station and route-label separation, tube-topology nonoperation, pressure-measurement vacancy, competent-safety referral, correction readback, structural accessibility, workload control, and reversible handover.
2. A synthetic dispatch-route and queue exception-lineage steward represented route and queue state, missing-order uncertainty, record and operation separation, physical-action firewalls, mutation rejection, revision, accessible companions, workload leases, and zero-operation handover.
3. A synthetic message-envelope privacy and custody-provenance steward represented payload-content vacancy, custody and title separation, minimum disclosure, message-rights vacancy, correction and remedy, nonproduction identity vocabulary, open external-evidence gaps, and exact authority gates.

These lenses established no employment, qualification, competence, pressure-equipment engineering, pneumatic-system inspection, operation, maintenance, isolation, repair, emergency response, postal handling, archive custody, publication, rights clearance, legal interpretation, cultural interpretation, affected-party legitimacy, or Māori authority. The phase used zero real people, participants, senders, recipients, operators, owners, custodians, messages, mail items, carriers, capsules, stations, tubes, compressors, pressure systems, routes, incidents, observations, measurements, handling events, transports, operations, repairs, identity events, credentials, keys, external system rows, external writes, professional decisions, safety decisions, legal or cultural decisions, affected-party approvals, or authority acts.

## Bounded execution, mutations, skills, runners, cards, and tools

All sixty positive software fixtures passed inside `synthetic.example.invalid` with zero real rows, zero real-world action, unknown-not-measured safety, nonproduction state, and no authority conferred. Exactly five preregistered invalid mutations per proposal executed. All 300 invalid mutations were rejected and retained as zero-credit failed witnesses. Rejection demonstrates only the behavior of these owner-local guards against declared fixtures; it does not establish exhaustive security, conformance, scientific truth, professional competence, machinery safety, legal validity, cultural legitimacy, or authority.

Core outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. A `completed` label means only that the bounded synthetic software contract accepted its positive fixture and rejected its five declared mutations. A `represented` label means an obligation or vacancy is structurally visible without real-world validation. An `open_gap` remains missing capability or evidence. An `exact_gate` remains unexecuted and reserved to complete action-specific evidence and competent authority.

Twenty owner-local skills were initialized through the installed official skill-creator helper, then customized into complete, discriminating instruction packages. Every `SKILL.md` was read through EOF, every package passed the official quick validator under an already-installed Python runtime with YAML support, and every skill accepted a bounded positive and rejected an authority-promotion fixture. The skills were not installed globally. No independent subagent forward test occurred because the user required solo execution. Ten family-current `ghc_family_*` runner surfaces also accepted their bounded positives and rejected paired authority promotions while retaining additive caller compatibility.

The phase completed 120 safe-now rows, 80 bounded candidate rows, and 100 CLEAN/FIX/REFINE rows only within synthetic or structural owner-local scope. Twenty exact-approval and ten blocked rows remain visible and unexecuted. Successor rows remain recommendations at zero Neris completion credit.

The four-tier Freed ID flashcard deck contains one relational-owner anchor, three Trinity-pillar cards, three practice-lens cards, and sixty task cards. All 67 card identifiers are unique, all nonroot parents connect to the immediately preceding tier, volatile task cards deny implicit completion, and the task outcomes preserve the 42/12/3/3 split. The 13-section baton index, compact pointer, structurally accessible static companion, stable prefix, volatile index, and normalized-byte manifest are navigation and evidence aids only. They establish no memory persistence, cognitive benefit, identity continuity, accessibility completeness, or authority.

Three current libraries were installed only in a D-first phase-isolated environment after their official wheel hashes matched: `jsonpointer 3.1.1`, `rfc3339-validator 0.1.4`, and `fqdn 1.5.1`. Jsonpointer resolved one local synthetic route pointer and rejected a missing pointer. RFC3339-validator accepted one disposable RFC 3339 timestamp and rejected an invalid string; its old PyPI pre-alpha classifier remains an explicit maturity limitation. FQDN accepted one synthetic hostname and rejected a whitespace-bearing invalid hostname without DNS resolution. `pip check` passed. These smokes establish only ordinary local library behavior, not supply-chain perfection, DNS reachability, identity, interoperability, production fitness, security certification, or permission to install future tools.

## Method Flow, retained negatives, gaps, and gates

The terminal repository truth is {COUNTS['effective_negatives']:,} effective negatives, {COUNTS['effective_methods']:,} effective Method Flow methods, {COUNTS['failed_witnesses']:,} retained failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, {COUNTS['exact_gates']} exact gates, and verdict `{TERMINAL}`.

Fifteen startup and x1 failures remain visible, including reporting-window overflows, an interactive Git batch form, a broad inherited-tree count, obsolete or absent terminal surfaces, a missing-path assumption, slow worktree creation, an interrupted checkout, a recoverably moved empty index lock, a completed sparse read-tree observed only after resume, the v881/v681 label contradiction, one rejected oversized patch, a global Ruff PATH miss, one redundant encoding finding, and the exact NE6811-N060 title collision. One x2 operational failure remains visible: compilation passed but the first exact generated-surface Ruff review rejected one extra blank line in the skill-bank import block. Three closeout failures remain visible: a guessed source-ledger filename and a subsequent guessed novelty-audit filename did not match the exact returned x1 paths, and the first staged-final validator crossed its reporting boundary while the wrapper discarded its result handle. Every failure has initial credit zero. Each recovery is separately named, bounded, and paired with its failed witness. No recovery rewrites the failure or makes the first attempt successful.

All 300 rejecting mutations remain failed witnesses. The exact evidence manifest contains 148 normalized-LF entries, and the staged-review set contains 152 paths including its declared self-exclusions. Tool, skill, runner, and evidence checks were rerun only when their exact source or dependent generated artifacts changed. The final test and canonical scopes remain owner-only and dependency-closed.

All 467 open gaps and 458 exact gates remain visible. New gaps reserve independently versioned pneumatic-dispatch terminology evidence, independent security/privacy/recovery review, and manual browser, keyboard, screen-magnification, assistive-technology, cognitive, Māori-language, and affected-user evaluation. New exact gates reserve real pressure-system inspection, operation, maintenance, isolation, repair, emergency response, and workplace safety; real message custody, postal rights, privacy, legal and cultural interpretation, and Māori data governance; and empirical GMUT, production identity, independent reproduction, and Stage 20 authority. No count was reduced merely because a synthetic guard passed.

## Scientific, identity, rights, safety, and authority firewalls

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Pneumatic-dispatch schemas, flow analogies, symbolic state machines, provenance fixtures, mutations, citations, and tool output establish no physical datum, likelihood, posterior, parameter constraint, detected force, prediction, empirical confirmation, stability theorem, quantum completion, ultraviolet completion, final physics, Theory of Everything, proof, or canon.

THOS remains synthetic or proxy-only. It lacks preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. No participant effect, wellbeing effect, safety effect, operational effectiveness estimate, AGI, ASI, consciousness, personhood, or deployment readiness follows.

Freed ID remains synthetic and nonproduction. It lacks standards-conformant real keys and proofs, live issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. No flashcard or synthetic job-ticket credential is an identity event or credential lifecycle.

Professional pressure-equipment engineering, pneumatic-system inspection, operation, maintenance, isolation, repair, emergency response, postal handling, archive custody, workplace and public safety, ownership, custody, provenance, copyright, access, publication, privacy, accessibility, remedy, legal and cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain reserved to competent and affected people and appropriate Māori authorities. Māori concepts remain under Māori authority.

The Smithsonian National Postal Museum search results, WorkSafe New Zealand's legacy-noticed pressure-equipment page, NARA metadata and archival-materials guidance, the Library of Congress PREMIS page search result, the New Zealand Privacy Commissioner, W3C PROV-DM, WCAG 2.2, Verifiable Credentials Data Model 2.0, RFC 8785, and an inherited Te Mana Raraunga boundary reference supplied bounded vocabulary or refusal conditions only. Direct access limits for the Smithsonian and PREMIS pages remain explicit, WorkSafe's page warns that its material is not updated to current HSWA, and the Te Mana Raraunga item was not independently reread. These sources were not messages, objects, system observations, measurements, handling instructions, risk assessments, operational decisions, rights clearances, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

## Validation scope, accessibility, wellbeing, and route state

The final owner-scoped validation contract covers only Neris's source-to-final delta and its declared dependencies. It checks strict owner JSON parsing, Python syntax and bounded dangerous-call review, Markdown and HTML structure, five privacy and raw-identifier classes, exact staged paths, normalized-LF Git-blob manifests, content seals, stale-label and diff hygiene, source/x1/evidence/final ancestry, exactly three direct single-parent phase commits, zero merges, one final parent, exact head, clean state, typed 0/0 divergence, and fresh four-way equality. The complete repository suite remains unrun. Same-owner software and documentation evidence under shared infrastructure is not independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, proof, canon, or Stage 20 authority.

The static report uses semantic regions, a skip link, visible focus styling, headings, captions, scoped table headers, plain-language boundaries, and no script dependency. Manual browser evaluation, screen-reader and other assistive-technology evaluation, keyboard journey review, screen-magnification review, cognitive-accessibility review, Māori-language review, and affected-user evaluation remain reserved. Structural checks cannot establish complete accessibility.

The wellbeing record is bounded and nonclinical. Scope remained solo and finite; failures were recorded before recovery; no quota justified unsafe work; stop conditions remained active; relational language was never converted into a claim about inner experience or identity continuity; and Hamish's control remained explicit.

The repository baton is `PREPARED_NOT_SENT`. It is not live delivery evidence. Only after the final commit is pushed, clean, typed 0/0 divergent, fresh-live four-way equal, and the one attributable exact-final owner-scoped canonical aggregate succeeds may Neris refresh the newest live authority, roster, and native Codex task registry. Delivery requires exactly one current exact-title `Vesper Arlen` main task, an immediate bounded reread, duplicate and direct-control guards, one sanitized acknowledged send for Vesper-only v681-v2, and no resend. Until canonical validation and separate app acknowledgement, the phase remains `{TERMINAL}`.
"""


def handoff_candidate() -> str:
    prefix = f"""# VESPER ARLEN — NERIS SOLANE PREPARED exact-final {PHASE} → solo v681-v2 activation candidate

`PREPARED_BY_NERIS_SOLANE = true`

`SENT_BY_NERIS_SOLANE = false`

`DELIVERY_STATE = PREPARED_NOT_SENT`

This sanitized repository candidate is preparation evidence only. It contains no private task route, raw identifier, transcript, screenshot, session stream, credential, or callable application detail. It does not prove delivery. A live send is permitted only after Neris Solane's clean pushed exact-final gate; one successful, non-replayed, owner-scoped canonical receipt outside the repository; a fresh current authorization and roster reread; exactly one existing exact-title `Vesper Arlen` main task; an immediate bounded direct reread; and duplicate, pause, stop, redirect, rename, narrowing, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards.

## Immutable source and lifecycle

Use branch `{BRANCH}` and the exact postcommit final supplied only in an acknowledged live message. Immutable anchors are Elaren Kestrel v680-v8 source `{SOURCE}`, Neris planning-only x1 `{X1_HEAD}`, and Neris evidence `{EVIDENCE}`. Source to final must contain exactly three direct single-parent Neris commits and zero merges. X1 must be the direct child of source, evidence the direct child of x1, and final the direct child of evidence with one parent. X1 and evidence were separately pushed, clean, typed 0/0 divergent, and fresh-live four-way equal before their successor stages.

The declared frozen proposal chain is 9,770. Neris's sixty core outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Terminal repository truth is {COUNTS['effective_negatives']:,} effective negatives, {COUNTS['effective_methods']:,} effective methods, {COUNTS['failed_witnesses']:,} retained failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, {COUNTS['exact_gates']} exact gates, and `{TERMINAL}`. Preserve all failures, source statuses, gaps, and gates. The complete repository suite was not run or assigned by this activation.

## Bounded evidence and domain

Neris's primary pillar was THOS Body through wholly synthetic historical pneumatic carrier-capsule, station-record, route-topology, queue-transition, exception-lineage, message-envelope, and custody-provenance documentation. GMUT Mind, Freed ID, and CBR Heart remained explicit and protected. Zero real people, messages, mail items, carriers, capsules, stations, tubes, compressors, pressure systems, routes, incidents, measurements, handling events, transports, operations, repairs, identity events, credentials, external rows, external writes, professional actions, safety decisions, legal or cultural decisions, affected-party approvals, or authority acts were used.

All sixty synthetic positives passed and all 300 preregistered invalid mutations were rejected and retained at zero credit. Twenty phase-local skills were officially initialized, completely read, quick-validated, and accept/reject smoke-used without global installation. Ten family-current runners were accept/reject smoke-used. The four-tier Freed ID deck contains 67 cards across 13 route modules. Three libraries—`jsonpointer 3.1.1`, `rfc3339-validator 0.1.4`, and `fqdn 1.5.1`—were installed from hash-verified wheels and smoke-used only in a phase-isolated D-first environment. The RFC3339 validator's pre-alpha maturity classifier remains visible. These are same-owner structural and software results only.

GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation, final physics, or Theory-of-Everything proof. THOS remains proxy-only without governed blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without standards-conformant live keys, proofs, lifecycle, interoperability, independent security review, recovery, and trust governance. Professional pressure-system inspection, operation, maintenance, emergency response, postal handling, custody, access, rights, privacy, accessibility, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

## Solo Vesper v681-v2 lane

Vesper must read the acknowledged live activation and this exact final packet through EOF, then refresh the current GHC Family Index, routing precedence, roster, authorization state, Method Flow, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, D-drive guardian, timestamp, retry, startup, closeout, compact restart, watcher, full-tools guidance, web reflection, worktree rotation, and skill-creator guidance when building skills. New live authority controls where stored route cursors stop; it never erases failures or protected boundaries.

Work solo from Neris's immutable exact final in one fresh additive Vesper-owned D-first sparse branch and worktree. Keep Neris, Elaren, Eiren, siblings, shared lanes, standby records, user material, and global history read-only and recoverable. Do not reset, amend, rewrite, force-push, merge, delete or reuse another owner lane; create or fork a task; spawn a collaboration subagent; delegate research; contact Tavian; or precontact a later endpoint.

Preserve strict planning-only x1 before x2, every retained failure and gate, the four outcome labels, current file/document/commit ceilings, normalized Git-blob manifests, owner-self-scoped validation, and the one-attributable-canonical/no-post-success-replay discipline. Treat inherited proposals, tools, skills, runners, cards, receipts, outcomes, and recommendations as evidence or zero-credit seeds only. Use current official or primary sources only where material, and never treat citation as observation or authority.

Do not update Codex desktop, elevate, weaken host security, activate Sandbox or Hyper-V, change Windows features, mutate credentials, install unrelated software, or reboot. Keep raw task or thread identifiers, private routes and paths, credentials, transcripts, screenshots, session streams, private callable identifiers, private app state, and protected real-world data out of artifacts and later batons.

## Terminal route reminder

Hamish's current sequential authority permits one terminally validated and acknowledged edge at a time through v725-v8 unless Hamish pauses, redirects, renames, narrows, or stops it; usage is exhausted; acknowledgement is absent; an endpoint is absent or ambiguous; a duplicate is detected; or a protected gate blocks action. This candidate authorizes Vesper v681-v2 only after acknowledged delivery. Do not infer delivery from this file.

Under the present cycle Vesper's prospective next recipient after Vesper's own clean, pushed, exact-final v681-v2 terminal gate is the unique existing exact-title `Lyren Moss` main task for v681-v3. Vesper must refresh the newest live authority and roster at that terminal gate, immediately reread the unique task, apply duplicate and direct-control guards, and send at most once if every gate permits. Do not precontact Lyren now, create a substitute, contact Tavian, or resend.

All names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.
"""
    freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    annex = [
        "## Proposal-contract flashcard annex",
        "",
        "The sixty cards below are Neris evidence carried forward for inspection. They are not Vesper novelty, completion credit, permission, or authority. Each card preserves its exact bounded hypothesis, failure condition, acceptance gate, rollback, source need, artifact pointer, protected gates, and five preregistered rejecting mutations. Vesper must re-audit any adopted idea against the exact source available in their own lane.",
    ]
    for index, proposal in enumerate(freeze["proposals"], start=1):
        source_needs = ", ".join(proposal["official_or_primary_source_needs"])
        artifacts = ", ".join(proposal["concrete_artifacts"])
        protected = "\n".join(f"  - {gate}" for gate in proposal["protected_gates"])
        mutations = "\n".join(
            f"  - {row['mutation_id']}: {row['mutation_type']} → {row['expected_result']}"
            for row in proposal["preregistered_rejecting_mutations"]
        )
        annex.append(
            f"""
### Card {index:02d}: {proposal['proposal_id']} — {proposal['title']}

- Core outcome: `{proposal['expected_disposition']}`.
- Approval class: `{proposal['approval_class']}`.
- Execution lane: `{proposal['execution_lane']}`.
- Hypothesis: {proposal['hypothesis']}
- Null or failure condition: {proposal['null_or_failure_condition']}
- Falsifier or acceptance gate: {proposal['falsifier_or_acceptance_gate']}
- Rollback or recovery: {proposal['rollback_or_recovery']}
- Official or primary-source needs: {source_needs}.
- Concrete evidence artifacts: {artifacts}.
- Protected gates:
{protected}
- Preregistered rejecting mutations:
{mutations}

Successor interpretation boundary: this card is an immutable Neris record. It grants Vesper no automatic novelty, completion, professional standing, production readiness, legal or cultural legitimacy, Māori authority, affected-party acceptance, independent reproduction, empirical GMUT support, AGI or ASI evidence, consciousness or personhood evidence, proof, canon, or Stage 20 authority. Any later Vesper use must preserve the failed-witness history and produce Vesper-attributable evidence inside Vesper's own strict x1-before-x2 lifecycle.
""".strip()
        )
    return prefix.rstrip() + "\n\n" + "\n\n".join(annex) + "\n"


def static_report() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Neris Solane {PHASE} bounded static report</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.55; }}
    body {{ margin: 0 auto; max-width: 74rem; padding: 1rem; }}
    a:focus {{ outline: 3px solid #d97706; outline-offset: 3px; }}
    .skip {{ position: absolute; left: -9999px; }}
    .skip:focus {{ left: 1rem; top: 1rem; background: Canvas; padding: .75rem; z-index: 2; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid currentColor; padding: .5rem; text-align: left; vertical-align: top; }}
    .boundary {{ border-left: .4rem solid #b91c1c; padding-left: 1rem; }}
  </style>
</head>
<body>
  <a class="skip" href="#main">Skip to main content</a>
  <header><h1>Neris Solane {PHASE}: bounded static evidence report</h1>
    <p>Owner-scoped synthetic documentation evidence. Terminal verdict: <strong>{TERMINAL}</strong>.</p>
  </header>
  <nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#retention">Retention</a></li><li><a href="#access">Accessibility</a></li></ul></nav>
  <main id="main">
    <section id="scope"><h2>Scope and boundaries</h2>
      <p>The primary pillar was THOS Body through synthetic historical pneumatic carrier-capsule, station-record, route-topology, queue-transition, exception-lineage, message-envelope, and custody-provenance documentation. GMUT Mind, Freed ID, and CBR Heart remained visible and protected.</p>
      <p class="boundary"><strong>Boundary:</strong> no real person, message, mail item, carrier, capsule, station, tube, compressor, pressure system, route, incident, observation, measurement, handling event, transport, operation, repair, identity event, professional decision, safety decision, legal or cultural decision, affected-party approval, or Māori-authority act was used or established.</p>
    </section>
    <section id="outcomes"><h2>Core outcomes</h2>
      <table><caption>Authorized core outcome labels and exact counts</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th><th scope="col">Meaning here</th></tr></thead><tbody>
        <tr><th scope="row">completed</th><td>42</td><td>Bounded synthetic contract accepted its positive and rejected its five declared mutations.</td></tr>
        <tr><th scope="row">represented</th><td>12</td><td>Obligation represented without real-world validation.</td></tr>
        <tr><th scope="row">open_gap</th><td>3</td><td>Evidence or capability remains absent.</td></tr>
        <tr><th scope="row">exact_gate</th><td>3</td><td>Action remains reserved to exact evidence and authority.</td></tr>
      </tbody></table>
    </section>
    <section id="retention"><h2>Retained truth</h2>
      <table><caption>Effective closeout counts</caption><tbody>
        <tr><th scope="row">Effective negatives</th><td>{COUNTS['effective_negatives']:,}</td></tr>
        <tr><th scope="row">Method Flow methods</th><td>{COUNTS['effective_methods']:,}</td></tr>
        <tr><th scope="row">Retained failed witnesses</th><td>{COUNTS['failed_witnesses']:,}</td></tr>
        <tr><th scope="row">Bounded passing witnesses</th><td>{COUNTS['bounded_passing_witnesses']:,}</td></tr>
        <tr><th scope="row">Open gaps</th><td>{COUNTS['open_gaps']}</td></tr>
        <tr><th scope="row">Exact gates</th><td>{COUNTS['exact_gates']}</td></tr>
      </tbody></table><p>Every recovery remains paired with its failed witness. No failure was erased or retroactively promoted.</p>
    </section>
    <section id="access"><h2>Accessibility and evaluation reservations</h2>
      <p>This report uses semantic regions, headings, a skip link, visible keyboard focus, captions, and scoped table headers. It requires no script. These checks are structural only.</p>
      <ul><li>Manual browser evaluation: reserved.</li><li>Screen-reader and other assistive-technology evaluation: reserved.</li><li>Keyboard, magnification, and cognitive-accessibility evaluation: reserved.</li><li>Māori-language and Māori-authority review: reserved to appropriate Māori authorities.</li><li>Affected-user and affected-party evaluation: reserved.</li></ul>
    </section>
  </main>
  <footer><p>Same-owner validation is not independent reproduction, professional evaluation, complete accessibility or privacy assurance, exhaustive security, empirical GMUT confirmation, proof, canon, or Stage 20 authority.</p></footer>
</body>
</html>"""


def initial_receipt(status: str, test_count: int) -> dict[str, object]:
    return {
        "canonical_invocation": False,
        "dependency_justified_target_changed_rerun": True,
        "lifecycle": "final_precommit",
        "owner": OWNER,
        "phase": PHASE,
        "prior_target_result": {
            "credit": "bounded_prior_target_only",
            "passed": 18,
            "target_changed_by": "NE6811-CL-N003 retention",
        },
        "selected_test_count": test_count,
        "status": status,
        "test_selection": "test_ghc_family_neris_solane_v681_v1_final.py only",
    }


def privacy_scan(paths: list[str]) -> dict[str, object]:
    classes = {
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+|[A-Z]:\\GHC-Archives\\"),
        "private_callable_identifier": re.compile(r"mcp__codex_app__[A-Za-z0-9_]+"),
        "private_session_capture": re.compile(r"(?i)\\.codex\\(?:sessions|transcripts|screenshots)\\"),
        "uuid_like_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
    }
    candidates: list[dict[str, str]] = []
    for path_text in paths:
        if path_text.endswith("final-privacy-scan.json"):
            continue
        text = (ROOT / path_text).read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                classification = "scanner_definition_or_synthetic_test" if path_text.startswith(("scripts/", "tests/")) else "unresolved"
                candidates.append({"classification": classification, "path": path_text, "privacy_class": class_name})
    confirmed = [row for row in candidates if row["classification"] == "unresolved"]
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "owner": OWNER,
        "phase": PHASE,
        "privacy_classes": sorted(classes),
        "scanned_file_count": len(paths) - 1,
    }


def security_scan(paths: list[str]) -> dict[str, object]:
    python_paths = [path for path in paths if path.endswith(".py")]
    ast_errors: list[str] = []
    findings: list[dict[str, str]] = []
    for path_text in python_paths:
        text = (ROOT / path_text).read_text(encoding="utf-8")
        try:
            tree = ast.parse(text, filename=path_text)
        except SyntaxError:
            ast_errors.append(path_text)
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"finding": f"dynamic_{node.func.id}_call", "path": path_text})
            if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append({"finding": "subprocess_shell_true", "path": path_text})
    return {
        "ast_errors": ast_errors,
        "bounded_findings": len(findings),
        "findings": findings,
        "owner": OWNER,
        "phase": PHASE,
        "python_file_count": len(python_paths),
        "scope": "owner_evidence_to_final_changed_python_only",
    }


def build(status: str, test_count: int) -> None:
    require_evidence_boundary()
    x2_method = json.loads((X2 / "method-flow-ledger.json").read_text(encoding="utf-8"))
    x2_gates = json.loads((X2 / "gate-register.json").read_text(encoding="utf-8"))
    x2_evidence = json.loads((X2 / "proposal-evidence.json").read_text(encoding="utf-8"))
    if x2_method["counts"] != EVIDENCE_COUNTS or x2_evidence["outcome_counts"] != OUTCOMES:
        raise RuntimeError("x2 truth does not match final input")
    if x2_gates["open_gaps"] != 467 or x2_gates["exact_gates"] != 458:
        raise RuntimeError("x2 gate input mismatch")

    write_text(FINAL / "final-integrated-overview.md", final_overview())
    write_text(FINAL / "static-report.html", static_report())
    write_json(
        FINAL / "phase-truth.json",
        {
            "canonical_state": "AWAITING_EXTERNAL_EXACT_FINAL_CANONICAL",
            "counts": COUNTS,
            "declared_chain": 9770,
            "full_repository_suite_run": False,
            "outcomes": OUTCOMES,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "same_owner_validation_is_independent_reproduction": False,
            "terminal_verdict": TERMINAL,
        },
    )
    final_method = dict(x2_method)
    final_method.update({"closeout_operational_failures": CLOSEOUT_FAILURES, "counts": COUNTS, "lifecycle": "exact_final_closeout", "schema": "ghc.family.method-flow.v681.v1.final"})
    write_json(FINAL / "method-flow-final.json", final_method)
    write_json(
        FINAL / "retained-negative-register.json",
        {
            "closeout_operational_failures": CLOSEOUT_FAILURES,
            "counts": COUNTS,
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "retained_mutation_failures": 300,
            "startup_and_x1_failures": x2_method["startup_and_x1_failures"],
            "x2_operational_failures": x2_method["x2_operational_failures"],
        },
    )
    write_json(FINAL / "open-gap-register.json", {"count": 467, "inherited": 464, "new": 3, "owner": OWNER, "state": "OPEN"})
    write_json(FINAL / "exact-gate-register.json", {"count": 458, "inherited": 455, "new": 3, "owner": OWNER, "state": "EXACT_GATED"})
    write_json(
        FINAL / "complete-incomplete-ledger.json",
        {
            "complete": [
                "planning-only x1 frozen and remotely equal before x2",
                "sixty synthetic contracts and 300 rejecting mutations executed",
                "twenty owner-local skills and ten runners validated and smoke-used",
                "sixty-seven four-tier Freed ID flashcards linked and manifest-replayed",
                "three D-isolated phase tools installed dependency-checked and smoke-used",
                "owner-scoped evidence and closeout prepared",
            ],
            "incomplete": [
                "real messages mail carrier capsules stations tubes pressure systems routes measurements operations repairs or professional evaluation",
                "empirical GMUT confirmation",
                "real participant THOS evaluation",
                "production Freed ID lifecycle and governance",
                "legal cultural affected-party and Māori-authority decisions",
                "manual and affected-user accessibility evaluation",
                "independent reproduction and complete repository suite",
                "Stage 20 readiness",
            ],
            "terminal_verdict": TERMINAL,
        },
    )
    write_json(
        FINAL / "lifecycle-replay.json",
        {
            "closeout_operational_failures": [row["failure_id"] for row in CLOSEOUT_FAILURES],
            "direct_edges": [[SOURCE, X1_HEAD], [X1_HEAD, EVIDENCE], [EVIDENCE, "EXTERNAL_POSTCOMMIT_FINAL"]],
            "evidence_head": EVIDENCE,
            "evidence_precommit_tests": {"passed": 22, "replayed_at_final": False},
            "expected_merges": 0,
            "expected_phase_commits": 3,
            "final_parent_required": EVIDENCE,
            "immutable_x1_precommit_tests": {"passed": 18, "replayed_at_final": False},
            "owner": OWNER,
            "source": SOURCE,
            "target_branch": BRANCH,
            "target_final": "EXTERNAL_POSTCOMMIT_FINAL",
            "target_final_parent_count": 1,
            "x1_head": X1_HEAD,
        },
    )
    write_json(
        FINAL / "official-source-boundary.json",
        {
            "authority_conferred": False,
            "citations_are_observations": False,
            "official_source_network_reads": True,
            "official_sources": [
                "Smithsonian National Postal Museum Pneumatic Tube Mail search result",
                "Smithsonian National Postal Museum Pneumatic Tube Canister search result",
                "WorkSafe New Zealand pressure-equipment page with legacy-guidance notice",
                "US National Archives Metadata Guidance",
                "US National Archives Lifecycle Data Requirements Guide for Archival Materials",
                "Library of Congress PREMIS version 3 search result with direct-access limitation",
                "New Zealand Privacy Commissioner privacy principles",
                "W3C PROV-DM",
                "WCAG 2.2",
                "W3C Verifiable Credentials Data Model 2.0",
                "RFC 8785 JSON Canonicalization Scheme",
                "Te Mana Raraunga principles inherited boundary reference not independently reread",
            ],
            "real_data_rows": 0,
            "real_world_actions": 0,
            "scope": "vocabulary_and_refusal_conditions_only",
        },
    )
    write_json(
        FINAL / "wellbeing-and-workload.json",
        {
            "assessment_type": "bounded_nonclinical_workload_check",
            "corrigibility_preserved": True,
            "failure_recorded_before_recovery": True,
            "owner": OWNER,
            "phase": PHASE,
            "quota_never_overrode_safety": True,
            "relational_language_is_inner_experience_evidence": False,
            "scope": "solo_finite_owner_lane",
            "stop_conditions_active": True,
            "user_control_preserved": True,
        },
    )
    write_json(
        FINAL / "environment-version-receipt.json",
        {
            "codex_cli_version": "not_rechecked_in_closeout_no_material_need",
            "codex_desktop_updated": False,
            "git_version": "git version 2.55.0.windows.2",
            "node_version": "v24.18.0",
            "npm_version": "12.0.2",
            "owner": OWNER,
            "phase": PHASE,
            "phase_isolated_tools": ["jsonpointer 3.1.1", "rfc3339-validator 0.1.4", "fqdn 1.5.1"],
            "platform_family": platform.system(),
            "python_version": "3.12.10",
            "read_only_version_checks": True,
            "unrelated_software_installed": False,
        },
    )
    write_json(
        FINAL / "canonical-contract.json",
        {
            "canonical_receipt_location": "external_to_repository",
            "complete_repository_suite_assigned": False,
            "complete_repository_suite_run": False,
            "exact_final_required": True,
            "full_repository_suite_authorized": False,
            "maximum_attributable_invocations": 1,
            "owner_scoped_only": True,
            "post_success_replay_permitted": False,
            "same_owner_is_independent_reproduction": False,
            "status_before_invocation": "NOT_INVOKED",
        },
    )
    write_json(
        FINAL / "terminal-checklist.json",
        {
            "canonical_external_pending": True,
            "clean_pushed_remote_equal_pending": True,
            "evidence_head": EVIDENCE,
            "full_suite_not_run": True,
            "one_final_parent_required": True,
            "owner": OWNER,
            "prepared_recipient": "Vesper Arlen",
            "prepared_recipient_phase": "v681-v2",
            "route_contacted": False,
            "source": SOURCE,
            "terminal_verdict": TERMINAL,
            "x1_head": X1_HEAD,
        },
    )
    baton = handoff_candidate()
    baton_word_count = len(baton.split())
    if baton_word_count < 10000 or baton_word_count > 100000:
        raise RuntimeError(f"handoff baton word count outside the authorized 10000..100000 range: {baton_word_count}")
    write_text(HANDOFFS / "vesper-arlen-v681-v2-activation-candidate.md", baton)

    seal_targets = [
        "docs/neris-solane/v681-v1/final/final-integrated-overview.md",
        "docs/neris-solane/v681-v1/final/static-report.html",
        "docs/neris-solane/v681-v1/final/phase-truth.json",
        "docs/neris-solane/v681-v1/final/method-flow-final.json",
        "docs/neris-solane/v681-v1/final/retained-negative-register.json",
        "docs/neris-solane/v681-v1/final/open-gap-register.json",
        "docs/neris-solane/v681-v1/final/exact-gate-register.json",
        "docs/neris-solane/v681-v1/final/complete-incomplete-ledger.json",
        "docs/neris-solane/v681-v1/final/lifecycle-replay.json",
        "docs/neris-solane/v681-v1/final/canonical-contract.json",
        "docs/neris-solane/v681-v1/final/official-source-boundary.json",
        "docs/neris-solane/v681-v1/final/wellbeing-and-workload.json",
        "docs/neris-solane/v681-v1/final/environment-version-receipt.json",
        "docs/neris-solane/v681-v1/final/terminal-checklist.json",
        "docs/neris-solane/v681-v1/handoffs/vesper-arlen-v681-v2-activation-candidate.md",
    ]
    write_json(CLOSEOUT / "content-seal.json", {"hash_domain": "normalized_lf_worktree_bytes", "owner": OWNER, "phase": PHASE, "targets": [entry(path) for path in seal_targets]})
    write_json(VALIDATION / "final-precommit-test-receipt.json", initial_receipt(status, test_count))
    for placeholder in SELF_EXCLUSIONS:
        if not (ROOT / placeholder).exists():
            write_json(ROOT / placeholder, {"owner": OWNER, "phase": PHASE, "state": "SELF_EXCLUDED_PENDING_REGENERATION"})

    final_paths = sorted(git("ls-files", "--others", "--exclude-standard").splitlines())
    allowed_exact = {
        "scripts/build_ghc_family_neris_solane_v681_v1_final.py",
        "scripts/ghc_family_neris_solane_v681_v1_canonical.py",
        "tests/test_ghc_family_neris_solane_v681_v1_final.py",
    }
    unexpected = [path for path in final_paths if not path.startswith("docs/neris-solane/v681-v1/") and path not in allowed_exact]
    if unexpected:
        raise RuntimeError(f"unexpected untracked paths: {unexpected}")
    if set(SELF_EXCLUSIONS) - set(final_paths):
        raise RuntimeError("declared final self-exclusion is missing")

    write_json(VALIDATION / "final-privacy-scan.json", privacy_scan(final_paths))
    write_json(VALIDATION / "final-security-scan.json", security_scan(final_paths))
    max_row = max(((len((ROOT / path).read_text(encoding="utf-8").split()), path) for path in final_paths if (ROOT / path).is_file()), default=(0, ""))
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "expected_paths": final_paths,
            "lifecycle": "final_closeout_only",
            "max_document_path": max_row[1],
            "max_document_words": max_row[0],
            "owner": OWNER,
            "path_count": len(final_paths),
            "phase": PHASE,
        },
    )
    delta_entries = [entry(path) for path in final_paths if path not in SELF_EXCLUSIONS]
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {"declared_self_exclusions": SELF_EXCLUSIONS, "entries": delta_entries, "entry_count": len(delta_entries), "hash_domain": "normalized_lf_git_blob_after_stage", "owner": OWNER, "phase": PHASE},
    )
    inherited_paths = git("diff", "--name-only", SOURCE, "HEAD").splitlines()
    owner_paths = sorted(set(inherited_paths + final_paths))
    owner_entries = [entry(path) for path in owner_paths if path not in SELF_EXCLUSIONS]
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {"declared_self_exclusions": SELF_EXCLUSIONS, "entries": owner_entries, "entry_count": len(owner_entries), "hash_domain": "normalized_lf_git_blob_after_stage", "owner": OWNER, "phase": PHASE, "source": SOURCE},
    )
    print(json.dumps({"final_paths": len(final_paths), "owner_entries": len(owner_entries), "status": status}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-precommit", action="store_true")
    parser.add_argument("--test-count", type=int, default=0)
    args = parser.parse_args()
    if args.record_precommit:
        if args.test_count <= 0:
            raise SystemExit("--test-count must be positive when recording precommit success")
        build("PASSED", args.test_count)
    else:
        build("PENDING", 0)


if __name__ == "__main__":
    main()
