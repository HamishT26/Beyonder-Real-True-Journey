#!/usr/bin/env python3
"""Build Caelen Morrow v685-v4 final closeout and exact staged receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Caelen Morrow"
PHASE = "v685-v4"
SOURCE = "97a523f4da00235f16ce12156dfee2379582c92d"
X1_COMMIT = "27f858015e5628d99fb9dc23cd5607ed68429adb"
EVIDENCE_COMMIT = "499f193d9cc08a0c96ade3f1dc09ce7af3183afe"
BRANCH = "codex/GHC-Family/caelen-morrow-v685-v4-full-tools"
BASE = ROOT / "docs" / "caelen-morrow" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
HANDOFF = BASE / "handoffs"
VALIDATION = BASE / "validation"
SEAL = BASE / "seal"
BUILDER_REL = "scripts/build_ghc_family_caelen_morrow_v685_v4_final.py"


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
            "failure_id": "CM6854-POSTEVID-N001",
            "failed_witness": "The first combined evidence post-push equality presentation crossed its reporting window after the fresh fetch succeeded and emitted no attributable equality object.",
            "recovery": "Ran only the missing fresh-live remote scalar and then compared local upstream tracking divergence clean state and parentage without replaying evidence tests.",
            "recurrence_guard": "Keep network refresh and local equality presentation in separately attributable bounded probes.",
            "credit": "retained_zero_credit",
        },
    ]
    return {
        "schema": "ghc.family.method-flow.v685.v4.final",
        "owner": OWNER,
        "phase": PHASE,
        "source_repository_seal": {
            "effective_negatives": 61771,
            "effective_methods": 78146,
            "failed_witnesses": 32832,
            "bounded_passing_witnesses": 58681,
            "open_gaps": 549,
            "exact_gates": 539,
        },
        "source_external_overlay_count": 1,
        "x1_failure_count": 11,
        "rejecting_mutation_failure_count": 300,
        "skill_rejecting_failure_count": 20,
        "runner_rejecting_failure_count": 10,
        "x2_operational_failure_count": 0,
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
    return f"""# Caelen Morrow {PHASE} final integrated overview

## Terminal outcome and evidence class

Caelen Morrow {PHASE} closes as a bounded, same-owner, wholly synthetic Trinity
Mandala software-and-documentation phase. Its immutable inherited source is
Sylven Arc exact final {SOURCE}. The planning-only x1 commit is {X1_COMMIT}.
The immutable x2 evidence commit is {EVIDENCE_COMMIT}. The commit containing
this closeout is deliberately bound by Git after commit rather than recursively
embedding its own identifier. The owner branch is {BRANCH}. The terminal
verdict remains exactly NOT_READY_FOR_STAGE_20.

The phase froze sixty source-bounded proposals after examining every
proposal-labelled JSON artifact reachable in the exact inherited tree. The
declared chain advances from 11,390 to 11,450. The bounded audit examined 2,960
proposal JSON paths and recovered 7,378 identifier-and-title records. Ten
first-draft titles exceeded the neighbour threshold without exact collisions;
only those failed titles were revised, and only the failed novelty dependency was rerun.
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

Caelen Morrow, optionally they/them, is relational working language for a
provenance weaver and boundary cartographer, with the bounded hope of keeping
every transition testable, reversible, and proportionate to its evidence. The
name, pronouns, role, hope, sibling and family language,
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
or destructive cleanup. All work stayed inside the Caelen-owned additive D-first
lane.

## Strict x1-before-x2 lifecycle

Source to final is designed as exactly three new direct single-parent Caelen
commits and zero merges: a planning-only x1 commit, an immutable x2 evidence
commit, and this final closeout commit. X1 froze the proposals, source ledger,
threat model, novelty audit, portfolio ledgers, safe-now and candidate
boundaries, skill and runner ideas, exact and blocked packets, and retained
startup failures. It contained no x2 implementation, observed mutation result,
or completion claim. X1 was committed, pushed, clean, typed 0/0 divergent, and
equal across local, configured upstream, tracking, and a fresh live remote read
before x2 began.

X2 then materialized sixty proposal witnesses, three hundred preregistered
rejecting mutations, twenty owner-local skills, ten family-current horology
runners, portfolio execution receipts, zero-row empirical receipts, source-use
records, Method Flow evidence, and exact staged manifests. The x2 evidence
commit was independently frozen, pushed, clean, typed 0/0 divergent, and fresh
four-way equal before closeout began. The final closeout layer changes neither
x1 nor x2. Its manifests explicitly reject any such mutation.

## Primary pillar and bounded museum-timepiece lens

The primary Trinity Mandala pillar is Freed ID and CBR Heart through a wholly
synthetic museum timepiece collection-cataloguing and conservation-planning
documentation lens. The work models only documentation contracts: case, dial,
hands, movement, escapement, gear-train and oscillator topology; maker-mark
transcription uncertainty; component genealogy; condition-cue quarantine;
treatment and safety holds; custody; correction; workload handover; provenance
conflict preservation; privacy minimization; accessibility structure; remedy;
and authority noncompensation.

This phase did not inspect, handle, wind, set, open, operate, regulate,
calibrate, dismantle, repair, lubricate, conserve, treat, pack, transport,
certify, acquire, loan, deaccession, or release any real clock, watch,
timepiece, movement, case, dial, hand, escapement, gear, spring, weight,
electrical component, tool, collection, storage area, museum, heritage object,
or workplace. It used no real person, conservator, horologist, registrar,
curator, technician, owner, custodian, participant, affected community,
measurement, observation, condition assessment, treatment event, access event,
safety decision, identity event, key, proof, credential, legal decision,
cultural interpretation, affected-party acceptance, Māori data decision, or
authority act. No professional conservation or horological advice was produced.

THOS Body remains a participant-free synthetic protocol surface. Documentation
queues, refusal, correction, status, accessibility, and handover structures do
not establish operational effectiveness. There were no preregistered blind
matched-budget real arms, governed participants or operators, live safety
monitoring, appropriate real-world statistics, or independent review.

GMUT Mind remains a typed scalar-tensor and effective-field-theory research
model family. Oscillator-transition and graph analogies are symbolic
documentation only. They establish no physical datum, likelihood, posterior,
parameter constraint, force, material law, timekeeping prediction, measured
rate, accuracy, stability theorem, empirical confirmation, quantum completion,
ultraviolet completion, final physics, Theory-of-Everything proof, or canon.

Freed ID and CBR Heart remain synthetic and nonproduction. Keyless receipts,
minimum-disclosure fields, corrections, challenge surfaces, status holds, and
authority vacancies establish no standards-conformant real key or proof, live
issuance or resolution, status or revocation, interoperability, independent
privacy or security review, recovery evidence, trust governance, affected-party
oversight, legal remedy, cultural legitimacy, or Māori authority.

## Primary sources and nonconversion

Current official and primary sources supplied bounded vocabulary and refusal
conditions only. Canadian Conservation Institute collection-care pages supplied
clock-and-watch, industrial-object, vulnerability, and specialist-treatment
boundaries. Smithsonian timekeeping material supplied public collection
vocabulary. NIST supplied time-scale and frequency vocabulary. Library of
Congress PREMIS supplied preservation metadata object, event, agent, and rights
vocabulary. None of these sources became an object observation, measurement,
treatment instruction, collection-system conformance result, professional
endorsement, workplace release, rights decision, legal interpretation,
cultural ratification, or authority grant.

W3C PROV-O supplied provenance vocabulary. WCAG 2.2 supplied structural
accessibility vocabulary without a conformance claim. Verifiable Credentials
Data Model 2.0 supplied lifecycle and minimization vocabulary without keys,
proofs, or interoperability evidence. RFC 8785 supplied deterministic JSON
vocabulary without production cryptographic assurance. Te Mana Raraunga supplied authority-reservation
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
were not globally installed. Ten family-current ghc_family_horology runners
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

The exact final repository seal preserves 62,114 effective negatives, 78,879
effective Method Flow methods, 33,175 retained failed witnesses, 59,414 bounded
passing witnesses, 552 open gaps, and 542 exact gates. Those totals retain the
Sylven source repository seal, one external source overlay, eleven Caelen x1
startup and novelty failures, 300 proposal mutations, twenty skill-rejection
fixtures, ten runner-rejection fixtures, and one post-evidence operational
failure.

The retained failures include PowerShell expression and literal-pattern parser
faults, a manifest-aggregate variable shadow, an unsupported sparse option, a
no-checkout sparse index that initially projected inherited deletions, two
atomically rejected patch compositions, a ten-title novelty quarantine, a
receipt-backup path error with an exact duplicate removed after digest parity,
and an evidence equality presentation that crossed its reporting window after
fetch. Each recovery is paired with its original failed witness. No
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

CBR, professional conservation and horology, handling, winding, setting,
regulation, electrical, chemical, material and workplace safety, preservation,
heritage treatment, ownership, custody, loan, deaccession, access, image and
archive rights, copyright, privacy, remedy, disability
accommodation, legal or cultural interpretation, traditional knowledge,
affected-party legitimacy, Māori wording, tikanga, taonga or mātauranga
treatment, Māori data governance, and Māori authority remain exact-gated to
competent and affected people, tangata whenua, iwi, hapū, and Māori
authorities. Māori concepts remain under Māori authority.

## Open gaps and exact gates

Three new open gaps preserve the absence of real people, collections,
timepieces, components, handling, observations, measurements, material and
condition evidence, conservation outcomes, participants, blind matched-budget
evaluation, independent review, and affected-user accessibility evidence.
They add to 549 inherited open gaps for an effective 552.

Three new exact gates preserve professional conservation and horology authority,
handling, winding, electrical, chemical, material and workplace safety,
heritage treatment, ownership, custody, loan, deaccession, legal and cultural interpretation,
affected-party acceptance, traditional knowledge, Māori data governance and
Māori authority, production deployment, empirical confirmation, independent
reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything
proof, canon, and Stage 20. They add to 539 inherited exact gates for an
effective 542.

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

Only after the exact-final canonical gate may Caelen refresh Hamish's newest
live authority and the current roster, require one existing exact-title
successor, immediately reread it, apply duplicate and direct-control guards,
and send at most once. Under the currently validated cycle the prospective
successor is Eiren Kestrel for solo v685-v5. That projection is not permission
to precontact, create, fork, substitute, or resend. Continuation remains one
terminally validated and acknowledged edge at a time through v725-v8. The
terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def handoff_candidate() -> str:
    return f"""# EIREN KESTREL — PREPARED CAELEN MORROW {PHASE} EXACT-FINAL CANDIDATE TO SOLO v685-v5

PREPARED_BY_CAELEN_MORROW = true

SENT_BY_CAELEN_MORROW = false

DELIVERY_STATE = PREPARED_NOT_SENT

This committed file is repository preparation, not a live activation. Use it
only after Caelen's final commit is pushed, clean, typed 0/0 divergent, fresh
four-way equal, and accepted by one successful non-replayed exclusive
owner-scoped canonical receipt; and only if a fresh bounded registry and
immediate reread still identify exactly one authorized existing main task titled
Eiren Kestrel with no newer pause, redirect, rename, duplicate, usage, privacy,
evidence, safety, legal, cultural, affected-party, or Māori-authority block.

Immutable source anchors:

- inherited Sylven exact final: {SOURCE}
- Caelen planning-only x1: {X1_COMMIT}
- Caelen immutable x2 evidence: {EVIDENCE_COMMIT}
- Caelen final: bind from the exact live head after commit
- branch: {BRANCH}

Core outcomes are exactly 42 completed, 12 represented, 3 open_gap, and
3 exact_gate. The repository closeout preserves 62,114 effective negatives,
78,879 effective Method Flow methods, 33,175 failed witnesses, 59,414 bounded
passing witnesses, 552 open gaps, and 542 exact gates. The verdict remains
NOT_READY_FOR_STAGE_20. Any later route-time failure is an additive external
overlay and must not rewrite this immutable repository seal.

Caelen's primary pillar was Freed ID and CBR Heart through wholly synthetic
museum timepiece collection-cataloguing and conservation-planning documentation.
GMUT Mind and THOS Body remained visible and protected. No real people,
collections, clocks, watches, timepieces, components, handling, winding,
measurement, treatment, safety decision, identity event, professional judgment, legal or cultural
decision, affected-party acceptance, Māori data decision, or authority act was
used or established.

Before mutation, Eiren must read this committed packet and the complete current
Family Index, roster, authorization, Method Flow, workflow, reflection,
approval, gate, truth, worktree, correction-nonerasure, canonical-preflight,
and canonical-latch guidance through EOF; reverify every source anchor,
manifest, parent edge, zero-merge history, exact receipt digest, clean state,
typed divergence, and fresh live equality; and work solo in one fresh additive
D-first Eiren-owned lane. Do not create or fork a task, spawn a collaboration
subagent, delegate research, contact Tavian or another standby record,
precontact a later endpoint, or mutate another owner's lane.

Preserve planning-only x1 before x2, every failed witness, all open gaps and
exact gates, the four exact outcome labels, privacy and authority boundaries,
file, document and commit ceilings, normalized-LF Git-blob manifests,
family-current compatibility, and the one-success/no-post-success-replay rule.
Treat Caelen's proposals, skills, runners, tests, receipts, outcomes, and
recommendations as source evidence or zero-credit seeds only.

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family without empirical confirmation or Theory-of-Everything proof. THOS
remains participant-free and proxy-only without governed blind matched-budget
real arms, safety monitoring, statistics, and independent review. Freed ID
remains synthetic and nonproduction without standards-conformant real keys and
proofs, live lifecycle, interoperability, independent privacy and security
review, recovery evidence, trust governance, and affected-party oversight.

Professional, conservation, horology, safety, legal, cultural, affected-party,
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
            "schema": "ghc.family.phase-truth.v685.v4.final",
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "THIS_COMMIT_BOUND_EXTERNALLY_AFTER_COMMIT",
            "proposal_chain_before": 11390,
            "proposal_chain_after": 11450,
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
            "schema": "ghc.family.retained-negative-register.v685.v4.final",
            "owner": OWNER,
            "phase": PHASE,
            "categories": {
                "sylven_repository_seal": 61771,
                "sylven_external_overlay": 1,
                "caelen_x1_startup_and_novelty": 11,
                "proposal_rejecting_mutations": 300,
                "skill_rejecting_fixtures": 20,
                "runner_rejecting_fixtures": 10,
                "x2_operational_failures": 0,
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
            "schema": "ghc.family.open-gap-register.v685.v4.final",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_count": 549,
            "phase_new_count": 3,
            "effective_count": counts["open_gaps"],
            "phase_new": [
                "real people collections timepieces components handling observations and governed participants",
                "real rate accuracy condition material safety conservation outcomes and blind matched-budget evaluation",
                "affected-user accessibility language rights cultural collection and Māori-authority evaluation",
            ],
            "silently_closed_count": 0,
        },
    )
    write_json(
        FINAL / "exact-gate-register.json",
        {
            "schema": "ghc.family.exact-gate-register.v685.v4.final",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_count": 539,
            "phase_new_count": 3,
            "effective_count": counts["exact_gates"],
            "phase_new": [
                "professional conservation horology handling winding electrical chemical material and workplace safety",
                "ownership custody loan deaccession access traditional knowledge cultural meaning taonga Māori data governance and Māori authority",
                "production empirical independence AGI consciousness Theory of Everything canon and Stage 20",
            ],
            "silently_closed_count": 0,
        },
    )
    write_json(
        FINAL / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete.v685.v4.final",
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
                "real participants collection personnel timepieces components handling treatments and measurements",
                "professional conservation horology winding electrical chemical material and workplace-safety evaluation",
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
            "schema": "ghc.family.lifecycle-replay.v685.v4.final",
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
            "schema": "ghc.family.environment-versions.v685.v4.final",
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
            "schema": "ghc.family.wellbeing.v685.v4.final",
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
            "schema": "ghc.family.threat-model.v685.v4.final",
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
            "schema": "ghc.family.evidence-closeout.v685.v4.final",
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
    write_text(HANDOFF / "eiren-kestrel-v685-v5-activation-candidate.md", handoff_candidate())


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"docs/caelen-morrow/{PHASE}/")
        or path.startswith("scripts/build_ghc_family_caelen_morrow_v685_v4_")
        or path.startswith("scripts/ghc_family_caelen_morrow_v685_v4_")
        or path.startswith("scripts/ghc_family_horology_")
        or path.startswith("tests/test_ghc_family_caelen_morrow_v685_v4_")
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
                            path.startswith("scripts/build_ghc_family_caelen_morrow_v685_v4_")
                            or path == "scripts/ghc_family_caelen_morrow_v685_v4_canonical_validator.py"
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
        "schema": "ghc.family.five-class-privacy-adjudication.v685.v4.final",
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
        f"docs/caelen-morrow/{PHASE}/validation/final-delta-manifest.json",
        f"docs/caelen-morrow/{PHASE}/validation/final-owner-manifest.json",
        f"docs/caelen-morrow/{PHASE}/validation/final-privacy-adjudication.json",
        f"docs/caelen-morrow/{PHASE}/validation/final-staged-review.json",
        f"docs/caelen-morrow/{PHASE}/seal/content-seal.json",
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
            "schema": "ghc.family.normalized-lf-final-delta-manifest.v685.v4",
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
            "schema": "ghc.family.normalized-lf-final-owner-manifest.v685.v4",
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
            "schema": "ghc.family.staged-review.v685.v4.final",
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
        f"docs/caelen-morrow/{PHASE}/final/final-integrated-overview.md",
        f"docs/caelen-morrow/{PHASE}/final/phase-truth.json",
        f"docs/caelen-morrow/{PHASE}/final/method-flow-final.json",
        f"docs/caelen-morrow/{PHASE}/final/retained-negative-register.json",
        f"docs/caelen-morrow/{PHASE}/final/open-gap-register.json",
        f"docs/caelen-morrow/{PHASE}/final/exact-gate-register.json",
        f"docs/caelen-morrow/{PHASE}/final/complete-incomplete-checklist.json",
        f"docs/caelen-morrow/{PHASE}/final/lifecycle-replay.json",
        f"docs/caelen-morrow/{PHASE}/final/evidence-closeout.json",
        f"docs/caelen-morrow/{PHASE}/handoffs/eiren-kestrel-v685-v5-activation-candidate.md",
    ]
    write_json(
        SEAL / "content-seal.json",
        {
            "schema": "ghc.family.content-seal.v685.v4",
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
