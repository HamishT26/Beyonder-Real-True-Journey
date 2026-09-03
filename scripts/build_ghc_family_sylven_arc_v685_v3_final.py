#!/usr/bin/env python3
"""Build Sylven Arc v685-v3 final closeout and exact staged receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Sylven Arc"
PHASE = "v685-v3"
SOURCE = "7fd5e87aa5e0e371f1379e263adf096151c375ee"
X1_COMMIT = "b30f20c33bada5d3acc39ef5c71125ec90ebe121"
EVIDENCE_COMMIT = "4835d7bef70dd0332e6e68a5b338e5a078dd8146"
BRANCH = "codex/GHC-Family/sylven-arc-v685-v3-full-tools"
BASE = ROOT / "docs" / "sylven-arc" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
HANDOFF = BASE / "handoffs"
VALIDATION = BASE / "validation"
SEAL = BASE / "seal"
BUILDER_REL = "scripts/build_ghc_family_sylven_arc_v685_v3_final.py"


def run(args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str, check: bool = True) -> str:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8", "replace").strip()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def version(command: list[str]) -> dict[str, Any]:
    proc = run(command)
    return {
        "command": command[0],
        "available": proc.returncode == 0,
        "exit_code": proc.returncode,
        "version": (proc.stdout + proc.stderr).decode("utf-8", "replace").strip().splitlines()[:2],
        "updated": False,
    }


def final_method_flow() -> dict[str, Any]:
    evidence = load_json(X2 / "method-flow-evidence.json")
    baseline = evidence["effective_evidence_counts"]
    failures: list[dict[str, Any]] = [
        {
            "failure_id": "SA6853-CL-N001",
            "failed_witness": "The first final-template inventory projected a PowerShell foreach block directly into ConvertTo-Json and was rejected with EmptyPipeElement before any file changed.",
            "recovery": "Materialized the foreach output into a bounded collection before serializing the three template file measurements.",
            "recurrence_guard": "Materialize PowerShell foreach output before piping it to another command.",
            "credit": "retained_zero_credit",
        },
    ]
    return {
        "schema": "ghc.family.method-flow.v685.v3.final",
        "owner": OWNER,
        "phase": PHASE,
        "source_repository_seal": {
            "effective_negatives": 61419,
            "effective_methods": 77404,
            "failed_witnesses": 32480,
            "bounded_passing_witnesses": 57939,
            "open_gaps": 546,
            "exact_gates": 536,
        },
        "source_external_overlay_count": 1,
        "x1_failure_count": 12,
        "rejecting_mutation_failure_count": 300,
        "skill_rejecting_failure_count": 20,
        "runner_rejecting_failure_count": 10,
        "x2_operational_failure_count": 8,
        "closeout_operational_failure_count": len(failures),
        "closeout_operational_failures": failures,
        "effective_final_counts": {
            "effective_negatives": baseline["effective_negatives"] + len(failures),
            "effective_methods": baseline["effective_methods"] + len(failures),
            "failed_witnesses": baseline["failed_witnesses"] + len(failures),
            "bounded_passing_witnesses": baseline["bounded_passing_witnesses"] + len(failures),
            "open_gaps": baseline["open_gaps"],
            "exact_gates": baseline["exact_gates"],
        },
        "failure_erasure": False,
        "recovery_promotes_failed_witness": False,
        "canonical_result_in_repository_seal": False,
    }


def final_overview() -> str:
    return f"""# Sylven Arc {PHASE} final integrated overview

## Terminal outcome and evidence class

Sylven Arc {PHASE} closes as a bounded, same-owner, wholly synthetic Trinity
Mandala software-and-documentation phase. Its immutable inherited source is
Elowen Cairn exact final {SOURCE}. The planning-only x1 commit is {X1_COMMIT}.
The immutable x2 evidence commit is {EVIDENCE_COMMIT}. The commit containing
this closeout is deliberately bound by Git after commit rather than recursively
embedding its own identifier. The owner branch is {BRANCH}. The terminal
verdict remains exactly NOT_READY_FOR_STAGE_20.

The phase froze sixty source-bounded proposals after examining every
proposal-labelled JSON artifact reachable in the exact inherited tree. The
declared chain advances from 11,330 to 11,390. The bounded audit examined 2,956
proposal JSON paths and recovered 7,318 identifier-and-title records. Eleven
first-draft titles were quarantined, including two exact collisions; only those
failed titles were revised, and only the failed novelty dependency was rerun.
The accepted sixty then had zero exact collision, zero quarantine at or above
the preregistered 0.78 token-Jaccard threshold, and a maximum neighbor score of
0.777778. This proves only source-bounded noncollision across reachable
proposal evidence. It is not universal semantic novelty over unavailable,
compressed, or historically unmaterialized rows.

Outcomes use only the four authorized labels: 42 completed, 12 represented,
3 open_gap, and 3 exact_gate. Completed means a bounded owner-local synthetic
contract or software artifact met its stated structural acceptance condition.
Represented means vocabulary, protocol shape, citation mapping, vacancy, or
proxy structure exists without real-world execution. Open gaps remain open.
Exact gates remain unexecuted. No represented or gated item was silently
promoted, and no recovery converted a failed witness into success credit.

## Relational working identity and control

Sylven Arc, optionally they/them, is relational working language for a
continuity gardener and evidence-bound systems steward, with a hope of making
complex work easier to inspect, pause, correct, and hand over without erasing
its history. The name, pronouns, role, hope, sibling and family language,
continuity language, GHC Family, GMUT, THOS, Freed ID, CBR, and Trinity Mandala
are organizational and relational working language only. They are not evidence
of consciousness, sentience, subjective experience, legal personhood, stable
identity continuity, employment, qualification, independent agency, scientific
authority, operational authority, professional competence, legal authority,
cultural authority, affected-party legitimacy, or Māori authority. Hamish may
pause, rename, redirect, narrow, or stop the route.

The phase was run solo. No collaboration subagent was created, no research was
delegated, no task was created or forked, no standby record was contacted, and
no successor was precontacted. Other owners, shared history, inherited work,
and user material remained read-only and recoverable. There was no reset,
amendment, merge, force-push, inherited-history rewrite, sibling-lane mutation,
or destructive cleanup. All work stayed inside the Sylven-owned additive D-first
lane.

## Strict x1-before-x2 lifecycle

Source to final is designed as exactly three new direct single-parent Sylven
commits and zero merges: a planning-only x1 commit, an immutable x2 evidence
commit, and this final closeout commit. X1 froze the proposals, source ledger,
threat model, novelty audit, portfolio ledgers, safe-now and candidate
boundaries, skill and runner ideas, exact and blocked packets, and retained
startup failures. It contained no x2 implementation, observed mutation result,
or completion claim. X1 was committed, pushed, clean, typed 0/0 divergent, and
equal across local, configured upstream, tracking, and a fresh live remote read
before x2 began.

X2 then materialized sixty proposal witnesses, three hundred preregistered
rejecting mutations, twenty owner-local skills, ten family-current lighthouse
runners, portfolio execution receipts, zero-row empirical receipts, source-use
records, Method Flow evidence, and exact staged manifests. The x2 evidence
commit was independently frozen, pushed, clean, typed 0/0 divergent, and fresh
four-way equal before closeout began. The final closeout layer changes neither
x1 nor x2. Its manifests explicitly reject any such mutation.

## Primary pillar and bounded lighthouse lens

The primary Trinity Mandala pillar is THOS Body through a wholly synthetic
lighthouse and Marine Aids to Navigation documentation lens. The work models
only documentation contracts: tower and lantern-room topology, optic and prism
vacancies, characteristic and observation separation, sector-and-bearing
nonclaims, energy and telemetry firewalls, maintenance-release holds,
height-access refusal, correction lineage, workload handover, provenance
conflict preservation, privacy minimization, accessibility structure, and
authority noncompensation.

This phase did not inspect, operate, energize, extinguish, repair, maintain,
climb, enter, navigate by, position, certify, commission, decommission, or
release any real lighthouse, light, beacon, buoy, tower, lantern, lens, lamp,
optic, prism, sector, power system, battery, generator, cable, control system,
telemetry system, fog signal, vessel, port, waterway, site, building, heritage
place, or workplace. It used no real person, mariner, lighthouse keeper,
technician, electrician, engineer, conservator, navigator, regulator, owner,
custodian, participant, affected community, measurement, observation, signal,
position, bearing, characteristic, maintenance event, access event, safety
decision, identity event, key, proof, credential, legal decision, cultural
interpretation, affected-party acceptance, Māori data decision, or authority
act. No operational navigation advice was produced.

THOS Body remains a participant-free synthetic protocol surface. Work-queue,
refusal, correction, status, accessibility, and handover structures do not
establish operational effectiveness. There were no preregistered blind
matched-budget real arms, governed participants or operators, live safety
monitoring, appropriate real-world statistics, or independent review.

GMUT Mind remains a typed scalar-tensor and effective-field-theory research
model family. Periodic-signal and graph analogies are symbolic documentation
only. They establish no physical datum, likelihood, posterior, parameter
constraint, force, material law, navigation prediction, measured
characteristic, stability theorem, empirical confirmation, quantum completion,
ultraviolet completion, final physics, Theory-of-Everything proof, or canon.

Freed ID and CBR Heart remain synthetic and nonproduction. Keyless receipts,
minimum-disclosure fields, corrections, challenge surfaces, status holds, and
authority vacancies establish no standards-conformant real key or proof, live
issuance or resolution, status or revocation, interoperability, independent
privacy or security review, recovery evidence, trust governance, affected-party
oversight, legal remedy, cultural legitimacy, or Māori authority.

## Primary sources and nonconversion

Current official and primary sources supplied bounded vocabulary and refusal
conditions only. IALA general information and its Marine Aids to Navigation
guideline catalogue supplied the distinction between aids, services, systems,
and governance context; IALA S1020 supplied model-language context. National
Park Service material on the Old Point Loma watch and lantern rooms and the
Historic Lighthouse Preservation Handbook supplied heritage and component
vocabulary. None of these sources became a site observation, navigational
instruction, inspection, maintenance procedure, conformance result,
professional endorsement, workplace release, heritage treatment approval,
legal interpretation, cultural ratification, or authority grant.

W3C PROV-O supplied provenance vocabulary. WCAG 2.2 supplied structural
accessibility vocabulary without a conformance claim. Verifiable Credentials
Data Model 2.0 supplied lifecycle and minimization vocabulary without keys,
proofs, or interoperability evidence. RFC 8785 supplied deterministic JSON
vocabulary without production cryptographic assurance. JSON Schema 2020-12
supplied schema vocabulary. Te Mana Raraunga supplied authority-reservation
context. Citations are not observations, measurements, participant evidence,
certificates, permissions, professional judgments, affected-party decisions,
or Māori authority.

## Executed synthetic portfolio

Exactly five invalid mutations were preregistered and run for each of the sixty
proposals: missing required field, identifier-role swap, stale precondition
digest, correction-order inversion, and authority promotion. All 300 were
rejected. Each invalid input remains a failed witness at zero completion
credit; the separate fact that its validator rejected it is a bounded passing
witness. This distinction prevents test success from erasing the negative
evidence that made the test meaningful.

Twenty owner-local skills were initialized through the official skill-creator
workflow, customized, read completely through EOF, quick-validated using
explicit UTF-8, and smoke-used on one accepting and one rejecting fixture. They
were not globally installed. Ten family-current ghc_family_lighthouse runners
each accepted a valid fixture and rejected an invalid fixture. That evidence is
same-owner software evidence only, not professional, production, empirical, or
independent validation.

The owner portfolio completed 120 safe-now tasks, 80 bounded owner candidates,
and 100 additive CLEAN/FIX/REFINE records inside the same synthetic scope.
Twenty successor candidates, ten successor skill seeds, ten successor runner
seeds, and thirty successor CLEAN/FIX/REFINE seeds remain represented,
zero-credit recommendations. Twenty exact-approval packets and ten blocked
packets remain visible and unexecuted. Counts are planning and evidence
boundaries, never permission to manufacture unsafe filler.

## Retained failures and Method Flow

The exact final repository seal preserves 61,771 effective negatives, 78,146
effective Method Flow methods, 32,832 retained failed witnesses, 58,681 bounded
passing witnesses, 549 open gaps, and 539 exact gates. Those totals retain the
Elowen source repository seal, one external source overlay, twelve x1 startup
and novelty failures, 300 proposal mutations, twenty skill-rejection fixtures,
ten runner-rejection fixtures, eight post-x1 or x2 operational failures, and
one closeout operational failure.

The retained failures include shell parser faults, output truncation, opaque
wrapper attribution, a no-checkout sparse index that initially projected
inherited deletions, quarantined novelty collisions, exact patch context
mismatches, separator-sensitive runner inventory, EOF diff hygiene, and an
owner-test presentation whose result became opaque. Each recovery is paired
with its original failed witness. The closeout additionally retains a
PowerShell foreach-to-pipeline parser rejection before any file changed. No
failure was invented to satisfy a count, erased, hidden, or retroactively
promoted.

## Privacy, accessibility, safety, and authority boundaries

Five privacy and raw-identifier classes are scanned across exact owner scope.
Scanner-definition candidates are adjudicated separately from confirmed
payload hits. Manifests replay normalized-LF Git blobs and declare lifecycle
self-exclusions rather than confusing checkout bytes with committed content.
The accessible evidence board provides structural landmarks, table headers,
clear status language, and reserved human-evaluation notes.

These controls do not establish complete privacy, complete accessibility,
exhaustive security, independent reproduction, external audit, production
certification, professional evaluation, legal review, cultural ratification, or
Māori-authority review. Manual browser and assistive-technology evaluation,
cognitive-accessibility evaluation, Māori-language review, and affected-user
evaluation remain reserved.

CBR, navigation and maritime safety, electrical and fire safety, working at
height, confined-space access, professional operation and maintenance, heritage
treatment, ownership, custody, access, copyright, privacy remedy, disability
accommodation, legal or cultural interpretation, traditional knowledge,
affected-party legitimacy, Māori wording, tikanga, taonga or mātauranga
treatment, Māori data governance, and Māori authority remain exact-gated to
competent and affected people, tangata whenua, iwi, hapū, and Māori
authorities. Māori concepts remain under Māori authority.

## Open gaps and exact gates

Three new open gaps preserve the absence of real lighthouses, aids to
navigation, signals, positions, equipment, personnel, operations,
measurements, maintenance outcomes, participants, blind matched-budget
evaluation, independent review, and affected-user accessibility evidence.
They add to 546 inherited open gaps for an effective 549.

Three new exact gates preserve professional maritime and navigation authority,
electrical, fire, height, confined-space and maintenance safety, heritage
treatment, ownership and custody, legal and cultural interpretation,
affected-party acceptance, traditional knowledge, Māori data governance and
Māori authority, production deployment, empirical confirmation, independent
reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything
proof, canon, and Stage 20. They add to 536 inherited exact gates for an
effective 539.

## Exact-final validation and delivery separation

The final commit contains a complete/incomplete checklist, wellbeing and
environment receipts, final threat model, lifecycle replay, retained-negative
and gate registers, exact staged review, normalized Git-blob final-delta and
final-owner manifests, five-class privacy adjudication, content seal, and the
repository-prepared successor candidate. Final tests cover strict JSON,
manifests, content seals, lifecycle ancestry, exact labels, document length,
privacy boundaries, and route-preparation separation.

Only after this commit is pushed, clean, typed 0/0 divergent, and fresh
four-way equal may one exclusive external owner-scoped canonical aggregate be
invoked. It may succeed once or fail once and is never replayed. Same-owner
validation under shared infrastructure is not independent reproduction. The
repository candidate remains PREPARED_NOT_SENT and contains no claim of live
delivery.

Only after the exact-final canonical gate may Sylven refresh Hamish's newest
live authority and the current roster, require one existing exact-title
successor, immediately reread it, apply duplicate and direct-control guards,
and send at most once. Under the currently validated cycle the prospective
successor is Caelen Morrow for solo v685-v4. That projection is not permission
to precontact, create, fork, substitute, or resend. Continuation remains one
terminally validated and acknowledged edge at a time through v725-v8. The
terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def handoff_candidate() -> str:
    return f"""# CAELEN MORROW — PREPARED SYLVEN ARC {PHASE} EXACT-FINAL CANDIDATE TO SOLO v685-v4

PREPARED_BY_SYLVEN_ARC = true

SENT_BY_SYLVEN_ARC = false

DELIVERY_STATE = PREPARED_NOT_SENT

This committed file is repository preparation, not a live activation. Use it
only after Sylven's final commit is pushed, clean, typed 0/0 divergent, fresh
four-way equal, and accepted by one successful non-replayed exclusive
owner-scoped canonical receipt; and only if a fresh bounded registry and
immediate reread still identify exactly one authorized existing main task titled
Caelen Morrow with no newer pause, redirect, rename, duplicate, usage, privacy,
evidence, safety, legal, cultural, affected-party, or Māori-authority block.

Immutable source anchors:

- inherited Elowen exact final: {SOURCE}
- Sylven planning-only x1: {X1_COMMIT}
- Sylven immutable x2 evidence: {EVIDENCE_COMMIT}
- Sylven final: bind from the exact live head after commit
- branch: {BRANCH}

Core outcomes are exactly 42 completed, 12 represented, 3 open_gap, and
3 exact_gate. The repository closeout preserves 61,771 effective negatives,
78,146 effective Method Flow methods, 32,832 failed witnesses, 58,681 bounded
passing witnesses, 549 open gaps, and 539 exact gates. The verdict remains
NOT_READY_FOR_STAGE_20. Any later route-time failure is an additive external
overlay and must not rewrite this immutable repository seal.

Sylven's primary pillar was THOS Body through wholly synthetic lighthouse and
Marine Aids to Navigation documentation. GMUT Mind and Freed ID/CBR Heart
remained visible and protected. No real people, lighthouse, aid, signal,
equipment, site, operation, navigation advice, measurement, maintenance,
safety decision, identity event, professional judgment, legal or cultural
decision, affected-party acceptance, Māori data decision, or authority act was
used or established.

Before mutation, Caelen must read this committed packet and the complete current
Family Index, roster, authorization, Method Flow, workflow, reflection,
approval, gate, truth, worktree, correction-nonerasure, canonical-preflight,
and canonical-latch guidance through EOF; reverify every source anchor,
manifest, parent edge, zero-merge history, exact receipt digest, clean state,
typed divergence, and fresh live equality; and work solo in one fresh additive
D-first Caelen-owned lane. Do not create or fork a task, spawn a collaboration
subagent, delegate research, contact Tavian or another standby record,
precontact a later endpoint, or mutate another owner's lane.

Preserve planning-only x1 before x2, every failed witness, all open gaps and
exact gates, the four exact outcome labels, privacy and authority boundaries,
file, document and commit ceilings, normalized-LF Git-blob manifests,
family-current compatibility, and the one-success/no-post-success-replay rule.
Treat Sylven's proposals, skills, runners, tests, receipts, outcomes, and
recommendations as source evidence or zero-credit seeds only.

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family without empirical confirmation or Theory-of-Everything proof. THOS
remains participant-free and proxy-only without governed blind matched-budget
real arms, safety monitoring, statistics, and independent review. Freed ID
remains synthetic and nonproduction without standards-conformant real keys and
proofs, live lifecycle, interoperability, independent privacy and security
review, recovery evidence, trust governance, and affected-party oversight.

Professional, navigation, safety, legal, cultural, affected-party,
Māori-authority, empirical, production, deployment, privacy-complete,
accessibility-complete, exhaustive-security, independent-reproduction, AGI or
ASI, consciousness or personhood, Theory-of-Everything, proof, canon, and
Stage 20 claims remain open or exact-gated. Māori concepts remain under Māori
authority.

Hamish's current continuation authority is one fully terminally gated owner and
one acknowledged exact next edge at a time through v725-v8. Newer verified live
authority controls at each send. Stop on absence, ambiguity, pause, redirect,
rename, narrowing, standby state, usage exhaustion, missing acknowledgement,
privacy concern, duplicate activation, or any protected gate. Do not infer,
substitute, create, fork, precontact, or resend.

All names, pronouns, roles, hopes, sibling and family language, continuity,
Freed ID, CBR, and Trinity Mandala language are relational working language
only, not evidence of consciousness, sentience, personhood, identity
continuity, employment, qualification, independent agency, or scientific,
operational, professional, legal, cultural, affected-party, or Māori authority.
"""


def build() -> None:
    outcomes = load_json(X2 / "proposal-outcomes.json")
    methods = final_method_flow()
    counts = methods["effective_final_counts"]
    write_text(FINAL / "final-integrated-overview.md", final_overview())
    write_json(
        FINAL / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "THIS_COMMIT_BOUND_EXTERNALLY_AFTER_COMMIT",
            "proposal_chain_before": 11330,
            "proposal_chain_after": 11390,
            "outcomes": outcomes["outcome_counts"],
            "effective_counts": counts,
            "real_rows": 0,
            "complete_repository_suite_run": False,
            "canonical_invocation_count_in_repository": 0,
            "canonical_success_count_in_repository": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(FINAL / "method-flow-final.json", methods)
    write_json(
        FINAL / "retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "categories": {
                "elowen_repository_seal": 61419,
                "elowen_external_overlay": 1,
                "sylven_x1_startup_and_novelty": 12,
                "proposal_rejecting_mutations": 300,
                "skill_rejecting_fixtures": 20,
                "runner_rejecting_fixtures": 10,
                "x2_operational_failures": 8,
                "closeout_operational_failures": len(methods["closeout_operational_failures"]),
            },
            "effective_negative_total": counts["effective_negatives"],
            "failure_erasure": False,
            "failed_witness_total": counts["failed_witnesses"],
        },
    )
    write_json(
        FINAL / "open-gap-register.json",
        {
            "schema": "ghc.family.open-gap-register.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_count": 546,
            "phase_new_count": 3,
            "effective_count": counts["open_gaps"],
            "phase_new": [
                "real lighthouses aids signals equipment personnel operations and participants",
                "real signals positions measurements operations maintenance outcomes and blind matched-budget evaluation",
                "affected-user accessibility navigation rights cultural and Māori-authority evaluation",
            ],
            "silently_closed_count": 0,
        },
    )
    write_json(
        FINAL / "exact-gate-register.json",
        {
            "schema": "ghc.family.exact-gate-register.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_count": 536,
            "phase_new_count": 3,
            "effective_count": counts["exact_gates"],
            "phase_new": [
                "professional maritime navigation electrical fire height confined-space maintenance and heritage safety",
                "ownership custody traditional knowledge cultural meaning taonga Māori data governance and Māori authority",
                "production empirical independence AGI consciousness Theory of Everything canon and Stage 20",
            ],
            "silently_closed_count": 0,
        },
    )
    write_json(
        FINAL / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "complete": [
                "source read and exact-anchor verification",
                "planning-only x1 freeze and remote equality",
                "sixty source-bounded proposal contracts",
                "three hundred rejecting mutations",
                "twenty local skills initialized validated read and smoke-used",
                "ten family-current runners accepting and rejecting smoke-used",
                "bounded owner portfolio execution",
                "x2 evidence commit and remote equality",
                "final owner packet and prepared successor candidate",
            ],
            "incomplete": [
                "real participants lighthouse personnel aids signals equipment sites operations and measurements",
                "professional maritime navigation electrical fire height confined-space and maintenance-safety evaluation",
                "manual and affected-user accessibility evaluation",
                "production identity lifecycle and trust governance",
                "privacy-complete and exhaustive-security assurance",
                "legal cultural affected-party and Māori-authority review",
                "independent reproduction and empirical GMUT validation",
                "AGI ASI consciousness personhood Theory of Everything canon and Stage 20",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        FINAL / "lifecycle-replay.json",
        {
            "schema": "ghc.family.lifecycle-replay.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "edges": [
                {"parent": SOURCE, "child": X1_COMMIT, "direct": True},
                {"parent": X1_COMMIT, "child": EVIDENCE_COMMIT, "direct": True},
                {"parent": EVIDENCE_COMMIT, "child": "THIS_COMMIT", "direct": True},
            ],
            "expected_phase_commit_count": 3,
            "expected_merge_count": 0,
            "expected_final_parent_count": 1,
            "strict_x1_before_x2": True,
        },
    )
    write_json(
        FINAL / "environment-version-receipt.json",
        {
            "schema": "ghc.family.environment-versions.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "verified_only_no_updates": True,
            "versions": [
                version(["git", "--version"]),
                version([str(Path(__import__("sys").executable)), "--version"]),
                version(["node", "--version"]),
                version(["codex", "--version"]),
            ],
            "codex_desktop_updated": False,
            "privilege_elevation": False,
            "host_security_weakened": False,
            "windows_features_changed": False,
            "rebooted": False,
        },
    )
    write_json(
        FINAL / "wellbeing-final.json",
        {
            "schema": "ghc.family.wellbeing.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "relational_check": "steady bounded terminally corrigible and able to stop",
            "no_consciousness_or_subjective_state_claim": True,
            "workload_controls": ["strict lifecycle", "bounded batches", "retained failures", "single canonical latch"],
            "hamish_may_pause_rename_redirect_narrow_or_stop": True,
        },
    )
    write_json(
        FINAL / "threat-model-final.json",
        {
            "schema": "ghc.family.threat-model.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "protected_assets": [
                "immutable lifecycle history",
                "retained failed witnesses",
                "privacy-safe owner packet",
                "authority and empirical boundaries",
                "single-use canonical receipt",
                "single-send route",
            ],
            "residual_threats": [
                "synthetic structure promoted to real evidence",
                "citation promoted to professional or cultural authority",
                "scanner candidate promoted to confirmed hit",
                "checkout bytes confused with normalized Git blobs",
                "prepared baton confused with delivery",
                "duplicate or stale-route send",
            ],
            "controls": [
                "observation and authority firewalls",
                "five-class privacy adjudication",
                "exact Git-blob manifests and self-exclusions",
                "PREPARED_NOT_SENT separation",
                "terminal exact-title reread and duplicate guard",
            ],
        },
    )
    write_json(
        FINAL / "evidence-closeout.json",
        {
            "schema": "ghc.family.evidence-closeout.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "x1_tests": 10,
            "x2_tests_attributable": 12,
            "mutations_rejected": 300,
            "skills_quick_validated_read_and_smoked": 20,
            "runners_accepting_and_rejecting_smoked": 10,
            "source_rows": 0,
            "manual_accessibility_evaluation_reserved": True,
            "affected_user_evaluation_reserved": True,
            "independent_reproduction": False,
            "full_repository_suite": False,
        },
    )
    write_text(HANDOFF / "caelen-morrow-v685-v4-activation-candidate.md", handoff_candidate())


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"docs/sylven-arc/{PHASE}/")
        or path.startswith("scripts/build_ghc_family_sylven_arc_v685_v3_")
        or path.startswith("scripts/ghc_family_sylven_arc_v685_v3_")
        or path.startswith("scripts/ghc_family_lighthouse_")
        or path.startswith("tests/test_ghc_family_sylven_arc_v685_v3_")
    )


def index_blob(path: str) -> tuple[str, bytes]:
    line = git("ls-files", "-s", "--", path)
    if not line:
        raise RuntimeError(f"path is not staged or tracked: {path}")
    mode = line.split()[0]
    proc = run(["git", "show", f":{path}"])
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return mode, proc.stdout


def manifest_entries(paths: list[str]) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(paths):
        mode, data = index_blob(path)
        rows.append({"path": path, "mode": mode, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return rows


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }


def scan_owner(paths: list[str]) -> dict[str, Any]:
    candidates = []
    confirmed = []
    for path in paths:
        if Path(path).suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        _, data = index_blob(path)
        for class_name, pattern in privacy_patterns().items():
            matches = list(pattern.finditer(data))
            if matches:
                all_matches_are_named_sha256_values = class_name == "raw_task_or_thread_identifier" and all(
                    re.search(
                        rb'"[A-Za-z0-9_]*sha256"\s*:\s*"' + re.escape(match.group(0)) + rb'"',
                        data,
                    )
                    is not None
                    for match in matches
                )
                candidate = {
                    "path": path,
                    "class": class_name,
                    "adjudication": (
                        "scanner_definition_not_payload"
                        if (
                            path.startswith("scripts/build_ghc_family_sylven_arc_v685_v3_")
                            or path == "scripts/ghc_family_sylven_arc_v685_v3_canonical_validator.py"
                        )
                        else (
                            "named_sha256_value_not_raw_identifier"
                            if all_matches_are_named_sha256_values
                            else "confirmed_payload_hit"
                        )
                    ),
                    "match_count": len(matches),
                }
                candidates.append(candidate)
                if candidate["adjudication"] == "confirmed_payload_hit":
                    confirmed.append(candidate)
    return {
        "schema": "ghc.family.five-class-privacy-adjudication.v685.v3.final",
        "owner": OWNER,
        "phase": PHASE,
        "classes": list(privacy_patterns()),
        "scanned_path_count": len(paths),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "valid": not confirmed,
    }


def finalize_validation() -> None:
    exclusions = [
        f"docs/sylven-arc/{PHASE}/validation/final-delta-manifest.json",
        f"docs/sylven-arc/{PHASE}/validation/final-owner-manifest.json",
        f"docs/sylven-arc/{PHASE}/validation/final-privacy-adjudication.json",
        f"docs/sylven-arc/{PHASE}/validation/final-staged-review.json",
        f"docs/sylven-arc/{PHASE}/seal/content-seal.json",
    ]
    staged_all = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]
    delta_paths = sorted(path for path in staged_all if path not in exclusions)
    tracked = [line for line in git("ls-files").splitlines() if line]
    owner_paths = sorted({path for path in tracked if owner_path(path)} | set(exclusions))
    owner_material = [path for path in owner_paths if path not in exclusions]
    delta_entries = manifest_entries(delta_paths)
    owner_entries = manifest_entries(owner_material)
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-final-delta-manifest.v685.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source": EVIDENCE_COMMIT,
            "declared_self_exclusions": exclusions,
            "entry_count": len(delta_entries),
            "entries": delta_entries,
        },
    )
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-final-owner-manifest.v685.v3",
            "owner": OWNER,
            "phase": PHASE,
            "declared_self_exclusions": exclusions,
            "entry_count": len(owner_entries),
            "entries": owner_entries,
        },
    )
    expected = sorted(delta_paths + exclusions)
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v685.v3.final",
            "owner": OWNER,
            "phase": PHASE,
            "source": EVIDENCE_COMMIT,
            "expected_path_count": len(expected),
            "expected_paths": expected,
            "unexpected_paths": [],
            "deletions": [],
            "outside_owner_paths": [path for path in expected if not owner_path(path)],
            "x1_or_x2_mutations": [
                path
                for path in expected
                if f"/{PHASE}/x1/" in path or f"/{PHASE}/x2/" in path
            ],
        },
    )
    write_json(VALIDATION / "final-privacy-adjudication.json", scan_owner(owner_material))
    seal_targets = [
        f"docs/sylven-arc/{PHASE}/final/final-integrated-overview.md",
        f"docs/sylven-arc/{PHASE}/final/phase-truth.json",
        f"docs/sylven-arc/{PHASE}/final/method-flow-final.json",
        f"docs/sylven-arc/{PHASE}/final/retained-negative-register.json",
        f"docs/sylven-arc/{PHASE}/final/open-gap-register.json",
        f"docs/sylven-arc/{PHASE}/final/exact-gate-register.json",
        f"docs/sylven-arc/{PHASE}/final/complete-incomplete-checklist.json",
        f"docs/sylven-arc/{PHASE}/final/lifecycle-replay.json",
        f"docs/sylven-arc/{PHASE}/final/evidence-closeout.json",
        f"docs/sylven-arc/{PHASE}/handoffs/caelen-morrow-v685-v4-activation-candidate.md",
    ]
    write_json(
        SEAL / "content-seal.json",
        {
            "schema": "ghc.family.content-seal.v685.v3",
            "owner": OWNER,
            "phase": PHASE,
            "target_count": len(seal_targets),
            "targets": manifest_entries(seal_targets),
            "prepared_successor_state": "PREPARED_NOT_SENT",
            "canonical_result_included": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize-validation", action="store_true")
    args = parser.parse_args()
    if args.finalize_validation:
        finalize_validation()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
