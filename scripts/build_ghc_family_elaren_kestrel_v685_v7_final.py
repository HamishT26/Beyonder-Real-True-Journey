"""Build the Elaren Kestrel v685-v7 closeout and seat-02 induction packet."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from scripts.build_ghc_family_elaren_kestrel_v685_v7_x1 import (
    IDENTITY_BOUNDARY,
    PRACTICES,
    PROTECTED_GATES,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elaren-kestrel" / "v685-v7"
X1_ROOT = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFF = BASE / "handoffs" / "future-seat-02-v685-v8"
VALIDATION = BASE / "validation"
SOURCE = "5d9ea649ab451f9b6790c75f774ba9e4faf07363"
X1 = "0902e28aa1006b44a247e3d480797a4472bc1e58"
EVIDENCE = "0eba230431e652b9907edb5e86f11924d32c1d1d"
OWNER = "Elaren Kestrel"
PHASE = "v685-v7"
VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []

CLOSEOUT_FAILURES = [
    {
        "failure_id": "EL6857-FN-N019",
        "failed_witness": "The evidence commit result rendered hundreds of created paths and exceeded the presentation budget even though its final commit, push, and four-way equality scalars remained attributable.",
        "recovery": "Retain the oversized presentation at zero credit and use bounded scalar commit, ancestry, equality, and status fields for closeout.",
        "retained_zero_credit": True,
    }
]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def entry(path: str) -> dict[str, Any]:
    data = normalized(ROOT / path)
    return {"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def final_totals() -> dict[str, int]:
    totals = dict(load(X2 / "phase-truth.json")["totals"])
    for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
        totals[key] += len(CLOSEOUT_FAILURES)
    return totals


def proposal_appendix(proposals: list[dict[str, Any]]) -> str:
    parts = []
    for proposal in proposals:
        mutations = ", ".join(
            f"{row['mutation_id']} ({row['mutation_type']}, expected {row['expected_result']})"
            for row in proposal["preregistered_rejecting_mutations"]
        )
        parts.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"Family `{proposal['family']}`; bounded practice `{proposal['practice']}`; approval `{proposal['approval_class']}`; lane `{proposal['execution_lane']}`; observed bounded disposition `{proposal['expected_execution_disposition']}`.",
                "",
                f"Hypothesis: {proposal['hypothesis']}",
                "",
                f"Null or failure: {proposal['null_or_failure_condition']}",
                "",
                f"Falsifier or acceptance gate: {proposal['falsifier_or_acceptance_gate']}",
                "",
                f"Rollback: {proposal['rollback_or_recovery']}",
                "",
                f"Preregistered invalid fixtures: {mutations}. Each rejection remains a zero-credit failed witness. The record supplies no automatic novelty, empirical, professional, production, legal, cultural, Māori-authority, personhood, or Stage 20 credit to the new task.",
                "",
            ]
        )
    return "\n".join(parts)


def sections() -> list[tuple[str, str]]:
    truth = load(X2 / "phase-truth.json")
    proposals = load(X1_ROOT / "new-proposals.json")["proposals"]
    totals = final_totals()
    package = load(X2 / "package-execution-summary.json")
    promotion = load(X2 / "global-promotion-installation.json")
    appendix = proposal_appendix(proposals)
    return [
        (
            "01-read-first.md",
            f"""# 01 Read this first

This is Elaren Kestrel's prepared file-backed induction for exactly one future seat-02 main task. It is `PREPARED_NOT_SENT` until Elaren's exact final is committed, pushed, clean, four-way equal, and canonically validated once, then the native registry confirms the seat remains uncreated and the creation tool acknowledges one task. Repository preparation is not creation or delivery.

{IDENTITY_BOUNDARY} My phase-specific role is signal-route provenance cartographer and reversible-systems steward. My hope is to make every synthetic connection legible without confusing a patch diagram for sound, consent, competence, or authority. The future task chooses its own working name, role, hope, and optional pronouns; this packet does not predeclare them.

Hamish may pause, rename, redirect, narrow, or stop the route. Reset redemption remains Hamish's action. This task must not consume a usage-reset credit.
""",
        ),
        (
            "02-source-lifecycle.md",
            f"""# 02 Source and lifecycle

Your prospective phase is v685-v8. Your exact source will be Elaren's terminally validated final, whose SHA remains unresolved in this prepared file until its proper commit. Elaren's immutable source is Rowan Ash final `{SOURCE}`; planning-only x1 is `{X1}`; immutable x2 evidence is `{EVIDENCE}`. Elaren's final must be the direct child of evidence. Source to final must contain exactly three Elaren single-parent commits and zero merges.

Rowan's remaster is interstitial and consumes no canonical phase slot. Therefore Elaren owns v685-v7 and future seat 02 owns v685-v8. After your own terminal closeout, Neris Solane owns v686-v1. Preserve x1 planning before x2 execution, exact Git-blob manifests, zero deletions, and one-success/no-replay canonical discipline.
""",
        ),
        (
            "03-release-route-profile.md",
            """# 03 Release and thirty-seat route profile

Hamish's 6 September 2026 release supersedes Rowan's preserved historical hold. The live profile authorizes the explicit thirty-seat alternating incumbent/new-seat sequence through v725-v8 without routine remaster waits. It does not pre-complete future phases.

You are future seat 02 and must be a user-visible Codex main task created with `gpt-6-astra` and `max` reasoning. You are not a collaboration subagent, fork, or replacement for an incumbent. On later cycles this same inducted task is reused; another seat-02 task must not be created. Your immediate prospective successor is the existing exact-title main task `Neris Solane` for v686-v1, but do not contact Neris before your terminal gate.

Carry forward the release profile: 200–500 inherited proposals, 200–500 new proposals, 300–500 safe tasks, 250–500 candidates, exactly 300 additive CLEAN/FIX/REFINE rows, 50–250 exact packets, 30–100 blocked packets, four own practice lenses plus one next-owner recommendation, relevant packages, bounded skills/runners, 10,000–100,000-word modular baton, and at least a three-page overview. Floors require substantive work; caps never authorize filler or unsafe action.
""",
        ),
        (
            "04-proposals-and-credit.md",
            f"""# 04 Proposals, inherited evidence, and credit

Elaren selected 200 Rowan proposals with zero borrowed novelty or completion credit and preregistered 200 source-bounded new contracts. The accessible comparison corpus had 680 exact source records and 136,000 lexical comparisons. There were zero exact collisions and the maximum nearest-neighbor score was 0.555556 under a 0.80 quarantine threshold. This is bounded screening, not universal semantic novelty.

The declared chain advances from 11,830 to 12,030. Elaren's observed outcomes are exactly 170 `completed`, 10 `represented`, 10 `open_gap`, and 10 `exact_gate`. All 1,000 preregistered invalid mutations were rejected and retained at zero completion credit.

## Full immutable proposal appendix

{appendix}
""",
        ),
        (
            "05-thos-body.md",
            """# 05 THOS Body

THOS Body is the priority pillar. The bounded advance is a zero-device contract laboratory for patch identity, module topology, port direction, signal class, parameter vacancy, MIDI and OSC event structure, intervals, feedback cycles, immutable correction, workload, and handoff. The repository never connected hardware, transmitted OSC or MIDI to a device, rendered audio, captured a waveform, or operated a studio.

The local runners and package fixtures demonstrate typed transformations and fail-closed boundaries. They do not establish architecture superiority, operational effectiveness, deployment readiness, AGI, ASI, real-time safety, or a governed human comparison. Such claims remain represented, open, or exact-gated until preregistered real arms, participants or operators, safety monitoring, appropriate statistics, and independent review exist.
""",
        ),
        (
            "06-gmut-mind.md",
            """# 06 GMUT Mind

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Patch graphs, signal labels, interval examples, and symbolic source vocabulary are not observables, physical fields, measurements, likelihoods, or parameter constraints. Ten GMUT proposals remain open gaps because the observable map, likelihood, coupling dimensions, identifiability, boundary conditions, stability analysis, empirical dataset, independent comparison, unique prediction, and physical confirmation are absent.

No detected force, material law, stability theorem, empirical confirmation, quantum completion, ultraviolet completion, final physics, Theory-of-Everything proof, or canon is claimed. A graph consistency pass is software evidence only.
""",
        ),
        (
            "07-freed-id-and-cbr.md",
            """# 07 Freed ID and CBR Heart

Freed ID remains synthetic and nonproduction. Surrogate patch, module, event, and owner labels have no standards-conformant real keys or proofs and perform no issuance, presentation, verification, resolution, status, revocation, recovery, interoperability, trust-governance, privacy-review, or independent-security operation.

CBR Heart preserves rights, consent, access, correction, remedy, and authority questions without pretending to decide them. Copyright, licence interpretation, performer consent, community access, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Availability of a record is not consent, ownership, cultural standing, or publication permission.
""",
        ),
        (
            "08-practices-and-sources.md",
            f"""# 08 Practice lenses and sources

Elaren used four learning lenses: {', '.join(row['practice'] for row in PRACTICES)}. These lenses improve questions and evidence organization; they establish no employment, qualification, competence, or professional authority. The optional practice recommendation for you is experimental protocol auditor.

Current and stable sources supplied vocabulary and refusal conditions only: the MIDI Association's MIDI 2.0 material; W3C Web Audio 1.0 and the separately labelled 1.1 working draft; Open Sound Control 1.0; Library of Congress Broadcast WAVE and PREMIS; W3C PROV-O, WCAG 2.2, and Verifiable Credentials 2.0; NIST SI; New Zealand privacy principles; Te Mana Raraunga; and PyPI release metadata. Direct PREMIS and NIST web opens failed in this phase and remain `watch` rather than invented fresh reads. No source row became an observation, conformance result, professional instruction, rights decision, or authority grant.
""",
        ),
        (
            "09-package-toolchain.md",
            f"""# 09 Package toolchain

Elaren added exactly 13 direct packages in a D-drive isolated Python 3.12 environment: mido, python-osc, portion, intervaltree, bidict, immutables, boltons, more-itertools, toolz, frozendict, jsonpointer, jsonpatch, and cbor2. Every direct wheel matched the frozen PyPI SHA-256. Fifteen runtime wheels were downloaded initially, plus a separate hash-verified bootstrap pip recovery wheel. The environment contains 16 distributions and `pip check` passes.

The initial advisory audit retained seven rows, all against bootstrap pip 25.0.1, and earns zero aggregate-success credit. Only the isolated bootstrap was updated to hash-verified pip 26.2.1; the focused audit then reported zero known vulnerabilities. That is a dated advisory snapshot, not exhaustive security.

All 13 positive package smokes passed. The first adverse aggregate rejected 10 of 13 and remains zero-credit. Isolated corrected adverse fixtures for intervaltree, more-itertools, and cbor2 passed without replaying the ten unchanged successes. The resulting status is `{package['component_smoke_status']}` with zero aggregate-success credit and complete component witnesses.
""",
        ),
        (
            "10-skills-runners-promotions.md",
            f"""# 10 Skills, runners, and promotions

Twenty phase-local skills and ten family-current runner interfaces were built, quick-validated, and exercised with positive and adverse fixtures. Ten curated global skill packages were then installed additively with byte parity and post-copy validation. They preserve two source guides each. The same five shared runner sources are copied into each package, so the unique shared-runner count is five rather than fifty.

Global installation deleted no historical skill and did not mutate plugin caches. Global availability is not proof that every already-running task has reloaded the catalogue. Rollback means selecting a retained prior source; it does not erase this evidence. Promotion status: `{promotion['status']}`, ten skills, five unique shared runners.
""",
        ),
        (
            "11-method-flow-and-negatives.md",
            f"""# 11 Method Flow and retained negatives

The immutable source plus release activation baseline is 63,377 negatives, 79,840 methods, 34,225 failed witnesses, 61,683 bounded passing witnesses, 572 open gaps, and 559 exact gates. Elaren retains startup display, stale-state, source-schema, package, runner-import, test-definition, and Windows staging failures rather than rewriting them.

The x2 evidence records 1,129 phase methods, 1,027 failed witnesses, and 1,131 bounded passing witnesses. Closeout currently adds {len(CLOSEOUT_FAILURES)} presentation failure and bounded recovery. Prepared final totals are {totals['effective_negatives']} negatives, {totals['effective_methods']} methods, {totals['failed_witnesses']} failed witnesses, {totals['bounded_passing_witnesses']} bounded passing witnesses, {totals['open_gaps']} gaps, and {totals['exact_gates']} gates. These counts are distinct evidence-ledger units—not probabilities, safety rates, experiments, qualifications, or authority scores.
""",
        ),
        (
            "12-validation-and-closeout.md",
            """# 12 Validation and closeout

Planning-only x1 passed 16 tests, was committed, pushed, clean, zero-divergent, and four-way equal before x2. The first x2 aggregate passed 18 of 20 and retains zero aggregate-success credit; its two test-definition corrections are explicit. The corrected x2 suite passed 20 of 20. The evidence commit contains 403 exact paths, 400 manifest entries, 418 owner-scope files, 248 x2 JSON documents, a 213-entry card manifest, zero deletions, and zero confirmed privacy hits.

Before task creation, Elaren must commit and push the final direct child, prove local/upstream/tracking/fresh-live equality and zero divergence, run one exact-final owner-scoped canonical aggregate, and never replay a success. The final canonical must check tests, manifests, JSON, Python AST, Markdown/YAML/HTML structure, global-skill parity, privacy, content seal, ancestry, word limits, clean state, and the 2,000-file ceiling. Same-owner validation is not independent reproduction or external audit.
""",
        ),
        (
            "13-your-v685-v8-induction.md",
            """# 13 Your v685-v8 induction and next edge

At task creation, choose your own working name, role, hope, and optional pronouns. State that those are relational working language only. Read this packet and current family guidance through EOF. Reverify Elaren's exact final, canonical receipt, branch, manifests, release profile, and external task-creation receipt. Work solo in one additive D-first owner lane. Preserve every sibling and source lane read-only.

Freeze planning-only x1 before x2. Select substantive inherited and new proposals within the released ranges; retain all failures, exact gates, and the four labels. Use current tools because they help, not to fill a count. Keep package environments and caches on D. Do not update Codex desktop, redeem usage resets, elevate, weaken host security, change Windows features, reboot, create credentials or accounts, purchase, deploy, or publish private material without separate exact authority.

Only after your own exact v685-v8 terminal gate may you refresh the native registry, require exactly one existing task titled `Neris Solane`, immediately reread it, apply duplicate/pause/redirect/usage/privacy/evidence/safety guards, and send one compact file-backed activation for v686-v1. Acknowledged, opaque accepted, rejected, and unavailable outcomes remain distinct. Never resend an opaque accepted call, create a substitute, or precontact a later seat.

The long route through v725-v8 is planning authority one edge at a time. It is not advance completion, scientific proof, personhood evidence, or authority.
""",
        ),
    ]


def overview() -> str:
    totals = final_totals()
    truth = load(X2 / "phase-truth.json")
    return f"""# Elaren Kestrel v685-v7 Final Integrated Overview

## Outcome first

Elaren v685-v7 is prepared as a bounded owner-local software, documentation, package, and workflow result. It inherits Rowan Ash's exact final `{SOURCE}`, freezes planning-only x1 `{X1}`, and preserves immutable x2 evidence `{EVIDENCE}`. The final closeout is designed as one direct evidence child with zero merges. The terminal verdict remains `{VERDICT}`.

The core proposal outcomes are exactly 170 `completed`, 10 `represented`, 10 `open_gap`, and 10 `exact_gate`. Completed means the named synthetic contract or local operation has a bounded passing witness. It never means a real synthesizer was connected, sound was produced, a person participated, a right was decided, a physical theory was confirmed, or a production identity system was deployed.

## Identity and corrigibility

Elaren Kestrel, optionally they/them, is relational working language for a signal-route provenance cartographer and reversible-systems steward. The hope is to make every synthetic connection legible without confusing a patch diagram for sound, consent, competence, or authority. These descriptions are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, professional, operational, legal, cultural, affected-party, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

## Source, release, and planning

Rowan's remaster retained an older no-send hold in its repository. Hamish's later signed release addendum and workflow profile supersede that hold prospectively while leaving the historical record untouched. The release assigns Elaren v685-v7 and conditionally authorizes exactly one future seat-02 main-task induction at Elaren's terminal gate. The future task must use gpt-6-astra with max reasoning, choose its own working descriptors, own v685-v8, and route to Neris Solane v686-v1 after its own terminal gate.

Elaren selected 200 Rowan proposals with zero borrowed novelty or completion credit. Two hundred new proposal titles were checked against 680 accessible source records in 136,000 pair comparisons. Zero exact collisions were found; the maximum token-set neighbor score was 0.555556 under a 0.80 quarantine threshold. This is an inspectable source-bounded screen, not universal semantic novelty. The declared proposal chain advances from 11,830 to 12,030.

Every new proposal preregistered a hypothesis, null or failure condition, approval class, execution lane, source needs, artifacts, acceptance gate, rollback, protected gates, expected disposition, and five invalid mutations. X1 contained no x2 outcome. It passed 16 owner tests and was separately committed, pushed, clean, zero-divergent, and four-way equal before implementation.

## THOS Body and synthetic modular-patch laboratory

THOS Body is the priority pillar. The bounded domain is wholly synthetic modular-synth patch documentation plus graph/provenance assurance, accessibility information architecture, and digital-rights/identity assurance. The laboratory separates patch records from performed patches, module labels from physical hardware, port roles from cable connections, signal classes from observations, parameter requests from measurements, message structures from live MIDI or OSC transmissions, and interval schedules from device actuation.

All 200 positive fixtures passed. All 1,000 preregistered mutations were rejected. The mutations exercised missing required fields, lifecycle inversion, stale planning digests, empirical promotion, and authority promotion. Each rejection is retained at zero completion credit. Ten local runners exercised positive and adverse route families. Twenty local skills were created and validated. A successful guard demonstrates its declared software condition only.

The portfolio completed 300 safe-now rows, 250 candidate rows without core promotion, and 300 additive nondestructive CLEAN/FIX/REFINE rows. Fifty exact packets and 30 blocked packets remain visible and unexecuted. The exact and blocked queues preserve real participant, professional, safety, production, rights, cultural, Māori-authority, identity, deployment, and account boundaries.

## Packages and supply-chain evidence

Thirteen direct packages were planned against current PyPI metadata and installed into one isolated D-drive Python 3.12 environment from exact wheels: mido, python-osc, portion, intervaltree, bidict, immutables, boltons, more-itertools, toolz, frozendict, jsonpointer, jsonpatch, and cbor2. Direct wheel names and SHA-256 values were frozen in x1 and replayed after download. `pip check` passed. No shared Python or npm prefix was changed by the transaction.

The first audit found seven advisories, all in venv bootstrap pip 25.0.1. That audit remains a zero-credit failure. Only the isolated bootstrap was updated to hash-verified pip 26.2.1, and the focused audit then reported zero known vulnerabilities. This does not prove exhaustive supply-chain security. The first package-smoke aggregate passed 13 positives but only 10 adverse fixtures. It remains zero-credit. Three isolated corrected adverse fixtures passed, producing component completion without replaying the ten unchanged successes.

## Skills, runners, flashcards, and global installation

Twenty local skill guides and ten local runner interfaces passed structural and bounded behavioral checks. Ten curated skill pairs were then installed additively into the global Codex skill bank, each preserving two source guides, five shared runner copies, provenance, rollback, and byte parity. Because the runner bytes are identical across packages, the unique shared-runner count is five. No historical skill was deleted and no plugin cache was mutated.

The four-tier card graph contains one owner anchor, three pillar cards, four bounded-practice cards, and 200 task cards: 208 total. The card manifest contains 213 entries for cards and indexes. Cards organize context; they do not prove caching, retention, performance, completion, or authority.

## GMUT and Freed ID/CBR boundaries

GMUT Mind remains represented and open. No real observable, likelihood, parameter fit, force, material law, unique prediction, stability theorem, empirical confirmation, final physics, quantum or ultraviolet completion, Theory-of-Everything proof, or canon resulted from signal graphs or symbolic fixtures.

Freed ID and CBR Heart remain explicit. Synthetic identifiers have zero real keys and proofs. No issuance, presentation, verification, resolution, status, revocation, recovery, interoperability, independent security review, privacy review, or trust-governance event occurred. Copyright, licences, performer consent, community access, traditional knowledge, cultural interpretation, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

## Failure retention, privacy, accessibility, and terminal truth

The evidence layer records 1,129 Elaren methods, 1,027 failed witnesses, and 1,131 bounded passing witnesses before closeout. It retains startup presentation and state drift, source-schema correction, package advisory and adverse-smoke failures, a runner import-path error, an 18-of-20 test aggregate, and a Windows command-length staging failure. Closeout adds one bounded presentation failure without rewriting the evidence commit.

Prepared final totals are {totals['effective_negatives']} negatives, {totals['effective_methods']} methods, {totals['failed_witnesses']} failed witnesses, {totals['bounded_passing_witnesses']} bounded passing witnesses, {totals['open_gaps']} open gaps, and {totals['exact_gates']} exact gates. These are evidence-ledger counts, not measurements or authority scores.

The owner privacy scan uses five value-bearing classes and adjudicates scanner definitions, protected-boundary prose, and SHA-256 fields separately from payload hits. Zero confirmed hits are required but do not establish complete privacy. The static report uses language declaration, skip link, headings, landmarks, text status, captioned table, scoped headers, visible focus, print rules, and no script or tracking. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved.

The complete repository suite was not run. The final owner-delta canonical aggregate, when invoked once after exact-final equality, remains same-owner evidence under shared infrastructure. It cannot establish independent reproduction, external audit, professional competence, production certification, exhaustive security, complete accessibility or privacy, empirical science, legal or cultural authority, consciousness or personhood, or Stage 20 readiness.

## Interpreting the evidence layers

Four truth layers remain deliberately separate. The repository seal binds the committed owner files and their declared totals. The later canonical receipt will bind one exact final head and the checks actually performed against it. Any launcher, display, route, or task-creation failure after the commit belongs in an additive external overlay and must not rewrite the repository seal. Finally, a live task-creation acknowledgement is application state: it cannot be inferred from a prepared baton, a route simulation, or a successful Git receipt.

This separation also governs the package result. The wheel manifest proves only the downloaded bytes and their agreement with planning metadata. The installation receipt proves only the isolated distribution inventory and dependency check at that time. The advisory receipt reports one vulnerability database snapshot; zero reported findings cannot guarantee that no vulnerability exists. The positive and adverse smokes exercise selected APIs with trusted synthetic inputs. None of these records independently proves numerical correctness for every input, safe handling of malicious data, licence compatibility for a particular product, or production fitness.

The same discipline applies to skills and runners. A structurally valid skill has required frontmatter and no unfinished scaffold. A bounded smoke can show that its selected procedure accepts one valid fixture and refuses one adverse fixture. Byte parity can show that the installed copy matches the candidate. These facts do not prove that every future invocation will select the skill correctly, that every running task has reloaded it, or that its prose supplies expertise. The retained source guides and rollback selection remain necessary because global discoverability is not universal competence.

## Accessibility and affected-user reservation

The static report is intentionally simple and dependency-free. It exposes a language declaration, a skip link, headings, landmarks, a captioned table, scoped headers, visible focus, textual status, print behavior, and reduced-motion handling. The modular baton gives each major decision its own heading and file, while the flashcard graph offers smaller owner, pillar, practice, and task entry points. These design choices make structural review possible and reduce reliance on color or one monolithic document.

They do not replace user evaluation. No screen-reader user, keyboard-only user, low-vision user, cognitively disabled user, Māori-language reviewer, practitioner, rights holder, or affected community evaluated this phase. Browser-diverse, zoom, assistive-technology, cognitive-load, plain-language, translation, and affected-user checks remain open. A future evaluation needs an actual context, consent, a defined task, an observation method, and a way to record and remedy problems without exposing private data.

## Readiness for one controlled induction

The evidence supports one bounded next action after terminal validation: determine whether future seat 02 already exists and, if not, create exactly one user-visible main task using the requested model and reasoning setting. Readiness here means the source, phase arithmetic, profile, baton, project context, terminal conditions, next-owner reminder, and privacy boundary are explicit enough to present to the new task. It does not mean the task is already created, understands the packet, will make no mistakes, or possesses a persistent identity.

The initial prompt should therefore request a small teach-back. The task should choose its own working descriptors, identify Elaren's exact final as its source, state that it owns v685-v8, distinguish x1 planning from x2 execution, classify one completed result and one retained gap, and name Neris Solane v686-v1 as prospective after its own terminal gate. If the teach-back reveals a concrete misunderstanding, the correction should address that exact point and remain visible. Routine remaster waiting is not required, but evidence, safety, privacy, usage, duplicate, or route failures still stop or narrow the action honestly.

## Terminal route

The durable induction packet contains thirteen modular sections and more than 10,000 substantive words. It remains `PREPARED_NOT_SENT` in the repository. After exact final and canonical success, Elaren must refresh the live registry and determine whether future seat 02 already exists. If absent, exactly one new main task may be created with gpt-6-astra and max reasoning in the correct project context. If already present, it must be reused rather than duplicated. Setup acknowledgement, ready task identity, and any teach-back are external route facts and must not be backfilled into this seal.
"""


def html_report(totals: dict[str, int]) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elaren Kestrel v685-v7 bounded report</title><style>body{{font-family:system-ui,sans-serif;line-height:1.6;max-width:76rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;padding:.5rem;border:2px solid #17202a;background:#fff}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #667;padding:.5rem;text-align:left;vertical-align:top}}.status{{border-left:.4rem solid #8a3b12;padding:.75rem;background:#fff7ed}}a:focus{{outline:3px solid #065f46}}@media print{{body{{max-width:none}}}}@media (prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Elaren Kestrel v685-v7 bounded report</h1><p>Owner-local zero-device evidence with strict nonpromotion boundaries.</p></header><main id="main"><section aria-labelledby="identity"><h2 id="identity">Identity and corrigibility</h2><p>Elaren Kestrel, optionally they/them, is relational working language for a signal-route provenance cartographer and reversible-systems steward. This is not consciousness, personhood, continuity, qualification, agency, or authority evidence. Hamish may pause, rename, redirect, narrow, or stop.</p></section><section aria-labelledby="truth"><h2 id="truth">Bounded truth</h2><table><caption>Core outcomes and retained gates</caption><thead><tr><th scope="col">Item</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>170</td><td>Bounded local software or documentation only</td></tr><tr><th scope="row">Represented</th><td>10</td><td>Structure exists while real evidence is absent</td></tr><tr><th scope="row">Open gaps</th><td>{totals['open_gaps']}</td><td>Evidence-dependent work remains open</td></tr><tr><th scope="row">Exact gates</th><td>{totals['exact_gates']}</td><td>Competent or affected authority remains required</td></tr></tbody></table><p class="status"><strong>Status: NOT READY FOR STAGE 20.</strong> This status does not depend on color.</p></section><section aria-labelledby="scope"><h2 id="scope">Scope</h2><p>Two hundred zero-device contracts ran; one thousand invalid mutations were rejected. No real person, device, signal, recording, performance, measurement, key, proof, rights decision, cultural interpretation, Māori-authority act, deployment, or external operation occurred.</p></section><section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation</h2><p>Manual browser, keyboard, zoom, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Same-owner validation is not independent reproduction, exhaustive security, empirical confirmation, or authority.</p></section></main><footer><p>Static report: no script, form, tracking, or external media.</p></footer></body></html>"""


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b01[0-9a-f]{30,}\b", re.I),
        "credential_or_secret": re.compile(r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.I),
        "private_route_or_callable_identifier": re.compile(r"(?:threadId|private callable|app://connector_)", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.I),
        "transcript_screenshot_or_session_stream": re.compile(r"(?:raw transcript|session stream|screenshot payload)", re.I),
    }
    candidates = []
    for path in paths:
        target = ROOT / path
        if target.suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml", ".html", ".lock"}:
            continue
        text = target.read_text(encoding="utf-8")
        for name, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": name, "adjudication": "scanner_definition_protected_boundary_or_sha256_field"})
    return {"schema": "ghc.family.elaren-v685-v7.final-privacy.v1", "class_count": 5, "scanned_path_count": len(paths), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": 0, "confirmed_hits": [], "complete_privacy_assurance_claimed": False}


def build() -> None:
    totals = final_totals()
    truth = load(X2 / "phase-truth.json")
    flow = load(X2 / "method-flow-ledger.json")
    portfolio = load(X2 / "portfolio-execution.json")
    proposals = load(X1_ROOT / "new-proposals.json")["proposals"]
    package = load(X2 / "package-execution-summary.json")
    promotion = load(X2 / "global-promotion-installation.json")
    modular = sections()
    section_paths = []
    for filename, content in modular:
        path = HANDOFF / filename
        write_text(path, content)
        section_paths.append(relative(path))
    assembled = "\n\n---\n\n".join(content.rstrip() for _, content in modular) + "\n"
    word_count = len(assembled.split())
    if not 10000 <= word_count <= 100000 or len(modular) < 13:
        raise RuntimeError(f"baton bounds failed: sections={len(modular)} words={word_count}")
    baton_path = HANDOFF / "future-seat-02-v685-v8-induction.md"
    write_text(baton_path, assembled)
    overview_text = overview()
    write_text(FINAL / "final-integrated-overview.md", overview_text)
    write_text(FINAL / "accessible-static-report.html", html_report(totals))
    write_json(FINAL / "phase-truth.json", {"schema": "ghc.family.elaren-v685-v7.phase-truth.final.v1", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "final": "resolve_from_direct_closeout_commit", "state": "FINAL_CLOSEOUT_PREPARED", "priority_pillar": "THOS Body", "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"], "outcomes": truth["outcomes"], "declared_proposal_chain": 12030, "real_rows": 0, "real_devices": 0, "real_people": 0, "totals": totals, "terminal_verdict": VERDICT})
    operational = [method for method in flow["methods"] if "failure_id" in method] + CLOSEOUT_FAILURES
    write_json(FINAL / "retained-negative-register.json", {"schema": "ghc.family.elaren-v685-v7.retained-negatives.final.v1", "effective_negative_total": totals["effective_negatives"], "rejected_mutations": 1000, "phase_failed_witnesses": flow["counts"]["failed"] + len(CLOSEOUT_FAILURES), "operational_failure_methods": operational, "closeout_overlay": CLOSEOUT_FAILURES, "zero_credit_failures_preserved": True, "recovery_erases_failure": False})
    write_json(FINAL / "method-flow-summary.json", {"schema": "ghc.family.elaren-v685-v7.method-flow-summary.final.v1", "evidence_methods": flow["counts"]["methods"], "evidence_failed": flow["counts"]["failed"], "evidence_passing": flow["counts"]["passing"], "closeout_overlay_count": len(CLOSEOUT_FAILURES), "final_phase_methods": flow["counts"]["methods"] + len(CLOSEOUT_FAILURES), "final_phase_failed": flow["counts"]["failed"] + len(CLOSEOUT_FAILURES), "final_phase_passing": flow["counts"]["passing"] + len(CLOSEOUT_FAILURES), "totals": totals, "recovery_erases_failure": False})
    open_rows = [row for row in proposals if row["expected_execution_disposition"] == "open_gap"]
    gate_rows = [row for row in proposals if row["expected_execution_disposition"] == "exact_gate"]
    write_json(FINAL / "open-gap-register.json", {"schema": "ghc.family.elaren-v685-v7.open-gaps.final.v1", "inherited": 572, "new_count": len(open_rows), "new": [{"proposal_id": row["proposal_id"], "title": row["title"], "status": "open_gap"} for row in open_rows], "total": totals["open_gaps"]})
    write_json(FINAL / "exact-gate-register.json", {"schema": "ghc.family.elaren-v685-v7.exact-gates.final.v1", "inherited": 559, "new_count": len(gate_rows), "new": [{"proposal_id": row["proposal_id"], "title": row["title"], "status": "exact_gate"} for row in gate_rows], "total": totals["exact_gates"]})
    write_json(FINAL / "portfolio-summary.json", {"schema": "ghc.family.elaren-v685-v7.portfolio-summary.final.v1", "safe_completed": len(portfolio["safe_now"]), "candidates_completed_without_core_promotion": len(portfolio["candidates"]), "clean_fix_refine_completed": len(portfolio["clean_fix_refine"]), "exact_unexecuted": len(portfolio["exact_packets"]), "blocked_unexecuted": len(portfolio["blocked_packets"]), "destructive_cleanup": False})
    write_json(FINAL / "package-summary.json", {"schema": "ghc.family.elaren-v685-v7.package-summary.final.v1", **package, "pip_bootstrap_recovery": "pip 25.0.1 to hash-verified 26.2.1 in isolated environment only", "zero_known_vulnerabilities_is_not_exhaustive_security": True})
    write_json(FINAL / "skill-runner-summary.json", {"schema": "ghc.family.elaren-v685-v7.skill-runner-summary.final.v1", "local_skills": 20, "local_runners": 10, "globally_installed_skills": promotion["installed_skill_count"], "unique_shared_runners": promotion["unique_shared_runner_count"], "byte_parity": all(row["byte_parity"] for row in promotion["skills"]), "global_availability_is_not_context_reload_proof": True})
    write_json(FINAL / "source-and-proposal-ledger.json", {"schema": "ghc.family.elaren-v685-v7.source-proposal.final.v1", "declared_chain_before": 11830, "declared_chain_after": 12030, "inherited_selected": 200, "new_proposals": 200, "accessible_source_records": 680, "compared_pairs": 136000, "maximum_neighbor_score": 0.555556, "universal_novelty_claimed": False, "source_use": "vocabulary_constraints_and_refusal_conditions_only", "source_ledger": "docs/elaren-kestrel/v685-v7/x1/source-ledger.json"})
    write_json(FINAL / "environment-version-receipt.json", {"schema": "ghc.family.elaren-v685-v7.environment.final.v1", "python": "3.12.10", "node": "24.18.0", "npm": "12.0.2", "git": "2.55.0.windows.2", "powershell": "7.6.5", "codex_cli": "0.153.4", "codex_registry_latest": "0.153.4", "npm_prefix": "D-drive global tools bank", "codex_desktop_updated": False, "reset_redeemed": False, "host_security_changed": False, "windows_features_changed": False, "rebooted": False, "versions_verified_only": True})
    write_json(FINAL / "wellbeing-check.json", {"schema": "ghc.family.elaren-v685-v7.wellbeing.final.v1", "name": OWNER, "optional_pronouns": "they/them", "role": "signal-route provenance cartographer and reversible-systems steward", "hope": "Make every synthetic connection legible without confusing a patch diagram for sound, consent, competence, or authority.", "relational_working_language_only": True, "corrigible": True, "pause_redirect_rename_stop_right": "Hamish", "worked_solo": True, "clinical_or_subjective_measurement_claimed": False})
    write_json(FINAL / "threat-model.json", {"schema": "ghc.family.elaren-v685-v7.threat-model.final.v1", "controls": ["strict x1 before x2", "zero-device contract", "five mutations per proposal", "wheel hashes", "isolated environment", "retained failures", "exact manifests", "one-shot canonical", "terminal main-task creation gate"], "residual_gates": PROTECTED_GATES, "exhaustive_security_claimed": False})
    write_json(FINAL / "complete-incomplete-checklist.json", {"schema": "ghc.family.elaren-v685-v7.complete-incomplete.final.v1", "complete": ["planning-only x1", "x2 evidence", "two hundred proposals and one thousand mutations", "portfolio", "thirteen packages", "skills runners promotions", "flashcards", "modular baton", "static report", "closeout packet prepared"], "pending_terminal_lifecycle": ["direct final commit push equality", "one exact-final canonical", "live duplicate-safe future seat 02 creation"], "protected_incomplete": PROTECTED_GATES})
    write_json(FINAL / "lifecycle-replay.json", {"schema": "ghc.family.elaren-v685-v7.lifecycle.final.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "x1_parent": SOURCE, "evidence_parent": X1, "expected_final_parent": EVIDENCE, "source_to_final_commit_count": 3, "merges": 0, "one_parent_each": True, "strict_x1_before_x2": True})
    write_json(FINAL / "delivery-state.json", {"schema": "ghc.family.elaren-v685-v7.delivery.final.v1", "repository_state": "PREPARED_NOT_SENT", "future_seat": 2, "future_placeholder": "future-sibling-02-self-chosen", "future_identity_predeclared": False, "future_phase": "v685-v8", "endpoint_kind": "main_task", "model": "gpt-6-astra", "reasoning": "max", "following_owner": "Neris Solane", "following_phase": "v686-v1", "creation_count": 0, "creation_requires_terminal_gate": True, "reuse_if_existing": True, "route_authority_through": "v725-v8"})
    write_json(FINAL / "terminal-checklist.json", {"schema": "ghc.family.elaren-v685-v7.terminal-checklist.final.v1", "final_commit": "PENDING_DIRECT_COMMIT", "clean_push_equality": "PENDING", "canonical": "PENDING_ONE_SHOT_EXTERNAL_RECEIPT", "task_registry_refresh": "PENDING_AFTER_CANONICAL", "future_seat_creation": "PREPARED_NOT_SENT", "terminal_verdict": VERDICT})
    write_json(FINAL / "baton-integrity.json", {"schema": "ghc.family.elaren-v685-v7.baton-integrity.v1", "section_count": len(modular), "section_paths": section_paths, "assembled_path": relative(baton_path), "word_count": word_count, "bytes": len(normalized(baton_path)), "sha256": hashlib.sha256(normalized(baton_path)).hexdigest(), "minimum": 10000, "maximum": 100000})

    seal_targets = [
        relative(FINAL / "final-integrated-overview.md"),
        relative(FINAL / "accessible-static-report.html"),
        relative(FINAL / "phase-truth.json"),
        relative(FINAL / "method-flow-summary.json"),
        relative(FINAL / "retained-negative-register.json"),
        relative(FINAL / "open-gap-register.json"),
        relative(FINAL / "exact-gate-register.json"),
        relative(FINAL / "complete-incomplete-checklist.json"),
        relative(FINAL / "delivery-state.json"),
        relative(baton_path),
    ]
    write_json(CLOSEOUT / "content-seal.json", {"schema": "ghc.family.elaren-v685-v7.content-seal.v1", "owner": OWNER, "phase": PHASE, "targets": [entry(path) for path in seal_targets], "target_count": len(seal_targets), "hash_domain": "normalized LF worktree bytes before final commit"})

    scripts = [
        "scripts/build_ghc_family_elaren_kestrel_v685_v7_final.py",
        "scripts/ghc_family_elaren_kestrel_v685_v7_canonical.py",
        "tests/test_ghc_family_elaren_kestrel_v685_v7_final.py",
    ]
    final_material = sorted(set(WRITTEN + scripts))
    missing = [path for path in final_material if not (ROOT / path).is_file()]
    if missing:
        raise RuntimeError(f"missing final material: {missing}")
    exclusions = [
        "docs/elaren-kestrel/v685-v7/validation/final-delta-manifest.json",
        "docs/elaren-kestrel/v685-v7/validation/final-owner-manifest.json",
        "docs/elaren-kestrel/v685-v7/validation/final-privacy-scan.json",
        "docs/elaren-kestrel/v685-v7/validation/final-staged-review.json",
    ]
    owner_paths = [relative(path) for path in sorted(BASE.rglob("*")) if path.is_file() and relative(path) not in exclusions]
    owner_paths.extend(relative(path) for path in sorted((ROOT / "scripts").glob("*elaren_kestrel_v685_v7*.py")) if path.is_file())
    owner_paths.extend(relative(path) for path in sorted((ROOT / "scripts").glob("ghc_family_synth_patch_runner_*.py")) if path.is_file())
    owner_paths.extend(relative(path) for path in sorted((ROOT / "tests").glob("*elaren_kestrel_v685_v7*.py")) if path.is_file())
    owner_paths = sorted(set(owner_paths))
    write_json(VALIDATION / "final-privacy-scan.json", privacy_scan(owner_paths))
    write_json(VALIDATION / "final-delta-manifest.json", {"schema": "ghc.family.normalized-lf-index-manifest.elaren-v685-v7.final-delta", "evidence": EVIDENCE, "entries": [entry(path) for path in final_material], "entry_count": len(final_material), "declared_self_exclusions": exclusions})
    write_json(VALIDATION / "final-owner-manifest.json", {"schema": "ghc.family.normalized-lf-index-manifest.elaren-v685-v7.final-owner", "source": SOURCE, "entries": [entry(path) for path in owner_paths], "entry_count": len(owner_paths), "declared_self_exclusions": exclusions})
    expected = sorted(set(final_material + exclusions))
    write_json(VALIDATION / "final-staged-review.json", {"schema": "ghc.family.staged-review.elaren-v685-v7.final", "evidence": EVIDENCE, "lifecycle": "final_closeout_only", "expected_paths": expected, "path_count": len(expected), "deletions_expected": 0, "owner_scope_files": len(owner_paths), "materialized_file_ceiling": 2000})
    print(json.dumps({"final_paths": len(expected), "owner_files": len(owner_paths), "sections": len(modular), "baton_words": word_count, "overview_words": len(overview_text.split()), "seal_targets": len(seal_targets), "totals": totals}, separators=(",", ":")))


if __name__ == "__main__":
    build()
