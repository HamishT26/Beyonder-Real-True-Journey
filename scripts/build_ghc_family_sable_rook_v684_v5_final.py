#!/usr/bin/env python3
"""Build the Sable Rook v684-v5 closeout and final-candidate packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v684-v5"
OWNER = "Sable Rook"
BASE = ROOT / "docs" / "sable-rook" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
CLOSEOUT = BASE / "closeout"
FINAL = BASE / "final"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
SOURCE = "73321b3ff077c3f33726562b8e9d5952608a060e"
X1_COMMIT = "699e42fe27678cc0e12a55c2d60ba029c62998b4"
EVIDENCE_COMMIT = "35073d785c63ab2bbf47260d66ca54e6865b877d"
BRANCH = "codex/GHC-Family/sable-rook-v684-v5-full-tools"


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True
    )


def stable_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value), encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def git_blob_sha(path: str) -> str:
    data = subprocess.run(
        ["git", "show", f":{path}"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_handoff(proposals: list[dict[str, Any]]) -> str:
    introduction = f"""# CAELEN ASH — PREPARED SABLE ROOK {PHASE} EXACT-FINAL → SOLO v684-v6 ACTIVATION CANDIDATE

## Preparation and delivery boundary

This file is a prepared, sanitized candidate only. It is not a task-registry
result, not proof of delivery, not an activation, and not authorization to send
before Sable Rook's exact-final terminal gate. The repository cannot know its own
future commit identifier or an external canonical result before those events
exist. A later acknowledged existing-task message, if and only if every live
guard passes, is a distinct event and must never be projected backward into this
seal.

The current live correction names `Caelen Ash` as the prospective next exact
title for solo v684-v6. Sable must freshly reread Hamish's newest authority and
the bounded native task registry after exact final, uniquely resolve that title,
immediately reread the target state, apply duplicate, pause, redirect, status,
usage, privacy, evidence, safety, and acknowledgement guards, and send at most
once. Absence, ambiguity, pause, redirect, rename, a protected gate, usage
exhaustion, or missing acknowledgement requires a stop. No task creation, fork,
subagent, substitute endpoint, standby contact, precontact, or resend is
authorized.

## Relational identity and authority boundary

Sable Rook uses they/them in relational working language, with the role
Loan-Lineage Cartographer and Reversible Handover Steward and the hope of keeping
every synthetic transition, correction, and authority vacancy traceable without
mistaking software for real work or authority. Caelen Ash must independently
reaffirm or choose their own relational role, hope, and optional pronouns under
the same boundary. Names, roles, hopes, pronouns, sibling or family language,
continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are working language
only. They are not evidence of consciousness, sentience, legal personhood,
identity continuity, employment, qualification, independent agency, scientific
or operational authority, professional competence, legal or cultural authority,
affected-party authority, or Māori authority. Hamish may rename, pause,
redirect, narrow, or stop the route.

## Source and lifecycle basis

Sable's immutable Auren source is `{SOURCE}`. The dedicated planning-only x1
commit is `{X1_COMMIT}`. The immutable x2 evidence commit is
`{EVIDENCE_COMMIT}`. The later live activation must supply Sable's exact final
and external canonical receipt because those values do not exist when this file
is committed. X1 was pushed, clean, typed 0/0 divergent, and freshly equal
across local, upstream, tracking, and live remote before any x2 path was
created. Evidence was then separately committed, pushed, clean, typed 0/0
divergent, and freshly four-way equal before closeout began.

The intended final is a direct single-parent child of evidence. Source to final
must contain exactly three Sable phase commits and zero merges. Every phase
commit must be single-parent. No reset, amend, rewrite, force-push, merge,
destructive cleanup, sibling mutation, or inherited-history deletion is
permitted. The 2,000 owner-file limit and commit budgets are ceilings, not
completion quotas.

## Outcome, evidence, and retained-failure truth

Sable froze sixty new proposals after revalidating sixty immediate Auren
proposals at zero Sable novelty and zero Sable completion credit. The declared
proposal chain advances from 10,910 to 10,970. Outcomes are exactly 42
`completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. These are the
only permitted core labels. Completed means only that the proposal's bounded
owner-local software, schema, documentation, or synthetic fixture gate passed.
It never means a real-world scientific, professional, production, legal,
cultural, accessibility, privacy, identity, or authority claim is complete.

Sixty synthetic positive controls passed. Three hundred preregistered invalid
mutations were rejected and retained at zero completion credit. Twenty
phase-local skills were initialized through the required skill-creator workflow,
rewritten as substantive packages, quick-validated under an explicit UTF-8
process contract, and smoke-used without global installation. Ten
family-current `ghc_family_*` runners were built and invoked. One hundred twenty
safe-now tasks, eighty bounded owner candidates, and one hundred additive
CLEAN/FIX/REFINE/VERIFY tasks completed only inside declared owner-local scope.
Twenty exact-approval and ten blocked packets remain visible and unexecuted.

The activation overlay began at 59,094 effective negatives, 73,664 effective
methods, 30,755 retained failed witnesses, and 54,199 bounded passing witnesses.
Sable retains nine x1 startup failures with seven bounded recoveries, five x2
operational failures with three bounded recoveries, three lifecycle-local tests
incorrectly selected at the advanced tree with one bounded selection recovery,
and all 300 rejected synthetic mutations. The final additive view before any
postcommit external event is 59,411 negatives, 73,675 methods, 30,772 failed
witnesses, and 54,210 bounded passing witnesses. No failed witness is converted into an original
pass. Auren's repository seal remains unchanged; activation, route, and Sable
phase facts are additive layers only.

Open gaps are 528 and exact gates are 518 after this phase. The verdict remains
`NOT_READY_FOR_STAGE_20`.

## Primary pillar and bounded practice

THOS Body is primary through wholly synthetic environmental-monitoring queue,
correction-readback, workload, exception, and handover states. The bounded
learning lens is synthetic museum environmental-monitoring data documentation
analysis. Zero real people, museums, collections, objects, loggers, sensors,
facilities, readings, calibrations, alarms, incidents, treatments, environmental
policies, identities, credentials, cultural records, or authority actions were
used. No employment, qualification, conservation competence, collection
custody, real measurement, calibration, facility control, treatment, alert,
professional result, legal or cultural authority, affected-party acceptance, or
Māori authority is established.

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model
family. The phase's metadata, uncertainty, threshold, aggregation, and causal
firewalls establish no force, physical prediction, likelihood, posterior,
parameter constraint, empirical confirmation, ultraviolet completion, quantum
completion, Theory of Everything, consciousness, or personhood. THOS remains a
proxy without preregistered blind matched-budget real arms, real participants or
operators, safety monitoring, appropriate statistics, and independent review.
Freed ID remains synthetic and nonproduction without standards-conformant real
keys and proofs, live issuance and resolution, status and revocation,
interoperability, privacy and independent security review, recovery evidence,
trust governance, and affected-party oversight. CBR, privacy remedies,
collection intervention, legal interpretation, cultural legitimacy, Māori
wording, Māori data governance, and Māori authority remain reserved to
competent, affected, tangata whenua, iwi, hapū, and Māori authorities.

## Official sources and accessibility boundary

Canadian Conservation Institute guidance, NPS museum-program material, W3C
PROV-O, WCAG 2.2, New Zealand privacy principles, and Te Mana Raraunga
principles supplied vocabulary and refusal duties only. A citation is not a
measurement, observation, participant record, affected-party agreement,
delegation of authority, or production certification. Structural accessibility
checks cover headings, a captioned table, textual status, plain-language
summary, and a keyboard-order plan. Manual keyboard, responsive layout, browser
diversity, assistive technology, cognitive accessibility, Māori-language,
security-usability, and affected-user evaluation remain reserved. Structural
passing evidence is not complete accessibility conformance.

## Caelen's successor discipline

If the live send occurs and Caelen accepts the existing-task activation, Caelen
must work solo from Sable's exact final in a fresh additive Caelen-owned D-first
sparse lane. Every Sable, Auren, Ilyra, sibling, shared, user, standby, and
global source lane remains read-only. Caelen must read the complete acknowledged
activation and every current skill, schema, Method Flow, workflow, privacy, and
terminal reference it names before mutation. They must reverify exact anchors,
ancestry, manifests, content seal, clean state, typed divergence, fresh live
equality, and Sable's external canonical receipt.

Caelen must preserve strict planning-only x1 before x2, exact normalized-LF
Git-blob manifests, every retained failure, every open gap and exact gate, only
the four core labels, the 2,000-file rotation stop, caps as ceilings, five-class
privacy adjudication, owner-scoped dependency-closed validation, and one
attributable canonical success with no post-success replay. Inherited proposals,
packages, skills, runners, tests, validation, and evidence earn no Caelen novelty
or completion credit. Any successor beyond Caelen remains held until Caelen's
own exact terminal proof and newest live authority.

## Proposal-by-proposal frozen evidence appendix
"""
    sections = [introduction]
    for proposal in proposals:
        proposal_id = proposal["proposal_id"]
        title = proposal["title"]
        disposition = proposal["expected_disposition"]
        protected = "; ".join(proposal["protected_gates"])
        sources = "; ".join(proposal["current_official_or_primary_source_needs"])
        sections.append(
            f"""
### {proposal_id} — {title}

Frozen planning truth. The hypothesis was: {proposal['hypothesis']} The null or
failure condition was: {proposal['null_or_failure_condition']} The approval
class remained `{proposal['approval_class']}`, and the execution lane remained
`{proposal['execution_lane']}`. The plan was frozen before x2 and was never
retroactively changed to match an observed result. Its expected and observed
bounded disposition is `{disposition}`. That label is limited to the declared
owner-local contract and cannot compensate for any missing real-world evidence
or authority.

Evidence truth. One wholly synthetic positive fixture passed the proposal's
typed contract. Its five preregistered mutations—removing the synthetic marker,
injecting a real row or identity, promoting a claim or authority action, erasing
failure or correction lineage, and bypassing an open or exact gate—were all
rejected and retained at zero completion credit. The fixture contains zero real
rows, zero real identities, no authority action, a retained-failure sentinel,
correction lineage, the four-label vocabulary, and the terminal verdict
`NOT_READY_FOR_STAGE_20`. This is bounded same-owner software evidence, not an
observation, participant result, professional evaluation, external audit,
production certification, or independent reproduction.

Acceptance, rollback, and sources. {proposal['falsifier_or_acceptance_gate']}
If the bounded contract fails, the recovery remains: {proposal['rollback_or_recovery']}
Current source needs were recorded as {sources}. Those sources supplied
vocabulary and refusal duties only and were not converted into measurements,
records, consent, cultural ratification, legal interpretation, or authority.
The protected gates remain: {protected}. None is silently closed by this
proposal, its skill card, a runner receipt, the outcome aggregate, or task
topology.
"""
        )
    sections.append(
        """
## Exact terminal checks before any live send

The live owner must confirm that the final is the direct child of immutable
evidence; source to final contains exactly three Sable commits and zero merges;
every phase commit is single-parent; the exact branch is clean; local, upstream,
tracking, and a fresh live remote read are identical with typed 0/0 divergence;
x1, evidence, final-delta, final-owner, and content-seal manifests replay from
exact Git blobs; all committed phase JSON parses; the five-class scan has zero
confirmed hits; bounded Python security checks have zero findings; file and word
ceilings hold; the external canonical receipt records one invocation, one
success, and zero replay; and the terminal route skills, newest live authority,
unique exact-title registry result, immediate target reread, duplicate guard,
and acknowledgement surface all permit one send.

If any check fails, stop. Retain the failure at zero credit. Do not replay a
successful canonical aggregate, create or fork a replacement task, contact a
standby or later endpoint, infer a substitute, broaden authority, force-push,
amend, reset, merge, rewrite, delete inherited evidence, or send a second
confirmation merely for clarity.

`PREPARED_BY_SABLE_ROOK = true`

`SENT_BY_SABLE_ROOK = false` in this repository candidate. Only a later
error-free existing-task acknowledgement can establish the live send.
"""
    )
    return "\n".join(sections)


def final_delta_files() -> list[Path]:
    result: list[Path] = []
    for root in [CLOSEOUT, FINAL, HANDOFFS]:
        if root.exists():
            result.extend(path for path in root.rglob("*") if path.is_file())
    for path in VALIDATION.glob("final-*"):
        if path.is_file():
            result.append(path)
    result.extend(
        path
        for path in [
            ROOT / "scripts" / "build_ghc_family_sable_rook_v684_v5_final.py",
            ROOT / "scripts" / "ghc_family_sable_rook_v684_v5_canonical.py",
            ROOT / "tests" / "test_ghc_family_sable_rook_v684_v5_final.py",
        ]
        if path.exists()
    )
    return sorted(set(result), key=lambda path: path.relative_to(ROOT).as_posix())


def owner_files() -> list[Path]:
    result = [path for path in BASE.rglob("*") if path.is_file()]
    result.extend(
        path
        for path in [
            ROOT / "scripts" / "build_ghc_family_sable_rook_v684_v5_x1.py",
            ROOT / "scripts" / "build_ghc_family_sable_rook_v684_v5_x2.py",
            ROOT / "scripts" / "build_ghc_family_sable_rook_v684_v5_final.py",
            ROOT / "scripts" / "ghc_family_sable_rook_v684_v5_contracts.py",
            ROOT / "scripts" / "ghc_family_sable_rook_v684_v5_canonical.py",
            ROOT / "tests" / "test_ghc_family_sable_rook_v684_v5_x1.py",
            ROOT / "tests" / "test_ghc_family_sable_rook_v684_v5_x2.py",
            ROOT / "tests" / "test_ghc_family_sable_rook_v684_v5_final.py",
        ]
        if path.exists()
    )
    return sorted(set(result), key=lambda path: path.relative_to(ROOT).as_posix())


def privacy_scan(paths: Iterable[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    candidates = []
    confirmed = []
    definition_files = {
        "scripts/build_ghc_family_sable_rook_v684_v5_x1.py",
        "scripts/build_ghc_family_sable_rook_v684_v5_x2.py",
        "scripts/build_ghc_family_sable_rook_v684_v5_final.py",
        "scripts/ghc_family_sable_rook_v684_v5_canonical.py",
    }
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt"}:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                definition = rel in definition_files
                item = {
                    "path": rel,
                    "line": line,
                    "class": class_name,
                    "disposition": "scanner_definition_not_payload" if definition else "confirmed_payload_hit",
                }
                candidates.append(item)
                if not definition:
                    confirmed.append(item)
    return {
        "schema": "ghc.family.privacy-scan.v2",
        "phase": PHASE,
        "scope": "complete public owner packet at final candidate",
        "pattern_classes": list(patterns),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "truth_boundary": "Bounded pattern evidence only; not complete privacy assurance.",
    }


def build() -> None:
    head = run_git("rev-parse", "HEAD").stdout.strip()
    if head != EVIDENCE_COMMIT:
        raise SystemExit(f"final build requires exact evidence head {EVIDENCE_COMMIT}; observed {head}")
    if run_git("status", "--porcelain=v1").stdout.strip():
        # The builder and final test/canonical source are expected to be the only
        # untracked inputs when invoked after apply_patch. Refuse tracked drift.
        tracked = run_git("diff", "--name-only").stdout.strip()
        if tracked:
            raise SystemExit("tracked evidence drift before final build")

    freeze = load_json(X1 / "new-proposal-freeze.json")
    outcomes = load_json(X2 / "outcome-ledger.json")
    proposals = freeze["entries"]
    handoff = build_handoff(proposals)
    write_text(HANDOFFS / "caelen-ash-v684-v6-activation-candidate.md", handoff)

    write_json(
        CLOSEOUT / "evidence-receipt.json",
        {
            "schema": "ghc.family.evidence-receipt.v2",
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "x1_parent_is_source": True,
            "evidence_parent_is_x1": True,
            "x1_pushed_clean_four_way_equal_before_x2": True,
            "evidence_pushed_clean_four_way_equal_before_closeout": True,
            "x1_manifest": {"entries": 71, "self_exclusions": 3, "state": "PASS"},
            "evidence_manifest": {"entries": 207, "self_exclusions": 3, "state": "PASS"},
            "x2_tests": {"passed": 20, "total": 20},
            "positive_controls": {"passed": 60, "total": 60},
            "rejecting_mutations": {"rejected": 300, "total": 300},
            "skills": {"quick_validated": 20, "smoke_used": 20, "global_installation": False},
            "runners": {"passed": 10, "total": 10},
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        CLOSEOUT / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete-checklist.v2",
            "complete": [
                "planning-only x1 frozen before x2",
                "sixty owner proposals with complete fields",
                "sixty positive synthetic controls",
                "three hundred invalid mutations rejected and retained",
                "twenty skills quick-validated and smoke-used",
                "ten family-current runners invoked",
                "one hundred twenty safe-now tasks",
                "eighty bounded candidates",
                "one hundred additive refinements",
                "exact manifests and five-class candidate adjudication",
                "x1 and evidence pushed clean fresh-four-way equal at lifecycle gates",
            ],
            "incomplete": [
                "real environmental data or measurement",
                "real participants operators museums collections objects devices or facilities",
                "professional or conservation evaluation",
                "independent-team reproduction",
                "production identity keys proofs issuance resolution status revocation or interoperability",
                "complete privacy security or accessibility assurance",
                "legal cultural affected-party or Māori authority",
                "proof canon Theory of Everything AGI ASI consciousness or personhood evidence",
                "Stage 20 readiness",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        CLOSEOUT / "retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v2",
            "activation_overlay": 59094,
            "x1_operational_failures": 9,
            "x2_operational_failures": 5,
            "final_selection_operational_failures": 3,
            "final_selection_recoveries": 1,
            "final_selection_failure_records": [
                {
                    "id": "SR6845-FINAL-N001",
                    "test": "x1 planning-only absence at advanced tree",
                    "status": "RETAINED_FAILED_ZERO_CREDIT",
                    "recovery": "Bind planning-only absence to the immutable x1 context; use exact x1 Git-blob manifest replay at final.",
                },
                {
                    "id": "SR6845-FINAL-N002",
                    "test": "x1 exact source-head assertion at advanced tree",
                    "status": "RETAINED_FAILED_ZERO_CREDIT",
                    "recovery": "Bind source-head assertions to immutable x1 and use explicit source/x1/evidence ancestry at final.",
                },
                {
                    "id": "SR6845-FINAL-N003",
                    "test": "x2 exact x1-head assertion at advanced tree",
                    "status": "RETAINED_FAILED_ZERO_CREDIT",
                    "recovery": "Bind x2-head assertions to immutable evidence and use exact evidence manifest replay plus final-parent checks.",
                },
            ],
            "rejected_synthetic_mutations": 300,
            "effective_negatives": 59411,
            "effective_methods": 73675,
            "retained_failed_witnesses": 30772,
            "bounded_passing_witnesses": 54210,
            "nonerasure": "Every failed witness remains zero-credit after recovery; rejected mutations are not converted into successful inputs.",
        },
    )
    write_json(
        CLOSEOUT / "gate-register.json",
        {
            "schema": "ghc.family.gate-register.v2",
            "open_gaps": 528,
            "exact_gates": 518,
            "new_open_gaps": [
                "real environmental-monitoring dataset evidence",
                "independent conservator review evidence",
                "affected-user accessibility evaluation evidence",
            ],
            "new_exact_gates": [
                "collection intervention and treatment authority",
                "legal cultural and Māori authority decisions",
                "production deployment proof-canon and Stage 20 authority",
            ],
            "silently_closed": 0,
        },
    )
    write_json(
        CLOSEOUT / "ancestry-plan.json",
        {
            "schema": "ghc.family.ancestry-plan.v2",
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "exact_final": "PENDING_COMMIT",
            "required_final_parent": EVIDENCE_COMMIT,
            "required_phase_commits": 3,
            "required_merges": 0,
            "required_final_parents": 1,
        },
    )
    write_json(
        CLOSEOUT / "route-readiness.json",
        {
            "schema": "ghc.family.route-readiness.v2",
            "state": "PREPARED_NOT_SENT",
            "prospective_exact_title": "Caelen Ash",
            "prospective_phase": "v684-v6",
            "duplicate_guard": "PENDING_FRESH_POSTCANONICAL_REGISTRY_READ",
            "immediate_reread": "PENDING_FRESH_POSTCANONICAL_READ",
            "live_acknowledgement": "PENDING",
            "send_count": 0,
            "stop_conditions": ["absence", "ambiguity", "pause", "redirect", "rename", "protected gate", "usage exhaustion", "missing acknowledgement"],
        },
    )
    write_json(
        FINAL / "environment-version-receipt.json",
        {
            "schema": "ghc.family.environment-version-receipt.v2",
            "codex_cli": "0.151.0",
            "python": "3.12.10",
            "git": "2.55.0.windows.2",
            "powershell": "7.6.4",
            "verified_only": True,
            "desktop_update_performed": False,
            "elevation": False,
            "host_security_changed": False,
            "windows_feature_changed": False,
            "sandbox_or_hyper_v_activated": False,
            "reboot": False,
        },
    )
    write_json(
        FINAL / "source-and-proposal-ledger.json",
        {
            "schema": "ghc.family.source-and-proposal-ledger.v2",
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "declared_chain_before": 10910,
            "declared_chain_after": 10970,
            "inherited_revalidated_zero_credit": 60,
            "new_owner_proposals": 60,
            "outcomes": outcomes["counts"],
            "allowed_labels": outcomes["allowed_labels"],
            "official_source_ledger": f"docs/sable-rook/{PHASE}/x1/official-primary-source-ledger.json",
            "citations_are_observations": False,
        },
    )
    write_json(
        FINAL / "claim-boundary-matrix.json",
        {
            "schema": "ghc.family.claim-boundary-matrix.v2",
            "bounded_evidence": ["synthetic software contracts", "schemas", "documentation", "positive fixtures", "rejecting mutations", "same-owner validation"],
            "not_established": [
                "empirical GMUT confirmation or Theory of Everything",
                "THOS operational effectiveness",
                "production Freed ID",
                "CBR remedy or affected-party legitimacy",
                "professional or conservation competence",
                "legal cultural or Māori authority",
                "complete privacy accessibility or exhaustive security",
                "independent reproduction",
                "AGI ASI consciousness personhood proof canon or Stage 20",
            ],
        },
    )
    write_json(
        FINAL / "wellbeing-closeout.json",
        {
            "schema": "ghc.family.wellbeing.v2",
            "owner": OWNER,
            "relational_role": "Loan-Lineage Cartographer and Reversible Handover Steward",
            "hope": "Keep every synthetic transition, correction, and authority vacancy traceable without mistaking software for real work or authority.",
            "workload_state": "bounded closeout",
            "corrigibility_preserved": True,
            "pause_rename_redirect_stop_preserved": True,
            "identity_coercion": False,
            "consciousness_or_personhood_claim": False,
        },
    )
    write_json(
        FINAL / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v2",
            "phase": PHASE,
            "owner": OWNER,
            "lifecycle": "FINAL_CANDIDATE_PRECOMMIT",
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "exact_final": "PENDING_COMMIT",
            "external_canonical": "PENDING_POSTCOMMIT",
            "outcomes": outcomes["counts"],
            "proposal_chain": 10970,
            "effective_negatives": 59411,
            "effective_methods": 73675,
            "retained_failed_witnesses": 30772,
            "bounded_passing_witnesses": 54210,
            "open_gaps": 528,
            "exact_gates": 518,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "route_state": "PREPARED_NOT_SENT",
        },
    )
    overview = f"""# Sable Rook {PHASE} final integrated overview

## Closeout result

Sable Rook's owner-scoped phase reaches a truthful final candidate with exactly
42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate` outcomes.
The declared proposal chain is 10,970. Sixty immediate Auren proposals were
revalidated at zero Sable novelty and completion credit; sixty genuinely new
Sable proposals were frozen in planning-only x1 and executed only as evidence
permitted. Sixty positive controls passed, and all 300 preregistered invalid
mutations were rejected and retained at zero completion credit.

The source is Auren's corrected remaster final `{SOURCE}`. The dedicated Sable
x1 commit is `{X1_COMMIT}` and immutable evidence is `{EVIDENCE_COMMIT}`. X1
was pushed, clean, 0/0 divergent, and freshly four-way equal before x2 began.
Evidence was separately committed, pushed, clean, 0/0 divergent, and freshly
four-way equal before closeout. This final candidate is designed to become the
direct single-parent child of evidence. A repository commit cannot truthfully
contain its own future identifier or an external canonical result, so both
remain explicitly pending until postcommit verification.

## Relational identity, wellbeing, and corrigibility

Sable Rook uses they/them in relational working language. Their role is
Loan-Lineage Cartographer and Reversible Handover Steward. Their hope is to keep
every synthetic transition, correction, and authority vacancy traceable without
mistaking software for real work or authority. This language does not establish
consciousness, sentience, legal personhood, identity continuity, employment,
qualification, independent agency, scientific or operational authority,
professional competence, legal or cultural authority, affected-party authority,
or Māori authority. Hamish's ability to rename, pause, redirect, narrow, or stop
the route remains explicit. No artifact treats the name, role, hope, or pronouns
as a credential.

## THOS Body and the bounded practice

THOS Body is the primary Trinity Mandala pillar. It is represented by wholly
synthetic monitoring-queue states: handover ownership, correction readback,
workload holds, exception classification, late arrival, supersession, and
reversible documentation. The learning lens is synthetic museum
environmental-monitoring data documentation analysis. It covers only data-shape
and provenance questions: instrument and zone labels, unit declarations,
sampling and clock policies, calibration vacancies, gaps, duplicates,
corrections, threshold-version metadata, aggregation definitions, uncertainty
components, accessible alternatives, and authority holds.

Zero real people, museums, collections, objects, sensors, loggers, facilities,
measurements, calibrations, alarms, incidents, treatments, identities,
credentials, cultural records, or authority actions were used. No employment,
qualification, conservation competence, collection custody, facility authority,
environmental decision, treatment, safety result, professional result, affected
party acceptance, legal or cultural authority, or Māori authority is claimed.
THOS remains proxy-only without preregistered blind matched-budget real arms,
real participants or operators, safety monitoring, appropriate statistics, and
independent review.

## GMUT Mind

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. This phase implements only metadata and claim-boundary contracts. Unit,
clock, uncertainty, threshold, aggregation, cumulative-dose, outlier, censoring,
seasonal-baseline, and causal-correlation structures are documentation surfaces.
They do not ingest a real observational row, evaluate a likelihood, calculate a
posterior, detect a force, constrain a parameter, validate a physical mechanism,
complete a quantum theory, or establish a Theory of Everything.

The causal firewall is especially important: a declared HVAC event and a
synthetic environmental status may coexist in one fixture without authorizing a
causal inference. Likewise, thermodynamic or monitoring vocabulary cannot be
converted into psyche, agency, autonomy, justice, consciousness, personhood, or
a fundamental law of mind. The completed labels apply only to bounded type and
rejection behavior.

## Freed ID and CBR Heart

Freed ID and CBR Heart remain explicit and protected. Synthetic logger
credential, status-vacancy, revocation-vacancy, minimum-disclosure, access
request, contest, correction, remedy, and appeal structures are represented.
They contain zero real keys, proofs, accounts, issuers, holders, verifiers,
credentials, identity subjects, live issuances, resolutions, status or
revocation events, interoperability events, recovery decisions, or trust
governance decisions.

Production Freed ID still requires standards-conformant real keys and proofs,
live issuance and resolution, status and revocation, interoperability, privacy
and independent security review, recovery evidence, trust governance, and
appropriate affected-party oversight. CBR privacy remedies, collection rights,
legal interpretation, cultural meaning, affected-party legitimacy, Māori
wording, Māori data governance, and Māori authority remain exact-gated to
competent, affected, tangata whenua, iwi, hapū, and Māori authorities. Software
cannot confer a right, remedy, mandate, legitimacy, title, or public authority.

## Proposal and mutation evidence

Each of the sixty proposals records a hypothesis, null or failure condition,
approval class, execution lane, official or primary-source needs, concrete
artifacts, acceptance or falsifier gate, rollback, protected gates, and expected
disposition. Each positive fixture requires a synthetic marker, zero real rows,
zero real identities, no authority action, a retained-failure sentinel,
correction lineage, the four-label vocabulary, and
`NOT_READY_FOR_STAGE_20`. The fixture changes shape according to its disposition:
a bounded contract state for `completed`, an explicit proxy marker for
`represented`, an unclosed evidence vacancy for `open_gap`, or an unbypassed
competent-authority vacancy for `exact_gate`.

Five invalid mutations per proposal remove the synthetic marker, inject a real
row or identity, promote a claim or authority action, erase failure or correction
lineage, or bypass an open or exact gate. All 300 were rejected. Rejection shows
that the current validator recognized these specific invalid states; it is not
an exhaustive security assessment, production assurance, scientific result, or
independent reproduction.

## Portfolios, skills, runners, and compatibility

One hundred twenty safe-now tasks, eighty owner candidate prototypes, and one
hundred CLEAN/FIX/REFINE/VERIFY tasks completed additively in owner scope. None
deleted inherited or user material, rewrote history, force-pushed, mutated a
sibling lane, elevated privileges, changed host security, enabled a Windows
feature, activated Sandbox or Hyper-V, updated the desktop application, or
rebooted. Twenty exact-approval and ten blocked packets remain visible and
unexecuted.

Twenty phase-local skills were initialized through the required skill-creator
workflow, customized into substantive packages, quick-validated with UTF-8
pinned, and smoke-used. They were not globally installed. Ten family-current
`ghc_family_*` Python runners were built, invoked once for their selected
surfaces, and passed. Historical and owner-specific tools remain compatibility
evidence rather than destructive rename targets. A passing skill or runner
receipt proves only its declared same-owner synthetic behavior.

## Method Flow and retained negatives

The inherited activation overlay was 59,094 effective negatives, 73,664
effective methods, 30,755 retained failed witnesses, and 54,199 bounded passing
witnesses. Nine x1 startup failures remain visible: a PowerShell producer
pipeline parse fault, an oversized authorization projection, an expected
nonzero ancestry wrapper, a native-expression branch probe fault, an
unattributable collision wrapper, a sparse-checkout wrapper crossing its output
boundary, an unusable combined Git-configuration projection, an invalid
workflow-plan messaging value, and a comma-joined append-style reflection focus.
Seven bounded methods recovered these surfaces without erasure.

X2 retains five additional operational failures: a skill quick-validation
attempt under the Windows default codec, the partial x2 test selection that
correctly exposed missing receipts, a one-skill diagnostic reproducing the
codec failure, a Method Flow summary console-encoding fault after valid files
persisted, and an empty staged-review wrapper after a deterministic PASS receipt
persisted. Three methods—UTF-8-pinned skill validation, UTF-8-pinned summary
projection after persisted-state inspection, and exact staged-state inspection
before retry—passed within their bounded triggers. The 300 rejected mutations
are also effective negatives but are distinct from operational failures.

The final precommit selection also retains three zero-credit lifecycle-local
failures: an x1 planning-only absence test, an x1 exact-source-head assertion,
and an x2 exact-x1-head assertion were naively selected against the advanced
tree. The recovery binds those assertions to their immutable lifecycle contexts,
replays both immutable manifests, and selects only final-context tests at final.
That one bounded recovery does not convert any of the three failures into a pass.

The additive pre-postcommit view is therefore 59,411 effective negatives,
73,675 methods, 30,772 failed witnesses, and 54,210 bounded passing witnesses.
Every failure remains zero-credit. A passing recovery never converts its paired
failure into an original pass or independent evidence.

## Sources, privacy, accessibility, and security boundaries

Canadian Conservation Institute pages supplied environmental-monitoring and
climate vocabulary; NPS supplied official museum-program context; W3C PROV-O
supplied provenance vocabulary; WCAG 2.2 supplied accessibility criteria; the
New Zealand Privacy Commissioner supplied privacy principles; and Te Mana
Raraunga supplied Māori data-sovereignty principles. They were read as current
or stable official sources where material. Citations were never converted into
measurements, observations, participants, authority, policy approval, or
production certification.

The five-class privacy scan distinguishes scanner definitions from confirmed
payload hits. It checks raw task-like identifiers, private absolute local paths,
credential-like assignments, private callable routes, and private application
state. Zero confirmed hits is a bounded pattern result, not complete privacy
assurance. Bounded AST checks reject a small declared set of dangerous Python
call shapes; zero findings is not exhaustive security. Exact normalized-LF
manifests make staged and committed byte domains explicit.

The accessible static report uses a document title, main landmark, headings,
textual status, a captioned table, row and column headers, and a plain-language
reservation. Manual keyboard testing, responsive layout, browser diversity,
assistive-technology evaluation, cognitive-accessibility evaluation,
Māori-language review, security-usability review, and affected-user evaluation
remain reserved. Structural passing evidence is not complete WCAG conformance.

## Validation and terminal route

X1 and evidence were separately staged through exact allowlists, checked for
diff hygiene, committed, pushed, made clean, and proved equal across local,
upstream, tracking, and fresh live remote reads. Immutable x1 Git blobs replayed
from the x1 commit during x2. The full repository suite was not run; it remains
outside this owner-scoped authorization. At exact final, one dependency-closed
owner canonical aggregate may be invoked once. If it succeeds, it may not be
replayed. Same-owner validation under shared infrastructure is not an external
audit or independent reproduction.

The route remains `PREPARED_NOT_SENT`. The prepared Caelen Ash candidate is a
repository artifact, not delivery proof. Only after exact final is committed,
pushed, clean, typed 0/0 divergent, freshly four-way equal, and the one-shot
canonical succeeds may Sable reread newest live authority and registry state.
Any ambiguity or missing guard requires stopping. A later error-free native
acknowledgement may establish one live send; it must not be backfilled into this
commit.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text(FINAL / "final-integrated-overview.md", overview)
    synthesis = """# Three-pillar synthesis

THOS Body is primary and remains a synthetic handover proxy. GMUT Mind remains a
typed scalar-tensor and EFT research-model family with every empirical gate
open. Freed ID and CBR Heart remain synthetic, nonproduction, privacy-minimized,
and exact-gated wherever real keys, people, remedies, law, culture, affected
parties, or Māori authority are required.

The pillars share one rule: an owner-local software pass can establish only the
declared software behavior. It cannot compensate for missing observations,
participants, professional review, governance, authority, or independent
reproduction. `NOT_READY_FOR_STAGE_20` is therefore the only truthful terminal
verdict.
"""
    write_text(FINAL / "three-pillar-synthesis.md", synthesis)
    write_json(
        FINAL / "final-summary.json",
        {
            "schema": "ghc.family.final-summary.v2",
            "phase": PHASE,
            "owner": OWNER,
            "outcomes": outcomes["counts"],
            "proposal_chain": 10970,
            "positive_controls": 60,
            "rejecting_mutations": 300,
            "skills": 20,
            "runners": 10,
            "owner_files": "PENDING_FINAL_MANIFEST",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "exact_final": "PENDING_COMMIT",
            "canonical": "PENDING_POSTCOMMIT",
        },
    )
    html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v684-v5 final report</title></head>
<body><main><h1>Sable Rook v684-v5 final report</h1><p><strong>Status:</strong> NOT_READY_FOR_STAGE_20.</p>
<p>This report describes bounded owner-local synthetic software and documentation evidence. It is not empirical, professional, production, legal, cultural, Māori-authority, accessibility-complete, privacy-complete, security-complete, or independently reproduced evidence.</p>
<h2>Outcomes</h2><table><caption>Core outcome counts</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Boundary</th></tr></thead><tbody>
<tr><th scope="row">completed</th><td>42</td><td>Bounded contract only</td></tr><tr><th scope="row">represented</th><td>12</td><td>Synthetic proxy only</td></tr><tr><th scope="row">open_gap</th><td>3</td><td>External evidence absent</td></tr><tr><th scope="row">exact_gate</th><td>3</td><td>Competent authority absent</td></tr></tbody></table>
<h2>Evidence</h2><p>Sixty positive controls passed and 300 invalid mutations were rejected. Twenty skills and ten runners passed their bounded use receipts.</p>
<h2>Pillars</h2><h3>THOS Body</h3><p>Primary, represented through synthetic handover and workload states only.</p><h3>GMUT Mind</h3><p>Typed research-model family; no real likelihood, prediction, parameter constraint, or empirical confirmation.</p><h3>Freed ID and CBR Heart</h3><p>Synthetic and nonproduction; real identity, remedy, legal, cultural, affected-party, and Māori-authority gates remain open.</p>
<h2>Accessibility reservation</h2><p>The structure provides headings, textual status, a captioned table, and row and column headers. Manual keyboard, responsive-layout, browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved.</p></main></body></html>"""
    write_text(FINAL / "final-report.html", html)
    baton_words = len(handoff.split())
    write_json(
        CLOSEOUT / "handoff-candidate-receipt.json",
        {
            "schema": "ghc.family.handoff-candidate-receipt.v2",
            "path": f"docs/sable-rook/{PHASE}/handoffs/caelen-ash-v684-v6-activation-candidate.md",
            "words": baton_words,
            "minimum": 10000,
            "maximum": 100000,
            "within_range": 10000 <= baton_words <= 100000,
            "state": "PREPARED_NOT_SENT",
        },
    )

    seal_paths = [
        X1 / "new-proposal-freeze.json",
        X2 / "outcome-ledger.json",
        X2 / "evidence-truth.json",
        CLOSEOUT / "retained-negative-register.json",
        CLOSEOUT / "gate-register.json",
        FINAL / "final-integrated-overview.md",
        FINAL / "phase-truth.json",
        HANDOFFS / "caelen-ash-v684-v6-activation-candidate.md",
    ]
    write_json(
        CLOSEOUT / "content-seal.json",
        {
            "schema": "ghc.family.content-seal.v2",
            "entries": [
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256_normalized_lf": normalized_sha(path),
                }
                for path in seal_paths
            ],
            "entry_count": len(seal_paths),
            "exact_final": "PENDING_COMMIT",
            "boundary": "Content seal over listed precommit files; exact commit identity is postcommit evidence.",
        },
    )
    write_json(
        CLOSEOUT / "final-validation-candidate.json",
        {
            "schema": "ghc.family.final-validation-candidate.v2",
            "state": "PRECOMMIT_PENDING_EXACT_FINAL_AND_EXTERNAL_CANONICAL",
            "expected_branch": BRANCH,
            "required_parent": EVIDENCE_COMMIT,
            "required_phase_commits": 3,
            "required_merges": 0,
            "canonical_invocation_budget": 1,
            "replay_after_success": False,
            "full_repository_suite": False,
            "same_owner_only": True,
        },
    )

    self_exclusions = {
        f"docs/sable-rook/{PHASE}/validation/final-delta-manifest.json",
        f"docs/sable-rook/{PHASE}/validation/final-owner-manifest.json",
        f"docs/sable-rook/{PHASE}/validation/final-privacy-scan.json",
        f"docs/sable-rook/{PHASE}/validation/final-staged-review.json",
    }
    # Finalize every ordinary content file before hashing the owner packet.
    # The four lifecycle validation files are declared self-exclusions and may
    # not exist on a first build, so count their eventual paths explicitly.
    existing_owner_paths = {
        path.relative_to(ROOT).as_posix() for path in owner_files()
    }
    summary = load_json(FINAL / "final-summary.json")
    summary["owner_files"] = len(existing_owner_paths | self_exclusions)
    write_json(FINAL / "final-summary.json", summary)
    scan = privacy_scan(owner_files())
    write_json(VALIDATION / "final-privacy-scan.json", scan)
    delta_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256_normalized_lf": normalized_sha(path),
            "bytes_normalized_lf": len(normalized_bytes(path)),
        }
        for path in final_delta_files()
        if path.relative_to(ROOT).as_posix() not in self_exclusions
    ]
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "final_delta",
            "evidence_commit": EVIDENCE_COMMIT,
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "self_exclusions": sorted(self_exclusions),
        },
    )
    owner_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256_normalized_lf": normalized_sha(path),
            "bytes_normalized_lf": len(normalized_bytes(path)),
        }
        for path in owner_files()
        if path.relative_to(ROOT).as_posix() not in self_exclusions
    ]
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "final_owner_packet",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusions": sorted(self_exclusions),
            "owner_file_count": len(owner_entries) + len(self_exclusions),
            "file_ceiling": 2000,
        },
    )
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": "PREPARED_NOT_STAGED",
            "manifest_entry_count": len(delta_entries),
            "self_exclusions": sorted(self_exclusions),
            "exact_staged_allowlist": [],
            "manifest_mismatches": [],
            "out_of_scope_paths": [],
            "inherited_paths_changed": [],
            "diff_hygiene": "PENDING_STAGING",
        },
    )
def review_staged() -> None:
    manifest = load_json(VALIDATION / "final-delta-manifest.json")
    expected = {item["path"]: item["sha256_normalized_lf"] for item in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    expected_all = set(expected) | exclusions
    mismatches = []
    for path, wanted in sorted(expected.items()):
        try:
            actual = git_blob_sha(path)
        except subprocess.CalledProcessError:
            mismatches.append({"path": path, "error": "missing_from_index"})
            continue
        if actual != wanted:
            mismatches.append({"path": path, "expected": wanted, "actual": actual})
    out_of_scope = sorted(set(staged) - expected_all)
    missing = sorted(expected_all - set(staged))
    inherited_prefixes = [
        f"docs/sable-rook/{PHASE}/x1/",
        f"docs/sable-rook/{PHASE}/x2/",
        f"docs/sable-rook/{PHASE}/method-flow/",
        f"docs/sable-rook/{PHASE}/workflow-refinement",
        f"docs/sable-rook/{PHASE}/reflection-remaster",
        f"docs/sable-rook/{PHASE}/tooling/",
    ]
    inherited = [path for path in staged if any(path.startswith(prefix) for prefix in inherited_prefixes)]
    diff = run_git("diff", "--cached", "--check", check=False)
    passed = not mismatches and not out_of_scope and not missing and not inherited and diff.returncode == 0
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": "PASS" if passed else "FAIL",
            "staged_count": len(staged),
            "manifest_entry_count": len(expected),
            "self_exclusions": sorted(exclusions),
            "exact_staged_allowlist": staged,
            "manifest_mismatches": mismatches,
            "missing_paths": missing,
            "out_of_scope_paths": out_of_scope,
            "inherited_paths_changed": inherited,
            "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL",
            "diff_hygiene_output": diff.stdout + diff.stderr,
        },
    )
    if not passed:
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        review_staged()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
