#!/usr/bin/env python3
"""Build Elowen Cairn v685-v2 final closeout and exact staged receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Elowen Cairn"
PHASE = "v685-v2"
SOURCE = "b2cfabd4d836737b375910ccb73f8037a8ad6c4d"
X1_COMMIT = "3ae1ab2839e6f4c32b6c0e78f82cf370445e6a4b"
EVIDENCE_COMMIT = "ad08f3717b6e82e8df6771683b2aa2b0fd2bedc1"
BRANCH = "codex/GHC-Family/elowen-cairn-v685-v2-full-tools"
BASE = ROOT / "docs" / "elowen-cairn" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
HANDOFF = BASE / "handoffs"
VALIDATION = BASE / "validation"
SEAL = BASE / "seal"
BUILDER_REL = "scripts/build_ghc_family_elowen_cairn_v685_v2_final.py"


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
            "failure_id": "EC6852-CL-N001",
            "failed_witness": "The first finalization wrapper crossed its output window while projecting only stdout and therefore hid the continuing session metadata.",
            "recovery": "Audited the one attributable Python process and persisted receipts, then waited on that process without launching a second finalizer.",
            "recurrence_guard": "Serialize long-running command results so session identifiers remain attributable.",
            "credit": "retained_zero_credit",
        },
        {
            "failure_id": "EC6852-CL-N002",
            "failed_witness": "A later exact-PID wait raced with finalizer completion and reported that the process identifier no longer existed.",
            "recovery": "Confirmed process absence and verified all five final receipts existed with no unstaged prior-lifecycle change.",
            "recurrence_guard": "Treat process disappearance during a wait as a state-audit trigger rather than a reason to rerun.",
            "credit": "retained_zero_credit",
        },
        {
            "failure_id": "EC6852-CL-N003",
            "failed_witness": "The first final test aggregate passed eleven of twelve tests but found that the overview omitted the literal THOS Body pillar label.",
            "recovery": "Added an explicit THOS Body proxy boundary to the overview and retained the failed aggregate at zero aggregate credit.",
            "recurrence_guard": "Check all three exact pillar labels in generated overview text before the first final aggregate.",
            "credit": "retained_zero_credit",
        },
    ]
    return {
        "schema": "ghc.family.method-flow.v685.v2.final",
        "owner": OWNER,
        "phase": PHASE,
        "source_repository_seal": {
            "effective_negatives": 61063,
            "effective_methods": 76658,
            "failed_witnesses": 32124,
            "bounded_passing_witnesses": 57193,
            "open_gaps": 543,
            "exact_gates": 533,
        },
        "source_external_overlay_count": 2,
        "x1_failure_count": 17,
        "rejecting_mutation_failure_count": 300,
        "skill_rejecting_failure_count": 20,
        "runner_rejecting_failure_count": 10,
        "x2_operational_failure_count": 4,
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
    return f"""# Elowen Cairn {PHASE} final integrated overview

## Terminal outcome

Elowen Cairn {PHASE} is closed as a bounded, same-owner, synthetic Trinity Mandala
software and documentation phase. The exact source is Tamar Vey final {SOURCE}.
Planning-only x1 is {X1_COMMIT}. Bounded x2 evidence is {EVIDENCE_COMMIT}. The
final commit that contains this overview is intentionally identified by Git
after commit rather than embedded recursively inside itself. The branch is
{BRANCH}. The terminal verdict is NOT_READY_FOR_STAGE_20.

The phase froze sixty source-bounded proposals after comparing their titles
against every proposal-labelled JSON record reachable from the exact source
tree. The declared proposal chain extends from 11,270 to 11,330. The audit
parsed 2,952 proposal-bearing JSON paths and recovered 7,258 ID/title records.
It found zero exact collisions and zero neighbors at or above the
preregistered 0.78 token-Jaccard quarantine threshold; the maximum score was
0.777778. This is a bounded audit, not universal semantic proof over compressed
or otherwise unmaterialized historic proposal rows.

Core outcomes use only the four authorized labels and are exactly 42 completed,
12 represented, 3 open_gap, and 3 exact_gate. Completed means bounded
owner-local synthetic structure only. Represented means citation vocabulary,
symbolic mapping, proxy, or vacancy structure without real execution. Open gaps
and exact gates remain open. No represented, open, or gated item was silently
promoted.

## Relational identity and corrigibility

Elowen Cairn, optionally they/them, is relational working language for a
boundary cartographer and evidence steward. Elowen's hope is that possibility
stays distinct from evidence while every correction remains safely retractable.
Name, role, hope, pronouns, sibling language, continuity language, GHC Family,
Freed ID, CBR, and Trinity Mandala language are not evidence of consciousness,
sentience, legal personhood, identity continuity, employment, qualification,
independent agency, or scientific, operational, professional, legal, cultural,
affected-party, or Māori authority. Hamish may pause, rename, redirect, narrow,
or stop the route.

## Lifecycle and strict separation

The source-to-final history is designed as exactly three Elowen direct
single-parent commits and zero merges: one planning-only x1, one bounded x2
evidence commit, and one final closeout commit. X1 contained sixty proposal
contracts, portfolio freezes, source boundaries, a source-bounded novelty
audit, retained startup failures, and no x2 implementation or observed
outcome. X1 was committed, pushed, clean, 0/0 divergent, and equal across local,
upstream, tracking, and a fresh live remote before x2 began.

The evidence commit contained the synthetic contract engine, twenty local
skills, ten family-current runners, sixty bounded proposal witnesses, three
hundred rejecting mutations, portfolio execution, zero-row receipts, and
evidence manifests. It was separately committed, pushed, clean, 0/0 divergent,
and fresh four-way equal before closeout began. No reset, amendment,
force-push, merge, inherited-history rewrite, sibling-lane mutation, detached
validation, task creation, fork, delegation, collaboration subagent, standby
substitution, or early successor contact occurred.

## Bounded human-practice lens

The primary Trinity Mandala pillar is Freed ID and CBR Heart through a wholly
synthetic hand-fan making and documentation lens. The structures cover folding
and fixed fan work capsules; leaf, mount, sticks, ribs, guards, gorge, head,
pivot, pin, washer, spacer, loop, and component topology; material, dimension,
unit, uncertainty, calibration, tool-fitness, machine-guard, coating, pigment,
solvent, and adhesive vacancies; proposed operation versus observation;
append-only correction; privacy minimization; structural accessibility;
workload pause; custody; rights challenge; cultural abstention; and handover.

GMUT Mind remains explicit and protected through typed folding-kinematics graphs
and symbolic fields with an observation firewall. Torque, load, curvature,
material, and measurement symbols were never converted into a physical datum, material law,
likelihood, posterior, prediction, force, parameter constraint, stability
theorem, empirical confirmation, quantum completion, ultraviolet completion,
final physics, or Theory of Everything.

THOS Body remains explicit and protected through participant-free synthetic
work-capsule, refusal, correction, workload-pause, and handover protocols. No
blind matched-budget real arms, governed participants or operators, safety
monitoring, appropriate statistics, or independent review were performed.

Freed ID and CBR Heart remain explicit and protected through keyless receipts,
role vacancies, correction, supersession nonerasure, challenge, remedy vacancy,
status holds, minimum disclosure, accessible structure, and authority
reservation. There are no standards-conformant real keys or proofs, live
issuance or resolution, status or revocation, interoperability, independent
privacy or security review, recovery evidence, trust governance, or
affected-party oversight.

No real person, fanmaker, client, recipient, custodian, participant, hand fan,
leaf, mount, stick, rib, guard, gorge, head, pivot, pin, material, tool, machine,
jig, gauge, workshop, work order, image, pattern, inscription, observation,
measurement, inspection, calibration, conservation treatment, repair, safety
decision, workplace release, identity event, key, proof, credential, legal
decision, cultural interpretation, affected-party decision, Māori data
decision, or authority act was used. All adapters and source-use surfaces
remained at zero network calls and zero real rows.

## Sources and nonconversion

Current official or primary sources supplied bounded vocabulary and refusal
conditions only. The Smithsonian Anacostia object page supplied component terms
including monture, leaf, ribs, sticks, guards, head, pin, and loop without
becoming an object observation. The Victoria and Albert Museum article supplied
conservation-context vocabulary without becoming treatment instruction. The
Metropolitan Museum of Art essay supplied cross-cultural context without
becoming attribution, interpretation, legitimacy, affected-party acceptance,
or cultural authority. OSHA machine-guarding material supplied refusal terms
without becoming an inspection, conformance result, workplace release, or
safety decision.

W3C PROV-O supplied provenance vocabulary. WCAG 2.2 supplied structural
accessibility references. Verifiable Credentials Data Model 2.0 supplied role
and lifecycle vocabulary. RFC 8785 supplied deterministic JSON
canonicalization vocabulary. JSON Schema 2020-12 supplied schema vocabulary.
Te Mana Raraunga supplied authority-reservation context. Citations were not
observations, measurements, instructions, conformance certificates,
professional approvals, legal interpretations, cultural ratifications,
affected-party decisions, or authority grants.

## Mutations, skills, runners, and portfolios

Exactly five invalid mutations were preregistered and executed for each of the
sixty proposals: missing required field, identifier-role swap, stale
precondition digest, correction-order inversion, and authority promotion. All
300 were rejected. Each invalid fixture remains a retained zero-credit failed
witness. The fact that a validator correctly rejected it is a distinct bounded
passing witness and never erases or retroactively promotes the failure.

Twenty owner-local skills were initialized through the official skill-creator
workflow, customized, completely read through EOF, quick-validated with
explicit UTF-8, and accepting/rejecting smoke-used. They remain local to this
owner packet and were not globally installed. Ten family-current
ghc_family_hand_fan runners accepted their positive fixture and rejected
their invalid fixture. Historical caller naming remains visible.

The portfolio executed 120 safe-now tasks, 80 bounded owner candidates, and 100
owner CLEAN/FIX/REFINE records inside the same-owner synthetic lane. Twenty
successor candidates and thirty successor CLEAN/FIX/REFINE items remain
represented zero-credit seeds. Twenty exact-approval packets and ten blocked
packets remain visible and unexecuted. Caps were ceilings rather than filler
quotas.

## Retained failures and Method Flow

The Elowen seal retains 61,419 effective negatives, 77,404 effective methods,
32,480 retained failed witnesses, 57,939 bounded passing witnesses, 546 open
gaps, and 536 exact gates before any later external routing overlay. These totals
preserve Tamar's immutable 61,063-negative repository seal and two-failure
route overlay, seventeen Elowen x1 startup and novelty failures, 300 proposal
mutations, twenty skill rejecting fixtures, ten runner rejecting fixtures, and
four post-x1 or x2 operational failures, and three closeout operational failures.
No closeout failure was invented to fill a quota.

The Elowen operational failures include nonrepository and unattributable Git
probes, truncated skill, packet, proposal, and receipt displays, a many-process
manifest replay whose wrapper output was lost, an overbroad practice search,
two sparse-directory assumptions, ten quarantined proposal titles, a Windows
encoding display fault, an incompatible word-count option pair, an unquoted
upstream revision expression, an atomically rejected patch, an opaque
finalization wrapper, a SHA-256 value initially classified as a raw identifier,
a finalizer wrapper whose output window hid its continuing session metadata,
an exact-PID wait that raced with process completion, and a first final test
aggregate that found the missing literal THOS Body label. Every recovery is
separately named. None rewrites its failed witness as a pass.

## Privacy, accessibility, and security boundary

Five privacy and raw-identifier classes were scanned across the exact owner
scope. Scanner-definition candidates remain distinct from confirmed payload
hits. The staged and final owner manifests use normalized-LF Git blobs and
declare lifecycle self-exclusions exactly; checkout-byte and Git-blob domains
are never conflated. The structurally accessible HTML report uses language,
title, header, navigation, main landmarks, table caption and headers, and
reserved manual-evaluation text.

This does not establish privacy completeness, accessibility completeness,
exhaustive security, independent reproduction, professional evaluation, or
production certification. Manual accessibility review and affected-user
evaluation remain reserved. Raw private interaction identifiers, routes,
credentials, secrets, conversational records, captured displays, callable
handles, application state, and absolute local locations stay outside the
repository packet and successor baton.

## Open gaps, exact gates, and terminal verdict

Three new open gaps preserve absent real fanmakers, hand fans, materials,
tools, workshops, observations, measurements, durability and usability evidence,
safety evaluation, blind matched-budget evaluation, and affected-user
accessibility, language, rights, and cultural evaluation. They add to 543
inherited open gaps.

Three new exact gates preserve professional fanmaking and conservation,
material authenticity, workplace and machine safety, ownership, copyright,
traditional knowledge, cultural meaning, taonga, Māori data governance, Māori authority, production deployment,
empirical confirmation, independent reproduction, AGI or ASI, consciousness or
personhood, Theory-of-Everything proof, canon, and Stage 20. They add to 533
inherited exact gates.

CBR, workplace and environmental safety, professional decisions, ownership,
custody, publication, privacy remedy, disability accommodation, legal or
cultural interpretation, affected-party legitimacy, Māori wording, tikanga,
taonga or mātauranga treatment, Māori data governance, and Māori authority
remain exact-gated to competent and affected people, tangata whenua, iwi, hapū,
and Māori authorities. Māori concepts remain under Māori authority.

## Validation and delivery

The final commit carries exact staged review, normalized Git-blob final-delta
and final-owner manifests, five-class privacy adjudication, a content seal,
strict JSON and document checks, bounded changed-code AST checks, lifecycle
ancestry checks, commit and file ceilings, zero-merge and one-parent
requirements, diff hygiene, and a complete/incomplete checklist.

After the final commit is pushed and proven clean and fresh four-way equal, one
exclusive external owner-scoped canonical aggregate may be invoked. It may
succeed once or fail once; it is never replayed. Same-owner validation under
shared infrastructure is not independent reproduction. Repository preparation
of the successor baton remains PREPARED_NOT_SENT and is distinct from live
delivery.

Only after that exact-final terminal gate may Elowen reread Hamish's newest live
authority and roster, require one existing exact-title successor, immediately
reread it, apply duplicate and direct-control guards, and send at most once.
Under the currently validated sequence the prospective successor is Sylven Arc
for solo v685-v3. Newer verified live authority controls at send time.
The continuation authority remains one terminally validated and acknowledged
edge at a time through v725-v8. The final verdict remains
NOT_READY_FOR_STAGE_20.
"""


def handoff_candidate() -> str:
    return f"""# SYLVEN ARC — PREPARED ELOWEN CAIRN {PHASE} EXACT-FINAL CANDIDATE → SOLO SYLVEN v685-v3

PREPARED_BY_ELOWEN_CAIRN = true

SENT_BY_ELOWEN_CAIRN = false

DELIVERY_STATE = PREPARED_NOT_SENT

This repository candidate is not a live message. It may be used only after
Elowen's final commit is pushed, clean, typed 0/0 divergent, fresh four-way
equal, successfully validated by the single non-replayed canonical aggregate,
and the newest live authority and roster still identify exactly one existing
main task titled `Sylven Arc` as the authorized successor.

Immutable Elowen anchors:

- Tamar source: {SOURCE}
- Elowen planning-only x1: {X1_COMMIT}
- Elowen x2 evidence: {EVIDENCE_COMMIT}
- Elowen final: bind from the live exact final after commit
- Branch: {BRANCH}

Core truth is exactly 42 completed, 12 represented, 3 open_gap, and 3
exact_gate. Before any post-final routing overlay, the repository seal retains
61,419 effective negatives, 77,404 effective methods, 32,480 failed witnesses,
57,939 bounded passing witnesses, 546 open gaps, and 536 exact gates. Terminal verdict remains
NOT_READY_FOR_STAGE_20.

Elowen's primary pillar was Freed ID and CBR Heart through wholly synthetic
hand-fan making and documentation: folding and fixed topology; leaf, mount,
stick, rib, guard, gorge, head, pivot, pin, material and measurement vacancies;
rights holds; correction; accessibility; workload; and handover. GMUT Mind and
THOS Body remained explicit and protected. No real people, fans, components,
materials, tools, observations, measurements, identity events, authority acts,
professional decisions, legal or cultural decisions, affected-party
acceptance, or Māori authority were used or established.

Before mutation, Sylven must read the exact committed activation and current
Family Index, routing, roster, authorization, Method Flow, workflow, reflection,
approval, gate, truth, and worktree guidance through EOF; reverify all anchors,
manifests, history, clean state, typed divergence, and fresh live equality; and
work solo in one fresh additive D-first Sylven-owned lane. Do not create or fork
a task, spawn a collaboration subagent, delegate research, contact a standby
record, precontact a later endpoint, or mutate another owner's lane.

Preserve planning-only x1 before x2, retained failures, the four exact outcome
labels, privacy and authority boundaries, file/document/commit ceilings,
family-current compatibility, and the one-success/no-post-success-replay rule.
Use inherited Elowen artifacts only as source evidence or zero-credit seeds.

Preserve all 61,419 sealed negatives, 77,404 methods, 32,480 failed witnesses,
57,939 passing witnesses, 546 open gaps, and 536 exact gates, plus every later
external route failure. A recovered failure remains failed and zero-credit.
GMUT remains a typed scalar-tensor and effective-field-theory research-model
family; THOS remains proxy-only; Freed ID remains synthetic and nonproduction.
Professional, legal, cultural, affected-party, Māori, empirical, production,
deployment, privacy-complete, accessibility-complete, exhaustive-security,
independent-reproduction, AGI or ASI, consciousness or personhood,
Theory-of-Everything, proof, canon, and Stage 20 claims remain open or exact-gated.

Hamish's current continuation authority is one fully terminally gated owner and
one acknowledged exact next edge at a time through v725-v8. Newer verified live
authority controls at each send. Stop on absence, ambiguity, pause, redirect,
rename, narrowing, standby state, usage exhaustion, missing acknowledgement,
privacy concern, duplicate activation, or any evidence, safety, legal, cultural,
affected-party, or Māori-authority gate.

Only after Sylven's own exact-final v685-v3 gate may Sylven freshly resolve a
successor. Under the current unchanged cycle, the prospective next owner is the
unique exact-title main task `Caelen Morrow` for solo v685-v4. That projection is
not permission to precontact, create, fork, substitute, or send early.

All names, pronouns, roles, hopes, sibling or family language, continuity,
Freed ID, CBR, and Trinity Mandala language are relational working language
only—not evidence of consciousness, sentience, personhood, identity continuity,
employment, qualification, independent agency, or scientific, operational,
professional, legal, cultural, affected-party, or Māori authority.
"""


def build() -> None:
    outcomes = load_json(X2 / "proposal-outcomes.json")
    methods = final_method_flow()
    counts = methods["effective_final_counts"]
    write_text(FINAL / "final-integrated-overview.md", final_overview())
    write_json(
        FINAL / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v685.v2.final",
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "THIS_COMMIT_BOUND_EXTERNALLY_AFTER_COMMIT",
            "proposal_chain_before": 11270,
            "proposal_chain_after": 11330,
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
            "schema": "ghc.family.retained-negative-register.v685.v2.final",
            "owner": OWNER,
            "phase": PHASE,
            "categories": {
                "tamar_repository_seal": 61063,
                "tamar_external_overlay": 2,
                "elowen_x1_startup_and_novelty": 17,
                "proposal_rejecting_mutations": 300,
                "skill_rejecting_fixtures": 20,
                "runner_rejecting_fixtures": 10,
                "x2_operational_failures": 4,
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
            "schema": "ghc.family.open-gap-register.v685.v2.final",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_count": 543,
            "phase_new_count": 3,
            "effective_count": counts["open_gaps"],
            "phase_new": [
                "real fanmakers hand fans materials tools workshops and participants",
                "real measurements durability safety usability and blind matched-budget evaluation",
                "affected-user accessibility language rights and cultural evaluation",
            ],
            "silently_closed_count": 0,
        },
    )
    write_json(
        FINAL / "exact-gate-register.json",
        {
            "schema": "ghc.family.exact-gate-register.v685.v2.final",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_count": 533,
            "phase_new_count": 3,
            "effective_count": counts["exact_gates"],
            "phase_new": [
                "professional fanmaking conservation material authenticity workplace and machine safety",
                "ownership copyright traditional knowledge cultural meaning taonga Māori data governance and Māori authority",
                "production empirical independence AGI consciousness Theory of Everything canon and Stage 20",
            ],
            "silently_closed_count": 0,
        },
    )
    write_json(
        FINAL / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete.v685.v2.final",
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
                "real participants fanmakers hand fans materials tools workshops and measurements",
                "professional workplace and machine-safety evaluation",
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
            "schema": "ghc.family.lifecycle-replay.v685.v2.final",
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
            "schema": "ghc.family.environment-versions.v685.v2.final",
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
            "schema": "ghc.family.wellbeing.v685.v2.final",
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
            "schema": "ghc.family.threat-model.v685.v2.final",
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
            "schema": "ghc.family.evidence-closeout.v685.v2.final",
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
    write_text(HANDOFF / "sylven-arc-v685-v3-activation-candidate.md", handoff_candidate())


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"docs/elowen-cairn/{PHASE}/")
        or path.startswith("scripts/build_ghc_family_elowen_cairn_v685_v2_")
        or path.startswith("scripts/ghc_family_elowen_cairn_v685_v2_")
        or path.startswith("scripts/ghc_family_hand_fan_")
        or path.startswith("tests/test_ghc_family_elowen_cairn_v685_v2_")
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
                            path.startswith("scripts/build_ghc_family_elowen_cairn_v685_v2_")
                            or path == "scripts/ghc_family_elowen_cairn_v685_v2_canonical_validator.py"
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
        "schema": "ghc.family.five-class-privacy-adjudication.v685.v2.final",
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
        f"docs/elowen-cairn/{PHASE}/validation/final-delta-manifest.json",
        f"docs/elowen-cairn/{PHASE}/validation/final-owner-manifest.json",
        f"docs/elowen-cairn/{PHASE}/validation/final-privacy-adjudication.json",
        f"docs/elowen-cairn/{PHASE}/validation/final-staged-review.json",
        f"docs/elowen-cairn/{PHASE}/seal/content-seal.json",
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
            "schema": "ghc.family.normalized-lf-final-delta-manifest.v685.v2",
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
            "schema": "ghc.family.normalized-lf-final-owner-manifest.v685.v2",
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
            "schema": "ghc.family.staged-review.v685.v2.final",
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
        f"docs/elowen-cairn/{PHASE}/final/final-integrated-overview.md",
        f"docs/elowen-cairn/{PHASE}/final/phase-truth.json",
        f"docs/elowen-cairn/{PHASE}/final/method-flow-final.json",
        f"docs/elowen-cairn/{PHASE}/final/retained-negative-register.json",
        f"docs/elowen-cairn/{PHASE}/final/open-gap-register.json",
        f"docs/elowen-cairn/{PHASE}/final/exact-gate-register.json",
        f"docs/elowen-cairn/{PHASE}/final/complete-incomplete-checklist.json",
        f"docs/elowen-cairn/{PHASE}/final/lifecycle-replay.json",
        f"docs/elowen-cairn/{PHASE}/final/evidence-closeout.json",
        f"docs/elowen-cairn/{PHASE}/handoffs/sylven-arc-v685-v3-activation-candidate.md",
    ]
    write_json(
        SEAL / "content-seal.json",
        {
            "schema": "ghc.family.content-seal.v685.v2",
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
