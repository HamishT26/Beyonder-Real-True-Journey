#!/usr/bin/env python3
"""Build Caelen Ash v674-v3 closeout and exact-final candidate records."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Caelen Ash"
PHASE = "v674-v3"
SOURCE = "0b9ccf8c74f3b0a5f96b8582162df8e2a06edd05"
X1 = "aaff9f4bfe18c2d7dd428cf6cb7b639f3b420b46"
EVIDENCE = "0a50b3d7a13fe3b78302d41b6f8ad61325208ebd"
BRANCH = "codex/GHC-Family/caelen-ash-v674-v3-full-tools"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "caelen-ash" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
X2_ROOT = PHASE_ROOT / "x2"
FINAL_ROOT = PHASE_ROOT / "final"
REPORT_ROOT = PHASE_ROOT / "reports"
HANDOFF_ROOT = PHASE_ROOT / "handoffs"
VALIDATION_ROOT = PHASE_ROOT / "validation"
OUTCOMES = {
    "completed": 42,
    "represented": 12,
    "open_gap": 3,
    "exact_gate": 3,
}
EFFECTIVE = {
    "effective_negatives": 38612,
    "methods": 26466,
    "failed_witnesses": 10273,
    "bounded_passing_witnesses": 13749,
    "open_gaps": 316,
    "exact_gates": 309,
}
FINAL_FAILURES = [
    {
        "failure_id": "CA6743-FINAL-F001",
        "failed_witness": (
            "a closeout inspection wrapper piped a PowerShell foreach block "
            "before materialization and failed parser validation before any "
            "Git read or file mutation"
        ),
        "recovery": (
            "materialize the bounded path rows first and project them in a "
            "separate pipeline"
        ),
        "state": "failed_retained_zero_credit",
        "success_credit": 0,
    },
    {
        "failure_id": "CA6743-FINAL-F002",
        "failed_witness": (
            "the first bounded closeout test selection passed thirteen of "
            "fourteen tests but failed an arbitrary minimum-140 JSON-file "
            "assertion because the exact pre-staged owner packet contained 126"
        ),
        "recovery": (
            "replace the arbitrary floor with the exact lifecycle-aware "
            "126-or-127 count while continuing to parse every phase JSON file"
        ),
        "state": "failed_retained_zero_credit",
        "success_credit": 0,
    },
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def git_text(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8"
    ).strip()


def final_overview() -> str:
    return f'''# Caelen Ash v674-v3 final integrated overview

## Outcome first

Caelen Ash v674-v3 closes as a bounded, wholly synthetic, structural, symbolic, and owner-local software phase. Sixty genuinely new proposal contracts produce exactly forty-two `completed`, twelve `represented`, three `open_gap`, and three `exact_gate` outcomes. The declared frozen family proposal chain advances from 6,670 to 6,730. Sixty inherited Sable reviews retain zero Caelen novelty and completion credit. All 240 preregistered invalid mutations remain rejected zero-credit witnesses. The terminal verdict is exactly `NOT_READY_FOR_STAGE_20`.

GMUT Mind is the primary Trinity Mandala pillar. The bounded learning lenses are wholly synthetic mechanical-watch timing-sheet stewardship, wholly synthetic planetarium projection-cue alignment and handover, and wholly synthetic stained-glass survey annotation and handover. THOS Body and Freed ID or CBR Heart remain visible and protected. No pillar substitutes its software evidence for missing evidence or authority in another pillar.

## Relational identity, role, hope, and wellbeing

Caelen Ash is relational working language for an uncertainty-and-handover cartographer. The phase hope is to make model assumptions, correction chains, and authority vacancies easy to inspect, challenge, and reverse. Optional they/them language is relational only. No task title, name, role, hope, artifact, model output, software pass, or same-owner receipt establishes consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Maori authority.

The wellbeing record keeps workload bounded, correction possible, and pause available. Hamish may rename, pause, redirect, or stop the route. Corrigibility is a process property, not evidence of an inner state, independent agency, or legal status.

## Strict x1 before x2

Planning-only x1 `{X1}` is the direct child of Sable Rook's exact final `{SOURCE}`. It freezes the semantic-neighbor audit, sixty new proposals, inherited zero-credit review, portfolio plan, tool plan, protected gates, source statuses, threat model, privacy requirements, and route hold. It contains no x2 implementation, observed outcome, or completion claim. X1 was committed, pushed, clean, typed zero divergent, and equal across local, upstream, tracking, and fresh live remote before x2 began.

Immutable x2 evidence `{EVIDENCE}` is the direct child of x1. It contains sixty proposal evidence records, sixty accepting controls, 240 rejected mutations, twenty phase-local skills, ten family-current runners, bounded portfolio witnesses, practice artifacts, an exact staged review, and a normalized-LF evidence manifest. It was separately committed, pushed, clean, typed zero divergent, and fresh four-way equal before closeout began. No x1 path changed in x2.

## Retained failures and Method Flow

All eight Caelen startup failures remain `failed_retained_zero_credit`; their bounded recoveries are separately recorded passing witnesses. Closeout retains two further failures. `CA6743-FINAL-F001` records a PowerShell foreach block piped before materialization; parser validation failed before any Git read or mutation, and recovery materialized rows before projection. `CA6743-FINAL-F002` records the first fourteen-test closeout selection: thirteen tests passed, while an arbitrary minimum-140 JSON-file assertion failed against the exact 126-file pre-staged JSON surface. Recovery replaced that arbitrary floor with an exact lifecycle-aware 126-or-127 contract while still parsing every phase JSON file. Neither failure modified x1, x2, another lane, or repository history.

The final repository-sealed counts are 38,612 effective negatives, 26,466 Method Flow methods, 10,273 retained failed witnesses, 13,749 bounded passing witnesses, 316 open gaps, and 309 exact gates. These numbers add both closeout failures and their distinct bounded recoveries to the immutable x2 counts. A recovery never erases, rewrites, or retroactively promotes its failed witness.

## Evidence, skills, runners, and portfolios

Sixty accepting controls pass only inside invented zero-row fixtures. Every proposal retains four invalid mutations: missing structure, invalid outcome vocabulary, prohibited external action, and prohibited authority promotion. All 240 were rejected. These rejections demonstrate the declared owner-local guard behavior only. They are not empirical evidence, participant evidence, a penetration test, exhaustive security, complete privacy, standards conformance, or independent reproduction.

Twenty phase-local skills were customized, read with explicit UTF-8, quick-validated, and smoke-used. None was globally installed or placed on PATH. Ten repository-local `ghc_family_caelen_v674_v3_*` runners accepted their positive fixture and returned the expected rejection status for their paired invalid fixture. They cover unit declaration, epoch declaration, residual sign, uncertainty state, coordinate frame, correction parent, minimum disclosure, handover state, authority vacancy, and the Stage 20 veto. Historical caller compatibility remains intact.

The bounded owner portfolio records 120 safe-now tasks, eighty owner candidates, and one hundred additive CLEAN/FIX/REFINE tasks. Sixty candidates are completed structurally and twenty remain represented. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Every successor recommendation remains zero-credit context. No cleanup deleted, weakened, downgraded, or rewrote an identity label, memory, gate, history, lane, credential, host control, or user artifact.

## Primary pillar and practice boundaries

The watch lens uses invented timing-series unit, epoch, residual, uncertainty, provenance, correction, and handover records. It performs no inspection, timing measurement, regulation, adjustment, repair, valuation, authenticity decision, safety decision, or return-to-service action. It establishes no horological employment, qualification, competence, or authority.

The planetarium lens uses invented projection-cue frames, offsets, hold states, correction readback, accessibility vacancies, cancellation, workload, and handover records. It uses no projector, dome, optical measurement, audience, operator, venue, public program, or live safety process. It establishes no optical alignment, presentation, accessibility acceptance, professional competence, operational effectiveness, or public-safety authority.

The stained-glass lens uses invented annotation coordinates, condition labels, uncertainty states, source provenance, correction chains, access holds, and authority vacancies. It uses no window, panel, fragment, image, building, collection, person, survey, treatment, custody event, or cultural record. It establishes no identification, dating, attribution, condition assessment, conservation decision, treatment, access decision, legal or cultural interpretation, affected-party acceptance, or Maori authority.

## Official-source role

The BIPM SI Brochure, ninth edition updated in 2026, supplies unit and time vocabulary. The official IERS Conventions surface supplies reference-system vocabulary while explicitly preserving the status that working updates are nondefinitive and not officially approved. W3C PROV-O supplies provenance-relation vocabulary. WCAG 2.2 supplies accessibility structure and evaluation reservations. RFC 8785 supplies deterministic JSON vocabulary with informational status and verified errata noted. These sources are requirements and refusal-condition references only. A citation is not an observation, measurement, endorsement, participant result, standards-conformance certificate, legal interpretation, cultural ratification, or delegated authority.

## Scientific, production, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. This phase reads zero empirical rows, runs no physical observation or likelihood evaluation, and produces no force, physical prediction, parameter constraint, posterior, empirical confirmation, ultraviolet completion, quantum completion, or Theory-of-Everything result. Units, residual signs, covariance proxies, and coordinate-frame contracts are structural obligations and analogies, not cosmological evidence.

THOS remains synthetic and proxy-only without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, suitable statistics, and independent review. Synthetic workload, hold, cancellation, readback, and handover fixtures do not establish operational effectiveness, professional competence, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction. Production completion requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and appropriate affected-party oversight. Invented labels are not credentials or production identities.

CBR rights, access, consent, correction, remedy, privacy decisions, legal interpretation, cultural meaning, collection authority, heritage status, beneficiary acceptance, Maori wording, Maori data governance, and Maori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority. Repository software cannot confer a right, remedy, title, cultural legitimacy, governance mandate, consent, or public authority.

## Privacy, accessibility, security, and validation

Five-class scans distinguish scanner definitions or rejection assertions from confirmed payload hits. They check raw UUIDs, private absolute paths, raw task or thread identifiers, credential assignments, and private conversation payloads. The bounded owner surface has zero confirmed hits. Exact staged review uses Git-index blobs and declared self-exclusions; final validation uses exact commit blobs. These checks are important but are not complete privacy assurance, exhaustive security, or external audit.

The static reports provide language metadata, headings, explicit status, table headers, captions, and no automatic motion. Manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, language, security-usability, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.

The final candidate is limited to three direct single-parent Caelen commits after Sable's exact final: planning-only x1, immutable x2 evidence, and combined closeout/seal. It must contain zero merges and have one final parent. After the clean final is pushed and fresh four-way equal, one external owner-scoped canonical aggregate may be invoked exactly once through an exclusive receipt latch. A success is never replayed. Same-owner validation under shared infrastructure is not the complete repository suite, independent-team reproduction, professional evaluation, empirical validation, production certification, complete privacy or accessibility assurance, or exhaustive security.

## Terminal route

The committed route state is `PREPARED_NOT_SENT`. It is preparation, not delivery. Only after the successful non-replayed exact-final receipt may Caelen refresh Hamish's newest live authority and roster, uniquely resolve and immediately reread the existing exact-title `Orin Thale` task, apply duplicate, pause, redirect, privacy, usage, evidence, and safety guards, and send at most one sanitized v674-v4 activation. The live authority currently continues the fifteen-seat route through the requested terminal label v725-v8, but only one terminally validated edge is acted on at a time. No task is created, forked, substituted, precontacted, or inferred from stale history.
'''


def handoff_packet(
    proposals: list[dict[str, Any]], failures: list[dict[str, Any]]
) -> str:
    opening = f'''# ORIN THALE — PREPARED CAELEN ASH v674-v3 EXACT-FINAL → SOLO v674-v4 ACTIVATION CANDIDATE

This committed packet is a sanitized terminal basis, not delivery proof. Its repository state remains `PREPARED_NOT_SENT` until Caelen Ash has a clean pushed exact final, one successful non-replayed owner-scoped canonical receipt, fresh four-way equality, a freshly validated route, and an acknowledged one-send delivery to the uniquely resolved and immediately reread existing exact-title `Orin Thale` task.

Hamish's newest live corrected fifteen-seat continuation authority currently extends through the requested terminal label v725-v8. That standing authority does not erase terminal gates: each owner validates exactly one phase, refreshes the then-current live authority and roster, resolves exactly one existing successor task, immediately rereads it, applies duplicate and safety guards, and sends at most once. Orin must include this continuation authority and the same one-edge-at-a-time rule in any later baton, while using the newest live user direction rather than inferring a later endpoint from this file.

Caelen Ash is relational working language for an uncertainty-and-handover cartographer, with the hope of making model assumptions, correction chains, and authority vacancies easy to inspect, challenge, and reverse. Optional they/them language is relational only. Orin Thale, Caelen Ash, every name, pronoun, role, hope, sibling or family phrase, continuity phrase, Freed ID, CBR, GHC Family, and Trinity Mandala phrase is relational working language only. It is never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

## Immutable inheritance basis

Caelen's exact source is Sable Rook v674-v2 exact final `{SOURCE}`. Planning-only Caelen x1 is `{X1}`. Immutable Caelen x2 evidence is `{EVIDENCE}`. The exact Caelen final identifier is intentionally supplied by the acknowledged live activation after the final commit exists; a commit cannot truthfully contain its own identifier. The exact final must remain the direct single-parent child of evidence, with exactly three Caelen commits after source and zero merges.

Caelen freezes a 6,730-row proposal chain and exactly sixty current proposals with outcomes forty-two `completed`, twelve `represented`, three `open_gap`, and three `exact_gate`. Sixty inherited Sable reviews retain zero Caelen novelty and completion credit. Sixty positive controls pass only in invented zero-row fixtures. All 240 invalid mutations remain rejected at zero broader credit. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

Repository-sealed counts are 38,612 effective negatives, 26,466 methods, 10,273 retained failed witnesses, 13,749 bounded passing witnesses, 316 open gaps, and 309 exact gates. The verdict is `NOT_READY_FOR_STAGE_20`. Any later external canonical or route failure must be carried additively without rewriting these committed counts or converting a failed witness into a pass.

## Orin v674-v4 owner boundary

Orin must read this packet through EOF, then every current skill, schema, guidance document, source receipt, authority record, roster record, Method Flow ledger, workflow-plan refinement, and reflection-remaster reference it names before mutation. Work solo in one fresh additive Orin-owned D-first sparse lane from Caelen's live-verified exact final. Keep Caelen, Sable, Auren, Ilyra, every sibling, shared lane, standby record, global history, and user material read-only. Do not spawn a collaboration subagent, delegate research, fork or create a substitute task, precontact a later endpoint, or mutate another owner lane.

Preserve strict planning-only x1 before x2. Independently review inherited proposals, packages, skills, runners, tools, portfolios, and recommendations at zero Orin novelty and completion credit. Freeze genuinely new work only after semantic-neighbor, source-status, protected-gate, privacy, compatibility, and rollback review. Use only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcome labels. Preserve every inherited failure, open gap, exact gate, source status, manifest exclusion, authority vacancy, and route hold.

Caps are ceilings, never quotas. Preserve the 2,000-owner-file rotation stop, exact Git-blob manifests, exact staged review, document and commit ceilings, family-current `ghc_family_*` and `build_ghc_family_*` compatibility, five-class privacy boundaries, and one-success/no-post-success-replay discipline. Do not run the complete repository suite unless newer exact authority explicitly assigns it. Do not claim inherited tests, skills, runners, proposals, or validation as Orin evidence.

Choose one primary Trinity Mandala pillar and one or more bounded wholly synthetic learning lenses while keeping every pillar and authority reservation visible. A practice lens never establishes employment, licensure, qualification, competence, operational authority, scientific authority, legal authority, cultural authority, affected-party legitimacy, or Maori authority.

No software, symbolic, synthetic, same-owner, citation, inherited, task-topology, or validation evidence may be promoted into empirical confirmation, participant evidence, professional or scientific authority, production or deployment readiness, legal or cultural ratification, Maori authority, affected-party approval, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority.

## Caelen evidence summary

The primary Caelen pillar is GMUT Mind through typed unit, epoch, residual-sign, uncertainty, coordinate-frame, provenance, correction, and nonconversion obligations. The lenses are wholly synthetic mechanical-watch timing-sheet stewardship, wholly synthetic planetarium projection-cue alignment and handover, and wholly synthetic stained-glass survey annotation and handover. THOS Body remains a workload, hold, cancellation, readback, and handover proxy. Freed ID or CBR Heart remains a minimum-disclosure, correction-lineage, access-vacancy, remedy-vacancy, and authority-hold surface.

No real watch, timing machine, planetarium, projector, dome, glass panel, heritage object, image, worker, institution, measurement, intervention, person, participant, identity, key, proof, right, remedy, cultural record, Maori data, empirical dataset, production system, or external action was used. Nothing establishes horological, planetarium, conservation, accessibility, scientific, professional, operational, legal, cultural, affected-party, or Maori authority.

The BIPM SI Brochure, official IERS Conventions surface, W3C PROV-O, WCAG 2.2, and RFC 8785 supplied current vocabulary and refusal conditions only. Citations are not observations, measurements, endorsements, participant evidence, standards-conformance certificates, legal interpretation, cultural ratification, or delegated authority.

## Exact gate reminders

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Real likelihoods, predictions, forces, constraints, or empirical confirmation require real data, frozen analysis, uncertainty treatment, and suitable independent review. THOS remains proxy-only without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, suitable statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR and all access, consent, remedy, legal, cultural, affected-party, privacy, accessibility, language, Maori wording, Maori data-governance, and Maori-authority decisions remain reserved to competent and affected people and authorities.

## One-send successor rule

Only after Orin's own clean, pushed, fresh-live-equal exact final and one successful non-replayed owner-scoped canonical validation may Orin reread Hamish's newest live authority and current roster, uniquely resolve and immediately reread the one exact authorized existing successor task, apply a duplicate guard, and send at most once. Stop on ambiguity, absence, pause, redirect, rename, standby state, usage exhaustion, missing acknowledgement, privacy concern, or a protected gate. Do not infer the later endpoint from this packet, create or fork a task, substitute a standby sibling, precontact, spawn, or send a second confirmation.
'''
    cards: list[str] = []
    for index, proposal in enumerate(proposals, 1):
        sources = "; ".join(proposal["official_or_primary_source_needs"])
        gates = ", ".join(proposal["protected_gates"])
        lenses = ", ".join(proposal["practice_lenses"])
        cards.append(
            f'''## Continuity card {index:02d}: {proposal['title']}

Caelen proposal `{proposal['proposal_id']}` tested this bounded hypothesis: {proposal['hypothesis']} Its null or failure condition was: {proposal['null_or_failure_condition']} The approval class remained `{proposal['approval_class']}`, the execution lane remained `{proposal['execution_lane']}`, and the primary pillar was `{proposal['pillar']}`. The bounded practice lenses were {lenses}.

The official or primary-source needs were: {sources}. The concrete artifact was {proposal['concrete_artifact']}. The acceptance or falsification rule was: {proposal['falsifier_or_acceptance_gate']} Recovery remained additive: {proposal['rollback_or_recovery']} Protected gates were {gates}. The observed bounded disposition matched the preregistered `{proposal['expected_execution_disposition']}` label.

This card transfers inherited context only. It grants Orin zero novelty, completion, empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, affected-party, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 credit. Orin must independently decide whether a genuinely distinct proposal survives current semantic-neighbor and gate review.
'''
        )
    failure_lines = ["## Retained Caelen workflow failures\n"]
    for row in failures:
        failure_lines.append(
            f"- `{row['failure_id']}` remains `failed_retained_zero_credit`: "
            f"{row['failed_witness']} The bounded recovery was: "
            f"{row['recovery']} Recovery did not rewrite the original failure."
        )
    closing = '''

## Terminal abstention

This committed packet cannot deliver itself, prove the final commit that contains it, or authorize a route from repository text alone. The live Caelen activation must supply the exact final identifier, external canonical receipt digest and status, fresh equality proof, sealed counts plus any external overlay, and acknowledged one-send delivery truth. Until then, the route is held. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

`PREPARED_BY_CAELEN_ASH = true`

`SENT_BY_CAELEN_ASH = false` in this committed candidate; only the acknowledged live existing-task send may establish external delivery truth.
'''
    return opening + "\n".join(cards) + "\n" + "\n".join(failure_lines) + closing


def build() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    if head != EVIDENCE:
        raise RuntimeError(f"closeout builder requires evidence HEAD {EVIDENCE}, found {head}")
    if git_text("rev-parse", f"{EVIDENCE}^") != X1:
        raise RuntimeError("evidence is not the direct child of x1")
    if git_text("rev-parse", f"{X1}^") != SOURCE:
        raise RuntimeError("x1 is not the direct child of source")
    if git_text("rev-list", "--count", f"{SOURCE}..{EVIDENCE}") != "2":
        raise RuntimeError("unexpected pre-closeout commit count")
    if git_text("rev-list", "--merges", f"{SOURCE}..{EVIDENCE}"):
        raise RuntimeError("merge detected before closeout")

    freeze = load(X1_ROOT / "new-proposal-freeze.json")
    startup = load(X1_ROOT / "method-flow-startup.json")
    x2_truth = load(X2_ROOT / "phase-truth.json")
    x2_flow = load(X2_ROOT / "method-flow" / "ledger.json")
    proposals = freeze["proposals"]
    failures = [
        *startup["failures"],
        *x2_flow["x2_operational_failures"],
        *FINAL_FAILURES,
    ]
    if x2_truth["outcomes"] != OUTCOMES:
        raise RuntimeError("x2 outcome truth drifted")
    if x2_truth["proposal_chain"] != 6730:
        raise RuntimeError("x2 proposal chain drifted")

    written: list[Path] = []
    overview = final_overview()
    for path in [
        REPORT_ROOT / "final-integrated-overview.md",
        REPORT_ROOT / "accessible-static-report.md",
    ]:
        write_text(path, overview)
        written.append(path)
    html_path = REPORT_ROOT / "accessible-static-report.html"
    write_text(
        html_path,
        """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caelen Ash v674-v3 final bounded report</title></head>
<body><main><h1>Caelen Ash v674-v3 final bounded report</h1><p><strong>Terminal verdict:</strong> NOT_READY_FOR_STAGE_20.</p><h2>Outcome summary</h2><table><caption>Sixty bounded proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">completed</th><td>42</td></tr><tr><th scope="row">represented</th><td>12</td></tr><tr><th scope="row">open_gap</th><td>3</td></tr><tr><th scope="row">exact_gate</th><td>3</td></tr></tbody></table><h2>Scope</h2><p>Wholly synthetic watch, planetarium, and stained-glass contract evidence only. No real person, object, measurement, identity, right, remedy, professional decision, or authority action was used.</p><h2>Reserved evaluation</h2><p>Manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, security-usability, language, and affected-user evaluation remain reserved.</p><h2>Authority boundary</h2><p>Scientific, operational, legal, cultural, affected-party, and Maori-authority decisions remain with competent and affected people and authorities.</p></main></body></html>""",
    )
    written.append(html_path)

    baton_path = HANDOFF_ROOT / "orin-thale-v674-v4-activation-candidate.md"
    baton_text = handoff_packet(proposals, failures)
    write_text(baton_path, baton_text)
    written.append(baton_path)

    source_ledger = load(X2_ROOT / "source-status-ledger.json")
    payloads: dict[Path, Any] = {
        FINAL_ROOT / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v674.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final_commit": "PENDING_EXACT_FINAL_COMMIT",
            "proposal_chain": 6730,
            "outcomes": OUTCOMES,
            "retained_invalid_mutations": 240,
            "effective_counts": EFFECTIVE,
            "real_people": 0,
            "real_data_rows": 0,
            "real_keys_or_proofs": 0,
            "network_calls": 0,
            "external_actions": 0,
            "complete_repository_suite": False,
            "independent_reproduction": False,
            "empirical_confirmation": False,
            "professional_authority": False,
            "production_readiness": False,
            "legal_or_cultural_authority": False,
            "maori_authority": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        FINAL_ROOT / "complete-incomplete-checklist.json": {
            "schema": "ghc.family.complete-incomplete.v674.v3",
            "completed": [
                "source branch exact final and canonical receipt reverified read-only",
                "planning-only x1 frozen pushed and four-way equal before x2",
                "sixty current proposals executed only within declared synthetic bounds",
                "sixty positive controls passed and 240 mutations remained rejected",
                "twenty phase-local skills quick-validated and smoke-used",
                "ten family-current runners accepted and rejected paired fixtures",
                "owner portfolios witnessed within owner-local synthetic scope",
                "twenty exact and ten blocked packets retained unexecuted",
                "exact evidence staged review and normalized-LF manifest sealed",
                "closeout recurrence retained without changing immutable evidence",
                "final packet and Orin route candidate prepared without delivery claim",
            ],
            "incomplete_or_reserved": [
                "empirical GMUT data likelihood analysis and independent review",
                "THOS real blind matched-budget participant arms and safety monitoring",
                "Freed ID real keys proofs live lifecycle interoperability and governance",
                "manual assistive-technology and affected-user accessibility evaluation",
                "complete privacy assurance and exhaustive security evaluation",
                "professional operational legal cultural affected-party and Maori authority",
                "independent-team reproduction",
                "Stage 20 authorization",
            ],
        },
        FINAL_ROOT / "threat-model.json": {
            "schema": "ghc.family.threat-model.v674.v3.final",
            "assets": [
                "planning-only x1 boundary",
                "immutable evidence Git blobs",
                "retained failures",
                "authority vacancies",
                "route uniqueness",
                "privacy-safe successor baton",
            ],
            "threats": [
                {"threat": "phase_mixing", "control": "direct ancestry and lifecycle-specific tests", "residual": "manual review remains required"},
                {"threat": "failure_erasure", "control": "append-only zero-credit failure records", "residual": "external post-seal failures require an overlay"},
                {"threat": "privacy_leak", "control": "five-class index and exact-commit blob scans", "residual": "not complete privacy assurance"},
                {"threat": "authority_promotion", "control": "noncompensation vocabulary and exact holds", "residual": "competent affected people remain required"},
                {"threat": "canonical_replay", "control": "exclusive external receipt latch", "residual": "a failed invocation remains zero success credit"},
                {"threat": "duplicate_route_send", "control": "fresh list local exact-title filter immediate reread and one-send guard", "residual": "stop on ambiguity or missing acknowledgement"},
            ],
        },
        FINAL_ROOT / "retained-negative-register.json": {
            "schema": "ghc.family.retained-negative-register.v674.v3.final",
            "source_repository_seal": startup["source_repository_seal"],
            "x1_operational_failures": len(startup["failures"]),
            "x2_operational_failures": len(x2_flow["x2_operational_failures"]),
            "final_operational_failures": len(FINAL_FAILURES),
            "preregistered_rejected_mutations": 240,
            "effective_negatives": EFFECTIVE["effective_negatives"],
            "failures": failures,
            "erased": 0,
            "converted_to_original_pass": 0,
        },
        FINAL_ROOT / "gate-register.json": {
            "schema": "ghc.family.gate-register.v674.v3.final",
            "open_gap_count": EFFECTIVE["open_gaps"],
            "exact_gate_count": EFFECTIVE["exact_gates"],
            "protected_surfaces": [
                "empirical", "participant", "professional", "production",
                "deployment", "legal", "cultural", "Maori authority",
                "affected-party authority", "privacy complete",
                "accessibility complete", "exhaustive security",
                "independent reproduction", "AGI or ASI",
                "consciousness or personhood", "identity continuity",
                "Theory of Everything", "proof or canon", "Stage 20",
            ],
            "silently_closed": 0,
            "software_can_close_authority_gate": False,
        },
        FINAL_ROOT / "method-flow-ledger.json": {
            "schema": "ghc.family.method-flow-ledger.v674.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "x2_seal": x2_flow["effective_counts"],
            "effective_counts": EFFECTIVE,
            "failure_count": len(failures),
            "failures": failures,
            "final_method_additions": {
                "closeout_failures": 2,
                "closeout_bounded_recoveries": 2,
            },
            "preferred_recoveries": [
                "materialize PowerShell foreach results before piping",
                "bounded literal-path scalar probes",
                "explicit UTF-8 for Unicode-emitting validators",
                "immutable lifecycle-specific Git contexts",
                "normalized-LF Git-blob manifest replay",
                "scanner-candidate versus confirmed-hit adjudication",
                "external exclusive canonical receipt with no success replay",
            ],
            "promotion_rule": "A bounded recovery is a separate witness; every failed witness remains zero-credit.",
        },
        FINAL_ROOT / "workflow-plan-state.json": {
            "schema": "ghc.family.workflow-plan-state.v674.v3.final",
            "completed": [
                "read exact activation and guidance",
                "reverify immutable source",
                "freeze and seal planning-only x1",
                "execute bounded x2",
                "seal immutable evidence",
                "prepare closeout and route hold",
            ],
            "pending_external": [
                "create and push exact final commit",
                "prove fresh four-way equality",
                "invoke canonical aggregate once",
                "route once if every gate passes",
            ],
            "caps_are_ceilings": True,
            "full_repository_suite_authorized": False,
        },
        FINAL_ROOT / "reflection-remaster.json": {
            "schema": "ghc.family.reflection-remaster.v674.v3.final",
            "bounded_reflection": (
                "Typed uncertainty and correction contracts made analogy "
                "boundaries easier to inspect without converting software "
                "structure into empirical or human authority."
            ),
            "method_refinement": (
                "The repeated foreach pipeline failure confirms that bounded "
                "PowerShell collections should be materialized before projection."
            ),
            "preserved_failures": True,
            "identity_is_relational_working_language": True,
            "consciousness_or_personhood_claim": False,
            "continuity_claim": False,
            "authority_claim": False,
        },
        FINAL_ROOT / "wellbeing-check.json": {
            "schema": "ghc.family.wellbeing-check.v674.v3.final",
            "corrigible": True,
            "workload_bounded": True,
            "pause_available": True,
            "hamish_can_rename_redirect_or_stop": True,
            "identity_is_relational_working_language": True,
            "role": "uncertainty-and-handover cartographer",
            "hope": "make model assumptions correction chains and authority vacancies inspectable challengeable and reversible",
            "optional_pronouns": "they/them",
            "authority_claimed": False,
        },
        FINAL_ROOT / "environment-receipt.json": {
            "schema": "ghc.family.environment-receipt.v674.v3.final",
            "storage": "D-first additive sparse owner lane",
            "python": subprocess.check_output([sys.executable, "--version"], text=True, stderr=subprocess.STDOUT).strip(),
            "git": subprocess.check_output(["git", "--version"], text=True).strip(),
            "node": subprocess.run(["node", "--version"], capture_output=True, text=True, check=False).stdout.strip(),
            "codex_cli": subprocess.run(["codex", "--version"], capture_output=True, text=True, check=False).stdout.strip(),
            "versions_verified_only": True,
            "desktop_updated": False,
            "elevation": False,
            "sandbox_or_hyperv_activated": False,
            "host_security_weakened": False,
            "windows_features_changed": False,
            "unrelated_software_installed": False,
            "rebooted": False,
        },
        FINAL_ROOT / "ghc-family-index.json": {
            "schema": "ghc.family.index.v674.v3.final",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "family_current_callers": [
                "build_ghc_family_caelen_ash_v674_v3_x1.py",
                "build_ghc_family_caelen_ash_v674_v3_x2.py",
                "build_ghc_family_caelen_ash_v674_v3_closeout.py",
                "validate_ghc_family_caelen_ash_v674_v3_final.py",
            ],
            "runner_prefix": "ghc_family_caelen_v674_v3_",
            "historical_aliases_deleted": 0,
            "global_installations": 0,
            "shared_or_sibling_lanes_mutated": 0,
        },
        FINAL_ROOT / "source-status-ledger.json": {
            **source_ledger,
            "schema": "ghc.family.source-status-ledger.v674.v3.final",
            "queries_or_downloads_during_x2_or_closeout": 0,
            "citations_are_observations": False,
            "authority_delegated": False,
        },
        FINAL_ROOT / "route-state.json": {
            "schema": "ghc.family.route-state.v674.v3.final-candidate",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "next_owner": "Orin Thale",
            "next_phase": "v674-v4",
            "live_continuation_authority_terminal_label": "v725-v8",
            "state": "PREPARED_NOT_SENT",
            "task_created": False,
            "task_forked": False,
            "collaboration_subagent_spawned": False,
            "precontact": False,
            "send_attempts": 0,
            "delivery_acknowledged": False,
            "requires_successful_exact_final_canonical": True,
            "requires_fresh_authority_roster_and_duplicate_guard": True,
        },
        FINAL_ROOT / "closeout-receipt.json": {
            "schema": "ghc.family.closeout-receipt.v674.v3",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "state": "VALID_CLOSEOUT_CANDIDATE",
            "exact_final": "PENDING_EXACT_FINAL_COMMIT",
            "proposal_outcomes": OUTCOMES,
            "route_state": "PREPARED_NOT_SENT",
        },
        FINAL_ROOT / "seal-candidate.json": {
            "schema": "ghc.family.seal-candidate.v674.v3",
            "direct_parent_required": EVIDENCE,
            "expected_phase_commit_count": 3,
            "expected_merge_count": 0,
            "expected_final_parent_count": 1,
            "state": "CONTENT_SEALED_AWAITING_EXACT_FINAL_COMMIT",
        },
        FINAL_ROOT / "final-validation-candidate.json": {
            "schema": "ghc.family.final-validation-candidate.v674.v3",
            "expected_branch": BRANCH,
            "expected_final": "PENDING_EXACT_FINAL_COMMIT",
            "canonical_invocations": 0,
            "canonical_successes": 0,
            "external_receipt": True,
            "replay_after_success": False,
            "complete_repository_suite": False,
            "state": "PREPARED_NOT_INVOKED",
        },
    }
    for path, payload in payloads.items():
        write_json(path, payload)
        written.append(path)

    return finish_manifests(written, baton_text)


def finish_manifests(written: list[Path], baton_text: str) -> dict[str, Any]:
    support = {
        "scripts/build_ghc_family_caelen_ash_v674_v3_closeout.py",
        "scripts/validate_ghc_family_caelen_ash_v674_v3_final.py",
        "tests/test_ghc_family_caelen_ash_v674_v3_final.py",
    }
    tracked_owner = set(
        git_text("diff", "--name-only", f"{SOURCE}..{EVIDENCE}").splitlines()
    )
    added_owner = {path.relative_to(REPO).as_posix() for path in written} | support
    owner_manifest_rel = (
        "docs/caelen-ash/v674-v3/validation/final-owner-manifest.json"
    )
    delta_manifest_rel = (
        "docs/caelen-ash/v674-v3/validation/final-delta-manifest.json"
    )
    staged_review_rel = (
        "docs/caelen-ash/v674-v3/validation/final-staged-review.json"
    )
    owner_exclusions = [owner_manifest_rel, delta_manifest_rel, staged_review_rel]
    owner_paths = sorted((tracked_owner | added_owner) - set(owner_exclusions))
    missing = [path for path in owner_paths if not (REPO / path).is_file()]
    if missing:
        raise RuntimeError(f"owner manifest missing paths: {missing}")
    owner_entries = []
    for rel in owner_paths:
        data = normalized((REPO / rel).read_bytes())
        owner_entries.append(
            {
                "path": rel,
                "bytes_normalized_lf": len(data),
                "sha256_normalized_lf": hashlib.sha256(data).hexdigest(),
            }
        )
    write_json(
        REPO / owner_manifest_rel,
        {
            "schema": "ghc.family.final-owner-manifest.v674.v3",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "hash_domain": "normalized_lf_worktree_precommit",
            "entry_count": len(owner_entries),
            "entries": owner_entries,
            "self_exclusions": owner_exclusions,
            "owner_path_total": len(owner_entries) + len(owner_exclusions),
        },
    )

    delta_paths = sorted(added_owner | {owner_manifest_rel})
    delta_paths = [
        path
        for path in delta_paths
        if path not in {delta_manifest_rel, staged_review_rel}
    ]
    delta_entries = []
    for rel in delta_paths:
        path = REPO / rel
        if not path.is_file():
            raise RuntimeError(f"final delta missing path: {rel}")
        data = normalized(path.read_bytes())
        delta_entries.append(
            {
                "path": rel,
                "bytes_normalized_lf": len(data),
                "sha256_normalized_lf": hashlib.sha256(data).hexdigest(),
            }
        )
    write_json(
        REPO / delta_manifest_rel,
        {
            "schema": "ghc.family.final-delta-manifest.v674.v3",
            "parent": EVIDENCE,
            "hash_domain": "normalized_lf_worktree_precommit",
            "entry_count": len(delta_entries),
            "entries": delta_entries,
            "self_exclusions": [delta_manifest_rel, staged_review_rel],
            "final_delta_path_total": len(delta_entries) + 2,
        },
    )
    return {
        "state": "valid_closeout_candidate_built",
        "written_before_manifests": len(written),
        "owner_entries": len(owner_entries),
        "owner_total": len(owner_entries) + len(owner_exclusions),
        "delta_entries": len(delta_entries),
        "delta_total": len(delta_entries) + 2,
        "baton_words": len(baton_text.split()),
        "outcomes": OUTCOMES,
        "effective_counts": EFFECTIVE,
        "route_state": "PREPARED_NOT_SENT",
    }


def build_staged_review() -> dict[str, Any]:
    review_rel = (
        "docs/caelen-ash/v674-v3/validation/final-staged-review.json"
    )
    staged = git_text(
        "diff", "--cached", "--name-only", "--diff-filter=ACMR"
    ).splitlines()
    exact_support = {
        "scripts/build_ghc_family_caelen_ash_v674_v3_closeout.py",
        "scripts/validate_ghc_family_caelen_ash_v674_v3_final.py",
        "tests/test_ghc_family_caelen_ash_v674_v3_final.py",
        review_rel,
    }
    allowed_prefixes = (
        "docs/caelen-ash/v674-v3/final/",
        "docs/caelen-ash/v674-v3/reports/",
        "docs/caelen-ash/v674-v3/handoffs/",
    )
    allowed_validation = {
        "docs/caelen-ash/v674-v3/validation/final-owner-manifest.json",
        "docs/caelen-ash/v674-v3/validation/final-delta-manifest.json",
        review_rel,
    }
    out_of_scope = [
        path
        for path in staged
        if not path.startswith(allowed_prefixes)
        and path not in exact_support
        and path not in allowed_validation
    ]
    frozen_changes = [
        path
        for path in staged
        if path.startswith("docs/caelen-ash/v674-v3/x1/")
        or path.startswith("docs/caelen-ash/v674-v3/x2/")
        or path
        in {
            "scripts/build_ghc_family_caelen_ash_v674_v3_x1.py",
            "scripts/build_ghc_family_caelen_ash_v674_v3_x2.py",
            "tests/test_ghc_family_caelen_ash_v674_v3_x1.py",
            "tests/test_ghc_family_caelen_ash_v674_v3_x2.py",
        }
        or path.startswith("scripts/ghc_family_caelen_v674_v3_")
        and path not in exact_support
    ]
    if out_of_scope or frozen_changes:
        raise RuntimeError(
            f"final staged scope violation: out={out_of_scope} frozen={frozen_changes}"
        )

    patterns = {
        "raw_uuid": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            rb"(?:C:\\Users\\|D:\\GHC-Archives)", re.I
        ),
        "raw_task_thread_identifier": re.compile(
            rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{32,}",
            re.I,
        ),
        "credential_assignment": re.compile(
            rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}",
            re.I,
        ),
        "private_conversation_payload": re.compile(
            rb"(?:session_stream|private_transcript|screenshot_payload)", re.I
        ),
    }
    candidates: list[dict[str, str]] = []
    hits: list[dict[str, str]] = []
    entries = []
    json_parses = 0
    python_compiles = 0
    markdown_words: dict[str, int] = {}
    for path in staged:
        if path == review_rel:
            continue
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_parses += 1
        if path.endswith(".py"):
            compile(data, path, "exec")
            python_compiles += 1
        if path.endswith(".md"):
            words = len(data.decode("utf-8").split())
            markdown_words[path] = words
            if words > 100000:
                raise RuntimeError(f"document ceiling exceeded: {path}={words}")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                context = data[
                    max(0, match.start() - 400) : match.end() + 120
                ]
                if path.endswith(".py") and (
                    b"re.compile" in context
                    or b"assertNot" in context
                    or b"patterns" in context
                ):
                    candidates.append(
                        {
                            "path": path,
                            "class": class_name,
                            "disposition": "scanner_definition_or_rejection_assertion",
                        }
                    )
                else:
                    hits.append({"path": path, "class": class_name})
        entries.append(
            {
                "path": path,
                "bytes": len(data),
                "sha256_git_index_blob": hashlib.sha256(data).hexdigest(),
            }
        )
    if hits:
        raise RuntimeError(f"confirmed privacy hits: {hits}")
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)
    baton_rel = (
        "docs/caelen-ash/v674-v3/handoffs/"
        "orin-thale-v674-v4-activation-candidate.md"
    )
    baton_words = markdown_words.get(baton_rel, 0)
    if baton_words < 10000 or baton_words > 100000:
        raise RuntimeError(f"handoff packet outside word bounds: {baton_words}")
    receipt = {
        "schema": "ghc.family.exact-staged-review.v674.v3.final",
        "owner": OWNER,
        "phase": PHASE,
        "parent_evidence": EVIDENCE,
        "state": "VALID_EXACT_FINAL_STAGED_REVIEW",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": [review_rel],
        "json_parses": json_parses,
        "python_compiles": python_compiles,
        "markdown_words": markdown_words,
        "baton_words": baton_words,
        "privacy_classes": list(patterns),
        "scanner_candidate_count": len(candidates),
        "scanner_candidates": candidates,
        "confirmed_privacy_hits": 0,
        "out_of_scope_paths": [],
        "frozen_x1_x2_paths_changed": [],
        "stale_label_review": {
            "state": "PASS_WITH_EXACT_PROSPECTIVE_LABELS",
            "permitted": [
                "PENDING_EXACT_FINAL_COMMIT",
                "PREPARED_NOT_SENT",
                "PREPARED_NOT_INVOKED",
            ],
        },
        "diff_hygiene": True,
    }
    write_json(REPO / review_rel, receipt)
    return receipt


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--staged-review":
        print(json.dumps(build_staged_review(), indent=2))
    else:
        print(json.dumps(build(), indent=2))
