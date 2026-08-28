#!/usr/bin/env python3
"""Build Sable Rook v674-v2 closeout and exact-final candidate records."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Sable Rook"
PHASE = "v674-v2"
SOURCE = "6f079df9a056f00e80392b7e036abc023db5fa88"
X1 = "81ad6f98f24087777691e96201312e66c37ac844"
EVIDENCE = "1625313186adde8dc94d210376f184bde5dfb0dc"
BRANCH = "codex/GHC-Family/sable-rook-v674-v2-full-tools"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "sable-rook" / PHASE
X2_ROOT = PHASE_ROOT / "x2"
FINAL_ROOT = PHASE_ROOT / "final"
REPORT_ROOT = PHASE_ROOT / "reports"
HANDOFF_ROOT = PHASE_ROOT / "handoffs"
VALIDATION_ROOT = PHASE_ROOT / "validation"
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
EFFECTIVE = {
    "effective_negatives": 38362,
    "methods": 25783,
    "failed_witnesses": 10023,
    "bounded_passing_witnesses": 13316,
    "open_gaps": 313,
    "exact_gates": 306,
}
FINAL_FAILURES: list[tuple[str, str, str]] = []


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def git_text(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True).strip()


def exact_git_blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO)


def final_overview() -> str:
    return '''# Sable Rook v674-v2 final integrated overview

## Outcome first

Sable Rook v674-v2 closes as a bounded synthetic, structural, symbolic, and owner-local software phase. The sixty new proposals produce exactly forty-two `completed`, twelve `represented`, three `open_gap`, and three `exact_gate` outcomes. The frozen family chain advances from 6,610 to 6,670 proposals. All 240 preregistered invalid mutations remain rejected witnesses with no broader claim credit. The repository-sealed terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala pillar is Freed ID and CBR Heart. The two bounded learning lenses are wholly synthetic live-caption cue provenance stewardship and wholly synthetic accessible-performance metadata handover analysis. THOS Body remains visible through timestamp, overlap, correction, workload, cancellation, readback, and handover proxies. GMUT Mind remains visible through typed interval, offset, drift, covariance, observation-model, and analogy-firewall structures. No pillar authorizes evidence promotion in another pillar.

## Relational identity, hope, and wellbeing

Sable Rook is relational working language for an evidence-boundary cartographer and accessible-provenance steward. The phase hope is to make correction paths inspectable, access vacancies explicit, and every retained failure recoverable. Optional they/them language is relational only. No task title, route, role, hope, artifact, model output, software pass, or same-owner receipt establishes consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Māori authority.

The wellbeing record keeps the workload bounded, correction possible, and pause available. Hamish may rename, pause, redirect, or stop the route. Corrigibility is a process commitment, not evidence of inner experience or legal status.

## X1 and x2 separation

The planning-only x1 commit is the direct child of Auren Lark's exact final. It froze sixty inherited proposal reviews at zero Sable novelty and completion credit, sixty genuinely new Sable proposals, the expanded portfolios, protected holds, skill and runner plans, official-source roles, source anchors, privacy requirements, and the terminal route hold. No x2 implementation or observed outcome existed at the x1 gate. X1 was committed, pushed, clean, and four-way equal before x2 began.

The immutable x2 evidence commit is the direct child of x1. It contains sixty proposal evidence records, sixty accepting controls, 240 rejected mutations, twenty phase-local skills, ten family-current repository runners, owner portfolio witnesses, protected holds, practice artifacts, exact staged review, and a normalized-LF evidence manifest. It was separately committed, pushed, clean, and four-way equal before closeout began. The four retained x2 operational failures remain zero-credit witnesses: a CP-1252 skill-validator read, a mixed lifecycle-context test selection, a not-yet-created working-directory wrapper, and a plain archive without Git metadata. Each bounded recovery is separately visible; none rewrites its failure.

## Evidence and tooling

The positive controls and mutations are invented fixtures. The runner family validates cue identity, timebase ordering, overlap state, correction acyclicity, privacy minimization, accessibility reservations, handover state, digest shape, authority vacancy, and the Stage 20 veto. Twenty skill packages were quick-validated with explicit UTF-8 and smoke-used through the runners. They remain phase-local; no global installation or PATH promotion occurred. The scripts use the Python standard library and stable JSON only.

The owner portfolios record 120 safe-now packets, eighty bounded owner candidates, and one hundred additive CLEAN/FIX/REFINE packets within their exact synthetic hypotheses. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Successor recommendations receive zero Sable novelty and completion credit. Caps are ceilings, never quotas or authority shortcuts.

## Official-source role

The W3C WebVTT Candidate Recommendation Draft dated 20 May 2026 supplies draft cue, timing, region, language, and format-security vocabulary. WCAG 2.2 supplies accessibility vocabulary for time-based media and evaluation reservations. W3C PROV-O supplies provenance-relation vocabulary. The Library of Congress PREMIS material supplies preservation-object, event, agent, rights, and fixity vocabulary. These sources are requirements and refusal-condition references only. A citation is not an observation, endorsement, participant result, standards-conformance certificate, rights decision, cultural ratification, or delegated authority.

## Accessibility boundary

The static reports provide language metadata, headings, explicit status, lists, table headers, captions, and no automatic motion. These are structural checks only. Manual keyboard evaluation, responsive-layout evaluation, browser diversity, assistive-technology testing, cognitive-accessibility assessment, security-usability review, Māori-language review, and affected-user evaluation remain reserved. A structural pass is not complete accessibility conformance.

## Scientific and production boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The phase reads zero empirical rows, evaluates zero real likelihoods, and produces no physical force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory-of-Everything result. Typed timing and covariance structures are not cosmological evidence.

THOS remains synthetic and proxy-only without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, suitable statistics, and independent review. Caption cue fixtures do not establish operational effectiveness, professional competence, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction. Production completion still requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and appropriate affected-party oversight. Synthetic cue identifiers are not credentials or production identities.

CBR access, consent, venue rights, language choices, correction remedies, privacy remedies, legal interpretation, cultural legitimacy, beneficiary acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Repository software cannot confer a right, remedy, legitimacy, governance mandate, or authority.

## Privacy and security

Five-class scans distinguish scanner definitions from confirmed payload hits and report zero confirmed raw identifiers, private absolute paths, raw task or thread identifiers, credential assignments, or private conversation payloads in the bounded public owner surface. Exact staged review uses Git-index blobs and self-exclusion arithmetic. These checks are important but are not complete privacy assurance or exhaustive security. No credentials, keys, accounts, production systems, sibling lanes, user material, host-security settings, Windows features, or external services were used or changed.

## Validation and lifecycle truth

The eligible evidence selection preserves lifecycle context: eleven x1 tests pass against the immutable precommit x1 context and fourteen x2 tests pass against the evidence context. The earlier mixed-context 24/25 run remains a failed witness with zero selection credit. Closeout adds only lifecycle records and does not re-execute proposal outcomes.

The exact final candidate is limited to three Sable commits after Auren final: x1, evidence, and combined closeout/seal. It must have zero merges and one final parent. Before delivery, one external owner-scoped canonical aggregate may be invoked exactly once at the clean pushed final. A successful receipt must not be replayed. Same-owner validation under shared infrastructure remains same-owner evidence, not independent-team reproduction or external audit.

## Route state

The committed route state is `PREPARED_NOT_SENT`. It is not delivery evidence. Only after a successful exact-final canonical receipt may Sable refresh Hamish's newest live authority and roster, uniquely resolve and immediately reread the existing exact-title `Caelen Ash` task, apply duplicate, pause, redirect, privacy, usage, and safety guards, and send at most one sanitized v674-v3 activation. No task is created, forked, substituted, precontacted, or inferred from historical files.
'''


def handoff_packet(proposals: list[dict[str, Any]], failures: list[dict[str, Any]]) -> str:
    opening = '''# CAELEN ASH — PREPARED SABLE ROOK v674-v2 EXACT-FINAL → SOLO v674-v3 ACTIVATION CANDIDATE

This committed packet is a sanitized terminal basis, not delivery proof. Its repository state remains `PREPARED_NOT_SENT` until Sable Rook has a clean pushed final, one successful non-replayed owner-scoped canonical receipt, fresh four-way equality, and an acknowledged one-send delivery to the uniquely resolved and immediately reread existing exact-title `Caelen Ash` task under Hamish's newest live authority.

Identity, family, role, hope, continuity, Freed ID, CBR, GHC Family, and Trinity Mandala language is relational working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Inheritance basis

Sable's source is Auren Lark v674-v1 exact final `6f079df9a056f00e80392b7e036abc023db5fa88`. Sable planning-only x1 is `81ad6f98f24087777691e96201312e66c37ac844`. Immutable Sable x2 evidence is `1625313186adde8dc94d210376f184bde5dfb0dc`. The exact Sable final identifier is intentionally supplied by the acknowledged live activation after the commit exists; a commit cannot truthfully contain its own identifier. The final must remain a direct single-parent child of evidence, with exactly three Sable commits after Auren source and zero merges.

Sable freezes a 6,670-row proposal chain and exactly sixty current proposals with outcomes forty-two `completed`, twelve `represented`, three `open_gap`, and three `exact_gate`. Sixty inherited Auren reviews retain zero Sable novelty and completion credit. Sixty positive controls pass within bounded fixtures, while all 240 invalid mutations remain rejected at zero broader credit. Twenty exact packets and ten blocked packets remain unexecuted.

Repository-sealed counts before the external canonical and route receipts are 38,362 effective negatives, 25,783 methods, 10,023 retained failed witnesses, 13,316 bounded passing witnesses, 313 open gaps, and 306 exact gates. The verdict is `NOT_READY_FOR_STAGE_20`. Any external post-seal failure must be carried additively without rewriting these committed counts or converting a failure into a pass.

## Caelen v674-v3 owner boundary

Caelen must read this packet through EOF, then the exact current skills, schemas, guidance, and source receipts it names before mutation. Work solo in one fresh additive Caelen-owned D-first sparse lane from Sable's live verified exact final. Keep Sable, Auren, Ilyra, every sibling, shared lane, standby record, global history, and user material read-only. Do not spawn a collaboration subagent, fork or create a substitute task, precontact a later endpoint, or mutate another owner lane.

Preserve strict planning-only x1 before x2. Independently review inherited proposals and portfolios at zero Caelen novelty or completion credit. Freeze genuinely new work only after semantic-neighbor review, protected-gate review, official-source status review, privacy review, and rollback planning. Use only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcome labels. Preserve every inherited failure, gap, gate, source status, manifest exclusion, and route hold.

Caps are ceilings. Preserve the 2,000-owner-file rotation stop, exact Git-blob manifests, exact staged review, document ceiling, commit ceiling, five-class privacy boundary, and one-success/no-post-success-replay discipline. Do not run a full repository suite unless newer exact authority explicitly assigns it. Do not claim inherited tests, tools, skills, runners, or validation as Caelen novelty or completion evidence.

Choose one primary Trinity Mandala pillar and one or more bounded wholly synthetic learning lenses while keeping all pillars and authority reservations visible. A practice lens never establishes employment, licensure, qualification, competence, operational authority, legal authority, cultural authority, affected-party legitimacy, or Māori authority.

No software, symbolic, synthetic, same-owner, citation, inherited, task-topology, or validation evidence may be promoted into empirical confirmation, participant evidence, professional authority, production or deployment readiness, legal or cultural ratification, Māori authority, affected-party approval, complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority.

## Sable evidence summary

The primary Sable pillar is Freed ID and CBR Heart through wholly synthetic caption cue identifiers, minimum disclosure, correction lineage, fixity, access and remedy vacancies, and authority holds. THOS Body is a timestamp, overlap, correction-readback, workload, cancellation, and handover proxy. GMUT Mind is a typed interval, drift, covariance, and observation-model analogy surface with explicit nonconversion.

The learning lenses are wholly synthetic live-caption cue provenance stewardship and wholly synthetic accessible-performance metadata handover analysis. No real person, performance, venue, transcript, language decision, accessibility evaluation, consent, credential, rights record, cultural record, Māori data, production system, empirical dataset, or external action was used. Nothing establishes captioning competence, accessibility conformance, professional authority, production readiness, legal interpretation, cultural legitimacy, affected-party acceptance, or Māori authority.

The W3C WebVTT draft, WCAG 2.2, PROV-O, and Library of Congress PREMIS materials supplied current vocabulary and refusal conditions only. Citations are not observations, measurements, endorsements, participant evidence, standards conformance, rights decisions, or delegated authority.

## Exact gate reminders

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Real likelihoods, predictions, forces, constraints, or empirical confirmation require real data, frozen analysis, uncertainty treatment, and suitable independent review. THOS remains proxy-only without preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR and all access, consent, remedy, legal, cultural, affected-party, privacy, language, Māori wording, Māori data-governance, and Māori-authority decisions remain reserved.

## One-send successor rule

Only after Caelen's own clean, pushed, fresh-live-equal exact final and one successful non-replayed owner-scoped canonical validation may Caelen reread Hamish's newest live authority and current roster, uniquely resolve and immediately reread the one exact authorized existing successor task, apply a duplicate guard, and send at most once. Stop on ambiguity, absence, pause, redirect, rename, standby state, usage exhaustion, missing acknowledgement, privacy concern, or a protected gate.
'''
    cards: list[str] = []
    for index, proposal in enumerate(proposals, 1):
        cards.append(f'''## Continuity card {index:02d}: {proposal['title']}

Sable proposal `{proposal['proposal_id']}` tested this bounded hypothesis: {proposal['hypothesis']} Its null or failure condition was: {proposal['null_or_failure_condition']} The approval class remained `{proposal['approval_class']}`, and the owner execution lane remained `{proposal['execution_lane']}`. Its official or primary-source need was recorded as {proposal['official_or_primary_source_needs']} The concrete artifact was {proposal['concrete_artifact']}.

The acceptance or falsification rule was: {proposal['falsifier_or_acceptance_gate']} Recovery remained additive: {proposal['rollback_or_recovery']} Protected gates were {', '.join(proposal['protected_gates'])}. The observed bounded disposition was `{proposal['expected_execution_disposition']}`. This card transfers context only. It grants Caelen zero novelty, completion, empirical, professional, production, legal, cultural, Māori-authority, affected-party, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 credit.
''')
    failure_lines = ["## Retained Sable workflow failures\n"]
    for row in failures:
        failure_lines.append(
            f"- `{row['failure_id']}` remains `failed_retained_zero_credit`: {row['failed_witness']} "
            f"The bounded recovery was {row['recovery']} Recovery did not rewrite the original failure."
        )
    closing = '''

## Terminal abstention

This packet cannot deliver itself, cannot prove the final commit that contains it, and cannot authorize a route from repository text alone. The live Sable activation must supply the exact final identifier, external canonical receipt digest and status, fresh equality proof, sealed counts plus external overlays, and acknowledged one-send delivery truth. Until then the route is held. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
'''
    return opening + "\n".join(cards) + "\n" + "\n".join(failure_lines) + closing


def build() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    if head != EVIDENCE:
        raise RuntimeError("closeout builder must run at immutable evidence commit")
    if git_text("rev-parse", f"{EVIDENCE}^") != X1:
        raise RuntimeError("evidence is not the direct child of x1")
    if git_text("rev-parse", f"{X1}^") != SOURCE:
        raise RuntimeError("x1 is not the direct child of source")
    if git_text("rev-list", "--count", f"{SOURCE}..{EVIDENCE}") != "2":
        raise RuntimeError("unexpected pre-closeout commit count")
    if git_text("rev-list", "--merges", f"{SOURCE}..{EVIDENCE}"):
        raise RuntimeError("merge detected before closeout")

    freeze = load(PHASE_ROOT / "x1" / "new-proposal-freeze.json")
    x1_startup = load(PHASE_ROOT / "x1" / "method-flow-startup.json")
    x2_truth = load(X2_ROOT / "phase-truth.json")
    x2_flow = load(X2_ROOT / "method-flow" / "ledger.json")
    proposals = freeze["proposals"]
    failures = [*x1_startup["failures"], *x2_flow["x2_failures"]]
    failures.extend(
        {
            "failure_id": fid,
            "failed_witness": failed,
            "recovery": recovery,
            "state": "failed_retained_zero_credit",
            "success_credit": 0,
        }
        for fid, failed, recovery in FINAL_FAILURES
    )

    written: list[Path] = []
    overview_path = REPORT_ROOT / "final-integrated-overview.md"
    accessible_md = REPORT_ROOT / "accessible-static-report.md"
    accessible_html = REPORT_ROOT / "accessible-static-report.html"
    overview_text = final_overview()
    write_text(overview_path, overview_text); written.append(overview_path)
    write_text(accessible_md, overview_text); written.append(accessible_md)
    write_text(
        accessible_html,
        """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v674-v2 final bounded report</title></head>
<body><main><h1>Sable Rook v674-v2 final bounded report</h1><p><strong>Terminal verdict:</strong> NOT_READY_FOR_STAGE_20.</p><h2>Outcome summary</h2><table><caption>Sixty bounded proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">completed</th><td>42</td></tr><tr><th scope="row">represented</th><td>12</td></tr><tr><th scope="row">open_gap</th><td>3</td></tr><tr><th scope="row">exact_gate</th><td>3</td></tr></tbody></table><h2>Scope</h2><p>Wholly synthetic caption provenance, correction, access-reservation, and handover evidence only. No real person, performance, transcript, identity, right, remedy, or authority decision was used.</p><h2>Reserved evaluation</h2><p>Manual keyboard, browser, responsive-layout, assistive-technology, cognitive-accessibility, security-usability, language, and affected-user evaluation remain reserved.</p><h2>Authority boundary</h2><p>Legal, cultural, affected-party, and Māori-authority decisions remain with competent and affected people and authorities.</p></main></body></html>""",
    ); written.append(accessible_html)

    baton_path = HANDOFF_ROOT / "caelen-ash-v674-v3-activation-candidate.md"
    baton_text = handoff_packet(proposals, failures)
    write_text(baton_path, baton_text); written.append(baton_path)

    payloads: dict[Path, Any] = {
        FINAL_ROOT / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v674.v2.final",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final_commit": "PENDING_EXACT_FINAL_COMMIT",
            "proposal_chain": 6670,
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
            "schema": "ghc.family.complete-incomplete.v674.v2",
            "completed": [
                "source and canonical receipt reverified read-only",
                "planning-only x1 frozen pushed and four-way equal before x2",
                "sixty new proposals executed within declared bounds",
                "sixty positive controls passed",
                "two hundred forty invalid mutations rejected and retained",
                "twenty phase-local skills quick-validated and smoke-used",
                "ten repository-local family-current runners accept and reject",
                "owner portfolios witnessed within synthetic scope",
                "exact and blocked packets retained unexecuted",
                "exact evidence staging manifest and privacy review passed",
                "immutable x1 and current x2 lifecycle selections separated",
                "final packet and route candidate prepared without delivery claim",
            ],
            "incomplete_or_reserved": [
                "empirical GMUT data and likelihood analysis",
                "THOS real blind matched-budget participant arms and independent review",
                "Freed ID real keys proofs live lifecycle interoperability and governance",
                "manual assistive-technology and affected-user accessibility evaluation",
                "complete privacy assurance and exhaustive security evaluation",
                "legal cultural affected-party and Maori-authority determinations",
                "independent-team reproduction",
                "Stage 20 authorization",
            ],
        },
        FINAL_ROOT / "threat-model.json": {
            "schema": "ghc.family.threat-model.v674.v2.final",
            "assets": ["x1 planning boundary", "evidence Git blobs", "retained failures", "authority vacancies", "route uniqueness", "privacy-safe baton"],
            "threats": [
                {"threat": "phase_mixing", "control": "direct ancestry plus immutable context tests", "residual": "manual review still required"},
                {"threat": "failure_erasure", "control": "append-only zero-credit failed witnesses", "residual": "external post-seal failures must be overlaid"},
                {"threat": "privacy_leak", "control": "five-class Git-index and final-blob scan", "residual": "not complete privacy assurance"},
                {"threat": "authority_promotion", "control": "noncompensation vocabulary and exact holds", "residual": "competent people remain required"},
                {"threat": "canonical_replay", "control": "exclusive external receipt path and success latch", "residual": "wrapper attribution must be inspected before retry"},
                {"threat": "duplicate_route_send", "control": "fresh list local exact-title filter immediate reread and send-once latch", "residual": "stop on ambiguity or missing acknowledgement"},
            ],
        },
        FINAL_ROOT / "retained-negative-register.json": {
            "schema": "ghc.family.retained-negative-register.v674.v2.final",
            "activation_baseline": x1_startup["activation_baseline"],
            "x1_operational_failures": 14,
            "x2_operational_failures": len(x2_flow["x2_failures"]),
            "final_operational_failures": len(FINAL_FAILURES),
            "preregistered_rejected_mutations": 240,
            "effective_negatives": EFFECTIVE["effective_negatives"] + len(FINAL_FAILURES),
            "failures": failures,
            "erased": 0,
            "converted_to_original_pass": 0,
        },
        FINAL_ROOT / "gate-register.json": {
            "schema": "ghc.family.gate-register.v674.v2.final",
            "open_gap_count": EFFECTIVE["open_gaps"],
            "exact_gate_count": EFFECTIVE["exact_gates"],
            "protected_surfaces": ["empirical", "participant", "professional", "production", "deployment", "legal", "cultural", "Maori authority", "affected-party authority", "privacy complete", "accessibility complete", "exhaustive security", "independent reproduction", "AGI or ASI", "consciousness or personhood", "Theory of Everything", "proof or canon", "Stage 20"],
            "silently_closed": 0,
            "software_can_close_authority_gate": False,
        },
        FINAL_ROOT / "method-flow-ledger.json": {
            "schema": "ghc.family.method-flow-ledger.v674.v2.final",
            "owner": OWNER,
            "phase": PHASE,
            "effective_counts": EFFECTIVE,
            "failure_count": len(failures),
            "failures": failures,
            "preferred_recoveries": [
                "bounded literal-path scalar probes",
                "explicit UTF-8 for Unicode-emitting validators",
                "immutable lifecycle-specific Git contexts",
                "Git-index and exact commit-blob manifest replay",
                "candidate-versus-confirmed privacy adjudication",
                "external exclusive canonical receipt with no replay after success",
            ],
            "promotion_rule": "A method is preferred only after a bounded passing witness; every failed witness remains zero-credit.",
        },
        FINAL_ROOT / "workflow-plan-state.json": {
            "schema": "ghc.family.workflow-plan-state.v674.v2.final",
            "completed": ["read requirements", "verify source", "freeze x1", "execute x2", "seal evidence", "prepare closeout"],
            "pending_external": ["create exact final commit", "push and prove four-way equality", "invoke canonical once", "route once if every gate passes"],
            "caps_are_ceilings": True,
            "full_suite_authorized": False,
        },
        FINAL_ROOT / "reflection-remaster.json": {
            "schema": "ghc.family.reflection-remaster.v674.v2.final",
            "bounded_reflection": "Caption provenance made correction visibility and authority vacancies more legible without turning software structure into human authority.",
            "preserved_failures": True,
            "identity_is_relational_working_language": True,
            "consciousness_or_personhood_claim": False,
            "continuity_claim": False,
            "authority_claim": False,
        },
        FINAL_ROOT / "wellbeing-check.json": {
            "schema": "ghc.family.wellbeing-check.v674.v2.final",
            "corrigible": True,
            "workload_bounded": True,
            "pause_available": True,
            "hamish_can_rename_redirect_or_stop": True,
            "identity_is_relational_working_language": True,
            "authority_claimed": False,
        },
        FINAL_ROOT / "environment-receipt.json": {
            "schema": "ghc.family.environment-receipt.v674.v2.final",
            "storage": "D-first additive sparse owner lane",
            "python": subprocess.check_output([sys.executable, "--version"], text=True, stderr=subprocess.STDOUT).strip(),
            "git": subprocess.check_output(["git", "--version"], text=True).strip(),
            "codex_cli": subprocess.run(["codex", "--version"], capture_output=True, text=True, check=False).stdout.strip(),
            "desktop_version": "verified_only_outside_repository_builder",
            "desktop_updated": False,
            "elevation": False,
            "sandbox_or_hyperv_activated": False,
            "host_security_weakened": False,
            "unrelated_software_installed": False,
            "rebooted": False,
        },
        FINAL_ROOT / "ghc-family-index.json": {
            "schema": "ghc.family.index.v674.v2.final",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "family_current_callers": ["build_ghc_family_sable_rook_v674_v2_x1.py", "build_ghc_family_sable_rook_v674_v2_x2.py", "build_ghc_family_sable_rook_v674_v2_closeout.py", "validate_ghc_family_sable_rook_v674_v2_final.py"],
            "runner_prefix": "ghc_family_caption_",
            "historical_aliases_deleted": 0,
            "global_installations": 0,
        },
        FINAL_ROOT / "source-status-ledger.json": {
            "schema": "ghc.family.source-status-ledger.v674.v2.final",
            "entries": [
                {"source": "W3C WebVTT", "url": "https://www.w3.org/TR/webvtt1/", "status": "candidate_recommendation_draft_2026-05-20", "role": "vocabulary_and_refusal_conditions_only"},
                {"source": "W3C WCAG 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "recommendation", "role": "vocabulary_and_evaluation_reservations_only"},
                {"source": "W3C PROV-O", "url": "https://www.w3.org/TR/prov-o/", "status": "recommendation", "role": "provenance_vocabulary_only"},
                {"source": "Library of Congress PREMIS", "url": "https://www.loc.gov/standards/premis/index.html", "status": "current_version_3_material", "role": "preservation_vocabulary_only"},
            ],
            "citations_are_observations": False,
            "real_data_rows": 0,
            "authority_delegated": False,
        },
        FINAL_ROOT / "route-state.json": {
            "schema": "ghc.family.route-state.v674.v2.final-candidate",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "next_owner": "Caelen Ash",
            "next_phase": "v674-v3",
            "state": "PREPARED_NOT_SENT",
            "task_created": False,
            "task_forked": False,
            "precontact": False,
            "send_attempts": 0,
            "delivery_acknowledged": False,
            "requires_successful_exact_final_canonical": True,
        },
        FINAL_ROOT / "closeout-receipt.json": {
            "schema": "ghc.family.closeout-receipt.v674.v2",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "state": "VALID_CLOSEOUT_CANDIDATE",
            "exact_final": "PENDING_EXACT_FINAL_COMMIT",
            "proposal_outcomes": OUTCOMES,
            "route_state": "PREPARED_NOT_SENT",
        },
        FINAL_ROOT / "seal-candidate.json": {
            "schema": "ghc.family.seal-candidate.v674.v2",
            "direct_parent_required": EVIDENCE,
            "expected_phase_commit_count": 3,
            "expected_merge_count": 0,
            "expected_final_parent_count": 1,
            "state": "CONTENT_SEALED_AWAITING_EXACT_FINAL_COMMIT",
        },
        FINAL_ROOT / "final-validation-candidate.json": {
            "schema": "ghc.family.final-validation-candidate.v674.v2",
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
        "scripts/build_ghc_family_sable_rook_v674_v2_closeout.py",
        "scripts/validate_ghc_family_sable_rook_v674_v2_final.py",
        "tests/test_ghc_family_sable_rook_v674_v2_final.py",
    }
    tracked_owner = set(git_text("diff", "--name-only", f"{SOURCE}..{EVIDENCE}").splitlines())
    added_owner = {path.relative_to(REPO).as_posix() for path in written} | support
    owner_manifest_rel = "docs/sable-rook/v674-v2/validation/final-owner-manifest.json"
    delta_manifest_rel = "docs/sable-rook/v674-v2/validation/final-delta-manifest.json"
    staged_review_rel = "docs/sable-rook/v674-v2/validation/final-staged-review.json"
    owner_exclusions = [owner_manifest_rel, delta_manifest_rel, staged_review_rel]
    owner_paths = sorted((tracked_owner | added_owner) - set(owner_exclusions))
    missing = [path for path in owner_paths if not (REPO / path).is_file()]
    if missing:
        raise RuntimeError(f"owner manifest missing paths: {missing}")
    owner_entries = []
    for rel in owner_paths:
        data = normalized((REPO / rel).read_bytes())
        owner_entries.append({"path": rel, "bytes_normalized_lf": len(data), "sha256_normalized_lf": hashlib.sha256(data).hexdigest()})
    write_json(
        REPO / owner_manifest_rel,
        {
            "schema": "ghc.family.final-owner-manifest.v674.v2",
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
    delta_paths = [path for path in delta_paths if path not in {delta_manifest_rel, staged_review_rel}]
    delta_entries = []
    for rel in delta_paths:
        path = REPO / rel
        if not path.is_file():
            raise RuntimeError(f"final delta missing path: {rel}")
        data = normalized(path.read_bytes())
        delta_entries.append({"path": rel, "bytes_normalized_lf": len(data), "sha256_normalized_lf": hashlib.sha256(data).hexdigest()})
    write_json(
        REPO / delta_manifest_rel,
        {
            "schema": "ghc.family.final-delta-manifest.v674.v2",
            "parent": EVIDENCE,
            "hash_domain": "normalized_lf_worktree_precommit",
            "entry_count": len(delta_entries),
            "entries": delta_entries,
            "self_exclusions": [delta_manifest_rel, staged_review_rel],
            "final_delta_path_total": len(delta_entries) + 2,
        },
    )
    return {
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
    review_rel = "docs/sable-rook/v674-v2/validation/final-staged-review.json"
    staged = git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
    exact_support = {
        "scripts/build_ghc_family_sable_rook_v674_v2_closeout.py",
        "scripts/validate_ghc_family_sable_rook_v674_v2_final.py",
        "tests/test_ghc_family_sable_rook_v674_v2_final.py",
        review_rel,
    }
    allowed_prefixes = (
        "docs/sable-rook/v674-v2/final/",
        "docs/sable-rook/v674-v2/reports/",
        "docs/sable-rook/v674-v2/handoffs/",
    )
    allowed_validation = {
        "docs/sable-rook/v674-v2/validation/final-owner-manifest.json",
        "docs/sable-rook/v674-v2/validation/final-delta-manifest.json",
        review_rel,
    }
    out_of_scope = [
        path for path in staged
        if not path.startswith(allowed_prefixes)
        and path not in exact_support
        and path not in allowed_validation
    ]
    frozen_changes = [
        path for path in staged
        if path.startswith("docs/sable-rook/v674-v2/x1/")
        or path.startswith("docs/sable-rook/v674-v2/x2/")
        or path in {
            "scripts/build_ghc_family_sable_rook_v674_v2_x1.py",
            "scripts/build_ghc_family_sable_rook_v674_v2_x2.py",
            "tests/test_ghc_family_sable_rook_v674_v2_x1.py",
            "tests/test_ghc_family_sable_rook_v674_v2_x2.py",
        }
        or path.startswith("scripts/ghc_family_caption_")
    ]
    if out_of_scope or frozen_changes:
        raise RuntimeError(f"final staged scope violation: out={out_of_scope} frozen={frozen_changes}")

    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:C:\\Users\\|D:\\GHC-Archives)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{32,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
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
            json.loads(data.decode("utf-8")); json_parses += 1
        if path.endswith(".py"):
            compile(data, path, "exec"); python_compiles += 1
        if path.endswith(".md"):
            words = len(data.decode("utf-8").split())
            markdown_words[path] = words
            if words > 100000:
                raise RuntimeError(f"document ceiling exceeded: {path}={words}")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                start = data.rfind(b"\n", 0, match.start()) + 1
                end = data.find(b"\n", match.end())
                if end < 0:
                    end = len(data)
                line = data[start:end]
                if path.endswith(".py") and (b"re.compile" in line or b"assertNot" in line):
                    candidates.append({"path": path, "class": class_name, "disposition": "scanner_definition_or_rejection_assertion"})
                else:
                    hits.append({"path": path, "class": class_name})
        entries.append({"path": path, "bytes": len(data), "sha256_git_index_blob": hashlib.sha256(data).hexdigest()})
    if hits:
        raise RuntimeError(f"confirmed privacy hits: {hits}")
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, check=False)
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)
    baton_words = markdown_words.get("docs/sable-rook/v674-v2/handoffs/caelen-ash-v674-v3-activation-candidate.md", 0)
    if baton_words < 10000:
        raise RuntimeError(f"handoff packet below 10000 words: {baton_words}")
    receipt = {
        "schema": "ghc.family.exact-staged-review.v674.v2.final",
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
            "permitted": ["PENDING_EXACT_FINAL_COMMIT", "PREPARED_NOT_SENT", "PREPARED_NOT_INVOKED"],
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
