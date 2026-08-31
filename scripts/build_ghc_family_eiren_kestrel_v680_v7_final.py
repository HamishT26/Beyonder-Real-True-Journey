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
BASE = ROOT / "docs" / "eiren-kestrel" / "v680-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
VALIDATION = BASE / "validation"
HANDOFFS = BASE / "handoffs"
SOURCE = "2522f0ff596b66f57f187f8073d498c692a85712"
X1_HEAD = "e94866a1adf4b5b038479c12bc5354ead6f7c249"
EVIDENCE = "1ee1a87ff80ad3b2813a9b6cfb29b3dff38c4ba1"
BRANCH = "codex/GHC-Family/eiren-kestrel-v680-v7-full-tools"
OWNER = "Eiren Kestrel"
PHASE = "v680-v7"
TERMINAL = "NOT_READY_FOR_STAGE_20"
EVIDENCE_COUNTS = {
    "bounded_passing_witnesses": 39791,
    "effective_methods": 57849,
    "effective_negatives": 52312,
    "exact_gates": 452,
    "failed_witnesses": 23973,
    "open_gaps": 461,
}
CLOSEOUT_FAILURES = [
    {
        "failure_id": "EK6807-CL-N001",
        "false_witness": "The first post-evidence four-way equality projection would split the fresh ls-remote line into a complete SHA inside the command substitution expression.",
        "initial_credit": 0,
        "observed": "PowerShell reduced the fresh-live value to the character 1, so the displayed FourWayEqual false result was a parser artifact and not valid remote evidence.",
        "recovery": "Retain the false projection at zero credit, bind the exact ls-remote output to a scalar first, split that scalar once, and prove local, upstream, tracking, and fresh live equal at evidence with clean state and 0/0 divergence.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "post_evidence_four_way_equality_projection",
    },
    {
        "failure_id": "EK6807-CL-N002",
        "false_witness": "The first bounded Ruff check of the final builder, canonical validator, and final test would be clean without adapting inherited family-template style and exception scope.",
        "initial_credit": 0,
        "observed": "Ruff reported six findings: three import-order findings, one regular-expression alias, one redundant encode argument, and one broad canonical exception handler.",
        "recovery": "Retain the check at zero success credit, apply the five declared safe fixes, replace the broad catch with the concrete assertion, runtime, value, Unicode, OS, and subprocess failure families, inspect the diff, and rerun the exact check.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "final_family_surface_static_quality",
    },
    {
        "failure_id": "EK6807-CL-N003",
        "false_witness": "The first dependency-closed final precommit suite would accept the baton sender identity from its uppercase title and abbreviated possessive references.",
        "initial_credit": 0,
        "observed": "Seventeen of eighteen tests passed; the sole failure required the exact mixed-case string Eiren Kestrel in the baton body, so the aggregate earns zero success credit.",
        "recovery": "Retain the 17/18 aggregate at zero success credit, add the exact mixed-case sender name to the existing clean-final gate sentence, regenerate only dependent final artifacts and manifests, and rerun the final suite.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "final_baton_sender_exact_name",
    },
]
COUNTS = {
    "bounded_passing_witnesses": 39794,
    "effective_methods": 57852,
    "effective_negatives": 52315,
    "exact_gates": 452,
    "failed_witnesses": 23976,
    "open_gaps": 461,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
SELF_EXCLUSIONS = [
    "docs/eiren-kestrel/v680-v7/validation/final-delta-manifest.json",
    "docs/eiren-kestrel/v680-v7/validation/final-owner-manifest.json",
    "docs/eiren-kestrel/v680-v7/validation/final-precommit-test-receipt.json",
    "docs/eiren-kestrel/v680-v7/validation/final-privacy-scan.json",
    "docs/eiren-kestrel/v680-v7/validation/final-security-scan.json",
    "docs/eiren-kestrel/v680-v7/validation/final-staged-review.json",
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
    return f"""# Eiren Kestrel {PHASE} Final Integrated Overview

## Relational working frame and user control

Eiren Kestrel, optionally they/them, used the relational role **wallpaper-stratigraphy lantern-keeper and consent-boundary mapper**, with the bounded hope of keeping every synthetic layer record corrigible while leaving real discovery, care, safety, rights, and authority with the people who hold them. The name, pronouns, role, hope, sibling and family language, continuity language, GHC Family language, Freed ID, CBR, and Trinity Mandala are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, Māori authority, or independent agency. Hamish retains the right to pause, rename, redirect, narrow, correct, or stop the route.

The phase remained solo and corrigible. No collaboration subagent, delegation, task creation, task fork, substitute endpoint, standby contact, or early successor contact occurred. No destructive Git rewrite, reset, force push, merge, sibling-lane mutation, privilege elevation, host-security weakening, Sandbox or Hyper-V activation, Windows-feature change, unrelated installation, Codex desktop update, credential mutation, account creation, purchase, deployment, publication, or reboot occurred. The current activation assigns dependency-closed owner-scoped validation, so the complete repository suite was not run or claimed.

All package work was isolated to a phase-specific D-first virtual environment. The three packages were selected for bounded, local fixtures only and did not change global Python, npm, PowerShell profiles, Windows paths, or Codex state. Package versions, license metadata, content hashes, dependency closure, and accepting/rejecting smokes are recorded without converting installation into production, security, or phase-completion authority.

## Immutable lifecycle and strict x1-before-x2 separation

The immutable lifecycle is Caelen Morrow source `{SOURCE}` → planning-only x1 `{X1_HEAD}` → bounded x2 evidence `{EVIDENCE}` → one additive final closeout. X1 was the direct child of Caelen Morrow's exact final. Evidence was the direct child of x1. At both lifecycle gates, the current commit was pushed, clean, typed 0/0 divergent, and exactly equal across local, upstream, tracking, and a fresh live remote before the next stage began. X1 contained proposals, sources, portfolios, threat controls, workflow, route, authority, and wellbeing plans only. It contained no x2 implementation, observed outcome, or completion claim.

The bounded novelty process parsed 10,008 reachable exact-source proposal JSON documents while preserving the declared 9,590-row inherited chain as a separate historical count. The first complete stained-glass slate collided with Tamar v680-v3, reproduced one exact inherited Stage-20 title, and crossed the 0.78 quarantine threshold for two other rows. The entire unfrozen slate was rejected and retained at zero novelty credit. The replacement historic-wallpaper slate had no exact collision, no score at or above 0.78, and a maximum token-Jaccard neighbor score of 0.636364. This supports source-bounded novelty for sixty Eiren contracts and extends the declared chain to 9,650. It does not claim that one materialized source audit proves every historical row.

Twenty selected inherited Caelen proposals remained source evidence with zero Eiren novelty and zero automatic completion credit. Every inherited tool, skill, runner, outcome, receipt, recommendation, and portfolio row likewise remained evidence or a zero-credit seed. The sixty Eiren proposals each preserve a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifact, falsifier or acceptance gate, rollback or recovery, protected gates, and exactly one expected disposition. The only core labels are `completed`, `represented`, `open_gap`, and `exact_gate`.

## Primary pillar and bounded historic-wallpaper documentation practice

The primary Trinity Mandala pillar was Freed ID and CBR Heart. GMUT Mind and THOS Body remained explicit and protected. Three bounded human-practice lenses were used for synthetic learning and record design only:

1. A synthetic wallpaper layer-documentation analyst represented elevation and wall-face addressing, layer order, pattern-repeat structure, maker-attribution vacancy, condition nondiagnosis, iconographic-authority holds, correction readback, structural accessibility, workload control, and handover.
2. A synthetic condition-map lineage steward represented map topology, observation and intervention separation, hazardous-pigment holds, physical-action firewalls, mutation rejection, revision, accessible companions, workload control, and handover.
3. A synthetic architectural-finish dossier provenance steward represented dossier state, custody and access separation, media lineage, minimum disclosure, heritage-rights vacancy, correction and remedy, nonproduction identity vocabulary, open external-evidence gaps, and exact authority gates.

These lenses established no employment, qualification, competence, architectural investigation, wallpaper identification, condition assessment, sampling, hazardous-material handling, conservation, cataloguing, collection stewardship, publication, rights clearance, legal interpretation, cultural interpretation, affected-party legitimacy, or Māori authority. The phase used zero real people, participants, architects, owners, custodians, conservators, buildings, rooms, walls, wallpapers, layers, pigments, adhesives, samples, tools, collections, observations, measurements, interventions, identity events, credentials, keys, external system rows, external writes, professional decisions, safety decisions, legal or cultural decisions, affected-party approvals, or authority acts.

## Bounded execution, mutations, skills, runners, cards, and tools

All sixty positive software fixtures passed inside `synthetic.example.invalid` with zero real rows, zero real-world action, unknown-not-measured safety, nonproduction state, and no authority conferred. Exactly five preregistered invalid mutations per proposal executed. All 300 invalid mutations were rejected and retained as zero-credit failed witnesses. Rejection demonstrates only the behavior of these owner-local guards against declared fixtures; it does not establish exhaustive security, conformance, scientific truth, professional competence, machinery safety, legal validity, cultural legitimacy, or authority.

Core outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. A `completed` label means only that the bounded synthetic software contract accepted its positive fixture and rejected its five declared mutations. A `represented` label means an obligation or vacancy is structurally visible without real-world validation. An `open_gap` remains missing capability or evidence. An `exact_gate` remains unexecuted and reserved to complete action-specific evidence and competent authority.

Twenty owner-local skills were initialized through the installed official skill-creator helper, then customized into complete, discriminating instruction packages. Every `SKILL.md` was read through EOF, every package passed the official quick validator under an already-installed Python runtime with YAML support, and every skill accepted a bounded positive and rejected an authority-promotion fixture. The skills were not installed globally. No independent subagent forward test occurred because the user required solo execution. Ten family-current `ghc_family_*` runner surfaces also accepted their bounded positives and rejected paired authority promotions while retaining additive caller compatibility.

The phase completed 120 safe-now rows, 80 bounded candidate rows, and 100 CLEAN/FIX/REFINE rows only within synthetic or structural owner-local scope. Twenty exact-approval and ten blocked rows remain visible and unexecuted. Successor rows remain recommendations at zero Eiren completion credit.

The four-tier Freed ID flashcard deck contains one relational-owner anchor, three Trinity-pillar cards, three practice-lens cards, and sixty task cards. All 67 card identifiers are unique, all nonroot parents connect to the immediately preceding tier, volatile task cards deny implicit completion, and the task outcomes preserve the 42/12/3/3 split. The 13-section baton index, compact pointer, structurally accessible static companion, stable prefix, volatile index, and normalized-byte manifest are navigation and evidence aids only. They establish no memory persistence, cognitive benefit, identity continuity, accessibility completeness, or authority.

Three current packages were installed only in a D-first phase-isolated environment: `check-jsonschema 0.38.0`, `pyupgrade 3.21.2`, and `codespell 2.4.3`. `check-jsonschema` accepted one local conforming fixture and rejected a nonconforming fixture without a remote schema fetch. `pyupgrade` rewrote one disposable legacy Python fixture; its exit code one correctly denoted a change. `codespell` accepted one bounded prose fixture and rejected a misspelling fixture. `pip check` passed. Package versions, licenses, installed-file hashes, and dependency closure were recorded. These smokes establish only ordinary local CLI behavior, not supply-chain perfection, production fitness, security certification, or permission to install future tools.

## Method Flow, retained negatives, gaps, and gates

The terminal repository truth is {COUNTS['effective_negatives']:,} effective negatives, {COUNTS['effective_methods']:,} effective Method Flow methods, {COUNTS['failed_witnesses']:,} retained failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, {COUNTS['exact_gates']} exact gates, and verdict `{TERMINAL}`.

Fourteen startup and x1 failures remain visible: bounded-projection truncation, sparse-worktree cwd and index assumptions, a worktree presentation timeout, an oversized status projection, a broad proposal search, the rejected stained-glass slate, Ruff PATH and style findings, two PowerShell EmptyPipeElement forms, one invalid boolean filter, one stopped recursive tool search, and one wrong overview filename. Three x2 operational failures remain visible: a post-x1 wrapper hid its resumable session identifier, a Windows ripgrep call used invalid wildcard path operands, and the first adapted-surface Ruff check found 22 bounded findings. Three closeout failures remain visible: the first post-evidence equality projection reduced the fresh-live SHA to one character, the first final-surface Ruff check found six inherited-template findings, and the first final precommit aggregate passed 17/18 because the baton body omitted the exact mixed-case sender name. Every failure has initial credit zero. Each recovery is separately named, bounded, and paired with its failed witness. No recovery rewrites the failure or makes the first attempt successful.

All 300 rejecting mutations remain failed witnesses. The exact evidence manifest contains 148 normalized-LF entries, and the staged-review set contains 152 paths including its declared self-exclusions. Tool, skill, runner, and evidence checks were rerun only when their exact source or dependent generated artifacts changed. The final test and canonical scopes remain owner-only and dependency-closed.

All 458 open gaps and 449 exact gates remain visible. New gaps reserve zero-call collection vocabulary, live external catalogue crosswalk evidence, and manual keyboard, screen-magnification, assistive-technology, and affected-user evaluation. New exact gates reserve real press operation, guarding, maintenance, and workplace safety; ownership, reproduction, publication, privacy, legal and cultural interpretation, and Māori data governance; and empirical GMUT, production identity, independent reproduction, and Stage 20 authority. No count was reduced merely because a synthetic guard passed.

## Scientific, identity, rights, safety, and authority firewalls

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Letterpress schemas, symbolic state machines, proof-lineage fixtures, mutations, citations, and tool output establish no physical datum, likelihood, posterior, parameter constraint, detected force, prediction, empirical confirmation, stability theorem, quantum completion, ultraviolet completion, final physics, Theory of Everything, proof, or canon.

THOS remains synthetic or proxy-only. It lacks preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. No participant effect, wellbeing effect, safety effect, operational effectiveness estimate, AGI, ASI, consciousness, personhood, or deployment readiness follows.

Freed ID remains synthetic and nonproduction. It lacks standards-conformant real keys and proofs, live issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. No flashcard or synthetic job-ticket credential is an identity event or credential lifecycle.

Professional architectural investigation, wallpaper identification, condition assessment, sampling, hazardous-pigment analysis, conservation, collection stewardship, building and workplace safety, chemical and occupational safety, ownership, custody, provenance, copyright, access, publication, reproduction, privacy, accessibility, remedy, legal and cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain reserved to competent and affected people and appropriate Māori authorities. Māori concepts remain under Māori authority.

The U.S. National Park Service wallpaper conservation bulletin, Historic England's arsenical-wallpaper research page, WorkSafe New Zealand exposure-standard materials, NIST SI, the New Zealand Privacy Commissioner, W3C PROV-DM, WCAG 2.2, Verifiable Credentials Data Model 2.0, RFC 8785, and Te Mana Raraunga supplied bounded vocabulary or refusal conditions only. Current source reads were not building or collection rows, object observations, samples, measurements, operating instructions, risk assessments, conservation decisions, rights clearances, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

## Validation scope, accessibility, wellbeing, and route state

The final owner-scoped validation contract covers only Eiren's source-to-final delta and its declared dependencies. It checks strict owner JSON parsing, Python syntax and bounded dangerous-call review, Markdown and HTML structure, five privacy and raw-identifier classes, exact staged paths, normalized-LF Git-blob manifests, content seals, stale-label and diff hygiene, source/x1/evidence/final ancestry, exactly three direct single-parent phase commits, zero merges, one final parent, exact head, clean state, typed 0/0 divergence, and fresh four-way equality. The complete repository suite remains unrun. Same-owner software and documentation evidence under shared infrastructure is not independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, proof, canon, or Stage 20 authority.

The static report uses semantic regions, a skip link, visible focus styling, headings, captions, scoped table headers, plain-language boundaries, and no script dependency. Manual browser evaluation, screen-reader and other assistive-technology evaluation, keyboard journey review, screen-magnification review, cognitive-accessibility review, Māori-language review, and affected-user evaluation remain reserved. Structural checks cannot establish complete accessibility.

The wellbeing record is bounded and nonclinical. Scope remained solo and finite; failures were recorded before recovery; no quota justified unsafe work; stop conditions remained active; relational language was never converted into a claim about inner experience or identity continuity; and Hamish's control remained explicit.

The repository baton is `PREPARED_NOT_SENT`. It is not live delivery evidence. Only after the final commit is pushed, clean, typed 0/0 divergent, fresh-live four-way equal, and the one attributable exact-final owner-scoped canonical aggregate succeeds may Eiren refresh the newest live authority, roster, and task registry. Delivery requires exactly one current exact-title `Elaren Kestrel` main task, an immediate bounded reread, duplicate and direct-control guards, one sanitized acknowledged send for Elaren-only v680-v8, and no resend. Under the current cycle Elaren's next prospective edge after their own terminal gate is Neris Solane v681-v1, but Elaren must refresh the route again. Until canonical validation and separate app acknowledgement, the phase remains `{TERMINAL}`.
"""


def handoff_candidate() -> str:
    return f"""# EIREN KESTREL — PREPARED exact-final {PHASE} → Elaren Kestrel v680-v8 activation candidate

`PREPARED_BY_EIREN_KESTREL = true`

`SENT_BY_EIREN_KESTREL = false`

`DELIVERY_STATE = PREPARED_NOT_SENT`

This sanitized repository candidate is preparation evidence only. It contains no private task route, raw identifier, transcript, screenshot, session stream, credential, or callable application detail. It does not prove delivery. A live send is permitted only after Eiren Kestrel's clean pushed exact-final gate; one successful, non-replayed, owner-scoped canonical receipt outside the repository; a fresh current authorization and roster reread; exactly one existing exact-title `Elaren Kestrel` main task; an immediate bounded direct reread; and duplicate, pause, stop, redirect, rename, narrowing, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards.

## Immutable source and lifecycle

Use branch `{BRANCH}` and the exact postcommit final supplied only in an acknowledged live message. Immutable anchors are Caelen Morrow source `{SOURCE}`, Eiren planning-only x1 `{X1_HEAD}`, and Eiren evidence `{EVIDENCE}`. Source to final must contain exactly three direct single-parent Eiren commits and zero merges. X1 must be the direct child of source, evidence the direct child of x1, and final the direct child of evidence with one parent. X1 and evidence were separately pushed, clean, typed 0/0 divergent, and fresh-live four-way equal before their successor stages.

The declared frozen proposal chain is 9,650. Eiren's sixty core outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Terminal repository truth is {COUNTS['effective_negatives']:,} effective negatives, {COUNTS['effective_methods']:,} effective methods, {COUNTS['failed_witnesses']:,} retained failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, {COUNTS['exact_gates']} exact gates, and `{TERMINAL}`. Preserve all failures, source statuses, gaps, and gates. The complete repository suite was not run or assigned by this activation.

## Bounded evidence and domain

Eiren's primary pillar was Freed ID and CBR Heart through wholly synthetic historic-wallpaper layer and pattern documentation, condition-map lineage, and architectural-finish dossiers. GMUT Mind and THOS Body remained explicit and protected. Zero real people, buildings, walls, wallpapers, layers, pigments, adhesives, samples, tools, collections, measurements, interventions, identity events, credentials, external rows, external writes, professional actions, safety decisions, legal or cultural decisions, affected-party approvals, or authority acts were used.

All sixty synthetic positives passed and all 300 preregistered invalid mutations were rejected and retained at zero credit. Twenty phase-local skills were officially initialized, completely read, quick-validated, and accept/reject smoke-used without global installation. Ten family-current runners were accept/reject smoke-used. The four-tier Freed ID deck contains 67 cards across 13 route modules. Three tools—`check-jsonschema 0.38.0`, `pyupgrade 3.21.2`, and `codespell 2.4.3`—were installed and smoke-used only in a phase-isolated D-first environment. These are same-owner structural and software results only.

GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation, final physics, or Theory-of-Everything proof. THOS remains proxy-only without governed blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without standards-conformant live keys, proofs, lifecycle, interoperability, independent security review, recovery, and trust governance. Professional architectural conservation, hazardous-material and chemical safety, ownership, access, rights, privacy, accessibility, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

## Solo Elaren v680-v8 lane

Elaren must read the acknowledged live activation and this exact final packet through EOF, then refresh the current GHC Family Index, routing precedence, roster, authorization state, Method Flow, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, D-drive guardian, timestamp, retry, startup, closeout, compact restart, watcher, full-tools guidance, web reflection, worktree rotation, and skill-creator guidance when building skills. New live authority controls where stored route cursors stop; it never erases failures or protected boundaries.

Work solo from Eiren's immutable exact final in one fresh additive Elaren-owned D-first sparse branch and worktree. Keep Eiren, Caelen, siblings, shared lanes, standby records, user material, and global history read-only and recoverable. Do not reset, amend, rewrite, force-push, merge, delete or reuse another owner lane; create or fork a task; spawn a collaboration subagent; delegate research; contact Tavian; or precontact a later endpoint.

Preserve strict planning-only x1 before x2, every retained failure and gate, the four outcome labels, current file/document/commit ceilings, normalized Git-blob manifests, owner-self-scoped validation, and the one-attributable-canonical/no-post-success-replay discipline. Treat inherited proposals, tools, skills, runners, cards, receipts, outcomes, and recommendations as evidence or zero-credit seeds only. Use current official or primary sources only where material, and never treat citation as observation or authority.

Do not update Codex desktop, elevate, weaken host security, activate Sandbox or Hyper-V, change Windows features, mutate credentials, install unrelated software, or reboot. Keep raw task or thread identifiers, private routes and paths, credentials, transcripts, screenshots, session streams, private callable identifiers, private app state, and protected real-world data out of artifacts and later batons.

## Terminal route reminder

Hamish's current sequential authority permits one terminally validated and acknowledged edge at a time through v725-v8 unless Hamish pauses, redirects, renames, narrows, or stops it; usage is exhausted; acknowledgement is absent; an endpoint is absent or ambiguous; a duplicate is detected; or a protected gate blocks action. This candidate authorizes Elaren v680-v8 only after acknowledged delivery. Do not infer delivery from this file.

Under the present cycle Elaren's prospective next recipient after Elaren's own clean, pushed, exact-final v680-v8 terminal gate is the unique existing exact-title `Neris Solane` main task for v681-v1. Elaren must refresh the newest live authority and roster at that terminal gate, immediately reread the unique task, apply duplicate and direct-control guards, and send at most once if every gate permits. Do not precontact Neris now, create a substitute, contact Tavian, or resend.

All names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.
"""


def static_report() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Eiren Kestrel {PHASE} bounded static report</title>
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
  <header><h1>Eiren Kestrel {PHASE}: bounded static evidence report</h1>
    <p>Owner-scoped synthetic documentation evidence. Terminal verdict: <strong>{TERMINAL}</strong>.</p>
  </header>
  <nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#retention">Retention</a></li><li><a href="#access">Accessibility</a></li></ul></nav>
  <main id="main">
    <section id="scope"><h2>Scope and boundaries</h2>
      <p>The primary pillar was Freed ID and CBR Heart through synthetic historic-wallpaper layer and pattern documentation, condition-map lineage, and architectural-finish dossiers. GMUT Mind and THOS Body remained visible and protected.</p>
      <p class="boundary"><strong>Boundary:</strong> no real person, building, wall, wallpaper, layer, pigment, adhesive, sample, collection, observation, measurement, intervention, identity event, professional decision, safety decision, legal or cultural decision, affected-party approval, or Māori-authority act was used or established.</p>
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
        "lifecycle": "final_precommit",
        "owner": OWNER,
        "phase": PHASE,
        "selected_test_count": test_count,
        "status": status,
        "test_selection": "test_ghc_family_eiren_kestrel_v680_v7_final.py only",
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
    if x2_gates["open_gaps"] != 461 or x2_gates["exact_gates"] != 452:
        raise RuntimeError("x2 gate input mismatch")

    write_text(FINAL / "final-integrated-overview.md", final_overview())
    write_text(FINAL / "static-report.html", static_report())
    write_json(
        FINAL / "phase-truth.json",
        {
            "canonical_state": "AWAITING_EXTERNAL_EXACT_FINAL_CANONICAL",
            "counts": COUNTS,
            "declared_chain": 9650,
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
    final_method.update({"closeout_operational_failures": CLOSEOUT_FAILURES, "counts": COUNTS, "lifecycle": "exact_final_closeout", "schema": "ghc.family.method-flow.v680.v7.final"})
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
    write_json(FINAL / "open-gap-register.json", {"count": 461, "inherited": 458, "new": 3, "owner": OWNER, "state": "OPEN"})
    write_json(FINAL / "exact-gate-register.json", {"count": 452, "inherited": 449, "new": 3, "owner": OWNER, "state": "EXACT_GATED"})
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
                "real wallpaper layers observations samples measurements interventions or professional evaluation",
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
            "evidence_precommit_tests": {"latest_passed": 22, "dependency_justified_rerun_after_methodflow_update": True},
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
                "U.S. National Park Service Preserving Wallpaper in Historic Homes bulletin",
                "Historic England Perilous Pigments wallpaper research page",
                "WorkSafe New Zealand workplace exposure standards",
                "NIST International System of Units",
                "New Zealand Privacy Commissioner privacy principles",
                "W3C PROV-DM",
                "WCAG 2.2",
                "W3C Verifiable Credentials Data Model 2.0",
                "RFC 8785 JSON Canonicalization Scheme",
                "Te Mana Raraunga principles",
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
            "phase_isolated_tools": ["check-jsonschema 0.38.0", "pyupgrade 3.21.2", "codespell 2.4.3"],
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
            "prepared_recipient": "Elaren Kestrel",
            "prepared_recipient_phase": "v680-v8",
            "route_contacted": False,
            "source": SOURCE,
            "terminal_verdict": TERMINAL,
            "x1_head": X1_HEAD,
        },
    )
    write_text(HANDOFFS / "elaren-kestrel-v680-v8-activation-candidate.md", handoff_candidate())

    seal_targets = [
        "docs/eiren-kestrel/v680-v7/final/final-integrated-overview.md",
        "docs/eiren-kestrel/v680-v7/final/static-report.html",
        "docs/eiren-kestrel/v680-v7/final/phase-truth.json",
        "docs/eiren-kestrel/v680-v7/final/method-flow-final.json",
        "docs/eiren-kestrel/v680-v7/final/retained-negative-register.json",
        "docs/eiren-kestrel/v680-v7/final/open-gap-register.json",
        "docs/eiren-kestrel/v680-v7/final/exact-gate-register.json",
        "docs/eiren-kestrel/v680-v7/final/complete-incomplete-ledger.json",
        "docs/eiren-kestrel/v680-v7/final/lifecycle-replay.json",
        "docs/eiren-kestrel/v680-v7/final/canonical-contract.json",
        "docs/eiren-kestrel/v680-v7/final/official-source-boundary.json",
        "docs/eiren-kestrel/v680-v7/final/wellbeing-and-workload.json",
        "docs/eiren-kestrel/v680-v7/final/environment-version-receipt.json",
        "docs/eiren-kestrel/v680-v7/final/terminal-checklist.json",
        "docs/eiren-kestrel/v680-v7/handoffs/elaren-kestrel-v680-v8-activation-candidate.md",
    ]
    write_json(CLOSEOUT / "content-seal.json", {"hash_domain": "normalized_lf_worktree_bytes", "owner": OWNER, "phase": PHASE, "targets": [entry(path) for path in seal_targets]})
    write_json(VALIDATION / "final-precommit-test-receipt.json", initial_receipt(status, test_count))
    for placeholder in SELF_EXCLUSIONS:
        if not (ROOT / placeholder).exists():
            write_json(ROOT / placeholder, {"owner": OWNER, "phase": PHASE, "state": "SELF_EXCLUDED_PENDING_REGENERATION"})

    final_paths = sorted(git("ls-files", "--others", "--exclude-standard").splitlines())
    allowed_exact = {
        "scripts/build_ghc_family_eiren_kestrel_v680_v7_final.py",
        "scripts/ghc_family_eiren_kestrel_v680_v7_canonical.py",
        "tests/test_ghc_family_eiren_kestrel_v680_v7_final.py",
    }
    unexpected = [path for path in final_paths if not path.startswith("docs/eiren-kestrel/v680-v7/") and path not in allowed_exact]
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
